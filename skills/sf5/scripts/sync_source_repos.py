#!/usr/bin/env python3
"""
Sync external SIMAI SF5 source repositories into the local ignored source tree.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ACTIVITY_HINT = {
    "activity_id": "source-refresh",
    "required_specialists": [
        "task-goal",
        "source-sync",
        "validation-qa",
    ],
}


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=True,
        check=False,
    )


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[3]


def error_payload(spec: dict, branch: str, message: str) -> dict:
    return {
        "name": spec["name"],
        "status": "error",
        "branch": branch,
        "localPath": spec["localPath"],
        "remote": spec["remote"],
        "priority": spec.get("priority"),
        "kind": spec.get("kind"),
        "error": message,
    }


def sync_repo(repo_root: Path, spec: dict) -> dict:
    local_path = repo_root / spec["localPath"]
    local_path.parent.mkdir(parents=True, exist_ok=True)
    branch = spec.get("defaultBranch", "main")
    remote = spec["remote"]

    if not (local_path / ".git").exists():
        result = run(
            ["git", "clone", "--depth", "1", "--branch", branch, remote, str(local_path)]
        )
        if result.returncode != 0:
            return error_payload(spec, branch, (result.stderr or result.stdout).strip())
    else:
        set_remote = run(["git", "remote", "set-url", "origin", remote], cwd=local_path)
        if set_remote.returncode != 0:
            return error_payload(spec, branch, (set_remote.stderr or set_remote.stdout).strip())

        fetch = run(["git", "fetch", "--depth", "1", "origin", branch], cwd=local_path)
        if fetch.returncode != 0:
            return error_payload(spec, branch, (fetch.stderr or fetch.stdout).strip())

        checkout = run(["git", "checkout", "-B", branch, "FETCH_HEAD"], cwd=local_path)
        if checkout.returncode != 0:
            return error_payload(spec, branch, (checkout.stderr or checkout.stdout).strip())

    head = run(["git", "rev-parse", "HEAD"], cwd=local_path)
    current_branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=local_path)

    if head.returncode != 0 or current_branch.returncode != 0:
        return error_payload(spec, branch, "Unable to read repository HEAD after sync")

    return {
        "name": spec["name"],
        "status": "ok",
        "branch": current_branch.stdout.strip(),
        "commit": head.stdout.strip(),
        "localPath": spec["localPath"],
        "remote": remote,
        "priority": spec.get("priority"),
        "kind": spec.get("kind"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-root",
        default=str(repo_root_from_script()),
        help="Repository root containing source/ and skills/sf5/",
    )
    parser.add_argument(
        "--manifest",
        default=None,
        help="Override path to source repo manifest JSON",
    )
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    manifest_path = (
        Path(args.manifest).resolve()
        if args.manifest
        else repo_root / "skills/sf5/references/vendor/source-repos.json"
    )
    lock_path = manifest_path.with_name("source-repos.lock.json")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    results = [sync_repo(repo_root, spec) for spec in manifest.get("repos", [])]

    lock_payload = {
        "schemaVersion": 1,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "repoRoot": str(repo_root),
        "manifest": str(manifest_path),
        "results": results,
    }
    lock_path.write_text(
        json.dumps(lock_payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    if args.format == "json":
        print(
            json.dumps(
                {
                    "ok": all(item["status"] == "ok" or item["priority"] == "optional" for item in results),
                    "activity_hint": ACTIVITY_HINT,
                    "lock_file": str(lock_path),
                    "results": results,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        for item in results:
            if item["status"] == "ok":
                print(f"ok\t{item['name']}\t{item['branch']}\t{item['commit']}")
            else:
                print(f"error\t{item['name']}\t{item.get('error', 'unknown error')}")

    return 0 if all(item["status"] == "ok" or item["priority"] == "optional" for item in results) else 1


if __name__ == "__main__":
    sys.exit(main())
