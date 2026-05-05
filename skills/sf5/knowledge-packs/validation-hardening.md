# Knowledge Pack: Validation Hardening

Use this pack when the activity is `validation-hardening`.

Focus:

- validators
- route/e2e/activity fixtures
- smoke checks
- strict bundle and snippet verification

Default artifacts:

- `scripts/run_local_checks.sh`
- `scripts/validate_route_fixtures.py`
- `scripts/validate_activity_fixtures.py`
- `scripts/validate_router_hints.py`
- `scripts/validate_e2e_fixtures.py`
- `scripts/validate_activity_manifests.py`
- `scripts/validate_validation_contract.py`
- `scripts/validate_sf5_html_files.py`
- `scripts/validate_page_recipes.py`

Execution contract:

- route fixtures protect top-level scenario/recipe/activity matching;
- activity fixtures protect coordinator activity, specialists, gate rules, knowledge packs, workflow snippets, and required outputs;
- router-hint fixtures protect lower-level JSON `activity_hint` surfaces;
- e2e fixtures protect `prepare_sf5_task.py` and `generate_sf5_working_set.py` together;
- `validate_validation_contract.py` protects validator presence plus minimum fixture richness.

Common failure classes:

- route ranking drift after new heuristics;
- lower-level routers returning stale `activity_hint`;
- fixtures that only check `activity_id` but stop checking roles or gate rules;
- validators existing on disk but silently dropping schema coverage.

Minimum verification:

- run the changed validator directly;
- update the narrowest fixture set that proves the change;
- keep route/activity/router-hint/e2e fixture layers consistent with each other;
- keep validation contract checks green;
- keep full local suite green after fixture and validator changes.
