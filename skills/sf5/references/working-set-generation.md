# SF5 Working Set Generation

Use this helper when one task should immediately turn into a small working directory with route data, task brief, scaffold, and reference index.

## CLI

```bash
python3 skills/sf5/scripts/generate_sf5_working_set.py \
  "checkout page with customer form, delivery, payment and summary" \
  --out-dir /tmp/sf5-checkout-working-set
```

## Generated Artifacts

- `route.json`: machine-readable route from `recommend_sf5_route.py`
- `activity.json`: machine-readable coordinator activity extracted from route output
- `task.json`: prepared task payload in JSON
- `task-brief.md`: human-readable task brief
- `references.md`: short index of scenario, recipe, and pattern playbooks
- `scaffold.html`: starter page scaffold when a recipe type exists
- `sections.md`: index of section-level variants for the matched page type
- `sections/*.html`: reusable section snippets such as toolbar, filters, KPI row, summary, or form blocks
- `sources.md`: upstream source map for generated sections from `ui-play` and `ui-doc`
- `upstream.md`: index of normalized upstream snippets extracted from `ui-play`
- `upstream/*.html`: extracted upstream snippets for selected section types
- `manifest.json`: summary of the bundle
- `README.md`: quick usage note for the generated directory

## Recommended Usage

- Use this when the task is concrete and implementation should start immediately.
- Use `prepare_sf5_task.py` when you only need a brief and optional scaffold.
- Use `recommend_sf5_route.py --format json` when another tool needs routing only.
- Use `recommend_sf5_activity.py --format json` when another tool needs coordinator activity only.
- Use the generated `sections/*.html` files when you want to swap page blocks quickly without rewriting the full scaffold.
- Use `sources.md` when a section should be reconciled with authoritative upstream examples or docs.
- Use `upstream/*.html` when you want the closest reusable snippet from real SF5 examples for a supported section.

## Coverage Source

- Section and upstream extraction coverage is defined in:
  - `references/vendor/working-set.section-variants.json`
  - `references/vendor/working-set.legacy-class-map.json`
- Source-path integrity for those manifests is validated with `scripts/validate_working_set_sources.py`.
- Extend these manifests first when adding new supported section types.
- Rebuild coverage reports after edits with `scripts/build_working_set_coverage.py`.

## Upstream Extract Modes

- Default upstream extracts use one balanced tag block selected by `tag + class_token + occurrence`.
- Multi-block extracts can use `mode: "range"` with `start` and `end` selectors from the same source file.
- Parent-style extracts can use `mode: "ancestor"` with a child selector plus `ancestor_tag` and `levels_up`.
- Use `range` when one section is better represented by several adjacent upstream blocks than by a single component shell.
- Use `ancestor` when the useful reusable fragment is the nearest stable container around a component, not the component tag itself.
