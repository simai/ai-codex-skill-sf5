#!/usr/bin/env python3
"""
Validate the Source Refresh Gate as a focused machine-check.
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
    repo_root = skill_root.parents[1]

    inventory_payload = run(
        [
            sys.executable,
            str(skill_root / "scripts" / "build_source_inventory.py"),
            "--repo-root",
            str(repo_root),
            "--skill-root",
            str(skill_root),
            "--format",
            "json",
        ]
    )
    contract_payload = run(
        [sys.executable, str(skill_root / "scripts" / "validate_source_refresh_contract.py")]
    )

    failures = []
    if inventory_payload.get("activity_hint", {}).get("activity_id") != "source-refresh":
        failures.append("build_source_inventory.py lost source-refresh activity hint")
    if not contract_payload.get("ok"):
        failures.append("validate_source_refresh_contract.py is not green")
    summary = inventory_payload.get("summary") or {}
    if summary.get("shippedComponentCount", 0) <= 0:
        failures.append("source inventory build returned zero shipped components")
    if summary.get("shippedSmartCount", 0) <= 0:
        failures.append("source inventory build returned zero shipped smart-components")

    payload = {
        "ok": not failures,
        "activityId": "source-refresh",
        "componentCount": summary.get("shippedComponentCount", 0),
        "smartCount": summary.get("shippedSmartCount", 0),
    }
    if failures:
        payload["failures"] = failures
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 1

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
