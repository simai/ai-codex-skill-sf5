#!/usr/bin/env python3
"""
Validate SF5 page recipe classes and sf-code values.

Vendor-first behavior:
- Uses SF5 vendor catalog/conditions/exclusions/smart manifests when present.
- Falls back to ui-doc-manifest class tokens for compatibility.
"""

from __future__ import annotations

import argparse
import glob
import json
import re
from pathlib import Path
from typing import Dict, List, Set


DEFAULT_BREAKPOINTS = ("sm", "md", "lg", "xl", "xxl")
DEFAULT_STATES = ("hover", "focus", "active")

ALLOW_EXACT = {
    "container",
    "link",
    "overflow-auto",
}

ALLOW_PATTERNS = [
    r"^theme-(light|dark)$",
    r"^txt-role-[a-z0-9-]+$",
    r"^(m|p)(t|b|x|y)?-[0-9]+(?:/[0-9]+)?$",
    r"^(m|p)-[xy]-[0-9]+(?:/[0-9]+)?$",
    r"^radius-[0-9]+(?:/[0-9]+)?$",
    r"^grid-col-[0-9]+$",
    r"^border-(top|bottom|inline-start|inline-end|x|y)-[0-9]+$",
    r"^(justify-main|items-cross|items-main)-[a-z0-9-]+$",
    r"^space-y-[0-9]+(?:/[0-9]+)?$",
    r"^min-h-[0-9]+$",
    r"^color-[a-z0-9-]+$",
    r"^bg-[a-z0-9-]+$",
]


def normalize(token: str, prefix_tokens: List[str]) -> str:
    token = token.strip().strip(",.;:")
    while True:
        changed = False
        for p in prefix_tokens:
            if token.startswith(p):
                token = token[len(p) :]
                changed = True
        if not changed:
            break
    return token


def extract_recipe_classes(md_text: str) -> List[str]:
    classes: List[str] = []
    for block in re.findall(r"```html\s*(.*?)\s*```", md_text, flags=re.DOTALL):
        for m in re.finditer(r'class\s*=\s*(["\'])(.*?)\1', block, flags=re.DOTALL):
            blob = m.group(2).replace("\n", " ")
            for token in blob.split():
                token = token.strip()
                if token and token not in {"...", ".."}:
                    classes.append(token)
    return classes


def extract_recipe_sf_codes(md_text: str) -> List[str]:
    codes: List[str] = []
    for block in re.findall(r"```html\s*(.*?)\s*```", md_text, flags=re.DOTALL):
        for m in re.finditer(r'sf-code\s*=\s*(["\'])(.*?)\1', block, flags=re.DOTALL):
            code = m.group(2).strip()
            if code and code not in {"...", ".."}:
                codes.append(code)
    return codes


def load_known_tokens(manifest_path: Path) -> Set[str]:
    known: Set[str] = set()
    if not manifest_path.exists():
        return known
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    for rec in data:
        for t in rec.get("class_tokens", []):
            known.add(t.lstrip("."))
        for t in rec.get("example_class_tokens", []):
            known.add(t)
    return known


def is_allowed_by_pattern(token: str) -> bool:
    if token in ALLOW_EXACT:
        return True
    return any(re.match(p, token) for p in ALLOW_PATTERNS)


def load_vendor_catalog(catalog_path: Path) -> Set[str]:
    if not catalog_path.exists():
        return set()
    data = json.loads(catalog_path.read_text(encoding="utf-8"))
    classes = data.get("classes", [])
    if not isinstance(classes, list):
        return set()
    return {str(x) for x in classes if isinstance(x, str)}


def load_vendor_excluded(excluded_path: Path) -> Set[str]:
    if not excluded_path.exists():
        return set()
    data = json.loads(excluded_path.read_text(encoding="utf-8"))
    classes = data.get("excludedNonSfClasses", [])
    if isinstance(classes, list):
        raw_values = [str(x) for x in classes if isinstance(x, str)]
    elif isinstance(classes, dict):
        raw_values = [str(x) for x in classes.keys() if isinstance(x, str)]
    else:
        return set()
    return {v.lstrip(".") for v in raw_values if v.strip()}


def load_vendor_prefixes(conditions_path: Path) -> tuple[List[str], Set[str]]:
    if not conditions_path.exists():
        names = set(DEFAULT_BREAKPOINTS + DEFAULT_STATES)
        return [f"{x}:" for x in names], names

    data = json.loads(conditions_path.read_text(encoding="utf-8"))
    names: Set[str] = set()
    for item in data.get("breakpoints", []):
        if isinstance(item, str) and item:
            names.add(item)
    for item in data.get("states", []):
        if isinstance(item, str) and item:
            names.add(item)
    if not names:
        names = set(DEFAULT_BREAKPOINTS + DEFAULT_STATES)
    return [f"{x}:" for x in sorted(names)], names


def extract_codes_from_regex(blob: str) -> List[str]:
    values = re.findall(r'sf-code\s*=\s*["\']([^"\']+)["\']', blob)
    return [v.strip() for v in values if v.strip()]


def load_vendor_smart_codes(smart_manifest_path: Path, smart_codes_path: Path) -> Set[str]:
    allowed: Set[str] = set()

    if smart_manifest_path.exists():
        data = json.loads(smart_manifest_path.read_text(encoding="utf-8"))
        for item in data.get("smart", []):
            if not isinstance(item, dict):
                continue
            code = item.get("sf_code")
            if isinstance(code, str) and code.strip():
                allowed.add(code.strip())

    if smart_codes_path.exists():
        data = json.loads(smart_codes_path.read_text(encoding="utf-8"))
        for item in data.get("items", []):
            if not isinstance(item, dict):
                continue
            for code in extract_codes_from_regex(str(item.get("regex", ""))):
                allowed.add(code)

    return allowed


def extract_prefix_parts(token: str) -> List[str]:
    token = token.strip().strip(",.;:")
    if ":" not in token:
        return []
    parts = token.split(":")
    if len(parts) < 2:
        return []
    return [p for p in parts[:-1] if p]


def append_unique(target: List[str], seen: Set[str], value: str) -> None:
    if value and value not in seen:
        seen.add(value)
        target.append(value)


def validate_files(
    recipe_files: List[Path],
    manifest_known: Set[str],
    vendor_known: Set[str],
    excluded_classes: Set[str],
    prefix_tokens: List[str],
    allowed_prefix_names: Set[str],
    smart_codes: Set[str],
    catalog_strict: bool,
) -> Dict[str, Dict[str, List[str]]]:
    findings_by_file: Dict[str, Dict[str, List[str]]] = {}
    known_union = manifest_known | vendor_known

    for path in recipe_files:
        text = path.read_text(encoding="utf-8")
        raw_classes = extract_recipe_classes(text)
        sf_codes = extract_recipe_sf_codes(text)

        unknown_classes: List[str] = []
        excluded_hits: List[str] = []
        unknown_prefixes: List[str] = []
        unknown_sf_codes: List[str] = []
        non_catalog_classes: List[str] = []

        seen_unknown_classes: Set[str] = set()
        seen_excluded: Set[str] = set()
        seen_prefixes: Set[str] = set()
        seen_sf_codes: Set[str] = set()
        seen_non_catalog: Set[str] = set()

        for raw in raw_classes:
            prefix_parts = extract_prefix_parts(raw)
            for prefix in prefix_parts:
                if prefix not in allowed_prefix_names:
                    append_unique(
                        unknown_prefixes,
                        seen_prefixes,
                        f"{prefix} (in `{raw}`)",
                    )

            core = normalize(raw, prefix_tokens)
            if not core:
                continue

            if raw in excluded_classes or core in excluded_classes:
                append_unique(excluded_hits, seen_excluded, raw)
                continue

            in_vendor = raw in vendor_known or core in vendor_known
            in_manifest = raw in manifest_known or core in manifest_known
            in_union = raw in known_union or core in known_union
            by_pattern = is_allowed_by_pattern(core)

            if catalog_strict and vendor_known:
                allowed = in_vendor
            else:
                allowed = in_union or by_pattern

            if not allowed:
                append_unique(unknown_classes, seen_unknown_classes, raw)
                continue

            # In compatibility mode we allow manifest-only classes,
            # but still flag them to reconcile against vendor catalog.
            if vendor_known and not in_vendor and (in_manifest or by_pattern):
                append_unique(non_catalog_classes, seen_non_catalog, raw)

        for code in sf_codes:
            if smart_codes and code not in smart_codes:
                append_unique(unknown_sf_codes, seen_sf_codes, code)

        if (
            unknown_classes
            or excluded_hits
            or unknown_prefixes
            or unknown_sf_codes
            or non_catalog_classes
        ):
            findings_by_file[path.name] = {
                "unknown_classes": unknown_classes,
                "excluded_classes": excluded_hits,
                "unknown_prefixes": unknown_prefixes,
                "unknown_sf_codes": unknown_sf_codes,
                "non_catalog_classes": non_catalog_classes,
            }
    return findings_by_file


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate SF5 page recipes against SF5 data.")
    parser.add_argument(
        "--manifest",
        default="",
        help="Path to ui-doc-manifest.json (default: references/ui-doc-manifest.json)",
    )
    parser.add_argument(
        "--catalog",
        default="",
        help="Path to vendor catalog-lite.sf-only.json (default: references/vendor/source/catalog-lite.sf-only.json)",
    )
    parser.add_argument(
        "--excluded",
        default="",
        help="Path to vendor excluded classes json (default: references/vendor/manifest/sf5.excluded-non-sf-classes.json)",
    )
    parser.add_argument(
        "--conditions",
        default="",
        help="Path to vendor conditions json (default: references/vendor/manifest/sf5.conditions.json)",
    )
    parser.add_argument(
        "--smart-manifest",
        default="",
        help="Path to vendor smart manifest (default: references/vendor/manifest/sf5.smart.json)",
    )
    parser.add_argument(
        "--smart-codes",
        default="",
        help="Path to vendor smart-codes registry (default: references/vendor/registries/smart-codes.json)",
    )
    parser.add_argument(
        "--recipes-glob",
        default="",
        help="Glob for page recipe files (default: references/page-recipe-*.md)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with non-zero if unknown classes are found",
    )
    parser.add_argument(
        "--catalog-strict",
        action="store_true",
        help="Require class presence in vendor catalog (ignores manifest fallback for class checks)",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    manifest_path = (
        Path(args.manifest).expanduser().resolve()
        if args.manifest
        else root / "references" / "ui-doc-manifest.json"
    )
    catalog_path = (
        Path(args.catalog).expanduser().resolve()
        if args.catalog
        else root / "references" / "vendor" / "source" / "catalog-lite.sf-only.json"
    )
    excluded_path = (
        Path(args.excluded).expanduser().resolve()
        if args.excluded
        else root
        / "references"
        / "vendor"
        / "manifest"
        / "sf5.excluded-non-sf-classes.json"
    )
    conditions_path = (
        Path(args.conditions).expanduser().resolve()
        if args.conditions
        else root / "references" / "vendor" / "manifest" / "sf5.conditions.json"
    )
    smart_manifest_path = (
        Path(args.smart_manifest).expanduser().resolve()
        if args.smart_manifest
        else root / "references" / "vendor" / "manifest" / "sf5.smart.json"
    )
    smart_codes_path = (
        Path(args.smart_codes).expanduser().resolve()
        if args.smart_codes
        else root / "references" / "vendor" / "registries" / "smart-codes.json"
    )
    recipes_glob = args.recipes_glob or str(root / "references" / "page-recipe-*.md")
    recipe_files = [Path(p) for p in sorted(glob.glob(recipes_glob))]

    manifest_known = load_known_tokens(manifest_path)
    vendor_known = load_vendor_catalog(catalog_path)
    excluded_classes = load_vendor_excluded(excluded_path)
    prefix_tokens, allowed_prefix_names = load_vendor_prefixes(conditions_path)
    smart_codes = load_vendor_smart_codes(smart_manifest_path, smart_codes_path)

    findings_by_file = validate_files(
        recipe_files=recipe_files,
        manifest_known=manifest_known,
        vendor_known=vendor_known,
        excluded_classes=excluded_classes,
        prefix_tokens=prefix_tokens,
        allowed_prefix_names=allowed_prefix_names,
        smart_codes=smart_codes,
        catalog_strict=args.catalog_strict,
    )

    print(f"Manifest tokens: {len(manifest_known)}")
    print(f"Vendor catalog classes: {len(vendor_known)}")
    print(f"Excluded vendor classes: {len(excluded_classes)}")
    print(f"Allowed prefixes: {', '.join(sorted(allowed_prefix_names))}")
    print(f"Known sf-code values: {len(smart_codes)}")
    print(f"Recipe files: {len(recipe_files)}")
    if not findings_by_file:
        print("Validation passed: no class/sf-code findings detected.")
        return 0

    print("Validation findings:")
    hard_fail_count = 0
    soft_warn_count = 0
    for file_name, payload in findings_by_file.items():
        print(f"- {file_name}:")
        if payload["unknown_classes"]:
            hard_fail_count += len(payload["unknown_classes"])
            print(f"  unknown classes: {', '.join(payload['unknown_classes'])}")
        if payload["excluded_classes"]:
            hard_fail_count += len(payload["excluded_classes"])
            print(f"  excluded classes: {', '.join(payload['excluded_classes'])}")
        if payload["unknown_prefixes"]:
            hard_fail_count += len(payload["unknown_prefixes"])
            print(f"  unknown prefixes: {', '.join(payload['unknown_prefixes'])}")
        if payload["unknown_sf_codes"]:
            hard_fail_count += len(payload["unknown_sf_codes"])
            print(f"  unknown sf-code: {', '.join(payload['unknown_sf_codes'])}")
        if payload["non_catalog_classes"]:
            soft_warn_count += len(payload["non_catalog_classes"])
            print(
                "  non-catalog classes (allowed by manifest compatibility): "
                + ", ".join(payload["non_catalog_classes"])
            )

    if soft_warn_count and not args.catalog_strict:
        print(
            "Compatibility note: non-catalog classes are accepted because "
            "vendor catalog strict mode is disabled."
        )
        print("Use --catalog-strict to enforce vendor-only class whitelist.")

    return 1 if args.strict and hard_fail_count > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
