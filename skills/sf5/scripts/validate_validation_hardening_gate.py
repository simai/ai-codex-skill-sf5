#!/usr/bin/env python3
"""
Validate the Validation Hardening Gate as a focused machine-check.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def skill_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> dict:
    result = subprocess.run(cmd, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout or "command failed")
    return json.loads(result.stdout)


def main() -> int:
    skill_root = skill_root_from_script()
    payloads = {
        "route": run([sys.executable, str(skill_root / "scripts" / "validate_route_fixtures.py")]),
        "activity": run([sys.executable, str(skill_root / "scripts" / "validate_activity_fixtures.py")]),
        "router_hints": run([sys.executable, str(skill_root / "scripts" / "validate_router_hints.py")]),
        "scaffold_hints": run([sys.executable, str(skill_root / "scripts" / "validate_scaffold_hints.py")]),
        "e2e": run([sys.executable, str(skill_root / "scripts" / "validate_e2e_fixtures.py")]),
        "contract": run([sys.executable, str(skill_root / "scripts" / "validate_validation_contract.py")]),
    }

    failures = []
    for name, payload in payloads.items():
        if not payload.get("ok"):
            failures.append(f"{name} validator is not green")

    payload = {
        "ok": not failures,
        "activityId": "validation-hardening",
        "counts": {
            "routeFixtures": payloads["route"].get("fixtureCount", 0),
            "activityFixtures": payloads["activity"].get("fixtureCount", 0),
            "routerHintFixtures": payloads["router_hints"].get("fixtureCount", 0),
            "scaffoldHintFixtures": payloads["scaffold_hints"].get("fixtureCount", 0),
            "e2eFixtures": payloads["e2e"].get("fixtureCount", 0),
        },
    }
    if failures:
        payload["failures"] = failures
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 1

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
