# SF5 Pattern: Forms And Inputs

Use this playbook for text inputs, textarea, field hints, validation, masks, and small form groups.

## Default Decision

- Use static markup when the form is server-rendered and does not need runtime instance APIs.
- Use smart input components when the team wants concise custom-element authoring, dynamic insertion, masks, or external template overrides.

## Best Upstream Sources

- Static textarea:
  `source/simai/ui-play/examples/components/inputs/textarea/index.html`
- Smart input:
  `source/simai/ui-play/examples/smart-components/inputs/element/index.html`
- Smart country-code variant:
  `source/simai/ui-play/examples/smart-components/inputs/country-code`

## Static Markup Shape

- Wrapper class:
  `sf-textarea`
- Size modifiers:
  `sf-textarea--size-1/3|1/2|1|2|3`
- Visual variants:
  `sf-textarea--bordered` or `sf-textarea--filled`
- Typical children:
  - label row
  - `textarea.transition`
  - hint text block
- State handling:
  - add `error` on wrapper and control for error state
  - use native `disabled` on `textarea`

## Smart Markup Shape

- Element:
  `sf-input`
- Useful attributes:
  - `size`
  - `type="bordered|filled"`
  - `label`
  - `placeholder`
  - `hint`
  - `name`
  - `required`
  - `disabled`
  - `error`
  - `left-icon`
  - `right-text`
  - `hint-icon`
  - `mask`
  - `mask-pattern`
  - `template`

## Use Smart Input When

- fields are inserted dynamically into the DOM
- mask behavior is needed without hand-building the control shell
- external/custom templates must be swapped via `template="custom"`
- the authoring format should stay compact and declarative

## Use Static Input When

- backend templates already render the control shell
- exact HTML structure must be controlled manually
- the task is primarily visual and does not need runtime input API

## Practical Rules

- Keep form layout in utilities, not inside field markup:
  `grid`, `gap-*`, `max-w-*`, `content-main-start`
- Keep size tokens consistent across one form row.
- Reuse hint and error text placement exactly as in upstream examples.
- Prefer native `disabled`, `required`, and `name` semantics even in smart mode.

## Common Assembly Pattern

1. Build form grid with utilities.
2. Choose one field mode for the group: static or smart.
3. Add validation/error states.
4. Add icons/masks only where they improve the UX.
5. Validate the final snippet in strict mode.
