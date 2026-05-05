# SF5 Pattern: Upload And Progress

Use this playbook for file uploads, upload status blocks, fake/real progress indicators, and value sliders used as progress-like inputs.

## Best Upstream Sources

- Static file upload:
  `source/simai/ui-play/examples/components/file-upload/default/index.html`
- Smart file upload:
  `source/simai/ui-play/examples/smart-components/file-upload/element/index.html`
- Static range slider:
  `source/simai/ui-play/examples/components/range-slider/default/index.html`
- Smart range slider:
  `source/simai/ui-play/examples/smart-components/range-slider/default/index.html`

## Default Decision

- Use static upload markup when the dropzone/status UI is mostly presentational.
- Use smart file upload when multiple files, accept rules, progress/error events, or dynamic state transitions matter.
- Use range slider as a compact quantitative selector, not as a substitute for upload status.

## Static Upload Shape

- Main wrapper:
  `sf-file-upload`
- Common modifiers:
  `sf-file-upload--size-*`
- Typical composition:
  - featured icon
  - upload call-to-action text
  - accepted format hint
  - disabled state
- Related status blocks:
  `sf-upload-progress`

## Smart Upload Shape

- Element:
  `sf-file-upload`
- Useful attributes:
  - `size`
  - `multiple`
  - `disabled`
  - `accept`
  - `formats`
- Useful surrounding elements:
  - `sf-button` triggers for fake progress/error demos
  - event log/output containers

## Range Slider Shape

- Static:
  `div.sf-range-slider` with `data-start`, `data-label`, `data-suffix`
- Smart:
  `sf-range-slider` with `min`, `max`, `start`, `label`, `suffix`

## Practical Rules

- Keep upload and progress state visually explicit.
- Prefer smart upload when event handling or status transitions are part of the feature.
- Prefer smart range slider when the UI needs concise declarative authoring and dynamic output binding.
- Keep accepted formats and constraints visible in the UI, not only in code.

## Common Assembly Pattern

1. Choose static or smart upload shell.
2. Define accepted formats and multi-file behavior.
3. Add progress/error surfaces.
4. Add sliders only for parameter selection, not as a fake upload replacement unless explicitly required.
5. Validate the final snippet.
