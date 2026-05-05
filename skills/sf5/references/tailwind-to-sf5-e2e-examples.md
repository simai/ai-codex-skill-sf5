# Tailwind to SF5 E2E Examples

These examples are original Tailwind-inspired fixtures for the converter pipeline. They are not copied from Tailwind Plus source.

## Covered Examples

- `auth-form`: `references/vendor/tailwind-to-sf5.e2e-auth.sf5.html`
- `card`: `references/vendor/tailwind-to-sf5.e2e-card.sf5.html`
- `data-table`: `references/vendor/tailwind-to-sf5.e2e-table.sf5.html`
- `toolbar`: `references/vendor/tailwind-to-sf5.e2e-toolbar.sf5.html`

## Validation

```bash
python3 skills/sf5/scripts/validate_sf5_html_files.py \
  --strict \
  --catalog-strict \
  skills/sf5/references/vendor/tailwind-to-sf5.e2e-auth.sf5.html \
  skills/sf5/references/vendor/tailwind-to-sf5.e2e-card.sf5.html \
  skills/sf5/references/vendor/tailwind-to-sf5.e2e-table.sf5.html \
  skills/sf5/references/vendor/tailwind-to-sf5.e2e-toolbar.sf5.html
```

## Current Pipeline

1. Convert safe utility classes with `convert_tailwind_to_sf5.py`.
2. Read `report.validationHints` before marking output SF5-ready.
3. Use `report.componentRecipes` for starter SF5 structure.
4. Treat `report.smartHints` as advisory until behavior is confirmed.
5. Validate final SF5 snippets with strict catalog validation.

## Next Practical Use

Use Tailwind Plus/Application UI blocks as source inspiration only after license review. Convert the pattern into an original SF5 example, then validate it through this pipeline.
