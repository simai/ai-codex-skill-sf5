# Knowledge Pack: Scenario Routing

Use this pack when top-level product scenario selection is the main risk.

Focus:

- `recommend_product_scenario.py`
- `recommend_sf5_route.py`
- scenario-level ambiguity between `auth`, `catalog`, `checkout`, `profile`, `dashboard`, `article`
- route-family workflow expectations

Default artifacts:

- `references/product-scenarios.md`
- `references/routing-overview.md`
- `scripts/recommend_product_scenario.py`
- `scripts/recommend_sf5_route.py`
- `scripts/validate_route_fixtures.py`
- `scripts/validate_e2e_fixtures.py`

Execution contract:

- top-level route payload must carry embedded coordinator activity
- product scenario router JSON must expose `activity_hint`
- route-family fixtures must protect scenario, recipe, and activity together

Common failure classes:

- `catalog` vs `dashboard-table` ambiguity
- `article` queries drifting into table/dashboard intent
- short or mixed RU/EN queries bypassing the intended scenario family

Minimum verification:

- keep route fixtures green
- keep e2e route-to-working-set fixtures green
- keep required activity specialists, gate rules, roles, and workflow snippets aligned for protected route families
