# SF5 Product Scenarios

Use this file for common product-level screens assembled from recurring SF5 patterns.

## Scenarios

- `references/scenario-auth.md`
  - sign in, sign up, reset password, compact auth shells
- `references/scenario-catalog-listing.md`
  - search, filter sidebar, cards, tags, pagination, empty results
- `references/scenario-checkout-flow.md`
  - customer form, delivery/payment choices, summary, submit actions
- `references/scenario-profile-settings.md`
  - account forms, preferences, toggles, avatar/upload zones, save feedback
- `references/scenario-dashboard-workspace.md`
  - KPI cards, tables, filters, activity lists, empty states, side actions
- `references/scenario-article-content.md`
  - article hero, TOC, long-form content, related posts, share/back actions

## Usage Rule

- Start from a product scenario when the user asks for a whole feature screen.
- Drop down into pattern playbooks when implementing a section inside that screen.
- Fall back to page recipes when the task is more about broad layout than feature semantics.
- If a starter markup file is needed immediately, use `scripts/generate_page_scaffold.py` with the matching recipe type where available.

## Routing

Use:

```bash
python3 skills/sf5/scripts/recommend_product_scenario.py "profile settings page with avatar upload and notification toggles"
```
