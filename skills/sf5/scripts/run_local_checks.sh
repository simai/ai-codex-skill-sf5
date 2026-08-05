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
  skills/sf5/scripts/recommend_ui_pattern.py \
  skills/sf5/scripts/recommend_product_scenario.py \
  skills/sf5/scripts/recommend_sf5_route.py \
  skills/sf5/scripts/recommend_sf5_activity.py \
  skills/sf5/scripts/validate_activity_manifests.py \
  skills/sf5/scripts/validate_route_fixtures.py \
  skills/sf5/scripts/validate_activity_fixtures.py \
  skills/sf5/scripts/validate_router_hints.py \
  skills/sf5/scripts/validate_scaffold_hints.py \
  skills/sf5/scripts/validate_source_refresh_contract.py \
  skills/sf5/scripts/validate_source_refresh_gate.py \
  skills/sf5/scripts/validate_tailwind_conversion_contract.py \
  skills/sf5/scripts/validate_tailwind_mapping_artifacts.py \
  skills/sf5/scripts/validate_validation_contract.py \
  skills/sf5/scripts/validate_validation_hardening_gate.py \
  skills/sf5/scripts/validate_working_set_sources.py \
  skills/sf5/scripts/validate_e2e_fixtures.py \
  skills/sf5/scripts/prepare_sf5_task.py \
  skills/sf5/scripts/generate_sf5_working_set.py \
  skills/sf5/scripts/build_working_set_coverage.py \
  skills/sf5/scripts/build_source_inventory.py \
  skills/sf5/scripts/build_component_smart_catalog.py \
  skills/sf5/scripts/sync_source_repos.py \
  skills/sf5/scripts/convert_tailwind_to_sf5.py \
  skills/sf5/scripts/probe_html_runtime.py \
  skills/sf5/scripts/validate_tailwind_converter.py \
  skills/sf5/scripts/validate_page_recipes.py \
  skills/sf5/scripts/validate_sf5_html_files.py

echo "[sf5] Legacy class alias check"
"$PYTHON_BIN" skills/sf5/scripts/migrate_recipe_classes_to_vendor.py --strict

echo "[sf5] Build working-set coverage report"
"$PYTHON_BIN" skills/sf5/scripts/build_working_set_coverage.py

SF5_UPSTREAM_SOURCES_AVAILABLE=0
if [[ -d "$ROOT_DIR/source/simai/ui/distr/component" \
  && -d "$ROOT_DIR/source/simai/ui-smart/smart" \
  && -d "$ROOT_DIR/source/simai/ui-play/examples" ]]; then
  SF5_UPSTREAM_SOURCES_AVAILABLE=1
fi
export SF5_UPSTREAM_SOURCES_AVAILABLE

if [[ "$SF5_UPSTREAM_SOURCES_AVAILABLE" == "1" ]]; then
  echo "[sf5] Build source inventory (machine-readable smoke)"
  "$PYTHON_BIN" skills/sf5/scripts/build_source_inventory.py \
    --repo-root "$ROOT_DIR" \
    --skill-root "$ROOT_DIR/skills/sf5" \
    --format json > /tmp/sf5-source-inventory-build.json

  echo "[sf5] Build component/smart catalog"
  "$PYTHON_BIN" skills/sf5/scripts/build_component_smart_catalog.py \
    --repo-root "$ROOT_DIR" \
    --skill-root "$ROOT_DIR/skills/sf5" \
    --format json > /tmp/sf5-component-smart-catalog.json

  echo "[sf5] Validate working-set source refs"
  "$PYTHON_BIN" skills/sf5/scripts/validate_working_set_sources.py > /tmp/sf5-working-set-sources.json
else
  echo "[sf5] Skip upstream source checks (source/simai is not present in this checkout)"
  printf '%s\n' '{"ok": true, "status": "skipped", "reason": "upstream_sources_unavailable"}' \
    > /tmp/sf5-source-inventory-build.json
  printf '%s\n' '{"ok": true, "status": "skipped", "reason": "upstream_sources_unavailable"}' \
    > /tmp/sf5-component-smart-catalog.json
  printf '%s\n' '{"ok": true, "status": "skipped", "reason": "upstream_sources_unavailable"}' \
    > /tmp/sf5-working-set-sources.json
fi

echo "[sf5] Validate activity manifests"
"$PYTHON_BIN" skills/sf5/scripts/validate_activity_manifests.py > /tmp/sf5-activity-manifests.json

if [[ "$SF5_UPSTREAM_SOURCES_AVAILABLE" == "1" ]]; then
  echo "[sf5] Validate source-refresh contract"
  "$PYTHON_BIN" skills/sf5/scripts/validate_source_refresh_contract.py > /tmp/sf5-source-refresh.json
else
  printf '%s\n' '{"ok": true, "status": "skipped", "reason": "upstream_sources_unavailable"}' \
    > /tmp/sf5-source-refresh.json
fi

echo "[sf5] Validate validation-layer contract"
"$PYTHON_BIN" skills/sf5/scripts/validate_validation_contract.py > /tmp/sf5-validation-contract.json

echo "[sf5] Validate lower-level router activity hints"
"$PYTHON_BIN" skills/sf5/scripts/validate_router_hints.py > /tmp/sf5-router-hints.json

echo "[sf5] Validate scaffold generator activity hints"
"$PYTHON_BIN" skills/sf5/scripts/validate_scaffold_hints.py > /tmp/sf5-scaffold-hints.json

if [[ "$SF5_UPSTREAM_SOURCES_AVAILABLE" == "1" ]]; then
  echo "[sf5] Validate source-refresh gate"
  "$PYTHON_BIN" skills/sf5/scripts/validate_source_refresh_gate.py > /tmp/sf5-source-refresh-gate.json
else
  printf '%s\n' '{"ok": true, "status": "skipped", "reason": "upstream_sources_unavailable"}' \
    > /tmp/sf5-source-refresh-gate.json
fi

echo "[sf5] Validate Tailwind conversion contract"
"$PYTHON_BIN" skills/sf5/scripts/validate_tailwind_conversion_contract.py > /tmp/sf5-tailwind-conversion.json

echo "[sf5] Validate Tailwind mapping artifacts"
"$PYTHON_BIN" skills/sf5/scripts/validate_tailwind_mapping_artifacts.py > /tmp/sf5-tailwind-mapping.json

echo "[sf5] Validate Tailwind converter"
"$PYTHON_BIN" skills/sf5/scripts/validate_tailwind_converter.py > /tmp/sf5-tailwind-converter.json

echo "[sf5] Validate visual score guard"
"$PYTHON_BIN" - <<'PY'
import struct
import subprocess
import sys
import zlib
from pathlib import Path

path = Path("/tmp/sf5-black-screen.png")
width, height = 128, 90
raw = b"".join(b"\x00" + b"\x00\x00\x00" * width for _ in range(height))

def chunk(kind: bytes, data: bytes) -> bytes:
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

png = (
    b"\x89PNG\r\n\x1a\n"
    + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    + chunk(b"IDAT", zlib.compress(raw))
    + chunk(b"IEND", b"")
)
path.write_bytes(png)
result = subprocess.run(
    [sys.executable, "skills/sf5/scripts/score_lab_visual.py", str(path)],
    text=True,
    capture_output=True,
    check=False,
)
assert result.returncode != 0, result.stdout
assert "nearly black" in result.stdout or "dark" in result.stdout, result.stdout
PY

echo "[sf5] Validate validation-hardening gate"
if [[ "$SF5_UPSTREAM_SOURCES_AVAILABLE" == "1" ]]; then
  "$PYTHON_BIN" skills/sf5/scripts/validate_validation_hardening_gate.py > /tmp/sf5-validation-gate.json
else
  printf '%s\n' '{"ok": true, "status": "skipped", "reason": "upstream_sources_unavailable"}' \
    > /tmp/sf5-validation-gate.json
fi

echo "[sf5] Validate page recipes (vendor strict)"
"$PYTHON_BIN" skills/sf5/scripts/validate_page_recipes.py --strict --catalog-strict

echo "[sf5] Validate component templates (vendor strict)"
"$PYTHON_BIN" skills/sf5/scripts/validate_page_recipes.py --strict --catalog-strict --recipes-glob "skills/sf5/references/component-template.md"
"$PYTHON_BIN" skills/sf5/scripts/validate_page_recipes.py --strict --catalog-strict --recipes-glob "skills/sf5/references/smart-component-template.md"
"$PYTHON_BIN" skills/sf5/scripts/validate_page_recipes.py --strict --catalog-strict --recipes-glob "skills/sf5/references/block-template.md"

echo "[sf5] Scaffold smoke checks"
"$PYTHON_BIN" skills/sf5/scripts/generate_page_scaffold.py --type landing --snippet-only > /tmp/sf5-page.html
"$PYTHON_BIN" skills/sf5/scripts/generate_page_scaffold.py --type auth --snippet-only > /tmp/sf5-auth-page.html
"$PYTHON_BIN" skills/sf5/scripts/generate_page_scaffold.py --type catalog --snippet-only > /tmp/sf5-catalog-page.html
"$PYTHON_BIN" skills/sf5/scripts/generate_page_scaffold.py --type catalog-empty --snippet-only > /tmp/sf5-catalog-empty-page.html
"$PYTHON_BIN" skills/sf5/scripts/generate_page_scaffold.py --type dashboard --snippet-only > /tmp/sf5-dashboard-page.html
"$PYTHON_BIN" skills/sf5/scripts/generate_page_scaffold.py --type dashboard-table --snippet-only > /tmp/sf5-dashboard-table-page.html
"$PYTHON_BIN" skills/sf5/scripts/generate_page_scaffold.py --type article --snippet-only > /tmp/sf5-article-page.html
"$PYTHON_BIN" skills/sf5/scripts/generate_page_scaffold.py --type checkout --snippet-only > /tmp/sf5-checkout-page.html
"$PYTHON_BIN" skills/sf5/scripts/generate_page_scaffold.py --type profile --snippet-only > /tmp/sf5-profile-page.html
"$PYTHON_BIN" skills/sf5/scripts/generate_component_scaffold.py --kind component --snippet-only > /tmp/sf5-component.html
"$PYTHON_BIN" skills/sf5/scripts/generate_component_scaffold.py --kind smart --smart-code cards --snippet-only > /tmp/sf5-smart.html
"$PYTHON_BIN" skills/sf5/scripts/generate_component_scaffold.py --kind block --snippet-only > /tmp/sf5-block.html

echo "[sf5] Route and preparation smoke checks"
"$PYTHON_BIN" skills/sf5/scripts/recommend_sf5_activity.py \
  "working set сломан после обновления ui-play, нужно поправить upstream extracts и manifest" \
  --format json > /tmp/sf5-activity.json
"$PYTHON_BIN" skills/sf5/scripts/recommend_sf5_route.py \
  "checkout page with customer form, delivery, payment, summary and submit confirmation" \
  --format json > /tmp/sf5-route.json
"$PYTHON_BIN" skills/sf5/scripts/recommend_page_recipe.py \
  --manifest skills/sf5/references/ui-doc-manifest.json \
  --format json \
  "profile settings page with avatar upload and notification toggles" \
  > /tmp/sf5-page-recipe.json
"$PYTHON_BIN" skills/sf5/scripts/recommend_product_scenario.py \
  --format json \
  "profile settings page with avatar upload and notification toggles" \
  > /tmp/sf5-product-scenario.json
"$PYTHON_BIN" skills/sf5/scripts/recommend_ui_pattern.py \
  --format json \
  "checkout page with customer form, delivery, payment and summary" \
  > /tmp/sf5-ui-pattern.json
"$PYTHON_BIN" skills/sf5/scripts/validate_route_fixtures.py > /tmp/sf5-route-fixtures.json
"$PYTHON_BIN" skills/sf5/scripts/validate_activity_fixtures.py > /tmp/sf5-activity-fixtures.json
if [[ "$SF5_UPSTREAM_SOURCES_AVAILABLE" == "1" ]]; then
  "$PYTHON_BIN" skills/sf5/scripts/validate_e2e_fixtures.py > /tmp/sf5-e2e-fixtures.json
else
  printf '%s\n' '{"ok": true, "status": "skipped", "reason": "upstream_sources_unavailable"}' \
    > /tmp/sf5-e2e-fixtures.json
fi
"$PYTHON_BIN" skills/sf5/scripts/prepare_sf5_task.py \
  "profile settings page with avatar upload and notification toggles" \
  --format json \
  --scaffold-out /tmp/sf5-prepared-profile.html \
  > /tmp/sf5-task.json
if [[ "$SF5_UPSTREAM_SOURCES_AVAILABLE" == "1" ]]; then
  "$PYTHON_BIN" skills/sf5/scripts/generate_sf5_working_set.py \
    "dashboard with KPI cards, activity table and filters" \
    --out-dir /tmp/sf5-working-set
fi

echo "[sf5] Validate generated HTML snippets (vendor strict)"
HTML_CHECK_PATHS=(
  /tmp/sf5-page.html \
  /tmp/sf5-auth-page.html \
  /tmp/sf5-catalog-page.html \
  /tmp/sf5-catalog-empty-page.html \
  /tmp/sf5-dashboard-page.html \
  /tmp/sf5-dashboard-table-page.html \
  /tmp/sf5-article-page.html \
  /tmp/sf5-checkout-page.html \
  /tmp/sf5-profile-page.html \
  /tmp/sf5-prepared-profile.html \
  /tmp/sf5-component.html \
  /tmp/sf5-smart.html \
  /tmp/sf5-block.html
)
if [[ "$SF5_UPSTREAM_SOURCES_AVAILABLE" == "1" ]]; then
  HTML_CHECK_PATHS+=(
    /tmp/sf5-working-set/scaffold.html
    /tmp/sf5-working-set/sections/kpi-row.html
    /tmp/sf5-working-set/sections/activity-table.html
    /tmp/sf5-working-set/sections/action-bar.html
    /tmp/sf5-working-set/upstream/activity-table.html
  )
fi
"$PYTHON_BIN" skills/sf5/scripts/validate_sf5_html_files.py --strict --catalog-strict "${HTML_CHECK_PATHS[@]}"

echo "[sf5] Validate JSON outputs"
"$PYTHON_BIN" - <<'PY'
import json
import os
from pathlib import Path

route = json.loads(Path("/tmp/sf5-route.json").read_text(encoding="utf-8"))
activity = json.loads(Path("/tmp/sf5-activity.json").read_text(encoding="utf-8"))
page_recipe = json.loads(Path("/tmp/sf5-page-recipe.json").read_text(encoding="utf-8"))
product_scenario = json.loads(Path("/tmp/sf5-product-scenario.json").read_text(encoding="utf-8"))
ui_pattern = json.loads(Path("/tmp/sf5-ui-pattern.json").read_text(encoding="utf-8"))
route_fixtures = json.loads(Path("/tmp/sf5-route-fixtures.json").read_text(encoding="utf-8"))
activity_fixtures = json.loads(Path("/tmp/sf5-activity-fixtures.json").read_text(encoding="utf-8"))
router_hints = json.loads(Path("/tmp/sf5-router-hints.json").read_text(encoding="utf-8"))
scaffold_hints = json.loads(Path("/tmp/sf5-scaffold-hints.json").read_text(encoding="utf-8"))
working_set_sources = json.loads(Path("/tmp/sf5-working-set-sources.json").read_text(encoding="utf-8"))
activity_manifests = json.loads(Path("/tmp/sf5-activity-manifests.json").read_text(encoding="utf-8"))
source_refresh = json.loads(Path("/tmp/sf5-source-refresh.json").read_text(encoding="utf-8"))
source_refresh_gate = json.loads(Path("/tmp/sf5-source-refresh-gate.json").read_text(encoding="utf-8"))
tailwind_conversion = json.loads(Path("/tmp/sf5-tailwind-conversion.json").read_text(encoding="utf-8"))
tailwind_mapping = json.loads(Path("/tmp/sf5-tailwind-mapping.json").read_text(encoding="utf-8"))
tailwind_converter = json.loads(Path("/tmp/sf5-tailwind-converter.json").read_text(encoding="utf-8"))
validation_contract = json.loads(Path("/tmp/sf5-validation-contract.json").read_text(encoding="utf-8"))
validation_gate = json.loads(Path("/tmp/sf5-validation-gate.json").read_text(encoding="utf-8"))
source_inventory_build = json.loads(Path("/tmp/sf5-source-inventory-build.json").read_text(encoding="utf-8"))
component_smart_catalog = json.loads(Path("/tmp/sf5-component-smart-catalog.json").read_text(encoding="utf-8"))
e2e_fixtures = json.loads(Path("/tmp/sf5-e2e-fixtures.json").read_text(encoding="utf-8"))
task = json.loads(Path("/tmp/sf5-task.json").read_text(encoding="utf-8"))
upstream_sources_available = os.environ.get("SF5_UPSTREAM_SOURCES_AVAILABLE") == "1"
manifest = (
    json.loads(Path("/tmp/sf5-working-set/manifest.json").read_text(encoding="utf-8"))
    if upstream_sources_available
    else None
)
coverage = json.loads(Path("skills/sf5/references/vendor/working-set.coverage.json").read_text(encoding="utf-8"))

assert route["matched"] is True
assert activity["matched"] is True
assert activity["activity_id"] == "working-set-maintenance"
assert page_recipe["activity_hint"]["activity_id"] == "recipe-scaffold-maintenance"
assert product_scenario["activity_hint"]["activity_id"] == "working-set-maintenance"
assert ui_pattern["activity_hint"]["activity_id"] == "recipe-scaffold-maintenance"
assert route["scenario_id"] == "checkout-flow"
assert route["recipe_type"] == "checkout"
assert "workflow" in route and len(route["workflow"]) >= 5
assert route_fixtures["ok"] is True
assert activity_fixtures["ok"] is True
assert router_hints["ok"] is True
assert scaffold_hints["ok"] is True
assert working_set_sources["ok"] is True
assert activity_manifests["ok"] is True
assert source_refresh["ok"] is True
assert source_refresh_gate["ok"] is True
if not upstream_sources_available:
    assert source_refresh["status"] == "skipped"
    assert source_refresh_gate["status"] == "skipped"
assert tailwind_conversion["ok"] is True
assert tailwind_conversion["activityId"] == "tailwind-conversion"
assert tailwind_mapping["ok"] is True
assert tailwind_mapping["familyCount"] >= 8
assert tailwind_mapping["mappingCount"] >= 20
assert tailwind_mapping["fixtureCount"] >= 4
assert tailwind_mapping["htmlFixtureCount"] >= 4
assert tailwind_mapping["componentHintCount"] >= 4
assert tailwind_mapping["componentRecipeCount"] >= 4
assert tailwind_mapping["componentRendererCount"] >= 5
assert tailwind_mapping["smartHintCount"] >= 4
assert tailwind_converter["ok"] is True
assert tailwind_converter["fixtureCount"] >= 4
assert tailwind_converter["htmlFixtureCount"] >= 4
assert tailwind_converter["promotionGateFixtureCount"] >= 4
assert tailwind_converter["e2eFixtureCount"] >= 4
assert validation_contract["ok"] is True
assert validation_gate["ok"] is True
if not upstream_sources_available:
    assert validation_gate["status"] == "skipped"
assert source_inventory_build["ok"] is True
assert component_smart_catalog["ok"] is True
if upstream_sources_available:
    assert source_inventory_build["activity_hint"]["activity_id"] == "source-refresh"
    assert component_smart_catalog["summary"]["componentCount"] > 0
    assert component_smart_catalog["summary"]["componentsWithExamples"] > 0
    assert component_smart_catalog["summary"]["smartComponentCount"] > 0
    assert component_smart_catalog["summary"]["smartComponentsWithExamples"] > 0
else:
    assert source_inventory_build["status"] == "skipped"
    assert component_smart_catalog["status"] == "skipped"
    assert working_set_sources["status"] == "skipped"
assert route_fixtures["fixtureCount"] >= 9
assert activity_fixtures["fixtureCount"] >= 5
assert router_hints["fixtureCount"] >= 4
assert scaffold_hints["fixtureCount"] >= 4
if upstream_sources_available:
    assert working_set_sources["checked"] >= 10
assert activity_manifests["checked"] >= 7
if upstream_sources_available:
    assert source_refresh["checked"] >= 5
assert validation_contract["routeFixtureCount"] >= 10
assert validation_contract["routerHintFixtureCount"] >= 4
assert validation_contract["scaffoldHintFixtureCount"] >= 4
if upstream_sources_available:
    assert source_inventory_build["summary"]["shippedComponentCount"] > 0
assert e2e_fixtures["ok"] is True
if upstream_sources_available:
    assert e2e_fixtures["fixtureCount"] >= 3
else:
    assert e2e_fixtures["status"] == "skipped"

assert task["route"]["matched"] is True
assert task["route"]["activity"]["activity_id"] == "working-set-maintenance"
assert task["route"]["scenario_id"] == "profile-settings"
assert task["route"]["recipe_type"] == "profile"
assert task["scaffold_output"] == "/tmp/sf5-prepared-profile.html"

if upstream_sources_available:
    assert manifest is not None
    assert manifest["route"]["matched"] is True
    assert manifest["activity"]["activity_id"] == "working-set-maintenance"
    assert manifest["route"]["scenario_id"] == "dashboard-workspace"
    assert manifest["route"]["recipe_type"] == "dashboard"
    assert manifest["files"]["activity_json"] == "activity.json"
    assert manifest["files"]["scaffold"] == "scaffold.html"
    assert manifest["files"]["sections_index"] == "sections.md"
    assert manifest["files"]["sources_index"] == "sources.md"
    assert manifest["files"]["sections_dir"] == "sections/"
    assert manifest["files"]["upstream_index"] == "upstream.md"
    assert manifest["files"]["upstream_dir"] == "upstream/"
    assert len(manifest["section_variants"]) >= 3
    assert manifest["section_variants"][0]["file"].startswith("sections/")
    assert manifest["section_variants"][0]["source_refs"]
    assert len(manifest["upstream_variants"]) >= 1
    assert manifest["upstream_variants"][0]["file"].startswith("upstream/")
assert coverage["summary"]["expectedRecipeTypeCount"] == 9
assert coverage["summary"]["supportedRecipeTypeCount"] == 9
assert coverage["summary"]["unsupportedRecipeTypes"] == []
assert coverage["summary"]["recipeTypesWithoutUpstreamExtracts"] == []
PY

echo "[sf5] All checks passed"
