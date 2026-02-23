---
name: sf5
description: Build, refactor, and maintain SIMAI Framework 5 (SF5) projects with frontend-first workflows for core, loader, utilities, components, smart-components, and blocks. Use when tasks involve SF5 architecture decisions, implementation patterns, code reviews, migration planning, or staged backend planning for Bitrix and Laravel.
---

# SF5

## Scope

- Treat this skill as frontend-first.
- Cover these layers first: core, loader, utilities, components, smart-components, blocks.
- Keep backend guidance at planning level until backend references are filled.

## Mandatory Workflow

1. Map the task to one or more SF5 layers.
2. Read `references/project-conventions.md` before proposing structure, naming, or contracts.
3. Read the relevant frontend references:
   - `references/frontend-playbook.md`
   - `references/frontend-loader.md` when loader/runtime is involved
   - `references/frontend-modifiers.md` for utility classes and theming
   - `references/frontend-components-smart.md` for component boundaries
4. Load vendor SF5 manifests for authoritative class/loader/smart contracts:
   - `references/vendor/source/catalog-lite.sf-only.json`
   - `references/vendor/manifest/sf5.excluded-non-sf-classes.json`
   - `references/vendor/manifest/sf5.conditions.json`
   - `references/vendor/manifest/sf5.loader.json`
   - `references/vendor/manifest/sf5.smart.json`
   - `references/vendor/registries/smart-codes.json`
   - `references/vendor/manifest/sf5.tokens.sf.json`
5. Implement at the narrowest layer that solves the task:
   - `core`: framework primitives and contracts
   - `loader`: bootstrapping and dependency wiring
   - `utilities`: shared helpers
   - `components`: reusable UI units
   - `smart-components`: stateful orchestration
   - `blocks`: page/feature composition
6. Validate behavior in both isolated and composed scenarios.
7. Report assumptions explicitly when project conventions are missing.

## Output Contract

For every substantial SF5 task, produce:

1. Layer mapping and decision rationale.
2. Planned/changed contracts (if any).
3. Verification checklist and result.
4. Follow-up items that require project-specific data.

## Layer Boundaries

### Core

- Keep contracts, base abstractions, and cross-cutting primitives.
- Avoid UI and feature-specific logic.

### Loader

- Keep startup deterministic and idempotent.
- Register modules explicitly and preserve stable boot order.

### Utilities

- Keep helpers framework-agnostic where possible.
- Prefer pure functions and avoid hidden side effects.

### Components

- Keep presentational behavior and local interaction logic.
- Delegate orchestration and data side effects to smart-components.

### Smart-components

- Coordinate state, data loading, and side effects.
- Keep side effects explicit and testable.

### Blocks

- Compose features from components and smart-components.
- Define explicit input/output contracts and extension points.

## Missing Data Protocol

- If required behavior is not documented in `references/project-conventions.md` or source docs, proceed with safe defaults.
- Mark each non-documented decision as `ASSUMPTION:` in task output.
- Keep patches minimal and reversible until project-specific conventions are confirmed.

## Resource Routing

- Read `references/frontend.md` first for scope, source map, and global rules.
- Read `references/project-conventions.md` for team-specific naming, layout, and compatibility requirements.
- Read `references/frontend-playbook.md` for deterministic implementation and review steps.
- Read `references/page-layout-playbook.md` when building or refactoring full page layouts.
- Read `references/page-recipes-index.md` to start from page-type templates.
- Read `references/page-recipe-routing.md` and use `scripts/recommend_page_recipe.py` for prompt-to-recipe routing.
- Use `scripts/generate_page_scaffold.py` to create starter page markup from recipe type.
- Use `scripts/run_local_checks.sh` to run full local validation suite before delivery.
- Use `scripts/install_pre_commit_hook.sh` to enforce local checks on commits that change `skills/sf5`.
- Use `scripts/migrate_recipe_classes_to_vendor.py --write` to normalize legacy recipe classes to vendor naming.
- Use `scripts/validate_page_recipes.py --strict` to verify recipe class compatibility against docs manifest.
- Read `references/task-intake-template.md` when clarifying task boundaries and acceptance criteria.
- Read `references/frontend-loader.md` for SFLoader architecture, cache model, API methods, and debug flow.
- Read `references/frontend-modifiers.md` for utility syntax, breakpoints, color roles, and RTL-safe styling.
- Read `references/frontend-components-smart.md` for boundaries between components, smart-components, and blocks.
- Read and reuse starter templates:
  - `references/component-template.md`
  - `references/smart-component-template.md`
  - `references/block-template.md`
- Use `scripts/generate_component_scaffold.py` to generate starter snippets for `component|smart|block`.
- Read `references/ui-doc-atlas-usage.md` before large lookup tasks.
- Use `scripts/query_ui_doc_manifest.py` with `references/ui-doc-manifest.json` to find exact doc pages quickly.
- Use `references/ui-doc-full-map.md` and `references/ui-doc-utility-atlas.md` for exhaustive documentation coverage.
- Read `references/ui-doc-curated-map.md` to locate the original doc pages by topic.
- Prefer vendor data as the source of truth for strict class/state/smart validation:
  - `references/vendor/source/catalog-lite.sf-only.json`
  - `references/vendor/manifest/sf5.conditions.json`
  - `references/vendor/manifest/sf5.excluded-non-sf-classes.json`
  - `references/vendor/manifest/sf5.smart.json`
  - `references/vendor/registries/smart-codes.json`
  - `references/vendor/manifest/sf5.tokens.sf.json`
- Read `references/backend-bitrix.md` only for Bitrix backend planning.
- Read `references/backend-laravel.md` only for Laravel backend planning.
- Keep SKILL.md compact; store variant-specific rules in references.
- Use `scripts/validate_page_recipes.py --strict` for compatibility validation (vendor + docs manifest).
- Use `scripts/validate_page_recipes.py --strict --catalog-strict` for vendor-only class whitelist enforcement.
- Use `scripts/migrate_recipe_classes_to_vendor.py --strict` in CI to detect legacy class aliases in recipes.
- Use `scripts/validate_sf5_html_files.py --strict --catalog-strict <path...>` for real HTML/PHP template validation.
- For one-shot local parity with CI, run `scripts/run_local_checks.sh`.
- Validate component/smart/block templates with:
  - `scripts/validate_page_recipes.py --strict --catalog-strict --recipes-glob references/component-template.md`
  - `scripts/validate_page_recipes.py --strict --catalog-strict --recipes-glob references/smart-component-template.md`
  - `scripts/validate_page_recipes.py --strict --catalog-strict --recipes-glob references/block-template.md`
- For standalone HTML checks, adapt `references/vendor/tools/validate-sf5-html.js` and `references/vendor/tools/sf5-lint.php` patterns.

## Delivery Rules

- Preserve backward compatibility unless the task explicitly allows breakage.
- Prefer small patches aligned with existing project conventions.
- Implement safe defaults when context is incomplete and mark each non-documented decision as `ASSUMPTION:`.
