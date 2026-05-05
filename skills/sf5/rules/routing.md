# Routing

The coordinator chooses the smallest sufficient activity and specialist set.

Activity selection:

- upstream refresh, mirrors, inventory rebuild, example drift -> `source-refresh`
- route ranking, scenario rules, recipe routing, fixtures -> `routing-maintenance`
- page/component/block scaffold changes -> `recipe-scaffold-maintenance`
- working-set sections, upstream extracts, bundle contract -> `working-set-maintenance`
- Tailwind CSS, Tailwind UI, Tailwind Plus, or class conversion to SF5 -> `tailwind-conversion`
- validators, strict checks, fixtures, local check suite -> `validation-hardening`
- references, maps, docs indexes, usage guides -> `documentation-update`
- SKILL architecture, metadata, coordinator model, specialist system -> `skill-architecture-update`

If the mapping is not obvious, use `scripts/recommend_sf5_activity.py` first and then narrow the specialist set.

Specialist selection:

- Always include `task-goal` for substantial autonomous work.
- Include `skill-maintainer` when changing skill structure, metadata, install surface, or council architecture.
- Include `source-sync` when touching `source/simai`, `source-inventory`, source repos, or upstream-derived contracts.
- Include `routing-orchestrator` when changing scenario/recipe/playbook routing or fixtures.
- Include `recipe-scaffold` for recipe, scaffold, and template work.
- Include `working-set` for section variants, upstream extracts, and bundle generation.
- Include `tailwind-converter` for Tailwind CSS to SF5 conversion, Tailwind UI source analysis, and conversion reports.
- Include `validation-qa` when validators, regression fixtures, or user-facing generated artifacts are touched.
- Include `docs-learning` when references, README, or learning surfaces are part of the result.

Default bias:

- simple source refresh: `source-sync` + light `validation-qa`
- routing change: `routing-orchestrator` + `validation-qa`
- recipe or working-set change: `recipe-scaffold` or `working-set` + `validation-qa`
- Tailwind CSS conversion: `tailwind-converter` + `validation-qa`, optionally `recipe-scaffold` or `working-set`
- architecture refactor: `skill-maintainer` + `task-goal` + `validation-qa` + `docs-learning`
