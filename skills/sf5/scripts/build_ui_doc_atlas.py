#!/usr/bin/env python3
"""
Build an exhaustive SF5 UI documentation atlas from a docs root.

Outputs:
- references/ui-doc-manifest.json
- references/ui-doc-full-map.md
- references/ui-doc-utility-atlas.md
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Tuple


def parse_frontmatter(text: str) -> Tuple[Dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text

    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return {}, text

    raw, body = parts
    meta: Dict[str, str] = {}
    for line in raw.splitlines()[1:]:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip('"').strip("'")
    return meta, body


def first_h1(body: str) -> str:
    for line in body.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def all_h2(body: str) -> List[str]:
    result: List[str] = []
    for line in body.splitlines():
        line = line.strip()
        if line.startswith("## "):
            result.append(line[3:].strip())
    return result


def normalize_class_token(token: str) -> str:
    token = token.strip()
    token = token.replace("`", "")
    token = token.replace("…", "")
    token = token.replace(" ", "")
    token = token.rstrip(".,;:|")
    if not token.startswith("."):
        return ""
    # guard against broken fragments like ".4}" or ".-"
    if len(token) < 3:
        return ""
    if not re.match(r"^\.[A-Za-z0-9_-]", token):
        return ""
    if token.endswith("-"):
        return ""
    return token


def extract_class_tokens_from_table_rows(body: str) -> List[str]:
    tokens = set()
    row_re = re.compile(r"^\|(.+)\|$")
    # match utility-like class patterns including placeholders: .radius-{size}
    class_re = re.compile(r"\.[A-Za-z0-9][A-Za-z0-9:_/\-]*(?:-\{[A-Za-z0-9_/\-, ]+\})?")

    for line in body.splitlines():
        m = row_re.match(line.strip())
        if not m:
            continue
        # first cell usually contains class names in these docs
        cells = [c.strip() for c in m.group(1).split("|")]
        if not cells:
            continue
        first = cells[0]
        if "класс" in first.lower() or "class" in first.lower():
            continue
        for cm in class_re.finditer(first.replace("`", "")):
            token = normalize_class_token(cm.group(0))
            if token:
                tokens.add(token)
    return sorted(tokens)


def extract_example_class_tokens(body: str) -> List[str]:
    tokens = set()
    # class="..." and class='...'
    for m in re.finditer(r'class\s*=\s*(["\'])(.*?)\1', body, flags=re.DOTALL):
        class_blob = m.group(2).replace("\n", " ")
        for raw in class_blob.split():
            token = raw.strip().strip(",.;:")
            if not token:
                continue
            # keep prefixed classes as-is (e.g. md:grid-col-3)
            if token in {"...", ".."}:
                continue
            if re.search(r"[<>]", token):
                continue
            tokens.add(token)
    return sorted(tokens)


def build_records(docs_root: Path) -> List[Dict]:
    records: List[Dict] = []
    for md_file in sorted(docs_root.rglob("*.md")):
        rel = md_file.relative_to(docs_root).as_posix()
        text = md_file.read_text(encoding="utf-8-sig")
        meta, body = parse_frontmatter(text)

        top = rel.split("/", 1)[0] if "/" in rel else "root"
        utility_group = ""
        if rel.startswith("utilities/"):
            parts = rel.split("/")
            if len(parts) > 2:
                utility_group = parts[1]
            else:
                utility_group = "_root"

        title = first_h1(body) or meta.get("title", "") or md_file.stem
        description = meta.get("description", "")
        headings = all_h2(body)
        class_tokens = extract_class_tokens_from_table_rows(body)
        example_class_tokens = extract_example_class_tokens(body)

        records.append(
            {
                "path": rel,
                "top": top,
                "utility_group": utility_group,
                "title": title,
                "description": description,
                "h2": headings,
                "has_playground": "sf-playground" in body or "play.simai.io/embed" in body,
                "class_tokens": class_tokens,
                "class_token_count": len(class_tokens),
                "example_class_tokens": example_class_tokens,
                "example_class_token_count": len(example_class_tokens),
            }
        )
    return records


def write_manifest(records: List[Dict], out_file: Path) -> None:
    out_file.write_text(
        json.dumps(records, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def write_full_map(records: List[Dict], out_file: Path) -> None:
    top_counts = Counter(r["top"] for r in records)
    util_counts = Counter(r["utility_group"] for r in records if r["top"] == "utilities")
    by_top: Dict[str, List[Dict]] = defaultdict(list)
    for r in records:
        by_top[r["top"]].append(r)

    lines: List[str] = []
    lines.append("# SF5 UI Docs Full Map")
    lines.append("")
    lines.append("Generated from:")
    lines.append("`/Users/rim/Downloads/ui-doc-main (2)/ui-doc-main/source/docs/ru`")
    lines.append("")
    lines.append("## Contents")
    lines.append("")
    lines.append("- Summary")
    lines.append("- Top-Level Sections")
    lines.append("- Utility Groups")
    lines.append("- Full File List By Section")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Total markdown files: `{len(records)}`")
    lines.append(
        f"- Utility files: `{sum(1 for r in records if r['top'] == 'utilities')}`"
    )
    lines.append(
        f"- Files with playground embeds: `{sum(1 for r in records if r['has_playground'])}`"
    )
    lines.append("")
    lines.append("## Top-Level Sections")
    lines.append("")
    for section, count in sorted(top_counts.items()):
        lines.append(f"- `{section}`: `{count}`")
    lines.append("")
    lines.append("## Utility Groups")
    lines.append("")
    for group, count in sorted(util_counts.items()):
        lines.append(f"- `utilities/{group}`: `{count}`")
    lines.append("")
    lines.append("## Full File List By Section")
    lines.append("")

    for section in sorted(by_top):
        lines.append(f"### `{section}`")
        lines.append("")
        for r in sorted(by_top[section], key=lambda x: x["path"]):
            title = r["title"].replace("`", "")
            lines.append(f"- `{r['path']}` - {title}")
        lines.append("")

    out_file.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_utility_atlas(records: List[Dict], out_file: Path) -> None:
    util_records = [r for r in records if r["top"] == "utilities"]
    groups: Dict[str, List[Dict]] = defaultdict(list)
    for r in util_records:
        groups[r["utility_group"]].append(r)

    lines: List[str] = []
    lines.append("# SF5 Utility Atlas")
    lines.append("")
    lines.append("Generated from utility pages in the SF5 docs snapshot.")
    lines.append("")
    lines.append("## Contents")
    lines.append("")
    lines.append("- Summary")
    lines.append("- Utility Groups")
    lines.append("- Group Details")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Utility files: `{len(util_records)}`")
    lines.append(
        f"- Files with extracted class tokens: `{sum(1 for r in util_records if r['class_token_count'] > 0)}`"
    )
    lines.append(
        f"- Total extracted class tokens (non-unique across files): `{sum(r['class_token_count'] for r in util_records)}`"
    )
    lines.append("")
    lines.append("## Utility Groups")
    lines.append("")
    for group in sorted(groups):
        lines.append(f"- `{group}` (`{len(groups[group])}` files)")
    lines.append("")
    lines.append("## Group Details")
    lines.append("")

    for group in sorted(groups):
        lines.append(f"### `{group}`")
        lines.append("")
        for r in sorted(groups[group], key=lambda x: x["path"]):
            lines.append(f"- `{r['path']}` - {r['title']}")
            if r["class_tokens"]:
                preview = ", ".join(r["class_tokens"][:12])
                lines.append(f"  - class tokens: {preview}")
                if len(r["class_tokens"]) > 12:
                    lines.append(f"  - more tokens: `+{len(r['class_tokens']) - 12}`")
            if r["has_playground"]:
                lines.append("  - playground: `yes`")
        lines.append("")

    out_file.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build SF5 UI docs atlas files.")
    parser.add_argument("--docs-root", required=True, help="Path to docs/ru root")
    parser.add_argument(
        "--skill-root",
        required=True,
        help="Path to skill folder (contains references/)",
    )
    args = parser.parse_args()

    docs_root = Path(args.docs_root).expanduser().resolve()
    skill_root = Path(args.skill_root).expanduser().resolve()
    refs = skill_root / "references"
    refs.mkdir(parents=True, exist_ok=True)

    records = build_records(docs_root)
    write_manifest(records, refs / "ui-doc-manifest.json")
    write_full_map(records, refs / "ui-doc-full-map.md")
    write_utility_atlas(records, refs / "ui-doc-utility-atlas.md")

    print(f"Processed {len(records)} markdown files.")
    print(f"Wrote {(refs / 'ui-doc-manifest.json').as_posix()}")
    print(f"Wrote {(refs / 'ui-doc-full-map.md').as_posix()}")
    print(f"Wrote {(refs / 'ui-doc-utility-atlas.md').as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
