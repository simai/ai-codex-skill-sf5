#!/usr/bin/env python3
"""
Validate top-level SF5 routing against a fixed fixture set.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def skill_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def run_route(script_path: Path, query: str) -> dict:
    result = subprocess.run(
        [sys.executable, str(script_path), query, "--format", "json"],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout or "route command failed")
    return json.loads(result.stdout)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate SF5 route fixtures.")
    parser.add_argument("--skill-root", default="", help="Optional skill root override")
    args = parser.parse_args()

    skill_root = Path(args.skill_root).resolve() if args.skill_root else skill_root_from_script()
    fixtures_path = skill_root / "references" / "vendor" / "route-fixtures.json"
    route_script = skill_root / "scripts" / "recommend_sf5_route.py"
    fixtures = load_json(fixtures_path)["fixtures"]

    failures = []
    for item in fixtures:
        payload = run_route(route_script, item["query"])
        actual_scenario = payload.get("scenario_id")
        actual_recipe = payload.get("recipe_type")
        actual_activity_payload = payload.get("activity", {})
        actual_activity = actual_activity_payload.get("activity_id")
        forbidden = item.get("forbiddenScenarioIds", [])
        if (
            actual_scenario != item["expectedScenarioId"]
            or actual_recipe != item["expectedRecipeType"]
            or actual_activity != item.get("expectedActivityId")
            or actual_scenario in forbidden
        ):
            failures.append(
                {
                    "query": item["query"],
                    "expectedScenarioId": item["expectedScenarioId"],
                    "actualScenarioId": actual_scenario,
                    "expectedRecipeType": item["expectedRecipeType"],
                    "actualRecipeType": actual_recipe,
                    "expectedActivityId": item.get("expectedActivityId"),
                    "actualActivityId": actual_activity,
                    "forbiddenScenarioIds": forbidden,
                }
            )
            continue

        actual_specialists = actual_activity_payload.get("required_specialists") or []
        actual_gate_rules = actual_activity_payload.get("gate_rules") or []
        actual_packs = actual_activity_payload.get("knowledge_packs") or []
        actual_roles = {
            role_item["name"]: role_item["role"]
            for role_item in actual_activity_payload.get("specialist_roles", [])
            if role_item.get("required")
        }
        missing_specialists = [
            name for name in item.get("requiredActivitySpecialists", []) if name not in actual_specialists
        ]
        if missing_specialists:
            failures.append(
                {
                    "query": item["query"],
                    "activityId": actual_activity,
                    "missingActivitySpecialists": missing_specialists,
                }
            )
        missing_gate_rules = [
            gate_rule for gate_rule in item.get("requiredActivityGateRules", []) if gate_rule not in actual_gate_rules
        ]
        if missing_gate_rules:
            failures.append(
                {
                    "query": item["query"],
                    "activityId": actual_activity,
                    "missingActivityGateRules": missing_gate_rules,
                }
            )
        missing_packs = [
            pack for pack in item.get("requiredActivityKnowledgePacks", []) if pack not in actual_packs
        ]
        if missing_packs:
            failures.append(
                {
                    "query": item["query"],
                    "activityId": actual_activity,
                    "missingActivityKnowledgePacks": missing_packs,
                }
            )
        for specialist, expected_role in item.get("requiredActivityRoles", {}).items():
            if actual_roles.get(specialist) != expected_role:
                failures.append(
                    {
                        "query": item["query"],
                        "activityId": actual_activity,
                        "specialist": specialist,
                        "expectedActivityRole": expected_role,
                        "actualActivityRole": actual_roles.get(specialist),
                    }
                )
        workflow = actual_activity_payload.get("workflow") or []
        for snippet in item.get("requiredActivityWorkflowSnippets", []):
            if not any(snippet.lower() in step.lower() for step in workflow):
                failures.append(
                    {
                        "query": item["query"],
                        "activityId": actual_activity,
                        "missingActivityWorkflowSnippet": snippet,
                    }
                )

    if failures:
        print(json.dumps({"ok": False, "failures": failures}, ensure_ascii=False, indent=2))
        return 1

    print(
        json.dumps(
            {
                "ok": True,
                "fixtureCount": len(fixtures),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
