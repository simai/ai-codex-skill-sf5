# SF5 Pattern Playbooks

Use this file as the entry point for recurring UI tasks that should map quickly to known SF5 markup and smart-component flows.

## When To Use

- The user wants a common UI pattern, not a full custom architecture pass.
- You need a fast answer to "static or smart?" for a typical SF5 feature.
- You want to start from real upstream examples instead of inventing markup.

## Playbooks

- `references/pattern-forms-inputs.md`
  - text inputs, textarea, mask, validation, disabled states
- `references/pattern-dropdown-selection.md`
  - select/tag dropdowns, list items, multiple selection, search/select flows
- `references/pattern-feedback-overlays.md`
  - modal, toast, tooltip, button-triggered feedback and overlays
- `references/pattern-pagination-filters.md`
  - page navigation, list paging, range filters, toggles, tag-based controls
- `references/pattern-upload-and-progress.md`
  - file upload, progress surfaces, range sliders, upload status blocks
- `references/pattern-routing.md`
  - quick routing rules and CLI helper for choosing the right playbook

## Fast Choice Rules

- Use static components when the task is mostly presentational and server-rendered markup is enough.
- Use smart-components when the feature needs instance API, dynamic insertion, event hooks, or a cleaner custom-element authoring model.
- Use utilities first for layout, spacing, typography, and responsive behavior around the component.

## Source Priority

1. `source/simai/ui-play/examples/components/*`
2. `source/simai/ui-play/examples/smart-components/*`
3. `source/simai/ui/distr/component/*`
4. `source/simai/ui-smart/smart/*`
5. `source/simai/ui-doc/source/docs/ru/start/loader/*` for loader semantics

## Validation Rule

After adapting a pattern, validate the final snippet with:

```bash
python3 skills/sf5/scripts/validate_sf5_html_files.py --strict --catalog-strict /tmp/example.html
```
