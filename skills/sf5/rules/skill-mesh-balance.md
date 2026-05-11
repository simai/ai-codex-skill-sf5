# Skill Mesh Balance

`$sf5` owns SIMAI Framework 5 frontend-first contracts: core, loader,
utilities, components, smart-components, blocks, source refresh, recipe
scaffolds, working-set generation, validation surfaces, and SF5 implementation
patterns for Bitrix/Laravel alignment.

## Does Not Own

- Larena platform/package lifecycle owned by `$larena`.
- Bitrix/SF4/OrgPortal facts owned by their domain skills.
- General repository delivery owned by `$dev`.
- Documentation methodology/content owned by `$docs`.
- UX design decisions owned by `$ux`.
- SEO Contract decisions owned by `$seo`.
- QA evidence owned by `$tester`.
- Runtime/deploy incidents owned by `$ops`.

## Companion Contracts

- Use `$larena` when SF5 work touches Larena packages, admin, installer/update,
  or registration flows.
- Use `$bitrix`, `$sf4`, or `$orgportal` when SF5 contracts must align with
  those platforms.
- Use `$ux` and `$seo` as contract owners for interface and public/search
  surfaces.
- Use `$docs` for substantial documentation and `$tester` for validation
  evidence.
- For SF4 -> SF5, Bitrix -> SF5, Larena/SF5, or other reference-adaptive work,
  `$sf5` owns target frontend adaptation: loader/runtime, components,
  smart-components, blocks, layout contracts, utilities, recipes, and generated
  working-set artifacts. `$tester` owns invariant evidence and verdict; source
  platform skills own the reference behavior.

## Handoff

Return SF5 layers/surfaces touched, source/recipe/working-set paths, generated
artifacts, validation commands, compatibility constraints, blockers, and the
companion owner expected to review.

For reference-adaptive handoff, also return target behavior, allowed SF5
adaptations, source/recipe mapping, already-working baseline, do-not-break list,
and regression checks after fix.
