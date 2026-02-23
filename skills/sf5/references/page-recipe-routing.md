# SF5 Page Recipe Routing

Use this routing table to map user prompts to page recipes and required utility groups.

## Landing

- Trigger keywords:
  landing, лендинг, hero, cta, презентация, promo.
- Recipe:
  `references/page-recipe-landing.md`
- Required utility groups:
  `layout`, `grid`, `typography`, `background`, `border`, `indents`, `interactivity`.

## Catalog

- Trigger keywords:
  catalog, каталог, listing, карточки, фильтры, сортировка, пагинация.
- Recipe:
  `references/page-recipe-catalog.md`
- Required utility groups:
  `layout`, `grid`, `forms`, `indents`, `border`, `typography`, `interactivity`.

## Dashboard

- Trigger keywords:
  dashboard, дашборд, kpi, метрики, таблица, widgets, admin.
- Recipe:
  `references/page-recipe-dashboard.md`
- Required utility groups:
  `layout`, `grid`, `tables`, `typography`, `interactivity`, `border`, `indents`.

## Article

- Trigger keywords:
  article, статья, blog, контент, оглавление, longform.
- Recipe:
  `references/page-recipe-article.md`
- Required utility groups:
  `layout`, `typography`, `text-formatting`, `links`, `indents`, `border`.

## Checkout

- Trigger keywords:
  checkout, чекаут, корзина, order, доставка, оплата, форма.
- Recipe:
  `references/page-recipe-checkout.md`
- Required utility groups:
  `layout`, `grid`, `forms`, `border`, `outline`, `interactivity`, `typography`.

## Fallback

- If no route matches:
  start from `references/page-layout-playbook.md`,
  then choose closest recipe from `references/page-recipes-index.md`.
