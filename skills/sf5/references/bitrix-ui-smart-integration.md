# Bitrix UI + Smart Integration Reference

Use this reference when SF5 frontend assets are shipped through a Bitrix module or a Bitrix site starter.

## Package Boundary

Keep the frontend packages separate:

```text
/simai/asset/simai.ui/<ui-version>/
  core/
  component/
  utility/
  rule/
  fonts/
  smart-component-meta.json

/simai/asset/simai.ui.smart/<smart-version>/
  smart/
    modal/js/modal.js
    buttons/js/buttons.js
    dropdown/js/dropdown.js

/simai/asset/highlight.js/<highlight-version>/
  highlight.min.js
  styles/github.min.css
  styles/github-dark.min.css
  LICENSE
```

Do not copy `ui-smart` assets into `simai.ui/<version>/component/`.

## Loader Wiring

Use explicit paths:

```html
<script>
  window.sfPath = '/simai/asset/simai.ui/5.0.1/';
  window.sfSmartPath = '/simai/asset/simai.ui.smart/5.0.0/';
</script>
```

Then connect UI core:

```html
<link rel="stylesheet" href="/simai/asset/simai.ui/5.0.1/core/css/core.css">
<script src="/simai/asset/simai.ui/5.0.1/core/js/core.js"></script>
```

The loader builds smart asset URLs from `window.sfSmartPath`:

```text
/simai/asset/simai.ui.smart/5.0.0/smart/<component>/js/<component>.js
```

## Bitrix Module Packaging

For `simai.main`-style modules:

- keep public starter assets under `install/starter/simai/asset/`;
- publish `simai.ui` and `simai.ui.smart` as independent versioned directories;
- use uninstall markers for module-owned public demo/starter folders;
- never delete or overwrite site-specific `simai.data` unless the installer explicitly selected that site;
- avoid deleting unrelated project folders under `/simai`, for example `/simai/property`.

## Release Payload Intake

When a user provides local release folders or unpacked archives, build the module payload from release contents, not from CDN URLs.

### UI package

Input examples:

```text
/Users/rim/Downloads/ui-5.0.1
/Users/rim/Downloads/ui-5.0.1/distr
```

Find the distributable root that contains:

```text
core/
component/
utility/
rule/
fonts/
```

Copy that distributable root into:

```text
local/modules/<module>/install/starter/simai/asset/simai.ui/<ui-version>/
```

The `<ui-version>` is normally derived from the release folder name, tag, or release metadata, for example `ui-5.0.1` -> `5.0.1`.

### Smart package

Input examples:

```text
/Users/rim/Downloads/ui-smart-5.0.0
/Users/rim/Downloads/ui-smart-5.0.0/ui-smart-5.0.0/smart
```

Find the release `smart/` directory and copy it into:

```text
local/modules/<module>/install/starter/simai/asset/simai.ui.smart/<smart-version>/smart/
```

The `<smart-version>` is independent from the UI version, for example:

```text
simai.ui/5.0.1/
simai.ui.smart/5.0.0/
```

Do not copy smart component files into `simai.ui/<version>/component/`.

### Required follow-up edits

After replacing release payloads:

- update `window.sfPath` to `/simai/asset/simai.ui/<ui-version>/`;
- update `window.sfSmartPath` to `/simai/asset/simai.ui.smart/<smart-version>/`;
- update Bitrix `Asset::addCss()` / `Asset::addJs()` paths;
- update static smoke pages and demo pages;
- update docs/release notes that mention package versions;
- remove old module-owned package directories when the replacement is intentional;
- keep unrelated public folders under `/simai` untouched.

### Validation

Validate the release intake with:

- PHP lint for changed Bitrix files;
- source scan for stale old paths in module-owned PHP/HTML/demo files;
- direct HTTP checks for `core/css/core.css`, `core/js/core.js`, and at least one smart JS file;
- browser/HAR smoke showing no CDN/external requests, no old version paths, and no unexpected 4xx/5xx;
- rule-vs-smart coverage check: smart rules in `simai.ui/<version>/rule/rule.json` should map to actual directories in `simai.ui.smart/<version>/smart/`; missing packages must be reported instead of faked.

## Demo And Smoke

A Bitrix-native demo should prove:

- `core/css/core.css` and `core/js/core.js` load from `simai.ui`;
- component and utility assets load from the same UI version;
- smart assets load from `simai.ui.smart`;
- syntax highlighting helpers, if used, load from local module-owned assets such as `/simai/asset/highlight.js/<version>/`, not from CDN;
- examples are isolated from the admin/demo shell when needed;
- source/example renderers are whitelist-based.

Keep the demo shell visually native to SF5:

- use the SF5 implementation ladder before writing custom UI: first look for a suitable smart-component, then for a normal component, then compose with SF5 utilities/tokens; only write custom/project/demo CSS or JS when the framework has no suitable surface, and record the missing capability for SF5 maintainers so the gap can be closed later;
- use SF5 primitives and utilities for visible cards, buttons, grids, spacing, borders, and text color;
- do not introduce a separate hardcoded demo palette for light/dark mode;
- shell-only CSS may handle fixed header, max-width, iframe/code panes, and copy/smoke states, but its colors should reference SF5 theme tokens such as `--sf-surface-*`, `--sf-on-surface*`, `--sf-outline-*`, and `--sf-*-container`;
- when a screenshot shows an unexpected color, verify whether it comes from SF5 tokens or from local shell CSS before treating it as a framework issue.

Practical layout lessons from `simai.main` demo work:

- Avoid wrapping a card grid in another decorative card. Page sections may be plain flow blocks with a heading and a grid; reserve `sf-card` for the repeated items, preview panes, code panes, or other genuinely framed content.
- In repeated card rows, keep row rhythm stable: cards in the same row should stretch to equal height and the usual CTA/action should sit on the bottom edge. Use a stretching grid/flex row, card `display:flex; flex-direction:column`, and action `margin-top:auto`.
- Do not make card CTAs full width unless the surrounding product pattern explicitly asks for full-width actions. In demo/catalog cards, prefer content-width buttons with `align-self:flex-start; width:auto; max-width:100%` while preserving bottom alignment.
- For example/detail pages, prefer a vertical reading flow: full-width preview first, source/code blocks below. Side-by-side preview/code layouts make wide component examples feel cramped and can create visual double nesting.
- Keep surface levels distinct. For normal pages, use the neutral page surface (`bg-surface` / `--sf-surface-1`) on the page/body and place first-level cards and fixed headers on the base surface (`bg-surface-0` / `--sf-surface-0`). This gives a light gray page background with white cards/header in light theme. Do not put the page and its cards on the same surface token.
- If a preview is rendered inside an iframe, keep it isolated for assets and JS, but inherit the parent theme class when possible. The iframe body should use the page surface (`bg-surface` / `--sf-surface-1`) and text token (`color-on-surface` / `--sf-on-surface`), not local hardcoded `#fff` or dark fallback colors.
- In preview renderers that show existing examples, apply a narrow fallback so `.sf-card` elements without an explicit `bg-*` class use `--sf-surface-0`. This preserves the surface hierarchy without rewriting every upstream example and without overriding examples that intentionally set their own background utility.
- Theme toggles must actively propagate into already loaded preview iframes. On parent theme change, update `iframe.contentDocument.documentElement` when accessible and also send a small `postMessage` such as `{type:"sf-demo-theme", theme:"light"}`; the `srcdoc` page should listen for it and update `theme-light` / `theme-dark`.
- Preview iframes should not be treated as small scroll boxes. Disable iframe scrolling and resize the iframe to its content height, for example with a `ResizeObserver` inside `srcdoc` posting `{type:"sf-demo-preview-height", height}` to the parent. The browser page should scroll, not the embedded example frame.
- In auto-height preview iframes, do not put `min-height:100vh` or equivalent viewport-height layout on the `srcdoc` body/root. The iframe viewport becomes the height assigned by the parent, so `100vh` can create a feedback loop where each resize increases the measured `scrollHeight`. Measure a stable content root such as `.demo-preview-root.getBoundingClientRect().bottom + body padding` instead of deriving the target height from a viewport-sized body.
- Do not add a decorative border around the preview iframe when the rendered example already contains its own cards, borders, or section framing. The iframe is an isolation mechanism, not an extra visual container.
- After removing the iframe border, also avoid iframe-body padding unless a specific example requires it. Otherwise the padding looks like a remaining invisible preview container. Let the example markup provide its own spacing with SF5 utilities.
- For source-code panels in demos, prefer a small local `highlight.js` browser bundle plus only the needed light/dark styles. If the demo uses standalone highlight.js instead of the SF5 `component/highlight`, avoid markup that triggers the SF5 highlight auto-rule (`language-*` classes or `<pre><code>`). Use an explicit demo-only marker such as `data-demo-language="html"` and call the highlighter directly. Switch the highlighter theme with the same SF5 theme toggle instead of adding another independent color mode.
- Before replacing a custom generated-code panel with SF5 `component/clipboard` or `component/highlight`, verify the interaction contract. Current `component/clipboard` exposes a shortcode `Copy` component that renders a full `sf-button`; it is not a drop-in replacement for compact icon-only copy actions in dense code headers. Current `component/highlight` owns `<pre><code>` / `language-*` blocks and injects `.source`, header, copy shortcode and line numbers. For continuously re-rendered playground snippets, standalone local `highlight.js` with `data-demo-language` plus custom copy glue over an SF5 `sf-icon-button` is an acceptable documented exception.
- The SF5 clipboard rule currently matches raw `source` in the rendered document as well as `btn-clipboard`. If a Bitrix demo page is not intentionally using `Copy`, avoid rendering `source` in shell class names, inline JS, or inline registry JSON; use neutral names such as `evidence` or escape registry keys in inline object literals when the runtime key must remain `source`.
- For icon buttons and Material Symbols in Bitrix demos/projects, configure icons before loading `core/js/core.js`: `window.SF_BOOT_CONFIG = window.SF_BOOT_CONFIG || {}; window.SF_BOOT_CONFIG.icons = Object.assign({accumulate:true}, window.SF_BOOT_CONFIG.icons || {});`. Use SF5 markup such as `sf-icon-button ...` with nested `<i class="sf-icon">dark_mode</i>` instead of custom text spans. With `accumulate:true`, the local SF5 loader still loads local `component/icons` and `component/icon-buttons` assets, but it can intentionally request generated subset CSS/fonts from `https://icons.simai.io/ms/...`; smoke checks should treat those icon-service requests as an explicit exception, not as an accidental CDN leak.
- SIMAI Font Service is a Node.js icon subset service, not a Bitrix module asset payload. Its public contract is `/ms/css?icon_names=...` returning `@font-face`, linked `/ms/font/{hash}.woff2`, `/ms/meta/{hash}`, `/ms/latest`, `/ms/test`, and `/health`. `icon_names` is required. `weight`/`wght` accepts a single value, a range such as `400..700`, or a list, but generated weights are limited to `100..700`; out-of-range values are ignored. It also supports `fill`, `grad`/`GRAD`, `opsz`, and `display` (`block` by default, `swap` allowed). Default `MAX_ICON_COUNT` is `200`, so icon catalogs must window/search icons instead of requesting thousands in one subset.
- In Bitrix/SF5 HAR checks, allow `https://icons.simai.io/ms/css...` and the linked `https://icons.simai.io/ms/font/...woff2` only when icon accumulation is intentional. Keep all other external demo media/CDN requests blocked unless explicitly approved. A proper icon smoke checks that subset CSS returns 200, the referenced WOFF2 returns 200, and no unrelated external requests appear.
- For icon catalog or icon-picker demos, store the Material Symbols name/codepoint index locally in the module payload and search it client-side. Do not render all 4000+ icons at once: render a small first window (for example 96), provide search and "show more", and generate copyable SF5 snippets such as `<i class="sf-icon sf-icon-rounded sf-icon-filled sf-icon-regular sf-icon--size-4">home</i>`. This keeps the page responsive and avoids forcing the icon subset service to accumulate thousands of glyphs in one request.
- For smart-component demo catalogs sourced from `ui-play/examples/smart-components`, treat `ui-play` as source material, not a runtime dependency. Copy only example files into the module payload, generate a whitelist PHP manifest from existing `index.html` leaves, and render each example through the shared isolated preview/source renderer. Remove relative `<script src="./index.js">` tags from copied example HTML because the renderer already injects the whitelisted JS source; leaving both can make `srcdoc` request a wrong relative URL and fail with `Unexpected token '<'`.
- For smart-component API documentation, do not infer the contract from example markup alone. Build a source-backed registry from the shipped `simai.ui.smart/<version>/smart/<component>/js/<component>.js` bundles: extract `.define("sf-*")`, `static get props()`, getter-derived enum/boolean/number defaults, common `SfBaseElement` lifecycle events, component events, methods found, and links to copied examples. Keep extracted facts separate from inferred descriptions, because minified bundles can expose internal methods that are not necessarily public API. Use that registry as the source for Bitrix demo API pages and future playground generators.
- When adding a PHP API/wrapper for SF5 smart-components in Bitrix, treat PHP as a declarative renderer, not as a server-side implementation of the smart component. Build calls from the same source-backed registry used by docs/playgrounds, validate props and compatibility constraints before rendering, emit canonical `<sf-*>` markup plus slots/data attributes, and connect assets through a Bitrix adapter. Keep the neutral smart-component contract portable so Larena or another backend can implement its own asset/config adapter without forking component semantics.
- Present smart-component API docs as a documentation interface, not as one long mixed catalog. Prefer a left rubricator/sidebar with search and a right detail pane for one selected `<sf-*>` tag. Keep the selected component addressable by hash or URL, show usage, attributes, events, methods and examples together, and move common lifecycle events into their own navigation item. On mobile, let the rubricator flow above the detail pane instead of forcing a sticky side column.
- Use the same left-rubricator pattern for framework demo catalogs such as utilities, components, and smart examples. The sidebar should provide section navigation, counts, and filtering; the right side should show scannable component/example sections. This is more usable than a flat card grid once a catalog has more than a handful of sections, while still keeping previews/examples accessible through explicit buttons.
- For documentation/playground side navigation, prefer ordinary `component/menu` over smart `sf-list-item` when the item is a real link. Use `ul.sf-menu > li.sf-menu-item > a.sf-menu-element` with an inner `.sf-menu-element-wrap` and `.sf-menu-element-text`; mark the current route with `open` and `aria-current="page"`. Avoid wrapping `sf-list-item` in `<a>` because the smart component renders its own interactive `role="button"`. Keep sticky positioning and text overflow as demo-shell glue only; let `sf-menu-element` own hover/active/focus styling.
- Utility catalogs are navigation-heavy, not action-heavy. Show utility groups as a second-level sidebar menu under their parent utility section, and use compact text links in the right pane instead of large primary buttons. Reserve button-like controls for opening component/smart examples where the item feels like a runnable demo action.
- Component catalogs may also expose example groups as second-level sidebar navigation. In catalog pages, prefer compact text links in the right pane instead of large CTA buttons; the actual runnable controls belong on the isolated example/preview page, not in the catalog overview.
- When a catalog item opens an isolated example page, keep the same left rubricator on the example page. The user should not lose the component/utility/smart navigation after clicking a group; the right pane should change to preview plus source code while the left pane keeps parent/group context and active states.
- For ordinary CSS/JS component playgrounds, build the API model from class modifiers rather than smart props. Use local component CSS, component utility JSON when present, and copied examples as the source of truth; group controls by modifier families such as type, scheme, size, density/tightness, radius, segment, and states. Start with one well-structured component such as buttons before generalizing to the whole catalog.
- For ordinary component playground pages, use a documentation-style three-zone layout on desktop: left catalog/rubricator, center preview + generated code + source facts, and right settings/controls. This keeps navigation stable while the user tunes the component, and mirrors mature component-doc patterns such as Gravity UI without copying their implementation model. Collapse to one column on narrow screens and verify no horizontal overflow.
- For Bitrix/SF5 playground workbench layouts, prefer SF5 grid utilities before custom CSS: `grid grid-col-12`, `col-span-*`, `gap-*`, `min-w-0`, and `items-cross-start`. Keep custom CSS only for named shell mechanics such as breakpoint collapse, sticky sidebar, fixed topbar, iframe/code-pane limits, or demo-specific renderer glue.
- When custom Bitrix demo shell remains after SF5-first refactoring, produce a source-backed gap report instead of leaving undocumented exceptions. Group gaps by component, smart-component, utility/layout, and documentation/API; for each gap record current workaround, desired SF5 surface, priority, affected URL, and evidence from code or browser smoke. Mark Bitrix bootstrapping, local package paths, PHP localization, and install/public publication as accepted shell unless the framework deliberately owns a docs-site product surface.
- Treat the component playground as a data-driven renderer, not as hand-authored per-component pages. The preferred model is one source-backed registry array per surface: components use class modifiers, states, HTML content controls, examples, and source facts; utilities use utility groups/classes/examples; smart-components use tag names, props/attributes, events, methods, and examples. Build the left menu and the right workbench from that registry so both humans and AI tools can reuse the same component contract.
- Component playground registries should include source-backed compatibility constraints between controls when modifiers are not freely composable. For CSS components, derive these constraints from selectors whenever possible, for example button `type -> scheme` pairs where `tonal` supports `secondary/on-surface` but not `primary`. The renderer should filter dependent controls and reset invalid selected values before updating preview or generated HTML.
- When SF5 smart controls drive a data-driven playground, keep technical values in the registry and treat visible labels as presentation only. In the current smart dropdown, selected state may expose the visible label through DOM state, so the renderer must normalize selected labels back to registry values before generating CSS classes. Preserve empty `value=""` as a valid default option instead of falling back to the label text. Recalculate dropdown constraints only when grouped controls change; plain text input and checkbox changes should only re-render preview/code so they do not disturb the dropdown option list.
- Do not use initialized smart-component DOM as the source of truth for playground option lists. For example, `sf-dropdown` may consume `sf-list-item` children and render internal `.sf-list-item` nodes that no longer preserve custom technical attributes such as `data-value`; `sf-list-item` also has no public `value` prop in the current registry. Pass option values/labels from the PHP/source-backed registry into the shared renderer, then use smart controls only as the visible UI surface.
- When rendering demo shell controls through the PHP `Smart` facade, respect the registry/global-attribute validator. Do not add native browser attributes such as `autocomplete` unless the smart-component registry or global attribute allow-list explicitly supports them; use declared props, `data-*`, `aria-*`, or update the registry contract instead. For search/filter controls, `Smart::input(['type' => 'bordered', ...])->data('...')` is the safe Bitrix demo-shell pattern, with JS reading the internal rendered input value.
- For Bitrix module demos, keep the generic component playground renderer in a shared public asset and let PHP pages only bootstrap Bitrix, load the registry/manifest, render safe markup, and call something like `ComponentPlayground.init(root, registryItem)`. Do not keep large per-component renderer logic inline in PHP pages once the renderer is intended to serve multiple components.
- Localize Bitrix demo UI through normal Bitrix `lang/<lang>/...` files from the start. Keep technical registry values stable for class generation, but translate visible option labels, page labels, sidebar labels, and renderer messages. Pass only runtime phrases needed by shared JS through `registryItem.messages` or an equivalent message payload.
- If a playground becomes a universal cross-component tool, expose it as a top-level demo section such as `/demo/framework/playground/` with its own top navigation item. Keep component/utility/smart catalogs focused on browsing examples and avoid large promo blocks inside catalog pages; use redirects from older nested playground URLs when needed.
- In this playground layout, everything to the right of the left rubricator should read as one workbench. Inside it, keep preview/code/source facts in the main lane and settings in the secondary lane. Do not constrain the settings lane with its own max-height/internal scroll unless the user explicitly asks for a sticky inspector; page-level scrolling is more usable for long component controls.
- In playground pages, the left sidebar should list playground entities from the playground registry, not example catalog groups. For a component playground, show component names only; each item links to its own playground route such as `/demo/framework/playground/?component=buttons`. Keep example counts, filters, and nested example groups in catalog pages, not in the playground workbench.
- Keep SF5 demo/playground copy sparse. Do not add helper phrases that only restate a heading or describe obvious behavior such as "live preview" or "change parameters"; use visible text for labels, actions, source facts, error prevention, and meaningful state only.
- Avoid decorative horizontal divider rules inside one playground workbench; use spacing and headings for hierarchy. Code/source panels must include internal padding so highlighted code does not touch the border.
- Present playground source facts as compact evidence, not raw debug output: use small stat cards for counts and a wrapping monospace source path; avoid horizontal scrollbars for normal source paths at desktop widths.
- Use compact icon buttons for copy actions inside dense code headers. They should be no taller than the heading line plus a small allowance and align visually on the same line; full-height action buttons create unnecessary whitespace in code panels.
- For icon-only utility actions in SF5 interfaces, prefer `sf-icon-button--link sf-icon-button--on-surface` as the default variant. It reads as an icon at rest and reveals the button affordance on hover/focus. Use `tonal` only when the icon action must be persistently prominent.
- Before shipping copied smart examples in a Bitrix module, sanitize demo-only external media URLs (`randomuser.me`, `placehold.co`, `picsum.photos`, demo iframes such as `wikipedia.org`) into local/inline placeholders unless the task explicitly allows those external requests. Keep icon-service subset requests separate from these accidental example-content requests.
- After each visual correction, verify the exact public URL with browser evidence and HAR: no external/CDN requests except explicitly approved SF5 icon-service subset requests, no old `simai.framework` paths, no unexpected `4xx/5xx`.

Preferred checks:

- PHP lint for touched Bitrix PHP files;
- authenticated HTTP smoke for admin-protected demo pages;
- Playwright/HAR or equivalent browser evidence;
- no CDN/external requests unless the task explicitly allows them;
- no old version paths after a version migration.

## Known 2026-05-13 Package Fact

The observed pair:

- `ui` payload: `/Users/rim/Downloads/ui-5.0.1/distr`
- `ui-smart` payload: `/Users/rim/Downloads/ui-smart-5.0.0/ui-smart-5.0.0/smart`

The UI loader `rule.json` has 35 smart rules. The smart payload has 34 matching smart directories. The missing package is:

```text
cl-tabs -> smart/tabs/js/tabs.js
```

Treat `tabs` as unavailable in demos until the smart package provides it. Do not fake it by loading the ordinary `component/tabs` asset as a smart component.
