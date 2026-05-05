#!/usr/bin/env python3
"""
Validate working-set source references and upstream extract sources.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def skill_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate working-set source refs.")
    parser.add_argument("--skill-root", default="", help="Optional skill root override")
    args = parser.parse_args()

    skill_root = Path(args.skill_root).resolve() if args.skill_root else skill_root_from_script()
    repo_root = skill_root.parents[1]
    manifest_path = skill_root / "references" / "vendor" / "working-set.section-variants.json"
    data = load_json(manifest_path)

    failures = []
    checked = 0
    for recipe_type, sections in data.items():
        for section in sections:
            for src in section.get("source_refs", []):
                checked += 1
                if not (repo_root / src).exists():
                    failures.append(
                        {
                            "recipeType": recipe_type,
                            "sectionId": section["id"],
                            "kind": "source_ref",
                            "path": src,
                        }
                    )
            for extract in section.get("upstream_extracts", []):
                src = extract.get("source")
                if not src:
                    continue
                checked += 1
                if not (repo_root / src).exists():
                    failures.append(
                        {
                            "recipeType": recipe_type,
                            "sectionId": section["id"],
                            "kind": "upstream_extract",
                            "path": src,
                        }
                    )

    if failures:
        print(json.dumps({"ok": False, "checked": checked, "failures": failures}, ensure_ascii=False, indent=2))
        return 1

    print(json.dumps({"ok": True, "checked": checked}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
