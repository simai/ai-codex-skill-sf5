#!/usr/bin/env python3
"""
Generate SF5 page scaffold from page recipes.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


RECIPE_BY_TYPE = {
    "auth": "page-recipe-auth.md",
    "landing": "page-recipe-landing.md",
    "catalog": "page-recipe-catalog.md",
    "catalog-empty": "page-recipe-catalog-empty.md",
    "dashboard": "page-recipe-dashboard.md",
    "dashboard-table": "page-recipe-dashboard-table.md",
    "article": "page-recipe-article.md",
    "checkout": "page-recipe-checkout.md",
    "profile": "page-recipe-profile.md",
}

ACTIVITY_HINT = {
    "activity_id": "recipe-scaffold-maintenance",
    "required_specialists": [
        "task-goal",
        "recipe-scaffold",
        "validation-qa",
    ],
}


def skill_root_from_script() -> Path:
    # scripts/<file>.py -> skill_root
    return Path(__file__).resolve().parents[1]


def extract_html_block(md_text: str) -> str:
    m = re.search(r"```html\s*(.*?)\s*```", md_text, flags=re.DOTALL)
    if not m:
        raise ValueError("No ```html code block found in recipe file.")
    return m.group(1).strip() + "\n"


def apply_theme(html: str, theme: str) -> str:
    if theme not in {"light", "dark"}:
        return html
    target = f"theme-{theme}"
    other = "theme-dark" if theme == "light" else "theme-light"
    html = re.sub(rf"\b{re.escape(other)}\b", target, html)
    if "theme-light" not in html and "theme-dark" not in html:
        html = re.sub(
            r'(<main\b[^>]*class=")([^"]*)(")',
            lambda m: f'{m.group(1)}{target} {m.group(2)}{m.group(3)}',
            html,
            count=1,
        )
    return html


def apply_title(html: str, title: str) -> str:
    if not title:
        return html
    # replace first h1 text
    m = re.search(r"(<h1\b[^>]*>)(.*?)(</h1>)", html, flags=re.DOTALL)
    if not m:
        return html
    return html[: m.start()] + f"{m.group(1)}{title}{m.group(3)}" + html[m.end() :]


def wrap_full_document(snippet: str, title: str) -> str:
    safe_title = title or "SF5 Page"
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate SF5 page scaffold from recipe.")
    parser.add_argument(
        "--type",
        required=True,
        choices=sorted(RECIPE_BY_TYPE.keys()),
        help="Page recipe type",
    )
    parser.add_argument("--theme", choices=["light", "dark"], default="light")
    parser.add_argument("--title", default="", help="Override first <h1> text and document title")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--snippet-only", action="store_true", help="Print only recipe snippet")
    parser.add_argument("--out", default="", help="Output file path (default: stdout)")
    args = parser.parse_args()

    root = skill_root_from_script()
    recipe_path = root / "references" / RECIPE_BY_TYPE[args.type]
    md_text = recipe_path.read_text(encoding="utf-8")

    html = extract_html_block(md_text)
    html = apply_theme(html, args.theme)
    html = apply_title(html, args.title)

    output = html if args.snippet_only else wrap_full_document(html, args.title or args.type.title())
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
            "kind": "page",
            "recipe_type": args.type,
            "recipe_path": str(recipe_path),
            "theme": args.theme,
            "snippet_only": args.snippet_only,
            "activity_hint": ACTIVITY_HINT,
        }
        if out_path:
            payload["output_file"] = str(out_path)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
