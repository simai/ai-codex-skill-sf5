---
name: sf5
description: Build, refactor, and maintain SIMAI Framework 5 (SF5) projects with frontend-first workflows for core, loader, utilities, components, smart-components, and blocks. Use when tasks involve SF5 architecture decisions, implementation patterns, code reviews, migration planning, or staged backend planning for Bitrix and Laravel.
metadata:
  display-name: "SIMAI Framework 5"
  short-description: "SF5 workflows, architecture, frontend and component work"
---

# SF5

`sf5` owns frontend-first SF5 architecture, loader, utilities, components,
smart-components, blocks, recipes, working sets and source-backed validation.

Before substantial work load the required kernel and rules:

- [kernel/sf5-dna.md](./kernel/sf5-dna.md);
- [kernel/scope-contract.md](./kernel/scope-contract.md);
- [kernel/output-contract.md](./kernel/output-contract.md);
- [rules/routing.md](./rules/routing.md);
- [rules/decision-policy.md](./rules/decision-policy.md);
- [rules/change-gates.md](./rules/change-gates.md);
- [rules/skill-mesh-balance.md](./rules/skill-mesh-balance.md).

## Mirai Graph Runtime Entry

Use current graph context for capability, route, gates and evidence. Raw SF5
sources remain authoritative; platform playbooks do not move into the central
graph. Graph-only runtime is forbidden.

Load [FULL_RUNTIME_PLAYBOOK.md](./FULL_RUNTIME_PLAYBOOK.md) for the complete
activity/specialist registry, source inventory, recipe/scaffold tools,
Tailwind conversion, Bitrix integration or exhaustive reference routing.

## Core Workflow

1. Define goal, `Done When` and affected SF5 layer.
2. Select an activity from `activities/activity-registry.json`; use
   `scripts/recommend_sf5_activity.py` when unclear.
3. Load only the selected activity, specialist and directly required reference.
4. Separate source refresh, routing, recipes and working-set changes into
   explicit batches.
5. Implement the nearest reversible slice with stated assumptions.
6. Run the selected change gates and source/route/scaffold validation.
7. Run `scripts/run_local_checks.sh` before delivery for repository-wide SF5
   changes.
8. Update source-backed inventories/references only when their inputs changed.

## Layer Boundaries

- Core: contracts and cross-cutting primitives, no feature UI.
- Loader: deterministic idempotent boot and explicit module order.
- Utilities: pure/framework-agnostic helpers without hidden side effects.
- Components: presentation and local interaction.
- Smart-components: state, data and explicit side effects.
- Blocks: composition with explicit input/output and extension contracts.

Preserve backward compatibility unless explicitly waived. `seo`, `ux`, `docs`,
`tester`, `bitrix` and `larena` retain their owner decisions; SF5 implements
them through its own surfaces.

## Fast Reference Routing

- general frontend: `references/frontend.md`;
- execution: `references/execution-workflow.md`;
- patterns/scenarios: `references/pattern-routing.md` and
  `references/product-scenarios.md`;
- recipes: `references/page-recipe-routing.md`;
- loader/components: `references/frontend-loader.md` and
  `references/frontend-components-smart.md`;
- task/working set: `scripts/prepare_sf5_task.py` and
  `scripts/generate_sf5_working_set.py`;
- strict HTML/recipe validation: `scripts/validate_page_recipes.py` and
  `scripts/validate_sf5_html_files.py`.

## Output

Return selected activity/layers, assumptions, changed source-backed artifacts,
validation/gate evidence, compatibility impact, blockers and next action.
