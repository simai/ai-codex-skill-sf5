#!/usr/bin/env python3
"""
Recommend the most relevant SF5 pattern playbooks for a free-form request.
"""

from __future__ import annotations

import argparse
import json
import re

ACTIVITY_HINT = {
    "activity_id": "recipe-scaffold-maintenance",
    "required_specialists": [
        "task-goal",
        "recipe-scaffold",
        "validation-qa",
    ],
}


PATTERNS = [
    {
        "id": "forms-inputs",
        "path": "references/pattern-forms-inputs.md",
        "keywords": [
            "form", "input", "textarea", "validation", "mask", "field",
            "country code", "phone", "email", "required", "hint",
        ],
    },
    {
        "id": "dropdown-selection",
        "path": "references/pattern-dropdown-selection.md",
        "keywords": [
            "dropdown", "select", "picker", "option", "options", "list-item",
            "tag select", "multiple", "choice", "page size",
        ],
    },
    {
        "id": "feedback-overlays",
        "path": "references/pattern-feedback-overlays.md",
        "keywords": [
            "modal", "dialog", "toast", "tooltip", "overlay", "popup",
            "message", "feedback", "notification",
        ],
    },
    {
        "id": "pagination-filters",
        "path": "references/pattern-pagination-filters.md",
        "keywords": [
            "pagination", "filter", "filters", "tag", "tags", "toggle",
            "range", "pager", "listing", "catalog", "results",
        ],
    },
    {
        "id": "upload-progress",
        "path": "references/pattern-upload-and-progress.md",
        "keywords": [
            "upload", "file", "dropzone", "progress", "drag", "attach",
            "attachment", "slider", "percent",
        ],
    },
]


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[_/,+.-]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def score_pattern(text: str, keywords: list[str]) -> tuple[int, list[str]]:
    hits = []
    score = 0
    for keyword in keywords:
        if keyword in text:
            hits.append(keyword)
            score += len(keyword.split())
    return score, hits


def main() -> int:
    parser = argparse.ArgumentParser(description="Recommend SF5 pattern playbooks.")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("query", help="Free-form task description")
    args = parser.parse_args()

    text = normalize(args.query)
    ranked = []
    for pattern in PATTERNS:
        score, hits = score_pattern(text, pattern["keywords"])
        if score > 0:
            ranked.append((score, pattern, hits))

    ranked.sort(key=lambda item: (-item[0], item[1]["id"]))

    if args.format == "json":
        if not ranked:
            payload = {
                "matched": False,
                "fallback_docs": ["references/pattern-playbooks.md"],
                "results": [],
                "activity_hint": ACTIVITY_HINT,
            }
        else:
            payload = {
                "matched": True,
                "results": [
                    {
                        "id": pattern["id"],
                        "path": pattern["path"],
                        "score": score,
                        "keywords": hits,
                    }
                    for score, pattern, hits in ranked[:3]
                ],
                "activity_hint": ACTIVITY_HINT,
            }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    if not ranked:
        print("No direct pattern match.")
        print("Fallback: references/pattern-playbooks.md")
        return 0

    for score, pattern, hits in ranked[:3]:
        print(f"{pattern['id']}\t{score}\t{pattern['path']}\tkeywords={', '.join(hits)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
