#!/usr/bin/env python3
"""
Validate consistency between source-refresh manifests and derived source inventory.
"""

from __future__ import annotations

import json
from pathlib import Path


def root_dir_from_script() -> Path:
    return Path(__file__).resolve().parents[3]


def skill_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def repo_map(items: list[dict]) -> dict[str, dict]:
    return {item["name"]: item for item in items}


def main() -> int:
    root = root_dir_from_script()
    vendor_dir = skill_root_from_script() / "references" / "vendor"

    source_repos = load_json(vendor_dir / "source-repos.json")
    source_locks = load_json(vendor_dir / "source-repos.lock.json")
    source_inventory = load_json(vendor_dir / "source-inventory.json")
    component_smart_catalog = load_json(vendor_dir / "component-smart-catalog.json")

    repo_specs = repo_map(source_repos.get("repos", []))
    lock_specs = repo_map(source_locks.get("results", []))
    inventory_specs = source_inventory.get("repos", {})

    failures: list[str] = []
    checked = 0

    for name, repo in repo_specs.items():
        checked += 1
        lock = lock_specs.get(name)
        inventory = inventory_specs.get(name)
        if not lock:
            failures.append(f"Missing lock entry for repo '{name}'")
            continue
        if not inventory:
            failures.append(f"Missing source inventory entry for repo '{name}'")
            continue

        if repo.get("localPath") != lock.get("localPath") or repo.get("localPath") != inventory.get("localPath"):
            failures.append(f"Repo '{name}' has inconsistent localPath across source-repos, lock, and inventory")
        if repo.get("kind") != inventory.get("kind"):
            failures.append(f"Repo '{name}' has inconsistent kind between source-repos and inventory")

        status = lock.get("status")
        optional = bool(repo.get("optional")) or repo.get("priority") == "optional"
        local_path = root / repo.get("localPath", "")

        if status == "ok" and not local_path.exists():
            failures.append(f"Repo '{name}' is marked ok but checkout path does not exist: {repo.get('localPath')}")
        if status == "error" and not optional:
            failures.append(f"Repo '{name}' is non-optional but lock status is error")

    required_ok_repos = ["ui", "ui-doc", "ui-play", "ui-smart", "ui-utilities"]
    for repo_name in required_ok_repos:
        if lock_specs.get(repo_name, {}).get("status") != "ok":
            failures.append(f"Required source-refresh repo '{repo_name}' is not synced with status ok")

    summary = source_inventory.get("summary", {})
    if summary.get("shippedComponentCount", 0) <= 0:
        failures.append("Source inventory summary reports no shipped components")
    if summary.get("shippedSmartCount", 0) <= 0:
        failures.append("Source inventory summary reports no shipped smart-components")
    if summary.get("componentExampleGroupCount", 0) <= 0:
        failures.append("Source inventory summary reports no component example groups")
    if summary.get("smartExampleGroupCount", 0) <= 0:
        failures.append("Source inventory summary reports no smart example groups")

    catalog_summary = component_smart_catalog.get("summary", {})
    if catalog_summary.get("componentCount", 0) <= 0:
        failures.append("Component/smart catalog reports no components")
    if catalog_summary.get("smartComponentCount", 0) <= 0:
        failures.append("Component/smart catalog reports no smart-components")
    if catalog_summary.get("componentsWithExamples", 0) <= 0:
        failures.append("Component/smart catalog reports no component examples")
    if catalog_summary.get("smartComponentsWithExamples", 0) <= 0:
        failures.append("Component/smart catalog reports no smart-component examples")

    payload = {"ok": not failures, "checked": checked}
    if failures:
        payload["failures"] = failures
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 1

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
