#!/usr/bin/env python3
"""
Validate activity-aware JSON hints for scaffold generators.
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


def run_script(skill_root: Path, fixture: dict) -> dict:
    script_path = skill_root / "scripts" / fixture["script"]
    cmd = [sys.executable, str(script_path), *fixture["args"]]
    result = subprocess.run(cmd, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout or "scaffold command failed")
    return json.loads(result.stdout)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate SF5 scaffold generator activity hints.")
    parser.add_argument("--skill-root", default="", help="Optional skill root override")
    args = parser.parse_args()

    skill_root = Path(args.skill_root).resolve() if args.skill_root else skill_root_from_script()
    fixtures = load_json(skill_root / "references" / "vendor" / "scaffold-hint-fixtures.json")["fixtures"]

    failures = []
    for fixture in fixtures:
        payload = run_script(skill_root, fixture)
        actual_activity = payload.get("activity_hint", {}).get("activity_id")
        if actual_activity != fixture["expectedActivityId"]:
            failures.append(
                {
                    "script": fixture["script"],
                    "args": fixture["args"],
                    "expectedActivityId": fixture["expectedActivityId"],
                    "actualActivityId": actual_activity,
                }
            )
            continue
        if payload.get("kind") != fixture["expectedKind"]:
            failures.append(
                {
                    "script": fixture["script"],
                    "args": fixture["args"],
                    "expectedKind": fixture["expectedKind"],
                    "actualKind": payload.get("kind"),
                }
            )
        if "expectedRecipeType" in fixture and payload.get("recipe_type") != fixture["expectedRecipeType"]:
            failures.append(
                {
                    "script": fixture["script"],
                    "args": fixture["args"],
                    "expectedRecipeType": fixture["expectedRecipeType"],
                    "actualRecipeType": payload.get("recipe_type"),
                }
            )

    if failures:
        print(json.dumps({"ok": False, "failures": failures}, ensure_ascii=False, indent=2))
        return 1

    print(json.dumps({"ok": True, "fixtureCount": len(fixtures)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
