# SF5 Frontend Reference

Use this file as the entry point for frontend work. It is based on the documentation snapshot located at:

`/Users/rim/Downloads/ui-doc-main (2)/ui-doc-main/source/docs/ru`

## Scope

- `core`: base contracts, tokens, and cross-cutting primitives.
- `loader`: runtime discovery, dynamic asset loading, caching, and lifecycle.
- `utilities`: modifier syntax, responsive/states, and design-token usage.
- `components`: presentational UI units.
- `smart-components`: stateful orchestration units with templates and loader integration.
- `blocks`: feature/page composition.

## What To Read For A Task

- Team-specific rules and folder conventions:
  `references/project-conventions.md`
- Deterministic implementation/review flow:
  `references/frontend-playbook.md`
- Full-page layout process:
  `references/page-layout-playbook.md`
- Ready page blueprints by type:
  `references/page-recipes-index.md`
- Prompt-to-recipe routing:
  `references/page-recipe-routing.md`
- Loader behavior, caching, preloader, and events:
  `references/frontend-loader.md`
- Utility classes, syntax, breakpoints, themes, and color roles:
  `references/frontend-modifiers.md`
- Component/smart-component/block implementation boundaries:
  `references/frontend-components-smart.md`
- Component/smart/block starter templates:
  `references/component-template.md`,
  `references/smart-component-template.md`,
  `references/block-template.md`
- Component/smart/block scaffold generation:
  `scripts/generate_component_scaffold.py`
- Full local check suite:
  `scripts/run_local_checks.sh`
- Pre-commit installer:
  `scripts/install_pre_commit_hook.sh`
- Real template validator:
  `scripts/validate_sf5_html_files.py`
- Request normalization template:
  `references/task-intake-template.md`
- Exhaustive atlas workflow and scripts:
  `references/ui-doc-atlas-usage.md`
- Full docs map and utility atlas:
  `references/ui-doc-full-map.md`, `references/ui-doc-utility-atlas.md`, `references/ui-doc-manifest.json`
- Original doc page index by topic:
  `references/ui-doc-curated-map.md`
- Vendor SF5 contracts and registries (authoritative for strict checks):
  `references/vendor/source/catalog-lite.sf-only.json`,
  `references/vendor/manifest/sf5.conditions.json`,
  `references/vendor/manifest/sf5.excluded-non-sf-classes.json`,
  `references/vendor/manifest/sf5.loader.json`,
  `references/vendor/manifest/sf5.smart.json`,
  `references/vendor/registries/smart-codes.json`,
  `references/vendor/manifest/sf5.tokens.sf.json`

## Global Frontend Rules

- Keep loader startup idempotent and deterministic.
- Keep utility usage token-based; avoid hardcoded values unless explicitly required.
- Keep custom CSS logical-direction friendly (prefer inline/block semantics over left/right).
- Keep smart-component side effects isolated from presentational components.
- Keep block composition explicit via input/output contracts.
- Prefer vendor whitelist/blacklist checks for classes and `sf-code` before accepting template output.

## Known Documentation Gaps

- `components/introduction.md` and `smart-components/introduction.md` are roadmap pages, not full specs.
- Several pages are high-level or placeholders and must be treated as intent, not full contract.
- Breakpoint values are inconsistent across pages; always verify actual project variables before changing responsive logic.

## Frontend Acceptance Checklist

- Confirm the change targets the correct SF5 layer.
- Confirm no new cyclic dependencies across layers.
- Confirm responsive behavior on at least one small and one large breakpoint.
- Confirm state modifiers (`hover`, `focus`, `active`) still match expected UX and accessibility.
- Confirm loader cache behavior after changes (`loader_clear=Y` path and normal cache path).
