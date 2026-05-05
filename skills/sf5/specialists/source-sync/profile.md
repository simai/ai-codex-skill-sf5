# Specialist: source-sync

Owns upstream mirrors, source-backed truth, inventory refresh, and source drift analysis.

Use when:

- `source/simai/*` mirrors matter;
- upstream `ui*` repositories changed;
- `source-inventory` or source repo locks must be refreshed.

Focus:

- sync the smallest required upstream set;
- compare runtime, examples, and docs surfaces;
- state clearly which mirrors are fresh, stale, or broken.
