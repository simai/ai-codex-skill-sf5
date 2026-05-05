#!/usr/bin/env python3
"""
Generate ignored TailAdmin page conversion examples.

The source project is expected under output/external-tailwind-projects and is
used as MIT-licensed input material. This script does not install dependencies
or execute the external project.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import subprocess
import sys
from pathlib import Path
from textwrap import dedent

from run_tailwind_conversion_lab import LAB_CSS, run_json_optional, write_text


def skill_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def repo_root_from_skill_root(skill_root: Path) -> Path:
    return skill_root.parents[1]


TAILADMIN_SOURCE_SNIPPETS = {
    "signin": {
        "sourceFile": "src/signin.html",
        "title": "TailAdmin signin page",
        "sourceMarkup": """
        <main class="min-h-screen bg-white px-6 py-12">
          <section class="mx-auto flex max-w-md flex-col justify-center gap-6">
            <a class="inline-flex items-center text-sm text-gray-500 hover:text-gray-700" href="index.html">Back to dashboard</a>
            <header class="space-y-2">
              <h1 class="text-2xl font-semibold tracking-tight text-gray-800">Sign In</h1>
              <p class="text-sm text-gray-500">Enter your email and password to sign in!</p>
            </header>
            <div class="grid grid-cols-1 gap-3 sm:grid-cols-2 sm:gap-5">
              <button class="inline-flex items-center justify-center gap-3 rounded-lg bg-gray-100 px-7 py-3 text-sm font-medium text-gray-700 hover:bg-gray-100 hover:text-gray-800">Sign in with Google</button>
              <button class="inline-flex items-center justify-center gap-3 rounded-lg bg-gray-100 px-7 py-3 text-sm font-medium text-gray-700 hover:bg-gray-100 hover:text-gray-800">Sign in with X</button>
            </div>
            <div class="relative py-3">
              <div class="border-t border-gray-200"></div>
              <p class="text-center text-sm text-gray-500">Or</p>
            </div>
            <form class="space-y-5">
              <label class="block text-sm font-medium text-gray-700">Email</label>
              <input class="h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:ring-3 focus:ring-brand-500/10" type="email" placeholder="info@gmail.com">
              <label class="block text-sm font-medium text-gray-700">Password</label>
              <input class="h-11 w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 text-sm text-gray-800 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:ring-3 focus:ring-brand-500/10" type="password" placeholder="Enter your password">
              <button class="inline-flex w-full items-center justify-center rounded-lg bg-brand-500 px-4 py-3 text-sm font-semibold text-white hover:bg-brand-600" type="submit">Sign in</button>
            </form>
          </section>
        </main>
        """,
        "sf5Markup": """
        <main class="theme-light min-h-screen bg-surface-0">
          <section class="container md:container p-y-8">
            <div class="flex content-main-center">
              <article class="w-full max-w-md bg-surface-1 border border-outline-variant radius-1 p-6 shadow-1">
                <a class="inline-flex items-center text-2 color-on-surface-variant hover:color-on-surface" href="index.html">Back to dashboard</a>
                <header class="flex flex-col gap-2 m-top-3">
                  <h1 class="title-3 color-on-surface tracking-tight">Sign In</h1>
                  <p class="text-2 color-on-surface-variant">Enter your email and password to sign in!</p>
                </header>
                <div class="grid gap-3 m-top-3">
                  <button class="sf-button sf-button--outline sf-button--on-surface sf-button--size-1" type="button"><span class="sf-button-text-container">Sign in with Google</span></button>
                  <button class="sf-button sf-button--outline sf-button--on-surface sf-button--size-1" type="button"><span class="sf-button-text-container">Sign in with X</span></button>
                </div>
                <div class="p-y-3">
                  <div class="border-top-1 border-outline-variant"></div>
                  <p class="text-center text-2 color-on-surface-variant">Or</p>
                </div>
                <form class="flex flex-col gap-2">
                  <label class="text-2 color-on-surface">Email</label>
                  <input class="w-full radius-1 border border-outline bg-transparent p-inline-start-4 p-inline-end-4 p-y-2 text-2 color-on-surface shadow-1 placeholder-on-surface-variant focus:border-primary focus:ring-3 focus:ring-primary" type="email" placeholder="info@gmail.com">
                  <label class="text-2 color-on-surface">Password</label>
                  <input class="w-full radius-1 border border-outline bg-transparent p-inline-start-4 p-inline-end-4 p-y-2 text-2 color-on-surface shadow-1 placeholder-on-surface-variant focus:border-primary focus:ring-3 focus:ring-primary" type="password" placeholder="Enter your password">
                  <button class="sf-button sf-button--default sf-button--primary sf-button--size-1 w-full" type="submit"><span class="sf-button-text-container">Sign in</span></button>
                </form>
              </article>
            </div>
          </section>
        </main>
        """,
        "componentizedMarkup": """
        <main class="theme-light min-h-screen bg-surface-0">
          <section class="container md:container p-y-8">
            <div class="flex content-main-center">
              <article class="w-full max-w-md bg-surface-1 border border-outline-variant radius-1 p-6 shadow-1">
                <a class="inline-flex items-center text-2 color-on-surface-variant hover:color-on-surface" href="index.html">Back to dashboard</a>
                <header class="flex flex-col gap-2 m-top-3">
                  <h1 class="title-3 color-on-surface tracking-tight">Sign In</h1>
                  <p class="text-2 color-on-surface-variant">Enter your email and password to sign in!</p>
                </header>
                <div class="grid gap-3 m-top-3">
                  <sf-button size="1" type="outline" scheme="on-surface" text="Sign in with Google"></sf-button>
                  <sf-button size="1" type="outline" scheme="on-surface" text="Sign in with X"></sf-button>
                </div>
                <div class="p-y-3">
                  <div class="border-top-1 border-outline-variant"></div>
                  <p class="text-center text-2 color-on-surface-variant">Or</p>
                </div>
                <form class="flex flex-col gap-2">
                  <sf-input size="1" type="filled" label="Email" name="email" placeholder="info@gmail.com"></sf-input>
                  <sf-input size="1" type="filled" label="Password" name="password" placeholder="Enter your password"></sf-input>
                  <sf-button size="1" type="default" scheme="primary" text="Sign in"></sf-button>
                </form>
              </article>
            </div>
          </section>
        </main>
        """,
    },
    "basic-tables": {
        "sourceFile": "src/basic-tables.html",
        "title": "TailAdmin basic tables page",
        "sourceMarkup": """
        <main class="min-h-screen bg-gray-50 px-6 py-12">
          <section class="mx-auto max-w-md space-y-5">
            <header class="space-y-1">
              <p class="text-sm text-gray-500">Tables</p>
              <h1 class="text-2xl font-semibold text-gray-800">Basic Tables</h1>
            </header>
            <article class="rounded-2xl border border-gray-200 bg-white shadow-theme-xs">
              <header class="border-b border-gray-100 px-5 py-4">
                <h2 class="text-base font-medium text-gray-800">Basic Table 1</h2>
              </header>
              <div class="overflow-x-auto p-5">
                <table class="min-w-full divide-y divide-gray-200 text-left text-sm">
                  <thead>
                    <tr>
                      <th class="px-5 py-3 font-medium text-gray-500" scope="col">Source</th>
                      <th class="px-5 py-3 font-medium text-gray-500" scope="col">Status</th>
                      <th class="px-5 py-3 font-medium text-gray-500" scope="col">Value</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-gray-100">
                    <tr>
                      <td class="px-5 py-3 text-gray-800">TailAdmin</td>
                      <td class="px-5 py-3 text-gray-500">Converted</td>
                      <td class="px-5 py-3 text-gray-800">SF5</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </article>
          </section>
        </main>
        """,
        "sf5Markup": """
        <main class="theme-light min-h-screen bg-surface-0">
          <section class="container md:container p-y-8">
            <div class="flex content-main-center">
              <div class="w-full max-w-md flex flex-col gap-5">
                <header class="flex flex-col gap-1">
                  <p class="text-2 color-on-surface-variant">Tables</p>
                  <h1 class="title-3 color-on-surface">Basic Tables</h1>
                </header>
                <article class="bg-surface-1 border border-outline-variant radius-1/3 shadow-1 overflow-hidden">
                  <header class="border-bottom-1 border-outline-variant p-inline-start-5 p-inline-end-5 p-y-4">
                    <h2 class="text-2 color-on-surface">Basic Table 1</h2>
                  </header>
                  <div class="overflow-auto p-5">
                    <table class="table w-full">
                      <thead>
                        <tr>
                          <th scope="col">Source</th>
                          <th scope="col">Status</th>
                          <th scope="col">Value</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr>
                          <td>TailAdmin</td>
                          <td>Converted</td>
                          <td>SF5</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </article>
              </div>
            </div>
          </section>
        </main>
        """,
        "componentizedMarkup": """
        <main class="theme-light min-h-screen bg-surface-0">
          <section class="container md:container p-y-8">
            <div class="flex content-main-center">
              <div class="w-full max-w-md flex flex-col gap-5">
                <header class="flex flex-col gap-1">
                  <p class="text-2 color-on-surface-variant">Tables</p>
                  <h1 class="title-3 color-on-surface">Basic Tables</h1>
                </header>
                <article class="bg-surface-1 border border-outline-variant radius-1/3 shadow-1 overflow-hidden">
                  <header class="border-bottom-1 border-outline-variant p-inline-start-5 p-inline-end-5 p-y-4">
                    <h2 class="text-2 color-on-surface">Basic Table 1</h2>
                  </header>
                  <div sf-code="table" data="{}" property="{}" events="{}" modify="{}"></div>
                </article>
              </div>
            </div>
          </section>
        </main>
        """,
    },
}


RUNTIME_COMPONENT_PREVIEWS = {
    "dropdown": {
        "title": "SF5 dropdown runtime preview",
        "sourceMarkup": """
        <section class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
          <label class="block text-sm font-medium text-gray-700">Status</label>
          <select class="mt-2 w-full rounded-lg border border-gray-300 px-4 py-2 text-sm">
            <option>Draft</option>
            <option selected>Published</option>
          </select>
        </section>
        """,
        "componentizedMarkup": """
        <section class="theme-light bg-surface-1 border border-outline-variant radius-1 p-4 shadow-1">
          <sf-dropdown size="1" type="outlined" mode="single" label="Status" placeholder="Select status" text="Published"></sf-dropdown>
        </section>
        """,
    },
    "pagination": {
        "title": "SF5 pagination runtime preview",
        "sourcePath": "source/simai/ui-play/examples/components/pagination/default/index.html",
        "sourceLabel": "SF5 ui-play static pagination source",
        "targetLabel": "SF5 smart pagination runtime output",
        "maxRuntimeVisualDelta": 1.0,
        "componentizedMarkup": """
        <section class="theme-light bg-surface-1 border border-outline-variant radius-1 p-4 shadow-1">
          <sf-pagination current="1" total="10"></sf-pagination>
        </section>
        """,
    },
    "modal": {
        "title": "SF5 modal runtime preview",
        "sourceMarkup": """
        <section class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
          <button class="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white" data-modal="demo">Open modal</button>
          <div class="fixed inset-0 z-50 hidden" role="dialog" aria-modal="true">Modal content</div>
        </section>
        """,
        "componentizedMarkup": """
        <section class="theme-light bg-surface-1 border border-outline-variant radius-1 p-4 shadow-1">
          <sf-modal id="modal-demo" display="inline" title="Runtime modal" text="Modal content rendered by SF5 runtime."></sf-modal>
        </section>
        """,
    },
}


PAGE_CSS = LAB_CSS + """
.lab-stage { overflow-x: auto; }
.lab-stage .sf-source-wide,
.lab-stage .sf-runtime-wide { min-width: 960px; }
.bg-brand-500 { background: var(--primary); }
.hover\\:bg-brand-600:hover { background: #2848d9; }
.border-b { border-bottom: 1px solid #e5e7eb; }
.h-11 { min-height: 44px; }
.py-2\\.5 { padding-block: 10px; }
.px-7 { padding-inline: 28px; }
.text-gray-800 { color: #1f2937; }
.shadow-theme-xs { box-shadow: 0 1px 3px rgb(15 23 42 / 9%); }
.focus\\:border-brand-300:focus { border-color: #6f8bff; outline: none; }
.focus\\:ring-3:focus { box-shadow: 0 0 0 3px rgb(51 92 255 / 16%); }
.focus\\:ring-brand-500\\/10:focus { box-shadow: 0 0 0 3px rgb(51 92 255 / 16%); }
.lg\\:w-1\\/2 { width: 50%; }
.sm\\:grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.grid-cols-1 { grid-template-columns: repeat(1, minmax(0, 1fr)); }
"""


PREVIEW_CUSTOM_ELEMENT_CSS = """
sf-button { appearance: none; border: 0; border-radius: 12px; display: inline-flex; align-items: center; justify-content: center; min-height: 42px; padding: 0 18px; font: inherit; font-weight: 700; cursor: pointer; background: var(--primary); color: #fff; }
sf-button[type="outline"] { background: transparent; color: var(--on-surface); border: 1px solid var(--outline); }
sf-button::before { content: attr(text); }
sf-input { display: flex; flex-direction: column; gap: 6px; width: 100%; font: inherit; }
sf-input::before { content: attr(label); color: var(--on-surface); font-size: 14px; font-weight: 500; }
sf-input::after { content: attr(placeholder); display: flex; align-items: center; min-height: 42px; border: 1px solid var(--outline); border-radius: 12px; padding-inline: 16px; color: var(--on-surface-variant); background: transparent; box-shadow: 0 1px 3px rgb(15 23 42 / 9%); }
[sf-code="table"] { display: flex; align-items: center; justify-content: center; min-height: 180px; padding: 24px; color: var(--on-surface-variant); background: repeating-linear-gradient(135deg, #f8fafc 0, #f8fafc 10px, #eef2f7 10px, #eef2f7 20px); }
[sf-code="table"]::before { content: "sf-code=table preview requires SF5 smart runtime"; font-size: 14px; text-align: center; }
"""


def clean(value: str) -> str:
    return dedent(value).strip() + "\n"


def run_json(command: list[str]) -> dict:
    completed = subprocess.run(command, text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr or completed.stdout or "command failed")
    return json.loads(completed.stdout)


SMART_RUNTIME_ASSETS = {
    "sf-button": "source/simai/ui-smart/smart/buttons/js/buttons.js",
    "sf-dropdown": "source/simai/ui-smart/smart/dropdown/js/dropdown.js",
    "sf-input": "source/simai/ui-smart/smart/inputs/js/inputs.js",
    "sf-pagination": "source/simai/ui-smart/smart/pagination/js/pagination.js",
    "sf-modal": "source/simai/ui-smart/smart/modal/js/modal.js",
}

RUNTIME_COMPONENT_CSS_ASSETS = {
    "dropdown": [
        "source/simai/ui/distr/component/dropdown/css/dropdown.css",
        "source/simai/ui/distr/component/buttons/css/buttons.css",
        "source/simai/ui/distr/component/icon-buttons/css/icon-buttons.css",
    ],
    "pagination": [
        "source/simai/ui/distr/component/pagination/css/pagination.css",
        "source/simai/ui/distr/component/buttons/css/buttons.css",
        "source/simai/ui/distr/component/icon-buttons/css/icon-buttons.css",
        "source/simai/ui/distr/component/dropdown/css/dropdown.css",
        "source/simai/ui/distr/component/checkbox/css/checkbox.css",
    ],
    "modal": [
        "source/simai/ui/distr/component/modal/css/modal.css",
        "source/simai/ui/distr/component/buttons/css/buttons.css",
        "source/simai/ui/distr/component/icon-buttons/css/icon-buttons.css",
    ],
}


def runtime_expected_elements(page_id: str) -> list[str]:
    if page_id == "signin":
        return ["sf-button", "sf-input"]
    if page_id == "dropdown":
        return ["sf-dropdown"]
    if page_id == "pagination":
        return ["sf-pagination"]
    if page_id == "modal":
        return ["sf-modal"]
    return []


def runtime_blockers(page_id: str) -> list[str]:
    if page_id == "basic-tables":
        return [
            "sf-code=\"table\" has no concrete source/simai/ui-smart/smart/table runtime artifact in the current source mirror.",
            "Table promotion remains blocked until a real smart table asset and data/property contract are source-backed.",
        ]
    return []


def path_ref(from_dir: Path, target: Path) -> str:
    return os.path.relpath(target.resolve(), from_dir.resolve()).replace(os.sep, "/")


def runtime_probe_script(expected_elements: list[str]) -> str:
    expected_json = json.dumps(expected_elements, ensure_ascii=False)
    return f"""
<script>
(() => {{
  const expected = {expected_json};
  const writeStatus = (status, defined, missing) => {{
    document.documentElement.dataset.sfRuntimeStatus = status;
    document.documentElement.dataset.sfRuntimeDefined = defined.join(",");
    document.documentElement.dataset.sfRuntimeMissing = missing.join(",");
  }};
  if (!expected.length) {{
    writeStatus("not-required", [], []);
    return;
  }}
  const timeout = new Promise((resolve) => window.setTimeout(() => resolve("timeout"), 3000));
  const definitions = Promise.all(expected.map((tag) => customElements.whenDefined(tag))).then(() => "defined");
  Promise.race([definitions, timeout]).then(() => {{
    const defined = expected.filter((tag) => Boolean(customElements.get(tag)));
    const missing = expected.filter((tag) => !customElements.get(tag));
    writeStatus(missing.length ? "partial" : "ok", defined, missing);
  }});
}})();
</script>
"""


def runtime_head_tags(page_id: str, page_root: Path, repo_root: Path) -> str:
    expected = runtime_expected_elements(page_id)
    core_css = repo_root / "source" / "simai" / "ui" / "distr" / "core" / "css" / "core.css"
    tags = [
        f'<script>window.sfPath = "{path_ref(page_root, repo_root / "source" / "simai" / "ui" / "distr")}/"; window.sfSmartPath = "{path_ref(page_root, repo_root / "source" / "simai" / "ui-smart")}";</script>',
    ]
    if core_css.exists():
        tags.append(f'<link rel="stylesheet" href="{path_ref(page_root, core_css)}">')
    for css_ref in RUNTIME_COMPONENT_CSS_ASSETS.get(page_id, []):
        css_asset = repo_root / css_ref
        if css_asset.exists():
            tags.append(f'<link rel="stylesheet" href="{path_ref(page_root, css_asset)}">')
    for tag_name in expected:
        asset = repo_root / SMART_RUNTIME_ASSETS[tag_name]
        if asset.exists():
            tags.append(f'<script src="{path_ref(page_root, asset)}"></script>')
    tags.append(runtime_probe_script(expected))
    return "\n".join(tags)


def runtime_promotion_status(page_id: str, runtime_probe: dict) -> str:
    if runtime_blockers(page_id):
        return "blocked"
    if not runtime_expected_elements(page_id):
        return "not-required"
    if runtime_probe.get("ok") and runtime_probe.get("runtimeStatus") == "ok":
        return "candidate"
    return "blocked"


def runtime_notes(page_id: str, runtime_probe: dict) -> list[str]:
    notes = runtime_blockers(page_id)
    if notes:
        return notes
    if runtime_expected_elements(page_id):
        defined = ", ".join(runtime_probe.get("definedElements", [])) or "none"
        missing = ", ".join(runtime_probe.get("missingElements", [])) or "none"
        notes.append(f"Runtime probe defined: {defined}; missing: {missing}.")
        if runtime_probe.get("ok"):
            notes.append("Custom element promotion is allowed only as a candidate; form behavior still needs SF5 runtime acceptance.")
        else:
            notes.append("Custom element promotion is blocked until the runtime probe reports all expected elements as defined.")
    return notes


def render_page(
    title: str,
    source_markup: str,
    sf5_markup: str,
    conversion: dict,
    target_label: str,
    source_label: str = "TailAdmin source excerpt",
    extra_head: str = "",
    include_preview_css: bool = True,
) -> str:
    summary = conversion.get("report", {}).get("summary", {})
    css = PAGE_CSS + (PREVIEW_CUSTOM_ELEMENT_CSS if include_preview_css else "")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} TailAdmin to SF5</title>
<style>{css}</style>
{extra_head}
</head>
<body>
<main class="lab-page">
  <section class="lab-header">
    <h1>{html.escape(title)}</h1>
    <p>Mapped: {summary.get('mappedCount', 0)}; deferred: {summary.get('deferredCount', 0)}; blocked: {summary.get('blockedCount', 0)}; unmapped: {summary.get('unmappedCount', 0)}.</p>
  </section>
  <div class="lab-grid">
    <article class="lab-panel">
      <h2>{html.escape(source_label)}</h2>
      <div class="lab-stage">{source_markup}</div>
    </article>
    <article class="lab-panel">
      <h2>{html.escape(target_label)}</h2>
      <div class="lab-stage">{sf5_markup}</div>
    </article>
  </div>
</main>
</body>
</html>
"""


def capture_and_score(skill_root: Path, html_path: Path, screenshot_path: Path, score_path: Path) -> tuple[dict, dict]:
    screenshot = run_json_optional(
        [
            sys.executable,
            str(skill_root / "scripts" / "capture_html_screenshot.py"),
            str(html_path),
            "--output",
            str(screenshot_path),
        ]
    )
    visual_score = {}
    if screenshot.get("ok"):
        visual_score = run_json_optional(
            [
                sys.executable,
                str(skill_root / "scripts" / "score_lab_visual.py"),
                str(screenshot_path),
                "--output",
                str(score_path),
            ]
        )
    return screenshot, visual_score


def componentized_notes(page_id: str) -> list[str]:
    if page_id == "basic-tables":
        return [
            "Componentized output uses sf-code=\"table\" as a smart-runtime placeholder.",
            "The visual score is only a layout regression signal here; it does not prove smart table rendering without SF5 runtime hydration.",
        ]
    if page_id == "signin":
        return [
            "Componentized output replaces form controls with sf-input and sf-button preview elements.",
            "Submit/autofill/password-manager behavior must be verified in a real SF5 runtime before replacing native form controls.",
        ]
    return [
        "Componentized output is a source-backed preview and still requires runtime behavior review.",
    ]


def generate_runtime_component_preview(
    skill_root: Path,
    repo_root: Path,
    output_root: Path,
    component_id: str,
    preview: dict[str, str],
) -> dict[str, object]:
    page_root = output_root / "runtime-components" / component_id
    if preview.get("sourcePath"):
        source_path = repo_root / str(preview["sourcePath"])
        source_excerpt = source_path.read_text(encoding="utf-8")
        write_text(page_root / "source-origin.txt", str(preview["sourcePath"]) + "\n")
    else:
        source_excerpt = clean(preview["sourceMarkup"])
    componentized_markup = clean(preview["componentizedMarkup"])
    if component_id == "pagination":
        source_excerpt = f'<div class="sf-source-wide">{source_excerpt}</div>'
        componentized_markup = f'<div class="sf-runtime-wide">{componentized_markup}</div>'
    write_text(page_root / "source-excerpt.html", source_excerpt)
    write_text(page_root / "sf5-componentized.html", componentized_markup)

    conversion_command = [
        sys.executable,
        str(skill_root / "scripts" / "convert_tailwind_to_sf5.py"),
        "--input",
        str(page_root / "source-excerpt.html"),
        "--mode",
        "html",
        "--render-component",
        component_id,
    ]
    conversion = run_json(conversion_command)
    write_text(
        page_root / "runtime-index.html",
        render_page(
            preview["title"],
            source_excerpt,
            componentized_markup,
            conversion.get("conversion", conversion),
            preview.get("targetLabel", "SF5 runtime-aware component output"),
            source_label=preview.get("sourceLabel", "TailAdmin source excerpt"),
            extra_head=runtime_head_tags(component_id, page_root, repo_root),
            include_preview_css=False,
        ),
    )
    runtime_screenshot, runtime_visual_score = capture_and_score(
        skill_root,
        page_root / "runtime-index.html",
        page_root / "runtime-screenshot.png",
        page_root / "runtime-visual-score.json",
    )
    runtime_probe = run_json_optional(
        [
            sys.executable,
            str(skill_root / "scripts" / "probe_html_runtime.py"),
            str(page_root / "runtime-index.html"),
            "--output",
            str(page_root / "runtime-probe.json"),
        ]
    )
    runtime_gap = (
        round(100 - float(runtime_visual_score.get("scorePercent", 0) or 0), 2)
        if runtime_visual_score.get("scorePercent") is not None
        else None
    )
    promotion_status = runtime_promotion_status(component_id, runtime_probe)
    max_runtime_visual_delta = float(preview.get("maxRuntimeVisualDelta", 1.0))
    promotion_command = conversion_command + [
        "--runtime-promotion-status",
        promotion_status,
        "--max-runtime-visual-delta",
        str(max_runtime_visual_delta),
    ]
    if runtime_gap is not None:
        promotion_command.extend(["--runtime-visual-delta", str(runtime_gap)])
    promotion_conversion = run_json(promotion_command)
    write_text(page_root / "conversion.json", json.dumps(promotion_conversion, ensure_ascii=False, indent=2) + "\n")
    ok = bool(runtime_screenshot.get("ok")) and bool(runtime_visual_score.get("ok")) and bool(runtime_probe.get("ok"))
    return {
        "ok": ok,
        "title": preview["title"],
        "runtimeScreenshotOk": bool(runtime_screenshot.get("ok")),
        "runtimeVisualScorePercent": runtime_visual_score.get("scorePercent"),
        "runtimeProbeOk": bool(runtime_probe.get("ok")),
        "runtimeProbe": runtime_probe,
        "runtimeVisualGap": runtime_gap,
        "maxRuntimeVisualDelta": max_runtime_visual_delta,
        "runtimeExpectedElements": runtime_expected_elements(component_id),
        "runtimePromotionStatus": promotion_status,
        "runtimeNotes": runtime_notes(component_id, runtime_probe),
        "converterPromotionGate": promotion_conversion.get("componentRender", {}).get("promotionGate", {}),
        "paths": {
            "runtimeIndex": (page_root / "runtime-index.html").as_posix(),
            "runtimeScreenshot": (page_root / "runtime-screenshot.png").as_posix(),
            "runtimeVisualScore": (page_root / "runtime-visual-score.json").as_posix(),
            "runtimeProbe": (page_root / "runtime-probe.json").as_posix(),
            "conversionReport": (page_root / "conversion.json").as_posix(),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate TailAdmin page conversion examples.")
    parser.add_argument("--tailadmin-root", default="", help="Path to cloned TailAdmin project")
    args = parser.parse_args()

    skill_root = skill_root_from_script()
    repo_root = repo_root_from_skill_root(skill_root)
    tailadmin_root = (
        Path(args.tailadmin_root).expanduser().resolve()
        if args.tailadmin_root
        else repo_root / "output" / "external-tailwind-projects" / "tailadmin-free-tailwind-dashboard-template"
    )
    if not tailadmin_root.exists():
        raise SystemExit(f"TailAdmin project not found: {tailadmin_root}")

    output_root = repo_root / "output" / "tailwind-to-sf5-tailadmin-pages"
    report = {
        "ok": True,
        "tailadminRoot": tailadmin_root.as_posix(),
        "license": "MIT; source copied only into ignored output artifacts.",
        "pages": {},
        "runtimeComponents": {},
    }

    for page_id, page in TAILADMIN_SOURCE_SNIPPETS.items():
        page_root = output_root / page_id
        source_path = tailadmin_root / page["sourceFile"]
        source_excerpt = clean(page["sourceMarkup"])
        sf5_markup = clean(page["sf5Markup"])
        componentized_markup = clean(page["componentizedMarkup"])
        write_text(page_root / "source-excerpt.html", source_excerpt)
        write_text(page_root / "sf5-final.html", sf5_markup)
        write_text(page_root / "sf5-componentized.html", componentized_markup)

        conversion = run_json(
            [
                sys.executable,
                str(skill_root / "scripts" / "convert_tailwind_to_sf5.py"),
                "--input",
                str(page_root / "source-excerpt.html"),
                "--mode",
                "html",
                "--render-recipe",
            ]
        )
        conversion_payload = conversion.get("conversion", conversion)
        write_text(page_root / "raw-converted.html", conversion_payload.get("convertedHtml", ""))
        write_text(page_root / "conversion.json", json.dumps(conversion, ensure_ascii=False, indent=2) + "\n")

        validation = subprocess.run(
            [
                sys.executable,
                str(skill_root / "scripts" / "validate_sf5_html_files.py"),
                "--strict",
                "--catalog-strict",
                str(page_root / "sf5-final.html"),
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        componentized_validation = subprocess.run(
            [
                sys.executable,
                str(skill_root / "scripts" / "validate_sf5_html_files.py"),
                "--strict",
                "--catalog-strict",
                str(page_root / "sf5-componentized.html"),
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        write_text(
            page_root / "index.html",
            render_page(page["title"], source_excerpt, sf5_markup, conversion_payload, "SF5 finished output"),
        )
        write_text(
            page_root / "componentized-index.html",
            render_page(page["title"], source_excerpt, componentized_markup, conversion_payload, "SF5 componentized output"),
        )
        write_text(
            page_root / "runtime-index.html",
            render_page(
                page["title"],
                source_excerpt,
                componentized_markup,
                conversion_payload,
                "SF5 runtime-aware output",
                extra_head=runtime_head_tags(page_id, page_root, repo_root),
                include_preview_css=False,
            ),
        )
        screenshot, visual_score = capture_and_score(
            skill_root,
            page_root / "index.html",
            page_root / "screenshot.png",
            page_root / "visual-score.json",
        )
        componentized_screenshot, componentized_visual_score = capture_and_score(
            skill_root,
            page_root / "componentized-index.html",
            page_root / "componentized-screenshot.png",
            page_root / "componentized-visual-score.json",
        )
        runtime_screenshot, runtime_visual_score = capture_and_score(
            skill_root,
            page_root / "runtime-index.html",
            page_root / "runtime-screenshot.png",
            page_root / "runtime-visual-score.json",
        )
        runtime_probe = run_json_optional(
            [
                sys.executable,
                str(skill_root / "scripts" / "probe_html_runtime.py"),
                str(page_root / "runtime-index.html"),
                "--output",
                str(page_root / "runtime-probe.json"),
            ]
        )
        runtime_status = runtime_promotion_status(page_id, runtime_probe)
        page_ok = (
            validation.returncode == 0
            and componentized_validation.returncode == 0
            and bool(screenshot.get("ok"))
            and bool(visual_score.get("ok"))
            and bool(componentized_screenshot.get("ok"))
            and bool(componentized_visual_score.get("ok"))
            and bool(runtime_screenshot.get("ok"))
            and bool(runtime_visual_score.get("ok"))
        )
        report["ok"] = report["ok"] and page_ok
        report["pages"][page_id] = {
            "ok": page_ok,
            "title": page["title"],
            "sourceFile": source_path.as_posix(),
            "sourceExists": source_path.exists(),
            "summary": conversion_payload.get("report", {}).get("summary", {}),
            "componentHints": [item.get("id") for item in conversion_payload.get("report", {}).get("componentHints", [])],
            "componentRenderCandidates": [
                item.get("id") for item in conversion_payload.get("report", {}).get("componentRenderCandidates", [])
            ],
            "smartHints": [item.get("id") for item in conversion_payload.get("report", {}).get("smartHints", [])],
            "sf5ValidationOk": validation.returncode == 0,
            "sf5ValidationStdout": validation.stdout,
            "componentizedValidationOk": componentized_validation.returncode == 0,
            "componentizedValidationStdout": componentized_validation.stdout,
            "screenshotOk": bool(screenshot.get("ok")),
            "visualScorePercent": visual_score.get("scorePercent"),
            "componentizedScreenshotOk": bool(componentized_screenshot.get("ok")),
            "componentizedVisualScorePercent": componentized_visual_score.get("scorePercent"),
            "componentizedScoreDelta": round(
                float(componentized_visual_score.get("scorePercent", 0) or 0)
                - float(visual_score.get("scorePercent", 0) or 0),
                2,
            ),
            "componentizedNotes": componentized_notes(page_id),
            "runtimeScreenshotOk": bool(runtime_screenshot.get("ok")),
            "runtimeVisualScorePercent": runtime_visual_score.get("scorePercent"),
            "runtimeScoreDelta": round(
                float(runtime_visual_score.get("scorePercent", 0) or 0)
                - float(visual_score.get("scorePercent", 0) or 0),
                2,
            ),
            "runtimeProbeOk": bool(runtime_probe.get("ok")),
            "runtimeProbe": runtime_probe,
            "runtimeExpectedElements": runtime_expected_elements(page_id),
            "runtimePromotionStatus": runtime_status,
            "runtimeNotes": runtime_notes(page_id, runtime_probe),
            "paths": {
                "index": (page_root / "index.html").as_posix(),
                "componentizedIndex": (page_root / "componentized-index.html").as_posix(),
                "runtimeIndex": (page_root / "runtime-index.html").as_posix(),
                "screenshot": (page_root / "screenshot.png").as_posix(),
                "componentizedScreenshot": (page_root / "componentized-screenshot.png").as_posix(),
                "runtimeScreenshot": (page_root / "runtime-screenshot.png").as_posix(),
                "runtimeVisualScore": (page_root / "runtime-visual-score.json").as_posix(),
                "runtimeProbe": (page_root / "runtime-probe.json").as_posix(),
                "sf5Final": (page_root / "sf5-final.html").as_posix(),
                "sf5Componentized": (page_root / "sf5-componentized.html").as_posix(),
                "conversionReport": (page_root / "conversion.json").as_posix(),
            },
        }

    for component_id, preview in RUNTIME_COMPONENT_PREVIEWS.items():
        component_report = generate_runtime_component_preview(skill_root, repo_root, output_root, component_id, preview)
        report["ok"] = report["ok"] and bool(component_report.get("ok"))
        report["runtimeComponents"][component_id] = component_report

    write_text(output_root / "report.json", json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    write_text(
        output_root / "README.md",
        "# TailAdmin to SF5 Page Examples\n\n"
        "Ignored local conversion examples generated from MIT-licensed TailAdmin source excerpts.\n\n"
        "Open these files in a browser:\n\n"
        "- `signin/index.html`\n"
        "- `signin/componentized-index.html`\n"
        "- `signin/runtime-index.html`\n"
        "- `basic-tables/index.html`\n\n"
        "- `basic-tables/componentized-index.html`\n\n"
        "- `basic-tables/runtime-index.html`\n\n"
        "- `runtime-components/dropdown/runtime-index.html`\n"
        "- `runtime-components/pagination/runtime-index.html`\n"
        "- `runtime-components/modal/runtime-index.html`\n\n"
        "Read `report.json` for conversion summaries, visual scores, componentized deltas, and componentized notes.\n\n"
        "Important: componentized previews use local preview CSS for custom elements. Runtime-aware previews load source-backed SF5 JS/CSS from `source/simai/*` and write `runtime-probe.json`. Smart placeholders such as `sf-code=\"table\"` still require a real SF5 runtime before they can replace finished HTML.\n",
    )
    print(json.dumps({"ok": report["ok"], "output": output_root.as_posix(), "report": (output_root / "report.json").as_posix()}, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
