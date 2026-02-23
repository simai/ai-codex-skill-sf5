# SF5 Loader Reference

This file captures practical loader rules from the SF UI docs snapshot.

## Contents

- Core Loader Responsibilities
- Plugin Discovery
- Dependency Ordering
- Dynamic Asset Loading
- Client Cache Model
- Cache Invalidation
- Preloader Behavior
- Standalone Mode
- Loader API Surface
- Server Mode Contract (When `standAlone: false`)
- Loader Debug Checklist

## Core Loader Responsibilities

- Discover required plugins in DOM.
- Resolve plugin dependencies before component initialization.
- Dynamically load JS/CSS assets (local paths or CDN URLs).
- Cache plugin/template data for repeated page loads.
- Support smart-component templates and runtime rendering.

## Plugin Discovery

- Primary marker: `sf-asset` attribute.
- Optional regex discovery: `findPlugins` config map.
- Runtime updates: `MutationObserver` rescans added/changed DOM.

Recommended pattern:

```js
new SFLoaderPlugin({
  attr: "sf-asset",
  findPlugins: {
    slider: { regex: /sf-slider/, type: "component" },
  },
});
```

## Dependency Ordering

- Configure dependency graph via `relations`.
- Load dependencies before dependent plugin.
- Prevent duplicate loads for repeated plugin usage.

Example:

```json
{
  "relations": {
    "tooltip": ["jquery", "wow"]
  }
}
```

## Dynamic Asset Loading

- Loader inserts `<script>` and `<link>` tags at runtime.
- Support both CDN and local asset paths.
- Keep async loading but enforce dependency order before init.

## Client Cache Model

- `SF_PLUGIN_LIST-<pageHash>`: loaded plugin set.
- `SF_SMART_LIST-<pageHash>`: smart templates.
- `SF_MISSING_PLUGINS`: known-missing assets.
- `pageHash`: doc examples describe `md5(pathname).slice(0, 16)`.
- Payloads may be compressed via `LZString.compressToUTF16`.

## Cache Invalidation

- URL switch: `?loader_clear=Y`.
- Runtime API: `SF.Loader.clearCache()`.
- Manual cleanup via browser storage if needed.

## Preloader Behavior

- Intended for first load without warm cache.
- Typical flow: hide body (`opacity: 0`) -> show loader -> restore UI when assets are ready.
- Disable when needed via config (`preloader: false`) for special contexts.

## Standalone Mode

- `standAlone: true`: skip backend assembly endpoint and use direct asset paths.
- `standAlone: false`: use server assembly flow (`/simai/loader/loader.php`).
- Docs indicate standalone is default in current project snapshot; verify per target project.

## Loader API Surface

Common methods (`window.SF.Loader`):

- `prepare(observer?)`
- `clearCache()`
- `checkTheme(body?)`
- `changeTheme()`
- `findShortCodes(node)`
- `checkToCacheClean()`

Common events:

- `sf-loader-init`
- `sf-loader-ready`
- `sf-shortcodes-ready`

Event handlers must be idempotent because ready events can arrive from multiple branches.

## Server Mode Contract (When `standAlone: false`)

Typical request params:

- `a`: requested plugin list
- `relations`: dependency map
- `checkFake`: smart fake-template flag
- `url`: current URL for hash generation
- `load`: prior backend call marker
- `gzip`: gzip support marker

Typical backend classes mentioned by docs:

- `Loader`
- `LoaderAsset`
- `AssetManager`
- `TemplateLoader`
- `LoaderRequest`
- `Constants`

## Loader Debug Checklist

1. Check plugin markers in DOM (`sf-asset`, regex targets).
2. Check dependency graph for cycles/missing items.
3. Check network requests (or standalone path resolution).
4. Check localStorage keys (`SF_PLUGIN_LIST-*`, `SF_SMART_LIST-*`, `SF_MISSING_PLUGINS`).
5. Run with `loader_clear=Y` to separate cache bugs from runtime bugs.
6. Check emitted events to verify lifecycle order.
