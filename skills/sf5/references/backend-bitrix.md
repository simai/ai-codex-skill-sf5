# SF5 Backend Bitrix Reference

Use this file for backend planning for Bitrix-based SF5 projects.

## Current Status

- Partial guidance extracted from loader backend docs.
- Treat as baseline architecture notes until full backend docs are added.

## Backend Classes Mentioned By Docs

- `Loader` (entrypoint/orchestration)
- `LoaderAsset` (asset manager bridge)
- `AssetManager` (bundle generation, hash, gzip, cache files)
- `TemplateLoader` (smart template processing/caching)
- `LoaderRequest` (request adapter for Bitrix and plain PHP)
- `Constants` (core paths like `SF_MAIN`, `SF_PATH`)

## Runtime Separation

- `init()`:
  initialize environment, config, and base assets.
- `initLoader()`:
  run full asset/template generation flow for frontend requests.

Keep this split in any refactoring to avoid coupling bootstrap and heavy generation paths.

## Frontend <-> Backend Loader Contract

When server mode is active (`standAlone: false`), docs describe request params:

- `a`
- `relations`
- `checkFake`
- `url`
- `load`
- `gzip`

Backend should return generated asset paths, smart fake/template payloads, and bundle/hash metadata.

## Cache And Bundle Notes

- Hash-based files (`bundle-<hash>.js/.css`) are used to avoid repeated regeneration.
- `window.BUNDLE_LOADED` and `window.BUNDLE_ID` are used by frontend to skip unnecessary first-load flow.
- Smart template cache directories and compressed payloads are central to warm-start performance.

## Bitrix Planning Checklist

1. Confirm autoload path and namespace layout for loader classes.
2. Confirm where `init()` is called in template bootstrap.
3. Confirm which routes invoke `initLoader()`.
4. Confirm cache clear path (`loader_clear=Y`) is safe in production.
5. Confirm `LoaderRequest` mapping aligns with Bitrix context/request objects.
6. Confirm frontend loader config (`standAlone`) matches backend availability.

## Current Backend Migration Pattern For Bitrix SF5

For staged migration from SF4 to SF5 on Bitrix, use these conventions as the current default backend pattern.

### Core Backend Module

- Treat `simai.main` as the backend core module for SF5 on Bitrix.
- Do not treat `simai.framework` as the target architecture.
- Use staged coexistence:
  - legacy SF4 stays operational;
  - SF5 backend services are introduced in parallel;
  - read integration and then write integration happen incrementally.

### Settings Model

Current backend baseline for settings in Bitrix SF5:

- settings stored in DB, not file-only config;
- schema/value/history/pending split;
- resolve by `site`, `section`, `page`, `all_users`, `role`, `user`;
- direct and resolved values must both be available;
- explain layers are required for admin UX and debugging.

### Namespace And Key Conventions

Use this canonical naming model:

- `namespace` in lowercase dot notation, for example:
  - `simai.main`
  - `simai.solution.seo`
  - `simai.solution.layout`
  - `simai.sveden`
- `key` in lowercase `snake_case`, for example:
  - `title_browser`
  - `layout_type`
  - `show_title`

Do not encode site identity into namespace.
Use `SITE_ID` for multisite separation.

### Platform vs Solution vs Module

- `simai.main.*` only for platform-level backend concerns.
- `simai.solution.*` for site/solution runtime settings.
- `simai.<module>` for module-owned backend settings.

### First Recommended Migration Stream

For real SF4 -> SF5 migration on Bitrix, start with settings before storage/grid/frontend.

Recommended first batch:

- `simai.solution.seo`
- `simai.solution.layout`
- `simai.solution.organization`

Avoid in the first batch:

- grid settings
- menu settings
- content binding values like `iblock_*_section_code`
- full storage migration
- full frontend migration

### Bridge Strategy

When integrating SF5 into a live SF4 site:

- do not replace the whole legacy property layer at once;
- keep SF4 property assembly as fallback;
- inject resolved SF5 values through a bridge layer in legacy key format;
- start with SEO;
- then move to a safe layout subset;
- only then enable deeper layout switches such as `layout_type` and `sidebar_show`.

### Current Next Stream After First Batch

After `simai.solution.seo`, `simai.solution.layout`, and `simai.solution.organization`, prefer this next settings stream:

1. `simai.solution.assets`
2. `simai.solution.fonts`
3. `simai.solution.editor`

Defer these to later streams:

- `simai.solution.menu`
- `simai.solution.social`
- `simai.solution.widget`
- `simai.sveden`

Reasoning:

- `assets/fonts/editor` behave like clean runtime settings and are easier to migrate incrementally;
- `menu/social/widget` are more coupled to legacy SF4 block/grid composition and third-party embeds;
- `simai.sveden` should be treated as a module-owned stream rather than a generic solution-level continuation.

### Editor Wave Boundary

Do not treat all editor-related SF4 keys as one regular settings namespace.

Current Bitrix pilot evidence shows two distinct categories:

- site-level editor policy:
  - `expert_mode`
  - `iblock_public_editor`
- user-level editor runtime state:
  - `show_bitrix_panel`
  - `edit_mode`
  - `grid_edit_mode`
  - helper payloads like `BLOCK`

Current recommended SF5 split:

- migrate only site-level policy into `simai.solution.editor` first;
- do not put user-level toggles into regular `schema/value/resolve` settings model;
- design a separate user-preferences or runtime-state layer in `simai.main` for editor toggles and authoring payloads.

### Current User Runtime State Layer

Current Bitrix pilot implementation in `simai.main` uses a separate session-backed runtime-state service for:

- `show_bitrix_panel`
- `edit_mode`
- `grid_edit_mode`

Current contract:

- keep this layer outside ordinary settings tables and schema/history/pending model;
- scope runtime values by `SITE_ID` and current user;
- allow fallback to legacy SF4 `$_SESSION['site_property']['user']` values during migration;
- expose runtime state through dedicated facade/controller endpoints;
- use a separate SF4 bridge to inject these values back into legacy property assembly.

Do not merge this layer with editor payload state such as:

- `BLOCK`
- `iblock_section_code`

Those keys need a separate contract as feature/editor session-state, not just runtime toggles.

### Current Editor/Listing Session-State Layer

Current Bitrix pilot implementation in `simai.main` also has a separate editor/listing session-state layer for:

- `BLOCK`
- `iblock_section_code`
- `page_team_view_type`
- `page_struct_view_type`

Current contract:

- keep this layer outside ordinary settings tables and outside simple `Y/N` runtime toggles;
- allow structured payloads for editor-heavy keys such as `BLOCK`;
- scope values by `SITE_ID` and current user;
- allow legacy fallback from SF4 `$_SESSION['site_property']['user']`;
- use a dedicated bridge for staged read integration on live SF4 pages.

Current pilot rollout already includes:

- read integration for `iblock_section_code`, `page_team_view_type`, `page_struct_view_type`;
- legacy write-path sync for `BLOCK` in SF4 block admin scripts;
- legacy write-path sync for `iblock_section_code` in `sf.iblock.section` component epilog;
- read preference for bridge-backed `BLOCK` in legacy block config entry point.

Recommended rule:

- `show_bitrix_panel`, `edit_mode`, `grid_edit_mode` -> user runtime state
- `BLOCK`, `iblock_section_code`, `page_team_view_type`, `page_struct_view_type` -> editor/listing session-state

### Backend Delivery Rule

For Bitrix SF5 backend work:

- prefer reversible changes;
- prefer pilot rollout on a real site;
- preserve explainability and audit trail;
- do not collapse migration planning into a single big-bang rewrite.
