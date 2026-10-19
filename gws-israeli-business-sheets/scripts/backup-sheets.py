#!/usr/bin/env python3
"""Backup Google Sheets tabs as local CSV files using the gws CLI.

Exports each tab from a Google Spreadsheet to a separate CSV file in the
specified output directory. Useful for creating accountant-ready backups.

Usage:
  python3 scripts/backup-sheets.py --spreadsheet-id SHEET_ID --output-dir ./backups
  python3 scripts/backup-sheets.py --spreadsheet-id SHEET_ID --output-dir ./backups --tabs "Sheet1,VAT-Period-1"
  python3 scripts/backup-sheets.py --spreadsheet-id SHEET_ID --output-dir ./backups --all-tabs
  python3 scripts/backup-sheets.py --help

Requires: gws CLI (npm install -g @googleworkspace/cli) with valid authentication.

The gws command surface is generated from Google's Discovery API. This script
uses the raw `gws sheets spreadsheets values get` method with `--format csv`.
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


class GwsError(RuntimeError):
    """A gws invocation failed. Raised so callers can continue with other tabs."""


def run_gws(args: list[str]) -> str:
    """Run a gws CLI command and return stdout."""
    cmd = ["gws"] + args
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode != 0:
            # Raise rather than sys.exit: sys.exit raises SystemExit, which the
            # per-tab `except Exception` handler cannot catch, so one bad tab
            # used to kill the whole backup silently.
            raise GwsError(f"gws exited {result.returncode}: {result.stderr.strip()}")
        return result.stdout
    except FileNotFoundError:
        raise GwsError(
            "gws CLI not found. The recommended install is the pre-built binary from "
            "https://github.com/googleworkspace/cli/releases, or: npm install -g @googleworkspace/cli"
        )
    except subprocess.TimeoutExpired:
        raise GwsError("gws command timed out after 60 seconds.")


def list_tabs(spreadsheet_id: str) -> list[str]:
    """Return every tab title, read from spreadsheets.get with a fields mask."""
    params = json.dumps({"spreadsheetId": spreadsheet_id, "fields": "sheets.properties.title"})
    raw = run_gws(["sheets", "spreadsheets", "get", "--params", params])
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        raise GwsError(f"could not parse the tab list returned by gws: {raw[:200]!r}")
    titles = [s.get("properties", {}).get("title") for s in data.get("sheets", [])]
    titles = [t for t in titles if t]
    if not titles:
        raise GwsError("gws returned no tabs for this spreadsheet.")
    return titles


def a1_sheet(tab_name: str) -> str:
    """Quote a tab name for A1 notation: 'VAT Period 1', with ' doubled."""
    return "'" + tab_name.replace("'", "''") + "'"


def export_tab(spreadsheet_id: str, tab_name: str, output_dir: Path, used: set) -> str:
    """Export a single sheet tab as CSV."""
    safe_name = "".join(c if c.isalnum() or c in "-_." else "_" for c in tab_name)
    timestamp = datetime.now().strftime("%Y%m%d")
    filename = f"{safe_name}_{timestamp}.csv"
    n = 2
    # Two tab names can sanitise to the same file name ("VAT Period 1" and
    # "VAT_Period_1"); never let one silently overwrite the other.
    while filename in used:
        filename = f"{safe_name}_{n}_{timestamp}.csv"
        n += 1
    used.add(filename)
    output_path = output_dir / filename

    params = json.dumps({"spreadsheetId": spreadsheet_id, "range": a1_sheet(tab_name)})
    csv_data = run_gws([
        "sheets", "spreadsheets", "values", "get",
        "--params", params,
        "--format", "csv",
    ])

    output_path.write_text(csv_data, encoding="utf-8")
    return str(output_path)


def main():
    parser = argparse.ArgumentParser(
        description="Backup Google Sheets tabs as local CSV files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  %(prog)s --spreadsheet-id abc123 --output-dir ./backups --all-tabs\n"
            "  %(prog)s --spreadsheet-id abc123 --output-dir ./backups --tabs 'Sheet1,Summary'\n"
        ),
    )
    parser.add_argument(
        "--spreadsheet-id",
        required=True,
        help="Google Spreadsheet ID (from the URL)",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory to save CSV files",
    )
    which = parser.add_mutually_exclusive_group()
    which.add_argument(
        "--tabs",
        help="Comma-separated list of tab names to export.",
    )
    which.add_argument(
        "--all-tabs",
        action="store_true",
        help="Read the tab list from the spreadsheet itself and export every tab.",
    )

    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.tabs:
        tab_names = [t.strip() for t in args.tabs.split(",") if t.strip()]
    elif args.all_tabs:
        try:
            tab_names = list_tabs(args.spreadsheet_id)
        except GwsError as e:
            print(f"Error: could not list the tabs: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("Error: pass --tabs 'Sheet1,VAT-Period-1' or --all-tabs.", file=sys.stderr)
        print("  Defaulting to a single tab would silently under-back-up records you", file=sys.stderr)
        print("  must retain for 7 years, so the script refuses to guess.", file=sys.stderr)
        print("  You can see the tab names with:", file=sys.stderr)
        print("    gws sheets spreadsheets get --params '{\"spreadsheetId\":\"<ID>\",\"fields\":\"sheets.properties.title\"}'", file=sys.stderr)
        sys.exit(1)

    print(f"Backing up {len(tab_names)} tab(s) to: {output_dir}/")
    exported = []
    used: set = set()

    for tab in tab_names:
        try:
            path = export_tab(args.spreadsheet_id, tab, output_dir, used)
            exported.append(path)
            print(f"  Exported: {tab} -> {path}")
        except Exception as e:
            print(f"  Failed: {tab} - {e}", file=sys.stderr)

    failed = len(tab_names) - len(exported)
    print(f"\nBackup complete: {len(exported)}/{len(tab_names)} tabs exported.")
    if failed:
        print(f"{failed} tab(s) FAILED. The backup is incomplete.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
