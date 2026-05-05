#!/usr/bin/env python3
"""
Convert Tailwind class strings or HTML snippets into an SF5 draft plus report.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


CLASS_ATTR_RE = re.compile(
    r"""(?P<prefix>(?<![:@.\w-])class\s*=\s*)(?P<quote>["'])(?P<classes>.*?)(?P=quote)""",
    re.DOTALL,
)
TAILWIND_RESIDUE_RE = re.compile(
    r"\b(?:"
    r"sm:|md:|lg:|xl:|2xl:|dark:|hover:|focus:|active:|disabled:|"
    r"flex-col|flex-row|items-|justify-|gap-|p[trblxy]?-[0-9]|m[trblxy]?-[0-9]|"
    r"w-full|h-full|rounded|rounded-|shadow|ring-|bg-|text-gray-|font-|"
    r"group|peer|space-|divide-|container|grid-cols-"
    r")"
)
TAILWIND_PALETTE_RE = re.compile(
    r"^(?:bg|text|border|ring|divide|placeholder:text)-"
    r"(?:slate|gray|zinc|neutral|stone|red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose)-"
    r"(?:50|100|200|300|400|500|600|700|800|900|950)$"
)
TAILWIND_EVIDENCE_RE = re.compile(
    r"^(?:"
    r"(?:sm|md|lg|xl|2xl|dark|hover|focus|active|disabled|placeholder|group-hover|peer-focus):.+|"
    r"(?:px|py|pt|pr|pb|pl|mx|my|mt|mr|mb|ml)-[0-9]+|"
    r"space-[xy]-[0-9]+|"
    r"divide-(?:x|y|gray-.+)|"
    r"rounded(?:-(?:sm|md|lg|xl|2xl|3xl|full))?|"
    r"shadow(?:-(?:sm|md|lg|xl|2xl))?|"
    r"ring(?:-.+)?|"
    r"(?:bg|text|border)-(?:white|black)|"
    r"text-(?:xs|sm|base|lg|xl|2xl|3xl|4xl)|"
    r"font-(?:medium|semibold|bold)|"
    r"tracking-.+"
    r")$"
)
PREFIX_MAP = {
    "sm": "sm",
    "md": "md",
    "lg": "lg",
    "xl": "xl",
    "hover": "hover",
    "focus": "focus",
    "active": "active",
}
BLOCKED_PREFIXES = {"2xl", "dark", "disabled"}


def skill_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def split_classes(class_string: str) -> list[str]:
    return [item for item in re.split(r"\s+", class_string.strip()) if item]


def unique_in_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


def wildcard_match(pattern: str, class_name: str) -> bool:
    if pattern.endswith("*"):
        return class_name.startswith(pattern[:-1])
    return class_name == pattern


def load_contract(
    skill_root: Path,
) -> tuple[
    dict[str, dict[str, Any]],
    list[dict[str, Any]],
    set[str],
    list[dict[str, Any]],
    dict[str, dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    vendor_root = skill_root / "references" / "vendor"
    utility_map = load_json(vendor_root / "tailwind-to-sf5.utility-map.json")
    groups = load_json(vendor_root / "tailwind-to-sf5.class-groups.json")
    catalog = load_json(vendor_root / "source" / "catalog-lite.sf-only.json")
    component_hints = load_json(vendor_root / "tailwind-to-sf5.component-hints.json")
    component_recipes = load_json(vendor_root / "tailwind-to-sf5.component-recipes.json")
    component_renderers = load_json(vendor_root / "tailwind-to-sf5.component-renderers.json")
    smart_hints = load_json(vendor_root / "tailwind-to-sf5.smart-hints.json")
    component_smart_catalog = load_json(vendor_root / "component-smart-catalog.json")
    mappings = {item["sourceClass"]: item for item in utility_map.get("mappings", [])}
    families = groups.get("families", [])
    catalog_classes = set(catalog.get("classes", []))
    recipes = {item["hintId"]: item for item in component_recipes.get("recipes", [])}
    return (
        mappings,
        families,
        catalog_classes,
        component_hints.get("hints", []),
        recipes,
        smart_hints.get("hints", []),
        component_renderers.get("renderers", []),
        component_smart_catalog,
    )


def classify_family(class_name: str, families: list[dict[str, Any]]) -> str:
    for family in families:
        for pattern in family.get("patterns", []):
            if wildcard_match(pattern, class_name):
                return str(family.get("id", "unknown"))
    if ":" in class_name:
        return "responsive-state"
    return "unknown"


def split_prefix(class_name: str) -> tuple[str | None, str]:
    if ":" not in class_name:
        return None, class_name
    prefix, base = class_name.split(":", 1)
    return prefix, base


def prefixed_targets(prefix: str, targets: list[str], catalog_classes: set[str]) -> list[str]:
    sf5_prefix = PREFIX_MAP.get(prefix)
    if not sf5_prefix:
        return []
    converted = [f"{sf5_prefix}:{target}" for target in targets]
    return converted if all(target in catalog_classes for target in converted) else []


def detect_component_hints(
    source_classes: list[str],
    html: str,
    component_hints: list[dict[str, Any]],
    component_recipes: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    class_set = set(source_classes)
    html_lower = html.lower()
    detected: list[dict[str, Any]] = []
    for hint in component_hints:
        class_matches = [item for item in hint.get("classSignals", []) if item in class_set]
        html_matches = [item for item in hint.get("htmlSignals", []) if item.lower() in html_lower]
        required_html_signals = [item.lower() for item in hint.get("requiredHtmlSignals", [])]
        if required_html_signals and not all(item in html_lower for item in required_html_signals):
            continue
        if hint.get("requiresHtmlSignal") and not html_matches:
            continue
        score = len(class_matches) + len(html_matches)
        if score < int(hint.get("minimumScore", 1)):
            continue
        hint_id = str(hint.get("id", ""))
        payload = {
            "id": hint_id,
            "title": hint.get("title"),
            "scenario": hint.get("scenario"),
            "score": score,
            "classMatches": class_matches,
            "htmlMatches": html_matches,
            "sf5Strategy": hint.get("sf5Strategy"),
            "sourceRefs": hint.get("sourceRefs", []),
        }
        recipe = component_recipes.get(hint_id)
        if recipe:
            payload["recipe"] = {
                "id": recipe.get("id"),
                "title": recipe.get("title"),
                "targetSurface": recipe.get("targetSurface"),
                "route": recipe.get("route", {}),
                "conversionSteps": recipe.get("conversionSteps", []),
                "starterMarkup": recipe.get("starterMarkup", ""),
                "manualChecks": recipe.get("manualChecks", []),
                "sourceRefs": recipe.get("sourceRefs", []),
            }
        detected.append(payload)
    return detected


def detect_smart_hints(
    source_classes: list[str],
    html: str,
    smart_hints: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    class_set = set(source_classes)
    html_lower = html.lower()
    detected: list[dict[str, Any]] = []
    for hint in smart_hints:
        class_matches = [item for item in hint.get("classSignals", []) if item in class_set]
        html_matches = [item for item in hint.get("htmlSignals", []) if item.lower() in html_lower]
        required_html_signals = [item.lower() for item in hint.get("requiredHtmlSignals", [])]
        if required_html_signals and not all(item in html_lower for item in required_html_signals):
            continue
        if hint.get("requiresHtmlSignal") and not html_matches:
            continue
        score = len(class_matches) + len(html_matches)
        if score < int(hint.get("minimumScore", 1)):
            continue
        detected.append(
            {
                "id": hint.get("id"),
                "title": hint.get("title"),
                "sfCode": hint.get("sfCode"),
                "score": score,
                "classMatches": class_matches,
                "htmlMatches": html_matches,
                "strategy": hint.get("strategy"),
                "sourceRefs": hint.get("sourceRefs", []),
                "advisory": True,
            }
        )
    return detected


def detect_component_renderers(
    source_classes: list[str],
    html: str,
    component_renderers: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    class_set = set(source_classes)
    html_lower = html.lower()
    detected: list[dict[str, Any]] = []
    for renderer in component_renderers:
        class_matches = [
            item
            for item in renderer.get("classSignals", [])
            if item in class_set or any(str(source_class).startswith(str(item)) for source_class in class_set)
        ]
        html_matches = [item for item in renderer.get("htmlSignals", []) if item.lower() in html_lower]
        required_html_signals = [item.lower() for item in renderer.get("requiredHtmlSignals", [])]
        if required_html_signals and not all(item in html_lower for item in required_html_signals):
            continue
        if renderer.get("requiresHtmlSignal") and not html_matches:
            continue
        score = len(class_matches) + len(html_matches)
        if score < int(renderer.get("minimumScore", 1)):
            continue
        detected.append(
            {
                "id": renderer.get("id"),
                "componentId": renderer.get("componentId"),
                "title": renderer.get("title"),
                "surface": renderer.get("surface"),
                "score": score,
                "classMatches": class_matches,
                "htmlMatches": html_matches,
                "starterMarkup": renderer.get("starterMarkup", ""),
                "manualChecks": renderer.get("manualChecks", []),
                "sourceRefs": renderer.get("sourceRefs", []),
            }
        )
    detected.sort(key=lambda item: (-int(item.get("score", 0)), str(item.get("id", ""))))
    return detected


def build_validation_hints_from_counts(
    target_classes: list[str],
    catalog_classes: set[str],
    deferred: list[dict[str, Any]],
    blocked: list[dict[str, Any]],
    unmapped: list[dict[str, Any]],
    mode: str,
) -> dict[str, Any]:
    unknown_targets = [item for item in target_classes if item not in catalog_classes]
    hard_blockers = bool(unknown_targets or blocked)
    review_needed = bool(deferred or unmapped)
    return {
        "mode": mode,
        "strictCatalogReady": not hard_blockers,
        "sf5Ready": not hard_blockers and not review_needed,
        "recommendedCommand": "python3 skills/sf5/scripts/validate_sf5_html_files.py --strict --catalog-strict <converted-file>",
        "unknownTargetClasses": unknown_targets,
        "deferredCount": len(deferred),
        "blockedCount": len(blocked),
        "unmappedCount": len(unmapped),
        "notes": [
            "Strict readiness is advisory until the converted HTML is written to a file and validated.",
            "Deferred and unmapped classes require manual review before marking output as SF5-ready.",
        ],
    }


def find_tailwind_residue(text: str) -> list[str]:
    residue: list[str] = []
    seen: set[str] = set()
    for match in CLASS_ATTR_RE.finditer(text):
        class_string = match.group("classes")
        for token in split_classes(class_string):
            if TAILWIND_RESIDUE_RE.search(token) and token not in seen:
                seen.add(token)
                residue.append(token)
    return residue


def tailwind_evidence_classes(class_string: str, catalog_classes: set[str]) -> list[str]:
    evidence: list[str] = []
    seen: set[str] = set()
    for token in split_classes(class_string):
        if token in catalog_classes:
            continue
        if token in seen:
            continue
        if TAILWIND_PALETTE_RE.match(token) or TAILWIND_EVIDENCE_RE.match(token):
            seen.add(token)
            evidence.append(token)
    return evidence


def tailwind_residue_gate(result: dict[str, Any], mode: str) -> dict[str, Any]:
    converted_text = result.get("convertedHtml") if mode == "html" else result.get("convertedClassString", "")
    residue = find_tailwind_residue(str(converted_text))
    validation_hints = result.get("report", {}).get("validationHints", {})
    sf5_ready = bool(validation_hints.get("sf5Ready"))
    blocking_counts = {
        "deferred": int(validation_hints.get("deferredCount", 0)),
        "blocked": int(validation_hints.get("blockedCount", 0)),
        "unmapped": int(validation_hints.get("unmappedCount", 0)),
    }
    blocking_total = sum(blocking_counts.values())
    ok = sf5_ready and blocking_total == 0
    return {
        "ok": ok,
        "mode": mode,
        "requiresSf5Ready": True,
        "sf5Ready": sf5_ready,
        "blockingCounts": blocking_counts,
        "diagnosticResidue": residue,
        "message": "Output is SF5-ready and has no deferred, blocked, or unmapped Tailwind classes."
        if ok
        else "Output is not SF5-ready: resolve deferred, blocked, or unmapped Tailwind classes before delivery.",
    }


def convert_class_string(
    class_string: str,
    mappings: dict[str, dict[str, Any]],
    families: list[dict[str, Any]],
    catalog_classes: set[str],
    component_hints: list[dict[str, Any]],
    component_recipes: dict[str, dict[str, Any]],
    smart_hints: list[dict[str, Any]],
    component_renderers: list[dict[str, Any]],
    keep_unmapped: bool = False,
    html_context: str = "",
) -> dict[str, Any]:
    source_classes = split_classes(class_string)
    target_classes: list[str] = []
    mapped: list[dict[str, Any]] = []
    deferred: list[dict[str, Any]] = []
    blocked: list[dict[str, Any]] = []
    unmapped: list[dict[str, Any]] = []

    for source_class in source_classes:
        source_prefix, base_class = split_prefix(source_class)
        mapping = mappings.get(source_class)
        prefix_target_classes: list[str] = []
        if not mapping and source_prefix:
            base_mapping = mappings.get(base_class)
            if source_prefix in BLOCKED_PREFIXES:
                mapping = {
                    "sourceClass": source_class,
                    "family": "responsive-state",
                    "status": "blocked",
                    "targetClasses": [],
                    "reason": f"Prefix {source_prefix}: is not supported by Stage 3 converter rules.",
                }
            elif base_mapping and base_mapping.get("status") == "mapped":
                prefix_target_classes = prefixed_targets(
                    source_prefix,
                    list(base_mapping.get("targetClasses", [])),
                    catalog_classes,
                )
                if prefix_target_classes:
                    mapping = {
                        "sourceClass": source_class,
                        "family": "responsive-state",
                        "status": "mapped",
                        "targetClasses": prefix_target_classes,
                        "reason": f"Prefix {source_prefix}: mapped because all prefixed SF5 target classes exist.",
                    }
                else:
                    mapping = {
                        "sourceClass": source_class,
                        "family": "responsive-state",
                        "status": "deferred",
                        "targetClasses": [],
                        "reason": f"Prefix {source_prefix}: cannot be mapped because at least one prefixed SF5 target class is missing.",
                    }
            elif base_mapping and base_mapping.get("status") in {"deferred", "blocked"}:
                mapping = {
                    "sourceClass": source_class,
                    "family": "responsive-state",
                    "status": base_mapping.get("status"),
                    "targetClasses": [],
                    "reason": f"Prefix {source_prefix}: follows base class policy: {base_mapping.get('reason', '')}",
                }

        family = mapping.get("family") if mapping else classify_family(source_class, families)
        if not mapping:
            item = {
                "sourceClass": source_class,
                "family": family,
                "reason": "No Stage 1-2 mapping rule exists.",
            }
            unmapped.append(item)
            if keep_unmapped:
                target_classes.append(source_class)
            continue

        status = mapping.get("status")
        item = {
            "sourceClass": source_class,
            "family": family,
            "targetClasses": mapping.get("targetClasses", []),
            "reason": mapping.get("reason", ""),
        }
        if status == "mapped":
            target_classes.extend(item["targetClasses"])
            mapped.append(item)
        elif status == "deferred":
            deferred.append(item)
            if keep_unmapped:
                target_classes.append(source_class)
        elif status == "blocked":
            blocked.append(item)
            if keep_unmapped:
                target_classes.append(source_class)
        else:
            item["reason"] = f"Invalid mapping status: {status}"
            unmapped.append(item)
            if keep_unmapped:
                target_classes.append(source_class)

    target_classes = unique_in_order(target_classes)
    component_hint_matches = detect_component_hints(
        source_classes,
        html_context,
        component_hints,
        component_recipes,
    )
    smart_hint_matches = detect_smart_hints(source_classes, html_context, smart_hints)
    component_renderer_matches = detect_component_renderers(
        source_classes,
        html_context,
        component_renderers,
    )
    validation_hints = build_validation_hints_from_counts(
        target_classes,
        catalog_classes,
        deferred,
        blocked,
        unmapped,
        "classes",
    )
    return {
        "sourceClassString": " ".join(source_classes),
        "convertedClassString": " ".join(target_classes),
        "targetClasses": target_classes,
        "report": {
            "mapped": mapped,
            "deferred": deferred,
            "blocked": blocked,
            "unmapped": unmapped,
            "componentHints": component_hint_matches,
            "componentRenderCandidates": component_renderer_matches,
            "smartHints": smart_hint_matches,
            "validationHints": validation_hints,
            "summary": {
                "sourceClassCount": len(source_classes),
                "targetClassCount": len(target_classes),
                "mappedCount": len(mapped),
                "deferredCount": len(deferred),
                "blockedCount": len(blocked),
                "unmappedCount": len(unmapped),
            },
        },
    }


def convert_html(
    html: str,
    mappings: dict[str, dict[str, Any]],
    families: list[dict[str, Any]],
    catalog_classes: set[str],
    component_hints: list[dict[str, Any]],
    component_recipes: dict[str, dict[str, Any]],
    smart_hints: list[dict[str, Any]],
    component_renderers: list[dict[str, Any]],
    keep_unmapped: bool = False,
) -> dict[str, Any]:
    class_reports: list[dict[str, Any]] = []

    def replace(match: re.Match[str]) -> str:
        quote = match.group("quote")
        class_string = match.group("classes")
        converted = convert_class_string(
            class_string,
            mappings,
            families,
            catalog_classes,
            component_hints,
            component_recipes,
            smart_hints,
            component_renderers,
            keep_unmapped=keep_unmapped,
            html_context=html,
        )
        class_reports.append(converted)
        return f"{match.group('prefix')}{quote}{converted['convertedClassString']}{quote}"

    converted_html = CLASS_ATTR_RE.sub(replace, html)
    aggregate = {
        "mappedCount": sum(item["report"]["summary"]["mappedCount"] for item in class_reports),
        "deferredCount": sum(item["report"]["summary"]["deferredCount"] for item in class_reports),
        "blockedCount": sum(item["report"]["summary"]["blockedCount"] for item in class_reports),
        "unmappedCount": sum(item["report"]["summary"]["unmappedCount"] for item in class_reports),
        "classAttributeCount": len(class_reports),
    }
    component_hints_report: list[dict[str, Any]] = []
    component_recipes_report: list[dict[str, Any]] = []
    smart_hints_report: list[dict[str, Any]] = []
    component_render_candidates_report: list[dict[str, Any]] = []
    seen_hint_ids: set[str] = set()
    seen_recipe_ids: set[str] = set()
    seen_smart_ids: set[str] = set()
    seen_component_renderer_ids: set[str] = set()
    all_target_classes: list[str] = []
    all_deferred: list[dict[str, Any]] = []
    all_blocked: list[dict[str, Any]] = []
    all_unmapped: list[dict[str, Any]] = []
    for item in class_reports:
        all_target_classes.extend(item.get("targetClasses", []))
        all_deferred.extend(item["report"].get("deferred", []))
        all_blocked.extend(item["report"].get("blocked", []))
        all_unmapped.extend(item["report"].get("unmapped", []))
        for hint in item["report"].get("componentHints", []):
            hint_id = str(hint.get("id"))
            if hint_id in seen_hint_ids:
                continue
            seen_hint_ids.add(hint_id)
            component_hints_report.append(hint)
            recipe = hint.get("recipe")
            if recipe:
                recipe_id = str(recipe.get("id"))
                if recipe_id not in seen_recipe_ids:
                    seen_recipe_ids.add(recipe_id)
                    component_recipes_report.append(recipe)
        for hint in item["report"].get("smartHints", []):
            smart_id = str(hint.get("id"))
            if smart_id in seen_smart_ids:
                continue
            seen_smart_ids.add(smart_id)
            smart_hints_report.append(hint)
        for candidate in item["report"].get("componentRenderCandidates", []):
            candidate_id = str(candidate.get("id"))
            if candidate_id in seen_component_renderer_ids:
                continue
            seen_component_renderer_ids.add(candidate_id)
            component_render_candidates_report.append(candidate)
    validation_hints = build_validation_hints_from_counts(
        unique_in_order(all_target_classes),
        catalog_classes,
        all_deferred,
        all_blocked,
        all_unmapped,
        "html",
    )
    return {
        "sourceHtml": html,
        "convertedHtml": converted_html,
        "report": {
            "classAttributes": class_reports,
            "componentHints": component_hints_report,
            "componentRecipes": component_recipes_report,
            "componentRenderCandidates": component_render_candidates_report,
            "smartHints": smart_hints_report,
            "validationHints": validation_hints,
            "summary": aggregate,
        },
    }


def scan_inventory_path(
    root_path: Path,
    mappings: dict[str, dict[str, Any]],
    families: list[dict[str, Any]],
    catalog_classes: set[str],
    component_hints: list[dict[str, Any]],
    component_recipes: dict[str, dict[str, Any]],
    smart_hints: list[dict[str, Any]],
    component_renderers: list[dict[str, Any]],
) -> dict[str, Any]:
    if root_path.is_file():
        files = [root_path]
    else:
        allowed_suffixes = {".html", ".htm", ".php", ".blade.php", ".vue", ".jsx", ".tsx"}
        files = [
            path
            for path in sorted(root_path.rglob("*"))
            if path.is_file()
            and not any(part in {"node_modules", ".git", "vendor", "dist", "build"} for part in path.parts)
            and (path.suffix in allowed_suffixes or path.name.endswith(".blade.php"))
        ]

    file_reports: list[dict[str, Any]] = []
    class_counter: dict[str, int] = {}
    evidence_counter: dict[str, int] = {}
    component_counter: dict[str, int] = {}
    smart_counter: dict[str, int] = {}
    risk_counter = {"blocked": 0, "deferred": 0, "unmapped": 0}

    for path in files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "class=" not in text and "className=" not in text:
            continue
        payload = convert_html(
            text,
            mappings,
            families,
            catalog_classes,
            component_hints,
            component_recipes,
            smart_hints,
            component_renderers,
            keep_unmapped=False,
        )
        summary = payload["report"]["summary"]
        if not any(summary.get(key, 0) for key in ["mappedCount", "deferredCount", "blockedCount", "unmappedCount"]):
            continue
        evidence: list[str] = []
        for attr in payload["report"].get("classAttributes", []):
            evidence.extend(tailwind_evidence_classes(attr.get("sourceClassString", ""), catalog_classes))
        evidence = unique_in_order(evidence)
        if len(evidence) < 2:
            continue

        for attr in payload["report"].get("classAttributes", []):
            for source_class in split_classes(attr.get("sourceClassString", "")):
                class_counter[source_class] = class_counter.get(source_class, 0) + 1
        for source_class in evidence:
            evidence_counter[source_class] = evidence_counter.get(source_class, 0) + 1
        for hint in payload["report"].get("componentHints", []):
            hint_id = str(hint.get("id"))
            component_counter[hint_id] = component_counter.get(hint_id, 0) + 1
        for hint in payload["report"].get("smartHints", []):
            hint_id = str(hint.get("id"))
            smart_counter[hint_id] = smart_counter.get(hint_id, 0) + 1
        risk_counter["blocked"] += int(summary.get("blockedCount", 0))
        risk_counter["deferred"] += int(summary.get("deferredCount", 0))
        risk_counter["unmapped"] += int(summary.get("unmappedCount", 0))

        file_reports.append(
            {
                "path": path.as_posix(),
                "summary": summary,
                "tailwindEvidenceClasses": evidence,
                "tailwindEvidenceCount": len(evidence),
                "componentHints": [item.get("id") for item in payload["report"].get("componentHints", [])],
                "smartHints": [item.get("id") for item in payload["report"].get("smartHints", [])],
                "validationHints": payload["report"].get("validationHints", {}),
            }
        )

    top_classes = sorted(class_counter.items(), key=lambda item: (-item[1], item[0]))[:50]
    top_evidence = sorted(evidence_counter.items(), key=lambda item: (-item[1], item[0]))[:50]
    return {
        "root": root_path.as_posix(),
        "filesScanned": len(files),
        "filesWithTailwindSignals": len(file_reports),
        "topClasses": [{"class": name, "count": count} for name, count in top_classes],
        "topTailwindEvidenceClasses": [{"class": name, "count": count} for name, count in top_evidence],
        "componentHintCounts": component_counter,
        "smartHintCounts": smart_counter,
        "riskCounts": risk_counter,
        "files": file_reports,
        "recommendedNextSteps": [
            "Convert low-risk files with no blocked classes first.",
            "Review deferred and unmapped classes before marking output as SF5-ready.",
            "Use component hints to choose SF5 recipes and smart hints only after confirming behavior.",
        ],
    }


def collect_component_recipes(result: dict[str, Any]) -> list[dict[str, Any]]:
    report = result.get("report", {})
    if report.get("componentRecipes"):
        return list(report.get("componentRecipes", []))

    recipes: list[dict[str, Any]] = []
    seen: set[str] = set()
    for hint in report.get("componentHints", []):
        recipe = hint.get("recipe")
        if not recipe:
            continue
        recipe_id = str(recipe.get("id", ""))
        if recipe_id in seen:
            continue
        seen.add(recipe_id)
        recipes.append(recipe)
    return recipes


def render_recipe_payload(result: dict[str, Any], recipe_selector: str) -> dict[str, Any]:
    recipes = collect_component_recipes(result)
    if not recipes:
        return {
            "ok": False,
            "error": "No component recipe was detected for this input.",
            "selectedRecipe": None,
            "starterMarkup": "",
        }

    selected = recipes[0] if recipe_selector == "auto" else None
    if recipe_selector != "auto":
        selected = next((recipe for recipe in recipes if recipe.get("id") == recipe_selector), None)
    if not selected:
        return {
            "ok": False,
            "error": f"Detected recipes do not include requested recipe: {recipe_selector}",
            "detectedRecipeIds": [recipe.get("id") for recipe in recipes],
            "selectedRecipe": None,
            "starterMarkup": "",
        }

    return {
        "ok": True,
        "selectedRecipe": selected,
        "starterMarkup": selected.get("starterMarkup", ""),
        "conversionSteps": selected.get("conversionSteps", []),
        "manualChecks": selected.get("manualChecks", []),
        "sourceRefs": selected.get("sourceRefs", []),
    }


COMPONENT_CUSTOM_ELEMENTS = {
    "button": "sf-button",
    "buttons": "sf-button",
    "dropdown": "sf-dropdown",
    "input": "sf-input",
    "inputs": "sf-input",
    "pagination": "sf-pagination",
    "modal": "sf-modal",
}


def build_component_promotion_gate(
    selected_candidate: dict[str, Any],
    runtime_promotion_status: str,
    runtime_visual_delta: float | None,
    max_runtime_visual_delta: float,
) -> dict[str, Any]:
    component_id = str(selected_candidate.get("componentId") or selected_candidate.get("id") or "")
    renderer_id = str(selected_candidate.get("id") or "")
    custom_element = COMPONENT_CUSTOM_ELEMENTS.get(renderer_id) or COMPONENT_CUSTOM_ELEMENTS.get(component_id)
    behavior_checks = list(selected_candidate.get("manualChecks", []))
    failures: list[str] = []
    if not custom_element:
        failures.append("No known SF5 custom element tag is associated with this renderer.")
    if runtime_promotion_status != "candidate":
        failures.append("Runtime promotion status is not candidate.")
    if runtime_visual_delta is None:
        failures.append("Runtime visual delta was not provided.")
    elif abs(runtime_visual_delta) > max_runtime_visual_delta:
        failures.append(
            f"Runtime visual delta {runtime_visual_delta} exceeds allowed threshold {max_runtime_visual_delta}."
        )
    if not behavior_checks:
        failures.append("No behavior checklist is attached to this renderer.")
    return {
        "ok": not failures,
        "status": "candidate" if not failures else "blocked",
        "customElement": custom_element,
        "runtimePromotionStatus": runtime_promotion_status,
        "runtimeVisualDelta": runtime_visual_delta,
        "maxRuntimeVisualDelta": max_runtime_visual_delta,
        "requiresBehaviorChecklist": True,
        "behaviorChecklist": behavior_checks,
        "failures": failures,
        "notes": [
            "Promote custom elements only when runtime preview is candidate, visual delta is within threshold, and behavior checks are explicit.",
            "A passing gate is still a promotion candidate, not a substitute for target-runtime acceptance.",
        ],
    }


def render_component_payload(
    result: dict[str, Any],
    component_selector: str,
    runtime_promotion_status: str = "unknown",
    runtime_visual_delta: float | None = None,
    max_runtime_visual_delta: float = 1.0,
) -> dict[str, Any]:
    candidates = list(result.get("report", {}).get("componentRenderCandidates", []))
    selected_candidate = candidates[0] if component_selector == "auto" and candidates else None
    if component_selector != "auto":
        selected_candidate = next(
            (
                candidate
                for candidate in candidates
                if candidate.get("id") == component_selector or candidate.get("componentId") == component_selector
            ),
            None,
        )
    if selected_candidate:
        return {
            "ok": True,
            "mode": "component",
            "selectedComponent": selected_candidate,
            "starterMarkup": selected_candidate.get("starterMarkup", ""),
            "manualChecks": selected_candidate.get("manualChecks", []),
            "sourceRefs": selected_candidate.get("sourceRefs", []),
            "promotionGate": build_component_promotion_gate(
                selected_candidate,
                runtime_promotion_status,
                runtime_visual_delta,
                max_runtime_visual_delta,
            ),
        }

    payload = render_recipe_payload(result, component_selector)
    if not payload.get("ok"):
        payload["error"] = payload.get("error", "No source-backed component recipe was detected.")
        return payload
    payload["mode"] = "component"
    payload["starterMarkup"] = payload.get("starterMarkup", "")
    return payload


def smart_registry_match(catalog: dict[str, Any], sf_code: str) -> dict[str, Any] | None:
    needle = f'sf-code="{sf_code}"'
    for item in catalog.get("sfCodeRegistry", []):
        if needle in str(item.get("regex", "")):
            return item
    return None


def smart_component_match(catalog: dict[str, Any], sf_code: str) -> dict[str, Any] | None:
    for item in catalog.get("smartComponents", []):
        if item.get("id") == sf_code:
            return item
    return None


def render_smart_payload(
    result: dict[str, Any],
    smart_selector: str,
    component_smart_catalog: dict[str, Any],
) -> dict[str, Any]:
    smart_hints = list(result.get("report", {}).get("smartHints", []))
    if not smart_hints:
        return {
            "ok": False,
            "error": "No smart-component hint was detected for this input.",
            "selectedSmart": None,
            "starterMarkup": "",
        }

    selected = smart_hints[0] if smart_selector == "auto" else None
    if smart_selector != "auto":
        selected = next(
            (
                hint
                for hint in smart_hints
                if hint.get("id") == smart_selector or hint.get("sfCode") == smart_selector
            ),
            None,
        )
    if not selected:
        return {
            "ok": False,
            "error": f"Detected smart hints do not include requested smart selector: {smart_selector}",
            "detectedSmartIds": [hint.get("id") for hint in smart_hints],
            "detectedSfCodes": [hint.get("sfCode") for hint in smart_hints],
            "selectedSmart": None,
            "starterMarkup": "",
        }

    sf_code = str(selected.get("sfCode", ""))
    registry_item = smart_registry_match(component_smart_catalog, sf_code)
    source_backed_component = smart_component_match(component_smart_catalog, sf_code)
    starter_markup = f'<div sf-code="{sf_code}" data="{{}}" property="{{}}" events="{{}}" modify="{{}}"></div>'
    source_backed = bool(source_backed_component)
    return {
        "ok": True,
        "mode": "smart",
        "selectedSmart": selected,
        "sfCode": sf_code,
        "registryItem": registry_item,
        "sourceBackedSmartComponent": source_backed_component,
        "sourceBacked": source_backed,
        "promotionStatus": "candidate" if source_backed else "blocked-by-missing-source-backed-smart",
        "starterMarkup": starter_markup,
        "manualChecks": [
            "Confirm source behavior before replacing static markup with a smart component.",
            "Wire real data/property/events/modify payloads instead of empty placeholders.",
            "Validate first-load and warm-cache behavior in the target SF5 runtime.",
            "Do not auto-promote registry-only sf-code placeholders until a source-backed smart runtime/data contract is found.",
        ],
        "sourceRefs": selected.get("sourceRefs", [])
        + (source_backed_component.get("playExamples", []) if source_backed_component else []),
    }


def read_input(args: argparse.Namespace) -> tuple[str, str]:
    if args.input:
        return Path(args.input).read_text(encoding="utf-8"), args.mode
    if args.html_string is not None:
        return args.html_string, "html"
    if args.class_string is not None:
        return args.class_string, "classes"
    if not sys.stdin.isatty():
        return sys.stdin.read(), args.mode
    raise SystemExit("Provide a class string, --html-string, --input, or stdin.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert Tailwind classes or HTML snippets to SF5 draft output.")
    parser.add_argument("class_string", nargs="?", help="Tailwind class string to convert")
    parser.add_argument("--html-string", help="HTML snippet to convert")
    parser.add_argument("--input", help="Input file path")
    parser.add_argument("--inventory", help="Scan a file or directory and report Tailwind-to-SF5 migration inventory")
    parser.add_argument("--mode", choices=["classes", "html"], default="classes")
    parser.add_argument("--keep-unmapped", action="store_true", help="Keep deferred, blocked, and unmapped source classes")
    parser.add_argument("--gate-tailwind-residue", action="store_true", help="Fail if SF5-ready output still contains Tailwind-like residue")
    parser.add_argument(
        "--render-recipe",
        nargs="?",
        const="auto",
        default="",
        metavar="RECIPE_ID",
        help="Render starter SF5 markup for the first detected recipe or a requested recipe id",
    )
    parser.add_argument(
        "--render-component",
        nargs="?",
        const="auto",
        default="",
        metavar="COMPONENT_RECIPE_ID",
        help="Render source-backed SF5 component starter markup for the first detected component recipe or a requested recipe id",
    )
    parser.add_argument(
        "--runtime-promotion-status",
        choices=["unknown", "candidate", "blocked", "not-required"],
        default="unknown",
        help="Runtime-aware preview status used by the component promotion gate.",
    )
    parser.add_argument(
        "--runtime-visual-delta",
        type=float,
        default=None,
        help="Runtime visual score delta used by the component promotion gate.",
    )
    parser.add_argument(
        "--max-runtime-visual-delta",
        type=float,
        default=1.0,
        help="Maximum absolute runtime visual score delta allowed by the component promotion gate.",
    )
    parser.add_argument(
        "--render-smart",
        nargs="?",
        const="auto",
        default="",
        metavar="SMART_ID_OR_SF_CODE",
        help="Render advisory SF5 smart-component starter markup for the first detected smart hint or requested smart id/sf-code",
    )
    parser.add_argument("--format", choices=["json", "text"], default="json")
    parser.add_argument("--skill-root", default="", help="Optional skill root override")
    args = parser.parse_args()

    skill_root = Path(args.skill_root).resolve() if args.skill_root else skill_root_from_script()
    (
        mappings,
        families,
        catalog_classes,
        component_hints,
        component_recipes,
        smart_hints,
        component_renderers,
        component_smart_catalog,
    ) = load_contract(skill_root)
    if args.inventory:
        result = scan_inventory_path(
            Path(args.inventory).expanduser().resolve(),
            mappings,
            families,
            catalog_classes,
            component_hints,
            component_recipes,
            smart_hints,
            component_renderers,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    source, mode = read_input(args)

    if mode == "html":
        result = convert_html(
            source,
            mappings,
            families,
            catalog_classes,
            component_hints,
            component_recipes,
            smart_hints,
            component_renderers,
            keep_unmapped=args.keep_unmapped,
        )
        text_output = result["convertedHtml"]
    else:
        result = convert_class_string(
            source,
            mappings,
            families,
            catalog_classes,
            component_hints,
            component_recipes,
            smart_hints,
            component_renderers,
            keep_unmapped=args.keep_unmapped,
        )
        text_output = result["convertedClassString"]

    if args.render_recipe:
        recipe_payload = render_recipe_payload(result, args.render_recipe)
        if args.format == "text":
            if not recipe_payload.get("ok"):
                print(recipe_payload.get("error", ""), file=sys.stderr)
                return 1
            print(recipe_payload.get("starterMarkup", ""))
            return 0
        result = {
            "conversion": result,
            "recipeRender": recipe_payload,
        }

    if args.render_component:
        component_payload = render_component_payload(
            result,
            args.render_component,
            runtime_promotion_status=args.runtime_promotion_status,
            runtime_visual_delta=args.runtime_visual_delta,
            max_runtime_visual_delta=args.max_runtime_visual_delta,
        )
        if args.format == "text":
            if not component_payload.get("ok"):
                print(component_payload.get("error", ""), file=sys.stderr)
                return 1
            print(component_payload.get("starterMarkup", ""))
            return 0
        result = {
            "conversion": result,
            "componentRender": component_payload,
        }

    if args.render_smart:
        smart_payload = render_smart_payload(result, args.render_smart, component_smart_catalog)
        if args.format == "text":
            if not smart_payload.get("ok"):
                print(smart_payload.get("error", ""), file=sys.stderr)
                return 1
            print(smart_payload.get("starterMarkup", ""))
            return 0
        result = {
            "conversion": result,
            "smartRender": smart_payload,
        }

    if args.gate_tailwind_residue:
        gate_source = result.get("conversion", result)
        gate_payload = tailwind_residue_gate(gate_source, mode)
        if isinstance(result, dict) and "conversion" in result:
            result["tailwindResidueGate"] = gate_payload
        else:
            result["tailwindResidueGate"] = gate_payload
        if not gate_payload.get("ok"):
            if args.format == "text":
                print(gate_payload.get("message", ""), file=sys.stderr)
            else:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            return 1

    if args.format == "text":
        print(text_output)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
