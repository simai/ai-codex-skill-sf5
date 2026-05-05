#!/usr/bin/env python3
"""
Validate the SF5 Tailwind conversion activity and specialist contract.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def skill_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def run_activity(skill_root: Path, query: str) -> dict:
    result = subprocess.run(
        [
            sys.executable,
            str(skill_root / "scripts" / "recommend_sf5_activity.py"),
            query,
            "--format",
            "json",
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout or "activity command failed")
    return json.loads(result.stdout)


def run_mapping_validator(skill_root: Path) -> dict:
    result = subprocess.run(
        [
            sys.executable,
            str(skill_root / "scripts" / "validate_tailwind_mapping_artifacts.py"),
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.stdout:
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            raise RuntimeError(result.stderr or result.stdout or "mapping validator failed") from exc
    raise RuntimeError(result.stderr or "mapping validator returned no output")


def main() -> int:
    skill_root = skill_root_from_script()
    failures: list[str] = []

    required_paths = [
        "activities/tailwind-conversion.json",
        "specialists/tailwind-converter/profile.md",
        "knowledge-packs/tailwind-to-sf5-conversion.md",
        "roadmap/tailwind-to-sf5-learning-plan.md",
        "roadmap/tailwind-to-sf5-stage-1-2-tz.md",
        "roadmap/future-specialties-and-tailwind-conversion.md",
        "references/vendor/tailwind-to-sf5.class-groups.json",
        "references/vendor/tailwind-to-sf5.utility-map.json",
        "references/vendor/tailwind-to-sf5.fixtures.json",
        "references/vendor/tailwind-to-sf5.component-hints.json",
        "references/vendor/tailwind-to-sf5.component-recipes.json",
        "references/vendor/tailwind-to-sf5.component-renderers.json",
        "references/vendor/tailwind-to-sf5.smart-hints.json",
        "references/vendor/component-smart-catalog.json",
        "references/vendor/tailwind-to-sf5.inventory-source.html",
        "references/component-smart-catalog.md",
        "references/vendor/tailwind-to-sf5.e2e-toolbar.sf5.html",
        "references/vendor/tailwind-to-sf5.e2e-auth.sf5.html",
        "references/vendor/tailwind-to-sf5.e2e-card.sf5.html",
        "references/vendor/tailwind-to-sf5.e2e-table.sf5.html",
        "references/tailwind-to-sf5-e2e-toolbar-example.md",
        "references/tailwind-to-sf5-e2e-examples.md",
        "scripts/convert_tailwind_to_sf5.py",
        "scripts/capture_html_screenshot.py",
        "scripts/probe_html_runtime.py",
        "scripts/run_tailwind_conversion_lab.py",
        "scripts/run_tailadmin_page_examples.py",
        "scripts/build_component_smart_catalog.py",
        "scripts/score_lab_visual.py",
        "scripts/validate_tailwind_mapping_artifacts.py",
        "scripts/validate_tailwind_converter.py",
    ]
    for rel_path in required_paths:
        if not (skill_root / rel_path).exists():
            failures.append(f"Missing Tailwind conversion artifact: {rel_path}")

    registry = load_json(skill_root / "activities" / "activity-registry.json")
    if "tailwind-conversion" not in registry.get("activities", []):
        failures.append("tailwind-conversion is missing from activity registry")

    manifest = load_json(skill_root / "activities" / "tailwind-conversion.json")
    expected_specialists = ["task-goal", "tailwind-converter", "validation-qa"]
    for specialist in expected_specialists:
        if specialist not in manifest.get("required_specialists", []):
            failures.append(f"tailwind-conversion manifest misses required specialist: {specialist}")
    if "knowledge-packs/tailwind-to-sf5-conversion.md" not in manifest.get("knowledge_packs", []):
        failures.append("tailwind-conversion manifest misses conversion knowledge pack")
    if "roadmap/tailwind-to-sf5-learning-plan.md" not in manifest.get("knowledge_packs", []):
        failures.append("tailwind-conversion manifest misses Tailwind learning plan")
    if "roadmap/tailwind-to-sf5-stage-1-2-tz.md" not in manifest.get("knowledge_packs", []):
        failures.append("tailwind-conversion manifest misses Stage 1-2 TZ")
    if not any("unmapped Tailwind" in item for item in manifest.get("required_outputs", [])):
        failures.append("tailwind-conversion manifest must require unmapped Tailwind report")

    payload = run_activity(
        skill_root,
        "convert Tailwind Plus application UI block to SF5 markup with unmapped class report",
    )
    if payload.get("activity_id") != "tailwind-conversion":
        failures.append(f"activity router returned {payload.get('activity_id')} instead of tailwind-conversion")
    if "tailwind-converter" not in payload.get("required_specialists", []):
        failures.append("activity router payload misses tailwind-converter")
    if "knowledge-packs/tailwind-to-sf5-conversion.md" not in payload.get("knowledge_packs", []):
        failures.append("activity router payload misses Tailwind conversion knowledge pack")
    if "roadmap/tailwind-to-sf5-learning-plan.md" not in payload.get("knowledge_packs", []):
        failures.append("activity router payload misses Tailwind conversion learning plan")
    if "roadmap/tailwind-to-sf5-stage-1-2-tz.md" not in payload.get("knowledge_packs", []):
        failures.append("activity router payload misses Tailwind conversion Stage 1-2 TZ")

    mapping_payload = run_mapping_validator(skill_root)
    if not mapping_payload.get("ok"):
        failures.append("Tailwind mapping artifacts validator failed")
        for failure in mapping_payload.get("failures", []):
            failures.append(str(failure))

    converter_result = subprocess.run(
        [
            sys.executable,
            str(skill_root / "scripts" / "validate_tailwind_converter.py"),
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    try:
        converter_payload = json.loads(converter_result.stdout)
    except json.JSONDecodeError:
        converter_payload = {"ok": False, "failures": [converter_result.stderr or converter_result.stdout]}
    if not converter_payload.get("ok"):
        failures.append("Tailwind converter validator failed")
        for failure in converter_payload.get("failures", []):
            failures.append(str(failure))

    result = {
        "ok": not failures,
        "activityId": "tailwind-conversion",
    }
    if failures:
        result["failures"] = failures
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
