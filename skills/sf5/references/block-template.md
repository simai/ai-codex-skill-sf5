# SF5 Template: Block

Use this snippet as a vendor-safe starter for feature/page block composition.

```html
<section class="container md:container p-y-3" data-block="__UNIT_NAME__">
  <header class="flex items-cross-center content-main-between gap-2">
    <h2 class="title-3">__UNIT_TITLE__</h2>
    <a class="link-underline-none text-small hover:color-primary" href="#">View all</a>
  </header>

  <div class="lg:flex gap-3 m-top-2">
    <aside class="bg-surface-1 border border-outline-variant p-2 radius-1/3">
      <h3 class="title-5">Filters</h3>
      <label class="flex gap-1 m-top-1"><input type="checkbox" /> New</label>
      <label class="flex gap-1 m-top-1"><input type="checkbox" /> In stock</label>
    </aside>

    <div class="flex-1 m-top-2 lg:m-top-0">
      <div class="grid grid-col-1 sm:grid-col-2 xl:grid-col-3 gap-2">
        <article class="bg-surface-1 border border-outline-variant p-2 radius-1/3">
          <h4 class="title-5">Item</h4>
          <p class="text-medium m-top-1">Short description.</p>
        </article>
      </div>
    </div>
  </div>
</section>
```

## Notes

- Keep block contracts explicit (inputs/outputs/events).
- Compose from components and smart-components; avoid duplicated business logic.
