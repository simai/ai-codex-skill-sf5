# Learning Plan: Tailwind CSS to SF5 Converter Specialist

This plan is the staged learning track for the `tailwind-converter` specialist. Use it when developing the Tailwind CSS -> SF5 conversion capability over several future batches.

## Goal

Build a reliable specialist that can convert Tailwind-heavy markup and examples into SF5-safe markup, explain unmapped decisions, and turn useful source examples into reusable SF5 patterns without mixing conversion logic into unrelated scaffold or working-set layers.

## Operating Principles

- Learn from smallest repeatable units first: tokens, class groups, layout primitives, then components and full screens.
- Treat SF5 vendor data, `ui-doc`, `ui`, `ui-smart`, and `ui-play` as target truth.
- Treat Tailwind examples as source material, not target truth.
- Convert known patterns deterministically and report unknown classes instead of guessing.
- Preserve semantic HTML, `aria-*`, form behavior, and useful data hooks.
- Keep commercial Tailwind Plus examples behind license review before storing copied source markup in distributable artifacts.
- Every learning stage must leave a reusable artifact: mapping data, fixture, reference note, converter behavior, or validation gate.

## Stage 0: Orientation and Boundaries

Purpose:

- understand what the converter is allowed to do;
- separate project-owned Tailwind markup from third-party source material;
- define output contracts before building conversion logic.

Inputs:

- `knowledge-packs/tailwind-to-sf5-conversion.md`
- `specialists/tailwind-converter/profile.md`
- `references/frontend-modifiers.md`
- `references/frontend-components-smart.md`
- `references/source-inventory.md`

Exercises:

- classify 5 sample snippets as project-owned, third-party inspiration, or blocked by license uncertainty;
- define whether each sample should produce final SF5 markup, a conversion plan, or only an analysis report.

Deliverables:

- source/license decision checklist;
- initial conversion output contract;
- first negative examples: cases where conversion must stop or require manual review.

Gate:

- every source sample has ownership/license status;
- every output states whether it is SF5-ready, draft, or analysis-only.

## Stage 1: Tailwind Utility Taxonomy

Purpose:

- group Tailwind classes by intent before mapping them;
- avoid one giant class replacement table without semantic structure.

Class families:

- layout: `container`, `block`, `inline`, `flex`, `grid`, positioning;
- spacing: `p-*`, `px-*`, `m-*`, `space-*`, `gap-*`;
- sizing: `w-*`, `h-*`, `min-*`, `max-*`;
- typography: `text-*`, `font-*`, `leading-*`, `tracking-*`;
- color: `bg-*`, `text-*`, `border-*`, opacity;
- border/radius/shadow: `border`, `rounded-*`, `shadow-*`, `ring-*`;
- responsive/state: `sm:`, `md:`, `hover:`, `focus:`, `disabled:`;
- structure helpers: `sr-only`, `divide-*`, `aspect-*`, `overflow-*`;
- behavior-adjacent classes: `group`, `peer`, transition/animation utilities.

Exercises:

- parse Tailwind class strings into class-family buckets;
- produce a report with `known`, `unknown`, `deferred`, and `unsafe` buckets;
- compare each family against SF5 utility docs and vendor class catalog.

Deliverables:

- `references/vendor/tailwind-to-sf5.class-groups.json`;
- `references/vendor/tailwind-to-sf5.fixtures.json`;
- report schema for unmapped classes.

Gate:

- no class is silently dropped;
- unknown state/group behavior is reported, not converted.

## Stage 2: Direct Utility Mapping

Purpose:

- build deterministic mappings only where SF5 equivalent is known and validated.

Mapping types:

- direct one-to-one class replacements;
- scale translations where Tailwind spacing/size scale matches an SF5 token family;
- semantic replacements where Tailwind intent maps to SF5 utility group;
- blocked mappings where SF5 has no safe equivalent.

Exercises:

- convert simple cards, forms, and toolbar snippets using only utility mappings;
- run SF5 strict validation on converted output;
- produce an unmapped report for every fixture.

Deliverables:

- `references/vendor/tailwind-to-sf5.utility-map.json`;
- first converter fixture set in `references/vendor/tailwind-to-sf5.fixtures.json`;
- conversion report examples.

Gate:

- SF5-ready output passes `validate_sf5_html_files.py --strict --catalog-strict`;
- every unmapped Tailwind class is reported with reason and suggested next action.

Current Stage 1-2 tool:

- `scripts/convert_tailwind_to_sf5.py` converts class strings and HTML snippets using the verified utility map;
- prefix conversion is catalog-aware and maps `sm:`, `md:`, `lg:`, `xl:`, `hover:`, `focus:`, and `active:` only when prefixed SF5 target classes exist;
- `references/vendor/tailwind-to-sf5.component-hints.json` provides first hints for `auth-form`, `card`, `data-table`, and `toolbar`;
- `references/vendor/tailwind-to-sf5.component-recipes.json` attaches advisory SF5 routes, conversion steps, starter markup, source refs, and manual checks to those hints;
- `references/vendor/tailwind-to-sf5.smart-hints.json` reports advisory smart candidates such as `search`, `select`, `pagination`, `table`, and `cards`;
- `scripts/convert_tailwind_to_sf5.py --render-recipe` can print starter SF5 markup for the first detected recipe or a requested recipe id;
- converter reports include `validationHints`, `--gate-tailwind-residue`, and `--inventory`;
- `scripts/run_tailwind_conversion_lab.py` generates an ignored `output/tailwind-to-sf5-lab/` visual QA lab for source-inspired auth/card/table examples;
- `scripts/run_tailadmin_page_examples.py` generates ignored `output/tailwind-to-sf5-tailadmin-pages/` examples for concrete TailAdmin pages such as `signin` and `basic-tables`, with source excerpt, raw conversion report, finished SF5 markup, screenshot, and visual score per page;
- `scripts/build_component_smart_catalog.py` builds `references/vendor/component-smart-catalog.json` and `references/component-smart-catalog.md` from `ui`, `ui-smart`, and `ui-play` so the converter can prefer existing SF5 components and smart-components instead of only class mappings;
- `scripts/convert_tailwind_to_sf5.py --render-component` and `--render-smart` provide first source-backed starter rendering modes for component and smart-component replacement candidates;
- `references/vendor/tailwind-to-sf5.component-renderers.json` now covers concrete source-backed starters for `button`, `dropdown`, `input`, `pagination`, and `modal`, with regression fixtures in `references/vendor/tailwind-to-sf5.fixtures.json`;
- `scripts/run_tailadmin_page_examples.py` now emits `sf5-componentized.html`, `componentized-index.html`, componentized screenshots, componentized visual scores, and notes so source-backed component/smart replacements can be compared against manually finished SF5 output;
- `scripts/run_tailadmin_page_examples.py` also emits `runtime-index.html`, runtime screenshots, runtime visual scores, and `runtime-probe.json` so source-backed custom elements are checked with real `ui-smart` JS assets instead of CSS-only preview stubs;
- `scripts/probe_html_runtime.py` verifies expected custom elements through headless Chrome and marks component promotion as candidate only when runtime definition succeeds;
- `scripts/run_tailadmin_page_examples.py` now includes runtime component previews for `dropdown`, `pagination`, and `modal`, with converter `promotionGate` evidence in each `conversion.json`;
- `sf-pagination` promotion is constrained to the full source-backed SF5 pagination contract and must compare against the real ui-play source example; compact previous/next pagers remain manual/static until a compact contract is found;
- `sf-code="table"` is documented as registry-only in the current source mirror, so smart table promotion is blocked and static `table` utility markup is the SF5-ready path;
- promotion gate fixtures now cover `candidate`, `blocked-by-runtime`, `blocked-by-visual-delta`, and `blocked-by-missing-checklist`;
- `scripts/capture_html_screenshot.py` provides a local Chrome/Chromium screenshot fallback when browser-use can inspect DOM/console but cannot capture screenshots;
- `scripts/score_lab_visual.py` adds a screenshot-based visual similarity regression score for the first visible source/SF5 panel pair and rejects blank, loader-like, or near-black screenshots before scoring;
- validated e2e examples live in `references/tailwind-to-sf5-e2e-examples.md`;
- `scripts/validate_tailwind_converter.py` locks converter behavior against `references/vendor/tailwind-to-sf5.fixtures.json`.

## Stage 3: Responsive and State Mapping

Purpose:

- handle Tailwind prefixes and interaction states without corrupting behavior.

Topics:

- breakpoint prefixes: `sm:`, `md:`, `lg:`, `xl:`, `2xl:`;
- states: `hover:`, `focus:`, `active:`, `disabled:`;
- structural states: `group-*`, `peer-*`, `aria-*`, `data-*`;
- dark mode and color mode assumptions.

Exercises:

- convert responsive layout snippets;
- convert hover/focus button and input states;
- mark group/peer interactions as manual behavior unless SF5 equivalent exists.

Deliverables:

- prefix mapping rules;
- state conversion policy;
- regression fixtures for responsive and state-heavy class strings.

Gate:

- responsive prefixes map only to supported SF5 prefixes;
- group/peer/data/aria behavior is preserved or explicitly reported.

## Stage 4: Component Recognition

Purpose:

- move beyond utility class replacement and recognize source blocks as SF5 components.

Component candidates:

- button groups;
- input groups;
- alerts and placeholders;
- avatars;
- badges/tags;
- dropdowns/selects;
- cards and lists;
- tables.

Exercises:

- classify Tailwind blocks into presentational component families;
- replace source markup with SF5 component markup where there is a source-backed pattern;
- trace substitutions to `ui-play`, `ui-doc`, or shipped component inventory.

Deliverables:

- future `references/vendor/tailwind-to-sf5.component-patterns.json`;
- component recognition fixtures;
- component substitution report format.

Gate:

- component substitution must cite an SF5 source or recipe;
- if no source-backed SF5 component exists, preserve semantic HTML and convert utilities only.

## Stage 5: Smart-Component Recognition

Purpose:

- detect when Tailwind markup represents behavior that should become an SF5 smart-component or remain manual.

Smart candidates:

- modal/dialog flows;
- dropdown/select flows;
- upload/progress flows;
- gallery/media flows;
- pagination/filter/search flows;
- table interaction patterns.

Exercises:

- classify behavior zones inside Tailwind examples;
- map recognized flows to `sf-code` only when the target smart-component exists;
- report JS/headless behavior that cannot be safely migrated automatically.

Deliverables:

- future `references/vendor/tailwind-to-sf5.smart-patterns.json`;
- smart-component conversion fixtures;
- behavior gap report examples.

Gate:

- no arbitrary JS behavior is claimed as converted;
- smart substitutions must cite `ui-smart`, `ui-play`, or smart registry data.

## Stage 6: Tailwind Plus Application UI Source Adaptation

Purpose:

- use Tailwind Plus Application UI as source material for SF5 examples while respecting license boundaries.

Rules:

- analyze structure and interaction intent;
- produce original SF5 examples, not blind copies of commercial markup;
- keep source URL and license status in the conversion report;
- store copied source only when license status is explicitly approved.

Exercises:

- choose 3 low-risk Application UI blocks for analysis: auth form, settings form, table/listing toolbar;
- create original SF5 equivalents using existing recipes, components, and smart-components;
- record which Tailwind patterns became SF5 utilities, components, smart-components, or manual notes.

Deliverables:

- source-analysis notes;
- SF5 original examples;
- conversion reports with license status and source references.

Gate:

- no copied commercial source enters distributable artifacts without license approval;
- generated SF5 examples pass strict validation.

## Stage 7: Project Migration Workflow

Purpose:

- convert real Tailwind-heavy project screens into SF5 in a controlled way.

Workflow:

1. Inventory Tailwind source files.
2. Identify repeated blocks and class families.
3. Convert low-risk static markup first.
4. Recognize components and smart-components.
5. Produce unmapped and behavior reports.
6. Validate SF5 output.
7. Review visual and interaction differences.

Exercises:

- migrate one simple project page;
- migrate one dashboard/listing page;
- migrate one form-heavy page;
- collect repeated unmapped classes into mapping backlog.

Deliverables:

- future project conversion checklist;
- project conversion report template;
- mapping backlog from real project data.

Gate:

- converted files pass SF5 strict validation;
- remaining Tailwind residue is intentional and reported;
- behavior changes are listed before delivery.

## Stage 8: Converter Tooling

Purpose:

- turn manual learning into repeatable scripts and machine-readable data.

Tooling targets:

- `convert_tailwind_to_sf5.py`: HTML input -> SF5 HTML + report;
- mapping manifests under `references/vendor/`;
- fixtures under `references/vendor/`;
- validator for unmapped Tailwind residue;
- optional working-set integration for converted sections.

Exercises:

- implement class parser;
- implement mapping application;
- implement conversion report;
- add strict SF5 validation integration;
- add fixtures for each stage above.

Deliverables:

- converter script;
- mapping manifests;
- conversion fixtures;
- conversion gate validator;
- README and knowledge-pack updates.

Gate:

- converter output is deterministic;
- fixtures cover direct utilities, responsive/state, components, smart-components, and full-page migration;
- full local suite stays green.

## Stage 9: Advanced Composite Scenarios

Purpose:

- handle larger real-world conversions where a page mixes layout, components, smart behavior, and project-specific constraints.

Scenarios:

- admin dashboard with KPI cards, filter toolbar, data table, and empty state;
- checkout with delivery/payment/summary steps;
- profile settings with avatar upload and notification preferences;
- catalog listing with filters, sorting, cards, pagination, and empty state;
- content article with table of contents, related cards, and CTA blocks.

Exercises:

- convert one scenario end-to-end from Tailwind source;
- compare against existing SF5 page recipes and working-set sections;
- decide whether converter should emit full page, section variants, or only a report.

Deliverables:

- advanced fixtures;
- scenario-level conversion reports;
- working-set integration candidates.

Gate:

- converted scenario is traceable to recipe/scenario/playbook layers;
- no behavior is silently lost;
- strict validation and manual review checklist both pass.

## Stage 10: Maintenance and Learning Loop

Purpose:

- keep converter knowledge current as SF5 and Tailwind source examples evolve.

Routine:

- when `ui`, `ui-doc`, `ui-play`, or `ui-smart` changes, check whether target mappings improve or break;
- when real migrations expose repeated unmapped classes, add mapping candidates to backlog;
- when Tailwind examples introduce useful patterns, classify them into learning stages before converting.

Deliverables:

- mapping backlog;
- fixture updates;
- source-backed substitution notes;
- periodic conversion coverage report.

Gate:

- every new mapping has at least one fixture;
- every converter behavior change is covered by regression;
- every reusable lesson updates the narrowest owner: mapping manifest, knowledge pack, specialist profile, or roadmap.

## Immediate Next Batch

Move from synthetic converter fixtures to real source-inspired conversion:

- run `scripts/convert_tailwind_to_sf5.py --inventory <project-or-snippet-dir>` on a real Tailwind-heavy project or an approved local sample;
- choose one auth form, one card/list item, and one data-table/toolbar block for end-to-end conversion;
- use `--render-recipe` to produce an SF5 starter, then manually finish original SF5 markup;
- use `--gate-tailwind-residue` before treating converted output as SF5-ready;
- extend `tailwind-to-sf5.utility-map.json`, component hints, smart hints, and e2e fixtures only for repeated misses found in real conversions.
