# Change Gates

Use these gates when the task changes one of the critical SF5 coordinator surfaces.

## Source Refresh Gate

Apply when the batch touches upstream mirrors, `source/simai/*`, source-backed inventory, or mirrored example paths.

Required before `approved`:

- verify that new upstream paths really exist in the local mirror;
- rebuild source-backed artifacts that depend on the changed mirrors;
- update source-backed references when paths or coverage changed;
- run the relevant regression or local checks after the refresh.

Do not close the batch if mirror refresh changed source structure but left stale manifests or stale docs behind.

## Working-Set Gate

Apply when the batch touches:

- `generate_sf5_working_set.py`
- `working-set.section-variants.json`
- section snippets
- upstream extracts
- working-set manifest contract

Required before `approved`:

- verify that every changed `source_ref` and upstream extract path exists;
- generate at least one real working set for the touched recipe or scenario;
- confirm that generated bundle files and manifest fields still match contract;
- run e2e and local checks when extraction or manifest logic changed.

Do not close the batch if generated snippets exist only synthetically while upstream source-backed snippets are now broken.

## Validation Hardening Gate

Apply when the batch touches validators, fixture sets, smoke checks, or bundle assertions.

Required before `approved`:

- add or update the narrowest fixture set that proves the behavior;
- run the specific validator directly before relying on the full local suite;
- keep validator output machine-readable where fixtures depend on it;
- update docs only after the new validator contract is confirmed green.

Do not close the batch if validation logic changed but there is no regression proof for the new behavior.
