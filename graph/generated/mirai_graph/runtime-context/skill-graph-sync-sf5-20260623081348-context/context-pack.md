# Mirai Graph Runtime Context: sf5

- Task: `Blade adapter template boundary rule`
- Objects: 9
- Relations: 20
- Canonical writes: false

## Included Objects

- `policy.sf5.frontend-first-boundary` (0.33): Keep SF5 frontend-first scope explicit and escalate staged backend work to the owning platform skill.
- `skill.sf5.core` (0.15): Owns SIMAI Framework 5 frontend-first workflows: loader, utilities, components, smart-components, recipes and staged backend planning.
- `policy.sf5.validation-hardening` (0.15): Component/recipe changes need validation hardening, working-set coverage and release gate evidence.
- `gate.sf5.release-readiness` (0.15): Blocks completion until component/loader changes have working-set, validation and release-gate evidence.
- `capability.sf5.frontend-components` (0.0): Implement SF5 frontend components, blocks, utilities, modifiers and component recipes.
- `capability.sf5.loader-runtime` (0.0): Handle frontend loader, smart runtime, backend-first integration and project conventions.
- `capability.sf5.smart-components` (0.0): Design and validate smart components, catalog entries, templates and smart hints.
- `capability.sf5.page-recipes` (0.0): Route work to page recipes and scenario playbooks for landing, dashboard, catalog, auth, checkout and profile flows.
- `capability.sf5.tailwind-conversion` (0.0): Convert Tailwind/UI source into SF5 components with working-set coverage and validation hardening.

## Raw Source Refs

- `skills/sf5/SKILL.md`
- `skills/sf5/kernel/scope-contract.md`
- `skills/sf5/rules/routing.md`
- `skills/sf5/activities/validation-hardening.json`
- `skills/sf5/knowledge-packs/validation-hardening.md`
- `skills/sf5/rules/change-gates.md`
- `skills/sf5/references/frontend-components-smart.md`
- `skills/sf5/references/frontend-playbook.md`
- `skills/sf5/references/frontend-loader.md`
- `skills/sf5/knowledge-packs/backend-first-smart-runtime.md`
- `skills/sf5/references/component-smart-catalog.md`
- `skills/sf5/references/smart-component-template.md`
- `skills/sf5/references/page-recipes-index.md`
- `skills/sf5/references/scenario-dashboard-workspace.md`
- `skills/sf5/activities/tailwind-conversion.json`
- `skills/sf5/knowledge-packs/tailwind-to-sf5-conversion.md`

## Runtime Boundary

Graph context is routing/capability orientation only. Raw skill files remain authoritative.
