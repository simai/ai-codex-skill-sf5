# UI Doc Atlas Usage

This file describes how to use the exhaustive docs atlas resources.

## Contents

- Atlas Files
- Build/Refresh Atlas
- Query Atlas
- Recommended Retrieval Flow

## Atlas Files

- `references/ui-doc-manifest.json`:
  full machine-readable metadata for all docs pages.
- `references/ui-doc-full-map.md`:
  full grouped list of all markdown pages.
- `references/ui-doc-utility-atlas.md`:
  utility-focused atlas with extracted class tokens and playground markers.
- `references/page-recipe-routing.md`:
  prompt routing to page recipe + required utility groups.

## Build/Refresh Atlas

Run when docs snapshot changes:

```bash
skills/sf5/scripts/build_ui_doc_atlas.py \
  --docs-root '/Users/rim/Downloads/ui-doc-main (2)/ui-doc-main/source/docs/ru' \
  --skill-root /Users/rim/Documents/GitHub/ai-codex-skill-sf5/skills/sf5
```

## Query Atlas

Search relevant pages before implementation:

```bash
skills/sf5/scripts/query_ui_doc_manifest.py \
  --manifest /Users/rim/Documents/GitHub/ai-codex-skill-sf5/skills/sf5/references/ui-doc-manifest.json \
  grid container --top utilities --limit 12
```

Common filters:

- `--top utilities|start|fundamentals|reference|...`
- `--utility-group layout|grid|typography|...`

Route prompt to page recipe:

```bash
skills/sf5/scripts/recommend_page_recipe.py \
  --manifest /Users/rim/Documents/GitHub/ai-codex-skill-sf5/skills/sf5/references/ui-doc-manifest.json \
  'Сверстай checkout: форма клиента, доставка, оплата, summary, валидация'
```

Generate page scaffold from recipe:

```bash
skills/sf5/scripts/generate_page_scaffold.py \
  --type landing --theme light --title "My Landing" --out /tmp/landing.html
```

Generate component/smart/block scaffold:

```bash
skills/sf5/scripts/generate_component_scaffold.py --kind component --name productCard --title "Product card" --snippet-only
skills/sf5/scripts/generate_component_scaffold.py --kind smart --name catalogCards --title "Catalog cards" --smart-code cards --snippet-only
skills/sf5/scripts/generate_component_scaffold.py --kind block --name catalogSection --title "Catalog section" --snippet-only
```

Validate recipe classes against docs manifest:

```bash
skills/sf5/scripts/validate_page_recipes.py --strict
```

Validate strict vendor compatibility:

```bash
skills/sf5/scripts/validate_page_recipes.py --strict --catalog-strict
skills/sf5/scripts/validate_page_recipes.py --strict --catalog-strict --recipes-glob skills/sf5/references/component-template.md
skills/sf5/scripts/validate_page_recipes.py --strict --catalog-strict --recipes-glob skills/sf5/references/smart-component-template.md
skills/sf5/scripts/validate_page_recipes.py --strict --catalog-strict --recipes-glob skills/sf5/references/block-template.md
```

Validate real HTML/PHP templates and generated snippets:

```bash
skills/sf5/scripts/validate_sf5_html_files.py --strict --catalog-strict /tmp/landing.html
skills/sf5/scripts/validate_sf5_html_files.py --strict --catalog-strict \
  --glob "/path/to/templates/**/*.html" \
  --glob "/path/to/templates/**/*.php"
```

Run all local checks in one command:

```bash
skills/sf5/scripts/run_local_checks.sh
```

Install pre-commit hook for automatic SF5 checks:

```bash
skills/sf5/scripts/install_pre_commit_hook.sh
```

## Recommended Retrieval Flow

1. Query manifest by task keywords.
2. For page tasks, route prompt with `recommend_page_recipe.py`.
3. Open top result pages and validate against `project-conventions.md`.
4. Cross-check final class choices in `ui-doc-utility-atlas.md`.
5. Implement and verify with `page-layout-playbook.md`.
