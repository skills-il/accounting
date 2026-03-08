---
name: israeli-financial-reports
description: >-
  Generate Israeli-standard financial reports including profit and loss (Doch Ruvach VeHefsed),
  balance sheet (Maazan), trial balance (Maazan Bochein), and cash flow statements. Supports
  bilingual Hebrew/English output with NIS formatting, VAT summary reports for bi-monthly and
  monthly filing, year-end annual report preparation, and comparison periods. Works with Osek
  Patur, Osek Murshe, and Chevra (company) business types. Compliant with Israeli accounting
  standards based on IFRS adaptations. Use when you need to produce financial statements,
  tax-related summaries, or periodic reports for Israeli businesses. Exports to PDF, Excel,
  and CSV formats. Do NOT use for tax filing submissions, payroll processing, or bank
  reconciliation workflows.
license: MIT
allowed-tools: "Bash(python:*) Edit Read Write"
compatibility: "Requires Claude Code"
metadata:
  author: skills-il
  version: 1.0.0
  category: accounting
  tags:
    he:
      - דוחות-כספיים
      - רווח-והפסד
      - מאזן
      - תקנים-ישראליים
      - דיווח
      - חשבונאות
    en:
      - financial-reports
      - profit-loss
      - balance-sheet
      - israeli-standards
      - reporting
      - accounting
  display_name:
    he: "דוחות כספיים ישראליים"
    en: "Israeli Financial Reports"
  display_description:
    he: "הפקת דוחות כספיים בתקנים ישראליים: רווח והפסד, מאזן, מאזן בוחן, תזרים מזומנים ודוחות מע\"מ"
    en: "Generate Israeli-standard financial reports: profit and loss, balance sheet, trial balance, cash flow, and VAT summaries"
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
---

# Israeli Financial Reports

## Instructions

### Step 1: Identify the Business Type and Reporting Period

Determine the business entity type before generating any report. Each type has different reporting requirements under Israeli law:

- **Osek Patur** (Exempt Dealer): Simplified reporting, no VAT collection, annual revenue under the exempt threshold. Reports focus on income summary and annual declaration.
- **Osek Murshe** (Licensed Dealer): Full VAT reporting required bi-monthly (or monthly if revenue exceeds threshold). Must produce profit and loss, and submit VAT returns.
- **Chevra (Company)**: Full financial statements required including balance sheet, profit and loss, cash flow statement, and notes to financial statements. Subject to Israeli Companies Ordinance and Securities Authority requirements if public.

Confirm the reporting period: monthly, bi-monthly (for VAT), quarterly, or annual.

### Step 2: Gather Financial Data

Collect the following data sources:

1. **Chart of Accounts (Matkonit Cheshbonot)**: The account structure following Israeli standard numbering:
   - 1xxx: Assets (Rechush)
   - 2xxx: Liabilities (Hitchayvuyot)
   - 3xxx: Equity (Hon Atzmi)
   - 4xxx: Revenue (Hachnasot)
   - 5xxx: Cost of Goods Sold (Olut HaMecher)
   - 6xxx: Operating Expenses (Hotzaot Tifuliyot)
   - 7xxx: Financial Income/Expenses (Hachnasot/Hotzaot Mimun)
   - 8xxx: Other Income/Expenses (Hachnasot/Hotzaot Acherot)
   - 9xxx: Tax and Adjustments (Mas VeHitakmuyot)

2. **Transaction Journal (Yoman Peulot)**: All posted transactions for the period.
3. **Opening Balances (Yitrot Pticha)**: Carried forward from previous period close.
4. **VAT Records**: Input VAT (Maam Tsfumot) and Output VAT (Maam Etzumot) for the period.

### Step 3: Generate the Trial Balance (Maazan Bochein)

Produce a trial balance that lists all accounts with their debit and credit balances:

```
Maazan Bochein / Trial Balance
Period: January - December 2025
Currency: NIS (New Israeli Shekel)

Account  | Account Name           | Debit (NIS)  | Credit (NIS)
---------|------------------------|-------------- |--------------
1010     | Cash (Kupah)           | 45,230.00    |
1020     | Bank Leumi (Current)   | 328,750.50   |
1030     | Accounts Receivable    | 125,400.00   |
2010     | Accounts Payable       |              | 89,200.00
2020     | VAT Payable            |              | 12,350.00
3010     | Owner's Equity         |              | 200,000.00
4010     | Service Revenue        |              | 650,800.00
5010     | Direct Costs           | 180,000.00   |
6010     | Salaries (Maskorot)    | 195,000.00   |
6020     | Rent (Schar Dira)      | 48,000.00    |
6030     | Office Expenses        | 15,200.00    |
7010     | Bank Charges           | 3,800.00     |
9010     | Income Tax Provision   | 10,969.50    |
         | TOTALS                 | 952,350.00   | 952,350.00
```

Verify that total debits equal total credits. Any imbalance indicates posting errors that must be resolved before proceeding.

### Step 4: Generate the Profit and Loss Statement (Doch Ruvach VeHefsed)

Structure the P&L according to Israeli format:

```
Doch Ruvach VeHefsed / Profit and Loss Statement
For the Year Ended December 31, 2025
(Amounts in NIS)

                                    Current Year    Previous Year
                                    -----------     ------------
Revenue (Hachnasot):
  Service Revenue                    650,800.00      580,200.00
  Other Revenue                        8,500.00        5,100.00
                                    -----------     ------------
Total Revenue                        659,300.00      585,300.00

Cost of Revenue (Olut HaMecher):
  Direct Costs                      (180,000.00)    (155,000.00)
                                    -----------     ------------
Gross Profit (Revach Golmi)          479,300.00      430,300.00

Operating Expenses (Hotzaot Tifuliyot):
  Salaries and Benefits             (195,000.00)    (175,000.00)
  Rent                               (48,000.00)     (48,000.00)
  Office and General                  (15,200.00)     (12,800.00)
  Depreciation (Pachat)              (22,000.00)     (20,000.00)
                                    -----------     ------------
Total Operating Expenses            (280,200.00)    (255,800.00)

Operating Profit (Revach Tifuli)     199,100.00      174,500.00

Financial Expenses (Hotzaot Mimun):
  Bank Charges                        (3,800.00)      (3,200.00)
  Interest Expense                    (6,500.00)      (5,800.00)
                                    -----------     ------------
Profit Before Tax (Revach Lifnei Mas) 188,800.00     165,500.00

Income Tax (Mas Hachnasa)            (43,424.00)     (38,065.00)
                                    -----------     ------------
Net Profit (Revach Naki)             145,376.00      127,435.00
```

Apply the current Israeli corporate tax rate (23% as of 2025) for Chevra entities. For Osek Murshe, use marginal personal tax brackets.

### Step 5: Generate the Balance Sheet (Maazan)

Structure according to Israeli format with assets on one side, liabilities and equity on the other:

```
Maazan / Balance Sheet
As of December 31, 2025
(Amounts in NIS)

ASSETS (RECHUSH)                          Current Year    Previous Year
Current Assets (Rechush Shotef):
  Cash and Cash Equivalents                 45,230.00       38,500.00
  Bank Accounts                            328,750.50      275,100.00
  Accounts Receivable (Chayavim)           125,400.00      110,200.00
  Prepaid Expenses (Hotzaot Mera'sh)        12,000.00       10,000.00
                                          -----------     ------------
Total Current Assets                       511,380.50      433,800.00

Non-Current Assets (Rechush Lo Shotef):
  Equipment (Tziud)                        180,000.00      160,000.00
  Less: Accumulated Depreciation           (62,000.00)     (40,000.00)
  Intangible Assets                         25,000.00       30,000.00
                                          -----------     ------------
Total Non-Current Assets                   143,000.00      150,000.00

TOTAL ASSETS                               654,380.50      583,800.00

LIABILITIES AND EQUITY (HITCHAYVUYOT VEHON ATZMI)
Current Liabilities (Hitchayvuyot Shotfot):
  Accounts Payable (Zakaim)                 89,200.00       75,400.00
  VAT Payable (Maam Leshalem)               12,350.00       10,800.00
  Accrued Expenses (Hotzaot Leshlem)        18,500.00       15,200.00
  Income Tax Payable                        43,424.00       38,065.00
                                          -----------     ------------
Total Current Liabilities                  163,474.00      139,465.00

Non-Current Liabilities:
  Long-term Loan (Halvaat Tzvei Aroch)     145,530.50      144,335.00
                                          -----------     ------------
Total Liabilities                          309,004.50      283,800.00

Equity (Hon Atzmi):
  Share Capital (Hon Minayot)              200,000.00      200,000.00
  Retained Earnings (Revachim Tzvurim)     145,376.00      100,000.00
                                          -----------     ------------
Total Equity                               345,376.00      300,000.00

TOTAL LIABILITIES AND EQUITY               654,380.50      583,800.00
```

### Step 6: Generate the Cash Flow Statement (Doch Tazrim Mezumanim)

Use the indirect method as standard in Israeli reporting:

1. **Operating Activities (Peulot Shototfot)**: Start with net profit, adjust for non-cash items (depreciation, provisions), and working capital changes.
2. **Investing Activities (Peulot Hashkaa)**: Capital expenditures, asset sales, investment purchases.
3. **Financing Activities (Peulot Mimun)**: Loan proceeds/repayments, equity contributions, dividend payments.

### Step 7: Generate VAT Summary Report (Doch Maam)

For Osek Murshe and Chevra, prepare the VAT summary:

```
VAT Summary Report (Doch Sikum Maam)
Period: November - December 2025
Business: Example Ltd. (Osek Murshe)
VAT Registration: 515-123456

Output VAT (Maam Etzumot):
  Taxable Sales                    185,400.00
  VAT at 17%                       31,518.00

Input VAT (Maam Tsfumot):
  Purchases and Expenses            98,200.00
  VAT Claimed                      16,694.00

VAT Payable (Maam Leshalem):        14,824.00
Due Date: January 15, 2026
```

### Step 8: Format and Export

Apply proper formatting for all reports:

- **Currency**: NIS amounts with thousands separator (comma) and two decimal places: 1,234,567.89
- **Negative amounts**: Use parentheses for negative values: (45,000.00)
- **Bilingual headers**: Include both Hebrew and English section headers
- **Comparison columns**: Current period alongside previous period
- **Export formats**: PDF (for submission), Excel (for analysis), CSV (for import into accounting software)

## Examples

### Example 1: Monthly VAT Report for Osek Murshe

User says: "Generate my VAT report for the Jan-Feb 2025 bi-monthly period. I am an Osek Murshe. My sales were 120,000 NIS and my deductible purchases were 45,000 NIS."

Actions:
1. Confirm business type as Osek Murshe (bi-monthly VAT filing).
2. Calculate Output VAT: 120,000 x 17% = 20,400 NIS.
3. Calculate Input VAT: 45,000 x 17% = 7,650 NIS.
4. Calculate net VAT payable: 20,400 - 7,650 = 12,750 NIS.
5. Generate formatted bilingual VAT summary report with due date (March 15, 2025).

Result: A formatted VAT summary report showing 12,750 NIS payable to the Tax Authority (Rashut HaMisim), with bilingual headers and proper NIS formatting.

### Example 2: Annual Financial Statements for a Chevra

User says: "Prepare the full annual financial statements for my company for 2025. I have my trial balance data ready."

Actions:
1. Import trial balance data from the user's source.
2. Verify trial balance balances (debits = credits).
3. Generate Profit and Loss statement with current year vs. previous year comparison.
4. Generate Balance Sheet with proper asset/liability/equity classification.
5. Generate Cash Flow Statement using indirect method.
6. Apply 23% corporate tax rate to calculate tax provision.
7. Add bilingual headers (Hebrew/English) to all reports.
8. Format all amounts in NIS with proper separators and parentheses for negatives.
9. Export to PDF and Excel.

Result: Complete set of annual financial statements (P&L, Balance Sheet, Cash Flow) in bilingual format, ready for submission to the Registrar of Companies (Rasham HaChevrot) and the Tax Authority.

### Example 3: Quarterly Comparison Report for Management

User says: "I need a Q3 vs Q2 profit and loss comparison for my business to present to investors."

Actions:
1. Extract Q2 and Q3 financial data from transaction records.
2. Generate side-by-side P&L with columns for Q2, Q3, and change (amount and percentage).
3. Highlight significant variances (changes exceeding 10%).
4. Calculate key ratios: gross margin, operating margin, net margin for both quarters.
5. Add trend indicators and summary commentary.

Result: A management-oriented P&L comparison report showing quarter-over-quarter performance, including variance analysis and margin trends, formatted in NIS with bilingual headers.

## Troubleshooting

### Error: "Trial balance does not balance"

Cause: Total debits do not equal total credits, indicating one or more posting errors in the transaction journal. Common causes include single-sided entries, transposed digits, or unposted adjustments.

Solution:
1. Review the difference amount; check if any single transaction matches that amount.
2. Divide the difference by 2 to check for entries posted to the wrong side.
3. Divide the difference by 9; if it divides evenly, look for transposed digits.
4. Run a journal entry audit to find entries without matching contra-entries.
5. Check for unposted period-end adjustments (depreciation, accruals, provisions).

### Error: "VAT rate mismatch"

Cause: The VAT calculation uses an incorrect rate. Israel's standard VAT rate is 17% (as of 2025). Some transactions may be zero-rated (exports) or exempt (financial services, certain food items, fruits and vegetables at reduced rate).

Solution:
1. Verify the current VAT rate from the Tax Authority (Rashut HaMisim) website.
2. Check if any transactions are zero-rated exports (VAT = 0% but still reportable).
3. Check for VAT-exempt items that should not have VAT applied.
4. Separate transactions by VAT category: standard (17%), zero-rated (0%), exempt.
5. Recalculate the VAT summary with correct rates per category.

### Error: "Currency formatting inconsistency"

Cause: Mixed formatting of NIS amounts across report sections, such as using different decimal separators or inconsistent negative number notation.

Solution:
1. Standardize all amounts to NIS with comma thousands separator: 1,234,567.89
2. Use parentheses for negative values, not minus signs: (45,000.00) not -45,000.00
3. Ensure all amounts show exactly two decimal places.
4. Verify that the NIS symbol or "NIS" label appears consistently in report headers.
