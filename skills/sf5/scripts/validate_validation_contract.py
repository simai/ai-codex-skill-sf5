#!/usr/bin/env python3
"""
Validate that the SF5 validation layer has the expected scripts and fixture density.
"""

from __future__ import annotations

import json
from pathlib import Path


def skill_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    skill_root = skill_root_from_script()
    scripts_dir = skill_root / "scripts"
    vendor_dir = skill_root / "references" / "vendor"

    required_scripts = [
        "validate_route_fixtures.py",
        "validate_activity_fixtures.py",
        "validate_e2e_fixtures.py",
        "validate_working_set_sources.py",
        "validate_page_recipes.py",
        "validate_sf5_html_files.py",
        "validate_activity_manifests.py",
        "validate_scaffold_hints.py",
        "validate_source_refresh_contract.py",
        "validate_source_refresh_gate.py",
        "validate_tailwind_conversion_contract.py",
        "validate_validation_contract.py",
        "validate_validation_hardening_gate.py",
        "validate_router_hints.py",
    ]
    required_fixtures = [
        "route-fixtures.json",
        "activity-fixtures.json",
        "e2e-fixtures.json",
        "router-hint-fixtures.json",
        "scaffold-hint-fixtures.json",
    ]

    failures: list[str] = []
    for file_name in required_scripts:
        if not (scripts_dir / file_name).exists():
            failures.append(f"Missing validator script: scripts/{file_name}")
    for file_name in required_fixtures:
        if not (vendor_dir / file_name).exists():
            failures.append(f"Missing fixture file: references/vendor/{file_name}")

    route_fixtures = load_json(vendor_dir / "route-fixtures.json")
    activity_fixtures = load_json(vendor_dir / "activity-fixtures.json")
    e2e_fixtures = load_json(vendor_dir / "e2e-fixtures.json")
    router_hint_fixtures = load_json(vendor_dir / "router-hint-fixtures.json")
    scaffold_hint_fixtures = load_json(vendor_dir / "scaffold-hint-fixtures.json")

    route_count = len(route_fixtures.get("fixtures", []))
    activity_count = len(activity_fixtures.get("fixtures", []))
    e2e_count = len(e2e_fixtures.get("fixtures", []))
    router_hint_count = len(router_hint_fixtures.get("fixtures", []))
    scaffold_hint_count = len(scaffold_hint_fixtures.get("fixtures", []))

    if route_count < 10:
        failures.append(f"Route fixture density too low: {route_count} < 10")
    if activity_count < 5:
        failures.append(f"Activity fixture density too low: {activity_count} < 5")
    if e2e_count < 5:
        failures.append(f"E2E fixture density too low: {e2e_count} < 5")
    if router_hint_count < 4:
        failures.append(f"Router-hint fixture density too low: {router_hint_count} < 4")
    if scaffold_hint_count < 4:
        failures.append(f"Scaffold-hint fixture density too low: {scaffold_hint_count} < 4")

    if not all("expectedActivityId" in item for item in route_fixtures.get("fixtures", [])):
        failures.append("Some route fixtures miss expectedActivityId")
    if not all(item.get("forbiddenScenarioIds") for item in route_fixtures.get("fixtures", [])):
        failures.append("Some route fixtures miss forbiddenScenarioIds")
    if not all(item.get("requiredRoles") for item in activity_fixtures.get("fixtures", [])):
        failures.append("Some activity fixtures miss requiredRoles")
    if not all(item.get("requiredWorkflowSnippets") for item in activity_fixtures.get("fixtures", [])):
        failures.append("Some activity fixtures miss requiredWorkflowSnippets")
    if not all(item.get("requiredOutputs") for item in activity_fixtures.get("fixtures", [])):
        failures.append("Some activity fixtures miss requiredOutputs")
    if not all(item.get("requiredFiles") for item in e2e_fixtures.get("fixtures", [])):
        failures.append("Some e2e fixtures miss requiredFiles")
    if not all("expectedActivityId" in item for item in e2e_fixtures.get("fixtures", [])):
        failures.append("Some e2e fixtures miss expectedActivityId")
    if not all(item.get("expectedActivityId") for item in router_hint_fixtures.get("fixtures", [])):
        failures.append("Some router-hint fixtures miss expectedActivityId")
    if not all(item.get("expectedActivityId") for item in scaffold_hint_fixtures.get("fixtures", [])):
        failures.append("Some scaffold-hint fixtures miss expectedActivityId")

    payload = {
        "ok": not failures,
        "routeFixtureCount": route_count,
        "activityFixtureCount": activity_count,
        "e2eFixtureCount": e2e_count,
        "routerHintFixtureCount": router_hint_count,
        "scaffoldHintFixtureCount": scaffold_hint_count,
    }
    if failures:
        payload["failures"] = failures
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 1

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
