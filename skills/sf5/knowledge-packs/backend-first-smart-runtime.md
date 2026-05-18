# Backend-First Smart Runtime

Use this knowledge pack when implementing or reviewing SF5 backend Smart API,
smart manifests, smart templates, composite smart components, or smart runtime
proofs.

## Rule

SF5 Smart is backend-first, but the frontend smart package remains the
hydration/behavior layer.

Do not duplicate frontend behavior in PHP. Backend Smart must produce:

```text
stable HTML
asset graph
hydration metadata
cache metadata
```

Frontend runtime owns:

```text
interaction
focus and keyboard behavior
opened/closed state
async client state
DOM hydration
```

Every backend-first Smart manifest should declare its hydration strategy. Do
not treat backend HTML as permission to bypass frontend rerender/adopt logic.

Supported strategy vocabulary:

```text
server-static
server-first-hydratable
client-owned
shadow-dom-owned
```

Use `server-first-hydratable` only when the frontend runtime can adopt existing
DOM without destroying it on first connection. Use `client-owned` when the
frontend smart component must fully own the internal DOM and rerender from host
attributes/props. Use `shadow-dom-owned` only when DOM/style isolation is a real
requirement, not as the default answer.

The manifest render contract can carry:

```json
{
  "mode": "server-first",
  "strategy": "server-first-hydratable",
  "hydration": "required",
  "domStrategy": "light-dom-adopt",
  "updateStrategy": "patch",
  "initialHtml": "complete",
  "frontendOwnership": "behavior"
}
```

## PHP Facade Pattern

Use `Simai\Main\UI\Smart` as the current backend facade:

```php
Smart::render('button', [
    'view' => 'primary-large',
    'props' => [
        'text' => 'Сохранить',
    ],
]);

Smart::tree($smartTree, [
    'artifactRoots' => [
        $_SERVER['DOCUMENT_ROOT'] . '/simai.data/smart',
        $_SERVER['DOCUMENT_ROOT'] . '/simai/smart',
    ],
]);
```

`Smart::render()` returns HTML. `Smart::tree()` returns a render-result with:

```text
html
assets.smart / assets.depends / assets.css / assets.js
hydration.nodes
cache.key / cache.tags
resolvedArtifacts
```

## Artifact Roots

The neutral runtime accepts explicit `artifactRoots`. Platform adapters should
build these roots from the platform context. The core Smart facade should not
read storage, settings, site structure, or page state directly.

Supported artifact layout:

```text
<root>/<smart>/manifest.json|php
<root>/<smart>/preset/<code>.json|php
<root>/<smart>/view/<code>.json|php
<root>/<smart>/template/<code>.php
```

Props merge order:

```text
preset props -> view props -> call props
```

If a template is found, it receives normalized context only:

```text
id
smart
manifest
view
preset
props
childrenHtml
slot
```

If a template is not found, fall back to the registry-backed custom element
renderer.

## Verification

For bx-simai.main, use:

```bash
php docs/developer/specifications/tools/proof_smart_runtime_api.php
```

This proof checks:

- registry-backed `Smart::render()`;
- nested `Smart::tree()`;
- manifest-backed `artifactRoots`;
- view props merge;
- template rendering;
- manifest asset collection;
- hydration/cache metadata;
- unknown smart and invalid compatibility guards.

For hydration strategy checks, use:

```bash
php docs/developer/specifications/tools/proof_smart_hydration_strategy.php
```

This proof checks that `server-static`, `server-first-hydratable`,
`client-owned`, and `shadow-dom-owned` manifest contracts are propagated into
`hydration.nodes` without duplicating frontend behavior in PHP.

For Smart Atlas generation, use:

```bash
python3 docs/developer/specifications/tools/build_smart_atlas.py --format markdown
```

The builder reads the source-backed frontend smart registry, creates Atlas
entries for every current smart component, validates each entry against
`smart.atlas.schema.json`, and can emit JSON for future compiled atlas/runtime
work.

For backend smart analog coverage and frontend sync checks, use:

```bash
python3 docs/developer/specifications/tools/build_backend_smart_coverage.py --format markdown
```

The coverage tool is read-only. It reads the frontend smart registry, classifies
each smart as recommended backend `native`, `host`, or `skeleton`, calculates
frontend source hashes, inspects backend smart roots for artifacts, and
validates generated `smart.sync` entries against `smart.sync.schema.json`.

Use this before creating backend templates. Do not generate or overwrite
production PHP templates directly from minified frontend source; update
metadata/draft reports automatically and require review for templates.

For the first backend-native system artifacts proof in `bx-simai.main`, use:

```bash
php docs/developer/specifications/tools/proof_backend_native_smart_artifacts.php
```

The first safe batch is limited to `server-static` smart artifacts:

```text
badge
icon
progress-bar
progress-scale
skeleton
spinner
```

Each artifact must have a manifest-backed template under system `/simai/smart`,
pass `validate_smart_artifacts.py`, and appear as `aligned` in
`build_backend_smart_coverage.py`. Do not include `client-owned` or complex
`host` smart in this batch class without a separate hydration/behavior proof.

For the second backend hydratable system artifacts proof in `bx-simai.main`,
use:

```bash
php docs/developer/specifications/tools/proof_backend_hydratable_smart_artifacts.php
```

This batch covers `server-first-hydratable` native smart:

```text
button
alert
avatar
avatars
close
download-file
icon-button
list-item
reference-link
tag
```

These templates may render complete initial HTML, but their manifests must keep
`domStrategy=light-dom-adopt` and `frontendOwnership=behavior`. Do not move
forms, overlays, async media, or other `client-owned` smart into this class
without a separate host/skeleton proof.

For the third backend host/skeleton artifacts proof in `bx-simai.main`, use:

```bash
php docs/developer/specifications/tools/proof_backend_host_skeleton_smart_artifacts.php
```

This batch covers the remaining frontend smart registry entries without
pretending they are backend-native:

```text
checkbox, context-menu, country-code, dropdown, file-upload, input, modal,
pagination, radio, range-slider, steps, switch, textarea, toast, toggle,
tooltip, gallery, slider
```

Host smart must use `strategy=client-owned`, `domStrategy=host-attributes`,
`initialHtml=host-only`, and `frontendOwnership=dom`. Media-heavy fallback smart
such as `gallery` and `slider` use the same ownership model with
`initialHtml=skeleton`. PHP may render a useful fallback, but must not duplicate
the frontend state machine, portals, focus/open behavior, async media behavior,
or overlay orchestration.

For smart artifact folders, use:

```bash
python3 docs/developer/specifications/tools/validate_smart_artifacts.py --format markdown
```

This validator checks `manifest`, `view`, and `preset` artifacts against the
current schemas and runs `php -l` for `template.php` or `template/*.php`. It is a
folder-level gate only; it must not read storage, page structure, settings, or
platform runtime state.

For platform route to Smart roots resolution, use:

```php
use Simai\Main\Runtime\SmartArtifactRootResolver;

$resolver = new SmartArtifactRootResolver($_SERVER['DOCUMENT_ROOT']);
$options = $resolver->renderOptionsForRoute('/company/news/article/');
```

The resolver feeds `artifactRoots` into `Smart::render()` or `Smart::tree()` in
this order:

```text
nearest path-scoped simai.data/smart
parent path overlays
site simai.data/smart
system simai/smart
```

Verify with:

```bash
php docs/developer/specifications/tools/proof_smart_platform_resolver.php
```

For compiled Smart metadata cache, use:

```php
use Simai\Main\Runtime\SmartRuntimeCache;

$cache = new SmartRuntimeCache('/path/to/cache/smart-runtime');
$roots = $cache->smartRootsForRoute($resolver, '/company/news/article/');
```

The cache is source-signature based. It can cache compiled Atlas payloads from
the frontend registry file and route-specific `artifactRoots` from Smart root
candidates. It is not a platform cache backend; Bitrix and Larena adapters may
wrap it later.

Verify with:

```bash
php docs/developer/specifications/tools/proof_smart_runtime_cache.php
```
