---
name: hashavshevet-data-tools
description: Import and export data between Hashavshevet accounting software and modern formats (JSON, CSV, Excel). Use when you need to extract journal entries, chart of accounts, trial balances, or customer/supplier lists from Hashavshevet, import bank transactions and invoices into Hashavshevet format, migrate data from Hashavshevet to cloud-based solutions (iCount, Rivhit, Invoice4U), or handle Hebrew encoding conversions (Windows-1255 to UTF-8). Supports Hashavshevet Gold, Hashavshevet 2000+, and newer versions. Validates data integrity during import/export operations. Do NOT use for real-time Hashavshevet API integrations, direct database modifications, or live bookkeeping within Hashavshevet.
license: MIT
allowed-tools: Bash(python:*) Read Edit Write
compatibility: Requires Python 3.9+ with openpyxl and chardet libraries
---


# Hashavshevet Data Tools

## Instructions

> **Important: use the official OPENFORMAT/BKMV export, not direct binary parsing.**
>
> Hashavshevet does NOT publish public per-byte offsets for its internal `.dat` / `.hsh` / `.mdb` files. The publicly documented and ITA-mandated export from any Israeli bookkeeping software is **OPENFORMAT (קובץ אחיד / BKMV)**. The export produces a ZIP of three files: `INI.TXT` (production summary, holds the leading `A000` record plus per-record-type control-count summary records), `BKMVDATA.TXT` (the business data, with one `A100` opening record, then `C100`, `D110`, `D120`, `B100`, `B110`, `M100` records, then one `Z900` closing record), and `README.TXT` (general production details for the user). Only `INI.TXT` and `BKMVDATA.TXT` are sent to the ITA or the CPA. Spec: <https://www.misim.gov.il/TmbakmmsmlNew/Files/horaot_131.pdf>. Hashavshevet's BKMV export guide: <https://downloads.h-erp.co.il/files/general/bkmv7-erp.pdf>. Validate output against the ITA simulator: <https://www.misim.gov.il/TmbakmmsmlNew/frmCheckFiles.aspx>.
>
> The fixed-width column maps below (HESHIN_COLUMNS / PKUDOT_COLUMNS) are **best-guess heuristics for legacy Windows installations**, not authoritative specifications. Use them only as a fallback when no OPENFORMAT export is available; never claim them as the canonical Hashavshevet format. For any ITA filing, CPA handoff, or PCN874 / Form 6111 generation, export via OPENFORMAT instead.

> **Hashavshevet בענן (H-WEB / Wizcloud) public REST API.** The cloud version of Hashavshevet exposes a public REST API for documents, accounts, and transactions: <https://home.wizcloud.co.il/help/apidocument/>. Use this for ongoing two-way sync with Green Invoice / Rivhit / iCount instead of one-shot file dumps where possible.

> **SHAAM allocation-number context (2026).** Sales-invoice journal entries created/imported through Hashavshevet for B2B amounts at or above the current threshold must carry an allocation number (mispar haktza'a). Threshold (VAT excluded): NIS 10,000 since January 2026. NIS 5,000 since 1 June 2026. An above-threshold tax invoice WITHOUT a valid allocation number cannot be used by the counterparty to deduct input VAT, so treat a missing allocation number as a hard validation error, not a soft "incomplete" warning. Hashavshevet בענן has built-in real-time SHAAM integration; the Windows version may need a separate workflow.

### Step 1: Identify the Hashavshevet version and file format

Determine which version of Hashavshevet the user is working with and identify the relevant file formats:

- **Legacy Hashavshevet (Windows, on-prem)**: Stores data in a proprietary ISAM or SQL backend. Direct binary parsing is unsupported and brittle; use the built-in OPENFORMAT export instead.
- **Hashavshevet H-ERP (current Windows ERP)**: Standard product line as of 2026. Exports OPENFORMAT/BKMV for ITA + CPA workflows; legacy `.dat` / `.hsh` files may still appear in archives.
- **Hashavshevet בענן (H-WEB / Wizcloud, SaaS)**: Cloud-native, exports OPENFORMAT directly, plus a public REST API for live integration.
- "Gold" / "2000+" naming is from 1990s/2000s legacy product lines; H-ERP / H-WEB are the current names.

Common Hashavshevet data files:

| File / Table | Hebrew Name | Description | Typical Format |
|---|---|---|---|
| `HESHIN.dat` | מאזן חשבונות | Chart of accounts | Fixed-width, Windows-1255 |
| `PKUDOT.dat` | פקודות יומן | Journal entries | Fixed-width, Windows-1255 |
| `MANOT.dat` | מנות | Batches | Fixed-width, Windows-1255 |
| `KARTIS.dat` | כרטיסי חשבון | Account cards / ledger | Fixed-width, Windows-1255 |
| `HESHBON.dat` | חשבונות | Account master list | Fixed-width, Windows-1255 |
| `MATZAV.dat` | מצב חשבון | Account balances | Fixed-width, Windows-1255 |
| `TNUOT.dat` | תנועות | Transactions | Fixed-width, Windows-1255 |

### Step 2: Handle Hebrew encoding

Hashavshevet files typically use Windows-1255 (Hebrew) encoding. Convert to UTF-8 before processing:

```python
import chardet

def detect_and_convert(file_path: str) -> str:
    """Detect encoding and convert Hashavshevet file to UTF-8."""
    with open(file_path, 'rb') as f:
        raw_data = f.read()

    detected = chardet.detect(raw_data)
    encoding = detected['encoding']

    # Hashavshevet almost always uses Windows-1255
    if encoding and encoding.lower() in ('windows-1255', 'iso-8859-8', 'hebrew'):
        encoding = 'windows-1255'
    elif encoding is None:
        encoding = 'windows-1255'  # Safe fallback for Hebrew accounting data

    return raw_data.decode(encoding, errors='replace')
```

Common encoding pitfalls:
- Hashavshevet Gold always uses Windows-1255
- Some exports may use ISO-8859-8 (visual Hebrew) instead of logical Hebrew
- Mixed encoding files occur when data was copy-pasted from other sources
- BOM (Byte Order Mark) may be present in newer CSV exports

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
        record = {}
        for field_name, (start, end) in columns.items():
            value = line[start:end].strip() if len(line) > start else ''
            record[field_name] = value
        records.append(record)
    return records
```

### Step 4: Export data to modern formats

Convert parsed Hashavshevet data to JSON, CSV, or Excel:

```python
import csv
import json

def export_to_csv(records: list[dict], output_path: str):
    """Export parsed records to UTF-8 CSV with BOM for Excel compatibility."""
    if not records:
        return
    with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

def export_to_json(records: list[dict], output_path: str):
    """Export parsed records to JSON with Hebrew support."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

def export_to_excel(records: list[dict], output_path: str, sheet_name: str = 'Data'):
    """Export parsed records to Excel with proper RTL formatting."""
    from openpyxl import Workbook
    from openpyxl.worksheet.properties import WorksheetProperties

    wb = Workbook()
    ws = wb.active
    ws.title = sheet_name
    ws.sheet_properties = WorksheetProperties(rightToLeft=True)

    # Write headers
    headers = list(records[0].keys())
    for col, header in enumerate(headers, 1):
        ws.cell(row=1, column=col, value=header)

    # Write data
    for row_idx, record in enumerate(records, 2):
        for col_idx, header in enumerate(headers, 1):
            ws.cell(row=row_idx, column=col_idx, value=record.get(header, ''))

    wb.save(output_path)
```

### Step 5: Import data into Hashavshevet format

When importing data into Hashavshevet, generate fixed-width files matching the expected layout:

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

    with open(output_path, 'w', encoding='windows-1255', errors='replace') as f:
        f.write('\n'.join(lines))
```

Import validation rules:
- Account numbers must exist in the chart of accounts
- Dates must be in DD/MM/YYYY format (Israeli date format)
- Amounts must use period as decimal separator (not comma)
- Debit and credit accounts cannot be the same
- Batch numbers must be sequential within a fiscal year
- Currency codes must match Hashavshevet's internal currency table. These internal numeric codes vary by installation, so confirm them against your installation's currency table rather than assuming a fixed mapping or reusing ISO 4217 codes.

### Step 6: Data migration to cloud solutions

When migrating from Hashavshevet to cloud-based accounting solutions:

**Before you start (read this first):**
- Migrating or exporting off Hashavshevet does NOT discharge the ניהול פנקסים retention duty. The accounting system and records must be retained 7 years from the end of the relevant tax year (or 6 years from the date the return was filed, whichever is later). Do NOT decommission or wipe the source Hashavshevet system after the cutover; keep it (or a complete archived copy) accessible for that full period.
- Where the target system supports it, import the native BKMV uniform file directly (יבוא נתונים מקובץ במבנה אחיד). Rivhit and other cloud systems accept the uniform file as-is. This is preferred over hand-mapped CSV/Excel because it preserves document-number continuity and the ITA-defined field structure.
- Preserve document-numbering continuity (מספר עוקב) across the cutover so each document type keeps an unbroken running number.
- Reconcile the new system's opening trial balance to the old system's closing trial balance before going live; investigate any difference rather than rounding it away.

**iCount migration:**
- Export chart of accounts, then map account numbers to iCount categories
- Export open invoices and customer/supplier balances
- iCount accepts CSV imports with specific column headers

**Rivhit migration:**
- Export full journal for the current fiscal year
- Map Hashavshevet account types to Rivhit's account classification
- Rivhit accepts Excel imports with predefined templates

**Invoice4U migration:**
- Focus on customer/supplier master data and open balances
- Export invoice history for reference (Invoice4U does not import historical journals)
- Use Invoice4U's API for programmatic data import

**Green Invoice migration:**
- Map customer/supplier master data and open balances, then import via Green Invoice's CSV templates or its API
- For an ongoing two-way sync (rather than a one-shot dump), prefer the cloud REST APIs on both sides and see the companion `green-invoice` skill

### Step 6.5: ITA filings (PCN874 and Form 6111)

Two ITA filings are commonly produced from Hashavshevet data. Both are software-independent specs, so generate them from an OPENFORMAT export rather than from heuristic binary parsing:

- **PCN874 (דוח מפורט מע"מ, detailed VAT report)**: a fixed-structure text file, NOT a flat invoice list. It starts with a header/opening record (the business osek number, the reporting period, and totals/counts), followed by detail records that are keyed by transaction-type code, sales/output transactions (עסקאות) versus input transactions (תשומות, plus special types such as import entries). For an input transaction the supplier's osek number is mandatory or the input VAT cannot be deducted. Detailed VAT reporting is obligatory only above the turnover threshold (for an individual osek, annual turnover above NIS 500,000 from 1 January 2026). A bookkeeper exports it monthly or bi-monthly and uploads it to the ITA, which cross-references input VAT against output VAT. Hashavshevet has a built-in PCN874 export. Spec lives on the ITA site (see Reference Links).
- **Form 6111 (טופס 6111, דוח התאמה למס, tax-adjustment report)**: an annex to the annual tax return carrying profit-and-loss, balance-sheet, and tax-adjustment data, filed online. A bookkeeper or CPA exports the trial balance from Hashavshevet, maps each account to the 6111 line codes, and submits the annex. Confirm the current line codes against the ITA's year-specific 6111 spec (see Reference Links).

### Step 7: Validate data integrity

After any import or export operation, validate data integrity:

```python
def validate_trial_balance(records: list[dict]) -> dict:
    """Validate that debits equal credits in journal entries."""
    total_debit = 0
    total_credit = 0
    errors = []

    for i, record in enumerate(records):
        try:
            amount = float(record.get('amount', 0))
            if record.get('account_debit'):
                total_debit += amount
            if record.get('account_credit'):
                total_credit += amount
        except ValueError:
            errors.append(f"Row {i+1}: Invalid amount '{record.get('amount')}'")

    balanced = abs(total_debit - total_credit) < 0.01
    return {
        'balanced': balanced,
        'total_debit': round(total_debit, 2),
        'total_credit': round(total_credit, 2),
        'difference': round(total_debit - total_credit, 2),
        'errors': errors,
    }

def validate_account_references(entries: list[dict], accounts: list[dict]) -> list[str]:
    """Verify all referenced accounts exist in the chart of accounts."""
    valid_accounts = {a['account_number'] for a in accounts}
    errors = []
    for i, entry in enumerate(entries):
        debit_acc = entry.get('account_debit', '').strip()
        credit_acc = entry.get('account_credit', '').strip()
        if debit_acc and debit_acc not in valid_accounts:
            errors.append(f"Row {i+1}: Debit account '{debit_acc}' not found in chart of accounts")
        if credit_acc and credit_acc not in valid_accounts:
            errors.append(f"Row {i+1}: Credit account '{credit_acc}' not found in chart of accounts")
    return errors
```

## Examples

### Example 1: Export journal entries from Hashavshevet to Excel

User says: "I have a PKUDOT.dat file from Hashavshevet Gold. I need to export all journal entries from 2025 to an Excel file for my auditor."

Actions:
1. Read the `PKUDOT.dat` file and detect encoding (Windows-1255)
2. Convert content from Windows-1255 to UTF-8
3. Parse the fixed-width data using the PKUDOT column layout
4. Filter records where `entry_date` falls within 01/01/2025 to 31/12/2025
5. Export filtered records to Excel with RTL formatting and Hebrew column headers
6. Validate that total debits equal total credits in the exported data

Result: An Excel file `pkudot_2025.xlsx` with all 2025 journal entries, properly formatted with Hebrew headers, RTL sheet direction, and a validation summary confirming the trial balance is balanced.

### Example 2: Import bank transactions into Hashavshevet format

User says: "I downloaded bank transactions from Leumi as a CSV. I need to convert them into a format I can import into Hashavshevet 2000+."

Actions:
1. Read the Bank Leumi CSV file (UTF-8 with BOM)
2. Map bank CSV columns to Hashavshevet PKUDOT fields: date to `entry_date`, description to `description`, amount to `amount`, reference number to `reference`
3. Assign debit/credit accounts based on transaction direction (positive = debit bank account / credit income, negative = credit bank account / debit expense)
4. Generate sequential entry numbers and assign to the current batch
5. Format dates from YYYY-MM-DD (bank format) to DD/MM/YYYY (Hashavshevet format)
6. Write the output as a fixed-width `.dat` file in Windows-1255 encoding
7. Validate all generated entries for data integrity

Result: A `bank_import.dat` file ready for import into Hashavshevet 2000+, with 47 transactions properly formatted, encoded in Windows-1255, and validated.

### Example 3: Migrate chart of accounts from Hashavshevet to Rivhit

User says: "We're moving from Hashavshevet Gold to Rivhit. I need to export our chart of accounts and opening balances in a format Rivhit can import."

Actions:
1. Read and parse `HESHIN.dat` (chart of accounts) and `MATZAV.dat` (account balances) from Hashavshevet
2. Convert encoding from Windows-1255 to UTF-8
3. Map Hashavshevet account types (1-5) to Rivhit account classifications
4. Merge account balances with account master data
5. Generate a Rivhit-compatible Excel template with columns: account number, account name, account type, opening balance, currency
6. Apply Rivhit's naming conventions and validation rules
7. Create a mapping reference document showing old Hashavshevet account numbers alongside new Rivhit account IDs

Result: A Rivhit-compatible Excel import file with 234 accounts, a mapping reference document, and a summary of 12 accounts that need manual review due to type classification differences.

### Example 4: Produce an OPENFORMAT (BKMV) export for an ITA filing or CPA handoff

User says: "My CPA asked for a BKMV / kovetz ahid (uniform structure) export from Hashavshevet for the 2025 tax year. How do I produce it and confirm it is valid before I send it?"

Actions:
1. Run Hashavshevet's built-in BKMV export (H-ERP: the uniform-structure export wizard; H-WEB / Wizcloud: the BKMV export screen) for the 2025 date range. This produces a ZIP of three files: `INI.TXT` (production summary, with the `A000` leading record and the per-record-type control-count summary records), `BKMVDATA.TXT` (the business data), and `README.TXT` (general production details). Only `INI.TXT` and `BKMVDATA.TXT` are sent onward.
2. Read `BKMVDATA.TXT` as Windows-1255 and convert to UTF-8 before any inspection.
3. Walk the record types in `BKMVDATA.TXT`: `A100` opening record, `C100` document headers, `D110` document line details, `D120` receipt/deposit details, `B100` accounting journal transactions, `B110` accounting accounts, `M100` inventory items, and `Z900` closing record (record-type code in the first field of each line). Note: `A000` is NOT in this file, it lives in `INI.TXT`.
4. Sanity-check the structure: every `C100` should have matching `D110` lines, the per-record-type counts in the `A000` summary records inside `INI.TXT` should equal the `Z900` total in `BKMVDATA.TXT` and the actual counts you observe, and `B100` debit and credit movements should balance.
5. Validate the ZIP against the ITA file-check simulator (see Reference Links) and save the simulator's feedback report.
6. Hand the validated `INI.TXT` plus `BKMVDATA.TXT` (with the simulator report) to the CPA, or attach them to the relevant ITA submission.

Result: A validated BKMV export for the 2025 tax year (`INI.TXT` + `BKMVDATA.TXT`, drawn from the three-file ZIP) that passes the ITA simulator, ready for the CPA or ITA. This is the canonical path for ITA filings and CPA handoffs, unlike the heuristic fixed-width parsing in Step 3, which is a last-resort fallback only.

## Gotchas

- Hashavshevet files use Windows-1255 encoding, not UTF-8. Agents will almost always attempt to read these files as UTF-8, causing UnicodeDecodeError on the first Hebrew character encountered.
- Hashavshevet date format is DD/MM/YYYY (Israeli standard). Bank exports may use YYYY-MM-DD (ISO) or MM/DD/YYYY (US). Agents may not detect the format mismatch, causing dates like 03/04/2025 to be interpreted incorrectly.
- Fixed-width column positions vary between Hashavshevet versions (Gold vs. 2000+ vs. newer). Agents may apply column layouts from one version to data from another, producing garbled output.
- Hashavshevet uses internal numeric currency codes that differ from ISO 4217. The exact mapping varies by installation, so confirm it against your installation's currency table rather than assuming fixed values. Agents that blindly use ISO 4217 codes will produce values Hashavshevet rejects on import.
- When exporting to CSV for Excel, files must use UTF-8 with BOM (utf-8-sig) encoding. Without the BOM, Excel will not display Hebrew characters correctly, showing gibberish instead.
- In OPENFORMAT, for a foreign-currency movement the record should carry both the NIS amount and the original-currency amount (the spec provides currency fields for this), so do not drop the original-currency value when converting. Very large `BKMVDATA.TXT` files may be rejected by the simulator or downstream importer and need splitting into smaller date ranges.


## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Hashavshevet H-ERP official | https://www.h-erp.co.il | Hashavshevet product versions, file format guides |
| Israel Tax Authority | https://www.gov.il/en/departments/israel_tax_authority | Digital bookkeeping directive, required journal fields |
| ITA OPENFORMAT / מבנה אחיד spec | https://www.misim.gov.il/TmbakmmsmlNew/Files/horaot_131.pdf | BKMV record types (A000 in INI.TXT; A100, C100, D110, D120, B100, B110, M100, Z900 in BKMVDATA.TXT), field offsets |
| Hashavshevet H-ERP BKMV guide | https://downloads.h-erp.co.il/files/general/bkmv7-erp.pdf | How to run the uniform-structure export, INI.TXT + BKMVDATA.TXT |
| ITA file-check simulator | https://www.misim.gov.il/TmbakmmsmlNew/frmCheckFiles.aspx | Validate a BKMV ZIP before CPA / ITA handoff |
| Form 6111 (tax-adjustment report) | https://www.gov.il/he/service/itc6111 | Annual-return annex line codes (P&L, balance sheet, tax adjustment) |
| openpyxl documentation | https://openpyxl.readthedocs.io/en/stable/ | Writing XLSX files from Python, styled export |
| pandas I/O reference | https://pandas.pydata.org/docs/reference/io.html | CSV/Excel import and export, encoding handling |
| CP1255 encoding table (unicode.org) | https://unicode.org/Public/MAPPINGS/VENDORS/MICSFT/WINDOWS/CP1255.TXT | Windows-1255 to UTF-8 Hebrew character mapping |

## Troubleshooting

### Error: "UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9"
Cause: The file is encoded in Windows-1255 (Hebrew) but is being read as UTF-8. This is the most common error when working with Hashavshevet files, as the software uses Windows-1255 by default.
Solution: Explicitly specify `encoding='windows-1255'` when reading the file. If unsure about the encoding, use the `chardet` library to auto-detect it. For files with mixed encoding, use `errors='replace'` to substitute undecodable characters.

### Error: "Trial balance is not balanced (difference: X.XX)"
Cause: Rounding differences from currency conversions, partial exports (missing entries from a batch), or corrupted data in the source file. Hashavshevet sometimes stores amounts with extra decimal places internally.
Solution: First check if the difference is a small rounding error (less than one shekel). If so, create an adjustment entry. For larger differences, verify the export includes all batches for the period. Re-export from Hashavshevet using the "full export" option rather than filtered export.

### Error: "Account number not found in chart of accounts"
Cause: Journal entries reference accounts that were deleted or renumbered in Hashavshevet, or the chart of accounts export is from a different fiscal year than the journal entries.
Solution: Export both the chart of accounts and journal entries from the same Hashavshevet database and fiscal year. If accounts were renumbered, create a mapping table and update references before import. Check for leading zeros being stripped during conversion.

### Error: "Date format mismatch during import"
Cause: Hashavshevet expects DD/MM/YYYY (Israeli format) but the source data uses MM/DD/YYYY (American format) or YYYY-MM-DD (ISO format). This commonly occurs when importing bank data or data from international systems.
Solution: Normalize all dates to DD/MM/YYYY before generating the import file. Check for ambiguous dates where day and month could be swapped (e.g., 03/04/2025 could be March 4 or April 3) and verify against the source system's format.
