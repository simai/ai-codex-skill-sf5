# SF5 Modifiers And Utilities Reference

This file summarizes modifier rules and utility usage from the docs snapshot.

## Contents

- Modifier Syntax
- Condition Types
- Breakpoints
- Value Families
- Direction Semantics
- Spacing And Tokens
- Common Utility Groups
- Themes And Colors
- Utility Review Checklist

## Modifier Syntax

Canonical pattern:

`{condition}:{modifier}`

Where:

- `condition` is optional (breakpoint or state).
- `modifier` is required.

Examples:

- `md:hidden`
- `hover:bg-primary`
- `focus:outline`
- `active:opacity-80`

## Condition Types

- Responsive conditions: breakpoint-prefixed modifiers.
- State conditions: `hover`, `focus`, `active`.

If no condition is provided, the modifier applies in all contexts.

## Breakpoints

Primary breakpoint description pages define:

- `sm >= 576px`
- `md >= 768px`
- `lg >= 960px`
- `xl >= 1152px`
- `xxl >= 1536px`

Variables are documented as:

- `--sf-breakpoint-sm`
- `--sf-breakpoint-md`
- `--sf-breakpoint-lg`
- `--sf-breakpoint-xl`
- `--sf-breakpoint-xxl`

Important:

- Some utility pages show different values (for example `sm >= 540px`, `xl >= 1140px`, `xxl >= 1320px`).
- Treat this as a docs inconsistency.
- Resolve by checking real project CSS variable values before implementing breakpoint-sensitive changes.

## Value Families

Docs describe these value families for modifiers:

- absolute dimensions
- relative dimensions
- proportional values
- binary values
- percentages
- degrees

Examples:

- absolute: `w-0`, `w-px`
- percentage/full: `w-full`
- negative modifier: `-m-2`
- degree: `rotate-45`

## Direction Semantics

Axis notation:

- `x` for horizontal behavior
- `y` for vertical behavior

Use logical properties for bidi support:

- prefer `inline-start`/`inline-end` and `block` semantics
- avoid hardcoding `left`/`right` in custom extensions when utility equivalents exist

## Spacing And Tokens

- Padding and margin utilities are mapped to `--sf-space-*` tokens.
- Typical spacing values include:
  `0, 1/4, 1/3, 1/2, 1, 2, 3, 4, 5, 6, 7, 8`
- Prefer utility/token usage over raw pixel literals.

## Common Utility Groups

Start with these groups for most tasks:

- layout
- grid
- flex and grid-flex helpers
- indents
- sizes
- typography and text-formatting
- border, outline, shadows
- background
- interactivity

Use specialized groups (`mask`, `filter`, `backdrop-filter`, `print`, etc.) only when task requirements justify the added complexity.

## Themes And Colors

Theme usage:

- `.theme-light`
- `.theme-dark`

Color model from docs:

- primitives -> tokens -> roles
- major roles include `surface`, `primary`, `secondary`, `tertiary`, plus status roles and `on-*` companion colors

Examples:

- `bg-surface-container`
- `color-primary`
- `border-warning`

## Utility Review Checklist

1. Confirm modifier syntax is valid and scoped correctly.
2. Confirm breakpoint choice uses actual project variables (not just docs text).
3. Confirm states (`hover`, `focus`, `active`) do not regress accessibility.
4. Confirm logical-direction safety (LTR/RTL compatibility).
5. Confirm token/role usage instead of hardcoded design values.
