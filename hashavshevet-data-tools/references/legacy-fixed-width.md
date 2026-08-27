# Legacy fixed-width parsing and import (fallback only)

**Read the warning first.** The column maps here are best-guess heuristics for legacy Windows
installations. They are NOT an authoritative Hashavshevet specification, they vary by version,
and a mis-aligned import can corrupt a live company's books, which is a ניהול פנקסים exposure.

Use this file ONLY when no OPENFORMAT/BKMV export is available. For any ITA filing, CPA handoff,
PCN874 or Form 6111 work, use the OPENFORMAT export instead (see SKILL.md). For writing data INTO
Hashavshevet, prefer Hashavshevet's own documented import template or the BKMV import path, and
always test against a COPY of the company file, never the live one.

### Step 3: Parse fixed-width Hashavshevet data files

Hashavshevet `.dat` files use fixed-width column layouts. The column widths vary by file type:

```python
# HESHIN.dat (Chart of Accounts) column layout
HESHIN_COLUMNS = {
    'account_number': (0, 15),     # מספר חשבון
    'account_name': (15, 65),      # שם חשבון
    'account_type': (65, 67),      # סוג חשבון (1=asset, 2=liability, 3=equity, 4=income, 5=expense)
    'parent_account': (67, 82),    # חשבון אב
    'sort_code': (82, 92),         # קוד מיון
    'is_active': (92, 93),         # פעיל (1=yes, 0=no)
    'opening_balance': (93, 113),  # יתרת פתיחה
    'currency': (113, 116),        # מטבע
}

# PKUDOT.dat (Journal Entries) column layout
PKUDOT_COLUMNS = {
    'entry_number': (0, 10),       # מספר פקודה
    'batch_number': (10, 18),      # מספר מנה
    'entry_date': (18, 28),        # תאריך (DD/MM/YYYY)
    'account_debit': (28, 43),     # חשבון חובה
    'account_credit': (43, 58),    # חשבון זכות
    'amount': (58, 73),            # סכום
    'currency': (73, 76),          # מטבע
    'reference': (76, 96),         # אסמכתא
    'description': (96, 146),      # תיאור
    'value_date': (146, 156),      # תאריך ערך
}
```

Parse these files using the column positions:

```python
def parse_fixed_width(content: str, columns: dict) -> list[dict]:
    """Parse a fixed-width Hashavshevet data file."""
    records = []
    for line in content.strip().split('\n'):
        if not line.strip():
            continue
        expected_len = max(end for _, end in columns.values())
        if len(line) < expected_len:
            # A short line means the layout does not match this file. Fail loudly:
            # silently truncating the last field is how mis-parsed data reaches the books.
            raise ValueError(
                f"Record length {len(line)} < expected {expected_len}. "
                "The column layout does not match this file (wrong Hashavshevet version?). "
                "Use an OPENFORMAT/BKMV export instead of guessing offsets."
            )
        record = {}
        for field_name, (start, end) in columns.items():
            record[field_name] = line[start:end].strip()
        records.append(record)
    return records
```

### Step 5: Import data into Hashavshevet format

When importing data into Hashavshevet, generate fixed-width files matching the expected layout. **Caution:** the column maps here are the same best-guess heuristics flagged in the Instructions block, not an authoritative spec, and importing mis-aligned fixed-width data into a live company can corrupt the books. Prefer Hashavshevet's own documented import interface/template, and always test a generated file against a COPY of the company file first, never the live one.

```python
def generate_hashavshevet_import(records: list[dict], columns: dict, output_path: str):
    """Generate a fixed-width file for Hashavshevet import."""
    lines = []
    for record in records:
        line = ''
        sorted_cols = sorted(columns.items(), key=lambda x: x[1][0])
        for field_name, (start, width_end) in sorted_cols:
            width = width_end - start
            value = str(record.get(field_name, ''))
            # Pad or truncate to exact width
            if len(value) > width:
                value = value[:width]
            else:
                value = value.ljust(width)
            line += value
        lines.append(line)

    # CRLF, not LF: legacy Windows fixed-width importers expect CRLF and a constant
    # record length. An LF-joined file loads as one giant record or shifts every offset.
    record_len = max(end for _, end in columns.values())
    for i, line in enumerate(lines):
        if len(line) != record_len:
            raise ValueError(f"Row {i+1}: record length {len(line)} != {record_len}")

    # errors='strict', NOT 'replace': a Hebrew character outside CP1255 silently becoming
    # '?' inside a customer name is silent data corruption that then fails to match the
    # master file. Fail here instead, and fix the source data.
    with open(output_path, 'w', encoding='windows-1255', errors='strict', newline='') as f:
        f.write('\r\n'.join(lines) + '\r\n')
```

Import validation rules:
- Account numbers must exist in the chart of accounts
- Dates must be in DD/MM/YYYY format (Israeli date format)
- Amounts must use period as decimal separator (not comma)
- Debit and credit accounts cannot be the same
- Batch numbers must be sequential within a fiscal year
- Currency codes must match Hashavshevet's internal currency table. These internal numeric codes vary by installation, so confirm them against your installation's currency table rather than assuming a fixed mapping or reusing ISO 4217 codes.

