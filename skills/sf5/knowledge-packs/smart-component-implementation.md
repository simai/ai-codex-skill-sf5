# Smart Component Implementation

Use this knowledge pack when creating, syncing, or reviewing SF5 smart
components across backend Smart artifacts and the frontend `ui-smart` package.
It is especially relevant for overlay/navigation primitives such as `drawer`,
`modal`, `sidebar`, `side-menu`, and navigation shells.

## Core Rule

Treat Smart as one backend-first component contract with optional frontend
hydration, not as two unrelated systems.

Backend Smart owns:

```text
initial HTML
normalized props
template/view/preset resolution
asset and hydration metadata
cache boundaries
server-side composition
```

Frontend Smart owns:

```text
interactive state
keyboard and focus behavior
DOM adoption or rerendering
portals and overlay runtime
client-only async behavior
```

Do not duplicate a frontend state machine in PHP. If the frontend component
needs to own its internal DOM, the backend artifact should render a host or
skeleton and declare `client-owned`. If the frontend can adopt existing light
DOM, use `server-first-hydratable`.

## Component Taxonomy

Use precise names. Do not merge layout, navigation content, and overlay
behavior into one component.

```text
modal
  Blocking dialog surface. Owns dialog semantics, overlay, focus trap,
  Escape behavior, portal root, stack, and rich modal states.

drawer
  Temporary off-canvas surface. Owns placement, overlay, close behavior,
  scroll lock, portal root, and stack. It is not a sidebar.

sidebar
  Persistent layout area. It should not own temporary overlay behavior.

side-menu
  Navigation content for vertical navigation. It can be rendered inside a
  sidebar or a drawer, but it should not open or close the drawer itself.

top-menu
  Horizontal navigation content. It can be used inside a header or collapsed
  into a drawer on narrow screens.

navigation-shell
  Composite smart component that decides how to combine top menu, side menu,
  sidebar, drawer, logo, theme switch, and responsive layout.
```

When the task is mobile navigation, the usual model is:

```text
desktop: navigation-shell -> sidebar + side-menu
mobile:  navigation-shell -> drawer + side-menu
```

## Backend Artifact Rules

System smart artifacts belong under `/simai/smart`. Local overrides,
site-specific templates, presets, views, and composite smart artifacts belong
under `/simai.data/smart`.

The neutral runtime should accept explicit artifact roots:

```php
Smart::tree($tree, [
    'artifactRoots' => [
        $_SERVER['DOCUMENT_ROOT'] . '/simai.data/smart',
        $_SERVER['DOCUMENT_ROOT'] . '/simai/smart',
    ],
]);
```

Platform adapters may discover the roots, but the Smart core should receive
them as context and should not read page structure, settings, or storage
directly.

Backend templates should:

- emit stable, semantic, accessible HTML;
- reuse existing SF5 classes and modifier names;
- expose `data-*` hooks that the frontend runtime can adopt;
- keep JS behavior out of PHP;
- declare required assets and hydration strategy in the manifest;
- support nesting through slots or children, including composite inside
  composite.

## Frontend Package Workflow

The frontend smart repository can be a static distribution repository. Do not
assume a build pipeline exists unless it is present in the repo.

For `ui-smart` static components:

1. Create a feature branch from `origin/main`.
2. Add the component under:

```text
smart/<code>/js/<code>.js
smart/<code>/js/<code>.js.gz
```

3. Keep the component self-contained unless the repo has an explicit shared
runtime package for the behavior.
4. Update the component list in `README.md`.
5. Add a short `CHANGELOG.md` entry.
6. Validate syntax and gzip:

```bash
node --check smart/<code>/js/<code>.js
gzip -t smart/<code>/js/<code>.js.gz
```

7. Run a browser smoke that creates the element, exercises the public API, and
checks the expected DOM state.
8. Commit, push, and open a PR with behavior, API, and validation notes.

If the repo ships compressed artifacts, generate them from the checked source:

```bash
gzip -c -9 smart/<code>/js/<code>.js > smart/<code>/js/<code>.js.gz
```

## Browser-Side Smart Contract

Modern frontend smart components must use `SfBaseElement` as the shared base.
Do not create a standalone `HTMLElement` implementation unless the component is
intentionally legacy or the repository owner explicitly asks for that exception.

`SfBaseElement` extends native `HTMLElement`; smart components use Lit as the
render engine inside light DOM, but they do not extend `LitElement`.

A compliant smart bundle should:

- define a class that extends `SfBaseElement` or the local bundled base alias;
- declare public inputs through `static get props()`;
- use `template()` and `templateContext()` or `createTemplateContext()`;
- call `define()` to register the custom element;
- export the base globals when bundling the base into the component:

```text
SF.SfBaseElement
SF.html
SF.nothing
SF.render
SF.smart.SfBaseElement
SF.smart.html
SF.smart.nothing
SF.smart.render
SF.smart.toBoolean
SF.smart.toAttributeName
SF.smart.toNumber
SF.smart.normalizeEnum
SF.smart.parseJsonAttribute
```

`static props` is the source of truth for observed attributes, default values,
type coercion, enum values, and external template context. Prefer props over
manual `observedAttributes`.

Use the extended prop form when needed:

```js
static get props() {
  return {
    templateName: { attribute: 'template', default: 'default' },
    placement: { default: 'right', values: ['left', 'right'] },
    overlay: { type: Boolean, default: true },
  };
}
```

`setState()` in `SfBaseElement` is attribute-state. It writes normalized keys
back to attributes and schedules render. If a component owns coupled state such
as `open`, `checked`, `value`, or `selectedIndex`, override `setState()` and
sync that state explicitly before delegating the rest to `super.setState()`.

External project templates are part of the public contract:

```text
/local/smart/templates/<component>/<template>/index.js
/local/smart/templates/<component>/<template>/index.css
```

The external template receives `html`, `nothing`, `context`, `component`, and
`changedAttributes`. Framework-bundled component CSS should still be shipped as
an explicit component asset; do not rely on arbitrary template JS to import CSS
unless the project bundler owns that path.

Use the base slot helpers for component content:

```js
this.getSlotContent('content')
this.setSlot('content', node)
this.clearSlot('content')
```

Declarative slot markup is cloned on render. Do not attach runtime-only
listeners to declarative slot template nodes; use `setSlot()` for live nodes
with event handlers or component references.

Components that register global listeners, observers, timers, portal nodes, or
outside-click handlers must release them from `disconnectedCallback()` or a
component-specific teardown method.

## Overlay Primitive Checklist

For drawer-like and modal-like frontend smart components, verify the following
before considering the component reusable:

- `open()`, `close()`, `toggle()`, `setState()`, and `getState()` or an
  equivalent stable public API;
- declarative triggers such as `data-sf-drawer-open`,
  `data-sf-drawer-close`, and `data-sf-drawer-toggle` when useful;
- lifecycle events for ready, update, before open, after open, before close,
  and after close;
- Escape handling;
- overlay click handling when enabled;
- scroll lock with scrollbar gap preservation;
- portal to `document.body` so parent containers cannot clip the overlay;
- z-index stack behavior for multiple opened surfaces;
- focus restore after close;
- accessible labels, title handling, and close labels;
- left/right or other supported placement modes;
- class passthrough for host, panel, overlay, header, body, and close button;
- no hidden dependency on demo-only markup.

The overlay/backdrop can be internal. Create a separate backdrop component only
when there is a real shared runtime contract that multiple smart components can
use without duplicating state ownership.

For close controls, prefer the existing `sf-close` visual pattern inside an
`sf-icon-button`-style button instead of inventing a new close icon API.

For a `drawer`-style component, also verify that the bundle does not
accidentally register or carry template code for unrelated smart components and
that `SF.smart.*` globals are available after the bundle is loaded.

## Backend and Frontend Sync

When a frontend smart has a backend analog, keep their public names aligned:

```text
placement
open
overlay
closeOnEsc
closeOnOverlay
closeLabel
title
width
zIndex
```

Use backend manifests to record the relationship:

```text
backend smart code
frontend smart code
hydration strategy
frontend source hash or version
asset dependencies
compatibility constraints
```

The source hash is a drift signal, not automatic permission to regenerate PHP
from frontend code. Treat drift as a review task: inspect changed frontend API,
events, DOM hooks, and behavior, then update the backend template or manifest
deliberately.

## Demo Expectations

When adding a backend smart component to `/demo/framework/`:

- keep examples close to the future SF5 model, even if demo data is file-based;
- prefer `Smart::render()` or `Smart::tree()` over hand-written repeated HTML;
- show generated HTML and, where useful, frontend and backend call examples;
- test responsive behavior at desktop, tablet, and mobile widths;
- verify theme toggles and persistent UI state when navigation is involved;
- keep example data in path-scoped `simai.data` when demonstrating local
  overrides.

## Verification Commands

For `bx-simai.main` backend smart runtime:

```bash
php docs/developer/specifications/tools/proof_smart_runtime_api.php
php docs/developer/specifications/tools/proof_backend_native_smart_artifacts.php
php docs/developer/specifications/tools/proof_backend_hydratable_smart_artifacts.php
php docs/developer/specifications/tools/proof_backend_host_skeleton_smart_artifacts.php
python3 docs/developer/specifications/tools/validate_smart_artifacts.py --format markdown
python3 docs/developer/specifications/tools/build_backend_smart_coverage.py --format markdown
```

For `ui-smart` frontend components:

```bash
node --check smart/<code>/js/<code>.js
gzip -t smart/<code>/js/<code>.js.gz
```

Use Playwright or the browser plugin for interaction checks when the component
has open/close, responsive, focus, keyboard, or persistent UI state.

For `SfBaseElement`-based frontend smart components, browser smoke should also
check:

```text
customElements.get('<tag>')
element instanceof SF.smart.SfBaseElement
SF.smart.html / SF.smart.render globals exist
setState() updates attributes and component-owned state
external/custom props appear in getState() or template context
no unrelated smart tag is registered by the bundle
```

## PR Handoff

For frontend smart PRs, include:

- component purpose;
- public attributes and methods;
- events;
- accessibility and keyboard behavior;
- relationship to existing components, especially `modal`, `close`, and
  `icon-button`;
- validation commands and browser smoke summary.

For backend smart PRs, include:

- artifact roots changed;
- manifests/views/presets/templates added;
- hydration strategy;
- generated HTML behavior;
- runtime proof commands;
- expected frontend dependency or standalone status.
