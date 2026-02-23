#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$ROOT_DIR"

PYTHON_BIN="${PYTHON_BIN:-python3}"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "Python executable not found: $PYTHON_BIN" >&2
  exit 2
fi

echo "[sf5] Python syntax checks"
"$PYTHON_BIN" -m py_compile \
  skills/sf5/scripts/build_ui_doc_atlas.py \
  skills/sf5/scripts/generate_page_scaffold.py \
  skills/sf5/scripts/generate_component_scaffold.py \
  skills/sf5/scripts/migrate_recipe_classes_to_vendor.py \
  skills/sf5/scripts/query_ui_doc_manifest.py \
  skills/sf5/scripts/recommend_page_recipe.py \
  skills/sf5/scripts/validate_page_recipes.py \
  skills/sf5/scripts/validate_sf5_html_files.py

echo "[sf5] Legacy class alias check"
"$PYTHON_BIN" skills/sf5/scripts/migrate_recipe_classes_to_vendor.py --strict

echo "[sf5] Validate page recipes (vendor strict)"
"$PYTHON_BIN" skills/sf5/scripts/validate_page_recipes.py --strict --catalog-strict

echo "[sf5] Validate component templates (vendor strict)"
"$PYTHON_BIN" skills/sf5/scripts/validate_page_recipes.py --strict --catalog-strict --recipes-glob "skills/sf5/references/component-template.md"
"$PYTHON_BIN" skills/sf5/scripts/validate_page_recipes.py --strict --catalog-strict --recipes-glob "skills/sf5/references/smart-component-template.md"
"$PYTHON_BIN" skills/sf5/scripts/validate_page_recipes.py --strict --catalog-strict --recipes-glob "skills/sf5/references/block-template.md"

echo "[sf5] Scaffold smoke checks"
"$PYTHON_BIN" skills/sf5/scripts/generate_page_scaffold.py --type landing --snippet-only > /tmp/sf5-page.html
"$PYTHON_BIN" skills/sf5/scripts/generate_component_scaffold.py --kind component --snippet-only > /tmp/sf5-component.html
"$PYTHON_BIN" skills/sf5/scripts/generate_component_scaffold.py --kind smart --smart-code cards --snippet-only > /tmp/sf5-smart.html
"$PYTHON_BIN" skills/sf5/scripts/generate_component_scaffold.py --kind block --snippet-only > /tmp/sf5-block.html

echo "[sf5] Validate generated HTML snippets (vendor strict)"
"$PYTHON_BIN" skills/sf5/scripts/validate_sf5_html_files.py --strict --catalog-strict \
  /tmp/sf5-page.html /tmp/sf5-component.html /tmp/sf5-smart.html /tmp/sf5-block.html

echo "[sf5] All checks passed"
