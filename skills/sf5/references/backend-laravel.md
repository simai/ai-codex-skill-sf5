# SF5 Backend Laravel Reference

Use this file for Laravel variant planning. The current docs snapshot is Bitrix/PHP loader-oriented, so this file maps required behavior to Laravel targets.

## Current Status

- No dedicated Laravel docs in the reviewed snapshot.
- Behavior requirements are inferred from frontend loader contract and backend architecture descriptions.

## Behavior To Preserve In Laravel Variant

- Endpoint that can assemble and return component asset paths.
- Dependency-aware ordering for requested plugin list.
- Smart template generation/cache and fake-template response branch.
- Hash-based bundle identity equivalent to `pageHash`/`BUNDLE_ID`.
- Cache invalidation path compatible with frontend (`loader_clear` semantics or equivalent).

## Suggested Laravel Architecture Mapping

- Request adapter: service class similar to `LoaderRequest`.
- Asset orchestration: service pair similar to `LoaderAsset` + `AssetManager`.
- Template orchestration: service similar to `TemplateLoader`.
- Entry routes:
  - bootstrap route (equivalent of `init()`)
  - generation route (equivalent of `initLoader()`)

## Contract Checklist

1. Keep request params compatible with frontend loader config.
2. Keep output schema stable (asset paths, smart templates, hash metadata).
3. Keep bundle/hash generation deterministic.
4. Keep cache storage strategy explicit (filesystem/redis) and test warm/cold starts.
5. Keep failure mode observable (missing plugin, missing template, invalid dependency).
