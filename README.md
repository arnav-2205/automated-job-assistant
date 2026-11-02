# Automated Job Assistant

A semi-automated job-application helper built on [Playwright](https://playwright.dev/python/). It searches for roles that fit a resume, opens each application in a real browser, pre-fills what it can, and **stops before the final submit** so a human reviews every application and clicks the button themselves.

> **Human in the loop by design.** Applications go out under your name. This tool automates the tedious parts (searching, ranking, retyping the same details) and leaves judgment and the irreversible click to you.

## Features

- **Job discovery**: LinkedIn search (Pune, remote, recent postings) plus public Greenhouse, Lever and Ashby job feeds for entry-level roles.
- **Resume-aware ranking**: listings are scored against the resume and a search brief (skills, seniority, location, deal-breakers).
- **Pre-filling**: LinkedIn Easy Apply flows and external application forms are filled from the resume and a local `profile.yaml`.
- **Review screenshots**: a screenshot of each prepared application is saved for later review.
- **Tracker**: a CSV log (`applications.csv`) de-duplicated by URL, with `prepared`, `needs_input`, `skipped` and `submitted` statuses.
- **Persistent login**: a dedicated Chromium profile keeps portal logins between runs, so you sign in once.

## Safety rules

| Rule | Why |
|---|---|
| Never clicks Submit / Apply Now / Submit application | The final click stays with you |
| You log in; no passwords, OTPs or CAPTCHA solving | Credentials never pass through the tool |
| Only facts from the resume or `profile.yaml` | Unknown fields (CTC, notice period, work authorization, consent boxes) are left blank and flagged |
| No account creation | Portals that require one are skipped |
| Paced, low-volume activity | Roughly 10 applications per session |

## How it works

```
 resume + profile.yaml ──► search (LinkedIn / ATS feeds) ──► rank ──► you approve a shortlist
                                                                         │
 applications.csv  ◄── tracker ◄── review screenshots ◄── pre-fill ◄────┘
                                                            │
                                            stops at the final step; you submit
```

Browser control uses a small command queue, because attaching to a running Chromium over CDP proved unreliable:

1. `work/server.py` launches one headed Chromium with the persistent profile and keeps it open.
2. Python snippets dropped into `work/q/` are executed against that live browser (`ctx`, `pages` are in scope).
3. `work/run.sh <snippet.py>` submits a snippet and prints its output, so tabs stay open between steps.

## Project structure

```
.
├── README.md
├── profile.example.yaml      # template for answers a resume doesn't contain
├── scripts/
│   ├── launch_browser.py     # headed Chromium with persistent profile
│   └── tracker.py            # CSV tracker (add / update / seen / list)
└── work/
    ├── server.py             # keeps the browser open, executes queued snippets
    ├── run.sh                # submit a snippet to the server and read its output
    ├── step.py               # helpers for stepping through LinkedIn Easy Apply modals
    ├── search_li.py          # LinkedIn search (Pune)
    ├── search_remote.py      # LinkedIn search (remote, entry level)
    ├── ats.py                # Greenhouse / Lever feed query
    └── ats2.py               # wider feed query incl. Ashby
```

Local-only files are git-ignored: your resume, `profile.yaml`, `applications.csv`, screenshots and any per-application scripts.

## Setup

Requires Python 3.10+.

```bash
pip install playwright pypdf
python -m playwright install chromium

cp profile.example.yaml profile.yaml    # fill in your details
```

Edit `profile.yaml` with your name, contact details, links and standard answers (notice period, expected CTC, work authorization, relocation). Anything left blank stays blank on forms.

## Usage

```bash
# 1. Start the persistent browser and keep it running
python work/server.py

# 2. Log in to LinkedIn yourself in that window (first run only)

# 3. Search (writes work/li_jobs.json or work/li_remote.json)
python work/search_li.py
python work/search_remote.py

# 4. Query public ATS job feeds
python work/ats.py
python work/ats2.py

# 5. Drive the open browser with a snippet
work/run.sh my_snippet.py

# 6. Track results
python scripts/tracker.py add --company "Acme" --role "SWE Intern" \
    --url "https://..." --portal linkedin --score 80 --status prepared
python scripts/tracker.py update --url "https://..." --status submitted
python scripts/tracker.py list
```

Note: `search_li.py` and `search_remote.py` open the same Chromium profile directly, so stop `server.py` first (or run them when it is not running). Two processes cannot share one profile.

## Known limitations

- LinkedIn changes its layout often; selectors (for example `componentkey^="job-card-component-ref-"`) may need updating.
- Naukri's Apply button submits instantly, so it is deliberately not automated. List matches and open links for the user to click.
- Workday usually requires an account and is skipped.
- Some external apply links show a LinkedIn "Share your profile?" prompt; that choice is left to the user.
- Many remote internship postings are templated, low-paying mass listings; check them before applying.
- Closing the Chromium window ends the session and loses unsaved prepared forms.

## Disclaimer

LinkedIn, Indeed and Naukri restrict automated access in their terms of service. This tool keeps volume low, runs in your own logged-in browser, paces its actions and never submits, which reduces but does not eliminate that risk. Use it at your own discretion. It makes no attempt to evade bot detection.
