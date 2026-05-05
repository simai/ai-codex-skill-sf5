# Knowledge Pack: Routing Maintenance

Use this pack when the activity is `routing-maintenance`.

Focus:

- scenario ranking
- recipe routing
- pattern playbook routing
- route fixtures and ambiguous query handling

Default artifacts:

- `scripts/recommend_sf5_route.py`
- `scripts/recommend_page_recipe.py`
- `scripts/recommend_product_scenario.py`
- `references/vendor/route-fixtures.json`
- `references/vendor/e2e-fixtures.json`

Minimum verification:

- direct route command works for the touched query family;
- route fixtures pass;
- e2e fixtures pass when route output affects downstream bundle generation.
