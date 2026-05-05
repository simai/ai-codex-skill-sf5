#!/usr/bin/env python3
"""
Prepare an SF5 task brief from a free-form request and optionally generate a scaffold file.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def root_dir_from_script() -> Path:
    return Path(__file__).resolve().parents[2]


def skill_dir_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, text=True, capture_output=True, check=False)


def build_brief(query: str, route: dict, scaffold_path: str | None) -> str:
    lines = []
    lines.append("# SF5 Task Brief")
    lines.append("")
    lines.append(f"- Query: `{query}`")
    if route.get("scenario_id"):
        lines.append(f"- Scenario: `{route['scenario_id']}`")
    if route.get("scenario_doc"):
        lines.append(f"- Scenario doc: `{route['scenario_doc']}`")
    if route.get("page_recipe"):
        lines.append(f"- Page recipe: `{route['page_recipe']}`")
    if route.get("recipe_type"):
        lines.append(f"- Recipe type: `{route['recipe_type']}`")
    if route.get("scaffold_command"):
        lines.append(f"- Scaffold command: `{route['scaffold_command']}`")
    if scaffold_path:
        lines.append(f"- Scaffold output: `{scaffold_path}`")
    lines.append("")
    if route.get("pattern_playbooks"):
        lines.append("## Pattern Playbooks")
        lines.append("")
        for item in route["pattern_playbooks"]:
            lines.append(f"- `{item}`")
        lines.append("")
    if route.get("workflow"):
        lines.append("## Workflow")
        lines.append("")
        for item in route["workflow"]:
            lines.append(f"- {item}")
        lines.append("")
    activity = route.get("activity") or {}
    if activity.get("activity_id"):
        lines.append("## Coordinator Activity")
        lines.append("")
        lines.append(f"- Activity: `{activity['activity_id']}`")
        if activity.get("title"):
            lines.append(f"- Title: {activity['title']}")
        if activity.get("required_specialists"):
            lines.append(f"- Required specialists: `{', '.join(activity['required_specialists'])}`")
        if activity.get("gate_rules"):
            lines.append("- Gate rules:")
            for item in activity["gate_rules"]:
                lines.append(f"  - `{item}`")
        if activity.get("knowledge_packs"):
            lines.append("- Knowledge packs:")
            for item in activity["knowledge_packs"]:
                lines.append(f"  - `{item}`")
        lines.append("")
    if route.get("alternatives"):
        lines.append("## Alternatives")
        lines.append("")
        for item in route["alternatives"]:
            lines.append(f"- {item}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def build_json_payload(query: str, route: dict, scaffold_path: str | None) -> dict:
    payload = {
        "query": query,
        "route": route,
    }
    if scaffold_path:
        payload["scaffold_output"] = scaffold_path
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare an SF5 task brief.")
    parser.add_argument("query", help="Free-form task description")
    parser.add_argument("--out", default="", help="Optional markdown output path")
    parser.add_argument("--scaffold-out", default="", help="Optional scaffold HTML output path")
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Prepared task output format",
    )
    parser.add_argument("--theme", choices=["light", "dark"], default="light")
    parser.add_argument("--title", default="", help="Optional scaffold title override")
    args = parser.parse_args()

    root = root_dir_from_script()
    skill = skill_dir_from_script()

    route_cmd = [
        sys.executable,
        str(skill / "scripts/recommend_sf5_route.py"),
        args.query,
        "--format",
        "json",
    ]
    route_result = run(route_cmd)
    if route_result.returncode != 0:
        sys.stderr.write(route_result.stderr or route_result.stdout)
        return route_result.returncode

    route = json.loads(route_result.stdout)
    scaffold_path = ""
    recipe_type = route.get("recipe_type")
    if args.scaffold_out and recipe_type:
        scaffold_cmd = [
            sys.executable,
            str(skill / "scripts/generate_page_scaffold.py"),
            "--type",
            recipe_type,
            "--theme",
            args.theme,
            "--out",
            args.scaffold_out,
        ]
        if args.title:
            scaffold_cmd.extend(["--title", args.title])
        scaffold_result = run(scaffold_cmd)
        if scaffold_result.returncode != 0:
            sys.stderr.write(scaffold_result.stderr or scaffold_result.stdout)
            return scaffold_result.returncode
        scaffold_path = args.scaffold_out

    if args.format == "json":
        output = json.dumps(
            build_json_payload(args.query, route, scaffold_path or None),
            ensure_ascii=False,
            indent=2,
        ) + "\n"
    else:
        output = build_brief(args.query, route, scaffold_path or None)

    if args.out:
        out_path = Path(args.out).expanduser().resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output, encoding="utf-8")
        print(f"Wrote {out_path}")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
