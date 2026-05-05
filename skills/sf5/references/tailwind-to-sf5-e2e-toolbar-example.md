# Tailwind to SF5 E2E Example: Toolbar

This example shows the current end-to-end flow for an original Tailwind-inspired toolbar snippet. It is not copied from Tailwind Plus; it is a safe fixture shaped like common Application UI patterns.

## Source Snippet

```html
<nav class="flex flex-row items-center justify-between gap-2 w-full">
  <input class="w-full rounded-lg border px-4 py-2" type="search" placeholder="Search">
  <select class="rounded-lg border px-4 py-2">
    <option>All</option>
  </select>
  <button class="rounded-lg px-4 py-2 font-semibold">Filter</button>
</nav>
```

## Converter Command

```bash
python3 skills/sf5/scripts/convert_tailwind_to_sf5.py \
  --html-string '<nav class="flex flex-row items-center justify-between gap-2 w-full"><input class="w-full rounded-lg border px-4 py-2" type="search" placeholder="Search"><select class="rounded-lg border px-4 py-2"><option>All</option></select><button class="rounded-lg px-4 py-2 font-semibold">Filter</button></nav>' \
  --render-recipe \
  --format text
```

## Converted Draft

The converter maps safe utilities and reports deferred or smart behavior separately:

- `justify-between` -> `content-main-between`
- `rounded-lg` -> `radius-2`
- `px-4` -> `p-inline-start-4 p-inline-end-4`
- `py-2` -> `p-top-2 p-bottom-2`
- `font-semibold` -> `weight-6`
- detected component recipe: `toolbar`
- detected smart hints: `search`, `select`

## Final SF5 Example

Validated final example:

- `references/vendor/tailwind-to-sf5.e2e-toolbar.sf5.html`

Validation:

```bash
python3 skills/sf5/scripts/validate_sf5_html_files.py \
  --strict \
  --catalog-strict \
  skills/sf5/references/vendor/tailwind-to-sf5.e2e-toolbar.sf5.html
```

## Remaining Manual Decisions

- Decide whether search/filter behavior should stay plain controls or use `sf-code="search"` and `sf-code="select"` in the target project.
- Confirm whether filter changes are immediate or submit-based.
- Run visual QA against the concrete project layout.
