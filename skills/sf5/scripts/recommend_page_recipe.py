#!/usr/bin/env python3
"""
Recommend SF5 page recipe and required utility groups from free-form prompt.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple


ROUTES = {
    "auth": {
        "keywords": [
            "login",
            "signin",
            "sign in",
            "register",
            "signup",
            "sign up",
            "auth",
            "password reset",
            "forgot password",
        ],
        "recipe": "references/page-recipe-auth.md",
        "groups": [
            "layout",
            "forms",
            "typography",
            "indents",
            "interactivity",
            "border",
        ],
    },
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
    "catalog-empty": {
        "keywords": [
            "no results",
            "empty catalog",
            "empty state",
            "пуст",
            "нет результатов",
            "ничего не найдено",
        ],
        "recipe": "references/page-recipe-catalog-empty.md",
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
    "dashboard-table": {
        "keywords": [
            "table dashboard",
            "data table",
            "orders dashboard",
            "оператор",
            "таблица заказов",
            "workspace table",
        ],
        "recipe": "references/page-recipe-dashboard-table.md",
        "groups": [
            "layout",
            "grid",
            "tables",
            "forms",
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
    "profile": {
        "keywords": [
            "profile",
            "settings",
            "account",
            "preferences",
            "avatar",
            "notification",
            "security settings",
        ],
        "recipe": "references/page-recipe-profile.md",
        "groups": [
            "layout",
            "grid",
            "forms",
            "indents",
            "border",
            "interactivity",
            "typography",
        ],
    },
}

ACTIVITY_HINT = {
    "activity_id": "recipe-scaffold-maintenance",
    "required_specialists": [
        "task-goal",
        "recipe-scaffold",
        "validation-qa",
    ],
}


def classify(prompt: str) -> Tuple[str, Dict]:
    p = prompt.lower()
    if (
        ("catalog" in p or "каталог" in p)
        and (
            "empty state" in p
            or "empty" in p
            or "no results" in p
            or "нет результатов" in p
            or "ничего не найдено" in p
            or "пуст" in p
        )
    ):
        return "catalog-empty", ROUTES["catalog-empty"]
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


def build_payload(route_name: str, route: Dict, pages: Dict[str, List[str]]) -> Dict:
    return {
        "matched": route_name != "fallback",
        "route": route_name,
        "recipe": route["recipe"],
        "required_utility_groups": route["groups"],
        "supporting_doc_pages": pages,
        "activity_hint": ACTIVITY_HINT,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Recommend SF5 page recipe from prompt.")
    parser.add_argument("--manifest", required=True, help="Path to ui-doc-manifest.json")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("prompt", help="Free-form prompt")
    args = parser.parse_args()

    manifest_path = Path(args.manifest).expanduser().resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    route_name, route = classify(args.prompt)
    pages = pick_pages(manifest, route["groups"], per_group=3)
    payload = build_payload(route_name, route, pages)

    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

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
