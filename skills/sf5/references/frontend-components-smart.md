# SF5 Components, Smart-Components, And Blocks

This file defines practical boundaries using the current docs snapshot.

## Documentation Status

- `components/introduction.md` is currently a roadmap page.
- `smart-components/introduction.md` is currently a roadmap page.
- Most concrete smart-component behavior is documented under loader frontend pages.

Use the rules below as the working contract until dedicated component docs are completed.

## Layer Boundaries

- `components`: reusable presentational UI with minimal side effects.
- `smart-components`: stateful orchestration, data loading, events, lifecycle logic.
- `blocks`: composition layer for features/pages, wiring inputs/outputs between components and smart-components.

Rule of thumb:

- Keep rendering primitives in `components`.
- Keep async/data/cache/event orchestration in `smart-components`.
- Keep page business composition in `blocks`.

## Smart-Component Runtime Contract

Docs describe smart components as:

- rendered from `<smart ... />` nodes
- identified by `name`
- configurable through attributes such as `data`, `property`, `events`, `modify`
- dynamically loaded via CSS/JS and template cache

Path pattern examples shown in docs:

- CSS:
  `/simai/asset/simai.framework/sf5.master/smart/<name>/css/<name>.css`
- JS:
  `/simai/asset/simai.framework/sf5.master/smart/<name>/js/<name>.js`

## Smart Template Caching

Template cache is tied to loader hash/page identity.

- localStorage key: `SF_SMART_LIST-<pageHash>`
- cached templates may be compressed/decompressed via UTF16 strategy
- fake templates may be used to speed up initial insertion

## Recommended Build Flow For New Smart-Component

1. Define public contract (`name`, expected attributes, events).
2. Implement presentational parts in a plain component first.
3. Implement smart orchestration and bind component rendering.
4. Ensure loader discovery and asset path resolution work.
5. Validate first-load, warm-cache, and cache-cleared behavior.
6. Validate composition inside at least one real block.

## Starter Templates And Generator

- Component starter:
  `references/component-template.md`
- Smart-component starter:
  `references/smart-component-template.md`
- Block starter:
  `references/block-template.md`
- Scaffold generator:
  `scripts/generate_component_scaffold.py`

Example commands:

```bash
skills/sf5/scripts/generate_component_scaffold.py --kind component --name productCard --title "Product card" --snippet-only
skills/sf5/scripts/generate_component_scaffold.py --kind smart --name catalogCards --title "Catalog cards" --smart-code cards --snippet-only
skills/sf5/scripts/generate_component_scaffold.py --kind block --name catalogSection --title "Catalog section" --snippet-only
```

Validation commands:

```bash
skills/sf5/scripts/validate_page_recipes.py --strict --catalog-strict --recipes-glob skills/sf5/references/component-template.md
skills/sf5/scripts/validate_page_recipes.py --strict --catalog-strict --recipes-glob skills/sf5/references/smart-component-template.md
skills/sf5/scripts/validate_page_recipes.py --strict --catalog-strict --recipes-glob skills/sf5/references/block-template.md
skills/sf5/scripts/validate_sf5_html_files.py --strict --catalog-strict /path/to/component-template.html
```

## Regression Checklist

1. Check component still renders without smart orchestration where applicable.
2. Check smart component does not duplicate side effects on repeated loader events.
3. Check template cache invalidation after markup/schema changes.
4. Check block composition remains stable when one child component fails to load.
