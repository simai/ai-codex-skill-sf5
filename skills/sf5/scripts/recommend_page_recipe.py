#!/usr/bin/env python3
"""
Recommend SF5 page recipe and required utility groups from free-form prompt.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple


ROUTES = {
    "landing": {
        "keywords": [
            "landing",
            "лендинг",
            "hero",
            "cta",
            "promo",
            "презентация",
        ],
        "recipe": "references/page-recipe-landing.md",
        "groups": [
            "layout",
            "grid",
            "typography",
            "background",
            "border",
            "indents",
            "interactivity",
        ],
    },
    "catalog": {
        "keywords": [
            "catalog",
            "каталог",
            "listing",
            "карточ",
            "фильтр",
            "сортиров",
            "пагина",
        ],
        "recipe": "references/page-recipe-catalog.md",
        "groups": [
            "layout",
            "grid",
            "forms",
            "indents",
            "border",
            "typography",
            "interactivity",
        ],
    },
    "dashboard": {
        "keywords": [
            "dashboard",
            "дашборд",
            "kpi",
            "метрик",
            "таблиц",
            "widget",
            "admin",
        ],
        "recipe": "references/page-recipe-dashboard.md",
        "groups": [
            "layout",
            "grid",
            "tables",
            "typography",
            "interactivity",
            "border",
            "indents",
        ],
    },
    "article": {
        "keywords": [
            "article",
            "статья",
            "blog",
            "контент",
            "оглавлен",
            "longform",
        ],
        "recipe": "references/page-recipe-article.md",
        "groups": [
            "layout",
            "typography",
            "text-formatting",
            "links",
            "indents",
            "border",
        ],
    },
    "checkout": {
        "keywords": [
            "checkout",
            "чекаут",
            "корзин",
            "order",
            "доставк",
            "оплат",
            "форма",
        ],
        "recipe": "references/page-recipe-checkout.md",
        "groups": [
            "layout",
            "grid",
            "forms",
            "border",
            "outline",
            "interactivity",
            "typography",
        ],
    },
}


def classify(prompt: str) -> Tuple[str, Dict]:
    p = prompt.lower()
    scores = Counter()
    for key, route in ROUTES.items():
        for kw in route["keywords"]:
            if kw in p:
                scores[key] += 1
    if not scores:
        return "fallback", {
            "recipe": "references/page-layout-playbook.md",
            "groups": ["layout", "grid", "typography", "indents", "border"],
        }
    best = scores.most_common(1)[0][0]
    return best, ROUTES[best]


def pick_pages(manifest: List[Dict], groups: List[str], per_group: int = 3) -> Dict[str, List[str]]:
    result: Dict[str, List[str]] = {}
    for g in groups:
        files = [
            r["path"]
            for r in manifest
            if r.get("top") == "utilities" and r.get("utility_group") == g
        ]
        result[g] = sorted(files)[:per_group]
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Recommend SF5 page recipe from prompt.")
    parser.add_argument("--manifest", required=True, help="Path to ui-doc-manifest.json")
    parser.add_argument("prompt", help="Free-form prompt")
    args = parser.parse_args()

    manifest_path = Path(args.manifest).expanduser().resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    route_name, route = classify(args.prompt)
    pages = pick_pages(manifest, route["groups"], per_group=3)

    print(f"route: {route_name}")
    print(f"recipe: {route['recipe']}")
    print("required utility groups:")
    print("  " + ", ".join(route["groups"]))
    print("suggested pages:")
    for g in route["groups"]:
        files = pages.get(g, [])
        if files:
            print(f"  - {g}: " + "; ".join(files))
        else:
            print(f"  - {g}: no direct utility files found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
