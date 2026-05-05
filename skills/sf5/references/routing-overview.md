# SF5 Routing Overview

Use this file when you need one top-level route from a free-form task to the most relevant SF5 artifacts.

## Routing Layers

1. Product scenario:
   whole feature screen such as auth, catalog, checkout, profile, dashboard
2. Page recipe:
   starter scaffold for a page type
3. Pattern playbooks:
   recurring UI parts inside the screen

## CLI Router

Use:

```bash
python3 skills/sf5/scripts/recommend_sf5_route.py "checkout page with customer form, delivery, payment, summary and submit confirmation"
```

Machine-readable mode:

```bash
python3 skills/sf5/scripts/recommend_sf5_route.py \
  "checkout page with customer form, delivery, payment, summary and submit confirmation" \
  --format json
```

The router returns:

- top scenario
- page recipe
- scaffold command if supported
- top pattern playbooks
- embedded coordinator activity with specialists, gates, and knowledge packs
- workflow steps
- JSON payload when another tool or automation should consume the result

## Ranking Notes

- Routing is keyword-based with intent boosts, not a full semantic classifier.
- It gives extra weight to compound signals such as `dashboard + table`, `table + filters/search/status`, `kpi + activity`, and similar high-signal combinations.
- It penalizes `catalog-listing` when the query contains table/dashboard/admin language without clear catalog or product signals.
- It separates `dashboard-table` from `dashboard-workspace`: table-first operator queries prefer the table recipe, while mixed KPI/activity/table dashboards prefer the workspace recipe.

## Regression Fixtures

- Stable routing expectations live in `references/vendor/route-fixtures.json`.
- Validate them with `python3 skills/sf5/scripts/validate_route_fixtures.py`.
- Route fixtures now also assert the embedded `activity.activity_id`, not only scenario and recipe.
- `run_local_checks.sh` runs this validator so route tuning for one scenario does not silently break another.
- End-to-end bundle expectations live in `references/vendor/e2e-fixtures.json`.
- Validate them with `python3 skills/sf5/scripts/validate_e2e_fixtures.py`.
- Fixtures now include short queries and mixed RU/EN phrasing, not only fully specified English tasks.

## How To Read The Result

- If scenario confidence is strong, start from the scenario doc.
- If a page recipe is returned, scaffold immediately and then adapt.
- If several pattern playbooks are returned, use them to implement page sections in order of importance.
- If no strong route is found, fall back to:
  - `references/sf5-fast-start.md`
  - `references/page-layout-playbook.md`
  - `references/source-inventory.md`
