# SF5 Scenario: Dashboard Workspace

Use this scenario for operator/admin/workspace screens with KPIs, widgets, tables, recent activity, actions, and empty states.

## Build From

- `references/page-recipe-dashboard.md`
- `references/pattern-pagination-filters.md`
- `references/pattern-feedback-overlays.md`
- `source/simai/ui-play/examples/tables/tables-default-parameters/index.html`
- `source/simai/ui-play/examples/components/buttons/all/index.html`

## Default Screen Structure

1. Top bar with actions
2. Sidebar or tabbed workspace navigation
3. KPI row
4. Main widgets or charts
5. Table/list section
6. Empty / loading / no-data surfaces

## Recommended Composition

- KPIs:
  presentational cards
- Filters/actions:
  buttons, dropdowns, tags, toggles
- Tables:
  static table utilities for data-heavy blocks
- Feedback:
  toast for soft actions, modal for destructive/critical actions
- Empty state:
  card or bordered surface with recovery CTA

## Practical Rules

- Keep widgets presentational and reusable.
- Keep data fetching and orchestration in smart-components.
- Do not bury primary actions inside dense tables.
- Use empty states explicitly instead of blank panels.
