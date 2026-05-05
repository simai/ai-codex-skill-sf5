# SF5 Scenario: Auth

Use this scenario for sign in, sign up, password reset, confirmation, and compact auth-related forms.

## Build From

- `references/page-recipe-auth.md`
- `references/pattern-forms-inputs.md`
- `references/pattern-feedback-overlays.md`
- `source/simai/ui-play/examples/smart-components/inputs/element/index.html`
- `source/simai/ui-play/examples/components/buttons/buttons/index.html`
- `source/simai/ui-play/examples/modal/all`

## Default Screen Structure

1. Brand/header strip
2. Main auth card
3. Primary form fields
4. Secondary actions
5. Inline validation / feedback

## Recommended Composition

- Outer shell:
  centered column with utility layout and restrained width
- Fields:
  smart `sf-input` for concise authoring or static input shell for legacy templates
- Primary CTA:
  `sf-button` or static `sf-button` classes
- Secondary flows:
  links or tonal/outline buttons
- Feedback:
  inline error states first, modal/toast only for global transitions

## Typical Sections

- Login:
  email/phone + password + remember me + forgot password
- Register:
  name + email/phone + password + confirm + consent checkbox
- Reset:
  single contact field + submit + success state

## Practical Rules

- Keep auth width narrow with `max-w-*`.
- Prefer one dominant CTA per screen.
- Keep validation messages close to the field.
- Use modal/toast only for transitions like “check your email” or “session expired”.
- If a quick starter is enough, generate:
  `scripts/generate_page_scaffold.py --type auth --snippet-only`
