# Demo Path Overlay Playground

Use this knowledge pack when implementing or reviewing SF5 demo sections that
must exercise the real architecture in a local/path-scoped environment.

## Rule

`/demo/framework/simai.data` is a demo-local overlay, not a place for base SF5
framework packages.

It may contain:

```text
section/
block/
smart/
design/
```

It must not contain copied system components that belong to:

```text
/simai/asset/simai.ui/<version>
/simai/asset/simai.ui.smart/<version>
```

## Playground Pattern

For interactive UI workbenches, prefer a composite smart artifact:

```text
demo/framework/simai.data/smart/playground/
  manifest.php
  template.php
```

The public page should call a backend facade:

```php
Smart::composite('playground', $context, $basePath)
```

The page shell owns routing and navigation. The composite smart owns preview,
settings, generated code, copy action, source metadata and parameter logic.

When a demo overlay already has `section/` and `block/` manifests, make the
chain executable instead of leaving the manifests as passive documentation:

```text
section/<code>/manifest.json
  -> blocks[0].block
  -> block/<code>/manifest.json
  -> smart.code
  -> Smart::composite(smart.code, context, overlayPath)
```

For Bitrix demo pages, a small filesystem reader is acceptable while the real
storage layer is not connected. Keep it explicitly demo/path-scoped and do not
turn it into a broad production registry by accident.

The visible playground entity list should also be overlay-controlled:

```text
smart/playground/entities.json
```

Use it to decide which source-backed component schemas are exposed in the demo
navigation. Do not build the left menu by blindly dumping the whole extracted
component registry.

Keep component schemas declarative enough for a shared renderer. A playground
entity should not require its own PHP page when the differences can be described
with fields such as:

```text
element
baseClass
textContainerClass
textClass
iconContainerClass
groups
constraints
```

Use source-backed CSS, utility JSON and examples as evidence for these fields.

Every enabled entity listed in `smart/playground/entities.json` should pass the
demo registry validator before being treated as supported:

```bash
php local/modules/simai.main/install/public/demo/framework/tools/validate-playground-registry.php
```

The validator is a small demo contract gate. It checks that each entity has a
source-backed schema, valid defaults, valid constraint pairs, and at least one
generated HTML smoke sample. Keep it bootstrap-free so it can run quickly before
browser checks.

When composing playground controls from SF5 smart dropdowns, treat host
attributes, inner dropdown state, and visible input labels as eventually
consistent rather than immediately identical. For registry-driven controls:

- normalize visible labels back to registry values before generating HTML;
- defer updates after `sf-dropdown:change` until the smart component has updated
  its own DOM;
- synchronize opened `.sf-list-item` options by visible label when the smart
  component does not render `data-value`;
- update runtime selection state from the normalized value before reading
  constraints or generated HTML.
- after a smart dropdown has rendered, do not write the normalized value back to
  the `value` attribute of the `sf-dropdown` host. Chrome can treat that as a
  component property update and re-render the light DOM to an empty state. Store
  playground state in `dataset`, the visible input, and selected item state
  instead.
- when reading rendered `.sf-list-item`, prefer `.sf-list-item-container`
  content over whole `textContent`; selected items may append a visual `check`
  label that is not part of the option value.

## Constraints

Component playground controls must be registry-driven. If one parameter limits
another parameter, encode that relation in the registry and enforce it in the
playground runtime.

Required behavior:

- invalid combinations are not generated;
- dependent controls switch to the first valid value when needed;
- smart dropdown/input state remains visible and non-empty after constraint
  changes;
- backend renderer should eventually validate the same constraints.
- mutually exclusive component states must be represented as one state selector,
  not as independent checkboxes. For example, a button playground should offer
  `default/disabled/active/loading` as one dropdown so it cannot generate
  impossible combinations such as disabled plus loading.

## Documentation

Project-level canonical document:

```text
bx-simai.main/docs/developer/specifications/demo-framework-simai-data.md
```
