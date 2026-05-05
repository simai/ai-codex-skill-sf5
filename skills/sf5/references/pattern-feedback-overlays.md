# SF5 Pattern: Feedback And Overlays

Use this playbook for modal dialogs, toast stacks, tooltip surfaces, and button-triggered feedback UI.

## Best Upstream Sources

- Smart modal:
  `source/simai/ui-play/examples/smart-components/modal/element/index.html`
- Static toast:
  `source/simai/ui-play/examples/components/toast/default/index.html`
- Smart toast:
  `source/simai/ui-play/examples/smart-components/toast/default/index.html`
- Static tooltip:
  `source/simai/ui-play/examples/components/tooltip/all/index.html`
- Smart tooltip:
  `source/simai/ui-play/examples/smart-components/tooltip/element/index.html`
- Buttons for triggers/state demos:
  `source/simai/ui-play/examples/components/buttons/buttons/index.html`
  `source/simai/ui-play/examples/smart-components/buttons/events/index.html`

## Modal Rule

- Prefer smart modal for interactive dialogs.
- Use `sf-modal` with slots:
  - `slot="content"`
  - `slot="footer"`
- Trigger with buttons or `sf-button`.
- Use `data-sf-modal-close="<id>"` for close actions wired through markup.

## Toast Rule

- Use static toast when you need a fixed rendered notification block.
- Use smart toast when you need an interactive stack inserted by actions/events.
- Keep toast variants aligned with message severity:
  `default`, `primary`, `error`, `warning`, `success`

## Tooltip Rule

- Use static tooltip when it is part of a fixed visual composition.
- Use smart tooltip when content is inserted dynamically or slot override is useful.
- Common smart tooltip attributes:
  - `size`
  - `arrow`
  - `text`
  - `supporting-text`

## Trigger Rule

- Build triggers with `sf-button` or static `sf-button` markup.
- Keep trigger controls outside the overlay surface body unless the component API expects internal actions.
- Treat feedback triggers and feedback containers as separate concerns.

## Practical Rules

- Keep overlay content in small layout wrappers with `flex`, `grid`, and `gap-*`.
- Prefer slot content over deep shell rewrites for smart overlays.
- Keep severity, iconography, and button style aligned.
- Use smart mode whenever dynamic insertion or instance API matters more than shell control.

## Common Assembly Pattern

1. Choose overlay type: modal, toast, or tooltip.
2. Decide static vs smart based on lifecycle needs.
3. Add trigger buttons.
4. Add states/variants and supporting text.
5. Validate the final snippet.
