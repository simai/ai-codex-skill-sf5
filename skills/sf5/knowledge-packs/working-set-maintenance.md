# Knowledge Pack: Working Set Maintenance

Use this pack when the activity is `working-set-maintenance`.

Focus:

- bundle contract
- section variants
- upstream extraction
- source-backed references inside generated working sets

Default artifacts:

- `scripts/generate_sf5_working_set.py`
- `scripts/prepare_sf5_task.py`
- `scripts/validate_e2e_fixtures.py`
- `references/vendor/working-set.section-variants.json`
- `references/vendor/working-set.coverage.json`
- `references/working-set-generation.md`
- `references/working-set-coverage.md`

Execution contract:

- route payload must carry embedded `activity`;
- generated working set must include `activity.json` and `manifest.activity`;
- `section_variants` and `upstream_variants` must stay source-backed where expected;
- bundle-level changes must still satisfy e2e fixtures and strict HTML checks.

Common failure classes:

- upstream snippet selectors drifting after `ui-play` changes;
- generated bundle losing `activity.json` or `manifest.activity`;
- sections staying synthetic after a better upstream snippet exists;
- route family changing without matching working-set sections and upstream extracts.

Minimum verification:

- changed upstream source paths exist;
- a real working set is generated for the touched recipe;
- `manifest.json`, `sections/*.html`, and `upstream/*.html` still match contract;
- embedded activity contract survives through `prepare_sf5_task.py` and `generate_sf5_working_set.py`;
- e2e and local checks pass.
