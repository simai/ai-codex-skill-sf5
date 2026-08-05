#!/usr/bin/env python3
"""
Build a source-backed SF5 inventory from synced upstream repositories.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

GENERATED_AT = "1970-01-01T00:00:00+00:00"
UTILITY_NON_GROUP_DIRS = {"js"}

ACTIVITY_HINT = {
    "activity_id": "source-refresh",
    "required_specialists": [
        "task-goal",
        "source-sync",
        "validation-qa",
    ],
}


COMPONENT_ALIAS_GROUPS = {
    "alerts": ["alert"],
    "avatars": ["avatar"],
    "avatars-group": ["avatar"],
}

SMART_ALIAS_GROUPS = {
    "avatars": ["avatar/group"],
    "country-code": ["inputs/country-code"],
    "progress-bar": ["progress/progress-bar"],
    "progress-scale": ["progress/progress-scale"],
}


def list_dirnames(path: Path) -> list[str]:
    if not path.exists():
        return []
    return sorted(item.name for item in path.iterdir() if item.is_dir())


def load_lock(lock_path: Path) -> dict:
    if not lock_path.exists():
        return {}
    return json.loads(lock_path.read_text(encoding="utf-8"))


def repo_commit_map(lock_data: dict) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for item in lock_data.get("results", []):
        result[item["name"]] = item
    return result


def with_alias_refs(name: str, direct: list[str], aliases: dict[str, list[str]]) -> list[str]:
    merged = list(direct)
    for item in aliases.get(name, []):
        if item not in merged:
            merged.append(item)
    return merged


def build_inventory(repo_root: Path, skill_root: Path) -> dict:
    source_root = repo_root / "source/simai"
    lock_data = load_lock(skill_root / "references/vendor/source-repos.lock.json")
    repo_map = repo_commit_map(lock_data)

    shipped_components = list_dirnames(source_root / "ui/distr/component")
    shipped_smart = list_dirnames(source_root / "ui-smart/smart")
    shipped_utility_groups = [
        name
        for name in list_dirnames(source_root / "ui/distr/utility")
        if name not in UTILITY_NON_GROUP_DIRS
    ]
    source_utility_groups = list_dirnames(source_root / "ui-loader/src/utility")
    utility_example_groups = sorted(
        name
        for name in list_dirnames(source_root / "ui-play/examples")
        if name not in {"components", "smart-components"}
    )

    component_examples_root = source_root / "ui-play/examples/components"
    smart_examples_root = source_root / "ui-play/examples/smart-components"

    component_examples = {
        name: list_dirnames(component_examples_root / name)
        for name in list_dirnames(component_examples_root)
    }
    smart_examples = {
        name: list_dirnames(smart_examples_root / name)
        for name in list_dirnames(smart_examples_root)
    }
    top_level_examples = sorted(
        name
        for name in list_dirnames(source_root / "ui-play/examples")
        if name not in {"components", "smart-components"}
    )

    exact_component_example_names = sorted(component_examples)
    exact_smart_example_names = sorted(smart_examples)

    component_coverage = {}
    for name in shipped_components:
        refs = []
        if name in component_examples:
            refs.extend(f"components/{name}/{group}" for group in component_examples[name])
        if name in top_level_examples:
            refs.append(f"examples/{name}")
        refs = with_alias_refs(name, refs, COMPONENT_ALIAS_GROUPS)
        component_coverage[name] = refs

    smart_coverage = {}
    for name in shipped_smart:
        refs = []
        if name in smart_examples:
            refs.extend(f"smart-components/{name}/{group}" for group in smart_examples[name])
        refs = with_alias_refs(name, refs, SMART_ALIAS_GROUPS)
        smart_coverage[name] = refs

    components_without_examples = sorted(name for name, refs in component_coverage.items() if not refs)
    smart_without_examples = sorted(name for name, refs in smart_coverage.items() if not refs)

    return {
        "schemaVersion": 1,
        "generatedAt": GENERATED_AT,
        "repoRoot": ".",
        "sourceRoot": "source/simai",
        "repos": repo_map,
        "summary": {
            "shippedComponentCount": len(shipped_components),
            "shippedSmartCount": len(shipped_smart),
            "shippedUtilityGroupCount": len(shipped_utility_groups),
            "sourceUtilityGroupCount": len(source_utility_groups),
            "utilityExampleGroupCount": len(utility_example_groups),
            "componentExampleGroupCount": len(component_examples),
            "smartExampleGroupCount": len(smart_examples),
            "componentsWithoutExamplesCount": len(components_without_examples),
            "smartWithoutExamplesCount": len(smart_without_examples),
        },
        "components": {
            "shipped": shipped_components,
            "playExampleGroups": component_examples,
            "playExampleGroupNames": exact_component_example_names,
            "coverageRefs": component_coverage,
            "withoutPlayExamples": components_without_examples,
        },
        "smartComponents": {
            "shipped": shipped_smart,
            "playExampleGroups": smart_examples,
            "playExampleGroupNames": exact_smart_example_names,
            "coverageRefs": smart_coverage,
            "withoutPlayExamples": smart_without_examples,
        },
        "utilities": {
            "shippedGroups": shipped_utility_groups,
            "sourceGroups": source_utility_groups,
            "shippedOnlyGroups": sorted(set(shipped_utility_groups) - set(source_utility_groups)),
            "sourceOnlyGroups": sorted(set(source_utility_groups) - set(shipped_utility_groups)),
            "playExampleGroups": utility_example_groups,
        },
    }


def write_markdown(inventory: dict, out_path: Path) -> None:
    summary = inventory["summary"]
    repos = inventory.get("repos", {})
    components = inventory["components"]
    smart = inventory["smartComponents"]
    utilities = inventory["utilities"]

    lines: list[str] = []
    lines.append("# SF5 Source Inventory")
    lines.append("")
    lines.append("Generated from synced upstream repositories under `source/simai`.")
    lines.append("")
    lines.append("## Source Revisions")
    lines.append("")
    for repo_name in ["ui", "ui-loader", "ui-doc", "ui-play", "ui-smart", "ui-vscode", "ui-components"]:
        item = repos.get(repo_name)
        if not item:
            continue
        if item.get("status") == "ok":
            lines.append(f"- `{repo_name}`: `{item['branch']}` @ `{item['commit']}`")
        else:
            lines.append(f"- `{repo_name}`: `error` - {item.get('error', 'unknown error')}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Shipped components in `ui`: `{summary['shippedComponentCount']}`")
    lines.append(f"- Shipped smart-components in `ui-smart`: `{summary['shippedSmartCount']}`")
    lines.append(f"- Shipped utility groups in `ui`: `{summary['shippedUtilityGroupCount']}`")
    lines.append(f"- Utility source groups in `ui-loader`: `{summary['sourceUtilityGroupCount']}`")
    lines.append(f"- Component example groups in `ui-play`: `{summary['componentExampleGroupCount']}`")
    lines.append(f"- Smart example groups in `ui-play`: `{summary['smartExampleGroupCount']}`")
    lines.append(f"- Shipped components without direct component example groups: `{summary['componentsWithoutExamplesCount']}`")
    lines.append(f"- Shipped smart-components without direct smart example groups: `{summary['smartWithoutExamplesCount']}`")
    lines.append("")
    lines.append("## Practical Reading Order")
    lines.append("")
    lines.append("- For utility/layout work: start with the `ui-doc` atlas, validate shipped groups in `ui`, then inspect rule and state semantics in `ui-loader`.")
    lines.append("- For presentational components: start with `ui-play/examples/components`, then confirm shipping in `ui/distr/component`.")
    lines.append("- For smart-components: start with `ui-play/examples/smart-components`, then confirm runtime presence in `ui-smart/smart`.")
    lines.append("- For loader/runtime assumptions: confirm actual boot paths in `ui-play/packages/*/setup-sf.ts` and shipped paths in `ui/distr/core`.")
    lines.append("")
    lines.append("## Component Coverage")
    lines.append("")
    for name in sorted(components["coverageRefs"]):
        refs = components["coverageRefs"][name]
        if refs:
            lines.append(f"- `{name}`: `{', '.join(refs)}`")
    lines.append("")
    lines.append("Direct component-example gaps:")
    lines.append("")
    for name in components["withoutPlayExamples"][:40]:
        lines.append(f"- `{name}`")
    if len(components["withoutPlayExamples"]) > 40:
        lines.append(f"- `... +{len(components['withoutPlayExamples']) - 40} more`")
    lines.append("")
    lines.append("## Smart-Component Coverage")
    lines.append("")
    for name in sorted(smart["coverageRefs"]):
        refs = smart["coverageRefs"][name]
        if refs:
            lines.append(f"- `{name}`: `{', '.join(refs)}`")
    lines.append("")
    lines.append("Direct smart-example gaps:")
    lines.append("")
    for name in smart["withoutPlayExamples"]:
        lines.append(f"- `{name}`")
    lines.append("")
    lines.append("## Utility Example Groups")
    lines.append("")
    for name in utilities["playExampleGroups"]:
        lines.append(f"- `{name}`")
    out_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build SF5 source inventory files.")
    parser.add_argument("--repo-root", required=True, help="Repository root")
    parser.add_argument("--skill-root", required=True, help="Path to skill folder")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).expanduser().resolve()
    skill_root = Path(args.skill_root).expanduser().resolve()
    refs = skill_root / "references"
    vendor = refs / "vendor"
    refs.mkdir(parents=True, exist_ok=True)
    vendor.mkdir(parents=True, exist_ok=True)

    inventory = build_inventory(repo_root, skill_root)
    json_path = vendor / "source-inventory.json"
    md_path = refs / "source-inventory.md"
    json_path.write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(inventory, md_path)

    if args.format == "json":
        print(
            json.dumps(
                {
                    "ok": True,
                    "activity_hint": ACTIVITY_HINT,
                    "files": {
                        "inventory_json": str(json_path),
                        "inventory_md": str(md_path),
                    },
                    "summary": inventory["summary"],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(f"Wrote {json_path}")
        print(f"Wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
