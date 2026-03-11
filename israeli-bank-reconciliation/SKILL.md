---
name: israeli-bank-reconciliation
description: >-
  Automates bank reconciliation for Israeli banks (Leumi, Hapoalim, Discount, Mizrahi
  Tefahot) using the israeli-bank-scrapers library. Matches scraped or imported transactions
  to invoices and receipts, detects discrepancies, and generates reconciliation reports
  with matched, unmatched, and suspicious entries. Handles shekel amounts, Hebrew
  merchant names, and Israeli date formats. Use when you need to reconcile bank statements
  against your accounting records, identify missing invoices, or prepare monthly closing
  reports for Israeli business accounts. Do NOT use for international bank accounts,
  cryptocurrency wallets, or investment portfolio reconciliation.
license: MIT
allowed-tools: Bash(node:*) Bash(npm:*) Bash(npx:*) Bash(python:*) Read Edit Write
  WebFetch
compatibility: >-
  Requires Node.js 18+ for israeli-bank-scrapers. Works with Claude Code, Cursor,
  and other compatible agents.
metadata:
  author: skills-il
  version: 1.0.0
  category: accounting
  tags:
    he:
    - התאמת-בנק
    - הנהלת-חשבונות
    - בנקים-ישראליים
    - אוטומציה
    - עסקאות
    - חשבונאות
    en:
    - bank-reconciliation
    - bookkeeping
    - israeli-banks
    - automation
    - transactions
    - accounting
  display_name:
    he: התאמת בנק ישראלי
    en: Israeli Bank Reconciliation
  display_description:
    he: אוטומציה של התאמת בנק לבנקים ישראליים, כולל זיהוי פערים והפקת דוחות התאמה
    en: >-
      Automates bank reconciliation for Israeli banks (Leumi, Hapoalim, Discount,
      Mizrahi Tefahot) using the israeli-bank-scrapers library. Matches scraped or
      imported transactions to invoices and receipts, detects discrepancies, and generates
      reconciliation reports with matched, unmatched, and suspicious entries. Handles
      shekel amounts, Hebrew merchant names, and Israeli date formats. Use when you
      need to reconcile bank statements against your accounting records, identify
      missing invoices, or prepare monthly closing reports for Israeli business accounts.
      Do NOT use for international bank accounts, cryptocurrency wallets, or investment
      portfolio reconciliation.
  supported_agents:
  - claude-code
  - cursor
  - github-copilot
  - windsurf
  - opencode
  - codex
---


# Israeli Bank Reconciliation

Automate the process of reconciling Israeli bank transactions against your accounting records. This skill leverages the open-source `israeli-bank-scrapers` library to fetch transactions and provides a structured workflow for matching, discrepancy detection, and report generation.

## Instructions

### Step 1: Set Up the Environment

Install the required dependencies for bank scraping and data processing.

```bash
npm init -y
npm install israeli-bank-scrapers csv-parse csv-stringify dayjs
```

If you plan to use OFX import instead of scraping, also install:

```bash
npm install ofx-js
```

For reference, the core scraping library is maintained at: https://github.com/eshaham/israeli-bank-scrapers

For users who want automated budget tracking alongside reconciliation, consider Caspion: https://github.com/brafdlog/caspion

### Step 2: Configure Bank Credentials

Create a configuration file for your bank connections. Never hardcode credentials directly in scripts.

Create a file named `bank-config.json` with the following structure:

```json
{
  "accounts": [
    {
      "id": "main-business",
      "bank": "hapoalim",
      "credentials": {
        "userCode": "${BANK_USER_CODE}",
        "password": "${BANK_PASSWORD}"
      }
    }
  ]
}
```

Supported bank identifiers:
- `hapoalim` - Bank Hapoalim
- `leumi` - Bank Leumi
- `discount` - Discount Bank
- `mizrahi` - Mizrahi Tefahot
- `otsar-hahayal` - Otsar Ha-Hayal
- `mercantile` - Mercantile Discount Bank
- `max` - Max (formerly Leumi Card)
- `visa-cal` - Visa Cal
- `isracard` - Isracard

Store actual credentials in environment variables, not in the config file.

### Step 3: Fetch Bank Transactions

Create a scraping script that fetches transactions for a configurable date range.

```javascript
const { createScraper } = require('israeli-bank-scrapers');

async function fetchTransactions(bankId, credentials, startDate) {
  const scraper = createScraper({
    companyId: bankId,
    startDate: startDate,
    combineInstallments: false,
    showBrowser: false
  });

  const result = await scraper.scrape(credentials);

  if (!result.success) {
    throw new Error(`Scrape failed: ${result.errorType} - ${result.errorMessage}`);
  }

  return result.accounts.flatMap(account =>
    account.txns.map(txn => ({
      date: txn.date,
      amount: txn.chargedAmount,
      description: txn.description,
      memo: txn.memo || '',
      reference: txn.identifier || '',
      status: txn.status,
      accountNumber: account.accountNumber
    }))
  );
}
```

### Step 4: Import Accounting Records

Load your invoices and receipts from CSV, or connect to your accounting system. The reconciliation expects records in a normalized format.

Expected accounting record format:

| Field | Type | Description |
|-------|------|-------------|
| `date` | `YYYY-MM-DD` | Transaction date |
| `amount` | `number` | Amount in ILS (negative for expenses) |
| `reference` | `string` | Invoice/receipt number |
| `vendor` | `string` | Vendor or payee name |
| `category` | `string` | Accounting category |

For CSV import, handle Israeli-specific formatting:
- Shekel amounts may use comma as decimal separator (1,234.56 or 1.234,56)
- Dates may appear as DD/MM/YYYY (Israeli format) rather than YYYY-MM-DD
- Hebrew merchant names require UTF-8 encoding

### Step 5: Define Matching Rules

Configure rules for automatic transaction matching. The matching engine supports multiple strategies applied in priority order.

**Exact match**: Match by reference number and exact amount.

**Fuzzy match**: Match by date range (+/- 3 days), amount tolerance (within 1 ILS), and vendor name similarity.

**Pattern match**: Define regex patterns for recurring transactions (rent, utilities, subscriptions).

```javascript
const matchingRules = [
  {
    name: 'exact-reference',
    priority: 1,
    match: (bankTxn, accRecord) =>
      bankTxn.reference === accRecord.reference &&
      Math.abs(bankTxn.amount - accRecord.amount) < 0.01
  },
  {
    name: 'amount-date-fuzzy',
    priority: 2,
    match: (bankTxn, accRecord) => {
      const dateDiff = Math.abs(
        dayjs(bankTxn.date).diff(dayjs(accRecord.date), 'day')
      );
      const amountDiff = Math.abs(bankTxn.amount - accRecord.amount);
      return dateDiff <= 3 && amountDiff <= 1.0;
    }
  },
  {
    name: 'recurring-pattern',
    priority: 3,
    patterns: [
      { regex: /חשמל|electric/i, category: 'utilities' },
      { regex: /ארנונה|municipal/i, category: 'municipal-tax' },
      { regex: /ביטוח|insurance/i, category: 'insurance' }
    ]
  }
];
```

### Step 6: Run the Reconciliation Engine

Execute the matching process and categorize results into three buckets:
1. **Matched** - Bank transaction paired with an accounting record
2. **Unmatched bank** - Bank transactions with no corresponding accounting record (missing invoices)
3. **Unmatched accounting** - Accounting records with no corresponding bank transaction (pending deposits or errors)

Additionally flag suspicious transactions:
- Duplicate amounts on the same date
- Unusually large transactions (above a configurable threshold)
- Transactions on weekends or holidays (Israeli calendar)

### Step 7: Generate Reconciliation Reports

Produce a structured report showing the reconciliation status.

The report should include:
- **Summary section**: Total matched, unmatched counts and amounts on each side
- **Matched transactions table**: Bank entry paired with its accounting record
- **Unmatched bank transactions**: Sorted by amount descending for prioritization
- **Unmatched accounting records**: Records to investigate
- **Suspicious items**: Flagged entries requiring manual review
- **Balance comparison**: Bank ending balance vs. accounting ledger balance, with the reconciliation difference

Output formats:
- CSV for import into spreadsheet software
- JSON for programmatic consumption
- Console summary for quick review

## Examples

### Example 1: Monthly Reconciliation for a Small Business

User says: "Reconcile my Hapoalim business account for January 2026 against my QuickBooks export."

Actions:
1. Fetch transactions from Bank Hapoalim for January 1-31, 2026 using `israeli-bank-scrapers`
2. Parse the QuickBooks CSV export, normalizing dates from DD/MM/YYYY to YYYY-MM-DD and amounts to ILS
3. Run matching rules: exact reference match first, then fuzzy date+amount match
4. Identify 142 matched transactions, 8 unmatched bank transactions, and 3 unmatched accounting records

Result: A reconciliation report showing 98% match rate. The 8 unmatched bank entries are petty cash ATM withdrawals missing receipts. The 3 unmatched accounting records are checks not yet cleared. The report highlights one suspicious duplicate charge of 2,450 ILS at the same vendor on the same date.

### Example 2: Multi-Bank Reconciliation with Credit Cards

User says: "I need to reconcile both my Leumi checking account and my Max credit card against my accounting system for Q4 2025."

Actions:
1. Fetch transactions from Bank Leumi (October-December 2025) and Max credit card for the same period
2. Load accounting records from a CSV export filtered to Q4
3. Run reconciliation separately for each account, then produce a combined summary
4. Flag credit card installment transactions (split payments) that appear as single entries in accounting

Result: Combined reconciliation report covering both accounts. Leumi checking shows 97% match rate with 12 unmatched items. Max credit card shows 91% match rate, with most unmatched items being installment splits. Report includes a recommendation to split 4 accounting entries to match the installment pattern. Total reconciliation difference: 127.50 ILS traced to a foreign currency conversion rounding difference.

### Example 3: Detecting Missing Invoices Before Tax Filing

User says: "I need to find all bank transactions from 2025 that don't have matching invoices before I file my annual tax return."

Actions:
1. Fetch full year of transactions from Discount Bank for 2025
2. Load the complete invoice register exported from the accounting system
3. Match all transactions, focusing on identifying unmatched bank debits (expenses without invoices)
4. Group unmatched transactions by vendor and category

Result: Found 34 expense transactions totaling 18,200 ILS without matching invoices. The largest gaps are: office supplies from a vendor billed in cash (6 transactions, 3,400 ILS), software subscriptions charged in USD and converted (8 transactions, 5,100 ILS), and parking/toll charges (20 small transactions, 9,700 ILS). Provides a prioritized list for the accountant to locate or create missing invoices.

## Bundled Resources

### References
- `israeli-bank-scrapers` library documentation: https://github.com/eshaham/israeli-bank-scrapers - Consult when adding support for new bank types or troubleshooting scraper configuration.
- Caspion automated budget tracking: https://github.com/brafdlog/caspion - Consult when users want to combine reconciliation with ongoing budget tracking and categorization.

## Troubleshooting

### Error: "Scrape failed: INVALID_PASSWORD"
Cause: The bank credentials are incorrect, expired, or the account requires a password reset. Some Israeli banks also enforce periodic password changes.
Solution: Verify credentials by logging into the bank's website manually. If the password was recently changed, update the environment variables. For banks requiring OTP or two-factor authentication, ensure the scraper configuration includes the required additional fields.

### Error: "No transactions found for the specified date range"
Cause: The date range may be too narrow, the account may have no activity, or the bank's scraper may require a different date format.
Solution: Expand the date range and verify that the `startDate` is a valid JavaScript Date object. Check that the bank account has transactions in the specified period by logging into the bank's website. Some scrapers return transactions from the start date to today, not to a specified end date.

### Error: "CSV parsing failed: unexpected character at position N"
Cause: Israeli accounting software often exports CSV with Windows-1255 (Hebrew) encoding or includes BOM markers that trip up UTF-8 parsers.
Solution: Convert the file to UTF-8 before parsing: `iconv -f WINDOWS-1255 -t UTF-8 input.csv > output.csv`. Alternatively, specify the encoding in the CSV parser options. Also check for semicolon delimiters (common in Israeli Excel exports) instead of commas.

### Error: "Amount mismatch: bank shows -X but accounting shows -Y"
Cause: Rounding differences in currency conversion, VAT calculations, or installment splitting can cause small discrepancies between bank amounts and accounting entries.
Solution: Configure the matching tolerance threshold. For shekel amounts, a tolerance of 1.00 ILS handles most rounding cases. For transactions involving foreign currency conversion, increase tolerance to 5.00 ILS. If discrepancies are systematic, check whether VAT (17% in Israel) is included in bank amounts but excluded in accounting entries.
