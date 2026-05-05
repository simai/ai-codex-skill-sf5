#!/usr/bin/env python3
"""
Generate an ignored Tailwind -> SF5 conversion lab under output/.

The lab uses original Tailwind-like snippets inspired by public Tailwind Plus
Application UI categories. It does not copy commercial Tailwind Plus source.
"""

from __future__ import annotations

import html
import json
import subprocess
import sys
from pathlib import Path
from textwrap import dedent


def skill_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def repo_root_from_skill_root(skill_root: Path) -> Path:
    return skill_root.parents[1]


SAMPLES: dict[str, dict[str, str]] = {
    "auth-form": {
        "title": "Sign-in and Registration inspired auth form",
        "source_url": "https://tailwindcss.com/plus/ui-blocks/application-ui",
        "html": """
        <main class="min-h-screen bg-gray-50 px-6 py-12">
          <section class="mx-auto flex max-w-md flex-col gap-6 rounded-2xl bg-white p-8 shadow-lg ring-1 ring-gray-200">
            <div class="space-y-2 text-center">
              <h1 class="text-2xl font-semibold tracking-tight text-gray-900">Sign in to Console</h1>
              <p class="text-sm text-gray-500">Use your work email to continue.</p>
            </div>
            <form class="space-y-5">
              <label class="block text-sm font-medium text-gray-700">Email</label>
              <input class="block w-full rounded-md border border-gray-300 px-3 py-2 text-sm placeholder:text-gray-400 focus:border-indigo-600 focus:ring-2 focus:ring-indigo-600" type="email" placeholder="name@example.com">
              <label class="block text-sm font-medium text-gray-700">Password</label>
              <input class="block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-indigo-600 focus:ring-2 focus:ring-indigo-600" type="password">
              <button class="flex w-full items-center justify-center rounded-md bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-500" type="submit">Continue</button>
            </form>
          </section>
        </main>
        """,
        "sf5": """
        <main class="theme-light min-h-screen bg-surface-0">
          <section class="container md:container p-y-3">
            <div class="flex content-main-center">
              <article class="w-full max-w-sm bg-surface-1 border border-outline-variant radius-1 p-3 shadow-1">
                <header class="flex flex-col gap-1">
                  <h1 class="title-3">Sign in to Console</h1>
                  <p class="text-2 color-on-surface-variant">Use your work email to continue.</p>
                </header>
                <form class="flex flex-col gap-2 m-top-3">
                  <label class="text-2 color-on-surface">Email</label>
                  <input class="w-full bg-surface-1 border border-outline-variant radius-1 p-2 text-2 color-on-surface" type="email" placeholder="name@example.com">
                  <label class="text-2 color-on-surface">Password</label>
                  <input class="w-full bg-surface-1 border border-outline-variant radius-1 p-2 text-2 color-on-surface" type="password">
                  <button class="sf-button sf-button--default sf-button--primary sf-button--size-1 w-full" type="submit">
                    <span class="sf-button-text-container">Continue</span>
                  </button>
                </form>
              </article>
            </div>
          </section>
        </main>
        """,
    },
    "summary-card": {
        "title": "Cards inspired summary card",
        "source_url": "https://tailwindcss.com/plus/ui-blocks/application-ui",
        "html": """
        <article class="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
          <div class="flex items-start justify-between gap-4">
            <div class="space-y-1">
              <p class="text-sm font-medium text-gray-500">Revenue</p>
              <h2 class="text-3xl font-semibold tracking-tight text-gray-900">$128,430</h2>
            </div>
            <span class="rounded-full bg-green-50 px-3 py-1 text-sm font-medium text-green-700">+12.5%</span>
          </div>
          <p class="mt-6 text-sm text-gray-500">Compared with the previous billing period.</p>
        </article>
        """,
        "sf5": """
        <article class="bg-surface-1 border border-outline-variant radius-1/3 p-3 shadow-1">
          <header class="flex items-start content-main-between gap-2">
            <div class="flex flex-col gap-1">
              <p class="text-2 color-on-surface-variant">Revenue</p>
              <h2 class="title-3 color-on-surface">$128,430</h2>
            </div>
            <span class="bg-success-container color-success radius-round p-x-2 p-y-1 text-2">+12.5%</span>
          </header>
          <p class="m-top-3 text-2 color-on-surface-variant">Compared with the previous billing period.</p>
        </article>
        """,
    },
    "data-table": {
        "title": "Tables inspired data table with toolbar",
        "source_url": "https://tailwindcss.com/plus/ui-blocks/application-ui",
        "html": """
        <section class="rounded-2xl border border-gray-200 bg-white shadow-sm">
          <header class="flex flex-col gap-4 border-b border-gray-200 p-6 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h2 class="text-lg font-semibold text-gray-900">Team members</h2>
              <p class="mt-1 text-sm text-gray-500">Manage active users and roles.</p>
            </div>
            <div class="flex gap-2">
              <input class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm" type="search" placeholder="Search">
              <button class="rounded-md bg-indigo-600 px-4 py-2 text-sm font-semibold text-white">Add user</button>
            </div>
          </header>
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200 text-left text-sm">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 font-semibold text-gray-900" scope="col">Name</th>
                  <th class="px-6 py-3 font-semibold text-gray-900" scope="col">Role</th>
                  <th class="px-6 py-3 font-semibold text-gray-900" scope="col">Status</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr>
                  <td class="px-6 py-4 text-gray-900">Alex Morgan</td>
                  <td class="px-6 py-4 text-gray-500">Admin</td>
                  <td class="px-6 py-4 text-green-700">Active</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>
        """,
        "sf5": """
        <article class="bg-surface-1 border border-outline-variant radius-1/3 shadow-1 overflow-hidden">
          <header class="flex flex-col gap-2 p-3 border-bottom-1 border-outline-variant sm:flex-row sm:items-center sm:content-main-between">
            <div class="flex flex-col gap-1">
              <h2 class="title-3 color-on-surface">Team members</h2>
              <p class="text-2 color-on-surface-variant">Manage active users and roles.</p>
            </div>
            <div class="flex flex-row flex-wrap gap-2">
              <input class="w-full border border-outline-variant radius-1 p-2 text-2" type="search" placeholder="Search">
              <button class="sf-button sf-button--default sf-button--primary sf-button--size-1" type="button">
                <span class="sf-button-text-container">Add user</span>
              </button>
            </div>
          </header>
          <div class="overflow-auto">
            <table class="table w-full">
              <thead>
                <tr>
                  <th scope="col">Name</th>
                  <th scope="col">Role</th>
                  <th scope="col">Status</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Alex Morgan</td>
                  <td>Admin</td>
                  <td>Active</td>
                </tr>
              </tbody>
            </table>
          </div>
        </article>
        """,
    },
}


LAB_CSS = """
:root {
  color-scheme: light;
  --surface-0: #f5f7fb;
  --surface-1: #ffffff;
  --surface-2: #eef2f7;
  --outline: #d8dee8;
  --outline-variant: #e5e9f0;
  --on-surface: #111827;
  --on-surface-variant: #667085;
  --primary: #335cff;
  --success: #047857;
  --success-container: #dcfce7;
}
* { box-sizing: border-box; }
body { margin: 0; font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: var(--surface-0); color: var(--on-surface); }
.lab-page { padding: 32px; }
.lab-header { max-width: 1180px; margin: 0 auto 24px; }
.lab-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 24px; max-width: 1180px; margin: 0 auto 32px; }
.lab-panel { border: 1px solid var(--outline-variant); border-radius: 20px; background: #fff; overflow: hidden; box-shadow: 0 18px 60px rgb(15 23 42 / 8%); }
.lab-panel h2 { margin: 0; padding: 16px 18px; font-size: 14px; letter-spacing: .08em; text-transform: uppercase; color: #475467; border-bottom: 1px solid var(--outline-variant); }
.lab-stage { padding: 24px; background: linear-gradient(180deg, #f8fafc, #eef2f7); min-height: 360px; }
.lab-notes { max-width: 1180px; margin: 0 auto; display: grid; gap: 12px; }
.lab-note { padding: 16px 18px; border: 1px solid var(--outline-variant); border-radius: 16px; background: #fff; }
/* Minimal Tailwind utility subset used only by local source-inspired lab snippets. */
.bg-gray-50 { background: #f9fafb; }
.bg-white { background: #fff; }
.bg-indigo-600 { background: #4f46e5; }
.bg-green-50 { background: #f0fdf4; }
.text-gray-900 { color: #111827; }
.text-gray-700 { color: #374151; }
.text-gray-500 { color: #6b7280; }
.text-green-700 { color: #15803d; }
.text-white { color: #fff; }
.text-sm { font-size: 14px; line-height: 20px; }
.text-lg { font-size: 18px; line-height: 28px; }
.text-2xl { font-size: 24px; line-height: 32px; }
.text-3xl { font-size: 30px; line-height: 36px; }
.font-medium { font-weight: 500; }
.font-semibold { font-weight: 700; }
.tracking-tight { letter-spacing: -.025em; }
.text-left { text-align: left; }
.text-center { text-align: center; }
.mx-auto { margin-inline: auto; }
.mt-1 { margin-top: 4px; }
.mt-6 { margin-top: 24px; }
.px-3 { padding-inline: 12px; }
.px-4 { padding-inline: 16px; }
.px-6 { padding-inline: 24px; }
.py-1 { padding-block: 4px; }
.py-2 { padding-block: 8px; }
.py-3 { padding-block: 12px; }
.py-4 { padding-block: 16px; }
.py-12 { padding-block: 48px; }
.p-6 { padding: 24px; }
.p-8 { padding: 32px; }
.max-w-md { max-width: 28rem; }
.min-w-full { min-width: 100%; }
.rounded-md { border-radius: 6px; }
.rounded-2xl { border-radius: 16px; }
.rounded-full { border-radius: 999px; }
.border-gray-200 { border-color: #e5e7eb; }
.border-gray-300 { border-color: #d1d5db; }
.border-b { border-bottom: 1px solid #e5e7eb; }
.shadow-sm { box-shadow: 0 1px 2px rgb(15 23 42 / 8%); }
.shadow-lg { box-shadow: 0 20px 45px rgb(15 23 42 / 12%); }
.ring-1 { box-shadow: 0 0 0 1px #e5e7eb, 0 20px 45px rgb(15 23 42 / 12%); }
.ring-gray-200 { --tw-ring-color: #e5e7eb; }
.space-y-1 > * + * { margin-top: 4px; }
.space-y-2 > * + * { margin-top: 8px; }
.space-y-5 > * + * { margin-top: 20px; }
.overflow-x-auto { overflow-x: auto; }
.divide-y > * + * { border-top: 1px solid #e5e7eb; }
.divide-gray-100 > * + * { border-color: #f3f4f6; }
.divide-gray-200 > * + * { border-color: #e5e7eb; }
.placeholder\\:text-gray-400::placeholder { color: #9ca3af; }
.theme-light, .bg-surface-0 { background: var(--surface-0); }
.bg-surface-1 { background: var(--surface-1); }
.bg-success-container { background: var(--success-container); }
.color-on-surface { color: var(--on-surface); }
.color-on-surface-variant { color: var(--on-surface-variant); }
.color-success { color: var(--success); }
.container { width: min(100%, 1120px); margin-inline: auto; }
.min-h-screen { min-height: 100vh; }
.flex { display: flex; }
.inline-flex { display: inline-flex; }
.flex-col { flex-direction: column; }
.flex-row { flex-direction: row; }
.flex-wrap { flex-wrap: wrap; }
.grid { display: grid; }
.items-center { align-items: center; }
.items-start { align-items: flex-start; }
.content-main-center { justify-content: center; }
.content-main-between { justify-content: space-between; }
.gap-1 { gap: 8px; }
.gap-2 { gap: 16px; }
.gap-3 { gap: 24px; }
.gap-4 { gap: 32px; }
.w-full { width: 100%; }
.max-w-sm { max-width: 24rem; }
.p-2 { padding: 16px; }
.p-3 { padding: 24px; }
.p-x-2 { padding-inline: 16px; }
.p-y-1 { padding-block: 8px; }
.p-y-3 { padding-block: 24px; }
.m-top-3 { margin-top: 24px; }
.border { border: 1px solid var(--outline); }
.border-outline-variant { border-color: var(--outline-variant); }
.border-bottom { border-bottom: 1px solid var(--outline-variant); }
.radius-1 { border-radius: 16px; }
.radius-1\\/3 { border-radius: 20px; }
.radius-round { border-radius: 999px; }
.shadow-1 { box-shadow: 0 16px 40px rgb(15 23 42 / 10%); }
.overflow-hidden { overflow: hidden; }
.overflow-auto { overflow: auto; }
.title-3 { margin: 0; font-size: 24px; line-height: 1.2; font-weight: 700; letter-spacing: -.02em; }
.text-2 { margin: 0; font-size: 14px; line-height: 1.5; }
.sf-button { appearance: none; border: 0; border-radius: 12px; display: inline-flex; align-items: center; justify-content: center; min-height: 42px; padding: 0 18px; font: inherit; font-weight: 700; cursor: pointer; }
.sf-button--primary { background: var(--primary); color: #fff; }
.sf-button--outline { background: transparent; color: var(--on-surface); border: 1px solid var(--outline); }
input { min-height: 42px; font: inherit; }
.table { border-collapse: collapse; min-width: 100%; background: var(--surface-1); }
.table th, .table td { padding: 14px 16px; border-bottom: 1px solid var(--outline-variant); text-align: left; font-size: 14px; }
.table th { color: var(--on-surface); font-weight: 700; background: var(--surface-2); }
@media (max-width: 860px) { .lab-grid { grid-template-columns: 1fr; } .lab-page { padding: 16px; } }
@media (min-width: 640px) { .sm\\:flex-row { flex-direction: row; } .sm\\:items-center { align-items: center; } .sm\\:content-main-between { justify-content: space-between; } }
"""


def clean_markup(value: str) -> str:
    return dedent(value).strip() + "\n"


def run_json(command: list[str]) -> dict:
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout or f"Command failed: {' '.join(command)}")
    return json.loads(result.stdout)


def run_json_optional(command: list[str]) -> dict:
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        payload = {
            "ok": False,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }
    return payload


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def render_harness(samples: dict[str, dict[str, str]], report: dict) -> str:
    sections: list[str] = []
    for sample_id, sample in samples.items():
        title = html.escape(sample["title"])
        source = sample["html"]
        sf5 = sample["sf5"]
        metrics = report["samples"][sample_id]
        sections.append(
            f"""
            <section class="lab-header">
              <h1>{title}</h1>
              <p>Mapped: {metrics['summary']['mappedCount']}; deferred: {metrics['summary']['deferredCount']}; blocked: {metrics['summary']['blockedCount']}; unmapped: {metrics['summary']['unmappedCount']}.</p>
            </section>
            <div class="lab-grid">
              <article class="lab-panel">
                <h2>Tailwind-like source</h2>
                <div class="lab-stage">{source}</div>
              </article>
              <article class="lab-panel">
                <h2>SF5 finished output</h2>
                <div class="lab-stage">{sf5}</div>
              </article>
            </div>
            """
        )
    notes = "\n".join(
        f"<div class=\"lab-note\"><strong>{html.escape(item['id'])}</strong>: {html.escape(item['note'])}</div>"
        for item in report["qaNotes"]
    )
    return (
        "<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        "<title>Tailwind to SF5 Lab</title>\n<style>\n"
        + LAB_CSS
        + "\n</style>\n</head>\n<body>\n<main class=\"lab-page\">\n"
        + "\n".join(sections)
        + "<section class=\"lab-notes\"><h2>QA notes</h2>"
        + notes
        + "</section>\n</main>\n</body>\n</html>\n"
    )


def main() -> int:
    skill_root = skill_root_from_script()
    repo_root = repo_root_from_skill_root(skill_root)
    output_root = repo_root / "output" / "tailwind-to-sf5-lab"
    source_dir = output_root / "source"
    raw_dir = output_root / "raw-converted"
    final_dir = output_root / "sf5-final"
    report_dir = output_root / "reports"

    report: dict = {
        "ok": True,
        "sourcePolicy": {
            "sourceUrl": "https://tailwindcss.com/plus/ui-blocks/application-ui",
            "licenseDecision": "Do not copy commercial Tailwind Plus source into repository artifacts. Use public categories as inspiration and original local snippets for tests.",
        },
        "samples": {},
        "qaNotes": [],
    }

    for sample_id, sample in SAMPLES.items():
        sample_html = clean_markup(sample["html"])
        sample_sf5 = clean_markup(sample["sf5"])
        source_path = source_dir / f"{sample_id}.html"
        final_path = final_dir / f"{sample_id}.sf5.html"
        write_text(source_path, sample_html)
        write_text(final_path, sample_sf5)

        converted = run_json(
            [
                sys.executable,
                str(skill_root / "scripts" / "convert_tailwind_to_sf5.py"),
                "--input",
                str(source_path),
                "--mode",
                "html",
                "--render-recipe",
            ]
        )
        conversion = converted.get("conversion", converted)
        write_text(raw_dir / f"{sample_id}.raw.html", conversion.get("convertedHtml", ""))
        write_text(report_dir / f"{sample_id}.conversion.json", json.dumps(converted, ensure_ascii=False, indent=2) + "\n")
        summary = conversion.get("report", {}).get("summary", {})
        report["samples"][sample_id] = {
            "title": sample["title"],
            "sourceUrl": sample["source_url"],
            "summary": summary,
            "componentHints": [item.get("id") for item in conversion.get("report", {}).get("componentHints", [])],
            "smartHints": [item.get("id") for item in conversion.get("report", {}).get("smartHints", [])],
            "recipeRenderOk": bool(converted.get("recipeRender", {}).get("ok")),
        }
        if summary.get("unmappedCount", 0) or summary.get("deferredCount", 0):
            report["qaNotes"].append(
                {
                    "id": sample_id,
                    "note": "Raw converter output still needs manual finishing before SF5-ready delivery.",
                }
            )

    inventory = run_json(
        [
            sys.executable,
            str(skill_root / "scripts" / "convert_tailwind_to_sf5.py"),
            "--inventory",
            str(source_dir),
        ]
    )
    write_text(report_dir / "inventory.json", json.dumps(inventory, ensure_ascii=False, indent=2) + "\n")
    report["inventory"] = {
        "filesScanned": inventory.get("filesScanned"),
        "filesWithTailwindSignals": inventory.get("filesWithTailwindSignals"),
        "riskCounts": inventory.get("riskCounts"),
        "topClasses": inventory.get("topClasses", [])[:20],
        "componentHintCounts": inventory.get("componentHintCounts"),
        "smartHintCounts": inventory.get("smartHintCounts"),
    }

    final_files = sorted(str(path) for path in final_dir.glob("*.html"))
    validator = subprocess.run(
        [
            sys.executable,
            str(skill_root / "scripts" / "validate_sf5_html_files.py"),
            "--strict",
            "--catalog-strict",
            *final_files,
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    report["sf5Validation"] = {
        "ok": validator.returncode == 0,
        "stdout": validator.stdout,
        "stderr": validator.stderr,
    }
    if validator.returncode != 0:
        report["ok"] = False
        report["qaNotes"].append({"id": "sf5-validation", "note": "Finished SF5 snippets did not pass strict validation."})

    index_path = output_root / "index.html"
    write_text(index_path, render_harness({k: {"title": v["title"], "html": clean_markup(v["html"]), "sf5": clean_markup(v["sf5"])} for k, v in SAMPLES.items()}, report))
    screenshot_payload = run_json_optional(
        [
            sys.executable,
            str(skill_root / "scripts" / "capture_html_screenshot.py"),
            str(index_path),
            "--output",
            str(output_root / "screenshots" / "index.png"),
        ]
    )
    report["screenshotFallback"] = screenshot_payload
    if not screenshot_payload.get("ok"):
        report["qaNotes"].append({"id": "screenshot-fallback", "note": "Headless browser screenshot fallback did not produce an image."})
    else:
        visual_score_payload = run_json_optional(
            [
                sys.executable,
                str(skill_root / "scripts" / "score_lab_visual.py"),
                str(output_root / "screenshots" / "index.png"),
                "--output",
                str(report_dir / "visual-score.json"),
            ]
        )
        report["visualScore"] = visual_score_payload
    write_text(report_dir / "lab-report.json", json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    write_text(
        output_root / "QA.md",
        "# Tailwind to SF5 Lab QA\n\n"
        f"- Source policy: {report['sourcePolicy']['licenseDecision']}\n"
        f"- Inventory files with Tailwind signals: {report['inventory']['filesWithTailwindSignals']}\n"
        f"- Risk counts: {report['inventory']['riskCounts']}\n"
        f"- SF5 strict validation: {'PASS' if report['sf5Validation']['ok'] else 'FAIL'}\n"
        f"- Browser target: `{(output_root / 'index.html').as_posix()}`\n",
    )
    print(json.dumps({"ok": report["ok"], "output": output_root.as_posix(), "report": (report_dir / "lab-report.json").as_posix()}, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
