# SF5 Project Conventions

Source snapshot:
`/Users/rim/Downloads/ui-doc-main (2)/ui-doc-main/source/docs/ru`

This file contains conventions extracted from the snapshot. If a rule is absent in snapshot docs, it is marked explicitly.

## Contents

- Repository Layout
- Naming Rules
- Loader Defaults
- Utilities And Styling Rules
- Component Contracts
- Testing And Verification
- Compatibility And Releases
- Integration Notes

## 1. Repository Layout

- Framework root URL/path:
  `/simai`
- Loader endpoint:
  `/simai/loader/loader.php`
- Loader backend source namespace/path:
  `SIMAI\Main\Loader\*` in `/simai/loader/src`
- Composer roots:
  `/simai/composer.json`, `/simai/vendor/autoload.php`
- Component asset path pattern:
  `/simai/asset/simai.framework/sf5.master/component/<name>/js/<name>.js`
  `/simai/asset/simai.framework/sf5.master/component/<name>/css/<name>.css`
- Smart-component asset path pattern:
  `/simai/asset/simai.framework/sf5.master/smart/<name>/js/<name>.js`
  `/simai/asset/simai.framework/sf5.master/smart/<name>/css/<name>.css`
- Bundle cache path:
  `/simai/cache/loader/bundle-<hash>.js|css`
- Smart cache path:
  `/simai/cache/smart/<pageHash>/`
- Template cache files:
  `/simai/cache/templates.txt`, `/simai/cache/fake.txt`
- Layer folder layout for `core/utilities/components/smart-components/blocks` is not documented explicitly in snapshot docs.

## 2. Naming Rules

- Utility syntax:
  `{condition}:{modifier}` or `{modifier}` without condition.
- Breakpoint prefixes:
  `sm`, `md`, `lg`, `xl`, `xxl`.
- State prefixes:
  `hover`, `focus`, `active`.
- Plugin discovery attribute default:
  `sf-asset` (overridable through `attr`).
- Plugin/component name convention in runtime:
  token from `sf-asset` value used as asset key/path segment (example: `tooltip`, `modal`).
- Smart-component markup contract:
  `<smart name="..." data="..." property="..." events="..." modify="..." />`
- Global CSS variable naming:
  `--sf-{value}` (example: `--sf-breakpoint-lg`).
- Local CSS variable naming:
  `--sf-{property}--{value}` (example: `--sf-font-size--heading`).
- Event naming documented for loader:
  `sf-loader-init`, `sf-loader-ready`, `sf-shortcodes-ready`.

## 3. Loader Defaults

- Default mode in current documented config:
  `standAlone: true`.
- Discovery attribute default:
  `sf-asset`.
- Additional discovery mode:
  `findPlugins` regex map.
- Dependency graph config:
  `relations` object passed to loader request/runtime config.
- Cache clear strategy:
  `?loader_clear=Y` and `SF.Loader.clearCache()`.
- Client cache keys:
  `SF_PLUGIN_LIST-<pageHash>`, `SF_SMART_LIST-<pageHash>`, `SF_MISSING_PLUGINS`.
- Loader boot recommendation:
  initialize in `<head>` to reduce FOUC and apply theme earlier.

## 4. Utilities And Styling Rules

- Breakpoint source of truth:
  `fundamentals/break-points/*` (`sm 576`, `md 768`, `lg 960`, `xl 1152`, `xxl 1536`) via `--sf-breakpoint-*`.
- Breakpoint inconsistency note:
  some utility pages show other numbers; prefer `break-points` and actual project CSS variables.
- Theme classes:
  `.theme-light`, `.theme-dark`.
- Loader theme control:
  can disable automatic theme assignment via `SF_BOOT_CONFIG.theme = false`.
- Color model:
  primitives -> tokens -> roles (`surface`, `primary`, `secondary`, `tertiary`, status roles, and `on-*` roles).
- Version note:
  migration page for `5.4.0` mentions status-role changes (`success/warning` removal and `code` role introduction). Validate target version before color-role refactors.
- RTL/LTR rule:
  keep logical properties and avoid hardcoded `left/right` custom styles when utility equivalents exist.
- Spacing rule:
  prefer token-driven utilities (`--sf-space-*`) over arbitrary literals.

## 5. Component Contracts

- Regular components:
  treat as presentational units loaded by loader/plugin mechanism.
- Smart-component required identifiers:
  `name` attribute and optional serialized attributes `data/property/events/modify`.
- Smart templates:
  cache by `pageHash` and loader template stores; use hash-based cache identity.
- Loader events payloads (documented):
  `sf-loader-init` detail `{ loader, timestamp }`,
  `sf-loader-ready` detail `{ message, timestamp }`,
  `sf-shortcodes-ready` detail `{ loader, timestamp }`.
- Event handlers must be idempotent because ready events may be emitted from multiple branches.

## 6. Testing And Verification

- Required command set is not documented in snapshot (no canonical npm/phpunit/lint command list in provided docs).
- Required manual checks from docs behavior:
  1. cold load (empty cache) and warm load (cached),
  2. `loader_clear=Y` cache invalidation path,
  3. standalone path (`standAlone: true`) versus backend path (`standAlone: false`) where applicable,
  4. dependency ordering via `relations`,
  5. smart-template cache restore from localStorage,
  6. loader events emission and idempotent handling.
- Required browser matrix is not documented in snapshot.

## 7. Compatibility And Releases

- Backward compatibility policy is not explicitly formalized in snapshot docs.
- Practical compatibility requirement from loader architecture:
  preserve cache key semantics, bundle hash behavior, and loader request/response contract.
- Migration signal available:
  `migration/change-history.md` documents `5.4.0` color/shadow/radius changes; treat this page as required pre-release diff check.
- Release gate recommended by docs behavior:
  verify cache clear + rebuild path after contract/asset changes.

## 8. Integration Notes

- Bitrix-specific notes in snapshot:
  backend runtime branches on `class_exists('\\Bitrix\\Main\\Application')` and uses Bitrix context/request when present.
- Non-Bitrix PHP mode is documented through `LoaderRequest` adapter and manual request hydration.
- Laravel-specific SF5 backend conventions are not documented in this snapshot; keep Laravel rules in `backend-laravel.md` as mapped behavior targets.
