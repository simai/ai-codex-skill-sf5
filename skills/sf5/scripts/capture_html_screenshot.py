#!/usr/bin/env python3
"""
Capture an HTML page screenshot with a local headless browser.

This is a fallback for cases where browser-use can load the page and inspect
DOM/console, but screenshot capture times out.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
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
    parser = argparse.ArgumentParser(description="Capture an HTML screenshot using a local headless browser.")
    parser.add_argument("input", help="HTML file path or URL")
    parser.add_argument("--output", required=True, help="PNG output path")
    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument("--height", type=int, default=900)
    parser.add_argument("--timeout", type=int, default=30)
    args = parser.parse_args()

    browser = find_browser()
    output_path = Path(args.output).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result = {
        "ok": False,
        "browser": browser,
        "input": args.input,
        "output": output_path.as_posix(),
        "width": args.width,
        "height": args.height,
    }
    if not browser:
        result["error"] = "No supported local Chrome/Chromium browser was found."
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    command = [
        browser,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        f"--window-size={args.width},{args.height}",
        f"--screenshot={output_path}",
        to_url(args.input),
    ]
    try:
        completed = subprocess.run(command, text=True, capture_output=True, timeout=args.timeout, check=False)
    except subprocess.TimeoutExpired as exc:
        result["error"] = f"Screenshot command timed out after {args.timeout}s."
        result["stderr"] = str(exc)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    result["returncode"] = completed.returncode
    result["stdout"] = completed.stdout.strip()
    result["stderr"] = completed.stderr.strip()
    result["ok"] = completed.returncode == 0 and output_path.exists() and output_path.stat().st_size > 0
    if not result["ok"] and "error" not in result:
        result["error"] = "Screenshot command did not produce a non-empty PNG."
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
