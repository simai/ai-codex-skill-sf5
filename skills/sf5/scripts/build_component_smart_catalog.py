#!/usr/bin/env python3
"""
Build a source-backed SF5 component and smart-component usage catalog.

The catalog is intentionally derived from ignored source mirrors under
source/simai so it can be refreshed after upstream repository syncs.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


CLASS_ATTR_RE = re.compile(r"""(?<![:@.\w-])class\s*=\s*["']([^"']+)["']""", re.DOTALL)
SF_CODE_RE = re.compile(r"""sf-code\s*=\s*["']([^"']+)["']""", re.IGNORECASE)
CUSTOM_ELEMENT_RE = re.compile(r"<(sf-[a-zA-Z0-9-]+)\b")


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[3]


def skill_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def list_child_dirs(path: Path) -> list[str]:
    if not path.exists():
        return []
    return sorted(item.name for item in path.iterdir() if item.is_dir() and not item.name.startswith("."))


def html_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(root.rglob("*.html"))


def class_tokens_from_text(text: str) -> list[str]:
    tokens: list[str] = []
    for match in CLASS_ATTR_RE.finditer(text):
        tokens.extend(item for item in re.split(r"\s+", match.group(1).strip()) if item)
    return tokens


def sf_prefixed_classes(tokens: list[str]) -> list[str]:
    return sorted({token for token in tokens if token.startswith("sf-")})


def class_prefix(token: str) -> str:
    if "--" in token:
        return token.split("--", 1)[0]
    return token


class AttributeParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.attrs: Counter[str] = Counter()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.startswith("sf-"):
            for name, _value in attrs:
                self.attrs[name] += 1


def example_group_paths(root: Path, group: str) -> list[Path]:
    group_root = root / group
    return html_files(group_root)


def coverage_ref_files(source_root: Path, surface: str, ref_value: str) -> list[Path]:
    examples_root = source_root / "ui-play" / "examples"
    surface_root = "components" if surface == "component" else "smart-components"
    candidates = [
        examples_root / ref_value,
        examples_root / surface_root / ref_value,
    ]
    files: list[Path] = []
    for candidate in candidates:
        files.extend(html_files(candidate))
    return sorted(set(files))


def runtime_flags(path: Path) -> dict[str, bool]:
    return {
        "hasCss": (path / "css").exists(),
        "hasJs": (path / "js").exists(),
        "hasJson": (path / "json").exists(),
        "hasTemplate": (path / "template").exists(),
    }


def sample_paths(paths: list[Path], root: Path, limit: int = 4) -> list[str]:
    return [rel(path, root) for path in paths[:limit]]


def build_component_entry(
    name: str,
    repo_root: Path,
    source_root: Path,
    inventory: dict[str, Any],
) -> dict[str, Any]:
    runtime_path = source_root / "ui" / "distr" / "component" / name
    play_root = source_root / "ui-play" / "examples" / "components"
    coverage_refs = inventory.get("components", {}).get("coverageRefs", {}).get(name, [])
    example_files: list[Path] = []
    for ref in coverage_refs:
        example_files.extend(coverage_ref_files(source_root, "component", ref))
    if not example_files:
        example_files.extend(example_group_paths(play_root, name))

    combined = "\n".join(read_text(path) for path in example_files[:4])
    classes = sf_prefixed_classes(class_tokens_from_text(combined))
    prefixes = sorted({class_prefix(token) for token in classes})
    states = sorted(token for token in classes if token in {"active", "disabled", "loading", "selected", "open"})

    return {
        "id": name,
        "surface": "component",
        "shipped": runtime_path.exists(),
        "runtimePath": rel(runtime_path, repo_root) if runtime_path.exists() else "",
        "runtime": runtime_flags(runtime_path),
        "playExamples": sample_paths(example_files, repo_root),
        "coverageRefs": coverage_refs,
        "contract": {
            "rootClassCandidates": prefixes[:12],
            "modifierClassExamples": classes[:24],
            "stateClassExamples": states,
        },
        "sourceRefs": [rel(runtime_path, repo_root)] if runtime_path.exists() else [],
    }


def build_smart_entry(
    name: str,
    repo_root: Path,
    source_root: Path,
    inventory: dict[str, Any],
) -> dict[str, Any]:
    runtime_path = source_root / "ui-smart" / "smart" / name
    play_root = source_root / "ui-play" / "examples" / "smart-components"
    coverage_refs = inventory.get("smartComponents", {}).get("coverageRefs", {}).get(name, [])
    example_files: list[Path] = []
    for ref in coverage_refs:
        example_files.extend(coverage_ref_files(source_root, "smart-component", ref))
    if not example_files:
        example_files.extend(example_group_paths(play_root, name))

    combined = "\n".join(read_text(path) for path in example_files[:4])
    parser = AttributeParser()
    parser.feed(combined)
    custom_elements = sorted(set(CUSTOM_ELEMENT_RE.findall(combined)))
    sf_codes = sorted(set(SF_CODE_RE.findall(combined)))

    return {
        "id": name,
        "surface": "smart-component",
        "shipped": runtime_path.exists(),
        "runtimePath": rel(runtime_path, repo_root) if runtime_path.exists() else "",
        "runtime": runtime_flags(runtime_path),
        "playExamples": sample_paths(example_files, repo_root),
        "coverageRefs": coverage_refs,
        "contract": {
            "customElements": custom_elements,
            "sfCodeValues": sf_codes,
            "attributeExamples": sorted(parser.attrs.keys())[:30],
            "attributeFrequency": dict(parser.attrs.most_common(30)),
        },
        "sourceRefs": [rel(runtime_path, repo_root)] if runtime_path.exists() else [],
    }


def write_catalog_markdown(path: Path, catalog: dict[str, Any]) -> None:
    components = catalog["components"]
    smart = catalog["smartComponents"]
    lines = [
        "# SF5 Component And Smart-Component Catalog",
        "",
        "Generated from local source mirrors. Refresh with:",
        "",
        "```bash",
        "python3 skills/sf5/scripts/sync_source_repos.py",
        "python3 skills/sf5/scripts/build_component_smart_catalog.py",
        "```",
        "",
        "## Summary",
        "",
        f"- Components: {catalog['summary']['componentCount']}",
        f"- Components with examples: {catalog['summary']['componentsWithExamples']}",
        f"- Smart-components: {catalog['summary']['smartComponentCount']}",
        f"- Smart-components with examples: {catalog['summary']['smartComponentsWithExamples']}",
        "",
        "## Use In Conversion",
        "",
        "- Prefer entries with `shipped=true` and at least one `playExamples` path.",
        "- Use component entries for presentational replacement of Tailwind blocks.",
        "- Use smart-component entries only when the source behavior requires state, events, data loading, or widget lifecycle.",
        "- Treat `contract.customElements`, `contract.sfCodeValues`, and `contract.attributeExamples` as source-backed hints, not as a complete API spec.",
        "",
        "## High-Value Components",
        "",
    ]
    for item in components:
        if not item["playExamples"]:
            continue
        roots = ", ".join(item["contract"]["rootClassCandidates"][:5]) or "-"
        lines.append(
            f"- `{item['id']}`: roots `{roots}`; examples: {', '.join(item['playExamples'][:2])}"
        )

    lines.extend(["", "## High-Value Smart-Components", ""])
    for item in smart:
        if not item["playExamples"]:
            continue
        elements = ", ".join(item["contract"]["customElements"][:5]) or "-"
        sf_codes = ", ".join(item["contract"]["sfCodeValues"][:5]) or "-"
        lines.append(
            f"- `{item['id']}`: elements `{elements}`; sf-code `{sf_codes}`; examples: {', '.join(item['playExamples'][:2])}"
        )

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build SF5 component/smart-component catalog.")
    parser.add_argument("--repo-root", default=str(repo_root_from_script()))
    parser.add_argument("--skill-root", default=str(skill_root_from_script()))
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    skill_root = Path(args.skill_root).resolve()
    source_root = repo_root / "source" / "simai"
    inventory_path = skill_root / "references" / "vendor" / "source-inventory.json"
    inventory = load_json(inventory_path)
    smart_codes_path = skill_root / "references" / "vendor" / "registries" / "smart-codes.json"
    smart_codes = load_json(smart_codes_path)

    component_names = sorted(inventory.get("components", {}).get("shipped", []))
    smart_names = sorted(inventory.get("smartComponents", {}).get("shipped", []))
    components = [build_component_entry(name, repo_root, source_root, inventory) for name in component_names]
    smart_components = [build_smart_entry(name, repo_root, source_root, inventory) for name in smart_names]

    catalog = {
        "schemaVersion": 1,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "sourceInventory": rel(inventory_path, repo_root),
        "smartCodeRegistry": rel(smart_codes_path, repo_root),
        "summary": {
            "componentCount": len(components),
            "componentsWithExamples": sum(1 for item in components if item["playExamples"]),
            "smartComponentCount": len(smart_components),
            "smartComponentsWithExamples": sum(1 for item in smart_components if item["playExamples"]),
        },
        "components": components,
        "smartComponents": smart_components,
        "sfCodeRegistry": smart_codes.get("items", []),
    }

    json_path = skill_root / "references" / "vendor" / "component-smart-catalog.json"
    md_path = skill_root / "references" / "component-smart-catalog.md"
    json_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_catalog_markdown(md_path, catalog)

    if args.format == "json":
        print(json.dumps({"ok": True, "json": rel(json_path, repo_root), "markdown": rel(md_path, repo_root), "summary": catalog["summary"]}, ensure_ascii=False, indent=2))
    else:
        print(f"Wrote {json_path}")
        print(f"Wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
