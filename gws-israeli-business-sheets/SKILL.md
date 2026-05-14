---
name: gws-israeli-business-sheets
description: Google Sheets financial tracking and automation for Israeli freelancers and small businesses using the Google Workspace CLI (gws). Use when user asks to create income/expense sheets with Shekel formatting, track VAT (18%) calculations, generate tax-period summaries for accountants, backup spreadsheets as CSV, or auto-log payments. Do NOT use for direct bank API integrations, payroll processing, or filing taxes with the Israel Tax Authority.
license: MIT
---


# GWS Israeli Business Sheets

## Instructions

The Google Workspace CLI (`gws`, package `@googleworkspace/cli`) generates its command surface dynamically from Google's Discovery API. Every Sheets call follows one of two shapes:

- Raw API methods: `gws sheets spreadsheets <method> --params '<JSON>' [--json '<body JSON>']`. The `--params` JSON carries path and query parameters (`spreadsheetId`, `range`, `valueInputOption`, etc.). The `--json` flag carries the request body for POST/PUT/PATCH methods.
- Helper shortcuts: `gws sheets +read` and `gws sheets +append` wrap the most common reads and appends with simple flags.

Useful global flags: `--dry-run` (validate locally, no API call), `--format json|table|yaml|csv` (output format, default `json`). When in doubt about a method's exact parameters, run `gws sheets --help`, `gws sheets spreadsheets --help`, or `gws schema sheets.spreadsheets.values.append`.

### Step 1: Verify GWS CLI Installation and Authentication

Before performing any Google Sheets operations, confirm the Google Workspace CLI is installed and authenticated.

```bash
# Check if gws is installed
gws --version

# If not installed, install globally
npm install -g @googleworkspace/cli

# Authenticate with Google OAuth
gws auth login

# Verify authentication status
gws auth status
```

If the user has not configured OAuth credentials, guide them through `gws auth login` with a Google Cloud project that has the Sheets API enabled. See `gws auth --help` for credential options.

### Step 2: Confirm the User's VAT Status

Before building any sheet, ask whether the user is an **osek murshe** (authorized dealer, charges and reclaims VAT) or an **osek patur** (exempt dealer, does not charge or reclaim VAT). This changes the sheet structure:

- **Osek murshe**: include the full VAT columns (net, VAT, total) and compute VAT liability.
- **Osek patur**: an osek patur does not charge VAT on income and cannot reclaim input VAT on expenses. Drop the VAT column entirely (or leave it at 0), record gross amounts only, and skip the VAT-liability calculation. The osek patur still tracks income and expenses for the annual income-tax return.

An osek patur whose annual turnover crosses the ceiling (NIS 120,000 for 2025, NIS 122,833 for 2026) must convert to osek murshe. If a user is near the ceiling, flag it.

### Step 3: Create a New Financial Tracking Spreadsheet

When the user wants to set up a new income/expense tracking sheet, create it with proper Israeli financial structure.

**Sheet structure for an osek murshe:**

| Column | Header (EN) | Header (HE) | Format | Purpose |
|--------|------------|-------------|--------|---------|
| A | Date | תאריך | DD/MM/YYYY | Transaction date |
| B | Description | תיאור | Text | What the transaction is |
| C | Category | קטגוריה | Text | Tax-deductible category |
| D | Amount (excl. VAT) | סכום (ללא מע"מ) | ILS currency | Net amount |
| E | VAT (18%) | מע"מ (18%) | ILS currency | Calculated VAT |
| F | Total (incl. VAT) | סכום כולל מע"מ | ILS currency | Gross amount |
| G | Type | סוג | Income/Expense | Direction of money |
| H | Invoice # | מספר חשבונית | Text | Invoice reference |
| I | Payment Method | אמצעי תשלום | Text | Bank/PayPal/Cash |
| J | Notes | הערות | Text | Additional details |

For an **osek patur**, drop columns D and E and rename column F to `Amount` / `סכום` (gross only), since no VAT applies.

**Tax-deductible categories for Israeli businesses:**

| Category (EN) | Category (HE) | Deduction Rate |
|---------------|---------------|----------------|
| Office Rent | שכירות משרד | 100% |
| Equipment | ציוד | 100% |
| Phone & Internet | טלפון ואינטרנט | 100% (if business-only) |
| Professional Services | שירותים מקצועיים | 100% |
| Car Expenses | הוצאות רכב | Limited (45% or fixed) |
| Meals & Entertainment | ארוחות ואירוח | 80% |
| Travel | נסיעות | 100% |
| Software & Subscriptions | תוכנה ומנויים | 100% |
| Marketing | שיווק | 100% |
| Insurance | ביטוח | 100% |

To create the spreadsheet and write the header row:

```bash
# Create a new spreadsheet (the response JSON includes "spreadsheetId")
gws sheets spreadsheets create --json '{"properties":{"title":"Business Tracker 2026"}}'

# Write the header row into the first row (use the spreadsheetId from the create response)
gws sheets spreadsheets values update \
  --params '{"spreadsheetId":"SPREADSHEET_ID","range":"Sheet1!A1:J1","valueInputOption":"RAW"}' \
  --json '{"values":[["Date","Description","Category","Amount (excl. VAT)","VAT (18%)","Total (incl. VAT)","Type","Invoice #","Payment Method","Notes"]]}'
```

### Step 4: Append Income and Expense Entries

When the user wants to log a transaction, calculate the VAT automatically (osek murshe only) and append the row.

**For income entries (user received payment):**

```bash
# Calculate: if user received 5,900 ILS total, the breakdown is:
# Amount excl. VAT = Total / 1.18 = 5,000 ILS
# VAT = Amount * 0.18 = 900 ILS
gws sheets spreadsheets values append \
  --params '{"spreadsheetId":"SPREADSHEET_ID","range":"Sheet1!A:J","valueInputOption":"USER_ENTERED"}' \
  --json '{"values":[["15/01/2026","Web Development Project","Professional Services","5000","900","5900","Income","INV-2026-001","Bank Transfer",""]]}'
```

The `+append` helper is a shorter equivalent for a single simple row:

```bash
gws sheets +append --spreadsheet SPREADSHEET_ID \
  --json-values '[["15/01/2026","Web Development Project","Professional Services","5000","900","5900","Income","INV-2026-001","Bank Transfer",""]]'
```

**For expense entries:**

```bash
# Example: Office internet bill of 236 ILS (200 + 36 VAT)
gws sheets spreadsheets values append \
  --params '{"spreadsheetId":"SPREADSHEET_ID","range":"Sheet1!A:J","valueInputOption":"USER_ENTERED"}' \
  --json '{"values":[["20/01/2026","Bezeq Internet","Phone & Internet","200","36","236","Expense","","Direct Debit",""]]}'
```

**VAT calculation formulas (osek murshe only):**

| Scenario | Formula | Example |
|----------|---------|---------|
| Have total (incl. VAT), need breakdown | Amount = Total / 1.18, VAT = Total - Amount | 1180 / 1.18 = 1000, VAT = 180 |
| Have net amount, need total | VAT = Amount * 0.18, Total = Amount + VAT | 1000 * 0.18 = 180, Total = 1180 |
| Meal expense (80% deductible) | Deductible = Amount * 0.80 | 500 * 0.80 = 400 |

### Step 5: Read and Summarize Financial Data

When the user needs a financial overview, read the data and compute summaries.

```bash
# Read all entries from the sheet using the helper (returns the raw values array)
gws sheets +read --spreadsheet SPREADSHEET_ID --range "Sheet1!A:J"

# Equivalent raw API call (response is a ValueRange with a "values" array of arrays)
gws sheets spreadsheets values get --params '{"spreadsheetId":"SPREADSHEET_ID","range":"Sheet1!A:J"}'
```

Both forms return JSON with a `values` field: an array of rows, each row an array of cell strings. The first row is the header. After reading the data, calculate and present:
- Total income for the period
- Total expenses for the period
- Net profit (income minus expenses)
- Total VAT collected (on income) - osek murshe only
- Total VAT paid (on expenses, input VAT) - osek murshe only
- VAT liability (collected minus paid, amount to report to tax authority) - osek murshe only

For an osek patur, present income, expenses, and net profit only.

**Bi-monthly VAT reporting periods (Israel):**

| Period | Months | Report Due By |
|--------|--------|---------------|
| 1 | January-February | March 15 |
| 2 | March-April | May 15 |
| 3 | May-June | July 15 |
| 4 | July-August | September 15 |
| 5 | September-October | November 15 |
| 6 | November-December | January 15 |

### Step 6: Generate Tax-Period Summary Reports

When the user needs to prepare data for their accountant or for VAT reporting, create a summary sheet.

```bash
# Read all data
gws sheets +read --spreadsheet SPREADSHEET_ID --range "Sheet1!A:J"
```

After reading, use Python (via `scripts/vat-summary.py`) to:
1. Filter transactions by the bi-monthly period
2. Group by income vs. expenses
3. Calculate total VAT collected and input VAT (osek murshe only)
4. Generate a summary suitable for the accountant

Then write the summary into a new tab. First add the tab with a `batchUpdate`, then write the rows:

```bash
# Add a new sheet tab named "VAT-Period-1"
gws sheets spreadsheets batchUpdate \
  --params '{"spreadsheetId":"SPREADSHEET_ID"}' \
  --json '{"requests":[{"addSheet":{"properties":{"title":"VAT-Period-1"}}}]}'

# Write summary headers and rows
gws sheets spreadsheets values update \
  --params '{"spreadsheetId":"SPREADSHEET_ID","range":"VAT-Period-1!A1:D1","valueInputOption":"RAW"}' \
  --json '{"values":[["Category","Total Amount","Total VAT","Transaction Count"]]}'

gws sheets spreadsheets values append \
  --params '{"spreadsheetId":"SPREADSHEET_ID","range":"VAT-Period-1!A:D","valueInputOption":"USER_ENTERED"}' \
  --json '{"values":[["Total Income","50000","9000","15"],["Total Expenses","20000","3600","25"],["VAT Liability","","5400",""],["Net Profit","30000","",""]]}'
```

### Step 7: Backup Sheets as CSV

When the user wants local backups or wants to share data with their accountant, export to CSV using the `--format csv` flag.

```bash
# Export the main tracking sheet as CSV
gws sheets spreadsheets values get \
  --params '{"spreadsheetId":"SPREADSHEET_ID","range":"Sheet1!A:J"}' --format csv > business-tracker-2026.csv

# Export a specific VAT period
gws sheets spreadsheets values get \
  --params '{"spreadsheetId":"SPREADSHEET_ID","range":"VAT-Period-1!A:D"}' --format csv > vat-period-1-2026.csv
```

Use the `scripts/backup-sheets.py` script for automated multi-tab backup:

```bash
python scripts/backup-sheets.py --spreadsheet-id SPREADSHEET_ID --output-dir ./backups/2026-01 --tabs "Sheet1,VAT-Period-1"
```

### Step 8: Auto-Log Payments from Structured Input

When the user provides transaction data in bulk (from a bank statement or invoice list), parse and append multiple rows in one call.

```bash
# Append multiple rows in one call
gws sheets spreadsheets values append \
  --params '{"spreadsheetId":"SPREADSHEET_ID","range":"Sheet1!A:J","valueInputOption":"USER_ENTERED"}' \
  --json '{"values":[
    ["01/02/2026","Client A - Monthly Retainer","Professional Services","10000","1800","11800","Income","INV-2026-010","Bank Transfer",""],
    ["03/02/2026","AWS Hosting","Software & Subscriptions","450","81","531","Expense","","Credit Card",""],
    ["05/02/2026","Business Lunch - Client B","Meals & Entertainment","300","54","354","Expense","","Credit Card","80% deductible"]
  ]}'
```

### Step 9: Use Dry-Run Mode for Validation

Before making changes, offer the user a dry-run preview. The `--dry-run` flag validates the request locally without sending it to the API.

```bash
# Preview what would be appended without writing
gws sheets spreadsheets values append \
  --params '{"spreadsheetId":"SPREADSHEET_ID","range":"Sheet1!A:J","valueInputOption":"USER_ENTERED"}' \
  --json '{"values":[["15/03/2026","Test Entry","Office Rent","5000","900","5900","Expense","","Bank Transfer",""]]}' \
  --dry-run
```

### Step 10: Issue a Compliant Tax Invoice

When the user needs to issue a tax invoice (חשבונית מס) to a customer, the sheet is the tracking record, not the legal invoice. The legal invoice itself is produced by an invoicing service (Morning, iCount, Rivhit and similar) or an approved template. A compliant Israeli tax invoice must include:

- The header "חשבונית מס" and a running invoice number
- The seller's business name and VAT/business ID (osek murshe number, or business ID for an osek patur issuing a "חשבונית עסקה" / receipt)
- The customer's name (and ID for invoices above the threshold)
- Invoice date
- Description, quantity, and unit price of goods or services
- Amount before VAT, the VAT amount, and the total including VAT (osek murshe). An osek patur issues a receipt or "חשבונית עסקה" with no VAT line.

**Allocation number (מספר הקצאה) e-invoice mandate.** Israel's continuous-transaction-control model requires an allocation number from the Tax Authority's platform for tax invoices at or above a threshold, before the buyer can deduct input VAT. As of 2026 the threshold steps down: invoices of NIS 10,000 or more (before VAT) from January 1, 2026, and NIS 5,000 or more (before VAT) from June 1, 2026. When logging a large invoice, remind the user to obtain the allocation number through their invoicing software and record it alongside the invoice number.

## Examples

### Example 1: Israeli Freelancer Sets Up Monthly Tracking

User says: "Create a Google Sheet to track my freelance income and expenses with VAT"

Actions:
1. Ask whether the user is an osek murshe or an osek patur (this decides whether VAT columns are included)
2. Run `gws sheets spreadsheets create --json '{"properties":{"title":"Freelance Tracker 2026"}}'` and read the `spreadsheetId` from the response
3. Write the header row with `gws sheets spreadsheets values update` (10 columns for an osek murshe, fewer for an osek patur)
4. Show the user the spreadsheet ID and link, and explain the column structure

Result: A new Google Sheet with the correct Israeli structure for the user's VAT status, ready for entries.

### Example 2: Generate Bi-Monthly VAT Summary for Accountant

User says: "Create a VAT summary for January-February 2026 and export it as CSV"

Actions:
1. Run `gws sheets +read --spreadsheet SPREADSHEET_ID --range "Sheet1!A:J"` to pull all entries
2. Run `python scripts/vat-summary.py` to filter Jan-Feb transactions and compute totals
3. Add a "VAT-Period-1-2026" tab with `gws sheets spreadsheets batchUpdate` and write the summary with `gws sheets spreadsheets values update`
4. Export the summary tab with `gws sheets spreadsheets values get --format csv`
5. Display the summary: total income, total expenses, VAT collected, input VAT, net VAT liability

Result: A clean VAT period summary both in the Google Sheet and as a local CSV file ready to send to the accountant.

### Example 3: Auto-Log Bank Transfers into Expense Sheet

User says: "I got these payments this month: Client A paid 11,800 for consulting, I paid 531 for hosting, and 354 for a business lunch"

Actions:
1. Parse each transaction, calculate the VAT breakdown (divide totals by 1.18)
2. Categorize: consulting = Professional Services (income), hosting = Software & Subscriptions (expense), lunch = Meals & Entertainment (expense, 80% deductible)
3. Use `gws sheets spreadsheets values append` with a multi-row `values` array in `--json`
4. Confirm all entries were logged with correct VAT calculations

Result: Three new rows appended to the tracking sheet with proper categorization, VAT breakdown, and deductibility notes.

## Bundled Resources

### Scripts
- `scripts/vat-summary.py` -- Generate bi-monthly VAT summary reports from sheet data. Run: `python scripts/vat-summary.py --help`
- `scripts/backup-sheets.py` -- Backup Google Sheets tabs as local CSV files. Run: `python scripts/backup-sheets.py --help`

### References
- `references/israeli-tax-categories.md` -- Complete list of Israeli tax-deductible expense categories with deduction rates, plus VAT and osek patur/murshe rules. Consult when categorizing a business expense or confirming a tax fact.
- `references/gws-sheets-recipes.md` -- Common gws CLI recipes for Google Sheets operations. Consult when performing sheet operations beyond basic read/append.

## Gotchas

- Israeli VAT reporting periods are bi-monthly (every 2 months), not quarterly as in many other countries. Agents may structure summaries on a quarterly basis, which does not match Israeli tax authority requirements.
- Israeli date format is DD/MM/YYYY, not MM/DD/YYYY. Agents may use the American format, which causes confusion and errors when dates like 03/04/2026 could mean either March 4 or April 3.
- An osek patur does not charge VAT on income and cannot reclaim input VAT on expenses. Agents may add VAT columns and compute a VAT liability for an osek patur, which is wrong. Always confirm the user's VAT status first.
- Meal and entertainment expenses are only 80% deductible in Israel. Agents may categorize these as 100% deductible, overstating tax deductions.
- Car expenses have complex deduction rules in Israel (45% or a fixed monthly amount, whichever is lower). Agents may apply 100% deduction, which would be incorrect for most businesses.
- Israeli VAT is 18% (since January 2025). Agents trained on older data may use 17%, which was the previous rate, leading to incorrect calculations throughout the spreadsheet.
- The `gws` command surface is generated from Google's Discovery API. There is no `gws sheets create` or `gws sheets read` top-level command. Use `gws sheets spreadsheets <method>` with `--params`/`--json`, or the `+read` / `+append` helpers. When unsure, run `gws sheets --help`.


## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Google Workspace CLI | https://github.com/googleworkspace/cli | Real gws command surface, helper commands, auth setup |
| Google Sheets API | https://developers.google.com/sheets/api | Sheets REST API, spreadsheets.values methods, batchUpdate |
| Google Apps Script | https://developers.google.com/apps-script | SpreadsheetApp API, custom functions, triggers |
| Israel Tax Authority | https://www.gov.il/he/departments/israel_tax_authority | Current VAT rate (18%), osek patur ceiling, allocation-number thresholds, reporting schedules |
| Bank of Israel - exchange rates | https://www.boi.org.il/roles/markets/exchangerates/ | Daily representative exchange rates, historical data for reports |

## Troubleshooting

### Error: "gws: command not found"
Cause: The Google Workspace CLI is not installed or not in PATH.
Solution: Install with `npm install -g @googleworkspace/cli`. If using npx, prefix commands with `npx @googleworkspace/cli`.

### Error: "Authentication required" or "Token expired"
Cause: The user has not authenticated or the OAuth token has expired.
Solution: Run `gws auth login` to re-authenticate. See `gws auth --help` for credential file and token options.

### Error: "Unknown service" or unexpected argument
Cause: Using a fabricated command shape such as `gws sheets create` or `gws sheets read`.
Solution: Use the real surface: `gws sheets spreadsheets <method> --params '<JSON>'` (with `--json '<body>'` for writes), or the `+read` / `+append` helpers. Run `gws sheets --help` and `gws sheets spreadsheets --help` to list real methods.

### Error: "Spreadsheet not found" or "404"
Cause: The spreadsheet ID is incorrect or the user does not have access.
Solution: Verify the spreadsheet ID from the Google Sheets URL (the string between /d/ and /edit). Ensure the authenticated Google account has edit access to the sheet.

### Error: "VAT calculation mismatch"
Cause: Rounding differences between manual calculation and sheet formulas.
Solution: Always round VAT to 2 decimal places. Use the formula `Math.round(amount * 18) / 100` for precise Shekel calculations. Israeli tax authority accepts rounding to the nearest agora.
