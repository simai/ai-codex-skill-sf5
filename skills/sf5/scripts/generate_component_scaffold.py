#!/usr/bin/env python3
"""
Generate SF5 component/smart-component/block scaffold from templates.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, Set


TEMPLATE_BY_KIND = {
    "component": "component-template.md",
    "smart": "smart-component-template.md",
    "block": "block-template.md",
}

ACTIVITY_HINT = {
    "activity_id": "recipe-scaffold-maintenance",
    "required_specialists": [
        "task-goal",
        "recipe-scaffold",
        "validation-qa",
    ],
}

DEFAULT_TITLES = {
    "component": "Component",
    "smart": "Smart Component",
    "block": "Block",
}


def skill_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def extract_html_block(md_text: str) -> str:
    m = re.search(r"```html\s*(.*?)\s*```", md_text, flags=re.DOTALL)
    if not m:
        raise ValueError("No ```html code block found in template file.")
    return m.group(1).strip() + "\n"


def wrap_full_document(snippet: str, title: str) -> str:
    safe_title = title or "SF5 Snippet"
    return (
        "<!doctype html>\n"
        '<html lang="ru">\n'
        "<head>\n"
        '  <meta charset="utf-8" />\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1" />\n'
        f"  <title>{safe_title}</title>\n"
        "  <!-- TODO: connect SF5 CSS/JS loader according to project conventions -->\n"
        "</head>\n"
        "<body>\n"
        f"{snippet.rstrip()}\n"
        "</body>\n"
        "</html>\n"
    )


def load_smart_codes(skill_root: Path) -> Set[str]:
    allowed: Set[str] = set()

    smart_manifest_path = skill_root / "references" / "vendor" / "manifest" / "sf5.smart.json"
    smart_registry_path = (
        skill_root / "references" / "vendor" / "registries" / "smart-codes.json"
    )

    if smart_manifest_path.exists():
        data = json.loads(smart_manifest_path.read_text(encoding="utf-8"))
        for item in data.get("smart", []):
            if isinstance(item, dict):
                sf_code = item.get("sf_code")
                if isinstance(sf_code, str) and sf_code.strip():
                    allowed.add(sf_code.strip())

    if smart_registry_path.exists():
        data = json.loads(smart_registry_path.read_text(encoding="utf-8"))
        for item in data.get("items", []):
            if not isinstance(item, dict):
                continue
            regex_blob = str(item.get("regex", ""))
            for code in re.findall(r'sf-code\s*=\s*["\']([^"\']+)["\']', regex_blob):
                if code.strip():
                    allowed.add(code.strip())

    return allowed


def replace_smart_code(html: str, smart_code: str) -> str:
    if not smart_code:
        return html

    return re.sub(
        r'(sf-code\s*=\s*["\'])([^"\']+)(["\'])',
        rf"\1{smart_code}\3",
        html,
        count=1,
    )


def apply_placeholders(html: str, name: str, title: str) -> str:
    return html.replace("__UNIT_NAME__", name).replace("__UNIT_TITLE__", title)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate SF5 component/smart-component/block scaffold."
    )
    parser.add_argument(
        "--kind",
        required=True,
        choices=sorted(TEMPLATE_BY_KIND.keys()),
        help="Template kind",
    )
    parser.add_argument("--name", default="unit", help="Unit name placeholder value")
    parser.add_argument("--title", default="", help="Unit title placeholder value")
    parser.add_argument(
        "--smart-code",
        default="",
        help="Override sf-code for --kind smart (must exist in vendor registry)",
    )
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--snippet-only", action="store_true", help="Print only snippet")
    parser.add_argument("--out", default="", help="Output file path (default: stdout)")
    args = parser.parse_args()

    skill_root = skill_root_from_script()
    template_path = skill_root / "references" / TEMPLATE_BY_KIND[args.kind]
    md_text = template_path.read_text(encoding="utf-8")
    html = extract_html_block(md_text)

    title = args.title or DEFAULT_TITLES[args.kind]
    html = apply_placeholders(html, name=args.name, title=title)

    if args.kind == "smart" and args.smart_code:
        allowed_codes = load_smart_codes(skill_root)
        if allowed_codes and args.smart_code not in allowed_codes:
            allowed_sorted = ", ".join(sorted(allowed_codes))
            parser.error(
                f"Unknown sf-code `{args.smart_code}`. Allowed values: {allowed_sorted}"
            )
        html = replace_smart_code(html, args.smart_code)

    output = html if args.snippet_only else wrap_full_document(html, title)

    out_path = None
    if args.out:
        out_path = Path(args.out).expanduser().resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output, encoding="utf-8")
        if args.format == "text":
            print(f"Wrote {out_path}")
    elif args.format == "text":
        print(output, end="")

    if args.format == "json":
        payload = {
            "ok": True,
            "kind": args.kind,
            "template_path": str(template_path),
            "unit_name": args.name,
            "unit_title": title,
            "snippet_only": args.snippet_only,
            "activity_hint": ACTIVITY_HINT,
        }
        if args.kind == "smart" and args.smart_code:
            payload["smart_code"] = args.smart_code
        if out_path:
            payload["output_file"] = str(out_path)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
