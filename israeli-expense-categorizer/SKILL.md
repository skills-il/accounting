---
name: israeli-expense-categorizer
description: AI-powered categorization of business expenses into Israeli tax-deductible categories based on current Israeli Tax Ordinance rules. Applies the correct deduction mechanics (vehicle = the higher of running-costs-minus-use-value or 45%, mobile phone with the ~50% disallowance floor, home office and internet proportional), maps to a common Israeli chart of accounts, and handles Osek Patur vs Osek Murshe differences for VAT eligibility (private-car VAT not deductible, running-cost VAT two-thirds). Use when you need to classify business expenses for Israeli tax reporting, prepare expense reports for your accountant, or verify deduction eligibility. Do NOT use for final tax filing, legal tax advice, or payroll-related expense processing.
license: MIT
allowed-tools: Bash(python:*) Read Edit Write
compatibility: Requires Claude Code or compatible agent with file access
---


# Israeli Expense Categorizer

## Instructions

### Step 1: Gather expense data

Collect the expense information to categorize. Accept input in any of these formats:

- CSV or Excel file with columns: date, vendor, amount, description
- Bank/credit card statement export
- Free-text list of expenses
- Individual expense for quick classification

If a file path is provided, read the file. If expenses are described in text, parse them into structured records.

### Step 2: Determine business entity type

Ask the user for their business registration type if not already known:

- **Osek Patur** (exempt dealer): Annual turnover under the threshold (NIS 122,833 for 2026, re-indexed from NIS 120,000 that applied in 2024-2025). Cannot charge or deduct VAT. Income tax deductions still apply.
- **Osek Murshe** (licensed dealer): Can charge and deduct VAT. Full income tax deductions apply.
- **Company (Chevra Ba'am)**: Corporate tax rules apply. Full VAT deduction on eligible business expenses, but subject to the same תקנה 14 / תקנה 18 limits as an osek murshe (no input VAT on a private-car purchase, the 2/3 vs 1/4 split on running-cost VAT) and the same אירוח / meals VAT disallowance. A company is NOT exempt from these limits.

This distinction is critical because it affects VAT deduction eligibility.

**עסק זעיר (small-business) election**: Under the 2026 small-business reform (חוק ההתייעלות הכלכלית, פרק "בעל עסק זעיר"), an osek (patur or murshe) whose turnover is under the osek-patur ceiling (the same NIS 122,833 for 2026) can ELECT a flat automatic income-tax deduction of 30% of turnover instead of itemizing actual expenses. An osek patur classified as עסק זעיר receives this 30% deduction automatically. Before categorizing every receipt, compare the 30%-of-turnover flat election against the itemized total this skill produces, the user should claim whichever is higher and confirm eligibility with their accountant.

### Step 3: Apply Israeli tax deduction rules

Categorize each expense using the following deduction rules from the Israeli Tax Ordinance (Pkudat Mas Hachnasa):

**Fully deductible expenses (100%)**:
- Office rent and utilities (electricity, water, arnona for dedicated office)
- Professional services (accountant, lawyer, consultant fees)
- Software subscriptions and SaaS tools used exclusively for business
- Raw materials and inventory
- Business insurance premiums
- Marketing and advertising costs
- Professional development courses directly related to the business
- Office supplies and low-value equipment (immediate expense rather than depreciation; ~1,200 ILS is a common working threshold for flagging low-value items, confirm the current figure with your accountant)
- Website hosting and domain costs
- Employee salaries and related social costs

**Partially deductible expenses**:
- **Vehicle expenses (higher-of rule)**: Fuel, licensing, compulsory + comprehensive insurance, leasing, repairs, parking, tolls, and depreciation. Per תקנות מס הכנסה (ניכוי הוצאות רכב) התשנ"ה-1995, the deductible amount is the HIGHER of [running expenses minus שווי שימוש (use-value)] OR [45% of running expenses]. The common "just take 45%" shortcut is wrong whenever the running-minus-use-value figure is larger. Note: שווי שימוש is NOT a computed or receipt-based number, it is a FIXED monthly amount the Tax Authority sets per vehicle from the official price-group (קבוצת מחיר) table, or for vehicles from 2010 onward as a percentage of the list price (currently 2.48%); look it up via the ITA שווי שימוש calculator so the higher-of branch is actually computable. Hard statutory condition: the user must record odometer (ק"מ) readings at the start and end of the tax year, or the deduction can be disqualified. Applies to a single vehicle used for business; a second vehicle is 0% unless proven business-essential.
- **Mobile phone (טלפון נייד)**: Not a flat 80%. Per תקנות מס הכנסה (ניכוי הוצאות מסוימות) תשל"ב-1972, only the portion ABOVE the lower of 1,380 NIS per year (~115 NIS/month) or 50% of the expense is deductible, which acts as an effective ~50% disallowance floor.
- **Landline from home (טלפון קווי מהבית)**: Deductible is the LOWER of 80% of the expense OR the amount exceeding 2,700 NIS (2025), within an annual ceiling of 26,600 NIS.
- **Internet**: No fixed percentage. Split by actual business-use proportion (for a home connection, use the same business-use share as the home office).
- **Home office (proportional)**: Deduct the percentage of home used exclusively for business. Calculate: (office area / total home area) x 100. Apply this percentage to rent, arnona, electricity, internet, and maintenance.
- **Meals and entertainment** (correct rule, often misapplied):
  - **Hospitality / business meals with Israeli clients (אירוח בארץ): 0% deductible.** Per תקנות ניכוי הוצאות מסויימות 1972 reg. 2(1), hosting Israeli clients/partners is disallowed regardless of receipts. Coffee with a client at Aroma is **not** an 80% expense.
  - **Hospitality with foreign guests visiting Israel (אירוח אורחי חוץ)**: deductible up to a "reasonable" amount with proper documentation of the foreign guest.
  - **Light refreshments at the workplace (כיבוד קל)**: up to 80% deductible per ITA practice (coffee/tea/snacks for staff and visitors at the office).
  - **Foreign-business-trip meals (אש"ל לחו"ל)**: 50% of documented meal cost. Per-diem caps (2025): roughly $97/day when lodging is claimed separately, or roughly $162/day when lodging is not claimed separately.
  - Meals during a regular workday for the self-employed person alone: not deductible.
- **Gifts to clients**: Up to 240 NIS per recipient per year (2025) for gifts given in Israel, and up to $15 USD per foreign recipient per year, per תקנות ניכוי הוצאות מסויימות 1972.

**Non-deductible expenses (0%)**:
- Personal clothing (unless uniforms or protective gear)
- Commuting costs (home to regular workplace)
- Fines and penalties (traffic tickets, late payment penalties to tax authority)
- Personal entertainment
- Life insurance premiums (unless keyman insurance for business)
- Political donations

**Special rules**:
- **Higher-value equipment**: Recognized through depreciation over its useful life rather than immediately (computers: 33% per year, office furniture: 6% per year). Low-value items are taken as an immediate expense; ~1,200 ILS is a common working threshold for flagging which items to treat as low-value, confirm the current figure with your accountant.
- **Depreciation of vehicles**: 15% per year applied to the vehicle cost; the deductible portion of that depreciation is itself folded into the 45% higher-of running-cost rule above.
- **Travel abroad**: Fully deductible if business purpose is documented. Per diem rules apply: accommodation receipts required, meal allowance up to the daily caps noted above (~$97/$162 per day, meals 50%).
- **Work clothing**: Deductible only if branded, protective, or required uniform. Regular business attire is not deductible.

**VAT (Osek Murshe only)**:
- **Private vehicle (רכב פרטי) purchase**: Input VAT on the purchase or import of a private vehicle is NOT deductible at all (תקנה 14).
- **Vehicle running costs (fuel, repairs)**: Input VAT is 2/3 deductible when business is the primary use of the vehicle, and 1/4 deductible otherwise (תקנה 18).
- Keep תקנה 14 and תקנה 18 separate: תקנה 14 blocks input VAT on the PURCHASE of a private vehicle entirely, while תקנה 18 governs the RUNNING-cost VAT (the 2/3 vs 1/4 split). They are different rules and should not be conflated.

### Step 4: Map to Israeli chart of accounts

Map each categorized expense to the appropriate account code using a common Israeli chart-of-accounts convention (the 60-70 ranges below are a widely used convention, not a legal standard; confirm against your accountant's actual scheme):

| Account Range | Category | Examples |
|---|---|---|
| 60-61 | Raw materials and purchases | Inventory, supplies for production |
| 62 | Subcontractors | Outsourced work, freelancer payments |
| 63 | Rent and building maintenance | Office rent, arnona, building repairs |
| 64 | Vehicle expenses | Fuel, car insurance, maintenance |
| 65 | Office and general expenses | Supplies, software, phone, internet |
| 66 | Marketing and sales | Advertising, business meals, events |
| 67 | Professional services | Accountant, lawyer, consulting |
| 68 | Salaries and related | Payroll, social benefits, pension |
| 69 | Financial expenses | Bank fees, interest, exchange differences |
| 70 | Depreciation | Equipment depreciation entries |

### Step 5: Flag items requiring attention

For each expense, flag issues that need human review:

- **Receipt required**: Mark expenses that require a tax invoice (heshbonit mas) vs regular receipt (kabala)
- **Dual-use warning**: Flag items that could be personal or business (phone, internet, car)
- **Missing documentation**: Identify expenses that lack required proof (business meals without attendee info)
- **Threshold alerts**: Note when gift limits or per diem limits are exceeded
- **VAT note**: For Osek Murshe, note which expenses have reclaimable VAT

### Step 6: Generate categorized report

Produce a structured output with:

1. **Summary table**: Total expenses by category, total deductible amount, total non-deductible amount
2. **Detailed line items**: Each expense with category, deduction percentage, deductible amount, account code, and any flags
3. **VAT summary** (Osek Murshe only): Total input VAT reclaimable
4. **Action items**: List of items needing receipts, documentation, or accountant review
5. **Common mistakes detected**: Any personal expenses mixed in, over-claimed dual-use items, or missing documentation

Output as a formatted table or CSV file, depending on user preference.

## Examples

### Example 1: Monthly expense categorization for a freelance developer

User says: "I'm an Osek Murshe freelance developer. Categorize these January expenses:
- Akamai Cloud (formerly Linode): 150 ILS
- Coffee meeting with client at Aroma: 85 ILS
- Cellcom phone bill: 180 ILS
- Fuel for car: 450 ILS
- New keyboard from KSP: 350 ILS
- Accountant monthly fee: 800 ILS
- WeWork hot desk: 1,200 ILS
- Udemy course on React: 120 ILS"

Actions:
1. Identify entity type: Osek Murshe (VAT deductible)
2. Categorize each expense:
   - Akamai Cloud (formerly Linode): 100% deductible, Account 65 (Office/General), 150 ILS
   - Client coffee at Aroma (Israeli client, hospitality in Israel / אירוח בארץ): **0% deductible per reg. 2(1)** of תקנות ניכוי הוצאות מסויימות 1972. The 85 NIS is fully disallowed. The "client meals are 80%" misconception is one of the most common Israeli categorization mistakes.
   - Cellcom mobile phone: NOT a flat 80%. Apply the floor: the non-deductible portion is the lower of 1,380 ILS/year (115 ILS/month) or 50% of the bill. For a 180 ILS monthly bill, 50% (90 ILS) is lower than 115 ILS, so 90 ILS is disallowed and 90 ILS is deductible. Account 65 (Office/General), 90 ILS deductible
   - Fuel: part of vehicle running costs. The simplified 45% gives 202.50 ILS, but the correct figure is the HIGHER of 45% or [running costs minus use-value], computed once across the whole vehicle bundle at year-end. Account 64 (Vehicle), ~202.50 ILS deductible (recompute under the higher-of rule with full-year data)
   - Keyboard: 100% deductible (low-value item, expensed immediately rather than depreciated), Account 65 (Office/General), 350 ILS
   - Accountant fee: 100% deductible, Account 67 (Professional Services), 800 ILS
   - WeWork: 100% deductible, Account 63 (Rent), 1,200 ILS
   - Udemy course: 100% deductible, Account 65 (Office/General), 120 ILS
3. Generate summary: Total expenses 3,335 ILS, Total deductible 2,912.50 ILS, Non-deductible 422.50 ILS (client coffee 85 + disallowed phone portion 90 + disallowed fuel portion 247.50)
4. VAT note: Input VAT reclaimable on most items; the client meal carries no VAT deduction, and vehicle running-cost VAT is limited to 2/3

Result: Categorized expense report with deduction amounts, account codes, and a flag to document the client meeting details.

### Example 2: Home-based business with mixed expenses

User says: "I run a graphic design business from home as Osek Patur. My apartment is 80 sqm and my office room is 12 sqm. Here are my expenses:
- Apartment rent: 5,000 ILS/month
- Electricity bill: 400 ILS
- Arnona: 800 ILS/quarter
- New iMac: 8,500 ILS
- Adobe Creative Cloud: 220 ILS/month
- Parking ticket: 250 ILS
- New jeans: 300 ILS
- Client dinner: 350 ILS
- Printer ink: 95 ILS"

Actions:
1. Identify entity type: Osek Patur (no VAT deduction)
2. Calculate home office ratio: 12/80 = 15%
3. Categorize:
   - Rent: 15% deductible (home office), Account 63, 750 ILS deductible
   - Electricity: 15% deductible, Account 63, 60 ILS deductible
   - Arnona: 15% deductible, Account 63, 120 ILS deductible (quarterly, so 40/month)
   - iMac: 100% deductible but must depreciate over 3 years (33%/year), Account 70, ~2,833 ILS/year depreciation
   - Adobe CC: 100% deductible, Account 65, 220 ILS
   - Parking ticket: 0% deductible (fine/penalty), flag as non-deductible
   - Jeans: 0% deductible (personal clothing), flag as non-deductible
   - Client dinner (אירוח בארץ, hosting an Israeli client): 0% deductible per תקנות ניכוי הוצאות מסויימות 1972. The full 350 ILS is disallowed. Flag as non-deductible (the "client meals are 80%" assumption is wrong)
   - Printer ink: 100% deductible, Account 65, 95 ILS
4. Generate summary with depreciation schedule for the iMac
5. Flag: No VAT deduction available (Osek Patur). Recommend evaluating whether switching to Osek Murshe would be beneficial given equipment purchases.

Result: Categorized report with home office calculations, depreciation schedule, and recommendation to consult accountant about entity type.

### Example 3: Bulk CSV categorization

User says: "Categorize this CSV file of expenses from my bank export" and provides a file path.

Actions:
1. Read the CSV file and parse columns (date, description, amount, vendor)
2. Ask for entity type if not specified
3. Auto-categorize based on vendor names and descriptions using pattern matching:
   - Gas station names (Paz, Sonol, Delek) -> Vehicle running costs; tag for the year-end higher-of rule (45% or running-minus-use-value), do not hard-code 45% per line
   - Cellcom/Partner mobile lines -> Mobile phone; apply the 1,380 ILS-or-50% floor, not a flat 80%
   - Bezeq landline / HOT / internet -> Landline-or-internet; landline is the lower of 80% or the amount over 2,700 ILS, internet is split by business-use proportion
   - Supermarket chains -> Flag as likely personal, 0%
   - Software vendors -> Office/General, 100%
4. Flag ambiguous items for manual review
5. Output categorized CSV with added columns: category, deduction_pct, deductible_amount, account_code, flags

Result: Enriched CSV file ready for accountant import, with flagged items requiring manual classification.

## Gotchas

- Israeli expense deduction rates are specific and easy to get wrong: vehicle expenses follow the higher-of rule (running-minus-use-value or 45%), the mobile phone has a 1,380 ILS-or-50% disallowance floor (not a flat 80%), hosting Israeli clients and business meals are 0% (only כיבוד קל at the workplace is 80%), and internet is a proportional business-use split. Agents may wrongly apply a flat 80% to phones and meals or a flat 45% to cars, or apply 100% deduction to all business expenses.
- Home office expenses in Israel are deductible based on the proportional area used for business, not a flat deduction. Agents may apply US-style simplified home office deduction rules.
- Israeli receipt numbers (mispar kabala) are legally required for expense documentation. A bank statement alone is not sufficient proof for tax deduction. Agents may accept bank records as complete documentation.
- Expense categories must match the Israeli Tax Ordinance (pkudat mas hachnasa) classifications. Agents may use generic US-style categories like "Office Supplies" that do not map directly to Israeli tax categories.
- Mixed personal/business expenses (like a phone used for both) require proportional allocation. Agents may categorize the entire expense as business without applying the required split.


## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Israel Tax Authority | https://www.gov.il/he/departments/israel_tax_authority | Recognized expense categories, VAT deduction rules, bookkeeping directive |
| Deduction of Certain Expenses Regulations 1972 (Nevo) | https://www.nevo.co.il/law_html/law01/255_418.htm | Hosting (אירוח בארץ) disallowance, כיבוד קל 80%, gifts, phone floor |
| Vehicle Expense Deduction Regulations 1995 (Nevo) | https://www.nevo.co.il/law_html/law01/255_439.htm | Higher-of vehicle rule, odometer recording condition |
| Vehicle input-tax (VAT) guide (gov.il) | https://www.gov.il/he/pages/instructions-for-deduction-of-input-tax-for-vehicles-and-motorcycles | Private-car VAT not deductible, running-cost VAT 2/3 vs 1/4 |
| Hashavshevet chart of accounts | https://www.h-erp.co.il | Common Israeli chart-of-accounts convention, account codes, tax codes |
| Kol Zchut - self-employed taxes | https://www.kolzchut.org.il/he/עובדים_עצמאים | Allowed expenses for self-employed, home office, vehicle expenses |
| pandas I/O reference | https://pandas.pydata.org/docs/reference/io.html | CSV/Excel import for bank/credit statements, encoding handling |

## Troubleshooting

### Error: "Cannot determine deduction percentage for this expense"

Cause: The expense description is too vague to classify (e.g., "payment to Moshe" or "transfer 500 ILS").

Solution: Ask the user for more context about the expense: What was purchased? What is the business purpose? Who is the vendor? With this information, apply the appropriate deduction rule. If still unclear, flag it as "requires accountant review" with 0% deduction as the conservative default.

### Error: "Home office percentage seems too high"

Cause: The calculated home office ratio exceeds 50%, which may trigger scrutiny from the tax authority (Mas Hachnasa).

Solution: Verify the room dimensions with the user. If the ratio genuinely exceeds 50%, warn that the tax authority may challenge this claim. Recommend the user keep documentation: floor plan, photos of dedicated office space, and proof that the space is used exclusively for business. If the space is shared (e.g., dining table used as desk), the deduction should be reduced proportionally.

### Error: "Expense file format not recognized"

Cause: The uploaded file is not in a parseable format (corrupted CSV, password-protected Excel, or image/PDF of receipts).

Solution: Ask the user to export their data as a plain CSV with columns: date, vendor/description, amount. For bank exports, most Israeli banks (Leumi, Hapoalim, Discount, Mizrahi) support CSV export from their online banking portal. Guide the user to the export function in their specific bank's interface.

### Error: "VAT deduction claimed but entity is Osek Patur"

Cause: The user's entity type is Osek Patur but VAT deductions were requested or assumed.

Solution: Remind the user that Osek Patur cannot deduct input VAT. Remove any VAT deduction lines from the report. If the user has significant expenses with VAT, suggest they consult their accountant about upgrading to Osek Murshe, especially if their revenue is approaching the Osek Patur threshold or if they regularly purchase expensive equipment.
