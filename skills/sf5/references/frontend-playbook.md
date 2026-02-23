# SF5 Frontend Playbook

Use this playbook for implementation, refactor, and review tasks.

## Mode 1: Implement Feature

1. Read task scope and map layers.
2. Read `project-conventions.md` and relevant layer references.
3. Define minimal contract changes (if any).
4. Implement in one layer at a time.
5. Run required checks.
6. Report assumptions and verification.

## Mode 2: Refactor Without Behavior Change

1. Capture current behavior and contracts.
2. Restrict changes to structure/readability.
3. Keep runtime output and public contracts identical.
4. Re-run loader/cache and responsive checks.
5. Report zero-behavior-delta evidence.

## Mode 3: Review/Diagnosis

1. Identify failing layer and boundary crossing.
2. Check loader lifecycle, cache keys, and dependency ordering.
3. Check utility class correctness and breakpoint/state usage.
4. Check component vs smart-component responsibility split.
5. Provide root cause and minimal fix path.

## Mode 4: Build Page Layout

1. Use `task-intake-template.md` to lock scope and breakpoints.
2. Use `ui-doc-atlas-usage.md` + manifest query script to find exact utility pages.
3. Select baseline blueprint in `page-recipes-index.md`.
4. Assemble layout with `page-layout-playbook.md`.
5. Normalize classes with `scripts/migrate_recipe_classes_to_vendor.py --write`.
6. Validate via `scripts/validate_page_recipes.py --strict --catalog-strict`.
7. Validate responsive/theme/state matrix before finalizing.

## Local Check Suite

- Run full local suite:
  `scripts/run_local_checks.sh`
- Install git pre-commit hook for automatic checks on `skills/sf5` changes:
  `scripts/install_pre_commit_hook.sh`
- Validate real templates/snippets (outside recipe markdown):
  `scripts/validate_sf5_html_files.py --strict --catalog-strict <path...>`

## Layer-Specific Gates

### Core Gate

- Keep change framework-level and reusable.
- Avoid feature-specific UI logic.

### Loader Gate

- Keep startup idempotent.
- Validate discovery -> dependency -> asset load -> ready flow.
- Validate both warm cache and cleared cache behavior.

### Utilities Gate

- Keep token/role-driven styling.
- Check responsive and state prefixes.
- Preserve LTR/RTL safety via logical properties.

### Components Gate

- Keep presentational responsibility local.
- Avoid hidden data-fetch side effects.

### Smart-Components Gate

- Keep side effects explicit.
- Ensure loader/template/cache integration is stable.
- Ensure repeated events do not duplicate effects.

### Blocks Gate

- Keep composition explicit.
- Prevent business logic leakage into presentational components.

## Required Verification Matrix

1. Cold load (after cache clear).
2. Warm load (existing cache).
3. One mobile breakpoint and one desktop breakpoint.
4. One interactive state check (`hover`, `focus`, or `active`) where relevant.
5. One composed block integration check.

## Report Template

1. Layer mapping:
   `...`
2. Contracts changed:
   `...`
3. Verification result:
   `...`
4. Assumptions:
   `...`
5. Follow-up data needed:
   `...`
