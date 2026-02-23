# SF5 Recipe: Checkout Page

## Goal

Build two-column checkout with form, delivery/payment steps, and order summary.

## Section Order

1. Checkout header
2. Customer form
3. Delivery and payment blocks
4. Sticky order summary
5. Submit and legal notes

## Base Layout Skeleton

```html
<main class="theme-light bg-surface-0 min-h-screen">
  <section class="container md:container p-y-3">
    <h1 class="title-3">Checkout</h1>
  </section>

  <section class="container md:container p-bottom-4">
    <div class="lg:flex gap-3">
      <form class="flex-1">
        <div class="bg-surface-1 border border-outline-variant p-2 radius-1/3">
          <h2 class="title-5">Customer info</h2>
          <div class="grid grid-col-1 md:grid-col-2 gap-1 m-top-1">
            <input class="border border-outline p-1 radius-1/3" placeholder="First name" />
            <input class="border border-outline p-1 radius-1/3" placeholder="Last name" />
            <input class="border border-outline p-1 radius-1/3" placeholder="Email" />
          </div>
        </div>

        <div class="bg-surface-1 border border-outline-variant p-2 radius-1/3 m-top-2">
          <h2 class="title-5">Delivery</h2>
          <label class="flex gap-1 m-top-1"><input type="radio" name="delivery" /> Standard</label>
          <label class="flex gap-1 m-top-1"><input type="radio" name="delivery" /> Express</label>
        </div>

        <div class="bg-surface-1 border border-outline-variant p-2 radius-1/3 m-top-2">
          <h2 class="title-5">Payment</h2>
          <label class="flex gap-1 m-top-1"><input type="radio" name="payment" /> Card</label>
          <label class="flex gap-1 m-top-1"><input type="radio" name="payment" /> Invoice</label>
        </div>

        <div class="flex gap-1 m-top-2">
          <button class="bg-primary color-on-primary p-x-2 p-y-1 radius-1/3">Place order</button>
          <a class="border border-outline p-x-2 p-y-1 radius-1/3" href="#">Back to cart</a>
        </div>
      </form>

      <aside class="m-top-2 lg:m-top-0">
        <div class="bg-surface-1 border border-outline-variant p-2 radius-1/3">
          <h2 class="title-5">Summary</h2>
          <div class="m-top-1 flex content-main-between"><span>Items</span><span>$120</span></div>
          <div class="m-top-1 flex content-main-between"><span>Delivery</span><span>$10</span></div>
          <div class="m-top-1 border-top-1 border-outline-variant p-top-1 flex content-main-between">
            <strong>Total</strong><strong>$130</strong>
          </div>
        </div>
      </aside>
    </div>
  </section>
</main>
```

## Responsive Strategy

- Mobile:
  summary appears below form.
- Desktop:
  two-column flow with fixed-width summary block.

## Notes

- Keep validation state styles mapped to role colors (`error`, `warning`, `success` as available per target version).
- Keep checkout state transitions in smart-components, not presentational form fields.
