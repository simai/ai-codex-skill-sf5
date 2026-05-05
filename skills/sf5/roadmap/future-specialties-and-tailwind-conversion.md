# SF5 Roadmap: Future Specialties and Tailwind Conversion

This roadmap captures useful follow-up work that should not be mixed into current implementation batches.

## Coordinator Maturity

- Run several real SF5 tasks through the coordinator, working-set, and validation flow.
- Use those field tests to prune weak fixtures and add practical route cases.
- Keep expanding specialist/activity context only when a new surface has stable ownership and its own validation path.

## Candidate Specialist Expansion

- `loader-runtime`: SF5 loader, boot order, idempotency, cache behavior, runtime init contracts.
- `utilities-catalog`: utility groups, tokens, vendor-safe class policy, docs-to-class mapping.
- `components-catalog`: shipped presentational components, source examples, component reuse rules.
- `smart-components-catalog`: `ui-smart`, `sf-code`, smart props/events/contracts, smart examples.
- `playground-examples`: `ui-play` examples, drift detection, source-backed snippet quality.
- `bundle-contract`: working-set manifest, sections, source refs, upstream extracts.
- `regression-architect`: fixture strategy, gate validators, machine-readable contracts.

## Tailwind CSS to SF5 Converter

Detailed learning plan:

- `roadmap/tailwind-to-sf5-learning-plan.md`
- Stage 1-2 executable TZ: `roadmap/tailwind-to-sf5-stage-1-2-tz.md`

Goal:

- make migration from Tailwind-heavy markup to SF5 utilities/components repeatable;
- reuse accumulated Tailwind UI examples as source material for SF5 examples;
- support controlled conversion of current projects into the SF5 design/runtime system.

Initial scope:

- convert class-level Tailwind utility patterns into SF5 utility equivalents where a known mapping exists;
- preserve semantic HTML and interaction hooks;
- flag unmapped classes and design decisions instead of guessing;
- prefer SF5 components and smart-components when a Tailwind block clearly represents a known SF5 component family;
- produce conversion reports with assumptions, unmapped tokens, and recommended follow-up checks.

Primary source candidates:

- existing project markup that uses Tailwind CSS;
- Tailwind Plus Application UI examples as inspiration/source material, subject to licensing and manual review;
- SF5 source mirrors and docs as the target truth.

Not in first scope:

- blindly copying commercial Tailwind Plus examples into distributable SF5 examples without license review;
- pixel-perfect conversion without an explicit design QA pass;
- automatic JS behavior migration from arbitrary Tailwind/headless examples;
- project-specific backend integration.

Suggested first batches:

1. Add `tailwind-converter` specialist and `tailwind-conversion` activity.
2. Build a vendor mapping manifest for common Tailwind -> SF5 class groups.
3. Add fixtures for known layouts: utility card, form row, toolbar, behavior-adjacent negative cases.
4. Add a converter script that accepts HTML and emits SF5 HTML plus a conversion report.
5. Add validation gates: SF5 strict class validation plus unmapped Tailwind report thresholds.
