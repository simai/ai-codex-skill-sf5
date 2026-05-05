#!/usr/bin/env python3
"""
Validate activity-aware JSON hints for lower-level SF5 routers.
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


def run_router(skill_root: Path, fixture: dict) -> dict:
    script_path = skill_root / "scripts" / fixture["script"]
    cmd = [sys.executable, str(script_path), "--format", "json"]
    if fixture["script"] == "recommend_page_recipe.py":
        cmd.extend(["--manifest", str(skill_root / "references" / "ui-doc-manifest.json")])
    cmd.append(fixture["query"])
    result = subprocess.run(cmd, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout or "router command failed")
    return json.loads(result.stdout)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate SF5 lower-level router activity hints.")
    parser.add_argument("--skill-root", default="", help="Optional skill root override")
    args = parser.parse_args()

    skill_root = Path(args.skill_root).resolve() if args.skill_root else skill_root_from_script()
    fixtures = load_json(skill_root / "references" / "vendor" / "router-hint-fixtures.json")["fixtures"]

    failures = []
    for fixture in fixtures:
        payload = run_router(skill_root, fixture)
        actual_activity = payload.get("activity_hint", {}).get("activity_id")
        if actual_activity != fixture["expectedActivityId"]:
            failures.append(
                {
                    "script": fixture["script"],
                    "query": fixture["query"],
                    "expectedActivityId": fixture["expectedActivityId"],
                    "actualActivityId": actual_activity,
                }
            )
            continue

        if fixture["script"] == "recommend_page_recipe.py":
            if payload.get("route") != fixture.get("expectedRoute"):
                failures.append(
                    {
                        "script": fixture["script"],
                        "query": fixture["query"],
                        "expectedRoute": fixture.get("expectedRoute"),
                        "actualRoute": payload.get("route"),
                    }
                )
        else:
            results = payload.get("results") or []
            actual_top = results[0]["id"] if results else None
            if actual_top != fixture.get("expectedTopId"):
                failures.append(
                    {
                        "script": fixture["script"],
                        "query": fixture["query"],
                        "expectedTopId": fixture.get("expectedTopId"),
                        "actualTopId": actual_top,
                    }
                )

    if failures:
        print(json.dumps({"ok": False, "failures": failures}, ensure_ascii=False, indent=2))
        return 1

    print(json.dumps({"ok": True, "fixtureCount": len(fixtures)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
