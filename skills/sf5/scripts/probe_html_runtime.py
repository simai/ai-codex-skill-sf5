#!/usr/bin/env python3
"""
Probe a local HTML page in headless Chrome and return its post-runtime DOM.

Use this for SF5 runtime-aware previews where custom elements must be defined
by real JS assets, not by static CSS fallbacks.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path


MAC_BROWSER_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]
PATH_BROWSER_CANDIDATES = [
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
    "microsoft-edge",
    "brave-browser",
]


def find_browser() -> str:
    env_browser = os.environ.get("SF5_SCREENSHOT_BROWSER", "").strip()
    if env_browser and Path(env_browser).exists():
        return env_browser
    for item in MAC_BROWSER_CANDIDATES:
        if Path(item).exists():
            return item
    for item in PATH_BROWSER_CANDIDATES:
        resolved = shutil.which(item)
        if resolved:
            return resolved
    return ""


def to_url(input_path_or_url: str) -> str:
    if input_path_or_url.startswith(("http://", "https://", "file://")):
        return input_path_or_url
    return Path(input_path_or_url).expanduser().resolve().as_uri()


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe HTML runtime DOM with headless Chrome.")
    parser.add_argument("input", help="HTML file path or URL")
    parser.add_argument("--output", help="Optional JSON output path")
    parser.add_argument("--virtual-time-budget", type=int, default=5000)
    parser.add_argument("--timeout", type=int, default=30)
    args = parser.parse_args()

    browser = find_browser()
    payload = {
        "ok": False,
        "browser": browser,
        "input": args.input,
        "virtualTimeBudget": args.virtual_time_budget,
    }
    if not browser:
        payload["error"] = "No supported local Chrome/Chromium browser was found."
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 1

    command = [
        browser,
        "--headless=new",
        "--disable-gpu",
        f"--virtual-time-budget={args.virtual_time_budget}",
        "--dump-dom",
        to_url(args.input),
    ]
    try:
        completed = subprocess.run(command, text=True, capture_output=True, timeout=args.timeout, check=False)
    except subprocess.TimeoutExpired as exc:
        payload["error"] = f"Runtime probe timed out after {args.timeout}s."
        payload["stderr"] = str(exc)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 1

    dom = completed.stdout
    payload.update(
        {
            "returncode": completed.returncode,
            "stderr": completed.stderr.strip(),
            "domLength": len(dom),
            "runtimeStatus": "",
            "definedElements": [],
            "missingElements": [],
        }
    )
    status_marker = 'data-sf-runtime-status="'
    if status_marker in dom:
        payload["runtimeStatus"] = dom.split(status_marker, 1)[1].split('"', 1)[0]
    defined_marker = 'data-sf-runtime-defined="'
    if defined_marker in dom:
        value = dom.split(defined_marker, 1)[1].split('"', 1)[0]
        payload["definedElements"] = [item for item in value.split(",") if item]
    missing_marker = 'data-sf-runtime-missing="'
    if missing_marker in dom:
        value = dom.split(missing_marker, 1)[1].split('"', 1)[0]
        payload["missingElements"] = [item for item in value.split(",") if item]

    payload["ok"] = completed.returncode == 0 and payload.get("runtimeStatus") in {"ok", "not-required"}
    if completed.returncode != 0 and "error" not in payload:
        payload["error"] = "Headless Chrome returned a non-zero exit code."
    elif payload.get("runtimeStatus") == "partial" and "error" not in payload:
        payload["error"] = "Runtime probe did not report all expected custom elements as defined."
    elif not payload["ok"] and "error" not in payload:
        payload["error"] = "Runtime probe status was not written by the page."

    if args.output:
        output = Path(args.output).expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
