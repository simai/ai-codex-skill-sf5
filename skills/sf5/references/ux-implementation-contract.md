# UX Implementation Contract

Use this reference when `$sf5` implements an interface designed or reviewed by `$ux`.

## Rule

Do not treat `$ux` output as generic layout advice. Convert it into SF5 layer, component, smart-component, block, recipe, and validation contracts.

## Required Mapping

- `Scenario`: user, primary action, success state.
- `Layer mapping`: utilities, components, smart-components, blocks, page recipe.
- `Component contract`: props, slots, events, visual states, validation states.
- `Smart-component contract`: data loading, persistence, permissions, side effects, state orchestration.
- `Recipe/pattern`: page recipe and pattern playbooks to use before custom composition.
- `State contract`: empty, loading, error, success, disabled, partial.
- `Validation`: SF5 catalog/manifest checks, recipe checks, local browser/screenshot checks.
- `Acceptance`: `$tester` usability gate, responsive checks, focus/keyboard where interactive.

## Output Back To `$ux`

If SF5 constraints change the design, report:

```markdown
UX deviation:
SF5 layer/component reason:
Alternative:
Retest point:
```
