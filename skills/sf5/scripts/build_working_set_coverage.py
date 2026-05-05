#!/usr/bin/env python3
"""
Build coverage reports for SF5 working-set section and upstream support.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


EXPECTED_RECIPE_TYPES = [
    "auth",
    "landing",
    "catalog",
    "catalog-empty",
    "dashboard",
    "dashboard-table",
    "article",
    "checkout",
    "profile",
]


def skill_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_report(section_variants: dict) -> dict:
    recipes = []
    total_sections = 0
    total_with_source_refs = 0
    total_with_upstream_extracts = 0

    for recipe_type in EXPECTED_RECIPE_TYPES:
        items = section_variants.get(recipe_type, [])
        section_count = len(items)
        with_source_refs = sum(1 for item in items if item.get("source_refs"))
        with_upstream_extracts = sum(1 for item in items if item.get("upstream_extracts"))
        total_sections += section_count
        total_with_source_refs += with_source_refs
        total_with_upstream_extracts += with_upstream_extracts

        recipes.append(
            {
                "recipeType": recipe_type,
                "supported": bool(items),
                "sectionCount": section_count,
                "withSourceRefs": with_source_refs,
                "withUpstreamExtracts": with_upstream_extracts,
                "sectionIds": [item["id"] for item in items],
                "sectionsWithoutSourceRefs": [
                    item["id"] for item in items if not item.get("source_refs")
                ],
                "sectionsWithoutUpstreamExtracts": [
                    item["id"] for item in items if not item.get("upstream_extracts")
                ],
            }
        )

    unsupported = [item["recipeType"] for item in recipes if not item["supported"]]
    no_upstream = [
        item["recipeType"]
        for item in recipes
        if item["supported"] and item["withUpstreamExtracts"] == 0
    ]

    return {
        "schemaVersion": 1,
        "summary": {
            "expectedRecipeTypeCount": len(EXPECTED_RECIPE_TYPES),
            "supportedRecipeTypeCount": sum(1 for item in recipes if item["supported"]),
            "unsupportedRecipeTypes": unsupported,
            "recipeTypesWithoutUpstreamExtracts": no_upstream,
            "sectionCount": total_sections,
            "sectionsWithSourceRefs": total_with_source_refs,
            "sectionsWithUpstreamExtracts": total_with_upstream_extracts,
        },
        "recipes": recipes,
    }


def render_markdown(report: dict) -> str:
    summary = report["summary"]
    lines = [
        "# SF5 Working Set Coverage",
        "",
        "Generated from `references/vendor/working-set.section-variants.json`.",
        "",
        "## Summary",
        "",
        f"- Expected page recipe types: `{summary['expectedRecipeTypeCount']}`",
        f"- Recipe types with section coverage: `{summary['supportedRecipeTypeCount']}`",
        f"- Total section variants: `{summary['sectionCount']}`",
        f"- Sections with source refs: `{summary['sectionsWithSourceRefs']}`",
        f"- Sections with upstream extracts: `{summary['sectionsWithUpstreamExtracts']}`",
        "",
        "## Recipe Coverage",
        "",
        "| Recipe type | Supported | Sections | Source refs | Upstream extracts |",
        "| --- | --- | ---: | ---: | ---: |",
    ]
    for item in report["recipes"]:
        lines.append(
            f"| `{item['recipeType']}` | "
            f"{'yes' if item['supported'] else 'no'} | "
            f"{item['sectionCount']} | {item['withSourceRefs']} | {item['withUpstreamExtracts']} |"
        )

    lines.extend(["", "## Gaps", ""])
    if summary["unsupportedRecipeTypes"]:
        lines.append("- Recipe types without section coverage:")
        for recipe_type in summary["unsupportedRecipeTypes"]:
            lines.append(f"  - `{recipe_type}`")
    else:
        lines.append("- Every expected recipe type has section coverage.")

    if summary["recipeTypesWithoutUpstreamExtracts"]:
        lines.append("- Supported recipe types without upstream extraction support:")
        for recipe_type in summary["recipeTypesWithoutUpstreamExtracts"]:
            lines.append(f"  - `{recipe_type}`")
    else:
        lines.append("- Every supported recipe type has at least one upstream extract.")

    lines.extend(["", "## Per-Recipe Notes", ""])
    for item in report["recipes"]:
        if not item["supported"]:
            continue
        lines.append(f"### {item['recipeType']}")
        lines.append("")
        lines.append(f"- Section ids: `{', '.join(item['sectionIds'])}`")
        if item["sectionsWithoutUpstreamExtracts"]:
            lines.append(
                "- Sections without upstream extracts: "
                f"`{', '.join(item['sectionsWithoutUpstreamExtracts'])}`"
            )
        else:
            lines.append("- Every section has upstream extracts.")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build SF5 working-set coverage reports.")
    parser.add_argument("--skill-root", default="", help="Skill root path")
    args = parser.parse_args()

    skill_root = Path(args.skill_root).resolve() if args.skill_root else skill_root_from_script()
    vendor_dir = skill_root / "references" / "vendor"
    section_variants = load_json(vendor_dir / "working-set.section-variants.json")
    report = build_report(section_variants)

    (vendor_dir / "working-set.coverage.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (skill_root / "references" / "working-set-coverage.md").write_text(
        render_markdown(report),
        encoding="utf-8",
    )
    print("Wrote working-set.coverage.json and working-set-coverage.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
