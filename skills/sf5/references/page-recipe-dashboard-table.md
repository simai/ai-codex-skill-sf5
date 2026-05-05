# SF5 Recipe: Dashboard Table Page

## Goal

Build a dashboard/workspace page variant centered on KPI cards, action bar, and a primary table surface.

## Section Order

1. Top bar with actions
2. KPI row
3. Table controls
4. Table card
5. Empty or secondary support panel

## Base Layout Skeleton

```html
<main class="theme-light min-h-screen bg-surface-0">
  <section class="container md:container p-y-3 border-bottom-1 border-outline-variant">
    <div class="flex flex-wrap items-cross-center content-main-between gap-2">
      <div class="flex flex-col gap-1">
        <h1 class="title-3">Orders dashboard</h1>
        <p class="text-2 color-on-surface-variant">Monitor activity, review rows, and trigger operator actions.</p>
      </div>
      <div class="flex gap-1">
        <button class="sf-button sf-button--outline sf-button--on-surface sf-button--size-1" type="button">
          <span class="sf-button-text-container">Export</span>
        </button>
        <button class="sf-button sf-button--default sf-button--primary sf-button--size-1" type="button">
          <span class="sf-button-text-container">Create order</span>
        </button>
      </div>
    </div>
  </section>

  <section class="container md:container p-y-3">
    <div class="grid grid-col-1 sm:grid-col-2 xl:grid-col-4 gap-2">
      <article class="bg-surface-1 border border-outline-variant p-2 radius-1/3">
        <p class="text-1/2 color-on-surface-variant">Revenue</p>
        <p class="title-3 m-top-1">$120k</p>
      </article>
      <article class="bg-surface-1 border border-outline-variant p-2 radius-1/3">
        <p class="text-1/2 color-on-surface-variant">Open orders</p>
        <p class="title-3 m-top-1">124</p>
      </article>
      <article class="bg-surface-1 border border-outline-variant p-2 radius-1/3">
        <p class="text-1/2 color-on-surface-variant">Delayed</p>
        <p class="title-3 m-top-1">8</p>
      </article>
      <article class="bg-surface-1 border border-outline-variant p-2 radius-1/3">
        <p class="text-1/2 color-on-surface-variant">Resolved today</p>
        <p class="title-3 m-top-1">32</p>
      </article>
    </div>

    <div class="flex flex-wrap gap-1 items-cross-center content-main-between m-top-3">
      <div class="flex flex-wrap gap-1">
        <sf-dropdown size="1" type="outlined" mode="select" label="Status">
          <sf-list-item type="text" size="1" text="All" selected></sf-list-item>
          <sf-list-item type="text" size="1" text="Open"></sf-list-item>
        </sf-dropdown>
        <sf-dropdown size="1" type="outlined" mode="select" label="Assignee">
          <sf-list-item type="text" size="1" text="Everyone" selected></sf-list-item>
          <sf-list-item type="text" size="1" text="My team"></sf-list-item>
        </sf-dropdown>
      </div>
      <button class="sf-button sf-button--outline sf-button--on-surface sf-button--size-1" type="button">
        <span class="sf-button-text-container">Reset filters</span>
      </button>
    </div>

    <article class="bg-surface-1 border border-outline-variant radius-1/3 p-2 m-top-2">
      <div class="overflow-auto">
        <table class="table">
          <thead>
            <tr>
              <th>Order</th>
              <th>Status</th>
              <th>Owner</th>
              <th>Updated</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>#1042</td>
              <td>Open</td>
              <td>A. Miller</td>
              <td>09:12</td>
            </tr>
            <tr>
              <td>#1041</td>
              <td>Delayed</td>
              <td>N. Banks</td>
              <td>08:45</td>
            </tr>
          </tbody>
        </table>
      </div>
    </article>
  </section>
</main>
```

## Responsive Strategy

- Mobile:
  KPI cards stack and the table stays inside horizontal overflow.
- Desktop:
  KPI cards spread across the row and filters stay inline above the table.

## Notes

- Keep the table as the primary workspace surface.
- Prefer explicit filters and one dominant primary action.
