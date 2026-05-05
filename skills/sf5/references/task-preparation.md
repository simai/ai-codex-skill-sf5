# SF5 Task Preparation

Use this helper when you want a prepared working bundle from one request: route, scenario, page recipe, pattern playbooks, and optional starter scaffold.

## CLI

```bash
python3 skills/sf5/scripts/prepare_sf5_task.py \
  "profile settings page with avatar upload and notification toggles" \
  --scaffold-out /tmp/profile-settings.html \
  --theme light
```

JSON mode:

```bash
python3 skills/sf5/scripts/prepare_sf5_task.py \
  "checkout page with customer form, delivery, payment and summary" \
  --format json
```

## What It Does

1. Calls `recommend_sf5_route.py`
2. Reuses the embedded coordinator activity from route output
3. Builds a compact task brief
4. Optionally generates scaffold HTML with `generate_page_scaffold.py`
5. Prints the result or writes it to a file

## Recommended Usage

- Use this when the request is concrete enough to start implementation.
- Use plain `recommend_sf5_route.py` when you only need routing.
- Use `recommend_sf5_activity.py` directly when the task is about coordinator work, validation, source refresh, or skill architecture rather than one page.
- Use `generate_page_scaffold.py` directly when the recipe type is already known.
- Use `--format json` when the result will be consumed by another script, automation, or agent workflow.
