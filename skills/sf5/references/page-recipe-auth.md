# SF5 Recipe: Auth Page

## Goal

Build a compact authentication page for login, registration, or password reset with clear primary action and inline validation.

## Section Order

1. Brand/header strip
2. Auth card
3. Primary fields
4. Secondary actions
5. Legal/help links

## Base Layout Skeleton

```html
<main class="theme-light min-h-screen bg-surface-0">
  <section class="container md:container p-y-3">
    <div class="flex items-cross-center content-main-between gap-2">
      <a class="link-underline-none title-5" href="#">Brand</a>
      <a class="text-2 link-underline-none hover:color-primary" href="#">Help</a>
    </div>
  </section>

  <section class="container md:container p-bottom-4">
    <div class="flex content-main-center">
      <div class="w-full max-w-sm bg-surface-1 border border-outline-variant radius-1 p-3">
        <div class="flex flex-col gap-1">
          <h1 class="title-3">Sign in</h1>
          <p class="text-2 color-on-surface-variant">
            Use your email and password to continue.
          </p>
        </div>

        <form class="flex flex-col gap-2 m-top-3">
          <sf-input
            size="1"
            type="filled"
            label="Email"
            name="email"
            placeholder="you@example.com"
            left-icon="mail"
          ></sf-input>

          <sf-input
            size="1"
            type="filled"
            label="Password"
            name="password"
            placeholder="Password"
            left-icon="lock"
          ></sf-input>

          <div class="flex items-cross-center content-main-between gap-2">
            <label class="flex items-cross-center gap-1 text-2">
              <input name="remember" type="checkbox" />
              <span>Remember me</span>
            </label>
            <a class="text-2 link-underline-none hover:color-primary" href="#">Forgot password?</a>
          </div>

          <button class="sf-button sf-button--default sf-button--primary sf-button--size-1" type="submit">
            <span class="sf-button-text-container">Continue</span>
          </button>
        </form>

        <div class="flex flex-col gap-1 m-top-2">
          <button class="sf-button sf-button--outline sf-button--on-surface sf-button--size-1" type="button">
            <span class="sf-button-text-container">Create account</span>
          </button>
          <p class="text-1/2 color-on-surface-variant">
            By continuing, you agree to the Terms and Privacy Policy.
          </p>
        </div>
      </div>
    </div>
  </section>
</main>
```

## Responsive Strategy

- Mobile:
  single centered auth card.
- Desktop:
  same centered auth card with larger breathing space.

## Notes

- Prefer one dominant primary action.
- Keep validation inline and close to fields.
- Reuse smart input components when the project prefers custom-element authoring.
