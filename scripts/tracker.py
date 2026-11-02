#!/usr/bin/env python3
"""Tiny CSV tracker for job applications. De-duplicates by URL.

Usage:
    python scripts/tracker.py add --company X --role Y --url U --portal linkedin --score 85 --status prepared
    python scripts/tracker.py update --url U --status submitted
    python scripts/tracker.py seen --url U        # exit 0 if already tracked, 1 if not
    python scripts/tracker.py list
"""
import argparse
import csv
import sys
from datetime import date
from pathlib import Path

FILE = Path("applications.csv")
FIELDS = ["date", "company", "role", "portal", "score", "status", "url", "notes"]


def read():
    if not FILE.exists():
        return []
    with FILE.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write(rows):
    with FILE.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add")
    for k in ("company", "role", "url", "portal"):
        a.add_argument(f"--{k}", required=True)
    a.add_argument("--score", default="")
    a.add_argument("--status", default="prepared")
    a.add_argument("--notes", default="")

    u = sub.add_parser("update")
    u.add_argument("--url", required=True)
    u.add_argument("--status", required=True)
    u.add_argument("--notes", default=None)

    s = sub.add_parser("seen")
    s.add_argument("--url", required=True)

    sub.add_parser("list")

    args = ap.parse_args()
    rows = read()

    if args.cmd == "add":
        if any(r["url"] == args.url for r in rows):
            print("Already tracked; skipping.")
            return
        rows.append({"date": date.today().isoformat(), "company": args.company, "role": args.role,
                     "portal": args.portal, "score": args.score, "status": args.status,
                     "url": args.url, "notes": args.notes})
        write(rows)
        print("Added.")
    elif args.cmd == "update":
        hit = False
        for r in rows:
            if r["url"] == args.url:
                r["status"] = args.status
                if args.notes is not None:
                    r["notes"] = args.notes
                hit = True
        if not hit:
            sys.exit("URL not found.")
        write(rows)
        print("Updated.")
    elif args.cmd == "seen":
        sys.exit(0 if any(r["url"] == args.url for r in rows) else 1)
    elif args.cmd == "list":
        for r in rows:
            print(f'{r["date"]} | {r["status"]:<10} | {r["company"]} | {r["role"]} | {r["portal"]}')


if __name__ == "__main__":
    main()
