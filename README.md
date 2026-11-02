# automated-job-assistant

Semi-automated job search helper built with Playwright. It finds roles that match a resume, pre-fills
applications in a real browser, and **stops before the final submit** so a human reviews and clicks it.

## What it does
- `scripts/launch_browser.py` – headed Chromium with a persistent profile (log in to portals once yourself).
- `work/server.py` + `work/run.sh` – keeps one browser open and runs small Python snippets against it.
- `work/search_li.py`, `work/search_remote.py` – collect LinkedIn job listings (Pune / remote, recent).
- `work/ats.py`, `work/ats2.py` – query public Greenhouse / Lever / Ashby job feeds for entry-level roles.
- `scripts/tracker.py` – CSV tracker (`applications.csv`) that de-duplicates by URL.
- `profile.example.yaml` – template for the answers a resume doesn't contain. Copy to `profile.yaml` (git-ignored).

## Rules it follows
- Never clicks the final submit button.
- You log in; it never types passwords, OTPs or solves CAPTCHAs.
- Only fills facts from your resume / `profile.yaml`; unknown fields are left blank and flagged.
- Keep volume low and paced; portals such as LinkedIn restrict automated access in their terms.

## Setup
```bash
pip install playwright pypdf
python -m playwright install chromium
cp profile.example.yaml profile.yaml   # then fill it in
python scripts/launch_browser.py
```
Personal files (resume, `profile.yaml`, `applications.csv`, screenshots) are git-ignored.
