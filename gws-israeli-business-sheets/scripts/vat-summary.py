#!/usr/bin/env python3
"""Generate bi-monthly VAT summary reports from Google Sheets data.

Reads exported sheet data (JSON or CSV) and produces a VAT period summary
with totals for income, expenses, VAT collected, input VAT, and net liability.

Usage:
  python3 scripts/vat-summary.py --input data.json --period 1 --year 2026
  python3 scripts/vat-summary.py --input data.csv --period 3 --year 2026 --output summary.csv
  python3 scripts/vat-summary.py --input data.json --month 7 --year 2026   # monthly filer
  python3 scripts/vat-summary.py --input data.json --full-year --year 2026 --osek-patur
  python3 scripts/vat-summary.py --help

Input: the JSON that `gws sheets +read` or `gws sheets spreadsheets values get`
prints (a ValueRange object, {"range": ..., "values": [[header...], [row...]]}),
the NDJSON that `--page-all` prints, a plain array of rows, an array of objects,
or a CSV export with a header row.

VAT Periods (Israel, bi-monthly):
  1 = Jan-Feb    2 = Mar-Apr    3 = May-Jun
  4 = Jul-Aug    5 = Sep-Oct    6 = Nov-Dec
Businesses above the monthly-filing turnover threshold report every month:
use --month instead of --period.
"""

import argparse
import csv
import json
import re
import sys
from datetime import date, datetime, timedelta
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

MONTH_NAMES = [
    "", "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]

# Allocation-number (מספר הקצאה) thresholds, amount before VAT. The rule
# applies when the amount EXCEEDS the threshold in force on the invoice date.
# Nothing before May 2024. Re-check before relying on it: it has been lowered
# repeatedly.
ALLOCATION_THRESHOLDS = [
    (date(2024, 5, 1), 25000),
    (date(2025, 1, 1), 20000),
    (date(2026, 1, 1), 10000),
    (date(2026, 6, 1), 5000),
]

# Osek patur annual turnover ceiling, by year. Revised each January.
OSEK_PATUR_CEILING = {2025: 120000, 2026: 122833}

DATE_KEYS = ("Date", "date", "תאריך")
TYPE_KEYS = ("Type", "type", "סוג")
CATEGORY_KEYS = ("Category", "category", "קטגוריה")
DESCRIPTION_KEYS = ("Description", "description", "תיאור")
AMOUNT_KEYS = ("Amount (excl. VAT)", "amount", "Amount", "amount_excl_vat",
               "Amount excl VAT", 'סכום (ללא מע"מ)', "סכום")
VAT_KEYS = ("VAT (18%)", "VAT (17%)", "vat", "VAT",
            'מע"מ', 'מע"מ (18%)', 'מע"מ (17%)')
ALLOCATION_KEYS = ("Allocation #", "Allocation", "allocation", "מספר הקצאה")
INVOICE_KEYS = ("Invoice #", "Invoice", "invoice", "מספר חשבונית")
WITHHOLDING_KEYS = ("Withholding", "withholding", "ניכוי במקור")

SHEETS_EPOCH = date(1899, 12, 30)


def allocation_threshold(d: date) -> int | None:
    """Threshold in force on date d, or None before the regime began."""
    current = None
    for start, amount in ALLOCATION_THRESHOLDS:
        if d >= start:
            current = amount
    return current


def parse_date(value) -> date | None:
    """Parse DD/MM/YYYY (and ISO), or a Google Sheets date serial number.

    A serial is what UNFORMATTED_VALUE returns for a date cell.
    """
    if value is None:
        return None
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        serial = float(value)
    else:
        s = str(value).strip()
        if re.fullmatch(r"\d{5}(\.\d+)?", s):
            serial = float(s)
        else:
            for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%d.%m.%Y"):
                try:
                    return datetime.strptime(s, fmt).date()
                except ValueError:
                    continue
            return None
    if 20000 <= serial <= 80000:
        return SHEETS_EPOCH + timedelta(days=int(serial))
    return None


def looks_us_format(value) -> bool:
    """True for M/D/YYYY strings that cannot be D/M (second part above 12)."""
    m = re.fullmatch(r"\s*(\d{1,2})/(\d{1,2})/(\d{4})\s*", str(value))
    return bool(m) and int(m.group(1)) <= 12 < int(m.group(2))


class AmountParseError(ValueError):
    """Raised when a non-empty cell cannot be read as a number."""


def parse_amount(amount_str) -> float:
    """Parse an amount cell into a float.

    Handles the shekel sign, thousands separators, currency words, direction
    marks, a Unicode minus, the accounting-format zero ("₪ -") and
    parenthesised negatives. The Sheets API returns FORMATTED_VALUE by default,
    so a column formatted as ILS currency arrives as a string with the shekel
    sign and thousands separators. Silently turning that into 0.0 is how this script used to
    print a confident all-zero VAT report, so an unparseable non-empty cell
    raises instead.
    """
    if amount_str is None:
        return 0.0
    if isinstance(amount_str, (int, float)) and not isinstance(amount_str, bool):
        return float(amount_str)
    raw = str(amount_str).strip()
    if not raw:
        return 0.0
    cleaned = re.sub(r"[‎‏‪-‮⁦-⁩]", "", raw)
    cleaned = cleaned.replace("−", "-")
    for token in ("₪", "ILS", "NIS", "ש\"ח", "שקל"):
        cleaned = cleaned.replace(token, "")
    cleaned = cleaned.replace(" ", " ").replace(" ", "")
    trailing_minus = cleaned.endswith("-") and len(cleaned) > 1
    if trailing_minus:
        cleaned = cleaned[:-1]  # "1,234.00-" accounting style
    if cleaned.startswith("+"):
        cleaned = cleaned[1:]
    if "," not in cleaned and re.fullmatch(r"[-(]*\d{1,3}(\.\d{3})+\)?", cleaned):
        # "9.000" or "1.234.567": dot-grouped thousands from a non-Israeli
        # locale (Germany, Italy, Turkey ...). Read as a decimal it would be
        # 1000x too small, so refuse it. Israeli amounts carry 2 decimals.
        raise AmountParseError(
            f"{raw!r} looks like a dot used as a thousands separator. The sheet is "
            "probably set to a non-Israeli locale. Set File > Settings > Locale to Israel, "
            "or re-read the range with valueRenderOption=UNFORMATTED_VALUE, and run again."
        )
    if "," in cleaned:
        # Israeli formatting uses the comma ONLY as a thousands separator, in
        # groups of exactly three digits before any decimal point. A decimal
        # comma ("4000,50", a European-locale sheet) or a dot-then-comma
        # pattern ("1.234,56") cannot be read safely, so refuse it rather than
        # strip the comma and report 400,050.
        if not re.fullmatch(r"[-(]*\d{1,3}(,\d{3})+(\.\d+)?\)?", cleaned):
            raise AmountParseError(
                f"{raw!r} has a comma that is not a thousands separator (a decimal comma, "
                "or a mixed 1.234,56 style). The sheet is probably set to a non-Israeli "
                "locale. Set File > Settings > Locale to Israel, or re-read the range with "
                "valueRenderOption=UNFORMATTED_VALUE, and run again."
            )
        cleaned = cleaned.replace(",", "")
    if cleaned in ("", "-"):
        return 0.0
    negative = cleaned.startswith("(") and cleaned.endswith(")")
    if negative:
        cleaned = cleaned[1:-1]
    try:
        value = float(cleaned)
        if value != value or value in (float("inf"), float("-inf")):
            raise ValueError("not a finite number")
    except ValueError:
        raise AmountParseError(
            f"could not read {raw!r} as a number. If the cell is currency-formatted, "
            "re-read the range with valueRenderOption=UNFORMATTED_VALUE (dates then "
            "arrive as serial numbers, which this script also reads)."
        )
    if negative and trailing_minus:
        raise AmountParseError(f"{raw!r} is marked negative twice (parentheses and a trailing minus).")
    return -value if negative or trailing_minus else value


def rows_to_dicts(rows: list) -> list[dict]:
    """Turn [header, row, row...] into dicts.

    The Sheets API drops trailing empty cells, so a row is often shorter than
    the header. Pad it rather than letting zip() silently drop columns. A row
    identical to the header (a repeated header) is skipped.
    """
    if not rows:
        return []
    headers = [str(h).strip() for h in rows[0]]
    out = []
    for row in rows[1:]:
        if not any(str(c).strip() for c in row):
            continue
        if [str(c).strip() for c in row] == headers:
            continue
        padded = list(row) + [""] * (len(headers) - len(row))
        out.append(dict(zip(headers, padded)))
    return out


def load_data(input_path: str) -> list[dict]:
    """Load transaction data from JSON, NDJSON or CSV file."""
    path = Path(input_path)

    if path.suffix in (".json", ".ndjson", ".jsonl"):
        text = path.read_text(encoding="utf-8").strip()
        if not text:
            return []
        try:
            docs = [json.loads(text)]
        except json.JSONDecodeError:
            # `gws ... --page-all` prints one JSON object per line (NDJSON).
            docs = [json.loads(line) for line in text.splitlines() if line.strip()]
        rows: list = []
        objects: list[dict] = []
        for data in docs:
            if isinstance(data, dict) and "error" in data and "values" not in data:
                print(f"Error: the input file is a gws error response: {data['error']}",
                      file=sys.stderr)
                sys.exit(1)
            if isinstance(data, dict):
                # A gws/Sheets ValueRange: the cells live under "values". An
                # empty range has no "values" key at all.
                rows.extend(data.get("values", []))
            elif isinstance(data, list) and data and isinstance(data[0], list):
                rows.extend(data)
            elif isinstance(data, list):
                objects.extend(d for d in data if isinstance(d, dict))
        if objects:
            return objects
        return rows_to_dicts(rows)

    elif path.suffix == ".csv":
        # utf-8-sig: a CSV saved from Excel or Sheets often starts with a BOM,
        # which would otherwise glue itself to the first header name.
        with open(path, encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            # Skip a repeated header row (pasted twice, or a merged export).
            return [r for r in reader
                    if [str(v).strip() for v in r.values()] != [str(k).strip() for k in r.keys()]]

    else:
        print(f"Error: Unsupported file format '{path.suffix}'. Use .json or .csv", file=sys.stderr)
        sys.exit(1)


def pick(txn: dict, keys) -> tuple:
    """Return (value, found) for the first key present with a non-empty value."""
    for k in keys:
        # None: a short CSV row (DictReader) or a JSON null. Not a value.
        if k in txn and txn[k] is not None and str(txn[k]).strip() != "":
            return txn[k], True
    return "", False


# Column K values that mean "no number yet", not a number.
ALLOCATION_PLACEHOLDERS = {"?", "x", "no", "none", "null", "nil", "n/a", "na", "missing", "tbd",
                           "pending", "no number", "none yet", "אין", "חסר", "ללא", "לא",
                           "ממתין", "בהמתנה", "אין מספר", "לא קיים", "טרם", "אין הקצאה"}


def allocation_status(value) -> str:
    """'ok', 'missing' or 'verify' for a column K cell.

    The Tax Authority's API spec (Israel Invoice model, v2.0, 7.2024) defines
    the full allocation number (Confirmation_Number) as up to 30 characters
    (its examples are 26 digits) and the SHORT allocation number as its
    rightmost 9 digits, which may be reported instead. Only those two shapes
    are accepted. Anything else non-empty is flagged for checking, never
    silently accepted: a number cell can lose leading zeros or precision.
    """
    if value is None:
        return "missing"
    if isinstance(value, float):
        if abs(value) > 2 ** 53:
            return "verify"  # a long number stored as a float has lost digits
        if value.is_integer():
            value = int(value)
    raw = re.sub(r"[\u200e\u200f\u202a-\u202e\u2066-\u2069]", "", str(value)).strip()
    if not raw:
        return "missing"
    # Dashes of any kind (hyphen, en dash, em dash, minus), zeros, dots.
    if (" ".join(raw.lower().split()) in ALLOCATION_PLACEHOLDERS
            or re.fullmatch(r"[0\s.\-\u2010-\u2015\u2212]+", raw)):
        return "missing"
    compact = re.sub(r"[\s\u00a0-]", "", raw)
    compact = re.sub(r"(?<=\d)\.0+$", "", compact)  # 123456789.0 from a number cell
    if re.fullmatch(r"\d{9}|\d{26}", compact):
        return "ok"
    return "verify"


def has_column(transactions: list[dict], keys) -> bool:
    return any(k in txn for txn in transactions for k in keys)


def filter_rows(transactions: list[dict], year: int, months: tuple[int, int]) -> list[tuple]:
    """Return [(date, txn)] for rows dated inside the given months of year."""
    start_month, end_month = months
    filtered = []
    undated = 0
    us_like = []
    for txn in transactions:
        raw = pick(txn, DATE_KEYS)[0]
        d = parse_date(raw)
        if d is None:
            if looks_us_format(raw):
                us_like.append(str(raw))
            undated += 1
            continue
        if d.year == year and start_month <= d.month <= end_month:
            filtered.append((d, txn))

    if us_like:
        print(
            "Error: some dates look like US month/day/year (e.g. "
            f"{', '.join(us_like[:3])}). The sheet is probably set to a US locale, so "
            "EVERY date may be read with day and month swapped. Set the spreadsheet "
            "locale to Israel (File > Settings) so dates are DD/MM/YYYY, re-read the "
            "range, and run again.",
            file=sys.stderr,
        )
        sys.exit(1)
    if undated:
        print(
            f"Warning: {undated} row(s) had no date the script could read (expected "
            "DD/MM/YYYY) and were left out of every period. Check them before filing.",
            file=sys.stderr,
        )
    return filtered


def words(text: str) -> set:
    return set(re.findall(r"[a-z]+", text.lower()))


CAR_EN = {"car", "cars", "vehicle", "vehicles", "fuel", "petrol", "gasoline", "diesel",
          "leasing", "parking", "toll", "pango"}
CAR_HE = ("רכב", "דלק", "ליסינג",
          "חניה", "חנייה", "פנגו")
CAR_HE_EXCLUDE = ("רכבת", "רכבות", "הרכבה", "הרכבות")  # train(s); assembly / installation
HOSP_EN = {"meal", "meals", "lunch", "dinner", "breakfast", "restaurant", "hospitality",
           "entertainment", "gift", "gifts", "coffee", "refreshments"}
HOSP_HE = ("אירוח", "ארוח", "כיבוד",
           "מסעדה", "מתנ")
HOSP_HE_EXCLUDE = ("אירוח אתר", "מתנדב")  # web hosting; volunteers
MIXED_EN = {"phone", "cellphone", "internet"}
MIXED_PHRASES = ("home office", "mobile phone")
MIXED_HE = ("טלפון", "סלולר",
            "אינטרנט", "משרד ביתי")


def he_hit(label: str, needles, excludes=()) -> bool:
    for ex in excludes:
        label = label.replace(ex, " ")
    return any(n in label for n in needles)


def classify_input(label: str) -> str | None:
    """'car', 'hospitality', 'mixed' or None. Advisory only."""
    w = words(label)
    low = label.lower()
    if w & CAR_EN or he_hit(label, CAR_HE, CAR_HE_EXCLUDE):
        return "car"
    if w & HOSP_EN or he_hit(label, HOSP_HE, HOSP_HE_EXCLUDE):
        return "hospitality"
    if w & MIXED_EN or any(p in low for p in MIXED_PHRASES) or he_hit(label, MIXED_HE):
        return "mixed"
    return None


IMPORT_EN = {"customs", "import", "imports"}
# Whole Hebrew words only, so יבואן (importer) and מכסה / מכסת (quota) do not hit.
IMPORT_HE = {"רשימון", "רשימונים", "מכס", "יבוא", "ייבוא"}
HE_PREFIXES = set("והבלמשכ")


def he_word_hit(label: str, stems: set) -> bool:
    """True if a Hebrew word in label is one of stems, allowing up to three
    one-letter prefixes (ו, ה, ב, ל, מ, ש, כ), as in "ביבוא" or "והמכס"."""
    for token in re.findall(r"[\u05d0-\u05ea]+", label):
        for i in range(min(3, len(token) - 1) + 1):
            if i and token[i - 1] not in HE_PREFIXES:
                break
            if token[i:] in stems:
                return True
    return False


# A customs broker's or forwarder's own fee is an ordinary tax invoice that
# does need an allocation number, so a row naming one stays in the check.
BROKER_EN = {"broker", "brokers", "brokerage", "forwarder", "forwarding", "agent"}
BROKER_HE = {"עמיל", "עמילות", "שילוח", "משלח"}


def is_import(label: str) -> bool:
    """Import VAT is paid at customs on an entry (רשימון), not a tax invoice."""
    if words(label) & BROKER_EN or he_word_hit(label, BROKER_HE):
        return False
    return bool(words(label) & IMPORT_EN) or he_word_hit(label, IMPORT_HE)


def is_zero_rated_category(category: str) -> bool:
    """A row is treated as zero-rated only when its CATEGORY says so.

    The description is deliberately ignored: "data export module" is ordinary
    taxable work, and matching it would hide a forgotten VAT cell.
    """
    c = category.strip().lower()
    if re.search(r"zero[- ]rated|(^|\W)0%|שיעור אפס", c):
        return True
    return c.startswith("export") or c.startswith("יצוא") or c.startswith("ייצוא")


# For an osek patur the turnover is the GROSS amount, so the gross headers win
# over a leftover net column from the osek murshe template.
PATUR_AMOUNT_KEYS = ("Total (incl. VAT)", 'סכום כולל מע"מ', "Total", "total",
                     "Amount", "amount", "סכום")


def cell_amount(value, d: date, column: str, description: str) -> float:
    """parse_amount, with the row named in the error."""
    try:
        return parse_amount(value)
    except AmountParseError as e:
        raise AmountParseError(f"row dated {d.strftime('%d/%m/%Y')} ({description or 'no description'}), "
                               f"{column} cell: {e}") from None


def compute_summary(rows: list[tuple], osek_patur: bool = False) -> dict:
    """Compute the summary from [(date, txn)] rows."""
    transactions = [t for _, t in rows]
    # An osek patur sheet may have kept the murshe header for its gross column.
    amount_keys = PATUR_AMOUNT_KEYS + AMOUNT_KEYS if osek_patur else AMOUNT_KEYS
    s = {
        "total_income": 0.0, "total_expenses": 0.0, "vat_collected": 0.0, "vat_paid": 0.0,
        "income_count": 0, "expense_count": 0, "withholding": 0.0, "withheld_from_suppliers": 0.0,
        "zero_rated_income": 0.0, "zero_rated_count": 0,
        "income_categories": {}, "expense_categories": {},
        "input_flags": [], "alloc_expense": [], "alloc_income": [], "unknown_types": [],
        "alloc_unchecked": 0, "duplicates": [], "export_with_vat": [],
    }
    unmatched_amount = unmatched_vat = income_missing_vat = 0
    has_alloc_col = has_column(transactions, ALLOCATION_KEYS)
    alloc_unchecked = 0
    s["import_rows"] = []
    s["verify_alloc"] = []
    patur_net_differs = []
    seen: dict = {}
    for d, txn in rows:
        key = tuple(sorted((str(k), str(v).strip()) for k, v in txn.items() if v is not None))
        seen[key] = seen.get(key, 0) + 1
        if seen[key] == 2:
            s["duplicates"].append([d.strftime("%d/%m/%Y"), str(pick(txn, DESCRIPTION_KEYS)[0]), key])
    for dup in s["duplicates"]:
        dup[2] = seen[dup[2]]  # times the row is counted
    if s["duplicates"]:
        print(f"Warning: {len(s['duplicates'])} row(s) appear more than once, identical in every "
              "column, and each copy is counted: "
              + "; ".join(f"{d} {w} (x{n})" for d, w, n in s["duplicates"][:5])
              + ". Delete accidental copies; keep them only if they really are separate invoices.",
              file=sys.stderr)

    for d, txn in rows:
        txn_type = str(pick(txn, TYPE_KEYS)[0]).strip().lower()
        raw_amount, found_amount = pick(txn, amount_keys)
        if not found_amount:
            unmatched_amount += 1
        description = str(pick(txn, DESCRIPTION_KEYS)[0])
        amount = cell_amount(raw_amount, d, "amount", description)
        if osek_patur:
            net_raw, net_found = pick(txn, ("Amount (excl. VAT)", 'סכום (ללא מע"מ)'))
            if net_found and abs(cell_amount(net_raw, d, "net amount", description) - amount) > 0.005:
                patur_net_differs.append(d.strftime("%d/%m/%Y"))
        raw_vat, found_vat = pick(txn, VAT_KEYS)
        if not found_vat:
            unmatched_vat += 1
        vat = 0.0 if osek_patur else cell_amount(raw_vat, d, "VAT", description)
        category_raw, has_cat = pick(txn, CATEGORY_KEYS)
        category = str(category_raw).strip() if has_cat else "Uncategorized"
        label = f"{category} {description}"
        withheld = cell_amount(pick(txn, WITHHOLDING_KEYS)[0], d, "withholding", description)
        # Zero-rated only when the category says so AND no VAT was charged: a
        # row carrying VAT is by definition not zero-rated, whatever its label.
        zero_rated_cat = is_zero_rated_category(category)
        zero_rated = zero_rated_cat and vat == 0
        if zero_rated_cat and vat != 0 and not osek_patur:
            s["export_with_vat"].append((d.strftime("%d/%m/%Y"), description or category, category, vat))
            print(f"Warning: '{category}' is marked export / zero-rated but carries "
                  f"{vat:,.2f} VAT; it is counted as an ordinary taxable row"
                  + (" and included in the allocation-number check" if vat > 0 else "")
                  + ". Check the row.",
                  file=sys.stderr)

        # Allocation number: the BUYER loses the input-VAT deduction on an
        # invoice above the threshold that has no number (VAT Law s.38(a1)),
        # whether or not the buyer asked for one.
        threshold = allocation_threshold(d)
        kind_of = ("expense" if txn_type in ("expense", "הוצאה")
                   else "income" if txn_type in ("income", "הכנסה") else None)
        if not osek_patur and threshold is not None and vat > 0 and not zero_rated and kind_of:
            if kind_of == "expense" and is_import(label):
                s["import_rows"].append((d.strftime("%d/%m/%Y"), description or category))
            elif amount > threshold:
                # Tested per ROW. Invoice numbers are not grouped: supplier
                # numbers repeat across suppliers and the sheet has no supplier
                # column, so a shared number proves nothing.
                if not has_alloc_col:
                    alloc_unchecked += 1
                elif (status := allocation_status(pick(txn, ALLOCATION_KEYS)[0])) == "verify":
                    s["verify_alloc"].append((d.strftime("%d/%m/%Y"), description or category,
                                              amount, vat, kind_of,
                                              str(pick(txn, ALLOCATION_KEYS)[0]).strip()))
                elif status == "missing":
                    entry = (d.strftime("%d/%m/%Y"), description or category, amount, vat,
                             threshold, pick(txn, INVOICE_KEYS)[1])
                    s["alloc_expense" if kind_of == "expense" else "alloc_income"].append(entry)

        if txn_type in ("income", "הכנסה"):
            if zero_rated:
                s["zero_rated_count"] += 1
                s["zero_rated_income"] += amount
            elif zero_rated_cat:
                pass  # carries VAT: warned above, counted as taxable
            elif found_vat and vat == 0 and amount != 0 and not osek_patur:
                income_missing_vat += 1
            # Withheld from YOU by a client: a credit against your tax.
            s["withholding"] += withheld
            s["total_income"] += amount
            s["vat_collected"] += vat
            s["income_count"] += 1
            s["income_categories"][category] = s["income_categories"].get(category, 0) + amount
        elif txn_type in ("expense", "הוצאה"):
            # Withheld BY you from a supplier: you owe it to the Tax Authority.
            s["withheld_from_suppliers"] += withheld
            s["total_expenses"] += amount
            s["vat_paid"] += vat
            s["expense_count"] += 1
            s["expense_categories"][category] = s["expense_categories"].get(category, 0) + amount
            kind = classify_input(label)
            if kind and vat and not osek_patur:
                s["input_flags"].append((category, vat, kind))
        else:
            s["unknown_types"].append(txn_type or "(blank)")

    # Fail loudly rather than reporting a confident zero.
    if transactions and unmatched_amount == len(transactions):
        print(
            "Error: no recognised amount column found in the input.\n"
            "  Expected one of: " + ", ".join(amount_keys) + "\n"
            "  Found columns: " + ", ".join(sorted(transactions[0].keys())) + "\n"
            "  Refusing to emit a summary that would report zero income.",
            file=sys.stderr,
        )
        sys.exit(1)
    if patur_net_differs:
        print(f"Warning: {len(patur_net_differs)} row(s) have both a net 'Amount (excl. VAT)' and a gross "
              f"total that differ ({', '.join(patur_net_differs[:5])}). For an osek patur the turnover "
              "is the gross total, so the gross column was used.", file=sys.stderr)
    if unmatched_amount:
        print(f"Warning: {unmatched_amount} of {len(transactions)} rows had no recognised "
              "amount and were counted as 0. Check the column headers before filing.",
              file=sys.stderr)
    if not osek_patur:
        if transactions and unmatched_vat == len(transactions):
            print(
                "Error: no recognised VAT column found in the input.\n"
                "  Expected one of: " + ", ".join(VAT_KEYS) + "\n"
                "  Found columns: " + ", ".join(sorted(transactions[0].keys())) + "\n"
                "  Refusing to emit a summary that would report a zero VAT liability.\n"
                "  For an osek patur sheet (no VAT column), run with --osek-patur.",
                file=sys.stderr,
            )
            sys.exit(1)
        if unmatched_vat:
            print(f"Warning: {unmatched_vat} of {len(transactions)} rows had no recognised "
                  "VAT value and were counted as 0 VAT. Check them before filing.",
                  file=sys.stderr)
        if income_missing_vat:
            print(
                f"Warning: {income_missing_vat} income row(s) carry an amount but 0 VAT and "
                "their category is not marked export / zero-rated. If the VAT cell was simply "
                "left blank, the VAT collected figure understates what you owe. Give genuine "
                "zero-rated exports the category 'Export (zero-rated)' / "
                "'יצוא (מע\"מ 0%)'.",
                file=sys.stderr,
            )
        s["alloc_unchecked"] = alloc_unchecked
        if alloc_unchecked:
            print(f"Warning: {alloc_unchecked} row(s) exceed the allocation-number threshold for "
                  "their date, but the input has no 'Allocation #' / 'מספר "
                  "הקצאה' column, so they could not be checked.",
                  file=sys.stderr)

    for key in ("total_income", "total_expenses", "vat_collected", "vat_paid",
                "withholding", "withheld_from_suppliers", "zero_rated_income"):
        s[key] = round(s[key], 2)
    s["income_minus_expenses"] = round(s["total_income"] - s["total_expenses"], 2)
    s["vat_liability"] = round(s["vat_collected"] - s["vat_paid"], 2)
    # Only rows with an invoice number recorded are summed here, and only on the
    # assumption that each is ONE tax invoice; an unnumbered row may sum several
    # smaller invoices.
    s["input_vat_no_allocation"] = round(sum(e[3] for e in s["alloc_expense"] if e[5]), 2)
    s["total_transactions"] = s["income_count"] + s["expense_count"]
    return s


def patur_ceiling_status(income: float, ceiling: float) -> str | None:
    if income > ceiling:
        return "exceeded"
    if income >= 0.9 * ceiling:
        return "near"
    return None


def period_label(period, month, full_year, year) -> tuple[str, str]:
    if full_year:
        return f"Full year {year}", "n/a (annual view)"
    if month is not None:
        due = MONTH_NAMES[month % 12 + 1] + " 15" + (" (next year)" if month == 12 else "")
        return f"monthly filer ({MONTH_NAMES[month]} {year})", due
    start, end = PERIOD_MONTHS[period]
    return f"Period {period} ({MONTH_NAMES[start]}-{MONTH_NAMES[end]} {year})", PERIOD_DUE_DATES[period]


def print_summary(s: dict, title: str, due: str, year: int, osek_patur: bool) -> None:
    print(f"\n{'='*64}")
    print(f"  {'Osek patur summary' if osek_patur else 'VAT Summary'} - {title}")
    if not osek_patur:
        print(f"  Due date: {due}")
        print("  (statutory: 15 days after the period ends. An osek not required to\n"
              "   file the detailed report who transmits online may report and pay\n"
              "   to the 19th of the following month. Detailed-report (PCN874)\n"
              "   filers report on the 23rd.)")
    print(f"{'='*64}\n")

    gross = "" if osek_patur else " (excl. VAT)"
    print(f"  Total Income{gross}:".ljust(32) + f"{s['total_income']:>12,.2f} ILS  ({s['income_count']} transactions)")
    print(f"  Total Expenses{gross}:".ljust(32) + f"{s['total_expenses']:>12,.2f} ILS  ({s['expense_count']} transactions)")
    print("  Income minus expenses:".ljust(32) + f"{s['income_minus_expenses']:>12,.2f} ILS")
    print("  (as recorded, NOT taxable profit: equipment is depreciated and some\n"
          "   expenses are only partly deductible)")
    if s["withholding"]:
        print("  Tax clients withheld from you:".ljust(32) + f"{s['withholding']:>12,.2f} ILS  (credited against advances and annual tax)")
    if s["withheld_from_suppliers"]:
        print("  Tax you withheld from suppliers:".ljust(32) + f"{s['withheld_from_suppliers']:>12,.2f} ILS  (you owe this to the Tax Authority, not a credit)")
    print()

    if osek_patur:
        ceiling = OSEK_PATUR_CEILING.get(year)
        if ceiling:
            print(f"  Osek patur turnover ceiling for {year}: {ceiling:,.0f} ILS (annual turnover,")
            print("  not profit). Declare the year's turnover to VAT by 31 January of the")
            print("  following year.")
            status = patur_ceiling_status(s["total_income"], ceiling)
            if status == "exceeded":
                print(f"  CEILING EXCEEDED: this run alone shows {s['total_income']:,.2f} ILS of income.")
                print("  Crossing the ceiling means converting to osek murshe. Contact your")
                print("  accountant / the VAT office now.")
            elif status == "near":
                print(f"  NEAR THE CEILING: {s['total_income']:,.2f} ILS is close to it. If this is")
                print("  not the full year, the rest of the year may push you over.")
        else:
            print(f"  No osek patur ceiling is recorded here for {year}; check the current figure.")
        print(f"\n{'='*64}\n")
        return

    if s["zero_rated_count"]:
        print("  of which zero-rated / export:".ljust(32) + f"{s['zero_rated_income']:>12,.2f} ILS  ({s['zero_rated_count']} transactions, 0% VAT)")
        print()
    print("  VAT Collected (on income):".ljust(32) + f"{s['vat_collected']:>12,.2f} ILS")
    print("  Input VAT as recorded:".ljust(32) + f"{s['vat_paid']:>12,.2f} ILS")
    print("  ---")
    liab = s["vat_liability"]
    if liab >= 0:
        print("  VAT Liability (to pay):".ljust(32) + f"{liab:>12,.2f} ILS")
    else:
        print(f"  VAT REFUND claim (not a payment): {abs(liab):>9,.2f} ILS")
        print("  A negative balance is a refund claim, which carries its own")
        print("  substantiation requirements. Do not enter it as an amount to pay.")
    print("  The input VAT above is what you RECORDED, summed. It is not necessarily")
    print("  what you may deduct: check the limits below with your accountant.")
    print()

    single = [e for e in s["alloc_expense"] if e[5]]
    unknown = [e for e in s["alloc_expense"] if not e[5]]
    if single:
        at_risk = s["input_vat_no_allocation"]
        print("  INPUT VAT AT RISK without an allocation number (VAT Law s.38(a1)): rows")
        print("  above the threshold for their date with an invoice number but no allocation")
        print("  number. If a row is ONE tax invoice, its input VAT is not deductible until")
        print("  the supplier adds a number. If it is only part of a larger invoice, test")
        print("  the whole invoice instead:")
        for d, what, amount, vat, thr, _ in single:
            print(f"    {d}  {what[:30]:<30} {amount:>11,.2f} + VAT {vat:,.2f}  (threshold {thr:,})")
        print(f"  Input VAT at risk: {at_risk:,.2f} ILS. If the suppliers cannot add numbers,")
        print(f"  net VAT becomes {liab + at_risk:,.2f} ILS (positive = to pay, negative = refund).")
        print()
    if unknown:
        print("  CHECK PER INVOICE: rows above the threshold with no invoice number and no")
        print("  allocation number. If a row is ONE tax invoice it needs a number; if it sums")
        print("  several smaller invoices, check each invoice instead:")
        for d, what, amount, vat, thr, _ in unknown:
            print(f"    {d}  {what[:30]:<30} {amount:>11,.2f} + VAT {vat:,.2f}  (threshold {thr:,})")
        print()
    if s["verify_alloc"]:
        print("  VERIFY THE ALLOCATION NUMBER: rows above the threshold whose column K is not")
        print("  a 9-digit short number or a 26-digit full number. It may be a valid number")
        print("  that lost digits in a number-formatted cell, or a note. Check it against the")
        print("  invoice; these rows are NOT in the at-risk figure above:")
        for d, what, amount, vat, kind, val in s["verify_alloc"]:
            print(f"    {d}  {what[:30]:<30} {amount:>11,.2f} + VAT {vat:,.2f}  ({kind}, K = {val!r})")
        print()
    if s["import_rows"]:
        print("  Import row(s) skipped in the allocation check (import VAT is paid on a")
        print("  customs entry, רשימון, not a tax invoice). Check these really are imports:")
        for d, what in s["import_rows"]:
            print(f"    {d}  {what[:50]}")
        print()
    if s["alloc_income"]:
        print("  YOUR invoices above the threshold with no allocation number. This matters only")
        print("  if the customer is an osek murshe (who loses the deduction without one and")
        print("  may ask you for it); a sale to a private customer needs none:")
        for d, what, amount, vat, thr, _ in s["alloc_income"]:
            print(f"    {d}  {what[:30]:<30} {amount:>11,.2f} + VAT {vat:,.2f}  (threshold {thr:,})")
        print()

    if s["income_categories"]:
        print("  Income by Category:")
        for cat, total in sorted(s["income_categories"].items(), key=lambda x: -x[1]):
            print(f"    {cat:<30} {total:>12,.2f} ILS")
        print()
    if s["expense_categories"]:
        print("  Expenses by Category:")
        for cat, total in sorted(s["expense_categories"].items(), key=lambda x: -x[1]):
            print(f"    {cat:<30} {total:>12,.2f} ILS")
        print()

    if s["unknown_types"]:
        print(f"  WARNING: {len(s['unknown_types'])} row(s) had an unrecognised Type "
              f"and were counted in NEITHER total: {sorted(set(s['unknown_types']))}")
        print("  Expected 'income'/'expense' or the Hebrew הכנסה/הוצאה.")
        print()

    if s["input_flags"]:
        print("  INPUT VAT REVIEW REQUIRED before filing (matched by keyword, advisory):")
        for cat, vat, kind in s["input_flags"]:
            if kind == "car":
                print(f"    {cat}: {vat:,.2f} ILS. VAT on buying or leasing a private vehicle is")
                print("      NOT deductible (Reg. 14(a)). Running costs (fuel, repairs) are limited")
                print("      to 2/3 if the car is mainly used for business, 1/4 otherwise (Reg. 18(b)).")
            elif kind == "hospitality":
                print(f"    {cat}: {vat:,.2f} ILS. VAT on hospitality (אירוח) is not deductible")
                print("      (Reg. 16), except hosting a guest from abroad. Confirm refreshments")
                print("      and gifts with your accountant.")
            else:
                print(f"    {cat}: {vat:,.2f} ILS was included at 100%, but a mixed")
                print("      business/private input is limited to 2/3 (mainly business) or 1/4")
                print("      (mainly private) under Reg. 18.")
        print("  The keyword match can miss rows and can flag the wrong ones; review every")
        print("  expense category yourself.")
        print()

    print(f"{'='*64}\n")


def export_csv(s: dict, title: str, output_path: str, osek_patur: bool, year: int) -> None:
    """Export summary to CSV file, including every flag."""
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([title])
        w.writerow(["Category", "Total Amount (ILS)", "Total VAT (ILS)", "Transaction Count"])
        w.writerow(["Total Income", s["total_income"], "" if osek_patur else s["vat_collected"], s["income_count"]])
        if not osek_patur:
            w.writerow(["of which zero-rated / export", s["zero_rated_income"], 0, s["zero_rated_count"]])
        w.writerow(["Total Expenses", s["total_expenses"], "" if osek_patur else s["vat_paid"], s["expense_count"]])
        if not osek_patur:
            w.writerow(["VAT Liability (input VAT as recorded)", "", s["vat_liability"], ""])
            w.writerow(["Input VAT at risk: rows with an invoice number above the threshold and no allocation number, if each row is one tax invoice (imports and unnumbered rows excluded)", "", s["input_vat_no_allocation"], len([e for e in s["alloc_expense"] if e[5]])])
        if not osek_patur and s["alloc_unchecked"]:
            w.writerow([f"Allocation-number check NOT RUN for {s['alloc_unchecked']} row(s) above the threshold: the input has no Allocation # column", "", "", s["alloc_unchecked"]])
        for d, what, cat, vat in s["export_with_vat"]:
            w.writerow([f"Row {d} {what}: category '{cat}' says export / zero-rated but the row carries VAT; counted as taxable, check it", "", vat, ""])
        if s["duplicates"]:
            for d, what, n in s["duplicates"]:
                w.writerow([f"Row {d} {what} appears {n} times, identical in every column, and is counted {n} times; check it", "", "", n])
        w.writerow(["Income minus expenses (as recorded, not taxable profit)", s["income_minus_expenses"], "", ""])
        w.writerow(["Tax clients withheld from you (credit)", s["withholding"], "", ""])
        w.writerow(["Tax you withheld from suppliers (owed to the Tax Authority)", s["withheld_from_suppliers"], "", ""])
        if osek_patur:
            ceiling = OSEK_PATUR_CEILING.get(year)
            status = patur_ceiling_status(s["total_income"], ceiling) if ceiling else None
            if status:
                w.writerow([f"OSEK PATUR CEILING {status.upper()}", s["total_income"], "", ceiling])
        w.writerow([])
        w.writerow(["Income by Category", "Amount (ILS)", "", ""])
        for cat, total in sorted(s["income_categories"].items(), key=lambda x: -x[1]):
            w.writerow([cat, round(total, 2), "", ""])
        w.writerow([])
        w.writerow(["Expenses by Category", "Amount (ILS)", "", ""])
        for cat, total in sorted(s["expense_categories"].items(), key=lambda x: -x[1]):
            w.writerow([cat, round(total, 2), "", ""])
        if s["alloc_expense"] or s["alloc_income"] or s["verify_alloc"] or s["input_flags"] or s["unknown_types"]:
            w.writerow([])
            w.writerow(["REVIEW BEFORE FILING", "", "", ""])
            for d, what, amount, vat, thr, one in s["alloc_expense"]:
                note = ("no allocation number; if this row is one tax invoice its input VAT is not deductible" if one else
                        "no invoice or allocation number; needs one if this is a single invoice, else check each invoice")
                w.writerow([f"Expense {d} {what}: {note}", amount, vat, ""])
            for d, what, amount, vat, thr, _ in s["alloc_income"]:
                w.writerow([f"Income {d} {what}: no allocation number on your invoice (needed if the customer is an osek murshe)", amount, vat, ""])
            for d, what, amount, vat, kind, val in s["verify_alloc"]:
                w.writerow([f"{kind.capitalize()} {d} {what}: verify the allocation number ({val!r} is not a 9- or 26-digit number)", amount, vat, ""])
            for cat, vat, kind in s["input_flags"]:
                w.writerow([f"{cat}: input VAT limited or not deductible ({kind})", "", vat, ""])
            if s["unknown_types"]:
                w.writerow([f"{len(s['unknown_types'])} row(s) with an unrecognised Type, in neither total", "", "", ""])

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
            "  %(prog)s --input data.json --month 7 --year 2026\n"
            "  %(prog)s --input data.json --full-year --year 2026 --osek-patur\n"
        ),
    )
    parser.add_argument("--input", required=True, help="Path to JSON or CSV data file")
    span = parser.add_mutually_exclusive_group(required=True)
    span.add_argument("--period", type=int, choices=range(1, 7), help="Bi-monthly VAT period (1-6)")
    span.add_argument("--month", type=int, choices=range(1, 13),
                      help="Single month (1-12), for businesses that file VAT monthly")
    span.add_argument("--full-year", action="store_true",
                      help="The whole calendar year (e.g. for the osek patur annual declaration)")
    parser.add_argument("--year", type=int, required=True, help="Tax year")
    parser.add_argument("--osek-patur", action="store_true",
                        help="Exempt dealer: no VAT column, gross amounts, no VAT liability")
    parser.add_argument("--output", help="Optional CSV output path")

    args = parser.parse_args()

    transactions = load_data(args.input)
    if not transactions:
        print("No transactions found in input file.", file=sys.stderr)
        sys.exit(1)

    if args.full_year:
        months = (1, 12)
    elif args.month is not None:
        months = (args.month, args.month)
    else:
        months = PERIOD_MONTHS[args.period]

    rows = filter_rows(transactions, args.year, months)
    title, due = period_label(args.period, args.month, args.full_year, args.year)
    if not rows:
        print(f"No transactions found for {title}.", file=sys.stderr)
        sys.exit(1)

    try:
        summary = compute_summary(rows, osek_patur=args.osek_patur)
    except AmountParseError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    print_summary(summary, title, due, args.year, args.osek_patur)

    if args.output:
        export_csv(summary, title, args.output, args.osek_patur, args.year)


if __name__ == "__main__":
    main()
