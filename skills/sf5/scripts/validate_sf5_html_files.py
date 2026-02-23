#!/usr/bin/env python3
"""
Validate real SF5 markup files (HTML/PHP/templated snippets) against vendor rules.
"""

from __future__ import annotations

import argparse
import glob
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Set


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from validate_page_recipes import (  # noqa: E402
    append_unique,
    extract_prefix_parts,
    is_allowed_by_pattern,
    load_known_tokens,
    load_vendor_catalog,
    load_vendor_excluded,
    load_vendor_prefixes,
    load_vendor_smart_codes,
    normalize,
)


CLASS_ATTR_RE = re.compile(r"(?:class|className)\s*=\s*(?:\"([^\"]+)\"|'([^']+)')", re.DOTALL)
SF_CODE_RE = re.compile(r'sf-code\s*=\s*(?:\"([^\"]+)\"|\'([^\']+)\')', re.DOTALL)
STYLE_ATTR_RE = re.compile(r"style\s*=\s*(?:\"([^\"]+)\"|'([^']+)')", re.DOTALL)
TOKEN_RE = re.compile(r"(--sf-[A-Za-z0-9_\\/\-]+)")


def normalize_sf_token(token: str) -> str:
    return token.strip().strip(",.;:").replace("\\/", "/")


def load_vendor_tokens(tokens_manifest_path: Path, catalog_path: Path) -> Set[str]:
    tokens: Set[str] = set()

    if tokens_manifest_path.exists():
        data = json.loads(tokens_manifest_path.read_text(encoding="utf-8"))
        sf_tokens = data.get("sfTokens", {})
        if isinstance(sf_tokens, dict):
            for key in sf_tokens.keys():
                if isinstance(key, str):
                    tokens.add(normalize_sf_token(key))
        elif isinstance(sf_tokens, list):
            for key in sf_tokens:
                if isinstance(key, str):
                    tokens.add(normalize_sf_token(key))

    if catalog_path.exists():
        data = json.loads(catalog_path.read_text(encoding="utf-8"))
        catalog_tokens = data.get("tokens", [])
        if isinstance(catalog_tokens, list):
            for key in catalog_tokens:
                if isinstance(key, str):
                    tokens.add(normalize_sf_token(key))
        elif isinstance(catalog_tokens, dict):
            for key in catalog_tokens.keys():
                if isinstance(key, str):
                    tokens.add(normalize_sf_token(key))

    return tokens


def extract_markup_classes(text: str) -> List[str]:
    classes: List[str] = []
    for match in CLASS_ATTR_RE.finditer(text):
        blob = (match.group(1) or match.group(2) or "").replace("\n", " ")
        for token in blob.split():
            token = token.strip()
            if token and token not in {"...", ".."}:
                classes.append(token)
    return classes


def extract_sf_codes(text: str) -> List[str]:
    codes: List[str] = []
    for match in SF_CODE_RE.finditer(text):
        code = (match.group(1) or match.group(2) or "").strip()
        if code and code not in {"...", ".."}:
            codes.append(code)
    return codes


def extract_sf_tokens(text: str) -> List[str]:
    tokens: List[str] = []
    for match in STYLE_ATTR_RE.finditer(text):
        style_blob = match.group(1) or match.group(2) or ""
        for token_match in TOKEN_RE.finditer(style_blob):
            token = normalize_sf_token(token_match.group(1))
            if token:
                tokens.append(token)
    return tokens


def validate_markup_files(
    files: List[Path],
    manifest_known: Set[str],
    vendor_known: Set[str],
    excluded_classes: Set[str],
    prefix_tokens: List[str],
    allowed_prefix_names: Set[str],
    smart_codes: Set[str],
    known_tokens: Set[str],
    catalog_strict: bool,
) -> Dict[str, Dict[str, List[str]]]:
    findings_by_file: Dict[str, Dict[str, List[str]]] = {}
    known_union = manifest_known | vendor_known

    for path in files:
        text = path.read_text(encoding="utf-8")
        raw_classes = extract_markup_classes(text)
        sf_codes = extract_sf_codes(text)
        sf_tokens = extract_sf_tokens(text)

        unknown_classes: List[str] = []
        excluded_hits: List[str] = []
        unknown_prefixes: List[str] = []
        unknown_sf_codes: List[str] = []
        unknown_sf_tokens: List[str] = []
        non_catalog_classes: List[str] = []

        seen_unknown_classes: Set[str] = set()
        seen_excluded: Set[str] = set()
        seen_prefixes: Set[str] = set()
        seen_sf_codes: Set[str] = set()
        seen_sf_tokens: Set[str] = set()
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

            if vendor_known and not in_vendor and (in_manifest or by_pattern):
                append_unique(non_catalog_classes, seen_non_catalog, raw)

        for code in sf_codes:
            if smart_codes and code not in smart_codes:
                append_unique(unknown_sf_codes, seen_sf_codes, code)

        for token in sf_tokens:
            if known_tokens and token not in known_tokens:
                append_unique(unknown_sf_tokens, seen_sf_tokens, token)

        if (
            unknown_classes
            or excluded_hits
            or unknown_prefixes
            or unknown_sf_codes
            or unknown_sf_tokens
            or non_catalog_classes
        ):
            findings_by_file[path.as_posix()] = {
                "unknown_classes": unknown_classes,
                "excluded_classes": excluded_hits,
                "unknown_prefixes": unknown_prefixes,
                "unknown_sf_codes": unknown_sf_codes,
                "unknown_sf_tokens": unknown_sf_tokens,
                "non_catalog_classes": non_catalog_classes,
            }

    return findings_by_file


def collect_files(paths: List[str], globs: List[str]) -> List[Path]:
    resolved: Set[Path] = set()

    for value in paths:
        p = Path(value).expanduser().resolve()
        if p.is_file():
            resolved.add(p)

    for pattern in globs:
        for match in glob.glob(pattern, recursive=True):
            p = Path(match).expanduser().resolve()
            if p.is_file():
                resolved.add(p)

    return sorted(resolved)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate SF5 HTML-like files.")
    parser.add_argument(
        "paths",
        nargs="*",
        help="Files to validate",
    )
    parser.add_argument(
        "--glob",
        action="append",
        default=[],
        help="Glob pattern for files (repeatable)",
    )
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
        "--tokens-manifest",
        default="",
        help="Path to vendor tokens manifest (default: references/vendor/manifest/sf5.tokens.sf.json)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with non-zero if hard findings are present",
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
    tokens_manifest_path = (
        Path(args.tokens_manifest).expanduser().resolve()
        if args.tokens_manifest
        else root / "references" / "vendor" / "manifest" / "sf5.tokens.sf.json"
    )

    files = collect_files(args.paths, args.glob)
    if not files:
        print("No files found. Provide paths or --glob.")
        return 0

    manifest_known = load_known_tokens(manifest_path)
    vendor_known = load_vendor_catalog(catalog_path)
    excluded_classes = load_vendor_excluded(excluded_path)
    prefix_tokens, allowed_prefix_names = load_vendor_prefixes(conditions_path)
    smart_codes = load_vendor_smart_codes(smart_manifest_path, smart_codes_path)
    known_tokens = load_vendor_tokens(tokens_manifest_path, catalog_path)

    findings_by_file = validate_markup_files(
        files=files,
        manifest_known=manifest_known,
        vendor_known=vendor_known,
        excluded_classes=excluded_classes,
        prefix_tokens=prefix_tokens,
        allowed_prefix_names=allowed_prefix_names,
        smart_codes=smart_codes,
        known_tokens=known_tokens,
        catalog_strict=args.catalog_strict,
    )

    print(f"Manifest tokens: {len(manifest_known)}")
    print(f"Vendor catalog classes: {len(vendor_known)}")
    print(f"Excluded vendor classes: {len(excluded_classes)}")
    print(f"Known sf-code values: {len(smart_codes)}")
    print(f"Known --sf-* tokens: {len(known_tokens)}")
    print(f"Allowed prefixes: {', '.join(sorted(allowed_prefix_names))}")
    print(f"Files: {len(files)}")

    if not findings_by_file:
        print("Validation passed: no class/sf-code/token findings detected.")
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
        if payload["unknown_sf_tokens"]:
            hard_fail_count += len(payload["unknown_sf_tokens"])
            print(f"  unknown --sf-* tokens: {', '.join(payload['unknown_sf_tokens'])}")
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
