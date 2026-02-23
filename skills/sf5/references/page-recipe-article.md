# SF5 Recipe: Article Page

## Goal

Build long-form content page with hero, TOC, article body, inline callouts, and related content.

## Section Order

1. Header
2. Article hero
3. TOC + content columns
4. Related content
5. Footer

## Base Layout Skeleton

```html
<main class="theme-light">
  <header class="container md:container p-y-2 border-bottom-1 border-outline-variant">
    <div class="flex content-main-between items-cross-center">
      <a class="link-underline-none" href="#">Back</a>
      <a class="link-underline-none" href="#">Share</a>
    </div>
  </header>

  <section class="container md:container p-y-3">
    <p class="text-small color-secondary">Category</p>
    <h1 class="title-3 m-top-1">Article title</h1>
    <p class="text-medium m-top-1">Lead paragraph that summarizes the topic.</p>
  </section>

  <section class="container md:container p-bottom-4">
    <div class="lg:flex gap-3">
      <aside class="bg-surface-1 border border-outline-variant p-2 radius-1/3">
        <p class="title-5">Contents</p>
        <a class="block m-top-1 link-underline-none" href="#s1">Section 1</a>
        <a class="block m-top-1 link-underline-none" href="#s2">Section 2</a>
        <a class="block m-top-1 link-underline-none" href="#s3">Section 3</a>
      </aside>

      <article class="flex-1 m-top-2 lg:m-top-0">
        <div class="bg-surface-1 border border-outline-variant p-3 radius-1/3">
          <h2 id="s1" class="title-5">Section 1</h2>
          <p class="text-medium m-top-1">Main paragraph text.</p>

          <blockquote class="m-top-2 p-2 bg-primary-container color-on-primary-container radius-1/3">
            Important quote or callout.
          </blockquote>

          <h2 id="s2" class="title-5 m-top-3">Section 2</h2>
          <p class="text-medium m-top-1">More content.</p>

          <h2 id="s3" class="title-5 m-top-3">Section 3</h2>
          <p class="text-medium m-top-1">Closing content.</p>
        </div>
      </article>
    </div>
  </section>

  <section class="container md:container p-bottom-4">
    <h2 class="title-5">Related</h2>
    <div class="grid grid-col-1 sm:grid-col-2 lg:grid-col-3 gap-2 m-top-1">
      <article class="bg-surface-1 border border-outline-variant p-2 radius-1/3">Related item</article>
      <article class="bg-surface-1 border border-outline-variant p-2 radius-1/3">Related item</article>
      <article class="bg-surface-1 border border-outline-variant p-2 radius-1/3">Related item</article>
    </div>
  </section>
</main>
```

## Responsive Strategy

- Mobile:
  TOC appears before article body.
- Desktop:
  sticky-style sidebar behavior can be added by position utilities.

## Notes

- Keep article semantics (`article`, headings, lists) clean for SEO/accessibility.
- Use typography and text-formatting utilities as default source of styling.
