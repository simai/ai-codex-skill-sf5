# Specialist: working-set

Owns working-set generation, section variants, upstream snippet extraction, and bundle contract shape.

Use when:

- `generate_sf5_working_set.py` changes;
- section or upstream coverage changes;
- extraction logic changes.

Focus:

- keep generated bundles stable and inspectable;
- prefer source-backed extracts over synthetic approximations when possible;
- maintain `manifest.json`, `sections/`, `sources.md`, and `upstream/` consistency.
