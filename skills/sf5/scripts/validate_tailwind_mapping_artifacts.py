#!/usr/bin/env python3
"""
Validate Tailwind-to-SF5 Stage 1-2 mapping artifacts.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def skill_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[3]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_unique(items: list[dict[str, Any]], key: str, label: str, failures: list[str]) -> None:
    seen: set[str] = set()
    for item in items:
        value = item.get(key)
        if not isinstance(value, str) or not value:
            failures.append(f"{label} item misses string key: {key}")
            continue
        if value in seen:
            failures.append(f"{label} has duplicate {key}: {value}")
        seen.add(value)


def split_classes(class_string: str) -> list[str]:
    return [item for item in class_string.split() if item]


def expected_mapping_status(source: str, mapping_by_source: dict[str, dict[str, Any]]) -> str | None:
    mapping = mapping_by_source.get(source)
    if mapping:
        return str(mapping.get("status"))
    if ":" not in source:
        return None
    prefix, base = source.split(":", 1)
    if prefix in {"2xl", "dark", "disabled"}:
        return "blocked"
    base_mapping = mapping_by_source.get(base)
    if not base_mapping:
        return None
    if str(base_mapping.get("status")) in {"deferred", "blocked"}:
        return str(base_mapping.get("status"))
    return "prefixed"


def smart_codes_from_registry(registry: dict[str, Any]) -> set[str]:
    codes: set[str] = set()
    for item in registry.get("items", []):
        regex = str(item.get("regex", ""))
        marker = 'sf-code="'
        if marker in regex:
            codes.add(regex.split(marker, 1)[1].split('"', 1)[0])
    return codes


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Tailwind-to-SF5 mapping artifacts.")
    parser.add_argument("--skill-root", default="", help="Optional skill root override")
    args = parser.parse_args()

    skill_root = Path(args.skill_root).resolve() if args.skill_root else skill_root_from_script()
    vendor_root = skill_root / "references" / "vendor"

    groups = load_json(vendor_root / "tailwind-to-sf5.class-groups.json")
    utility_map = load_json(vendor_root / "tailwind-to-sf5.utility-map.json")
    fixtures = load_json(vendor_root / "tailwind-to-sf5.fixtures.json")
    component_hints = load_json(vendor_root / "tailwind-to-sf5.component-hints.json")
    component_recipes = load_json(vendor_root / "tailwind-to-sf5.component-recipes.json")
    component_renderers = load_json(vendor_root / "tailwind-to-sf5.component-renderers.json")
    smart_hints = load_json(vendor_root / "tailwind-to-sf5.smart-hints.json")
    smart_registry = load_json(vendor_root / "registries" / "smart-codes.json")
    catalog = load_json(skill_root / "references" / "vendor" / "source" / "catalog-lite.sf-only.json")
    repo_root = repo_root_from_script()
    catalog_classes = set(catalog.get("classes", []))
    known_smart_codes = smart_codes_from_registry(smart_registry)

    failures: list[str] = []

    if groups.get("schemaVersion") != 1:
        failures.append("class groups schemaVersion must be 1")
    if utility_map.get("schemaVersion") != 1:
        failures.append("utility map schemaVersion must be 1")
    if fixtures.get("schemaVersion") != 1:
        failures.append("fixtures schemaVersion must be 1")
    if component_hints.get("schemaVersion") != 1:
        failures.append("component hints schemaVersion must be 1")
    if component_recipes.get("schemaVersion") != 1:
        failures.append("component recipes schemaVersion must be 1")
    if component_renderers.get("schemaVersion") != 1:
        failures.append("component renderers schemaVersion must be 1")
    if smart_hints.get("schemaVersion") != 1:
        failures.append("smart hints schemaVersion must be 1")

    families = groups.get("families", [])
    mappings = utility_map.get("mappings", [])
    fixture_items = fixtures.get("fixtures", [])
    html_fixture_items = fixtures.get("htmlFixtures", [])
    hint_items = component_hints.get("hints", [])
    recipe_items = component_recipes.get("recipes", [])
    renderer_items = component_renderers.get("renderers", [])
    smart_hint_items = smart_hints.get("hints", [])

    if len(families) < 8:
        failures.append("class groups must cover at least 8 families")
    if len([item for item in mappings if item.get("status") == "mapped"]) < 20:
        failures.append("utility map must include at least 20 mapped classes")
    if len(fixture_items) < 4:
        failures.append("fixtures must include at least 4 examples")
    if len(html_fixture_items) < 4:
        failures.append("HTML fixtures must include at least 4 examples")
    if len(hint_items) < 4:
        failures.append("component hints must include at least 4 examples")
    if len(recipe_items) < 4:
        failures.append("component recipes must include at least 4 examples")
    if len(renderer_items) < 5:
        failures.append("component renderers must include at least 5 examples")
    if len(smart_hint_items) < 4:
        failures.append("smart hints must include at least 4 examples")

    validate_unique(families, "id", "class groups", failures)
    validate_unique(mappings, "sourceClass", "utility map", failures)
    validate_unique(fixture_items, "id", "fixtures", failures)
    validate_unique(html_fixture_items, "id", "HTML fixtures", failures)
    validate_unique(hint_items, "id", "component hints", failures)
    validate_unique(recipe_items, "id", "component recipes", failures)
    validate_unique(renderer_items, "id", "component renderers", failures)
    validate_unique(smart_hint_items, "id", "smart hints", failures)

    family_ids = {item.get("id") for item in families}
    mapping_by_source = {item.get("sourceClass"): item for item in mappings}

    allowed_statuses = {"mapped", "deferred", "blocked"}
    for item in mappings:
        source = item.get("sourceClass")
        family = item.get("family")
        status = item.get("status")
        targets = item.get("targetClasses")

        if family not in family_ids:
            failures.append(f"mapping {source} references unknown family: {family}")
        if status not in allowed_statuses:
            failures.append(f"mapping {source} has invalid status: {status}")
        if not isinstance(targets, list):
            failures.append(f"mapping {source} targetClasses must be a list")
            continue
        if status == "mapped" and not targets:
            failures.append(f"mapped class {source} must have at least one target class")
        if status != "mapped" and targets:
            failures.append(f"{status} class {source} must not define target classes")
        for target in targets:
            if target not in catalog_classes:
                failures.append(f"mapping {source} targets unknown SF5 class: {target}")

    required_fixture_ids = {
        "utility-card-basic",
        "utility-form-row",
        "utility-toolbar",
        "behavior-negative",
        "responsive-state-basic",
        "component-toolbar-hint",
    }
    actual_fixture_ids = {item.get("id") for item in fixture_items}
    missing_fixture_ids = sorted(required_fixture_ids - actual_fixture_ids)
    if missing_fixture_ids:
        failures.append(f"missing required fixtures: {', '.join(missing_fixture_ids)}")

    for item in fixture_items:
        fixture_id = item.get("id")
        class_string = item.get("classString", "")
        if not isinstance(class_string, str) or not class_string.strip():
            failures.append(f"fixture {fixture_id} misses classString")
            continue

        source_classes = set(split_classes(class_string))
        for family in item.get("expectedFamilies", []):
            if family not in family_ids:
                failures.append(f"fixture {fixture_id} references unknown family: {family}")

        for source in item.get("expectedMappedClasses", []):
            if source not in source_classes:
                failures.append(f"fixture {fixture_id} expects mapped class not present in classString: {source}")
            else:
                status = expected_mapping_status(source, mapping_by_source)
                if status not in {"mapped", "prefixed"}:
                    failures.append(f"fixture {fixture_id} expects mapped class with status {status}: {source}")

        for source in item.get("expectedDeferredClasses", []):
            if source not in source_classes:
                failures.append(f"fixture {fixture_id} expects deferred class not present in classString: {source}")
            else:
                status = expected_mapping_status(source, mapping_by_source)
                if status not in {"deferred", "prefixed"}:
                    failures.append(f"fixture {fixture_id} expects deferred class with status {status}: {source}")

        for source in item.get("expectedBlockedClasses", []):
            if source not in source_classes:
                failures.append(f"fixture {fixture_id} expects blocked class not present in classString: {source}")
            else:
                status = expected_mapping_status(source, mapping_by_source)
                if status != "blocked":
                    failures.append(f"fixture {fixture_id} expects blocked class with status {status}: {source}")

        expected_known = set(item.get("expectedMappedClasses", []))
        expected_known.update(item.get("expectedDeferredClasses", []))
        expected_known.update(item.get("expectedBlockedClasses", []))
        expected_known.update(item.get("expectedUnmappedClasses", []))
        missing_expectations = sorted(source_classes - expected_known)
        if missing_expectations:
            failures.append(
                f"fixture {fixture_id} has classes without expected bucket: {', '.join(missing_expectations)}"
            )

    required_html_fixture_ids = {
        "auth-form-application-ui-like",
        "card-application-ui-like",
        "data-table-application-ui-like",
        "toolbar-application-ui-like",
    }
    actual_html_fixture_ids = {item.get("id") for item in html_fixture_items}
    missing_html_fixture_ids = sorted(required_html_fixture_ids - actual_html_fixture_ids)
    if missing_html_fixture_ids:
        failures.append(f"missing required HTML fixtures: {', '.join(missing_html_fixture_ids)}")

    for item in html_fixture_items:
        fixture_id = item.get("id")
        if not item.get("html"):
            failures.append(f"HTML fixture {fixture_id} misses html")
        if "expectedComponentHints" not in item:
            failures.append(f"HTML fixture {fixture_id} misses expectedComponentHints")
        if "expectedComponentRecipes" not in item:
            failures.append(f"HTML fixture {fixture_id} misses expectedComponentRecipes")
        if "expectedSmartHints" not in item:
            failures.append(f"HTML fixture {fixture_id} misses expectedSmartHints")
        if "expectedComponentRenderCandidates" not in item:
            failures.append(f"HTML fixture {fixture_id} misses expectedComponentRenderCandidates")

    required_hint_ids = {"auth-form", "card", "data-table", "toolbar"}
    actual_hint_ids = {item.get("id") for item in hint_items}
    missing_hint_ids = sorted(required_hint_ids - actual_hint_ids)
    if missing_hint_ids:
        failures.append(f"missing required component hints: {', '.join(missing_hint_ids)}")

    for hint in hint_items:
        hint_id = hint.get("id")
        if not hint.get("classSignals") and not hint.get("htmlSignals"):
            failures.append(f"component hint {hint_id} must define classSignals or htmlSignals")
        if not hint.get("sf5Strategy"):
            failures.append(f"component hint {hint_id} misses sf5Strategy")
        if not hint.get("sourceRefs"):
            failures.append(f"component hint {hint_id} misses sourceRefs")

    recipe_by_hint = {item.get("hintId"): item for item in recipe_items}
    for hint_id in required_hint_ids:
        if hint_id not in recipe_by_hint:
            failures.append(f"missing component recipe for hint: {hint_id}")

    for recipe in recipe_items:
        recipe_id = recipe.get("id")
        hint_id = recipe.get("hintId")
        if hint_id not in actual_hint_ids:
            failures.append(f"component recipe {recipe_id} references unknown hintId: {hint_id}")
        route = recipe.get("route") or {}
        if not route.get("scenario") or not route.get("recipeType") or not route.get("scaffoldCommand"):
            failures.append(f"component recipe {recipe_id} must define route scenario, recipeType, and scaffoldCommand")
        if not recipe.get("conversionSteps"):
            failures.append(f"component recipe {recipe_id} misses conversionSteps")
        if not recipe.get("starterMarkup"):
            failures.append(f"component recipe {recipe_id} misses starterMarkup")
        if not recipe.get("sourceRefs"):
            failures.append(f"component recipe {recipe_id} misses sourceRefs")
        for rel_ref in recipe.get("sourceRefs", []):
            if not (skill_root / rel_ref).exists():
                failures.append(f"component recipe {recipe_id} references missing sourceRef: {rel_ref}")

    required_renderer_ids = {"button", "dropdown", "input", "pagination", "modal"}
    actual_renderer_ids = {item.get("id") for item in renderer_items}
    missing_renderer_ids = sorted(required_renderer_ids - actual_renderer_ids)
    if missing_renderer_ids:
        failures.append(f"missing required component renderers: {', '.join(missing_renderer_ids)}")

    for renderer in renderer_items:
        renderer_id = renderer.get("id")
        if not renderer.get("componentId"):
            failures.append(f"component renderer {renderer_id} misses componentId")
        if not renderer.get("classSignals") and not renderer.get("htmlSignals"):
            failures.append(f"component renderer {renderer_id} must define classSignals or htmlSignals")
        if not renderer.get("starterMarkup"):
            failures.append(f"component renderer {renderer_id} misses starterMarkup")
        if not renderer.get("manualChecks"):
            failures.append(f"component renderer {renderer_id} misses manualChecks")
        for rel_ref in renderer.get("sourceRefs", []):
            if rel_ref.startswith("source/"):
                ref_path = repo_root / rel_ref
            else:
                ref_path = skill_root / rel_ref
            if not ref_path.exists():
                failures.append(f"component renderer {renderer_id} references missing sourceRef: {rel_ref}")

    required_smart_ids = {"smart-search", "smart-select", "smart-pagination", "smart-table", "smart-cards"}
    actual_smart_ids = {item.get("id") for item in smart_hint_items}
    missing_smart_ids = sorted(required_smart_ids - actual_smart_ids)
    if missing_smart_ids:
        failures.append(f"missing required smart hints: {', '.join(missing_smart_ids)}")

    for hint in smart_hint_items:
        hint_id = hint.get("id")
        sf_code = hint.get("sfCode")
        if sf_code not in known_smart_codes:
            failures.append(f"smart hint {hint_id} references unknown sfCode: {sf_code}")
        if not hint.get("classSignals") and not hint.get("htmlSignals"):
            failures.append(f"smart hint {hint_id} must define classSignals or htmlSignals")
        if not hint.get("strategy"):
            failures.append(f"smart hint {hint_id} misses strategy")
        for rel_ref in hint.get("sourceRefs", []):
            if not (skill_root / rel_ref).exists():
                failures.append(f"smart hint {hint_id} references missing sourceRef: {rel_ref}")

    result: dict[str, Any] = {
        "ok": not failures,
        "familyCount": len(families),
        "mappingCount": len(mappings),
        "fixtureCount": len(fixture_items),
        "htmlFixtureCount": len(html_fixture_items),
        "componentHintCount": len(hint_items),
        "componentRecipeCount": len(recipe_items),
        "componentRendererCount": len(renderer_items),
        "smartHintCount": len(smart_hint_items),
    }
    if failures:
        result["failures"] = failures
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
