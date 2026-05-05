# SF5 Pattern: Pagination And Filters

Use this playbook for list paging, page-size selectors, filter bars, tag/toggle controls, and numeric ranges.

## Best Upstream Sources

- Static pagination:
  `source/simai/ui-play/examples/components/pagination/default/index.html`
- Smart pagination:
  `source/simai/ui-play/examples/smart-components/pagination/default/index.html`
- Static tags:
  `source/simai/ui-play/examples/components/tags/all/index.html`
- Static toggle:
  `source/simai/ui-play/examples/components/toggle/default/index.html`
- Static range slider:
  `source/simai/ui-play/examples/components/range-slider/default/index.html`
- Smart range slider:
  `source/simai/ui-play/examples/smart-components/range-slider/default/index.html`

## Default Decision

- Use static pagination when the surrounding list shell is server-rendered and markup ownership matters.
- Use smart pagination when you want the full SF5 custom-element pagination contract with selected count, numeric page list, page-size control, last-page control, and configurable top/main/bottom sections.
- Do not auto-promote compact previous/next-only pagers to `sf-pagination`; keep them as static markup or implement a separate compact recipe until a source-backed compact contract exists.
- Use tags/toggles/range sliders as filter controls around the paging shell.

## Static Pagination Shape

- Main wrapper:
  `sf-pagination`
- Typical sections:
  - `sf-pagination-top`
  - `sf-pagination-main`
  - `sf-pagination-bottom`
- Common companions:
  - `sf-page-number`
  - `sf-button`
  - embedded `sf-dropdown`
  - `sf-checkbox`

## Smart Pagination Shape

- Element:
  `sf-pagination`
- Useful attributes:
  - `current`
  - `total`
  - `top`
  - `bottom`
  - `top-class`
  - `main-class`
  - `bottom-class`

## Filter Controls

- Use `sf-tag` for filter chips, status chips, quantity chips, color chips.
- Use `sf-toggle` for binary filters or mode switches.
- Use `sf-range-slider` when numeric ranges should stay compact and visual.

## Practical Rules

- Keep pagination and filters in one horizontal system only when space allows.
- Prefer smart range slider for interactive change output and a simpler API.
- Use static tags/toggles when visual control over shell details matters.
- Keep page-size and bulk-action dropdowns inside the pagination area only if they are truly coupled to paging behavior.

## Common Assembly Pattern

1. Choose static or smart pagination shell.
2. Add page-size or action dropdowns only if the pattern needs them.
3. Add tags/toggles/range sliders as separate filter controls.
4. Use utilities for wrapping and breakpoint behavior.
5. Validate the final snippet.
