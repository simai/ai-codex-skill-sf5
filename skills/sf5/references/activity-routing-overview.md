# Activity Routing Overview

Use `scripts/recommend_sf5_activity.py` when the task should first be classified as a coordinator activity before choosing page routes or bundle generation.

Current primary activities:

- `source-refresh`
- `routing-maintenance`
- `recipe-scaffold-maintenance`
- `working-set-maintenance`
- `validation-hardening`
- `documentation-update`
- `skill-architecture-update`

Default usage:

```bash
python3 skills/sf5/scripts/recommend_sf5_activity.py "ui-play changed and working set extracts are broken"
python3 skills/sf5/scripts/recommend_sf5_activity.py "надо усилить фикстуры и проверки для activity routing" --format json
```

What it returns:

- selected `activity_id`
- matched signals
- required and optional specialists
- recommended specialist roles
- required rules
- knowledge packs
- gate rules
- current-batch workflow

Lower-level routers now also expose machine-readable `activity_hint` contracts:

- `recommend_page_recipe.py --format json`
- `recommend_product_scenario.py --format json`
- `recommend_ui_pattern.py --format json`
- `sync_source_repos.py --format json`
- `build_source_inventory.py --format json`
- `generate_page_scaffold.py --format json`
- `generate_component_scaffold.py --format json`

Use these outputs when a coordinator needs to keep recipe/scenario/pattern routing aligned with the owning activity family instead of treating them as standalone helpers.

Use this output in:

- `prepare_sf5_task.py`
- `generate_sf5_working_set.py`
- architecture and regression work where page route alone is too narrow

Contract validators that protect this coordinator layer:

- `validate_activity_manifests.py`
- `validate_source_refresh_contract.py`
- `validate_source_refresh_gate.py`
- `validate_validation_contract.py`
- `validate_validation_hardening_gate.py`
- `validate_router_hints.py`
- `validate_scaffold_hints.py`
