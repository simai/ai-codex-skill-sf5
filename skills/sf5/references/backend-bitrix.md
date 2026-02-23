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
