#!/usr/bin/env python3
"""Generate bi-monthly VAT summary reports from Google Sheets data.

Reads exported sheet data (JSON or CSV) and produces a VAT period summary
with totals for income, expenses, VAT collected, input VAT, and net liability.

Usage:
  python3 scripts/vat-summary.py --input data.json --period 1 --year 2026
  python3 scripts/vat-summary.py --input data.csv --period 3 --year 2026 --output summary.csv
  python3 scripts/vat-summary.py --help

VAT Periods (Israel, bi-monthly):
  1 = Jan-Feb    2 = Mar-Apr    3 = May-Jun
  4 = Jul-Aug    5 = Sep-Oct    6 = Nov-Dec
"""

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path


PERIOD_MONTHS = {
    1: (1, 2),
    2: (3, 4),
    3: (5, 6),
    4: (7, 8),
    5: (9, 10),
    6: (11, 12),
}

PERIOD_DUE_DATES = {
    1: "March 15",
    2: "May 15",
    3: "July 15",
    4: "September 15",
    5: "November 15",
    6: "January 15 (next year)",
}


def parse_date(date_str: str) -> datetime | None:
    """Parse DD/MM/YYYY date format."""
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    return None


class AmountParseError(ValueError):
    """Raised when a non-empty cell cannot be read as a number."""


def parse_amount(amount_str) -> float:
    """Parse an amount cell into a float.

    Handles the shekel sign, thousands separators, currency words and
    parenthesised negatives. The Sheets API returns FORMATTED_VALUE by default,
    so a column formatted as ILS currency arrives as a string like
    '\u20aa5,900.00'. Silently turning that into 0.0 is how this script used to
    print a confident all-zero VAT report, so an unparseable non-empty cell now
    raises instead.
    """
    if amount_str is None:
        return 0.0
    raw = str(amount_str).strip()
    if not raw:
        return 0.0
    cleaned = raw
    for token in ("\u20aa", "ILS", "NIS", "\u05e9\"\u05d7", "\u05e9\u05e7\u05dc", ","):
        cleaned = cleaned.replace(token, "")
    cleaned = cleaned.replace("\u00a0", " ").strip()
    negative = cleaned.startswith("(") and cleaned.endswith(")")
    if negative:
        cleaned = cleaned[1:-1].strip()
    try:
        value = float(cleaned)
    except ValueError:
        raise AmountParseError(
            f"could not read {raw!r} as a number. If the cell is currency-formatted, "
            "re-read the range with valueRenderOption=UNFORMATTED_VALUE."
        )
    return -value if negative else value


def load_data(input_path: str) -> list[dict]:
    """Load transaction data from JSON or CSV file."""
    path = Path(input_path)

    if path.suffix == ".json":
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list) and len(data) > 0:
            if isinstance(data[0], list):
                headers = data[0]
                return [dict(zip(headers, row)) for row in data[1:]]
            return data
        return []

    elif path.suffix == ".csv":
        with open(path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)

    else:
        print(f"Error: Unsupported file format '{path.suffix}'. Use .json or .csv", file=sys.stderr)
        sys.exit(1)


def filter_by_period(transactions: list[dict], period: int, year: int) -> list[dict]:
    """Filter transactions to the specified bi-monthly VAT period."""
    if period not in PERIOD_MONTHS:
        print(f"Error: Invalid period {period}. Must be 1-6.", file=sys.stderr)
        sys.exit(1)

    DATE_KEYS = ("Date", "date", "תאריך")
    start_month, end_month = PERIOD_MONTHS[period]
    filtered = []

    for txn in transactions:
        date_str = ""
        for k in DATE_KEYS:
            if k in txn and str(txn[k]).strip() != "":
                date_str = txn[k]
                break
        date = parse_date(date_str)
        if date and date.year == year and start_month <= date.month <= end_month:
            filtered.append(txn)

    return filtered


def compute_summary(transactions: list[dict]) -> dict:
    """Compute VAT summary from filtered transactions."""
    total_income = 0.0
    total_expenses = 0.0
    vat_collected = 0.0
    vat_paid = 0.0
    income_count = 0
    expense_count = 0
    income_categories: dict[str, float] = {}
    expense_categories: dict[str, float] = {}
    blocked_flags: list = []
    mixed_flags: list = []
    unknown_types: list = []

    AMOUNT_KEYS = ("Amount (excl. VAT)", "amount", "Amount", "amount_excl_vat",
                   "Amount excl VAT", 'סכום (ללא מע"מ)')
    VAT_KEYS = ("VAT (18%)", "VAT (17%)", "vat", "VAT",
                'מע"מ', 'מע"מ (18%)', 'מע"מ (17%)')
    unmatched_amount = 0
    unmatched_vat = 0
    income_missing_vat = 0

    def pick(txn, keys):
        for k in keys:
            if k in txn and str(txn[k]).strip() != "":
                return txn[k], True
        return "0", False

    for txn in transactions:
        TYPE_KEYS = ("Type", "type", "סוג")
        CATEGORY_KEYS = ("Category", "category", "קטגוריה")
        DESCRIPTION_KEYS = ("Description", "description", "תיאור")
        txn_type = str(pick(txn, TYPE_KEYS)[0] if pick(txn, TYPE_KEYS)[1] else "").strip().lower()
        raw_amount, found_amount = pick(txn, AMOUNT_KEYS)
        if not found_amount:
            unmatched_amount += 1
        amount = parse_amount(raw_amount)
        raw_vat, found_vat = pick(txn, VAT_KEYS)
        if not found_vat:
            unmatched_vat += 1
        vat = parse_amount(raw_vat)
        category = pick(txn, CATEGORY_KEYS)[0] if pick(txn, CATEGORY_KEYS)[1] else "Uncategorized"

        if txn_type in ("income", "\u05d4\u05db\u05e0\u05e1\u05d4"):
            if found_vat and vat == 0 and amount != 0:
                income_missing_vat += 1
            total_income += amount
            vat_collected += vat
            income_count += 1
            income_categories[category] = income_categories.get(category, 0) + amount
        elif txn_type in ("expense", "\u05d4\u05d5\u05e6\u05d0\u05d4"):
            total_expenses += amount
            vat_paid += vat
            expense_count += 1
            expense_categories[category] = expense_categories.get(category, 0) + amount
            low = f"{category} {(pick(txn, DESCRIPTION_KEYS)[0] if pick(txn, DESCRIPTION_KEYS)[1] else '')}".lower()
            if any(k in low for k in ("car", "vehicle", "fuel", "\u05e8\u05db\u05d1", "\u05d3\u05dc\u05e7")):
                blocked_flags.append((category, amount, vat, "car"))
            elif any(k in low for k in ("meal", "lunch", "restaurant", "hospitality", "gift",
                                        "\u05d0\u05e8\u05d5\u05d7", "\u05db\u05d9\u05d1\u05d5\u05d3",
                                        "\u05d0\u05d9\u05e8\u05d5\u05d7", "\u05de\u05ea\u05e0")):
                blocked_flags.append((category, amount, vat, "hospitality"))
            elif any(k in low for k in ("home", "phone", "internet", "mobile",
                                        "\u05d1\u05d9\u05ea", "\u05d8\u05dc\u05e4\u05d5\u05df",
                                        "\u05d0\u05d9\u05e0\u05d8\u05e8\u05e0\u05d8")):
                mixed_flags.append((category, amount, vat))
        else:
            unknown_types.append(txn_type or "(blank)")

    # Fail loudly rather than reporting a confident zero. Silently returning
    # 0.00 income next to a plausible VAT liability is a filing hazard: the
    # figure looks usable and is not.
    if transactions and unmatched_amount == len(transactions):
        print(
            "Error: no recognised amount column found in the input.\n"
            "  Expected one of: " + ", ".join(AMOUNT_KEYS) + "\n"
            "  Found columns: " + ", ".join(sorted(transactions[0].keys())) + "\n"
            "  Refusing to emit a summary that would report zero income.",
            file=sys.stderr,
        )
        sys.exit(1)
    if unmatched_amount:
        print(
            f"Warning: {unmatched_amount} of {len(transactions)} rows had no recognised "
            "amount column and were counted as 0. Check the column headers before filing.",
            file=sys.stderr,
        )
    if transactions and unmatched_vat == len(transactions):
        print(
            "Error: no recognised VAT column found in the input.\n"
            "  Expected one of: " + ", ".join(VAT_KEYS) + "\n"
            "  Found columns: " + ", ".join(sorted(transactions[0].keys())) + "\n"
            "  Refusing to emit a summary that would report a zero VAT liability.",
            file=sys.stderr,
        )
        sys.exit(1)
    if unmatched_vat:
        print(
            f"Warning: {unmatched_vat} of {len(transactions)} rows had no recognised "
            "VAT column and were counted as 0 VAT. Check the column headers before filing.",
            file=sys.stderr,
        )
    if income_missing_vat:
        print(
            f"Warning: {income_missing_vat} income row(s) carry an amount but 0 VAT. "
            "If these are zero-rated exports that is correct; if the VAT cell was simply "
            "left blank, the VAT collected figure below understates what you owe.",
            file=sys.stderr,
        )

    net_profit = total_income - total_expenses
    vat_liability = vat_collected - vat_paid

    return {
        "total_income": round(total_income, 2),
        "total_expenses": round(total_expenses, 2),
        "net_profit": round(net_profit, 2),
        "vat_collected": round(vat_collected, 2),
        "vat_paid": round(vat_paid, 2),
        "vat_liability": round(vat_liability, 2),
        "income_count": income_count,
        "expense_count": expense_count,
        "total_transactions": income_count + expense_count,
        "income_categories": income_categories,
        "expense_categories": expense_categories,
        "blocked_flags": blocked_flags,
        "mixed_flags": mixed_flags,
        "unknown_types": unknown_types,
    }


def print_summary(summary: dict, period: int, year: int) -> None:
    """Print formatted VAT summary to stdout."""
    start_month, end_month = PERIOD_MONTHS[period]
    month_names = [
        "", "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
    ]

    print(f"\n{'='*60}")
    print(f"  VAT Summary - Period {period} ({month_names[start_month]}-{month_names[end_month]} {year})")
    print(f"  Due date: {PERIOD_DUE_DATES[period]}")
    print("  (statutory: 15 days after the period ends. An osek not required to\n"
          "   file the detailed report who transmits online may report and pay\n"
          "   to the 19th of the following month.)")
    print(f"{'='*60}\n")

    print(f"  Total Income (excl. VAT):     {summary['total_income']:>12,.2f} ILS  ({summary['income_count']} transactions)")
    print(f"  Total Expenses (excl. VAT):   {summary['total_expenses']:>12,.2f} ILS  ({summary['expense_count']} transactions)")
    print(f"  Net Profit:                   {summary['net_profit']:>12,.2f} ILS")
    print()
    print(f"  VAT Collected (on income):    {summary['vat_collected']:>12,.2f} ILS")
    print(f"  VAT Paid (input VAT):         {summary['vat_paid']:>12,.2f} ILS")
    print(f"  ---")
    liab = summary["vat_liability"]
    if liab >= 0:
        print(f"  VAT Liability (to pay):       {liab:>12,.2f} ILS")
    else:
        print(f"  VAT REFUND claim (not a payment): {abs(liab):>9,.2f} ILS")
        print("  A negative balance is a refund claim, which carries its own")
        print("  substantiation requirements. Do not enter it as an amount to pay.")
    print()

    if summary["income_categories"]:
        print("  Income by Category:")
        for cat, total in sorted(summary["income_categories"].items(), key=lambda x: -x[1]):
            print(f"    {cat:<30} {total:>12,.2f} ILS")
        print()
    if summary["expense_categories"]:
        print("  Expenses by Category:")
        for cat, total in sorted(summary["expense_categories"].items(), key=lambda x: -x[1]):
            print(f"    {cat:<30} {total:>12,.2f} ILS")
        print()

    if summary["unknown_types"]:
        print(f"  WARNING: {len(summary['unknown_types'])} row(s) had an unrecognised Type "
              f"and were counted in NEITHER total: {sorted(set(summary['unknown_types']))}")
        print("  Expected 'income'/'expense' or the Hebrew הכנסה/הוצאה.")
        print()

    if summary["blocked_flags"] or summary["mixed_flags"]:
        print("  INPUT VAT REVIEW REQUIRED before filing:")
        for cat, amount, vat, kind in summary["blocked_flags"]:
            if kind == "car":
                print(f"    {cat}: {vat:,.2f} ILS input VAT was included, but VAT on the")
                print("      purchase or import of a private vehicle is NOT deductible at all")
                print("      (Reg. 14), even at 100% business use; running costs are limited.")
            else:
                print(f"    {cat}: {vat:,.2f} ILS input VAT was included, but VAT on")
                print("      hospitality, refreshments and gifts is generally not deductible.")
        for cat, amount, vat in summary["mixed_flags"]:
            print(f"    {cat}: {vat:,.2f} ILS input VAT was included at 100%, but a mixed")
            print("      business/private input is limited to 2/3 (mainly business) or 1/4")
            print("      (mainly private) under Reg. 18.")
        print("  This script SUMS what you recorded; it does not apply these limits.")
        print("  Adjust the input VAT with your accountant before filing.")
        print()

    print(f"{'='*60}\n")


def export_csv(summary: dict, period: int, year: int, output_path: str) -> None:
    """Export summary to CSV file."""
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Category", "Total Amount (ILS)", "Total VAT (ILS)", "Transaction Count"])
        writer.writerow(["Total Income", summary["total_income"], summary["vat_collected"], summary["income_count"]])
        writer.writerow(["Total Expenses", summary["total_expenses"], summary["vat_paid"], summary["expense_count"]])
        writer.writerow(["VAT Liability", "", summary["vat_liability"], ""])
        writer.writerow(["Net Profit", summary["net_profit"], "", ""])
        writer.writerow([])
        writer.writerow(["Income by Category", "Amount (ILS)", "", ""])
        for cat, total in sorted(summary["income_categories"].items(), key=lambda x: -x[1]):
            writer.writerow([cat, round(total, 2), "", ""])
        writer.writerow([])
        writer.writerow(["Expenses by Category", "Amount (ILS)", "", ""])
        for cat, total in sorted(summary["expense_categories"].items(), key=lambda x: -x[1]):
            writer.writerow([cat, round(total, 2), "", ""])

    print(f"Summary exported to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate bi-monthly VAT summary from Google Sheets data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "VAT Periods (Israel, bi-monthly):\n"
            "  1 = Jan-Feb    2 = Mar-Apr    3 = May-Jun\n"
            "  4 = Jul-Aug    5 = Sep-Oct    6 = Nov-Dec\n"
            "\n"
            "Examples:\n"
            "  %(prog)s --input data.json --period 1 --year 2026\n"
            "  %(prog)s --input data.csv --period 3 --year 2026 --output summary.csv\n"
        ),
    )
    parser.add_argument("--input", required=True, help="Path to JSON or CSV data file")
    parser.add_argument("--period", type=int, required=True, choices=range(1, 7), help="VAT period (1-6)")
    parser.add_argument("--year", type=int, required=True, help="Tax year")
    parser.add_argument("--output", help="Optional CSV output path")

    args = parser.parse_args()

    transactions = load_data(args.input)
    if not transactions:
        print("No transactions found in input file.", file=sys.stderr)
        sys.exit(1)

    filtered = filter_by_period(transactions, args.period, args.year)
    if not filtered:
        print(f"No transactions found for period {args.period} ({args.year}).", file=sys.stderr)
        sys.exit(1)

    summary = compute_summary(filtered)
    print_summary(summary, args.period, args.year)

    if args.output:
        export_csv(summary, args.period, args.year, args.output)


if __name__ == "__main__":
    main()
