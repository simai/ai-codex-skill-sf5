#!/usr/bin/env python3
"""
Recommend the most relevant SF5 product scenario references for a free-form request.
"""

from __future__ import annotations

import argparse
import json
import re

ACTIVITY_HINT = {
    "activity_id": "working-set-maintenance",
    "required_specialists": [
        "task-goal",
        "working-set",
        "validation-qa",
    ],
}


SCENARIOS = [
    {
        "id": "auth",
        "path": "references/scenario-auth.md",
        "keywords": [
            "login", "sign in", "sign-in", "register", "sign up", "signup",
            "reset password", "auth", "authentication", "forgot password",
            "вход", "авторизация", "регистрация", "сброс пароля", "забыли пароль",
        ],
    },
    {
        "id": "catalog-listing",
        "path": "references/scenario-catalog-listing.md",
        "keywords": [
            "catalog", "listing", "product list", "search", "filters",
            "sidebar filter", "results", "cards", "sort",
            "каталог", "товары", "поиск", "фильтры", "сортировка", "результаты",
        ],
    },
    {
        "id": "checkout-flow",
        "path": "references/scenario-checkout-flow.md",
        "keywords": [
            "checkout", "cart", "order", "delivery", "payment",
            "summary", "place order", "billing",
            "оформление заказа", "корзина", "заказ", "доставка", "оплата", "итог",
        ],
    },
    {
        "id": "profile-settings",
        "path": "references/scenario-profile-settings.md",
        "keywords": [
            "profile", "settings", "preferences", "account", "avatar",
            "notification", "security settings", "personal data",
            "профиль", "настройки", "предпочтения", "аккаунт", "аватар",
            "уведомления", "настройки безопасности", "личные данные",
        ],
    },
    {
        "id": "dashboard-workspace",
        "path": "references/scenario-dashboard-workspace.md",
        "keywords": [
            "dashboard", "workspace", "admin", "kpi", "table", "activity",
            "analytics", "metrics", "operator",
            "дашборд", "рабочее пространство", "админка", "таблица", "активность",
            "аналитика", "метрики", "оператор",
        ],
    },
    {
        "id": "article-content",
        "path": "references/scenario-article-content.md",
        "keywords": [
            "article", "content page", "blog", "editorial", "knowledge base",
            "table of contents", "toc", "related posts", "related content",
            "long form", "long-form", "reading",
            "статья", "контентная страница", "блог", "база знаний", "оглавление",
            "похожие материалы", "похожие статьи", "длинное чтение",
        ],
    },
]


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[_/,+.-]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def score(text: str, keywords: list[str]) -> tuple[int, list[str]]:
    hits = []
    total = 0
    for kw in keywords:
        if kw in text:
            hits.append(kw)
            total += len(kw.split())
    return total, hits


def main() -> int:
    parser = argparse.ArgumentParser(description="Recommend SF5 product scenarios.")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("query", help="Free-form task description")
    args = parser.parse_args()

    text = normalize(args.query)
    ranked = []
    for scenario in SCENARIOS:
        s, hits = score(text, scenario["keywords"])
        if s > 0:
            ranked.append((s, scenario, hits))
    ranked.sort(key=lambda item: (-item[0], item[1]["id"]))

    if args.format == "json":
        if not ranked:
            payload = {
                "matched": False,
                "fallback_docs": ["references/product-scenarios.md"],
                "results": [],
                "activity_hint": ACTIVITY_HINT,
            }
        else:
            payload = {
                "matched": True,
                "results": [
                    {
                        "id": scenario["id"],
                        "path": scenario["path"],
                        "score": s,
                        "keywords": hits,
                    }
                    for s, scenario, hits in ranked[:3]
                ],
                "activity_hint": ACTIVITY_HINT,
            }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    if not ranked:
        print("No direct scenario match.")
        print("Fallback: references/product-scenarios.md")
        return 0

    for s, scenario, hits in ranked[:3]:
        print(f"{scenario['id']}\t{s}\t{scenario['path']}\tkeywords={', '.join(hits)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
