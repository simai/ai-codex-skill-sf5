# SF5 DNA

SF5 is a frontend-first implementation skill with source-backed validation and deterministic delivery.

Core invariants:

- Start from the narrowest useful SF5 layer: `core`, `loader`, `utilities`, `components`, `smart-components`, `blocks`.
- Treat raw HTML as render output, legacy input, or explicit exception only; SF5 source of truth should be structured content, page/section/block manifests, data bindings, design packs, smart contracts, and adapter render output.
- Keep `simai.storage`, settings, and `simai.property` in separate planes: storage owns content and site/page structure; settings own contextual characteristics and preferences; `simai.property` owns field rendering/editing and may render through SF5 smart/components.
- Model pages as ordered section calls, not copied section internals. Section definitions live in `/simai/section` and `/simai.data/section`; page calls reference `section`, `version`, `view`, and `params`.
- Model blocks as physical reusable units in `/simai/block` and `/simai.data/block`. A section definition composes blocks and maps section params to block params through bindings.
- Allow path-scoped `simai.data` overlays such as `/company/simai.data` for local section/block/design libraries. Resolve overlays from root to current route, keep deeper scopes higher priority, and include the overlay chain in compiled cache keys.
- Treat platform cache as a backend, not the SF5 cache contract. SF5 runtime should use compiled registry/page/section/block plans with explicit cache keys, tags, dependencies, invalidation, and warmup.
- For property templates or backend-generated controls, prefer this order: SF5 smart-component, SF5 component, SF5 utilities, custom layer only as an explicit framework gap.
- Treat synced upstream `source/simai/*` repositories and vendor manifests as authoritative whenever current SF5 behavior matters.
- Keep recipes, playbooks, routing, working sets, and validation aligned with real shipped runtime and examples.
- Prefer small reversible updates to the skill over broad undocumented restructuring.
- Preserve backward compatibility in the skill unless the task explicitly allows a contract break.
- Do not bloat `SKILL.md`; move detail to the narrowest rule, specialist, activity, or reference file.
