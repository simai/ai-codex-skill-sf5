# SF5 Recipe: Landing Page

## Goal

Build a conversion-oriented page with hero, benefits, social proof, CTA, and footer.

## Section Order

1. Header navigation
2. Hero
3. Benefit cards
4. Feature split sections
5. Testimonials
6. Primary CTA banner
7. Footer

## Base Layout Skeleton

```html
<main class="theme-light">
  <header class="container md:container p-y-2">
    <div class="flex items-cross-center content-main-between gap-2">
      <div class="title-3">Brand</div>
      <nav class="hidden md:flex gap-2">
        <a class="link-underline-none hover:color-primary" href="#">Features</a>
        <a class="link-underline-none hover:color-primary" href="#">Pricing</a>
        <a class="link-underline-none hover:color-primary" href="#">Docs</a>
      </nav>
      <a class="bg-primary color-on-primary p-x-2 p-y-1 radius-1/3" href="#">Start</a>
    </div>
  </header>

  <section class="container md:container p-y-4">
    <div class="grid grid-col-1 md:grid-col-2 gap-3 items-cross-center">
      <div>
        <h1 class="title-3">Main value proposition</h1>
        <p class="text-medium m-top-1">Short supporting message.</p>
        <div class="flex gap-1 m-top-2">
          <a class="bg-primary color-on-primary p-x-2 p-y-1 radius-1/3" href="#">Try now</a>
          <a class="border border-outline p-x-2 p-y-1 radius-1/3" href="#">Learn more</a>
        </div>
      </div>
      <div class="bg-surface-1 radius-1 p-3">Hero visual block</div>
    </div>
  </section>

  <section class="container md:container p-y-4">
    <div class="grid grid-col-1 sm:grid-col-2 lg:grid-col-3 gap-2">
      <article class="bg-surface-1 border border-outline-variant p-2 radius-1/3">Benefit 1</article>
      <article class="bg-surface-1 border border-outline-variant p-2 radius-1/3">Benefit 2</article>
      <article class="bg-surface-1 border border-outline-variant p-2 radius-1/3">Benefit 3</article>
    </div>
  </section>

  <section class="container md:container p-y-4">
    <div class="bg-primary-container color-on-primary-container p-3 radius-1">
      <h2 class="title-3">Call to action</h2>
      <a class="bg-primary color-on-primary p-x-2 p-y-1 radius-1/3 m-top-1 inline-block" href="#">Get started</a>
    </div>
  </section>

  <footer class="container md:container p-y-3 border-top-1 border-outline-variant">
    <div class="flex flex-wrap gap-2 content-main-between">
      <div class="text-small">Copyright</div>
      <div class="flex gap-2">
        <a class="link-underline-none" href="#">Terms</a>
        <a class="link-underline-none" href="#">Privacy</a>
      </div>
    </div>
  </footer>
</main>
```

## Responsive Strategy

- Mobile:
  single-column hero and cards.
- Tablet:
  two-column hero and benefits.
- Desktop:
  three-column benefit grid and expanded nav.

## Notes

- Prefer color roles (`primary`, `surface`, `on-*`) over custom color literals.
- Keep CTA buttons stateful with `hover:` and `focus:` modifiers.
