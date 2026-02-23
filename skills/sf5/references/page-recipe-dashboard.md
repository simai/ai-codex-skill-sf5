# SF5 Recipe: Dashboard Page

## Goal

Build data-heavy workspace with sidebar navigation, KPI cards, charts, and activity list.

## Section Order

1. Top bar
2. Sidebar + main workspace
3. KPI row
4. Chart widgets
5. Recent activity table/list

## Base Layout Skeleton

```html
<main class="theme-light min-h-screen bg-surface-0">
  <header class="container md:container p-y-2 border-bottom-1 border-outline-variant">
    <div class="flex items-cross-center content-main-between gap-2">
      <h1 class="title-3">Dashboard</h1>
      <div class="flex gap-1">
        <button class="border border-outline p-x-1 p-y-1 radius-1/3">Filter</button>
        <button class="bg-primary color-on-primary p-x-1 p-y-1 radius-1/3">Create</button>
      </div>
    </div>
  </header>

  <section class="container md:container p-y-3">
    <div class="lg:flex gap-3">
      <aside class="bg-surface-1 border border-outline-variant p-2 radius-1/3">
        <nav class="flex lg:block gap-1">
          <a class="block p-1 radius-1/3 bg-primary-container" href="#">Overview</a>
          <a class="block p-1 radius-1/3 hover:bg-surface-2" href="#">Sales</a>
          <a class="block p-1 radius-1/3 hover:bg-surface-2" href="#">Users</a>
        </nav>
      </aside>

      <div class="flex-1 m-top-2 lg:m-top-0">
        <div class="grid grid-col-1 sm:grid-col-2 xl:grid-col-4 gap-2">
          <article class="bg-surface-1 border border-outline-variant p-2 radius-1/3">
            <p class="text-small">Revenue</p>
            <p class="title-3 m-top-1">$120k</p>
          </article>
          <article class="bg-surface-1 border border-outline-variant p-2 radius-1/3">
            <p class="text-small">Orders</p>
            <p class="title-3 m-top-1">1,240</p>
          </article>
        </div>

        <div class="grid grid-col-1 xl:grid-col-2 gap-2 m-top-2">
          <article class="bg-surface-1 border border-outline-variant p-2 radius-1/3 h-g7">Chart A</article>
          <article class="bg-surface-1 border border-outline-variant p-2 radius-1/3 h-g7">Chart B</article>
        </div>

        <article class="bg-surface-1 border border-outline-variant p-2 radius-1/3 m-top-2">
          <h2 class="title-5">Recent activity</h2>
          <div class="overflow-auto m-top-1">
            <table class="w-full">
              <tr><td class="p-1">09:12</td><td class="p-1">Order created</td></tr>
              <tr><td class="p-1">09:04</td><td class="p-1">Payment confirmed</td></tr>
            </table>
          </div>
        </article>
      </div>
    </div>
  </section>
</main>
```

## Responsive Strategy

- Mobile:
  sidebar collapses to horizontal nav.
- Desktop:
  fixed left nav and denser KPI/chart grid.

## Notes

- Keep data fetch and polling logic in smart-components.
- Keep widgets presentational and reusable.
