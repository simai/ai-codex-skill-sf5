# SF5 Pattern Routing

Use this file when the user request is a recurring UI task and you need to route quickly to the most relevant playbook.

## Routing Rules

- Forms, validation, masks, textarea, text fields, country code:
  `references/pattern-forms-inputs.md`
- Select, dropdown, picker, list-item, tag selection, page-size chooser:
  `references/pattern-dropdown-selection.md`
- Modal, dialog, tooltip, toast, overlay, button-triggered feedback:
  `references/pattern-feedback-overlays.md`
- Pagination, filters, chips, tags, toggle, range selector:
  `references/pattern-pagination-filters.md`
- Upload, drag-and-drop, progress, upload error, file status, range control:
  `references/pattern-upload-and-progress.md`

## Escalation Rules

- If the task spans several playbooks, start from the dominant interaction:
  - input-heavy flow -> forms
  - choice-heavy flow -> dropdown/selection
  - feedback-heavy flow -> overlays
  - list/results flow -> pagination/filters
  - file/value transfer flow -> upload/progress
- If the task becomes a full page or multi-block feature, switch to:
  `references/page-layout-playbook.md`

## CLI Helper

Use:

```bash
python3 skills/sf5/scripts/recommend_ui_pattern.py "checkout form with validation, country code, dropdown city, submit modal"
```
