# SF5 Template: Component

Use this snippet as a vendor-safe starter for presentational components.

```html
<article class="bg-surface-1 border border-outline-variant p-2 radius-1/3" data-component="__UNIT_NAME__">
  <header class="flex items-cross-center content-main-between gap-1">
    <h3 class="title-5">__UNIT_TITLE__</h3>
    <a class="link-underline-none text-small hover:color-primary" href="#">Action</a>
  </header>
  <p class="text-medium m-top-1">Component body text.</p>
  <footer class="flex items-cross-center content-main-between m-top-2">
    <span class="text-small color-secondary">Meta</span>
    <button class="bg-primary color-on-primary p-x-1 p-y-1 radius-1/3">Open</button>
  </footer>
</article>
```

## Notes

- Keep this layer presentational and stateless.
- Move asynchronous logic and side effects to smart-components.
