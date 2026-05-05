# SF5 Scenario: Profile And Settings

Use this scenario for account settings, personal data, preferences, notification controls, avatar management, and save flows.

## Build From

- `references/page-recipe-profile.md`
- `references/pattern-forms-inputs.md`
- `references/pattern-upload-and-progress.md`
- `references/pattern-pagination-filters.md`
- `references/pattern-feedback-overlays.md`
- `source/simai/ui-play/examples/smart-components/file-upload/element/index.html`
- `source/simai/ui-play/examples/components/toggle/default/index.html`

## Default Screen Structure

1. Profile header
2. Identity block
3. Contact/security block
4. Preferences block
5. Avatar/upload block
6. Save/discard actions

## Recommended Composition

- Identity/contact:
  inputs and textarea where needed
- Preferences:
  toggles, tags, or checkboxes
- Avatar:
  file upload block with current preview and replacement action
- Save feedback:
  toast for success, inline error or modal for conflict/critical failure

## Practical Rules

- Separate personal data from preferences.
- Use toggles only for true binary settings.
- Keep save/discard actions visible and predictable.
- Prefer compact upload zones inside the profile card, not full-page dropzones.
- If a quick starter is enough, generate:
  `scripts/generate_page_scaffold.py --type profile --snippet-only`
