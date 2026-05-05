#!/usr/bin/env python3
"""
Validate end-to-end SF5 task preparation and working-set generation fixtures.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def skill_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, text=True, capture_output=True, check=False)


def validate_fixture(skill_root: Path, fixture: dict, temp_root: Path) -> dict | None:
    fixture_dir = temp_root / fixture["id"]
    fixture_dir.mkdir(parents=True, exist_ok=True)

    prepare_json = fixture_dir / "task.json"
    scaffold_html = fixture_dir / "prepared.html"
    prepare_cmd = [
        sys.executable,
        str(skill_root / "scripts/prepare_sf5_task.py"),
        fixture["query"],
        "--format",
        "json",
        "--scaffold-out",
        str(scaffold_html),
    ]
    prepare_result = run(prepare_cmd)
    if prepare_result.returncode != 0:
        return {
            "id": fixture["id"],
            "stage": "prepare",
            "error": prepare_result.stderr or prepare_result.stdout or "prepare failed",
        }
    prepare_json.write_text(prepare_result.stdout, encoding="utf-8")
    task = json.loads(prepare_result.stdout)

    working_set_dir = fixture_dir / "working-set"
    working_set_cmd = [
        sys.executable,
        str(skill_root / "scripts/generate_sf5_working_set.py"),
        fixture["query"],
        "--out-dir",
        str(working_set_dir),
    ]
    working_set_result = run(working_set_cmd)
    if working_set_result.returncode != 0:
        return {
            "id": fixture["id"],
            "stage": "working-set",
            "error": working_set_result.stderr or working_set_result.stdout or "working set failed",
        }

    manifest = load_json(working_set_dir / "manifest.json")
    actual_section_ids = [item["id"] for item in manifest.get("section_variants", [])]
    actual_upstream_ids = [item["id"] for item in manifest.get("upstream_variants", [])]
    task_activity = task["route"].get("activity", {})
    manifest_activity = manifest.get("activity", {})

    errors = []
    if task["route"].get("scenario_id") != fixture["expectedScenarioId"]:
        errors.append(
            f"prepare scenario mismatch: expected {fixture['expectedScenarioId']}, got {task['route'].get('scenario_id')}"
        )
    if task["route"].get("recipe_type") != fixture["expectedRecipeType"]:
        errors.append(
            f"prepare recipe mismatch: expected {fixture['expectedRecipeType']}, got {task['route'].get('recipe_type')}"
        )
    if manifest["route"].get("scenario_id") != fixture["expectedScenarioId"]:
        errors.append(
            f"manifest scenario mismatch: expected {fixture['expectedScenarioId']}, got {manifest['route'].get('scenario_id')}"
        )
    if manifest["route"].get("recipe_type") != fixture["expectedRecipeType"]:
        errors.append(
            f"manifest recipe mismatch: expected {fixture['expectedRecipeType']}, got {manifest['route'].get('recipe_type')}"
        )
    expected_activity = fixture.get("expectedActivityId")
    if expected_activity and task_activity.get("activity_id") != expected_activity:
        errors.append(
            f"prepare activity mismatch: expected {expected_activity}, got {task_activity.get('activity_id')}"
        )
    if expected_activity and manifest_activity.get("activity_id") != expected_activity:
        errors.append(
            f"manifest activity mismatch: expected {expected_activity}, got {manifest_activity.get('activity_id')}"
        )
    if not task["route"].get("matched"):
        errors.append("prepare route is not matched")
    if not manifest["route"].get("matched"):
        errors.append("manifest route is not matched")
    if not scaffold_html.exists():
        errors.append("prepared scaffold not generated")
    if not (working_set_dir / "scaffold.html").exists():
        errors.append("working-set scaffold not generated")
    for rel_path in fixture.get("requiredFiles", []):
        if not (working_set_dir / rel_path).exists():
            errors.append(f"missing required file: {rel_path}")
    if manifest.get("files", {}).get("scaffold") != "scaffold.html":
        errors.append("manifest files.scaffold mismatch")
    if manifest.get("files", {}).get("activity_json") != "activity.json":
        errors.append("manifest files.activity_json mismatch")
    if manifest.get("files", {}).get("sections_dir") != "sections/":
        errors.append("manifest files.sections_dir mismatch")
    if manifest.get("files", {}).get("upstream_dir") != "upstream/":
        errors.append("manifest files.upstream_dir mismatch")
    if len(task["route"].get("workflow", [])) < fixture.get("minWorkflowSteps", 0):
        errors.append("prepare workflow too short")
    if len(manifest["route"].get("workflow", [])) < fixture.get("minWorkflowSteps", 0):
        errors.append("manifest workflow too short")
    missing_playbooks = [
        item
        for item in fixture.get("requiredPatternPlaybooks", [])
        if item not in (task["route"].get("pattern_playbooks") or [])
    ]
    if missing_playbooks:
        errors.append(f"missing required pattern playbooks: {', '.join(missing_playbooks)}")

    missing_sections = [item for item in fixture["expectedSectionIds"] if item not in actual_section_ids]
    if missing_sections:
        errors.append(f"missing sections: {', '.join(missing_sections)}")

    missing_upstream = [item for item in fixture["expectedUpstreamIds"] if item not in actual_upstream_ids]
    if missing_upstream:
        errors.append(f"missing upstream variants: {', '.join(missing_upstream)}")

    required_activity_specialists = fixture.get("requiredActivitySpecialists", [])
    for specialist in required_activity_specialists:
        if specialist not in (task_activity.get("required_specialists") or []):
            errors.append(f"missing prepare activity specialist: {specialist}")
        if specialist not in (manifest_activity.get("required_specialists") or []):
            errors.append(f"missing manifest activity specialist: {specialist}")

    required_activity_gate_rules = fixture.get("requiredActivityGateRules", [])
    for gate_rule in required_activity_gate_rules:
        if gate_rule not in (task_activity.get("gate_rules") or []):
            errors.append(f"missing prepare activity gate rule: {gate_rule}")
        if gate_rule not in (manifest_activity.get("gate_rules") or []):
            errors.append(f"missing manifest activity gate rule: {gate_rule}")

    required_activity_packs = fixture.get("requiredActivityKnowledgePacks", [])
    for pack in required_activity_packs:
        if pack not in (task_activity.get("knowledge_packs") or []):
            errors.append(f"missing prepare activity knowledge pack: {pack}")
        if pack not in (manifest_activity.get("knowledge_packs") or []):
            errors.append(f"missing manifest activity knowledge pack: {pack}")

    required_activity_roles = fixture.get("requiredActivityRoles", {})
    task_roles = {
        role_item["name"]: role_item["role"]
        for role_item in task_activity.get("specialist_roles", [])
        if role_item.get("required")
    }
    manifest_roles = {
        role_item["name"]: role_item["role"]
        for role_item in manifest_activity.get("specialist_roles", [])
        if role_item.get("required")
    }
    for specialist, expected_role in required_activity_roles.items():
        if task_roles.get(specialist) != expected_role:
            errors.append(
                f"prepare activity role mismatch for {specialist}: expected {expected_role}, got {task_roles.get(specialist)}"
            )
        if manifest_roles.get(specialist) != expected_role:
            errors.append(
                f"manifest activity role mismatch for {specialist}: expected {expected_role}, got {manifest_roles.get(specialist)}"
            )

    required_activity_workflow_snippets = fixture.get("requiredActivityWorkflowSnippets", [])
    task_workflow = task_activity.get("workflow") or []
    manifest_workflow = manifest_activity.get("workflow") or []
    for snippet in required_activity_workflow_snippets:
        if not any(snippet.lower() in step.lower() for step in task_workflow):
            errors.append(f"missing prepare activity workflow snippet: {snippet}")
        if not any(snippet.lower() in step.lower() for step in manifest_workflow):
            errors.append(f"missing manifest activity workflow snippet: {snippet}")

    if errors:
        return {
            "id": fixture["id"],
            "stage": "assert",
            "errors": errors,
        }
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate SF5 e2e fixtures.")
    parser.add_argument("--skill-root", default="", help="Optional skill root override")
    args = parser.parse_args()

    skill_root = Path(args.skill_root).resolve() if args.skill_root else skill_root_from_script()
    fixtures = load_json(skill_root / "references" / "vendor" / "e2e-fixtures.json")["fixtures"]

    temp_root = Path(tempfile.mkdtemp(prefix="sf5-e2e-fixtures-"))
    failures = []
    try:
        for fixture in fixtures:
            failure = validate_fixture(skill_root, fixture, temp_root)
            if failure:
                failures.append(failure)
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)

    if failures:
        print(json.dumps({"ok": False, "failures": failures}, ensure_ascii=False, indent=2))
        return 1

    print(json.dumps({"ok": True, "fixtureCount": len(fixtures)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
