#!/usr/bin/env python3
"""
Migrate legacy SF5 recipe classes to vendor catalog naming.

This script rewrites class tokens only inside HTML code fences in markdown files.
"""

from __future__ import annotations

import argparse
import glob
import re
from collections import Counter
from pathlib import Path
from typing import Counter as CounterType
from typing import Dict, List, Tuple


LEGACY_CLASS_MAP: Dict[str, str] = {
    "py-2": "p-y-2",
    "py-3": "p-y-3",
    "py-4": "p-y-4",
    "pb-4": "p-bottom-4",
    "pt-1": "p-top-1",
    "mt-0": "m-top-0",
    "mt-1": "m-top-1",
    "mt-2": "m-top-2",
    "mt-3": "m-top-3",
    "justify-main-between": "content-main-between",
    "justify-main-center": "content-main-center",
    "txt-role-title": "title-3",
    "txt-role-subtitle": "title-5",
    "txt-role-body": "text-medium",
    "txt-role-caption": "text-small",
    "link": "link-underline-none",
    "min-h-7": "h-g7",
}


def map_class_token(token: str) -> str:
    parts = token.split(":")
    base = parts[-1]
    mapped = LEGACY_CLASS_MAP.get(base, base)
    parts[-1] = mapped
    return ":".join(parts)


def rewrite_class_attrs(html: str) -> Tuple[str, CounterType[str]]:
    changes: CounterType[str] = Counter()

    def replace_class_attr(match: re.Match) -> str:
        quote = match.group(1)
        blob = match.group(2)
        raw_tokens = blob.replace("\n", " ").split()
        mapped_tokens: List[str] = []

        for raw in raw_tokens:
            mapped = map_class_token(raw)
            if mapped != raw:
                changes[f"{raw} -> {mapped}"] += 1
            mapped_tokens.append(mapped)

        return f'class={quote}{" ".join(mapped_tokens)}{quote}'

    rewritten = re.sub(
        r'class\s*=\s*(["\'])(.*?)\1',
        replace_class_attr,
        html,
        flags=re.DOTALL,
    )
    return rewritten, changes


def rewrite_markdown(md_text: str) -> Tuple[str, CounterType[str]]:
    total_changes: CounterType[str] = Counter()

    def replace_html_fence(match: re.Match) -> str:
        html = match.group(1)
        rewritten_html, changes = rewrite_class_attrs(html)
        total_changes.update(changes)
        return "```html\n" + rewritten_html.strip() + "\n```"

    rewritten = re.sub(
        r"```html\s*(.*?)\s*```",
        replace_html_fence,
        md_text,
        flags=re.DOTALL,
    )
    return rewritten, total_changes


def process_file(path: Path, write: bool) -> Tuple[bool, CounterType[str]]:
    original = path.read_text(encoding="utf-8")
    rewritten, changes = rewrite_markdown(original)
    changed = rewritten != original
    if changed and write:
        path.write_text(rewritten, encoding="utf-8")
    return changed, changes


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Migrate legacy SF5 recipe classes to vendor naming."
    )
    parser.add_argument(
        "--glob",
        default="",
        help="File glob (default: references/page-recipe-*.md)",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write changes in place (default: dry-run)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero if any legacy classes are found",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    recipes_glob = args.glob or str(root / "references" / "page-recipe-*.md")
    files = [Path(p) for p in sorted(glob.glob(recipes_glob))]

    if not files:
        print("No files matched.")
        return 0

    total = Counter()
    files_with_changes = 0

    for path in files:
        changed, changes = process_file(path, write=args.write)
        total.update(changes)
        if changed:
            files_with_changes += 1
            mode = "updated" if args.write else "would update"
            print(f"{mode}: {path.name}")

    print(f"Files scanned: {len(files)}")
    print(f"Files with class changes: {files_with_changes}")
    print(f"Legacy token replacements: {sum(total.values())}")
    for key, count in sorted(total.items()):
        print(f"  - {key}: {count}")

    if args.strict and total:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
