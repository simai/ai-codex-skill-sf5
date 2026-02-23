# SF5 Template: Smart-Component

Use this snippet as a vendor-safe starter for smart-component integration.

```html
<section class="bg-surface-1 border border-outline-variant p-2 radius-1/3" data-smart="__UNIT_NAME__">
  <header class="flex items-cross-center content-main-between gap-1">
    <h3 class="title-5">__UNIT_TITLE__</h3>
    <button class="border border-outline p-x-1 p-y-1 radius-1/3">Reload</button>
  </header>

  <smart
    name="__UNIT_NAME__"
    sf-code="cards"
    data='{"endpoint":"/api/catalog","method":"GET"}'
    property='{"limit":6}'
    events='{"ready":"onReady"}'
    modify='{"theme":"light"}'
  ></smart>

  <div class="m-top-2 grid grid-col-1 sm:grid-col-2 gap-2">
    <article class="bg-surface-2 p-2 radius-1/3 text-medium">Template placeholder item</article>
  </div>
</section>
```

## Notes

- `sf-code="cards"` is a valid default from vendor smart-code registry.
- Replace endpoint/events with project-specific contracts.
