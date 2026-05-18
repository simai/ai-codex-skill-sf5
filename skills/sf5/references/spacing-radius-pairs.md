# SF5 Spacing And Radius Pairs

Use this reference when choosing SF5 utility classes for cards, panels, nested surfaces, code/source blocks, chips, compact controls, and visual examples.

## Core Rule

Spacing and corner radius must move together.

When a surface uses a spacing level, use the matching radius level unless the component contract explicitly defines its own shape:

- `space-4` / `p-4` / `gap-4` -> `radius-4`
- `space-3` / `p-3` / `gap-3` -> `radius-3`
- `space-2` / `p-2` / `gap-2` -> `radius-2`
- `space-1` / `p-1` / `gap-1` -> `radius-1`
- `space-1/2` / compact axis padding -> `radius-1/2`

Do not combine a large internal spacing level with a tiny radius, or a tiny spacing level with a large radius. That makes nested SF5 surfaces visually inconsistent.

## Nesting Scale

Use this scale for nested surfaces:

| Level | Typical use | Utilities |
| --- | --- | --- |
| 4 | Page section, large hero surface, wide demo canvas | `p-4 radius-4` |
| 3 | Large panel, card group, editor shell | `p-3 radius-3` |
| 2 | Normal card, form panel, preview area | `p-2 radius-2` |
| 1 | Nested block, code block, stat card, list item container | `p-1 radius-1` |
| 1/2 | Chip, inline code, compact label, small inner control | `p-y-1/2 p-x-1 radius-1/2` or equivalent compact padding |
| circle | Avatar, badge dot, icon-only round action | `radius-circle` |

For nested layouts, descend one level per visual layer:

```html
<section class="p-4 radius-4">
  <div class="p-3 radius-3">
    <div class="p-2 radius-2">
      <div class="p-1 radius-1">
        <span class="p-y-1/2 p-x-1 radius-1/2">Text example</span>
      </div>
    </div>
  </div>
</section>
```

## Utility Families

The design shorthand `space-N` means "use the matching SF5 spacing token for the job".

In actual markup, choose the utility family that matches the axis and behavior:

- `p-*`, `p-x-*`, `p-y-*` for internal padding;
- `m-*`, `m-x-*`, `m-y-*` for external spacing;
- `gap-*`, `gap-x-*`, `gap-y-*` for layout gaps;
- `radius-*` for rounded surfaces;
- `radius-circle` for fully round shapes.

Prefer utility classes and SF5 tokens over raw pixel values.

## Code And Source Blocks

Code/source blocks inside another panel should normally use:

```html
<pre class="p-1 radius-1">...</pre>
```

Use `p-2 radius-2` only when the source block is a large standalone surface. Code text must never touch the border.

## Component Contracts

If a component already has its own size and shape modifiers, do not override its internals with arbitrary spacing/radius utilities.

Examples:

- Buttons use their own size and variant classes such as `sf-button--size-1`.
- Dropdowns/selects use their component contract.
- Backend Smart templates should emit the component host/contract and only add surface wrappers when the layout needs them.

## Avoid

- `radius-4` on compact chips, small buttons, labels, or code tokens.
- `p-4 radius-1` on large panels.
- `p-1 radius-4` on compact nested elements.
- Raw `padding: 24px` or `border-radius: 18px` when an SF5 utility/token exists.
- Extra decorative nested cards when a plain surface or layout wrapper is enough.
