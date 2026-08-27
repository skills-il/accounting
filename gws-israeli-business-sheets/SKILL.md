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

# If not installed: the recommended install is the pre-built binary for the
# user's OS from https://github.com/googleworkspace/cli/releases, placed on $PATH.
# npm is a convenience wrapper that downloads that same binary (needs Node 18+):
npm install -g @googleworkspace/cli

# Authenticate with Google OAuth
gws auth login

# Verify authentication status
gws auth status
```

If the user has not configured OAuth credentials, guide them through `gws auth login` with a Google Cloud project that has the Sheets API enabled. See `gws auth --help` for credential options.

Two things to tell the user up front, because they affect whether this workflow keeps working:
- `gws` is **not an officially supported Google product**, and it is under active development before v1.0, so breaking changes are expected. If a command in this skill fails, check `gws --help` and the current release notes before assuming the user did something wrong.
- `gws` builds its command surface dynamically from Google's Discovery Service rather than shipping a fixed command list, so subcommands mirror the Sheets API resources and methods and can change when the API does. Run `gws sheets --help` to see what the installed version actually exposes rather than trusting a remembered command.

### Step 2: Confirm the User's VAT Status

Before building any sheet, ask whether the user is an **osek murshe** (authorized dealer, charges and reclaims VAT) or an **osek patur** (exempt dealer, does not charge or reclaim VAT). This changes the sheet structure:

- **Osek murshe**: include the full VAT columns (net, VAT, total) and compute VAT liability.
- **Osek patur**: an osek patur does not charge VAT on income and cannot reclaim input VAT on expenses. Drop the VAT column entirely (or leave it at 0), record gross amounts only, and skip the VAT-liability calculation. The osek patur still tracks income and expenses for the annual income-tax return.

An osek patur whose annual turnover crosses the ceiling (NIS 120,000 for 2025, NIS 122,833 for 2026) must convert to osek murshe. If a user is near the ceiling, flag it.

**Osek zair (micro-dealer) 2026 reform.** A separate income-tax track for low-turnover self-employed (turnover ceiling CPI-linked, about NIS 122,833 for 2026) grants an automatic 30% expense deduction off turnover with no need to itemize receipts, plus a simplified annual report and no advance payments. If the user is a low-turnover freelancer, mention that this track may suit them and tell them to confirm eligibility with their accountant or the Tax Authority before opting in.

**Before anything else, set expectations about what this sheet is.** It is a management and reporting tool, not a legal book of account. Israeli bookkeeping rules require a computerised book to be a fixed file with non-deletable, automatically numbered records and additive corrections, and a freely editable Google Sheet meets none of that. The user still needs a compliant invoicing and bookkeeping system alongside this, and their allocation numbers come from that system. Say this once, early, rather than letting them discover it at an audit.

Input-VAT deductibility also follows its own rules, separate from the income-tax percentages in this skill: VAT on a private vehicle is not reclaimable at all, VAT on hospitality and refreshments is generally not reclaimable, and mixed business/private inputs are limited to 2/3 or 1/4. See `references/israeli-tax-categories.md`. The VAT column records what was charged; that is not automatically what can be reclaimed.

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
| K | Allocation # | מספר הקצאה | Text | Israel Invoice allocation number for invoices at/above the threshold |
| L | Withholding | ניכוי במקור | ILS currency | Tax withheld at source by the payer, if any |

Column K records the **allocation number (מספר הקצאה)** the seller obtains from the Tax Authority's Israel Invoice platform. **The threshold in force is NIS 5,000 (before VAT) from June 2026**, but the threshold is date-dependent and the sheet holds history: NIS 25,000 from May 2024, NIS 20,000 from January 2025, NIS 10,000 from January 2026, NIS 5,000 from June 2026, and nothing at all before May 2024. Test each row against the threshold in force on that row's own date, and see Step 10 for the four conditions that must all hold. Without an allocation number the buyer cannot deduct input VAT on the invoice, so capture it whenever it applies, and re-check the threshold before quoting it since it has been lowered repeatedly.

Column L records **withholding tax at source (ניכוי במקור)**. Some clients are required to withhold income tax and pay the business net of that amount, so log the withheld sum here. The business needs its own אישור ניכוי מס במקור (withholding rate certificate) and this column feeds the annual Form 856 the payer files.

For an **osek patur**, drop columns D and E and rename column F to `Amount` / `סכום` (gross only), since no VAT applies. Keep column L (withholding), which can still apply. Drop column K: an osek patur is outside the allocation-number regime in both directions, because it issues receipts rather than tax invoices and cannot deduct input VAT.

**Tax-deductible categories for Israeli businesses:**

| Category (EN) | Category (HE) | Deduction Rate |
|---------------|---------------|----------------|
| Office Rent | שכירות משרד | 100% |
| Equipment | ציוד | Depreciable (פחת) - capitalize and depreciate, not 100% in year 1 |
| Phone & Internet | טלפון ואינטרנט | 100% (if business-only) |
| Professional Services | שירותים מקצועיים | 100% |
| Car Expenses | הוצאות רכב | Income tax: higher of 45% or upkeep minus שווי שימוש. VAT: purchase not deductible, running costs limited |
| Light refreshments on the premises (כיבוד קל) | כיבוד קל בבית העסק | 80% |
| Hosting / entertainment (אירוח) | אירוח | Generally NOT deductible |
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
  --params '{"spreadsheetId":"SPREADSHEET_ID","range":"Sheet1!A1:L1","valueInputOption":"RAW"}' \
  --json '{"values":[["Date","Description","Category","Amount (excl. VAT)","VAT (18%)","Total (incl. VAT)","Type","Invoice #","Payment Method","Notes","Allocation #","Withholding"]]}'
```

### Step 4: Append Income and Expense Entries

When the user wants to log a transaction, calculate the VAT automatically (osek murshe only) and append the row.

**For income entries (user received payment):**

```bash
# Calculate: if user received 5,900 ILS total, the breakdown is:
# Amount excl. VAT = Total / 1.18 = 5,000 ILS
# VAT = Amount * 0.18 = 900 ILS
gws sheets spreadsheets values append \
  --params '{"spreadsheetId":"SPREADSHEET_ID","range":"Sheet1!A:L","valueInputOption":"USER_ENTERED"}' \
  --json '{"values":[["15/01/2026","Web Development Project","Professional Services","5000","900","5900","Income","INV-2026-001","Bank Transfer","","HK-2026-0001","0"]]}'
```

The `+append` helper is a shorter equivalent for a single simple row:

```bash
gws sheets +append --spreadsheet SPREADSHEET_ID \
  --json-values '[["15/01/2026","Web Development Project","Professional Services","5000","900","5900","Income","INV-2026-001","Bank Transfer","","HK-2026-0001","0"]]'
```

**For expense entries:**

```bash
# Example: Office internet bill of 236 ILS (200 + 36 VAT)
gws sheets spreadsheets values append \
  --params '{"spreadsheetId":"SPREADSHEET_ID","range":"Sheet1!A:L","valueInputOption":"USER_ENTERED"}' \
  --json '{"values":[["20/01/2026","Bezeq Internet","Phone & Internet","200","36","236","Expense","","Direct Debit","","",""]]}'
```

**VAT calculation formulas (osek murshe only):**

| Scenario | Formula | Example |
|----------|---------|---------|
| Have total (incl. VAT), need breakdown | Amount = Total / 1.18, VAT = Total - Amount | 1180 / 1.18 = 1000, VAT = 180 |
| Have net amount, need total | VAT = Amount * 0.18, Total = Amount + VAT | 1000 * 0.18 = 180, Total = 1180 |
| Light refreshments on the premises (80%) | Deductible = Amount * 0.80 | 500 * 0.80 = 400 |

### Step 5: Read and Summarize Financial Data

When the user needs a financial overview, read the data and compute summaries.

```bash
# Read all entries from the sheet using the helper (returns the raw values array)
gws sheets +read --spreadsheet SPREADSHEET_ID --range "Sheet1!A:L"

# Equivalent raw API call (response is a ValueRange with a "values" array of arrays)
gws sheets spreadsheets values get --params '{"spreadsheetId":"SPREADSHEET_ID","range":"Sheet1!A:L"}'
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

Limitation: businesses above the monthly-VAT turnover threshold (turnover over NIS 1,775,000 as of 1 January 2026) file VAT **monthly**, not bi-monthly; at or below it they file bi-monthly. Turnover is measured over the determining year, the 12 consecutive months ending 31 August of the preceding tax year, not the calendar year. This threshold is re-indexed each January, so confirm the current figure. Do not confuse it with the separate detailed-reporting (דיווח מפורט) obligation, whose threshold is much LOWER: from 1 January 2026 a self-employed individual with turnover above NIS 500,000 must file the itemised PCN874 report, which lists every invoice rather than totals and must reconcile exactly with the periodic return. Above that turnover a plain spreadsheet stops being sufficient on its own. `scripts/vat-summary.py` and Steps 5-6 assume the 6 bi-monthly periods only. For a monthly filer, run the summary per calendar month instead of per bi-monthly period and confirm the reporting cadence with the accountant.

### Step 6: Generate Tax-Period Summary Reports

When the user needs to prepare data for their accountant or for VAT reporting, create a summary sheet.

```bash
# Read all data
gws sheets +read --spreadsheet SPREADSHEET_ID --range "Sheet1!A:L"
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
  --params '{"spreadsheetId":"SPREADSHEET_ID","range":"Sheet1!A:L"}' --format csv > business-tracker-2026.csv

# Export a specific VAT period
gws sheets spreadsheets values get \
  --params '{"spreadsheetId":"SPREADSHEET_ID","range":"VAT-Period-1!A:D"}' --format csv > vat-period-1-2026.csv
```

Use the `scripts/backup-sheets.py` script for automated multi-tab backup (both bundled scripts need Python 3.10 or newer, and `--tabs` is required because the script does not enumerate tabs for you):

```bash
python3 scripts/backup-sheets.py --spreadsheet-id SPREADSHEET_ID --output-dir ./backups/2026-01 --tabs "Sheet1,VAT-Period-1"
```

**Document retention.** Israeli bookkeeping rules require the business to keep its books and all supporting documents (invoices, receipts, bank records) for at least 7 years from the end of the tax year (or 6 years from the date the annual return was filed, whichever is later). A CSV backup is a convenience copy, not a substitute for retaining the original documents. Tell the user to archive backups in dated folders and keep the source invoices/receipts for the full retention period.

### Step 8: Auto-Log Payments from Structured Input

When the user provides transaction data in bulk (from a bank statement or invoice list), parse and append multiple rows in one call.

```bash
# Append multiple rows in one call
gws sheets spreadsheets values append \
  --params '{"spreadsheetId":"SPREADSHEET_ID","range":"Sheet1!A:L","valueInputOption":"USER_ENTERED"}' \
  --json '{"values":[
    ["01/02/2026","Client A - Monthly Retainer","Professional Services","10000","1800","11800","Income","INV-2026-010","Bank Transfer","","HK-2026-0010","0"],
    ["03/02/2026","AWS Hosting","Software & Subscriptions","450","81","531","Expense","","Credit Card","","",""],
    ["05/02/2026","Office refreshments","כיבוד קל","300","54","354","Expense","","Credit Card","80% for income tax; input VAT on refreshments generally NOT deductible","",""]
  ]}'
```

### Step 9: Use Dry-Run Mode for Validation

Before making changes, offer the user a dry-run preview. The `--dry-run` flag validates the request locally without sending it to the API.

```bash
# Preview what would be appended without writing
gws sheets spreadsheets values append \
  --params '{"spreadsheetId":"SPREADSHEET_ID","range":"Sheet1!A:L","valueInputOption":"USER_ENTERED"}' \
  --json '{"values":[["15/03/2026","Test Entry","Office Rent","5000","900","5900","Expense","","Bank Transfer","","",""]]}' \
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

**Allocation number (מספר הקצאה) e-invoice mandate.** Israel's continuous-transaction-control model requires an allocation number from the Tax Authority's platform for a tax invoice above the threshold, before the buyer can deduct input VAT. The regime began in May 2024 and the threshold has stepped down since, so a sheet that holds several years of history needs the WHOLE table, not just today's row (amounts exclude VAT):

| In force from | Threshold |
|---|---|
| May 2024 | NIS 25,000 |
| January 2025 | NIS 20,000 |
| January 2026 | NIS 10,000 |
| June 2026 | NIS 5,000 |

Invoices dated before May 2024 predate the regime entirely and never needed an allocation number. Scope the check to each invoice's OWN date against the threshold in force on that date: do not apply today's NIS 5,000 figure to a 2025 invoice that only needed a number above NIS 20,000, or to a 2024 invoice whose threshold was NIS 25,000, and do not flag a pre-May-2024 row as missing one. Backfilling old invoices into a new sheet is exactly where this goes wrong.

An allocation number is required only when ALL of these hold, so do not flag a row that fails any of them: the amount is above the threshold in force on that date; the invoice carries a VAT component (a zero-rated invoice, or one covering only exempt transactions, does NOT need an allocation number, so do not flag export or zero-rated rows); the recipient is an osek murshe; and the recipient asked for an allocation number. A ledger row does not record whether the buyer asked, so do not treat that last condition as a reason to stay silent: flag any row that meets the first three and has an empty column K as "verify", rather than skipping it. The number itself is 9 digits. Note the precise effect of a missing one: it blocks the RECIPIENT's input-VAT deduction. It does not, by itself, make the invoice void. When logging a qualifying invoice, remind the user to obtain the number through their invoicing software and record it in column K alongside the invoice number.

## Examples

### Example 1: Israeli Freelancer Sets Up Monthly Tracking

User says: "Create a Google Sheet to track my freelance income and expenses with VAT"

Actions:
1. Ask whether the user is an osek murshe or an osek patur (this decides whether VAT columns are included)
2. Run `gws sheets spreadsheets create --json '{"properties":{"title":"Freelance Tracker 2026"}}'` and read the `spreadsheetId` from the response
3. Write the header row with `gws sheets spreadsheets values update` (12 columns for an osek murshe, fewer for an osek patur)
4. Show the user the spreadsheet ID and link, and explain the column structure

Result: A new Google Sheet with the correct Israeli structure for the user's VAT status, ready for entries.

### Example 2: Generate Bi-Monthly VAT Summary for Accountant

User says: "Create a VAT summary for January-February 2026 and export it as CSV"

Actions:
1. Run `gws sheets +read --spreadsheet SPREADSHEET_ID --range "Sheet1!A:L"` to pull all entries
2. Run `python3 scripts/vat-summary.py` to filter Jan-Feb transactions and compute totals
3. Add a "VAT-Period-1-2026" tab with `gws sheets spreadsheets batchUpdate` and write the summary with `gws sheets spreadsheets values update`
4. Export the summary tab with `gws sheets spreadsheets values get --format csv`
5. Display the summary: total income, total expenses, VAT collected, input VAT, net VAT liability

Result: A clean VAT period summary both in the Google Sheet and as a local CSV file ready to send to the accountant.

### Example 3: Auto-Log Bank Transfers into Expense Sheet

User says: "I got these payments this month: Client A paid 11,800 for consulting, I paid 531 for hosting, and 354 for a business lunch"

Actions:
1. Parse each transaction, calculate the VAT breakdown (divide totals by 1.18)
2. Categorize: consulting = Professional Services (income), hosting = Software & Subscriptions (expense). A client lunch is NOT an 80% item: hosting and entertainment in Israel are generally not deductible at all, and the 80% rate applies only to light refreshments consumed at the place of business
3. Use `gws sheets spreadsheets values append` with a multi-row `values` array in `--json`
4. Confirm all entries were logged with correct VAT calculations

Result: Three new rows appended to the tracking sheet with proper categorization, VAT breakdown, and deductibility notes.

## Bundled Resources

### Scripts
- `scripts/vat-summary.py` -- Generate bi-monthly VAT summary reports from sheet data. Run: `python3 scripts/vat-summary.py --help`
- `scripts/backup-sheets.py` -- Backup Google Sheets tabs as local CSV files. Run: `python3 scripts/backup-sheets.py --help`

### References
- `references/israeli-tax-categories.md` -- Complete list of Israeli tax-deductible expense categories with deduction rates, plus VAT and osek patur/murshe rules. Consult when categorizing a business expense or confirming a tax fact.
- `references/gws-sheets-recipes.md` -- Common gws CLI recipes for Google Sheets operations. Consult when performing sheet operations beyond basic read/append.

## Gotchas

- Israeli VAT reporting periods are bi-monthly (every 2 months), not quarterly as in many other countries. Agents may structure summaries on a quarterly basis, which does not match Israeli tax authority requirements.
- Israeli date format is DD/MM/YYYY, not MM/DD/YYYY. Agents may use the American format, which causes confusion and errors when dates like 03/04/2026 could mean either March 4 or April 3.
- An osek patur does not charge VAT on income and cannot reclaim input VAT on expenses. Agents may add VAT columns and compute a VAT liability for an osek patur, which is wrong. Always confirm the user's VAT status first.
- The 80% rate applies ONLY to light refreshments (כיבוד קל) consumed at the place of business. Hosting and entertainment (אירוח), including taking a client to a restaurant, are generally not deductible at all. Treating a client lunch as an 80% item overstates the deduction, and treating it as 100% overstates it further.
- Car expenses: for income tax the deductible amount is the HIGHER of 45% of the vehicle upkeep or the upkeep minus the שווי שימוש (use value), not the lower of the two, and there is no per-kilometre deduction regime for the Israeli self-employed. For VAT the rule is stricter still: input VAT on the purchase or import of a private vehicle is not deductible at all, even at 100% business use, and running costs are limited. Applying a 100% deduction is wrong on both taxes.
- Equipment (computers, monitors, furniture) is a depreciable asset (פחת), not a 100%-in-year-one expense. Agents may book the full purchase price as a one-time expense, which overstates the first-year deduction. Capitalize the asset and spread the deduction over its useful life (for example, computers are commonly depreciated at 33.33% a year over 3 years). Only low-value or consumable office items are expensed in full in the year of purchase. The input VAT on the purchase is still fully reclaimable in the first period (osek murshe). Confirm the depreciation rate and any low-value threshold with the accountant.
- Israeli VAT is 18% (since January 2025). Agents trained on older data may use 17%, which was the previous rate, leading to incorrect calculations throughout the spreadsheet. The rate is also date-dependent, so a sheet that carries 2024 rows crosses the change: derive VAT on each row from the rate in force at that row's date rather than applying the column header's 18% to everything.
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
Solution: Always round VAT to 2 decimal places. In Python use `round(amount * 0.18, 2)`; in the sheet itself use `=ROUND(D2*0.18, 2)`. (`Math.round` is JavaScript and runs on neither surface this skill uses.) Israeli tax authority accepts rounding to the nearest agora.
