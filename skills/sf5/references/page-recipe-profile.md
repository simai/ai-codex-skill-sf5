# SF5 Recipe: Profile Settings Page

## Goal

Build a profile/settings page with identity fields, preferences, avatar/upload zone, and explicit save/discard actions.

## Section Order

1. Profile header
2. Personal info block
3. Security/contact block
4. Preferences block
5. Avatar/upload block
6. Save/discard actions

## Base Layout Skeleton

```html
<main class="theme-light min-h-screen bg-surface-0">
  <section class="container md:container p-y-3">
    <div class="flex flex-wrap items-cross-center content-main-between gap-2">
      <div class="flex flex-col gap-1">
        <h1 class="title-3">Profile settings</h1>
        <p class="text-2 color-on-surface-variant">Manage your account, preferences, and notifications.</p>
      </div>
      <div class="flex gap-1">
        <button class="sf-button sf-button--outline sf-button--on-surface sf-button--size-1" type="button">
          <span class="sf-button-text-container">Discard</span>
        </button>
        <button class="sf-button sf-button--default sf-button--primary sf-button--size-1" type="button">
          <span class="sf-button-text-container">Save changes</span>
        </button>
      </div>
    </div>
  </section>

  <section class="container md:container p-bottom-4">
    <div class="grid grid-col-1 xl:grid-col-3 gap-3 content-main-start">
      <div class="xl:col-span-2 flex flex-col gap-3">
        <article class="bg-surface-1 border border-outline-variant radius-1/3 p-2">
          <h2 class="title-5">Personal info</h2>
          <div class="grid grid-col-1 md:grid-col-2 gap-2 m-top-2">
            <sf-input size="1" type="filled" label="First name" name="first_name" placeholder="First name"></sf-input>
            <sf-input size="1" type="filled" label="Last name" name="last_name" placeholder="Last name"></sf-input>
            <sf-input size="1" type="filled" label="Email" name="email" placeholder="you@example.com"></sf-input>
            <sf-input size="1" type="filled" label="Phone" name="phone" placeholder="+33 ..."></sf-input>
          </div>
        </article>

        <article class="bg-surface-1 border border-outline-variant radius-1/3 p-2">
          <h2 class="title-5">Preferences</h2>
          <div class="grid grid-col-1 md:grid-col-2 gap-2 m-top-2">
            <label class="flex items-cross-center gap-1 text-2">
              <input type="checkbox" name="marketing" />
              <span>Marketing emails</span>
            </label>
            <label class="flex items-cross-center gap-1 text-2">
              <input type="checkbox" name="product_updates" checked />
              <span>Product updates</span>
            </label>
          </div>
        </article>
      </div>

      <aside class="bg-surface-1 border border-outline-variant radius-1/3 p-2 flex flex-col gap-2">
        <h2 class="title-5">Avatar</h2>
        <sf-file-upload size="1" accept=".png,.jpg,.jpeg" formats="PNG, JPG up to 2 MB"></sf-file-upload>
      </aside>
    </div>
  </section>
</main>
```

## Responsive Strategy

- Mobile:
  stacked blocks with save actions near the header.
- Desktop:
  two-column settings body with sidebar upload zone.

## Notes

- Keep preferences separate from personal data.
- Prefer toggles only for real binary settings.
- Use toast or inline save feedback depending on project conventions.
