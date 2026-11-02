#!/usr/bin/env python3
"""Launch a headed Chromium with a persistent profile so portal logins survive between sessions.

Usage:
    python scripts/launch_browser.py            # opens browser and keeps it open
    python scripts/launch_browser.py --port 9222

The browser exposes a local DevTools port so Playwright scripts can attach with:
    browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
    context = browser.contexts[0]

The user logs in manually in this window. Credentials are never handled by the skill.
"""
import argparse
import os
import signal
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

PROFILE_DIR = Path(os.path.expanduser("~/.job-apply/browser-profile"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=9222)
    args = parser.parse_args()

    PROFILE_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=False,
            args=[f"--remote-debugging-port={args.port}"],
            viewport={"width": 1366, "height": 850},
        )
        print(f"Browser running. Profile: {PROFILE_DIR}")
        print(f"Attach with connect_over_cdp('http://localhost:{args.port}'). Ctrl+C to close.")
        if not context.pages:
            context.new_page()

        signal.signal(signal.SIGINT, lambda *_: sys.exit(0))
        while True:
            time.sleep(3600)


if __name__ == "__main__":
    main()
