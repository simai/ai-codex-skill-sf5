#!/usr/bin/env python3
"""
Validate SF5 activity manifests and referenced coordinator assets.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def skill_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_ref(path_value: str) -> str:
    return path_value.split("#", 1)[0]


def main() -> int:
    skill_root = skill_root_from_script()
    registry = load_json(skill_root / "activities" / "activity-registry.json")
    activity_ids = registry.get("activities", [])
    failures: list[str] = []
    checked = 0

    for activity_id in activity_ids:
        manifest_path = skill_root / "activities" / f"{activity_id}.json"
        if not manifest_path.exists():
            failures.append(f"Missing manifest file: activities/{activity_id}.json")
            continue

        manifest = load_json(manifest_path)
        checked += 1
        for key in [
            "activity_id",
            "title",
            "triggers",
            "required_specialists",
            "optional_specialists",
            "required_rules",
            "required_outputs",
        ]:
            if key not in manifest:
                failures.append(f"{manifest_path.name}: missing key '{key}'")

        if manifest.get("activity_id") != activity_id:
            failures.append(
                f"{manifest_path.name}: activity_id '{manifest.get('activity_id')}' "
                f"does not match registry id '{activity_id}'"
            )

        specialists = manifest.get("required_specialists", []) + manifest.get("optional_specialists", [])
        for specialist in specialists:
            profile = skill_root / "specialists" / specialist / "profile.md"
            if not profile.exists():
                failures.append(
                    f"{manifest_path.name}: missing specialist profile specialists/{specialist}/profile.md"
                )

        for bucket in ["required_rules", "knowledge_packs", "gate_rules"]:
            for ref in manifest.get(bucket, []):
                normalized = normalize_ref(ref)
                if not normalized:
                    failures.append(f"{manifest_path.name}: empty reference in '{bucket}'")
                    continue
                target = skill_root / normalized
                if not target.exists():
                    failures.append(
                        f"{manifest_path.name}: missing referenced file '{normalized}' from '{bucket}'"
                    )

    payload = {"ok": not failures, "checked": checked}
    if failures:
        payload["failures"] = failures
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 1

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
