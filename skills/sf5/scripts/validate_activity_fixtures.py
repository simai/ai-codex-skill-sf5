#!/usr/bin/env python3
"""
Validate SF5 activity routing against a fixed fixture set.
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


def run_activity(script_path: Path, query: str) -> dict:
    result = subprocess.run(
        [sys.executable, str(script_path), query, "--format", "json"],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout or "activity command failed")
    return json.loads(result.stdout)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate SF5 activity fixtures.")
    parser.add_argument("--skill-root", default="", help="Optional skill root override")
    args = parser.parse_args()

    skill_root = Path(args.skill_root).resolve() if args.skill_root else skill_root_from_script()
    fixtures = load_json(skill_root / "references" / "vendor" / "activity-fixtures.json")["fixtures"]
    script_path = skill_root / "scripts" / "recommend_sf5_activity.py"

    failures = []
    for item in fixtures:
        payload = run_activity(script_path, item["query"])
        actual = payload.get("activity_id")
        actual_specialists = payload.get("required_specialists") or []
        actual_gate_rules = payload.get("gate_rules") or []
        actual_packs = payload.get("knowledge_packs") or []
        actual_roles = {
            item["name"]: item["role"]
            for item in payload.get("specialist_roles", [])
            if item.get("required")
        }
        if actual != item["expectedActivityId"]:
            failures.append(
                {
                    "query": item["query"],
                    "expectedActivityId": item["expectedActivityId"],
                    "actualActivityId": actual,
                }
            )
            continue
        missing_specialists = [s for s in item.get("requiredSpecialists", []) if s not in actual_specialists]
        if missing_specialists:
            failures.append(
                {
                    "query": item["query"],
                    "activityId": actual,
                    "missingRequiredSpecialists": missing_specialists,
                }
            )
        missing_gate_rules = [g for g in item.get("requiredGateRules", []) if g not in actual_gate_rules]
        if missing_gate_rules:
            failures.append(
                {
                    "query": item["query"],
                    "activityId": actual,
                    "missingGateRules": missing_gate_rules,
                }
            )
        missing_packs = [p for p in item.get("requiredKnowledgePacks", []) if p not in actual_packs]
        if missing_packs:
            failures.append(
                {
                    "query": item["query"],
                    "activityId": actual,
                    "missingKnowledgePacks": missing_packs,
                }
            )
        for specialist, expected_role in item.get("requiredRoles", {}).items():
            if actual_roles.get(specialist) != expected_role:
                failures.append(
                    {
                        "query": item["query"],
                        "activityId": actual,
                        "specialist": specialist,
                        "expectedRole": expected_role,
                        "actualRole": actual_roles.get(specialist),
                    }
                )
        workflow = payload.get("workflow") or []
        for snippet in item.get("requiredWorkflowSnippets", []):
            if not any(snippet.lower() in step.lower() for step in workflow):
                failures.append(
                    {
                        "query": item["query"],
                        "activityId": actual,
                        "missingWorkflowSnippet": snippet,
                    }
                )
        outputs = payload.get("required_outputs") or []
        missing_outputs = [o for o in item.get("requiredOutputs", []) if o not in outputs]
        if missing_outputs:
            failures.append(
                {
                    "query": item["query"],
                    "activityId": actual,
                    "missingRequiredOutputs": missing_outputs,
                }
            )

    if failures:
        print(json.dumps({"ok": False, "failures": failures}, ensure_ascii=False, indent=2))
        return 1

    print(json.dumps({"ok": True, "fixtureCount": len(fixtures)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
