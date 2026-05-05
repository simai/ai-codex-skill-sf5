# TZ: Tailwind CSS to SF5 Converter Stage 1-2

This TZ defines the first executable batch for the `tailwind-converter` specialty.

## Goal

Create the minimum reliable foundation for converting Tailwind utility-heavy markup into SF5-safe markup:

- classify Tailwind classes by intent;
- map only verified direct utility equivalents;
- report unmapped or unsafe classes instead of silently dropping them;
- validate mapping data against the SF5 vendor class catalog.

## Done When

- Tailwind class families are described in `references/vendor/tailwind-to-sf5.class-groups.json`.
- Initial direct utility mappings are described in `references/vendor/tailwind-to-sf5.utility-map.json`.
- Stage 1-2 fixtures are described in `references/vendor/tailwind-to-sf5.fixtures.json`.
- First component-recognition hints are described in `references/vendor/tailwind-to-sf5.component-hints.json`.
- Component-specific advisory recipes are described in `references/vendor/tailwind-to-sf5.component-recipes.json`.
- Smart-component advisory hints are described in `references/vendor/tailwind-to-sf5.smart-hints.json`.
- First end-to-end validated examples are saved in `references/tailwind-to-sf5-e2e-examples.md`.
- `scripts/convert_tailwind_to_sf5.py` converts class strings and HTML snippets into SF5 draft output with a report.
- `scripts/validate_tailwind_mapping_artifacts.py` validates all three artifacts.
- `scripts/validate_tailwind_converter.py` validates converter output against fixtures.
- `scripts/validate_tailwind_conversion_contract.py` requires these artifacts.
- `scripts/run_local_checks.sh` runs the new validator.

## Scope

In scope:

- class-family taxonomy for layout, spacing, sizing, typography, color, border/radius/shadow, responsive/state, structure helpers, and behavior-adjacent classes;
- first direct mappings for low-risk SF5 classes confirmed in `catalog-lite.sf-only.json`;
- explicit `blocked` and `deferred` entries for risky Tailwind patterns;
- fixture coverage for card, form, toolbar, and behavior-adjacent negative cases.

Out of scope for this batch:

- parsing full HTML documents;
- rewriting class attributes automatically;
- component and smart-component substitution;
- pixel-perfect Tailwind Plus block conversion;
- storing copied commercial Tailwind Plus source snippets.

## Implementation Plan

1. Add class-family taxonomy with matcher patterns and conversion policy.
2. Add initial direct utility map with `mapped`, `deferred`, and `blocked` statuses.
3. Add fixtures that describe expected family detection and mapping behavior.
4. Add a converter that applies mapped classes, removes unmapped classes from draft output by default, and reports mapped/deferred/blocked/unmapped buckets.
5. Add validators that check artifact shape, unique identifiers, mapping references, fixture references, target SF5 classes, and converter output.
6. Wire the validators into the Tailwind conversion contract and local checks.

## Acceptance Criteria

- Every mapped target class exists in the SF5 vendor class catalog.
- No fixture references an unknown class family.
- No fixture expects a mapped class that is missing from the utility map.
- Unsupported Tailwind behavior classes such as `group`, `peer`, `dark:*`, and `disabled:*` are represented as `deferred` or `blocked`.
- The validator fails if a future change removes the class groups, utility map, fixtures, or learning plan.

## Converter CLI

Use:

- `scripts/convert_tailwind_to_sf5.py "flex flex-col gap-2"`
- `scripts/convert_tailwind_to_sf5.py --html-string '<div class="flex gap-2"></div>'`
- `scripts/convert_tailwind_to_sf5.py --input /path/to/snippet.html --mode html`
- `scripts/convert_tailwind_to_sf5.py --html-string '<nav class="flex gap-2"><button>Filter</button></nav>' --render-recipe --format text`
- `scripts/convert_tailwind_to_sf5.py --html-string '<table class="w-full"></table>' --render-recipe data-table --format json`

Default behavior:

- mapped classes are replaced with SF5 target classes;
- `sm:`, `md:`, `lg:`, `xl:`, `hover:`, `focus:`, and `active:` prefixes are mapped only when every prefixed target exists in the SF5 catalog;
- deferred, blocked, and unmapped classes are omitted from draft output and listed in the report;
- component-recognition hints are reported as guidance, not applied as automatic component replacement;
- detected component hints attach advisory recipes with route, conversion steps, starter markup, source refs, and manual checks;
- smart-component recognition is advisory and reports candidate `sf-code` values without inserting them automatically;
- `validationHints` report strict-catalog readiness and manual review blockers before output is marked SF5-ready;
- `--render-recipe` emits starter SF5 markup for the first detected recipe, while `--render-recipe <recipe-id>` selects a specific detected recipe;
- `--gate-tailwind-residue` fails when output marked SF5-ready still contains Tailwind-like residue;
- `--inventory <file-or-dir>` scans real Tailwind-heavy projects and reports classes, component hints, smart hints, and migration risks;
- `--keep-unmapped` preserves deferred, blocked, and unmapped source classes for diagnostic output.

## Next Batch After This TZ

Expand the Tailwind converter further:

- add source-backed recipes that can consume converted examples into working-set sections;
- add real project migration reports from representative Tailwind-heavy repositories;
- add source-backed SF5 examples from Tailwind Plus/Application UI inspiration after license review.
