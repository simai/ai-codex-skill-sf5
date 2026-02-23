# SF5 Recipe: Catalog Page

## Goal

Build product/content listing with filters, sorting, cards, and pagination.

## Section Order

1. Header with search and sort
2. Filter sidebar
3. Product grid
4. Pagination or load-more

## Base Layout Skeleton

```html
<main class="theme-light">
  <section class="container md:container p-y-3">
    <div class="flex flex-wrap gap-2 items-cross-center content-main-between">
      <h1 class="title-3">Catalog</h1>
      <div class="flex gap-1">
        <input class="border border-outline p-x-1 p-y-1 radius-1/3" placeholder="Search" />
        <select class="border border-outline p-x-1 p-y-1 radius-1/3">
          <option>Popular</option>
          <option>Price</option>
          <option>Newest</option>
        </select>
      </div>
    </div>
  </section>

  <section class="container md:container p-bottom-4">
    <div class="lg:flex gap-3">
      <aside class="bg-surface-1 border border-outline-variant p-2 radius-1/3">
        <h2 class="title-5">Filters</h2>
        <div class="m-top-2 space-y-1">
          <label class="flex gap-1"><input type="checkbox" /> In stock</label>
          <label class="flex gap-1"><input type="checkbox" /> New</label>
          <label class="flex gap-1"><input type="checkbox" /> Discount</label>
        </div>
      </aside>

      <div class="flex-1 m-top-2 lg:m-top-0">
        <div class="grid grid-col-1 sm:grid-col-2 xl:grid-col-3 gap-2">
          <article class="bg-surface-1 border border-outline-variant p-2 radius-1/3">
            <div class="bg-surface-2 radius-1/3 p-2">Image</div>
            <h3 class="title-5 m-top-1">Item name</h3>
            <p class="text-medium">Short description.</p>
            <div class="flex items-cross-center content-main-between m-top-1">
              <span class="title-5">$99</span>
              <button class="bg-primary color-on-primary p-x-1 p-y-1 radius-1/3">Add</button>
            </div>
          </article>
        </div>

        <div class="flex content-main-center gap-1 m-top-3">
          <button class="border border-outline p-x-1 p-y-1 radius-1/3">Prev</button>
          <button class="bg-primary color-on-primary p-x-1 p-y-1 radius-1/3">1</button>
          <button class="border border-outline p-x-1 p-y-1 radius-1/3">2</button>
          <button class="border border-outline p-x-1 p-y-1 radius-1/3">Next</button>
        </div>
      </div>
    </div>
  </section>
</main>
```

## Responsive Strategy

- Mobile:
  filters collapse above grid.
- Desktop:
  fixed sidebar + multi-column cards.

## Notes

- If filters are dynamic, wire them through a smart-component and keep card markup in presentational components.
- Keep card grid based on `grid-col-*` and `gap-*` utilities.
