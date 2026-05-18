---
name: sf5
description: Build, refactor, and maintain SIMAI Framework 5 (SF5) projects with frontend-first workflows for core, loader, utilities, components, smart-components, and blocks. Use when tasks involve SF5 architecture decisions, implementation patterns, code reviews, migration planning, or staged backend planning for Bitrix and Laravel.
---

# SF5

Use this skill as an SF5 coordinator, not as one monolithic expert. The coordinator selects the activity, engages only the relevant specialists, executes the nearest useful batch, validates it, and records the remaining path cleanly.

Before activity logic, load and obey:

- [kernel/sf5-dna.md](./kernel/sf5-dna.md)
- [kernel/scope-contract.md](./kernel/scope-contract.md)
- [kernel/output-contract.md](./kernel/output-contract.md)
- [rules/routing.md](./rules/routing.md)
- [rules/decision-policy.md](./rules/decision-policy.md)
- [rules/change-gates.md](./rules/change-gates.md)
- [rules/skill-mesh-balance.md](./rules/skill-mesh-balance.md)

Do not load every file by default. Load narrowly, then expand only when the task crosses SF5 surfaces.

## Core Operating Model

Follow this sequence for every substantial SF5 task:

1. Identify the user goal and derive `Done when` if it is missing.
2. Identify the primary activity from [activities/activity-registry.json](./activities/activity-registry.json).
3. If the activity is not obvious, use `scripts/recommend_sf5_activity.py`.
4. Select the smallest sufficient specialist set using [rules/routing.md](./rules/routing.md).
5. Define specialist roles with [rules/specialist-engagement-model.md](./rules/specialist-engagement-model.md) when the task is non-trivial.
6. Load only the selected activity manifest, specialist profiles, knowledge packs, and directly required references.
7. Map the task to one or more SF5 layers or surfaces.
8. Execute the current batch without waiting for confirmation unless a real blocker appears.
9. Validate at the right depth: source truth, routing, scaffolds, working-set outputs, or strict local checks.
10. Apply explicit change gates from [rules/change-gates.md](./rules/change-gates.md) when the task touches source refresh, working-set, or validation surfaces.
11. Update durable references, fixtures, or source-backed artifacts when the change makes them relevant.
12. When implementing an SEO Contract from `$seo`, keep `$seo` as the contract owner and implement through SF5-owned surfaces: semantic HTML, layout, components, smart-components, blocks, loader behavior, renderability, headings, internal links, media behavior, and visible content order. If SF5 constraints conflict with the contract, report a blocker back to `$seo` instead of silently changing URL/canonical/meta/content decisions.
13. For substantial SF5 documentation, docs maps, screenshots, developer usage docs, or documentation audits, use `$docs` as the technical-writing owner and keep `$sf5` responsible for source-backed SF5 facts, examples, compatibility, and validation.
14. If a reusable SF5 lesson was learned, apply [rules/learning.md](./rules/learning.md) and update the narrowest owner.

Autonomy is the default for work packages. If the user explicitly asks only to discuss or analyze, stay in that narrower mode.

## Default Activities

Use activity manifests as the first routing layer:

- [activities/source-refresh.json](./activities/source-refresh.json)
- [activities/routing-maintenance.json](./activities/routing-maintenance.json)
- [activities/recipe-scaffold-maintenance.json](./activities/recipe-scaffold-maintenance.json)
- [activities/working-set-maintenance.json](./activities/working-set-maintenance.json)
- [activities/tailwind-conversion.json](./activities/tailwind-conversion.json)
- [activities/validation-hardening.json](./activities/validation-hardening.json)
- [activities/documentation-update.json](./activities/documentation-update.json)
- [activities/skill-architecture-update.json](./activities/skill-architecture-update.json)

If no activity matches, create a temporary activity with:

- `activity_id`
- `title`
- `triggers`
- `required_specialists`
- `optional_specialists`
- `required_rules`
- `required_outputs`

## Specialists

Default specialist roles:

- `task-goal`: goal, `Done when`, scope control, remaining work
- `source-sync`: source mirrors, inventory, upstream drift, source-backed truth
- `routing-orchestrator`: scenarios, recipe routing, playbook routing, fixtures
- `recipe-scaffold`: page recipes, generators, starter templates
- `working-set`: bundle generation, section variants, upstream extraction
- `tailwind-converter`: Tailwind CSS to SF5 conversion, mapping quality, unmapped token reports
- `validation-qa`: validators, regression fixtures, strict local checks
- `bitrix-integration`: Bitrix installable usage, local asset packaging, `sfPath`/`sfSmartPath` wiring, admin/public demo surfaces, and storage-safe deployment.
- `docs-learning`: SF5 references, indexes, usage facts, and narrow learning updates; coordinate substantial writing method with `$docs`
- `skill-maintainer`: coordinator architecture, metadata, folder structure

Load specialist files only when selected:

- [specialists/task-goal/profile.md](./specialists/task-goal/profile.md)
- [specialists/source-sync/profile.md](./specialists/source-sync/profile.md)
- [specialists/routing-orchestrator/profile.md](./specialists/routing-orchestrator/profile.md)
- [specialists/recipe-scaffold/profile.md](./specialists/recipe-scaffold/profile.md)
- [specialists/working-set/profile.md](./specialists/working-set/profile.md)
- [specialists/tailwind-converter/profile.md](./specialists/tailwind-converter/profile.md)
- [specialists/validation-qa/profile.md](./specialists/validation-qa/profile.md)
- [specialists/bitrix-integration/profile.md](./specialists/bitrix-integration/profile.md)
- [specialists/docs-learning/profile.md](./specialists/docs-learning/profile.md)
- [specialists/skill-maintainer/profile.md](./specialists/skill-maintainer/profile.md)

## Coordinator Rules

The coordinator must:

1. keep work inside SF5 scope;
2. choose the narrowest useful activity;
3. avoid mixing source refresh, routing changes, recipe changes, and working-set changes into one undocumented batch;
4. assign specialists as `author`, `reviewer`, `gatekeeper`, or `consulted` when the task is non-trivial;
5. require validation for all routing, working-set, validator, or source-backed truth changes;
6. keep `SKILL.md` compact and push detail into activities, specialists, rules, and references;
7. stop only for real blockers: missing access, broken upstream source, unsafe irreversible action, or materially different architectural choices that cannot be inferred safely.

## Required Baseline

For substantial tasks, the baseline result must include:

1. Goal and `Done when` or a compact equivalent.
2. Selected activity and specialist set for non-trivial work.
3. Implemented or documented current batch.
4. Verification result or a clear reason verification could not run.
5. Remaining required work and optional follow-up.

Use templates when helpful:

- [quality/specialist-assessment-template.md](./quality/specialist-assessment-template.md)
- [quality/coordinator-gate-template.md](./quality/coordinator-gate-template.md)

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
- Read `references/source-repositories.md` before source-backed discovery or upstream refresh tasks.
- Read `references/source-inventory.md` to see shipped coverage and where runnable examples exist.
- Read `references/pattern-playbooks.md` for recurring UI tasks such as forms, dropdowns, overlays, pagination, and uploads.
- Read `references/pattern-routing.md` or use `scripts/recommend_ui_pattern.py` to route recurring UI tasks to the right playbook.
- Read `references/product-scenarios.md` or use `scripts/recommend_product_scenario.py` for whole feature screens such as auth, catalog, checkout, profile, and dashboard.
- Read `references/routing-overview.md` or use `scripts/recommend_sf5_route.py` for one-shot top-level routing from task -> scenario -> recipe -> patterns.
- Read `references/activity-routing-overview.md` or use `scripts/recommend_sf5_activity.py` for coordinator-level activity, specialist, and gate selection.
- Read `knowledge-packs/tailwind-to-sf5-conversion.md` before Tailwind CSS, Tailwind UI, or Tailwind Plus conversion tasks.
- Read `references/execution-workflow.md` for the default step-by-step execution order from intake to validation.
- Read `references/task-preparation.md` or use `scripts/prepare_sf5_task.py` when you want a prepared task brief and optional starter scaffold in one command.
- Read `references/working-set-generation.md` or use `scripts/generate_sf5_working_set.py` when you want a ready directory with route data, task brief, scaffold, and reference index.
- Read `references/working-set-coverage.md` or use `scripts/build_working_set_coverage.py` to see which recipe types already have section coverage and upstream extraction support.
- Read `references/sf5-fast-start.md` when the user wants to connect SF5 quickly and start layout work immediately.
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
- Read `references/spacing-radius-pairs.md` when choosing padding, gap, margin, and radius utilities for cards, panels, nested surfaces, code/source blocks, chips, and compact controls.
- Read `references/frontend-components-smart.md` for boundaries between components, smart-components, and blocks.
- Read `references/bitrix-ui-smart-integration.md` when packaging SF5 UI assets into Bitrix modules, wiring `sfPath`/`sfSmartPath`, or building Bitrix-native SF5 demo pages.
- Read `knowledge-packs/backend-first-smart-runtime.md` when working on backend-first `Smart::render()`, `Smart::tree()`, smart manifests, smart templates, composite smart runtime, or smart runtime proofs.
- Read `knowledge-packs/smart-component-implementation.md` when creating, syncing, or reviewing backend/frontend smart components, especially overlay and navigation primitives such as `drawer`, `modal`, `sidebar`, `side-menu`, `top-menu`, and `navigation-shell`.
- Read `knowledge-packs/demo-path-overlay-playground.md` when `/demo/framework/` or another demo path is used as a path-scoped `simai.data` overlay with composite smart artifacts.
- Read `references/ux-implementation-contract.md` when a `$ux` screen spec or UX handoff exists, or when the task starts from interface design.
- Read `references/component-smart-catalog.md` when choosing existing shipped components or smart-components.
- Read and reuse starter templates:
  - `references/component-template.md`
  - `references/smart-component-template.md`
  - `references/block-template.md`
- Use `scripts/generate_component_scaffold.py` to generate starter snippets for `component|smart|block`.
- Read `references/ui-doc-atlas-usage.md` before large lookup tasks.
- Use `scripts/sync_source_repos.py` to sync the local ignored source mirror in `source/simai/`.
- Use `scripts/build_source_inventory.py` to refresh the source-backed coverage map after syncing.
- Use `scripts/recommend_ui_pattern.py "<task>"` to route recurring UI tasks quickly.
- Use `scripts/recommend_product_scenario.py "<task>"` to route product-level screen tasks quickly.
- Use `scripts/recommend_sf5_route.py "<task>"` to get the top scenario, page recipe, scaffold command, and key playbooks in one step.
- Use `scripts/recommend_sf5_activity.py "<task>"` to get the top activity, specialist set, knowledge packs, and gate rules in one step.
- Use `scripts/prepare_sf5_task.py "<task>" --scaffold-out /tmp/page.html` to build a task brief and optional starter scaffold together.
- Use `scripts/generate_sf5_working_set.py "<task>" --out-dir /tmp/sf5-task` to build a ready working directory for immediate implementation.
- Extend working set coverage through:
  - `references/vendor/working-set.section-variants.json`
  - `references/vendor/working-set.legacy-class-map.json`
- Refresh coverage reports with:
  - `scripts/build_working_set_coverage.py`
- Use `scripts/generate_page_scaffold.py --type <auth|landing|catalog|dashboard|article|checkout|profile>` to generate starter page markup from recipe type.
- Use `scripts/build_component_smart_catalog.py` after source sync to refresh the source-backed component and smart-component catalog.
- Use `scripts/run_tailwind_conversion_lab.py` to build an ignored `output/tailwind-to-sf5-lab/` QA harness for Tailwind-to-SF5 source-inspired conversion checks.
- Use `scripts/run_tailadmin_page_examples.py` to build ignored `output/tailwind-to-sf5-tailadmin-pages/` concrete TailAdmin page examples with source/SF5 panes, conversion reports, screenshots, and visual scores.
- Use `scripts/capture_html_screenshot.py <html> --output <png>` as a Chrome/Chromium fallback when browser-use screenshot capture times out during local visual QA.
- Use `scripts/score_lab_visual.py <png>` to compute a lightweight screenshot-based source/SF5 similarity regression score for the conversion lab.
- Use `scripts/query_ui_doc_manifest.py` with `references/ui-doc-manifest.json` to find exact doc pages quickly.
- Use `references/ui-doc-full-map.md` and `references/ui-doc-utility-atlas.md` for exhaustive documentation coverage.
- Read `references/ui-doc-curated-map.md` to locate the original doc pages by topic.
- Use source mirrors as topic-specific truth:
  - `source/simai/ui-doc/source/docs/ru` for docs pages
  - `source/simai/ui-play/examples` for runnable examples
  - `source/simai/ui/distr/component` for shipped component inventory
  - `source/simai/ui-smart/smart` for shipped smart inventory
  - `source/simai/ui-utilities/distr/utility` for utility group inventory
- Prefer vendor data as the source of truth for strict class/state/smart validation:
  - `references/vendor/source/catalog-lite.sf-only.json`
  - `references/vendor/source-repos.json`
  - `references/vendor/source-inventory.json`
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
