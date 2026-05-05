#!/usr/bin/env python3
"""
Recommend an SF5 coordinator activity, specialists, and gate set for a free-form task.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROLE_BIAS = {
    "task-goal": "author",
    "skill-maintainer": "author",
    "source-sync": "author",
    "routing-orchestrator": "author",
    "recipe-scaffold": "author",
    "working-set": "author",
    "tailwind-converter": "author",
    "validation-qa": "gatekeeper",
    "docs-learning": "reviewer",
}

ACTIVITY_NOTES = {
    "source-refresh": [
        "source-refresh gate",
        "verify source mirror paths and rebuild source-backed artifacts",
    ],
    "routing-maintenance": [
        "routing regression gate",
        "update fixtures before closing ranking changes",
    ],
    "recipe-scaffold-maintenance": [
        "scaffold compatibility gate",
        "validate generated scaffold output after recipe changes",
    ],
    "working-set-maintenance": [
        "working-set gate",
        "verify source refs, upstream extracts, and generated manifest contract",
    ],
    "tailwind-conversion": [
        "tailwind conversion gate",
        "map only verified classes and report unmapped Tailwind residue",
    ],
    "validation-hardening": [
        "validation hardening gate",
        "prove the change with the narrowest fixture layer first",
    ],
    "documentation-update": [
        "docs cross-link gate",
        "keep entrypoints and usage docs aligned with current behavior",
    ],
    "skill-architecture-update": [
        "coordinator consistency gate",
        "keep manifests, specialists, rules, and entrypoints aligned",
    ],
}


def skill_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[_/,+.-]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_activity_manifests(skill_root: Path) -> list[dict]:
    registry = load_json(skill_root / "activities" / "activity-registry.json")
    return [
        load_json(skill_root / "activities" / f"{activity_id}.json")
        for activity_id in registry["activities"]
    ]


def has_any(text: str, phrases: list[str]) -> bool:
    return any(phrase in text for phrase in phrases)


def score_from_triggers(text: str, manifest: dict) -> tuple[int, list[str]]:
    score = 0
    hits = []
    for trigger in manifest.get("triggers", []):
        if trigger in text:
            hits.append(trigger)
            score += max(1, len(trigger.split()))
    return score, hits


def apply_activity_heuristics(text: str, activity_id: str, score: int, hits: list[str]) -> tuple[int, list[str]]:
    bonus_hits = []

    if activity_id == "source-refresh":
        if has_any(text, ["ui-play", "ui-smart", "ui-doc", "ui repo", "upstream", "mirror", "inventory", "playground", "новые компоненты", "обновились репозитории"]):
            score += 3
            bonus_hits.append("source-drift-intent")

    if activity_id == "routing-maintenance":
        if has_any(text, ["route", "routing", "scenario", "ranking", "matcher", "recipe routing", "fixtures", "роутинг", "маршрутизация", "ранжирование", "фикстуры"]):
            score += 3
            bonus_hits.append("routing-intent")

    if activity_id == "recipe-scaffold-maintenance":
        if has_any(text, ["scaffold", "recipe", "template", "page recipe", "component scaffold", "template update", "шаблон", "рецепт", "скелет страницы"]):
            score += 3
            bonus_hits.append("scaffold-intent")

    if activity_id == "working-set-maintenance":
        if has_any(text, ["working set", "upstream extract", "section variants", "bundle generation", "manifest", "sections", "sources.md", "upstream.md", "рабочий пакет", "апстрим сниппеты"]):
            score += 4
            bonus_hits.append("working-set-intent")
        if has_any(text, ["page", "screen", "layout", "profile", "checkout", "catalog", "dashboard", "article", "login", "auth", "account", "preferences", "form", "workspace", "table", "orders", "search", "status", "statuses", "страница", "экран", "профиль", "оформление заказа", "каталог", "дашборд", "статья", "вход", "таблица", "заказы", "поиск", "статусы", "форма"]):
            score += 3
            bonus_hits.append("page-implementation-intent")

    if activity_id == "tailwind-conversion":
        if has_any(text, ["tailwind", "tailwindcss", "tailwind ui", "tailwind plus", "convert tailwind", "tailwind to sf5", "application ui", "конвертировать tailwind", "tailwind в sf5", "перенести tailwind"]):
            score += 7
            bonus_hits.append("tailwind-conversion-intent")
        if has_any(text, ["convert", "conversion", "migrate", "migration", "перенести", "конвертировать", "миграция"]) and has_any(text, ["class", "classes", "markup", "html", "utilities", "классы", "разметка"]):
            score += 2
            bonus_hits.append("class-conversion-intent")

    if activity_id == "validation-hardening":
        if has_any(text, ["validator", "validation", "fixture", "regression", "checks", "smoke", "strict", "валидатор", "проверки", "регрессия", "смоук"]):
            score += 4
            bonus_hits.append("validation-intent")

    if activity_id == "documentation-update":
        doc_surface = has_any(text, ["docs", "readme", "guide", "reference map", "atlas", "usage", "документация", "гайд", "справка"])
        doc_action = has_any(text, ["update", "refresh", "rewrite", "обнови", "обновить", "перепиши", "актуализируй"])
        if "readme" in text or (doc_surface and doc_action):
            score += 5
            bonus_hits.append("docs-intent")

    if activity_id == "skill-architecture-update":
        if has_any(text, ["specialists", "expert system", "activity manifests", "skill architecture", "специалисты", "архитектура скила", "экспертная система"]):
            score += 5
            bonus_hits.append("architecture-intent")
        elif has_any(text, ["coordinator", "council", "координатор", "совет ролей"]):
            score += 2
            bonus_hits.append("coordinator-intent")

    return score, hits + bonus_hits


def build_specialist_roles(activity_id: str, required: list[str], optional: list[str]) -> list[dict]:
    roles = []
    for name in required:
        role = ROLE_BIAS.get(name, "author")
        if name == "validation-qa":
            role = "gatekeeper"
        roles.append({"name": name, "role": role, "required": True})
    for name in optional:
        roles.append({"name": name, "role": ROLE_BIAS.get(name, "consulted"), "required": False})
    return roles


def build_payload(best: dict, hits: list[str], ranked: list[tuple[int, dict, list[str]]]) -> dict:
    activity_id = best["activity_id"]
    required = best.get("required_specialists", [])
    optional = best.get("optional_specialists", [])
    return {
        "matched": True,
        "activity_id": activity_id,
        "title": best["title"],
        "matched_signals": hits,
        "required_specialists": required,
        "optional_specialists": optional,
        "specialist_roles": build_specialist_roles(activity_id, required, optional),
        "required_rules": best.get("required_rules", []),
        "required_outputs": best.get("required_outputs", []),
        "knowledge_packs": best.get("knowledge_packs", []),
        "gate_rules": best.get("gate_rules", []),
        "workflow": best.get("workflow", []),
        "gate_notes": ACTIVITY_NOTES.get(activity_id, []),
        "alternatives": [
            {
                "activity_id": item["activity_id"],
                "score": score,
                "title": item["title"],
                "signals": alt_hits,
            }
            for score, item, alt_hits in ranked[1:3]
            if score > 0
        ],
    }


def build_fallback() -> dict:
    return {
        "matched": False,
        "fallback_docs": [
            "rules/routing.md",
            "references/activity-routing-overview.md",
            "references/execution-workflow.md",
        ],
    }


def format_markdown(payload: dict, query: str) -> str:
    if not payload.get("matched"):
        return "\n".join(
            [
                "# SF5 Activity Recommendation",
                "",
                f"- Query: `{query}`",
                "- No confident activity match.",
                "",
                "Fallback docs:",
                "",
                *[f"- `{item}`" for item in payload.get("fallback_docs", [])],
                "",
            ]
        )

    lines = [
        "# SF5 Activity Recommendation",
        "",
        f"- Query: `{query}`",
        f"- Activity: `{payload['activity_id']}`",
        f"- Title: {payload['title']}",
        "",
        "## Required Specialists",
        "",
    ]
    for item in payload["specialist_roles"]:
        if item["required"]:
            lines.append(f"- `{item['name']}` as `{item['role']}`")
    lines.extend(["", "## Gate Rules", ""])
    for item in payload["gate_rules"]:
        lines.append(f"- `{item}`")
    lines.extend(["", "## Workflow", ""])
    for item in payload["workflow"]:
        lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Recommend an SF5 coordinator activity.")
    parser.add_argument("query", help="Free-form task description")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    manifests = load_activity_manifests(skill_root_from_script())
    text = normalize(args.query)

    ranked = []
    for manifest in manifests:
        score, hits = score_from_triggers(text, manifest)
        score, hits = apply_activity_heuristics(text, manifest["activity_id"], score, hits)
        ranked.append((score, manifest, hits))
    ranked.sort(key=lambda item: item[0], reverse=True)

    best_score, best, hits = ranked[0]
    payload = build_fallback() if best_score <= 0 else build_payload(best, hits, ranked)

    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(format_markdown(payload, args.query))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
