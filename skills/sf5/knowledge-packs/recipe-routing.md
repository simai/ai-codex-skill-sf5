# Knowledge Pack: Recipe Routing

Use this pack when the task is in `recipe-scaffold-maintenance` or when page-level route selection is the main risk.

Focus:

- `recommend_page_recipe.py`
- `generate_page_scaffold.py`
- page recipe type selection
- utility-group mapping
- scaffold generator activity hints

Default artifacts:

- `references/page-recipe-routing.md`
- `references/page-recipes-index.md`
- `scripts/recommend_page_recipe.py`
- `scripts/generate_page_scaffold.py`
- `scripts/validate_scaffold_hints.py`

Execution contract:

- `recommend_page_recipe.py --format json` must expose `activity_hint`
- `generate_page_scaffold.py --format json` must expose `activity_hint`
- selected recipe type must stay aligned with generator support

Common failure classes:

- page route points to a recipe type that the scaffold generator no longer supports
- recipe router returns the right family in text mode but loses machine-readable contract in JSON mode
- utility-group mapping drifts away from the recipe family

Minimum verification:

- validate route selection on at least one representative prompt
- validate scaffold generator JSON hint contract
- keep strict recipe validation green
