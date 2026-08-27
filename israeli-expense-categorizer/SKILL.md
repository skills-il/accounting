---
name: israeli-expense-categorizer
description: AI-powered categorization of business expenses into Israeli tax-deductible categories based on current Israeli Tax Ordinance rules. Applies the correct deduction mechanics (vehicle = the higher of running-costs-minus-use-value or 45%, mobile phone with the ~50% disallowance floor, home office and internet proportional), maps to a common Israeli chart of accounts, and handles Osek Patur vs Osek Murshe differences for VAT eligibility (private-car VAT not deductible, running-cost VAT two-thirds). Use when you need to classify business expenses for Israeli tax reporting, prepare expense reports for your accountant, or verify deduction eligibility. Do NOT use for final tax filing, legal tax advice, or payroll-related expense processing.
license: MIT
allowed-tools: Bash(python:*) Read Edit Write
compatibility: Requires Claude Code or compatible agent with file access
---


# Israeli Expense Categorizer

## Legal notice

This is a free information tool operated by an AI model. It explains the tax rules and helps you organise your own figures. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by a tax adviser or accountant. The output is not a tax opinion, not a return prepared by a licensed representative, and not professional advice, but a general calculation and explanation only: it does not examine the full extent of your income or your complete documents. An AI model may err, omit data, or present a wrong conclusion.

Any form or text this tool produces is an automatic draft for your personal preparation only, and is not a filed return. Responsibility for reporting and for paying the tax is yours, the binding computation is the Tax Authority's, and representation before the Tax Authority is reserved to those permitted by law. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person. Consult a tax adviser or accountant before filing or paying. All use of its output is the user's sole responsibility.


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

- **Osek Patur** (exempt dealer): Annual turnover under the threshold (NIS 122,833 for 2026, up from NIS 120,000 in 2025). Cannot charge or deduct VAT. Income tax deductions still apply.
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
- Raw materials consumed in the period (see the inventory warning below)
- Business insurance premiums
- Marketing and advertising costs
- Professional development courses directly related to the business
- Office supplies and low-value equipment (immediate expense rather than depreciation; ~1,200 ILS is a common working threshold for flagging low-value items, confirm the current figure with your accountant)
- Website hosting and domain costs
- Employee salaries and related social costs

**Inventory is NOT a period expense.** Stock bought and still unsold at year end does not reduce this year's profit. It reaches the P&L only through cost of goods sold (opening stock + purchases - closing stock), and a stocktake (ספירת מלאי) at the year end is required under the bookkeeping directives. Treating a December stock buy-in as "100% deductible" overstates the year's expense by the entire closing-stock balance. Flag inventory purchases for the accountant rather than expensing them.

**Partially deductible expenses**:
- **Vehicle expenses**: Fuel, licensing, compulsory + comprehensive insurance, leasing, repairs, parking, tolls, and depreciation, per תקנות מס הכנסה (ניכוי הוצאות רכב) התשנ"ה-1995. **Pick the right branch before picking a rate, because the regulation has three of them:**
  - **תקנה 2, expenses in producing income that is NOT employment income** (the self-employed case): the deductible amount is the HIGHER of [running expenses minus שווי שימוש] OR a percentage of running expenses. **That percentage is not always 45%.** תקנה 2 sets five: 45% for an ordinary vehicle; **25% for an L3 motorcycle** (תקנה 2(1א)); 90% for an M1 whose sub-classification is a public bus or taxi (2(1ב)); 80% for an M1 tour or desert vehicle (2(1ג)); and 77.5%, or 68% where the taxpayer has two such cars and only one is automatic, for a driving-instruction vehicle (2(1ד)). A courier on an L3 motorcycle who applies 45% over-claims by 20 points of the whole running-cost bundle; a taxi driver who applies 45% instead of 90% loses half the deduction. Check the vehicle's classification on the רישיון רכב first.
  - **תקנה 3, a vehicle the EMPLOYER put at an employee's disposal (רכב צמוד)**: running costs are deductible **IN FULL** ("יותרו בניכוי במלואן"). The employer does not apply the 45% higher-of rule at all; the employee is instead grossed up with שווי שימוש. Routing a small company with a company car to 45% under-claims roughly half the fleet cost.
  - **תקנה 4, the employee's own side**: no deduction at all for vehicle running costs incurred in producing employment income.
  - **שווי שימוש** is NOT computed from receipts: it is a fixed amount the Tax Authority sets per vehicle from the price-group (קבוצת מחיר) table, or for vehicles from 2010 onward as a percentage of the list price (currently 2.48%); look it up via the ITA calculator so the higher-of branch is actually computable.
  - A **רכב תפעולי** (operational vehicle) falls OUTSIDE the regulation's definition of "רכב" entirely: a security vehicle used only operationally, or a vehicle put at no employee's disposal, used only for the business, where the place of business is not the owner's home and the vehicle does not leave the premises after hours. That, not any invented "second vehicle" rule, is the real carve-out. **There is no rule disallowing a second vehicle**: the regulation applies per vehicle, and each one stands or falls on the ordinary Sec. 17 wholly-and-exclusively test.
  - Hard condition: the regulations' reporting rule requires the odometer (ק"מ) reading at the start and end of the tax year to be recorded per vehicle in the Sec. 131 return, or the deduction can be disqualified. (תקנה 5, the in-vehicle measuring device, never entered force: the regulations commenced in 1995 except for that one, whose start date was left to the Finance Minister. Do not tell a user their deduction fails for want of a device.)
- **Mobile phone (טלפון נייד)**: Not a flat 80%. Per תקנות מס הכנסה (ניכוי הוצאות מסוימות) תשל"ב-1972, only the portion ABOVE the lower of about 1,380 NIS per year (~115 NIS/month) or 50% of the expense is deductible, which acts as an effective ~50% disallowance floor. This shekel figure is index-adjusted annually under תקנה 2ג, so confirm the current year's table.
- **Landline from home (טלפון קווי מהבית)**: The default under תקנה 2ב(א) is that home landline costs are NOT DEDUCTIBLE AT ALL. They become deductible only if the taxpayer proves to the assessing officer that the home is the MAIN place of his business or vocation (עיקר עסקו). Do not let a home landline claim 80% without that. Once proven, two branches apply: if annual costs are at or below the indexed ceiling (about 26,600 NIS), deduct the LOWER of 80% of the cost or the part exceeding about 2,700 NIS; if costs exceed that ceiling, deduct only the part exceeding about 5,300 NIS. If the home served as the main place of business for only part of the year, תקנה 2ב(א1) pro-rates both the costs and the thresholds by the number of qualifying months over 12. The shekel figures here are the index-adjusted amounts (the regulation's own nominal texts are 1,800 / 3,600 / 18,000); they are re-adjusted annually under תקנה 2ג, so confirm the current tax year's table.
- **Internet**: No fixed percentage. Split by actual business-use proportion (for a home connection, use the same business-use share as the home office).
- **Home office (proportional)**: Deduct the percentage of home used exclusively for business. Calculate: (office area / total home area) x 100. Apply this percentage to rent, arnona, electricity, internet, and maintenance.
- **Meals and entertainment** (correct rule, often misapplied):
  - **Hospitality / business meals with Israeli clients (אירוח בארץ): 0% deductible.** Per תקנות ניכוי הוצאות מסויימות 1972 reg. 2(1), hosting Israeli clients/partners is disallowed regardless of receipts. Coffee with a client at Aroma is **not** an 80% expense.
  - **Hospitality with foreign guests visiting Israel (אירוח אורחי חוץ)**: deductible up to a "reasonable" amount with proper documentation of the foreign guest.
  - **Light refreshments at the workplace (כיבוד קל)**: up to 80% deductible per ITA practice (coffee/tea/snacks for staff and visitors at the office).
  - **Foreign-business-trip subsistence (אש"ל לחו"ל)**: meals abroad are not deductible at a separate percentage, they fall inside the daily "other stay expenses" cap. Caps for 2026: up to $102 per day of stay when lodging expenses are also claimed, or up to $171 per day of stay when lodging expenses are not claimed.
  - Meals during a regular workday for the self-employed person alone: not deductible.
- **Gifts to clients**: Up to about 240 NIS per recipient per year for gifts given in Israel, and up to $15 USD per foreign recipient per year, per תקנות ניכוי הוצאות מסויימות 1972. These are index-adjusted amounts re-set annually under תקנה 2ג, so check the current year's coordination table rather than assuming last year's figure carried over.

**Commonly-missed deduction heads (Sec. 17 of the Ordinance)**: the general rule in Sec. 17 is that expenses laid out wholly and exclusively in producing income are deducted unless limited elsewhere, and it names heads this skill's category lists otherwise skip:
- **Interest and linkage differences** on money borrowed, where the assessing officer is satisfied it funded the income-producing activity (Sec. 17(1)). This is what account 69 is for; a bank interest charge is a deduction, not an unclassifiable item.
- **Repairs** to premises, plant and machinery (Sec. 17(3)), as distinct from an improvement, which is capital.
- **Bad and doubtful debts** (Sec. 17(4)), on proof to the assessing officer that they went bad in the tax year; a later recovery is taxed when received. There is a separate VAT limb: a written-off debt can support a credit note and an input-VAT refund claim, which has its own procedure and time limit, so raise it with the accountant rather than only writing the debt off for income tax.
- **The cost of preparing the return and handling assessments and appeals** (Sec. 17(11)), expressly denied where books were not kept.

**Non-deductible expenses (0%)**:
- Personal clothing (unless uniforms or protective gear)
- Commuting costs (home to regular workplace)
- Fines and penalties (traffic tickets, late payment penalties to tax authority)
- Personal entertainment
- Life insurance premiums (unless keyman insurance for business)
- Political donations

**Self-employed retirement and insurance deductions (PERSONAL annual-return deductions, often missed)**:
These are the self-employed filer's OWN deductions, claimed on the annual return and its schedules, NOT business-expense (P&L) lines. Do NOT book them to the chart of accounts below, account 68 "pension" there is for EMPLOYEES' pension (an employer cost); booking your own pension or keren hishtalmut as a business expense misstates profit and risks double-counting when the accountant also claims the personal deduction. They are also distinct from the ordinary life insurance listed as non-deductible above:
- Contributions to a self-employed keren hishtalmut (קרן השתלמות לעצמאי) are deductible up to 4.5% of determining income (hachnasa kovaat) per Sec. 17(5a) of the Ordinance, where determining income is business or vocation taxable income before this deduction, capped at the amount stated in the section, NIS 156,000, which is the Ordinance's NOMINAL figure and is index-linked under Sec. 120B, so the live ceiling for the current tax year is materially higher. Look up the current indexed figure rather than using 156,000 directly.
- Of the self-employed person's OWN National Insurance, exactly 52% of the ביטוח לאומי (National Insurance) component is income-tax deductible (Sec. 47A(a)), excluding the addition under Sec. 179(a) of the National Insurance Law, and the deduction cannot exceed taxable income before it; the health-tax component (דמי ביטוח בריאות) is NOT deductible at all. A self-employed Bituach Leumi bill bundles both, so apply the 52% to the NI portion only, the annual Bituach Leumi certificate (ishur) pre-computes the deductible base. This is the filer's own contribution, not employee withholding, so do NOT treat it as out-of-scope payroll.
- Loss-of-work-capacity insurance (ביטוח אובדן כושר עבודה) is deductible up to an income-based cap.
- Self-employed pension contributions (kupat gemel / keren pensia) earn a deduction (Sec. 47) and a separate tax credit (Sec. 45A) up to caps.
Confirm the exact caps with the accountant, they interact and are all capped against income.

**Special rules**:
- **Higher-value equipment**: Recognized through depreciation over its useful life rather than immediately (computers: 33% per year, office furniture: 6% per year). Low-value items are taken as an immediate expense; ~1,200 ILS is a common working threshold for flagging which items to treat as low-value, confirm the current figure with your accountant.
- **Depreciation of vehicles**: 15% per year applied to the vehicle cost; the deductible portion of that depreciation is itself folded into the 45% higher-of running-cost rule above.
- **Travel abroad**: Fully deductible if business purpose is documented. Per diem rules apply: accommodation receipts required, subsistence up to the daily caps noted above ($102/$171 per day of stay).
- **Work clothing (ביגוד)**: Per תקנה 2(6), qualifying work clothing is **80%** deductible, and 100% ONLY where the clothing cannot be used other than for work. It qualifies as ביגוד only if it prominently identifies the taxpayer's business, or the law requires it to be worn. So a branded polo shirt is 80%, not 100%. Regular business attire is not deductible at all.

**Book amounts gross or net? Decide this before any figure is produced.**
- An **osek murshe** books expenses NET of recoverable input VAT: the VAT is a receivable from the Tax Authority, not an expense. Do not take the gross invoice amount as the deductible base and then also report the VAT as reclaimable, that counts it twice.
- An **osek patur** recovers no input VAT at all, so he books the VAT-INCLUSIVE amount as the expense, and depreciates equipment on the VAT-inclusive cost.
- Where input VAT is only PARTLY recoverable (vehicle running costs at 2/3, or a mixed-use asset), the non-recoverable remainder is itself an expense.
State which basis you used in the output, because every figure changes by roughly the VAT rate depending on the answer.

**VAT (Osek Murshe only)**:
- **Private vehicle (רכב פרטי) purchase**: Input VAT on the purchase or import of a private vehicle is NOT deductible (תקנה 14(א)). This is not absolute: תקנה 14 carries exceptions for businesses whose vehicles are their trade, and the ITA's own guide has a section on the exceptions (חריגים לאיסור ניכוי מס תשומות). If the client is a car dealer, a driving school, a rental fleet or a taxi/transport operator, do NOT apply the block without checking the exception, or they forgo the input VAT on every vehicle they buy.
- **Vehicle running costs (fuel, repairs)**: Input VAT is 2/3 deductible when business is the primary use of the vehicle, and 1/4 deductible otherwise (תקנה 18).
- **Allocation number (מספר הקצאה) on a supplier's tax invoice, the newest way to lose an input-VAT deduction.** Under the "Israel Invoices" regime a tax invoice above the threshold in force ON THE INVOICE DATE must carry a 9-digit allocation number, or the RECIPIENT cannot deduct the input VAT on it. The thresholds (before VAT) are NIS 25,000 from May 2024, NIS 20,000 from January 2025, NIS 10,000 from January 2026, and NIS 5,000 from June 2026, so at the current threshold this now reaches ordinary business expenses: equipment, subcontractors, a quarter's rent. When categorizing an above-threshold expense for an osek murshe, check the supplier invoice actually carries the number and flag it if not. Do not over-apply it either: an allocation number is required only where the invoice carries a VAT component (a zero-rated or exempt-only invoice does not need one), the recipient is an osek murshe, and the recipient asked for one. Scope historical expenses to the threshold in force on their own date rather than today's.
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
   - iMac: 100% deductible but must depreciate over 3 years (33%/year), Account 70, ~2,805 ILS/year depreciation (8,500 x 33%)
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
   - Bezeq landline / HOT / internet -> Landline-or-internet; a HOME landline is disallowed entirely unless the home is proven to be the main place of business, and only then is it the lower of 80% or the amount over about 2,700 ILS. Internet is split by business-use proportion
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
