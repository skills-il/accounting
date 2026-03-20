---
name: israeli-expense-categorizer
description: >-
  AI-powered categorization of business expenses into Israeli tax-deductible categories
  based on current Israeli Tax Ordinance rules. Applies correct deduction percentages
  (car 45%, phone/internet 80%, home office proportional), maps to standard Israeli
  chart of accounts, and handles Osek Patur vs Osek Murshe differences for VAT eligibility.
  Use when you need to classify business expenses for Israeli tax reporting, prepare
  expense reports for your accountant, or verify deduction eligibility. Do NOT use
  for final tax filing, legal tax advice, or payroll-related expense processing.
license: MIT
allowed-tools: Bash(python:*) Read Edit Write
compatibility: Requires Claude Code or compatible agent with file access
metadata:
  author: skills-il
  version: 1.0.1
  category: accounting
  tags:
    he:
    - מיון-הוצאות
    - ניכויי-מס
    - הנהלת-חשבונות
    - מס-ישראלי
    - הוצאות-עסקיות
    - חשבונאות
    en:
    - expense-categorizer
    - tax-deductions
    - bookkeeping
    - israeli-tax
    - business-expenses
    - accounting
  display_name:
    he: מיון הוצאות עסקיות ישראליות
    en: Israeli Expense Categorizer
  display_description:
    he: מיון אוטומטי של הוצאות עסקיות לקטגוריות מס ישראליות עם אחוזי ניכוי מדויקים
    en: >-
      AI-powered categorization of business expenses into Israeli tax-deductible categories
      based on current Israeli Tax Ordinance rules. Applies correct deduction percentages
      (car 45%, phone/internet 80%, home office proportional), maps to standard Israeli
      chart of accounts, and handles Osek Patur vs Osek Murshe differences for VAT
      eligibility. Use when you need to classify business expenses for Israeli tax
      reporting, prepare expense reports for your accountant, or verify deduction
      eligibility. Do NOT use for final tax filing, legal tax advice, or payroll-related
      expense processing.
  supported_agents:
  - claude-code
  - cursor
  - github-copilot
  - windsurf
  - opencode
  - codex
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

- **Osek Patur** (exempt dealer): Annual revenue under the threshold (currently ~120,000 ILS). Cannot charge or deduct VAT. Income tax deductions still apply.
- **Osek Murshe** (licensed dealer): Can charge and deduct VAT. Full income tax deductions apply.
- **Company (Chevra Ba'am)**: Corporate tax rules apply. Full VAT deduction on business expenses.

This distinction is critical because it affects VAT deduction eligibility.

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
- Office supplies and equipment under 1,200 ILS (immediate expense)
- Website hosting and domain costs
- Employee salaries and related social costs

**Partially deductible expenses**:
- **Vehicle expenses (45%)**: Fuel, maintenance, insurance, parking, tolls. Applies to a single vehicle used for business. Second vehicle: 0% unless proven business-essential.
- **Phone and internet (80%)**: Mobile phone bills, landline, internet service. The 20% disallowed portion reflects assumed personal use.
- **Home office (proportional)**: Deduct the percentage of home used exclusively for business. Calculate: (office area / total home area) x 100. Apply this percentage to rent, arnona, electricity, internet, and maintenance.
- **Meals and entertainment (80%)**: Business meals with clients or partners. Must document: who attended, business purpose, and relationship. Meals during regular workday for self: not deductible.
- **Gifts to clients**: Up to 220 ILS per recipient per year.

**Non-deductible expenses (0%)**:
- Personal clothing (unless uniforms or protective gear)
- Commuting costs (home to regular workplace)
- Fines and penalties (traffic tickets, late payment penalties to tax authority)
- Personal entertainment
- Life insurance premiums (unless keyman insurance for business)
- Political donations

**Special rules**:
- **Equipment over 1,200 ILS**: Must be depreciated over useful life (computers: 3 years at 33%, furniture: 6 years at 15%, vehicles: 5-7 years)
- **Depreciation of vehicles**: 15% per year, applied to max ceiling (currently ~240,000 ILS for standard vehicles)
- **Travel abroad**: Fully deductible if business purpose is documented. Per diem rules apply: accommodation receipts required, meal allowance up to set daily limits.
- **Work clothing**: Deductible only if branded, protective, or required uniform. Regular business attire is not deductible.

### Step 4: Map to Israeli chart of accounts

Map each categorized expense to the appropriate account code in the standard Israeli chart of accounts:

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
   - Client coffee: 80% deductible, Account 66 (Marketing/Sales), 68 ILS deductible. Flag: document attendee name and business purpose
   - Cellcom phone: 80% deductible, Account 65 (Office/General), 144 ILS deductible
   - Fuel: 45% deductible, Account 64 (Vehicle), 202.50 ILS deductible
   - Keyboard: 100% deductible (under 1,200 ILS threshold), Account 65 (Office/General), 350 ILS
   - Accountant fee: 100% deductible, Account 67 (Professional Services), 800 ILS
   - WeWork: 100% deductible, Account 63 (Rent), 1,200 ILS
   - Udemy course: 100% deductible, Account 65 (Office/General), 120 ILS
3. Generate summary: Total expenses 3,335 ILS, Total deductible 3,169.50 ILS, Non-deductible 165.50 ILS
4. VAT note: Input VAT reclaimable on all items except the meal (partial)

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
   - Client dinner: 80% deductible, Account 66, 280 ILS deductible. Flag: document attendees
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
   - Gas station names (Paz, Sonol, Delek) -> Vehicle expenses, 45%
   - Bezeq/Cellcom/Partner/HOT -> Phone/Internet, 80%
   - Supermarket chains -> Flag as likely personal, 0%
   - Software vendors -> Office/General, 100%
4. Flag ambiguous items for manual review
5. Output categorized CSV with added columns: category, deduction_pct, deductible_amount, account_code, flags

Result: Enriched CSV file ready for accountant import, with flagged items requiring manual classification.

## Gotchas

- Israeli expense deduction rates are specific and non-negotiable: car expenses at 45% (or fixed amount), meals/entertainment at 80%, phone/internet at a proportional business-use rate. Agents may apply 100% deduction to all business expenses.
- Home office expenses in Israel are deductible based on the proportional area used for business, not a flat deduction. Agents may apply US-style simplified home office deduction rules.
- Israeli receipt numbers (mispar kabala) are legally required for expense documentation. A bank statement alone is not sufficient proof for tax deduction. Agents may accept bank records as complete documentation.
- Expense categories must match the Israeli Tax Ordinance (pkudat mas hachnasa) classifications. Agents may use generic US-style categories like "Office Supplies" that do not map directly to Israeli tax categories.
- Mixed personal/business expenses (like a phone used for both) require proportional allocation. Agents may categorize the entire expense as business without applying the required split.

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
