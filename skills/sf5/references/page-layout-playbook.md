# SF5 Page Layout Playbook

Use this playbook when the task is to build or refactor full page layout in SF5.

## Contents

- Input Checklist
- Step-By-Step Layout Workflow
- Ready Recipes
- Utility Group Mapping
- Typical Page Sections
- Verification Matrix

## Input Checklist

1. Page type:
   landing, dashboard, catalog, article, form-heavy page, mixed content.
2. Required breakpoints:
   mobile-first + target desktop behavior.
3. Theme requirements:
   light/dark or single theme.
4. Interaction requirements:
   hover/focus/active states and keyboard accessibility needs.

## Step-By-Step Layout Workflow

1. Build frame:
   use `layout/container` and `layout/max-container` for outer shell.
2. Build composition:
   pick `grid` or `flex` as primary composition model.
3. Apply spacing:
   use `indents` + `grid-and-flexbox-utilities/gap`.
4. Apply sizing:
   use `sizes` and constraints (`min-*`, `max-*` patterns).
5. Apply typography:
   use `typography` and `text-formatting` roles.
6. Apply color/theming:
   use role-driven background/border/text utilities and `theme-light`/`theme-dark`.
7. Apply states:
   use `hover:`, `focus:`, `active:` modifiers where needed.
8. Add optional visual layers:
   shadows, outline, divider, background gradient/pattern, filters.
9. Wire dynamic behavior:
   if needed, bind component loading/runtime through SFLoader conventions.

## Ready Recipes

- Landing:
  `references/page-recipe-landing.md`
- Catalog:
  `references/page-recipe-catalog.md`
- Dashboard:
  `references/page-recipe-dashboard.md`
- Article:
  `references/page-recipe-article.md`
- Checkout:
  `references/page-recipe-checkout.md`
- Index:
  `references/page-recipes-index.md`
- Prompt routing:
  `references/page-recipe-routing.md` and `scripts/recommend_page_recipe.py`
- Scaffold generation:
  `scripts/generate_page_scaffold.py`
- Legacy-to-vendor class normalization:
  `scripts/migrate_recipe_classes_to_vendor.py --write`
- Recipe validation:
  `scripts/validate_page_recipes.py --strict --catalog-strict`
- Real HTML template validation:
  `scripts/validate_sf5_html_files.py --strict --catalog-strict <path...>`
- Full local parity suite:
  `scripts/run_local_checks.sh`

## Utility Group Mapping

- Page shell:
  `utilities/layout/*`
- Columns and content grids:
  `utilities/grid/*`
- Axis alignment and placement:
  `utilities/flex/*`, `utilities/grid-and-flexbox-utilities/*`
- Spacing system:
  `utilities/indents/*`
- Visual hierarchy:
  `utilities/typography/*`, `utilities/text-formatting/*`
- Interactive affordances:
  `utilities/interactivity/*`, `utilities/outline/*`
- Brand/surface rendering:
  `utilities/background/*`, `utilities/border/*`, `utilities/shadows/*`

## Typical Page Sections

1. Header:
   container + flex row + spacing + interactive link styles.
2. Hero:
   grid/flex split + typography roles + action buttons.
3. Content cards/list:
   grid template + card spacing + border/shadow + responsive collapse.
4. Form area:
   forms utilities + focus states + validation color roles.
5. Footer:
   compact typography + divider + responsive alignment.

## Verification Matrix

1. Responsive:
   check at least `sm`, `md`, `lg`.
2. Theme:
   check `theme-light` and `theme-dark` where required.
3. States:
   check hover/focus/active for interactive elements.
4. Layout stability:
   check overflow, wrapping, and min/max constraints.
5. Loader integration:
   if page relies on dynamic components, verify cold/warm cache behavior.
