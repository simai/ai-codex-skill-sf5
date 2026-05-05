# SF5 Execution Workflow

Use this file as the default execution order for real SF5 tasks.

## Goal

Turn a free-form request into a reproducible implementation path with minimal ambiguity.

## Default Sequence

1. Route the task:

```bash
python3 skills/sf5/scripts/recommend_sf5_route.py "<task>"
```

If the task is architecture-, validation-, or source-refresh-heavy, first ask for coordinator activity:

```bash
python3 skills/sf5/scripts/recommend_sf5_activity.py "<task>"
```

For agent or automation handoff, prefer:

```bash
python3 skills/sf5/scripts/recommend_sf5_route.py "<task>" --format json
```

If work starts one layer lower than the top route, the supporting routers also expose machine-readable coordinator hints:

```bash
python3 skills/sf5/scripts/recommend_page_recipe.py --manifest skills/sf5/references/ui-doc-manifest.json --format json "<task>"
python3 skills/sf5/scripts/recommend_product_scenario.py --format json "<task>"
python3 skills/sf5/scripts/recommend_ui_pattern.py --format json "<task>"
python3 skills/sf5/scripts/generate_page_scaffold.py --type profile --snippet-only --format json
python3 skills/sf5/scripts/generate_component_scaffold.py --kind smart --smart-code cards --snippet-only --format json
```

For source-refresh activity, the source chain also exposes coordinator hints:

```bash
python3 skills/sf5/scripts/sync_source_repos.py --format json
python3 skills/sf5/scripts/build_source_inventory.py --repo-root "$PWD" --skill-root "$PWD/skills/sf5" --format json
```

Or prepare the whole starter bundle in one step:

```bash
python3 skills/sf5/scripts/prepare_sf5_task.py "<task>" --scaffold-out /tmp/page.html
```

Or generate a full working directory:

```bash
python3 skills/sf5/scripts/generate_sf5_working_set.py "<task>" --out-dir /tmp/sf5-task
```

This working set can include section-level variants in `sections/*.html` for faster block replacement.
It can also include `sources.md`, which points back to the upstream `ui-play` and `ui-doc` files behind those sections.
For supported sections it can also include `upstream/*.html`, which stores normalized snippets extracted from upstream examples.
It now also includes `activity.json` and `manifest.activity`, so the bundle carries coordinator intent together with page route data.

2. If the task depends on current upstream SF5 behavior, refresh local mirrors:

```bash
python3 skills/sf5/scripts/sync_source_repos.py
python3 skills/sf5/scripts/build_source_inventory.py \
  --repo-root "$PWD" \
  --skill-root "$PWD/skills/sf5"
```

3. If docs changed or exact docs routing matters, refresh atlas:

```bash
python3 skills/sf5/scripts/build_ui_doc_atlas.py \
  --docs-root "$PWD/source/simai/ui-doc/source/docs/ru" \
  --skill-root "$PWD/skills/sf5"
```

4. If a full-page starter is needed, generate scaffold from recipe:

```bash
python3 skills/sf5/scripts/generate_page_scaffold.py --type <recipe-type> --snippet-only
```

5. Use the returned pattern playbooks to implement sections.

6. Validate the final result:

```bash
python3 skills/sf5/scripts/validate_sf5_html_files.py --strict --catalog-strict /tmp/example.html
```

7. Before delivery or repository updates, run:

```bash
bash skills/sf5/scripts/run_local_checks.sh
```

The local suite now also verifies:

- activity manifest integrity
- source-refresh manifest/lock/inventory consistency
- validation-layer fixture density and validator presence
- activity-aware JSON contracts for page recipe, product scenario, and pattern routers
- activity-aware JSON contracts for source-refresh scripts
- activity-aware JSON contracts for scaffold generators
- focused gate validators for `source-refresh` and `validation-hardening`

## Decision Rules

- Start from product scenario when the user asks for a whole screen.
- Start from pattern playbooks when the user asks for a section or reusable interaction.
- Sync upstream only when current source truth matters.
- Prefer generated scaffold plus adaptation over writing full pages from scratch.
- Prefer JSON output for script-to-script chaining and markdown output for human review.
- For coordinator-centric tasks, verify gate rules and knowledge packs before widening the batch.

## Minimal Artifact Set

For a normal feature request, the expected working set is:

- one route from `recommend_sf5_route.py`
- one scenario or recipe
- one to three pattern playbooks
- one strict validation pass
