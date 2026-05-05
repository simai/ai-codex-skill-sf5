#!/usr/bin/env python3
"""
Recommend a top-level SF5 route: product scenario, page recipe, and pattern playbooks.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


SCENARIOS = [
    {
        "id": "auth",
        "doc": "references/scenario-auth.md",
        "recipe": "references/page-recipe-auth.md",
        "recipe_type": "auth",
        "patterns": [
            "references/pattern-forms-inputs.md",
            "references/pattern-feedback-overlays.md",
        ],
        "keywords": [
            "login", "sign in", "sign-in", "register", "sign up", "signup",
            "reset password", "auth", "authentication", "forgot password",
            "вход", "авторизация", "регистрация", "сброс пароля", "забыли пароль",
        ],
    },
    {
        "id": "catalog-empty",
        "doc": "references/scenario-catalog-listing.md",
        "recipe": "references/page-recipe-catalog-empty.md",
        "recipe_type": "catalog-empty",
        "patterns": [
            "references/pattern-dropdown-selection.md",
            "references/pattern-pagination-filters.md",
            "references/pattern-feedback-overlays.md",
        ],
        "keywords": [
            "empty catalog", "no results", "empty state", "нет результатов",
            "ничего не найдено", "пустой каталог", "пустая выдача",
        ],
    },
    {
        "id": "catalog-listing",
        "doc": "references/scenario-catalog-listing.md",
        "recipe": "references/page-recipe-catalog.md",
        "recipe_type": "catalog",
        "patterns": [
            "references/pattern-dropdown-selection.md",
            "references/pattern-pagination-filters.md",
            "references/pattern-feedback-overlays.md",
        ],
        "keywords": [
            "catalog", "listing", "product list", "search", "filters",
            "sidebar filter", "results", "cards", "sort",
            "каталог", "товары", "поиск", "фильтры", "сортировка", "результаты",
        ],
    },
    {
        "id": "checkout-flow",
        "doc": "references/scenario-checkout-flow.md",
        "recipe": "references/page-recipe-checkout.md",
        "recipe_type": "checkout",
        "patterns": [
            "references/pattern-forms-inputs.md",
            "references/pattern-dropdown-selection.md",
            "references/pattern-feedback-overlays.md",
        ],
        "keywords": [
            "checkout", "cart", "order", "delivery", "payment",
            "summary", "place order", "billing",
            "оформление заказа", "корзина", "заказ", "доставка", "оплата", "итог",
        ],
    },
    {
        "id": "article-content",
        "doc": "references/scenario-article-content.md",
        "recipe": "references/page-recipe-article.md",
        "recipe_type": "article",
        "patterns": [
            "references/pattern-playbooks.md",
            "references/pattern-feedback-overlays.md",
        ],
        "keywords": [
            "article", "content page", "blog", "editorial", "knowledge base",
            "table of contents", "toc", "related posts", "related content",
            "long form", "long-form", "reading",
            "статья", "контентная страница", "блог", "база знаний", "оглавление",
            "похожие материалы", "похожие статьи", "длинное чтение",
        ],
    },
    {
        "id": "profile-settings",
        "doc": "references/scenario-profile-settings.md",
        "recipe": "references/page-recipe-profile.md",
        "recipe_type": "profile",
        "patterns": [
            "references/pattern-forms-inputs.md",
            "references/pattern-upload-and-progress.md",
            "references/pattern-feedback-overlays.md",
        ],
        "keywords": [
            "profile", "settings", "preferences", "account", "avatar",
            "notification", "security settings", "personal data",
            "профиль", "настройки", "предпочтения", "аккаунт", "аватар",
            "уведомления", "настройки безопасности", "личные данные",
        ],
    },
    {
        "id": "dashboard-table",
        "doc": "references/scenario-dashboard-workspace.md",
        "recipe": "references/page-recipe-dashboard-table.md",
        "recipe_type": "dashboard-table",
        "patterns": [
            "references/pattern-pagination-filters.md",
            "references/pattern-feedback-overlays.md",
        ],
        "keywords": [
            "table dashboard", "data table", "orders dashboard", "operator",
            "таблица заказов", "workspace table",
            "дашборд с таблицей", "таблица", "операторский стол",
        ],
    },
    {
        "id": "dashboard-workspace",
        "doc": "references/scenario-dashboard-workspace.md",
        "recipe": "references/page-recipe-dashboard.md",
        "recipe_type": "dashboard",
        "patterns": [
            "references/pattern-pagination-filters.md",
            "references/pattern-feedback-overlays.md",
        ],
        "keywords": [
            "dashboard", "workspace", "admin", "kpi", "activity",
            "analytics", "metrics",
            "дашборд", "рабочее пространство", "админка", "активность", "метрики", "аналитика",
        ],
    },
]


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[_/,+.-]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def skill_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def run_activity(query: str) -> dict:
    skill_root = skill_root_from_script()
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


def score_keywords(text: str, keywords: list[str]) -> tuple[int, list[str]]:
    hits = []
    score = 0
    for kw in keywords:
        if kw in text:
            hits.append(kw)
            score += len(kw.split())
    return score, hits


def has_any(text: str, phrases: list[str]) -> bool:
    return any(phrase in text for phrase in phrases)


def score_scenario(text: str, scenario: dict) -> tuple[int, list[str]]:
    score, hits = score_keywords(text, scenario["keywords"])
    bonus_hits = []
    toc_intent = has_any(text, ["table of contents", "toc", "оглавление"])

    if scenario["id"] == "dashboard-table":
        if has_any(text, ["table", "data table", "orders dashboard", "workspace table", "таблица", "дашборд с таблицей"]) and not toc_intent:
            score += 3
            bonus_hits.append("table-intent")
        if has_any(text, ["status", "search", "filter", "filters", "статусы", "поиск", "фильтр", "фильтры"]) and has_any(
            text, ["table", "dashboard", "workspace", "admin", "order", "orders", "таблица", "дашборд", "админка", "заказы"]
        ) and not toc_intent:
            score += 3
            bonus_hits.append("table-filter-intent")
        if has_any(text, ["dashboard", "workspace", "admin", "дашборд", "рабочее пространство", "админка"]) and has_any(
            text, ["table", "status", "search", "filter", "filters", "таблица", "статусы", "поиск", "фильтр", "фильтры"]
        ) and not toc_intent:
            score += 2
            bonus_hits.append("dashboard-table-intent")
        if has_any(text, ["kpi", "activity", "analytics", "metrics", "cards", "активность", "аналитика", "метрики", "карточки"]):
            score -= 2
            bonus_hits.append("table-penalty-mixed-dashboard")

    if scenario["id"] == "dashboard-workspace":
        if has_any(text, ["dashboard", "workspace", "admin", "дашборд", "рабочее пространство", "админка"]) and has_any(
            text, ["kpi", "activity", "analytics", "metrics", "table", "filters", "активность", "аналитика", "метрики", "таблица", "фильтры"]
        ):
            score += 2
            bonus_hits.append("dashboard-intent")
        if has_any(text, ["kpi", "activity", "analytics", "metrics", "активность", "аналитика", "метрики"]):
            score += 2
            bonus_hits.append("dashboard-signals")
        if has_any(text, ["kpi", "activity", "cards", "активность", "карточки"]) and has_any(
            text, ["table", "filter", "filters", "search", "таблица", "фильтр", "фильтры", "поиск"]
        ):
            score += 3
            bonus_hits.append("mixed-dashboard-intent")

    if scenario["id"] == "catalog-listing":
        catalog_signals = has_any(
            text,
            ["catalog", "listing", "product", "products", "results", "cards", "sort", "каталог", "товары", "результаты", "карточки", "сортировка"],
        )
        if has_any(text, ["search", "filter", "filters", "поиск", "фильтр", "фильтры"]) and catalog_signals:
            score += 1
            bonus_hits.append("catalog-intent")
        if has_any(text, ["dashboard", "workspace", "admin", "table", "kpi", "activity", "дашборд", "админка", "таблица", "метрики", "активность"]) and not catalog_signals:
            score -= 2
            bonus_hits.append("catalog-penalty-non-catalog")

    if scenario["id"] == "catalog-empty":
        if has_any(text, ["empty state", "no results", "nothing found", "нет результатов", "ничего не найдено", "пустая выдача"]):
            score += 3
            bonus_hits.append("catalog-empty-intent")
        if has_any(text, ["catalog", "filters", "reset", "clear", "каталог", "фильтры", "сброс", "очистить"]) and has_any(
            text, ["empty state", "no results", "nothing found", "empty catalog", "пустой каталог", "пустая выдача"]
        ):
            score += 2
            bonus_hits.append("catalog-empty-actions")

    if scenario["id"] == "checkout-flow":
        if has_any(text, ["checkout", "payment", "delivery", "billing", "summary", "оформление заказа", "оплата", "доставка", "итог"]):
            score += 2
            bonus_hits.append("checkout-intent")

    if scenario["id"] == "profile-settings":
        if has_any(text, ["profile", "settings", "preferences", "avatar", "notification", "профиль", "настройки", "аватар", "уведомления"]):
            score += 2
            bonus_hits.append("profile-intent")

    if scenario["id"] == "auth":
        if has_any(text, ["login", "sign in", "register", "forgot password", "auth", "вход", "авторизация", "регистрация", "забыли пароль"]):
            score += 2
            bonus_hits.append("auth-intent")

    if scenario["id"] == "article-content":
        if has_any(text, ["article", "content page", "blog", "editorial", "knowledge base", "статья", "контентная страница", "блог", "база знаний"]):
            score += 2
            bonus_hits.append("article-intent")
        if toc_intent or has_any(text, ["related posts", "related content", "long form", "long-form", "похожие материалы", "похожие статьи", "длинное чтение"]):
            score += 3
            bonus_hits.append("article-structure-intent")

    return score, hits + bonus_hits


def build_fallback_payload() -> dict:
    return {
        "matched": False,
        "fallback_docs": [
            "references/sf5-fast-start.md",
            "references/page-layout-playbook.md",
            "references/source-inventory.md",
        ],
    }


def build_payload(best: dict, hits: list[str], ranked: list[tuple[int, dict, list[str]]], activity: dict) -> dict:
    payload = {
        "matched": True,
        "scenario_id": best["id"],
        "scenario_doc": best["doc"],
        "scenario_keywords": hits,
        "page_recipe": best["recipe"],
        "recipe_type": best["recipe_type"],
        "scaffold_command": (
            "python3 skills/sf5/scripts/generate_page_scaffold.py "
            f"--type {best['recipe_type']} --snippet-only"
        ),
        "pattern_playbooks": best["patterns"],
        "workflow": [
            "Read scenario doc",
            "Generate starter scaffold",
            "Read listed pattern playbooks",
            "Adapt markup to the project task",
            "Validate with strict HTML checks",
        ],
        "activity": activity,
        "alternatives": [
            {
                "scenario_id": scenario["id"],
                "score": score,
                "scenario_doc": scenario["doc"],
                "scenario_keywords": alt_hits,
            }
            for score, scenario, alt_hits in ranked[1:4]
        ],
    }
    return payload


def print_text_fallback() -> None:
    print("No direct top-level route match.")
    print("Fallback docs:")
    print("  references/sf5-fast-start.md")
    print("  references/page-layout-playbook.md")
    print("  references/source-inventory.md")


def print_text_payload(payload: dict) -> None:
    print(f"scenario_id: {payload['scenario_id']}")
    print(f"scenario_doc: {payload['scenario_doc']}")
    print(f"scenario_keywords: {', '.join(payload['scenario_keywords'])}")
    print(f"page_recipe: {payload['page_recipe']}")
    print(f"recipe_type: {payload['recipe_type']}")
    print(f"scaffold_command: {payload['scaffold_command']}")
    print("pattern_playbooks:")
    for path in payload["pattern_playbooks"]:
        print(f"  - {path}")
    print("workflow:")
    for step_index, item in enumerate(payload["workflow"], start=1):
        print(f"  {step_index}. {item}")
    activity = payload.get("activity") or {}
    if activity.get("activity_id"):
        print("activity:")
        print(f"  - activity_id: {activity['activity_id']}")
        if activity.get("required_specialists"):
            print(f"  - required_specialists: {', '.join(activity['required_specialists'])}")
        if activity.get("gate_rules"):
            print(f"  - gate_rules: {', '.join(activity['gate_rules'])}")
    if payload["alternatives"]:
        print("alternatives:")
        for item in payload["alternatives"]:
            print(
                "  - "
                f"{item['scenario_id']} ({item['score']}) -> "
                f"{item['scenario_doc']} [keywords={', '.join(item['scenario_keywords'])}]"
            )


def main() -> int:
    parser = argparse.ArgumentParser(description="Recommend a top-level SF5 route.")
    parser.add_argument("query", help="Free-form task description")
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format",
    )
    args = parser.parse_args()

    text = normalize(args.query)
    ranked = []
    for scenario in SCENARIOS:
        score, hits = score_scenario(text, scenario)
        if score > 0:
            ranked.append((score, scenario, hits))
    ranked.sort(key=lambda item: (-item[0], item[1]["id"]))

    if not ranked:
        fallback = build_fallback_payload()
        if args.format == "json":
            print(json.dumps(fallback, ensure_ascii=False, indent=2))
        else:
            print_text_fallback()
        return 0

    _best_score, best, hits = ranked[0]
    activity = run_activity(args.query)
    payload = build_payload(best, hits, ranked, activity)
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print_text_payload(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
