# SF5 Source Repositories

This file explains which `simai/*` repositories feed the `sf5` skill, what each repository is authoritative for, and how to refresh local source snapshots safely.

## Why This Exists

- Keep `SKILL.md` compact and route-heavy.
- Keep external source ingestion reproducible instead of relying on ad-hoc local folders.
- Make it clear which repository to trust for docs, shipped assets, smart components, and runnable examples.

## Local Layout

- External repositories are synced into the repo-local ignored directory:
  `/Users/rim/Documents/GitHub/ai-codex-skill-sf5/source/simai`
- Source sync configuration lives in:
  `references/vendor/source-repos.json`
- Last sync result is written to:
  `references/vendor/source-repos.lock.json`
- Aggregated source inventory is written to:
  `references/vendor/source-inventory.json` and `references/source-inventory.md`

## Repository Roles

### `simai/ui`

Use as the source of truth for shipped SF runtime assets.

- Local path: `source/simai/ui`
- Trust for:
  - loader runtime paths in `distr/core`
  - shipped component inventory in `distr/component`
  - final asset folder names that templates must target
- Use when:
  - validating whether a component name is actually shipped
  - checking loader-facing asset paths
  - verifying final distribution layout rather than documentation wording

### `simai/ui-doc`

Use as the source of truth for official documentation pages.

- Local path: `source/simai/ui-doc`
- Trust for:
  - `start/loader/*`
  - utility docs taxonomy
  - quickstart/project setup wording
- Use when:
  - building or refreshing `ui-doc-manifest.json`
  - mapping task keywords to docs pages
  - extracting loader/cache semantics into references
- Caveat:
  component and smart-component sections are still sparse; treat them as intent, not full implementation contracts

### `simai/ui-play`

Use as the source of truth for runnable examples and real integration wiring.

- Local path: `source/simai/ui-play`
- Trust for:
  - actual HTML examples under `examples/`
  - host/runner setup
  - how `window.sfPath` and `window.sfSmartPath` are wired in practice
  - deploy expectations for playground-hosted smart assets
- Use when:
  - searching for working markup faster than reading docs
  - checking if a component or smart-component already has a runnable example
  - understanding how a standalone or demo environment boots SF5

### `simai/ui-smart`

Use as the source of truth for available smart runtime artifacts.

- Local path: `source/simai/ui-smart`
- Trust for:
  - smart component names under `smart/*`
  - smart JS/CSS/template folder structure
  - deploy shape for publishing `/smart/`
- Use when:
  - checking whether a smart component actually exists
  - deriving inventory for `smart-codes` or related registries
  - verifying template/js/css co-location conventions

### `simai/ui-utilities`

Use as the source of truth for standalone utility distribution.

- Local path: `source/simai/ui-utilities`
- Trust for:
  - utility bundle files in `distr/full`
  - utility group folder names in `distr/utility/*`
  - utility-only integration paths
- Use when:
  - validating utility group names against shipped folders
  - reasoning about standalone utility delivery

### `simai/ui-vscode`

Use as a secondary tooling source.

- Local path: `source/simai/ui-vscode`
- Trust for:
  - editor-facing metadata generation
  - modifier hinting workflows
- Use when:
  - improving developer ergonomics
  - extracting autocomplete-oriented utility metadata

### `simai/ui-components`

Treat as optional until access is confirmed.

- Local path target: `source/simai/ui-components`
- Current state:
  visible in the organization listing shared by the user, but current sync sees no usable `main` branch and no published heads
- Use when:
  - access is granted later
  - raw component source needs to be reconciled against shipped `simai/ui` distribution

## Trust Order By Question

- "How do I find the right docs page?" -> `ui-doc`
- "What actually ships in the runtime?" -> `ui`
- "How is this used in a working example?" -> `ui-play`
- "Does this smart-component really exist?" -> `ui-smart`
- "Which utility folders/classes are delivered standalone?" -> `ui-utilities`
- "How can we improve editor support?" -> `ui-vscode`

## Refresh Workflow

1. Sync repositories:

```bash
python3 skills/sf5/scripts/sync_source_repos.py
```

2. Rebuild docs atlas from the freshly synced docs repo:

```bash
python3 skills/sf5/scripts/build_ui_doc_atlas.py \
  --docs-root /Users/rim/Documents/GitHub/ai-codex-skill-sf5/source/simai/ui-doc/source/docs/ru \
  --skill-root /Users/rim/Documents/GitHub/ai-codex-skill-sf5/skills/sf5
```

3. Run local checks:

```bash
bash skills/sf5/scripts/run_local_checks.sh
```

Optional but recommended for source-backed discovery:

```bash
python3 skills/sf5/scripts/build_source_inventory.py \
  --repo-root /Users/rim/Documents/GitHub/ai-codex-skill-sf5 \
  --skill-root /Users/rim/Documents/GitHub/ai-codex-skill-sf5/skills/sf5
python3 skills/sf5/scripts/build_component_smart_catalog.py \
  --repo-root /Users/rim/Documents/GitHub/ai-codex-skill-sf5 \
  --skill-root /Users/rim/Documents/GitHub/ai-codex-skill-sf5/skills/sf5
```

## Practical Search Shortcuts

Find a runnable example:

```bash
rg -n "sf-button|sf-code|<smart" source/simai/ui-play/examples
```

List shipped components:

```bash
find source/simai/ui/distr/component -maxdepth 1 -mindepth 1 -type d | sort
```

List shipped smart components:

```bash
find source/simai/ui-smart/smart -maxdepth 1 -mindepth 1 -type d | sort
```

List utility groups from the standalone distribution:

```bash
find source/simai/ui-utilities/distr/utility -maxdepth 1 -mindepth 1 -type d | sort
```
