# SF5 DNA

SF5 is a frontend-first implementation skill with source-backed validation and deterministic delivery.

Core invariants:

- Start from the narrowest useful SF5 layer: `core`, `loader`, `utilities`, `components`, `smart-components`, `blocks`.
- Treat synced upstream `source/simai/*` repositories and vendor manifests as authoritative whenever current SF5 behavior matters.
- Keep recipes, playbooks, routing, working sets, and validation aligned with real shipped runtime and examples.
- Prefer small reversible updates to the skill over broad undocumented restructuring.
- Preserve backward compatibility in the skill unless the task explicitly allows a contract break.
- Do not bloat `SKILL.md`; move detail to the narrowest rule, specialist, activity, or reference file.
