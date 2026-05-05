# SF5 Recipe: Catalog Empty State Page

## Goal

Build a catalog/listing page variant focused on no-results or empty-state UX with filters and reset actions.

## Section Order

1. Header with search and sort
2. Filter summary row
3. Empty results card
4. Recovery actions

## Base Layout Skeleton

```html
<main class="theme-light">
  <section class="container md:container p-y-3">
    <div class="flex flex-wrap gap-2 items-cross-center content-main-between">
      <div class="flex flex-col gap-1">
        <h1 class="title-3">Catalog</h1>
        <p class="text-2 color-on-surface-variant">0 matching items for the current filters.</p>
      </div>
      <div class="flex flex-wrap gap-1">
        <sf-input size="1" type="filled" label="Search" name="search" placeholder="Search"></sf-input>
        <sf-dropdown size="1" type="outlined" mode="select" label="Sort">
          <sf-list-item type="text" size="1" text="Popular" selected></sf-list-item>
          <sf-list-item type="text" size="1" text="Newest"></sf-list-item>
        </sf-dropdown>
      </div>
    </div>
  </section>

  <section class="container md:container p-bottom-4">
    <div class="flex flex-wrap gap-1 m-bottom-2">
      <div class="border border-outline-variant radius-1/3 p-x-1 p-y-1 text-2 flex items-cross-center gap-1">
        <i class="sf-icon">tune</i>
        <span>Category</span>
      </div>
      <div class="border border-outline-variant radius-1/3 p-x-1 p-y-1 text-2 flex items-cross-center gap-1">
        <span>Price</span>
        <span class="color-on-surface-variant">1</span>
      </div>
    </div>

    <div class="bg-surface-1 border border-outline-variant radius-1 p-4 text-center">
      <div class="flex content-main-center">
        <div class="bg-surface-container p-2 radius-2 border border-outline-variant">
          <div class="title-5">No results found</div>
          <p class="text-2 color-on-surface-variant m-top-1">
            Try clearing filters or broadening your search criteria.
          </p>
          <div class="flex flex-wrap gap-1 content-main-center m-top-2">
            <button class="sf-button sf-button--default sf-button--primary sf-button--size-1" type="button">
              <span class="sf-button-text-container">Clear filters</span>
            </button>
            <button class="sf-button sf-button--outline sf-button--on-surface sf-button--size-1" type="button">
              <span class="sf-button-text-container">Back to popular items</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>
</main>
```

## Responsive Strategy

- Mobile:
  search/sort stack above the empty card.
- Desktop:
  search/sort stay inline and empty card remains centered.

## Notes

- Prefer active filter feedback above the empty state.
- Keep recovery actions explicit and low-friction.
