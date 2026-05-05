# SF5 Scenario: Checkout Flow

Use this scenario for order placement, multi-section customer forms, delivery/payment choice, promo codes, and summary panels.

## Build From

- `references/page-recipe-checkout.md`
- `references/pattern-forms-inputs.md`
- `references/pattern-dropdown-selection.md`
- `references/pattern-feedback-overlays.md`
- `references/pattern-pagination-filters.md`

## Default Screen Structure

1. Checkout header
2. Customer info block
3. Delivery block
4. Payment block
5. Summary sidebar/card
6. Submit + legal/consent note

## Recommended Composition

- Fields:
  use consistent input mode across the flow
- Delivery/payment:
  radio, dropdown, tags, or toggle controls depending on complexity
- Summary:
  static card with item rows, subtotals, total, promo line
- Submit:
  one dominant primary action, one safe secondary action
- Feedback:
  inline field errors first, modal/toast for confirmation or failure summary

## Practical Rules

- Keep summary separate from form logic.
- Use a stable vertical rhythm between blocks.
- Do not overload the payment block with unrelated upsells.
- Keep the summary below the form on mobile.
