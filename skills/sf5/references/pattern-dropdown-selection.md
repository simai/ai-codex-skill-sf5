# SF5 Pattern: Dropdown And Selection

Use this playbook for select-like inputs, list-item choices, tag selection, page-size dropdowns, and searchable pickers.

## Default Decision

- Use static dropdown markup when you need full control of the HTML shell or are adapting existing server-rendered templates.
- Use smart dropdown when you want a cleaner authoring model based on `sf-dropdown` and nested `sf-list-item` nodes.

## Best Upstream Sources

- Static dropdown:
  `source/simai/ui-play/examples/components/dropdown/dropdown/index.html`
- Smart dropdown:
  `source/simai/ui-play/examples/smart-components/dropdown/element/index.html`
- Static pagination + embedded dropdowns:
  `source/simai/ui-play/examples/components/pagination/default/index.html`

## Static Markup Shape

- Main wrapper:
  `sf-dropdown`
- Common modifiers:
  - `sf-dropdown--size-*`
  - `sf-dropdown--outlined|filled`
  - `sf-dropdown--text`
- Internal structure usually includes:
  - label row
  - clickable field row
  - `sf-icon-button` caret trigger
  - optional search `sf-input`
  - `sf-list` with `sf-list-item`

## Smart Markup Shape

- Main element:
  `sf-dropdown`
- Useful attributes:
  - `size`
  - `type="outlined|filled"`
  - `mode="select|tag"`
  - `label`
  - `placeholder`
  - `multiple`
  - `disabled`
- Child items:
  `sf-list-item`
- Common child item attributes:
  - `type="text|icon|color"`
  - `size`
  - `text`
  - `icon`
  - `color-class`
  - `selected`

## Use Smart Dropdown When

- the authoring model should stay small and readable
- multiple selection/tag mode is needed
- items are created dynamically
- item semantics should live in child nodes instead of long static shell markup

## Use Static Dropdown When

- the backend already emits the control shell
- you need exact ownership of nested wrappers for integration into a legacy template
- you are adjusting just the visual layer of an already-rendered list/select UI

## Practical Rules

- Prefer `sf-list-item` as the canonical choice unit.
- Keep the dropdown width constrained with utilities like `max-w-sm`.
- For filters and page-size selectors, keep dropdown composition close to pagination/filter controls.
- For tag mode, only enable `multiple` when the UI visibly supports chip/tag feedback.

## Common Assembly Pattern

1. Choose `select` or `tag` mode.
2. Define item type: text, icon, or color.
3. Add disabled/selected states.
4. Place the control inside a layout utility wrapper.
5. Validate class and custom-element usage.
