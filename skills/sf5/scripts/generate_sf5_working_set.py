#!/usr/bin/env python3
"""
Generate a ready-to-use SF5 working set directory from a free-form task.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


SECTION_VARIANTS_BY_RECIPE = {}
LEGACY_EXTRACTED_CLASS_MAP = {}


def root_dir_from_script() -> Path:
    return Path(__file__).resolve().parents[3]


def skill_dir_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_working_set_manifests(skill_root: Path) -> tuple[dict, dict]:
    vendor_dir = skill_root / "references" / "vendor"
    section_variants = load_json(vendor_dir / "working-set.section-variants.json")
    legacy_map = load_json(vendor_dir / "working-set.legacy-class-map.json")
    return section_variants, legacy_map


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, text=True, capture_output=True, check=False)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def normalize_class_token(token: str) -> str:
    parts = token.split(":")
    base = parts[-1]
    base = LEGACY_EXTRACTED_CLASS_MAP.get(base, base)
    parts[-1] = base
    return ":".join(parts)


def normalize_class_attrs(html: str) -> str:
    def replace_class_attr(match: re.Match) -> str:
        quote = match.group(1)
        blob = match.group(2)
        tokens = [normalize_class_token(token) for token in blob.replace("\n", " ").split()]
        return f'class={quote}{" ".join(tokens)}{quote}'

    return re.sub(
        r'class\s*=\s*(["\'])(.*?)\1',
        replace_class_attr,
        html,
        flags=re.DOTALL,
    )


def normalize_html_snippet(text: str) -> str:
    return normalize_class_attrs(text.strip()) + "\n"


def iter_tag_tokens(text: str):
    pattern = re.compile(r"<(/?)([a-zA-Z][\w:-]*)\b[^>]*?>", flags=re.IGNORECASE)
    for match in pattern.finditer(text):
        token = match.group(0)
        yield {
            "start": match.start(),
            "end": match.end(),
            "tag": match.group(2).lower(),
            "is_closing": match.group(1) == "/",
            "is_self_closing": token.endswith("/>"),
        }


def locate_balanced_tag_block(
    text: str,
    tag: str,
    class_token: str,
    occurrence: int = 1,
) -> tuple[int, int]:
    class_pattern = re.compile(
        rf"<{tag}\b[^>]*class=\"[^\"]*\b{re.escape(class_token)}\b[^\"]*\"[^>]*>",
        flags=re.IGNORECASE,
    )
    matches = list(class_pattern.finditer(text))
    if not matches and tag.lower() == class_token.lower():
        tag_pattern = re.compile(rf"<{tag}\b[^>]*>", flags=re.IGNORECASE)
        matches = list(tag_pattern.finditer(text))
    if occurrence < 1 or len(matches) < occurrence:
        raise ValueError(
            f"Could not find occurrence {occurrence} of <{tag}> with class token '{class_token}'."
        )
    start_match = matches[occurrence - 1]
    tag_pattern = re.compile(rf"<(/?){tag}\b[^>]*?>", flags=re.IGNORECASE)
    depth = 0
    started = False
    for match in tag_pattern.finditer(text, start_match.start()):
        token = match.group(0)
        is_closing = match.group(1) == "/"
        is_self_closing = token.endswith("/>")
        if not is_closing:
            depth += 1
            started = True
        elif started:
            depth -= 1
        if started and depth == 0:
            return start_match.start(), match.end()
        if is_self_closing and started:
            depth -= 1
            if depth == 0:
                return start_match.start(), match.end()
    raise ValueError(f"Could not extract balanced <{tag}> block for class token '{class_token}'.")


def locate_balanced_tag_from_start(text: str, tag: str, start_pos: int) -> tuple[int, int]:
    tag_pattern = re.compile(rf"<(/?){tag}\b[^>]*?>", flags=re.IGNORECASE)
    depth = 0
    started = False
    for match in tag_pattern.finditer(text, start_pos):
        token = match.group(0)
        is_closing = match.group(1) == "/"
        is_self_closing = token.endswith("/>")
        if match.start() == start_pos and is_closing:
            raise ValueError(f"Encountered closing tag at ancestor start for <{tag}>.")
        if not is_closing:
            depth += 1
            started = True
        elif started:
            depth -= 1
        if started and depth == 0:
            return start_pos, match.end()
        if is_self_closing and started:
            depth -= 1
            if depth == 0:
                return start_pos, match.end()
    raise ValueError(f"Could not extract balanced ancestor <{tag}> block.")


def extract_balanced_tag_block(text: str, tag: str, class_token: str, occurrence: int = 1) -> str:
    start, end = locate_balanced_tag_block(
        text=text,
        tag=tag,
        class_token=class_token,
        occurrence=occurrence,
    )
    return normalize_html_snippet(text[start:end])


def extract_range_block(text: str, start_spec: dict, end_spec: dict) -> str:
    start, _ = locate_balanced_tag_block(
        text=text,
        tag=start_spec["tag"],
        class_token=start_spec["class_token"],
        occurrence=start_spec.get("occurrence", 1),
    )
    _, end = locate_balanced_tag_block(
        text=text,
        tag=end_spec["tag"],
        class_token=end_spec["class_token"],
        occurrence=end_spec.get("occurrence", 1),
    )
    if start >= end:
        raise ValueError("Range extract start must appear before end.")
    return normalize_html_snippet(text[start:end])


def extract_ancestor_block(
    text: str,
    child_tag: str,
    child_class_token: str,
    ancestor_tag: str,
    occurrence: int = 1,
    levels_up: int = 1,
) -> str:
    child_start, _ = locate_balanced_tag_block(
        text=text,
        tag=child_tag,
        class_token=child_class_token,
        occurrence=occurrence,
    )
    stack: list[dict] = []
    for token in iter_tag_tokens(text):
        if token["start"] >= child_start:
            break
        if token["is_closing"]:
            if stack:
                stack.pop()
            continue
        if not token["is_self_closing"]:
            stack.append(token)

    matching = [item for item in stack if item["tag"] == ancestor_tag.lower()]
    if len(matching) < levels_up:
        raise ValueError(
            f"Could not find ancestor level {levels_up} <{ancestor_tag}> for "
            f"<{child_tag}> with class token '{child_class_token}'."
        )
    ancestor = matching[-levels_up]
    start, end = locate_balanced_tag_from_start(text, ancestor_tag.lower(), ancestor["start"])
    return normalize_html_snippet(text[start:end])


def extract_from_spec(text: str, extract: dict) -> str:
    if extract.get("mode") == "range":
        return extract_range_block(
            text=text,
            start_spec=extract["start"],
            end_spec=extract["end"],
        )
    if extract.get("mode") == "ancestor":
        return extract_ancestor_block(
            text=text,
            child_tag=extract["tag"],
            child_class_token=extract["class_token"],
            ancestor_tag=extract["ancestor_tag"],
            occurrence=extract.get("occurrence", 1),
            levels_up=extract.get("levels_up", 1),
        )
    return extract_balanced_tag_block(
        text=text,
        tag=extract["tag"],
        class_token=extract["class_token"],
        occurrence=extract.get("occurrence", 1),
    )


def write_upstream_variants(out_dir: Path, recipe_type: str | None, repo_root: Path) -> list[dict]:
    section_specs = SECTION_VARIANTS_BY_RECIPE.get(recipe_type or "", [])
    upstream_dir = out_dir / "upstream"
    created = []
    for spec in section_specs:
        extracts = spec.get("upstream_extracts", [])
        if not extracts:
            continue
        chunks = []
        for extract in extracts:
            source_path = repo_root / extract["source"]
            source_text = source_path.read_text(encoding="utf-8")
            chunk = extract_from_spec(source_text, extract)
            chunks.append(chunk)
        file_name = f"{spec['id']}.html"
        write_text(upstream_dir / file_name, "\n\n".join(chunks).strip() + "\n")
        created.append(
            {
                "id": spec["id"],
                "file": f"upstream/{file_name}",
                "source_refs": spec.get("source_refs", []),
            }
        )
    return created


def write_section_variants(out_dir: Path, recipe_type: str | None) -> list[dict]:
    section_specs = SECTION_VARIANTS_BY_RECIPE.get(recipe_type or "", [])
    sections_dir = out_dir / "sections"
    created = []
    for spec in section_specs:
        file_name = f"{spec['id']}.html"
        write_text(sections_dir / file_name, spec["html"])
        created.append(
            {
                "id": spec["id"],
                "title": spec["title"],
                "description": spec["description"],
                "file": f"sections/{file_name}",
                "source_refs": spec.get("source_refs", []),
            }
        )
    return created


def build_sections_index(section_files: list[dict]) -> str:
    lines = [
        "# SF5 Section Variants",
        "",
        "Use these snippets to replace or extend page areas without rewriting the full scaffold.",
        "",
    ]
    for item in section_files:
        lines.append(f"## {item['title']}")
        lines.append("")
        lines.append(f"- File: `{item['file']}`")
        lines.append(f"- Purpose: {item['description']}")
        if item.get("source_refs"):
            lines.append("- Source refs:")
            for ref in item["source_refs"]:
                lines.append(f"  - `{ref}`")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def build_sources_index(section_files: list[dict]) -> str:
    lines = [
        "# SF5 Section Source Map",
        "",
        "Use this file when a generated section should be checked against upstream SF5 sources.",
        "",
    ]
    for item in section_files:
        refs = item.get("source_refs") or []
        if not refs:
            continue
        lines.append(f"## {item['title']}")
        lines.append("")
        lines.append(f"- Section file: `{item['file']}`")
        lines.append("- Upstream refs:")
        for ref in refs:
            lines.append(f"  - `{ref}`")
        lines.append("")
    if len(lines) == 4:
        lines.append("No upstream refs recorded for this working set.")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def build_upstream_index(upstream_files: list[dict]) -> str:
    lines = [
        "# SF5 Upstream Snippets",
        "",
        "These files contain normalized snippets extracted from upstream SF5 examples.",
        "",
    ]
    for item in upstream_files:
        lines.append(f"## {item['id']}")
        lines.append("")
        lines.append(f"- File: `{item['file']}`")
        if item.get("source_refs"):
            lines.append("- Source refs:")
            for ref in item["source_refs"]:
                lines.append(f"  - `{ref}`")
        lines.append("")
    if len(lines) == 4:
        lines.append("No upstream snippets were extracted for this working set.")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def build_reference_index(route: dict) -> str:
    lines = [
        "# SF5 Working Set References",
        "",
        "Always read these first:",
        "",
        "- `references/execution-workflow.md`",
        "- `references/activity-routing-overview.md`",
        "- `references/sf5-fast-start.md`",
        "- `references/source-inventory.md`",
        "",
    ]
    activity = route.get("activity") or {}
    packs = activity.get("knowledge_packs") or []
    if packs:
        lines.append("Activity knowledge packs:")
        lines.append("")
        for item in packs:
            lines.append(f"- `{item}`")
        lines.append("")

    if route.get("scenario_doc"):
        lines.append("Primary scenario:")
        lines.append("")
        lines.append(f"- `{route['scenario_doc']}`")
        lines.append("")

    if route.get("page_recipe"):
        lines.append("Primary page recipe:")
        lines.append("")
        lines.append(f"- `{route['page_recipe']}`")
        lines.append("")

    playbooks = route.get("pattern_playbooks") or []
    if playbooks:
        lines.append("Pattern playbooks:")
        lines.append("")
        for item in playbooks:
            lines.append(f"- `{item}`")
        lines.append("")

    alternatives = route.get("alternatives") or []
    if alternatives:
        lines.append("Nearby alternatives:")
        lines.append("")
        for item in alternatives:
            lines.append(
                f"- `{item['scenario_id']}` -> `{item['scenario_doc']}`"
            )
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def build_bundle_readme(query: str, route: dict, files: dict[str, str]) -> str:
    lines = [
        "# SF5 Working Set",
        "",
        f"- Query: `{query}`",
        f"- Matched route: `{route.get('matched', False)}`",
    ]

    if route.get("scenario_id"):
        lines.append(f"- Scenario: `{route['scenario_id']}`")
    if route.get("recipe_type"):
        lines.append(f"- Recipe type: `{route['recipe_type']}`")
    activity = route.get("activity") or {}
    if activity.get("activity_id"):
        lines.append(f"- Activity: `{activity['activity_id']}`")

    lines.extend(
        [
            "",
            "Generated files:",
            "",
        ]
    )
    for label, rel_path in files.items():
        lines.append(f"- `{label}`: `{rel_path}`")

    lines.extend(
        [
            "",
            "Recommended order:",
            "",
            "1. Read `task-brief.md`.",
            "2. Read `references.md`.",
            "3. Read `sections.md` if it exists and pick useful section variants.",
            "4. Start from `scaffold.html` if it exists.",
            "5. Adapt markup to the real project task.",
            "6. Validate with `validate_sf5_html_files.py --strict --catalog-strict`.",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate an SF5 working set directory.")
    parser.add_argument("query", help="Free-form task description")
    parser.add_argument("--out-dir", required=True, help="Directory for generated artifacts")
    parser.add_argument("--theme", choices=["light", "dark"], default="light")
    parser.add_argument("--title", default="", help="Optional scaffold title override")
    args = parser.parse_args()

    repo_root = root_dir_from_script()
    skill = skill_dir_from_script()
    global SECTION_VARIANTS_BY_RECIPE, LEGACY_EXTRACTED_CLASS_MAP
    SECTION_VARIANTS_BY_RECIPE, LEGACY_EXTRACTED_CLASS_MAP = load_working_set_manifests(skill)
    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

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
    route_json_path = out_dir / "route.json"
    write_text(route_json_path, json.dumps(route, ensure_ascii=False, indent=2) + "\n")
    activity = route.get("activity") or {}
    activity_json_path = out_dir / "activity.json"
    if activity:
        write_text(activity_json_path, json.dumps(activity, ensure_ascii=False, indent=2) + "\n")

    task_json_path = out_dir / "task.json"
    task_json_cmd = [
        sys.executable,
        str(skill / "scripts/prepare_sf5_task.py"),
        args.query,
        "--format",
        "json",
    ]
    if args.title:
        task_json_cmd.extend(["--title", args.title])
    task_json_result = run(task_json_cmd)
    if task_json_result.returncode != 0:
        sys.stderr.write(task_json_result.stderr or task_json_result.stdout)
        return task_json_result.returncode
    write_text(task_json_path, task_json_result.stdout)

    task_brief_path = out_dir / "task-brief.md"
    task_brief_cmd = [
        sys.executable,
        str(skill / "scripts/prepare_sf5_task.py"),
        args.query,
    ]
    if args.title:
        task_brief_cmd.extend(["--title", args.title])
    task_brief_result = run(task_brief_cmd)
    if task_brief_result.returncode != 0:
        sys.stderr.write(task_brief_result.stderr or task_brief_result.stdout)
        return task_brief_result.returncode
    write_text(task_brief_path, task_brief_result.stdout)

    scaffold_path = None
    recipe_type = route.get("recipe_type")
    if route.get("matched") and recipe_type:
        scaffold_cmd = [
            sys.executable,
            str(skill / "scripts/generate_page_scaffold.py"),
            "--type",
            recipe_type,
            "--theme",
            args.theme,
            "--out",
            str(out_dir / "scaffold.html"),
        ]
        if args.title:
            scaffold_cmd.extend(["--title", args.title])
        scaffold_result = run(scaffold_cmd)
        if scaffold_result.returncode != 0:
            sys.stderr.write(scaffold_result.stderr or scaffold_result.stdout)
            return scaffold_result.returncode
        scaffold_path = out_dir / "scaffold.html"

    section_files = write_section_variants(out_dir, recipe_type)
    upstream_files = write_upstream_variants(out_dir, recipe_type, repo_root)

    references_path = out_dir / "references.md"
    write_text(references_path, build_reference_index(route))
    sections_index_path = out_dir / "sections.md"
    sources_index_path = out_dir / "sources.md"
    upstream_index_path = out_dir / "upstream.md"
    if section_files:
        write_text(sections_index_path, build_sections_index(section_files))
        write_text(sources_index_path, build_sources_index(section_files))
    if upstream_files:
        write_text(upstream_index_path, build_upstream_index(upstream_files))

    files: dict[str, str] = {
        "route_json": route_json_path.name,
        "task_json": task_json_path.name,
        "task_brief": task_brief_path.name,
        "references": references_path.name,
    }
    if activity:
        files["activity_json"] = activity_json_path.name
    if scaffold_path:
        files["scaffold"] = scaffold_path.name
    if section_files:
        files["sections_index"] = sections_index_path.name
        files["sources_index"] = sources_index_path.name
        files["sections_dir"] = "sections/"
    if upstream_files:
        files["upstream_index"] = upstream_index_path.name
        files["upstream_dir"] = "upstream/"

    manifest = {
        "query": args.query,
        "theme": args.theme,
        "title": args.title,
        "route": route,
        "activity": activity,
        "files": files,
        "section_variants": section_files,
        "upstream_variants": upstream_files,
    }
    manifest_path = out_dir / "manifest.json"
    write_text(manifest_path, json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    files["manifest"] = manifest_path.name

    readme_path = out_dir / "README.md"
    write_text(readme_path, build_bundle_readme(args.query, route, files))

    print(f"Wrote working set to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
