# SF5 Scenario: Catalog Listing

Use this scenario for product or content listings with search, filters, cards, sorting, pagination, and empty states.

## Build From

- `references/page-recipe-catalog.md`
- `references/pattern-dropdown-selection.md`
- `references/pattern-pagination-filters.md`
- `references/pattern-feedback-overlays.md`
- `source/simai/ui-play/examples/components/pagination/default/index.html`
- `source/simai/ui-play/examples/components/tags/all/index.html`

## Default Screen Structure

1. Heading + search/sort row
2. Filter sidebar or filter bar
3. Results grid/list
4. Pagination / load more
5. Empty or no-results state

## Recommended Composition

- Search and sort:
  smart/static input + dropdown
- Filters:
  tags, toggles, range slider, checkbox/radio where needed
- Results:
  presentational cards in grid/list layout
- Pagination:
  smart `sf-pagination` when behavior is dynamic, static shell when server-rendered
- Empty state:
  message card + clear filters / reset CTA

## Practical Rules

- Keep filters detachable from cards.
- Do not mix too many control types in one row on mobile.
- Use tags for active filter feedback.
- Keep empty state in the same visual language as result cards.
