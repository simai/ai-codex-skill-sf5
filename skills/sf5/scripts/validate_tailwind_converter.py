#!/usr/bin/env python3
"""
Validate the Tailwind-to-SF5 converter against fixture expectations.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def skill_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def run_converter(skill_root: Path, class_string: str) -> dict[str, Any]:
    result = subprocess.run(
        [
            sys.executable,
            str(skill_root / "scripts" / "convert_tailwind_to_sf5.py"),
            class_string,
            "--format",
            "json",
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout or "converter command failed")
    return json.loads(result.stdout)


def run_converter_html(skill_root: Path, html: str) -> dict[str, Any]:
    result = subprocess.run(
        [
            sys.executable,
            str(skill_root / "scripts" / "convert_tailwind_to_sf5.py"),
            "--html-string",
            html,
            "--format",
            "json",
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout or "converter html command failed")
    return json.loads(result.stdout)


def run_recipe_render(skill_root: Path, html: str, recipe_id: str = "") -> str:
    command = [
        sys.executable,
        str(skill_root / "scripts" / "convert_tailwind_to_sf5.py"),
        "--html-string",
        html,
        "--render-recipe",
    ]
    if recipe_id:
        command.append(recipe_id)
    command.extend(["--format", "text"])
    result = subprocess.run(
        command,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout or "recipe render command failed")
    return result.stdout.strip()


def run_recipe_render_json(skill_root: Path, html: str, recipe_id: str = "") -> dict[str, Any]:
    command = [
        sys.executable,
        str(skill_root / "scripts" / "convert_tailwind_to_sf5.py"),
        "--html-string",
        html,
        "--render-recipe",
    ]
    if recipe_id:
        command.append(recipe_id)
    command.extend(["--format", "json"])
    result = subprocess.run(
        command,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout or "recipe render json command failed")
    return json.loads(result.stdout)


def run_component_render(skill_root: Path, html: str, recipe_id: str = "") -> str:
    command = [
        sys.executable,
        str(skill_root / "scripts" / "convert_tailwind_to_sf5.py"),
        "--html-string",
        html,
        "--render-component",
    ]
    if recipe_id:
        command.append(recipe_id)
    command.extend(["--format", "text"])
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout or "component render command failed")
    return result.stdout.strip()


def run_component_render_json(
    skill_root: Path,
    html: str,
    recipe_id: str = "",
    runtime_promotion_status: str = "unknown",
    runtime_visual_delta: float | None = None,
    max_runtime_visual_delta: float = 1.0,
) -> dict[str, Any]:
    command = [
        sys.executable,
        str(skill_root / "scripts" / "convert_tailwind_to_sf5.py"),
        "--html-string",
        html,
        "--render-component",
    ]
    if recipe_id:
        command.append(recipe_id)
    command.extend(
        [
            "--runtime-promotion-status",
            runtime_promotion_status,
            "--max-runtime-visual-delta",
            str(max_runtime_visual_delta),
            "--format",
            "json",
        ]
    )
    if runtime_visual_delta is not None:
        command.extend(["--runtime-visual-delta", str(runtime_visual_delta)])
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout or "component render json command failed")
    return json.loads(result.stdout)


def run_smart_render_json(skill_root: Path, html: str, smart_selector: str = "") -> dict[str, Any]:
    command = [
        sys.executable,
        str(skill_root / "scripts" / "convert_tailwind_to_sf5.py"),
        "--html-string",
        html,
        "--render-smart",
    ]
    if smart_selector:
        command.append(smart_selector)
    command.extend(["--format", "json"])
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout or "smart render json command failed")
    return json.loads(result.stdout)


def run_sf5_html_validator(skill_root: Path, path: Path) -> dict[str, Any]:
    result = subprocess.run(
        [
            sys.executable,
            str(skill_root / "scripts" / "validate_sf5_html_files.py"),
            "--strict",
            "--catalog-strict",
            str(path),
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return {"ok": False, "stdout": result.stdout, "stderr": result.stderr}
    return {"ok": True, "stdout": result.stdout}


def run_sf5_html_validator_many(skill_root: Path, paths: list[Path]) -> dict[str, Any]:
    result = subprocess.run(
        [
            sys.executable,
            str(skill_root / "scripts" / "validate_sf5_html_files.py"),
            "--strict",
            "--catalog-strict",
            *[str(path) for path in paths],
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return {"ok": False, "stdout": result.stdout, "stderr": result.stderr}
    return {"ok": True, "stdout": result.stdout}


def run_inventory(skill_root: Path, path: Path) -> dict[str, Any]:
    result = subprocess.run(
        [
            sys.executable,
            str(skill_root / "scripts" / "convert_tailwind_to_sf5.py"),
            "--inventory",
            str(path),
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout or "inventory command failed")
    return json.loads(result.stdout)


def run_residue_gate(skill_root: Path, html: str) -> dict[str, Any]:
    result = subprocess.run(
        [
            sys.executable,
            str(skill_root / "scripts" / "convert_tailwind_to_sf5.py"),
            "--html-string",
            html,
            "--gate-tailwind-residue",
            "--format",
            "json",
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout or "residue gate command failed")
    return json.loads(result.stdout)


def source_classes(items: list[dict[str, Any]]) -> list[str]:
    return [str(item.get("sourceClass", "")) for item in items]


def ids(items: list[dict[str, Any]]) -> list[str]:
    return [str(item.get("id", "")) for item in items]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Tailwind-to-SF5 converter fixtures.")
    parser.add_argument("--skill-root", default="", help="Optional skill root override")
    args = parser.parse_args()

    skill_root = Path(args.skill_root).resolve() if args.skill_root else skill_root_from_script()
    fixture_data = load_json(skill_root / "references" / "vendor" / "tailwind-to-sf5.fixtures.json")
    fixtures = fixture_data["fixtures"]
    html_fixtures = fixture_data.get("htmlFixtures", [])
    promotion_gate_fixtures = fixture_data.get("promotionGateFixtures", [])

    failures: list[dict[str, Any]] = []
    for fixture in fixtures:
        payload = run_converter(skill_root, fixture["classString"])
        report = payload["report"]

        if payload.get("convertedClassString") != fixture.get("expectedConvertedClassString"):
            failures.append(
                {
                    "fixtureId": fixture["id"],
                    "expectedConvertedClassString": fixture.get("expectedConvertedClassString"),
                    "actualConvertedClassString": payload.get("convertedClassString"),
                }
            )
        if payload.get("targetClasses") != fixture.get("expectedTargetClasses"):
            failures.append(
                {
                    "fixtureId": fixture["id"],
                    "expectedTargetClasses": fixture.get("expectedTargetClasses"),
                    "actualTargetClasses": payload.get("targetClasses"),
                }
            )

        expected_buckets = {
            "mapped": fixture.get("expectedMappedClasses", []),
            "deferred": fixture.get("expectedDeferredClasses", []),
            "blocked": fixture.get("expectedBlockedClasses", []),
            "unmapped": fixture.get("expectedUnmappedClasses", []),
        }
        for bucket, expected in expected_buckets.items():
            actual = source_classes(report.get(bucket, []))
            if actual != expected:
                failures.append(
                    {
                        "fixtureId": fixture["id"],
                        "bucket": bucket,
                        "expected": expected,
                        "actual": actual,
                    }
                )

        expected_hints = fixture.get("expectedComponentHints")
        if expected_hints is not None:
            actual_hints = [str(item.get("id", "")) for item in report.get("componentHints", [])]
            if actual_hints != expected_hints:
                failures.append(
                    {
                        "fixtureId": fixture["id"],
                        "bucket": "componentHints",
                        "expected": expected_hints,
                        "actual": actual_hints,
                    }
                )
        validation_hints = report.get("validationHints", {})
        expects_blockers = bool(fixture.get("expectedBlockedClasses"))
        if not expects_blockers and not validation_hints.get("strictCatalogReady", False):
            failures.append(
                {
                    "fixtureId": fixture["id"],
                    "bucket": "validationHints",
                    "expected": "strictCatalogReady true for fixture converted classes",
                    "actual": validation_hints,
                }
            )

    for fixture in html_fixtures:
        payload = run_converter_html(skill_root, fixture["html"])
        report = payload["report"]

        actual_component_hints = ids(report.get("componentHints", []))
        expected_component_hints = fixture.get("expectedComponentHints", [])
        if actual_component_hints != expected_component_hints:
            failures.append(
                {
                    "fixtureId": fixture["id"],
                    "bucket": "htmlComponentHints",
                    "expected": expected_component_hints,
                    "actual": actual_component_hints,
                }
            )

        actual_component_recipes = ids(report.get("componentRecipes", []))
        expected_component_recipes = fixture.get("expectedComponentRecipes", [])
        if actual_component_recipes != expected_component_recipes:
            failures.append(
                {
                    "fixtureId": fixture["id"],
                    "bucket": "htmlComponentRecipes",
                    "expected": expected_component_recipes,
                    "actual": actual_component_recipes,
                }
            )

        actual_smart_hints = ids(report.get("smartHints", []))
        expected_smart_hints = fixture.get("expectedSmartHints", [])
        if actual_smart_hints != expected_smart_hints:
            failures.append(
                {
                    "fixtureId": fixture["id"],
                    "bucket": "htmlSmartHints",
                    "expected": expected_smart_hints,
                    "actual": actual_smart_hints,
                }
            )

        actual_component_render_candidates = ids(report.get("componentRenderCandidates", []))
        expected_component_render_candidates = fixture.get("expectedComponentRenderCandidates", [])
        if actual_component_render_candidates != expected_component_render_candidates:
            failures.append(
                {
                    "fixtureId": fixture["id"],
                    "bucket": "htmlComponentRenderCandidates",
                    "expected": expected_component_render_candidates,
                    "actual": actual_component_render_candidates,
                }
            )

        validation_hints = report.get("validationHints", {})
        if not validation_hints.get("strictCatalogReady", False):
            failures.append(
                {
                    "fixtureId": fixture["id"],
                    "bucket": "htmlValidationHints",
                    "expected": "strictCatalogReady true for converted HTML draft",
                    "actual": validation_hints,
                }
            )

    html_payload = run_converter_html(
        skill_root,
        '<section class="flex flex-row justify-between gap-2"><div class="block p-4 bg-white"></div></section>',
    )
    expected_html = '<section class="flex flex-row content-main-between gap-2"><div class="block p-4 bg-surface-1"></div></section>'
    if html_payload.get("convertedHtml") != expected_html:
        failures.append(
            {
                "fixtureId": "html-smoke",
                "expectedConvertedHtml": expected_html,
                "actualConvertedHtml": html_payload.get("convertedHtml"),
            }
        )

    html_hint_payload = run_converter_html(
        skill_root,
        '<nav class="flex flex-row items-center justify-between gap-2 w-full"><button>Filter</button></nav>',
    )
    actual_html_hints = [str(item.get("id", "")) for item in html_hint_payload["report"].get("componentHints", [])]
    if "toolbar" not in actual_html_hints:
        failures.append(
            {
                "fixtureId": "html-component-hint-smoke",
                "expectedHint": "toolbar",
                "actualHints": actual_html_hints,
            }
        )
    actual_html_recipes = [str(item.get("id", "")) for item in html_hint_payload["report"].get("componentRecipes", [])]
    if "toolbar" not in actual_html_recipes:
        failures.append(
            {
                "fixtureId": "html-component-recipe-smoke",
                "expectedRecipe": "toolbar",
                "actualRecipes": actual_html_recipes,
            }
        )

    first_toolbar_recipe = next(
        (item for item in html_hint_payload["report"].get("componentRecipes", []) if item.get("id") == "toolbar"),
        {},
    )
    if not first_toolbar_recipe.get("starterMarkup") or not first_toolbar_recipe.get("conversionSteps"):
        failures.append(
            {
                "fixtureId": "html-component-recipe-detail-smoke",
                "missing": "starterMarkup or conversionSteps",
                "actualRecipe": first_toolbar_recipe,
            }
        )

    rendered_toolbar = run_recipe_render(
        skill_root,
        '<nav class="flex flex-row items-center justify-between gap-2 w-full"><button>Filter</button></nav>',
    )
    if "sf-button sf-button--default sf-button--primary sf-button--size-1" not in rendered_toolbar:
        failures.append(
            {
                "fixtureId": "recipe-render-text-smoke",
                "expectedSnippet": "sf-button sf-button--default sf-button--primary sf-button--size-1",
                "actual": rendered_toolbar,
            }
        )

    rendered_toolbar_component = run_component_render(
        skill_root,
        '<nav class="flex flex-row items-center justify-between gap-2 w-full"><button>Filter</button></nav>',
        "toolbar",
    )
    if "sf-button sf-button--default sf-button--primary sf-button--size-1" not in rendered_toolbar_component:
        failures.append(
            {
                "fixtureId": "component-render-text-smoke",
                "expectedSnippet": "sf-button sf-button--default sf-button--primary sf-button--size-1",
                "actual": rendered_toolbar_component,
            }
        )

    rendered_table_json = run_recipe_render_json(
        skill_root,
        '<table class="w-full text-left border"><thead><tr><th>Title</th></tr></thead><tbody><tr><td>Value</td></tr></tbody></table>',
        "data-table",
    )
    if not rendered_table_json.get("recipeRender", {}).get("ok"):
        failures.append(
            {
                "fixtureId": "recipe-render-json-smoke",
                "expected": "ok recipeRender",
                "actual": rendered_table_json.get("recipeRender"),
            }
        )
    elif rendered_table_json["recipeRender"]["selectedRecipe"].get("id") != "data-table":
        failures.append(
            {
                "fixtureId": "recipe-render-json-selection-smoke",
                "expectedRecipe": "data-table",
                "actualRecipe": rendered_table_json["recipeRender"]["selectedRecipe"].get("id"),
            }
        )

    rendered_smart_json = run_smart_render_json(
        skill_root,
        '<table class="w-full text-left border"><thead><tr><th>Title</th></tr></thead><tbody><tr><td>Value</td></tr></tbody></table>',
        "table",
    )
    smart_render = rendered_smart_json.get("smartRender", {})
    if not smart_render.get("ok") or smart_render.get("sfCode") != "table":
        failures.append(
            {
                "fixtureId": "smart-render-json-smoke",
                "expected": "ok smartRender for sf-code table",
                "actual": smart_render,
            }
        )
    elif 'sf-code="table"' not in smart_render.get("starterMarkup", ""):
        failures.append(
            {
                "fixtureId": "smart-render-markup-smoke",
                "expectedSnippet": 'sf-code="table"',
                "actual": smart_render.get("starterMarkup", ""),
            }
        )
    if smart_render.get("sfCode") == "table":
        if smart_render.get("sourceBacked") is not True:
            failures.append(
                {
                    "fixtureId": "smart-render-table-source-backed-smoke",
                    "expected": "sf-code table is backed by the current ui-smart table runtime",
                    "actual": smart_render,
                }
            )
        if smart_render.get("promotionStatus") != "candidate":
            failures.append(
                {
                    "fixtureId": "smart-render-table-promotion-smoke",
                    "expected": "candidate",
                    "actual": smart_render.get("promotionStatus"),
                }
            )

    sys.path.insert(0, str(skill_root / "scripts"))
    from convert_tailwind_to_sf5 import build_component_promotion_gate  # pylint: disable=import-outside-toplevel

    for fixture in promotion_gate_fixtures:
        if fixture.get("directCandidate"):
            gate = build_component_promotion_gate(
                fixture["directCandidate"],
                fixture.get("runtimePromotionStatus", "unknown"),
                fixture.get("runtimeVisualDelta"),
                fixture.get("maxRuntimeVisualDelta", 1.0),
            )
        else:
            payload = run_component_render_json(
                skill_root,
                fixture["html"],
                fixture.get("componentSelector", ""),
                fixture.get("runtimePromotionStatus", "unknown"),
                fixture.get("runtimeVisualDelta"),
                fixture.get("maxRuntimeVisualDelta", 1.0),
            )
            gate = payload.get("componentRender", {}).get("promotionGate", {})
        if gate.get("ok") != fixture.get("expectedGateOk"):
            failures.append(
                {
                    "fixtureId": fixture["id"],
                    "bucket": "promotionGateOk",
                    "expected": fixture.get("expectedGateOk"),
                    "actual": gate,
                }
            )
        if gate.get("status") != fixture.get("expectedGateStatus"):
            failures.append(
                {
                    "fixtureId": fixture["id"],
                    "bucket": "promotionGateStatus",
                    "expected": fixture.get("expectedGateStatus"),
                    "actual": gate,
                }
            )
        expected_failure_contains = fixture.get("expectedFailureContains", [])
        actual_failure_text = "\n".join(str(item) for item in gate.get("failures", []))
        for expected_text in expected_failure_contains:
            if expected_text not in actual_failure_text:
                failures.append(
                    {
                        "fixtureId": fixture["id"],
                        "bucket": "promotionGateFailures",
                        "expectedContains": expected_text,
                        "actual": gate.get("failures", []),
                    }
                )

    e2e_files = [
        skill_root / "references" / "vendor" / "tailwind-to-sf5.e2e-auth.sf5.html",
        skill_root / "references" / "vendor" / "tailwind-to-sf5.e2e-card.sf5.html",
        skill_root / "references" / "vendor" / "tailwind-to-sf5.e2e-table.sf5.html",
        skill_root / "references" / "vendor" / "tailwind-to-sf5.e2e-toolbar.sf5.html",
    ]
    e2e_validation = run_sf5_html_validator_many(skill_root, e2e_files)
    if not e2e_validation.get("ok"):
        failures.append(
            {
                "fixtureId": "e2e-sf5-validation",
                "expected": "strict catalog validation passed",
                "actual": e2e_validation,
            }
        )

    residue_gate = run_residue_gate(
        skill_root,
        '<nav class="flex flex-row justify-between gap-2"><button class="font-semibold">Filter</button></nav>',
    )
    if not residue_gate.get("tailwindResidueGate", {}).get("ok"):
        failures.append(
            {
                "fixtureId": "tailwind-residue-gate-clean-smoke",
                "expected": "residue gate ok",
                "actual": residue_gate.get("tailwindResidueGate"),
            }
        )

    inventory = run_inventory(skill_root, skill_root / "references" / "vendor" / "tailwind-to-sf5.inventory-source.html")
    if inventory.get("filesWithTailwindSignals", 0) < 1 or not inventory.get("topClasses"):
        failures.append(
            {
                "fixtureId": "tailwind-inventory-smoke",
                "expected": "inventory finds Tailwind signals",
                "actual": inventory,
            }
        )

    result: dict[str, Any] = {
        "ok": not failures,
        "fixtureCount": len(fixtures),
        "htmlFixtureCount": len(html_fixtures),
        "promotionGateFixtureCount": len(promotion_gate_fixtures),
        "e2eFixtureCount": len(e2e_files),
        "htmlSmoke": True,
    }
    if failures:
        result["failures"] = failures
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
