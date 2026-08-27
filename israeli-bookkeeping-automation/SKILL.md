---
name: israeli-bookkeeping-automation
description: Generate proper double-entry journal entries (pkudat yoman) for common Israeli business transactions including payroll with all statutory components, VAT handling, asset depreciation, and revenue recognition. Use when you need to create accurate bookkeeping entries using an illustrative Israeli account-numbering convention that you map onto the business's own kartesset and its Form 6111 codes. Supports both Osek Murshe (authorized dealer) double-entry and Osek Patur (exempt dealer) single-entry bookkeeping. Handles salary payments with income tax, bituach leumi, health insurance, pension, keren hishtalmut, and convalescence pay. Do NOT use for tax filing submissions, annual financial statement audits, or replacing a certified public accountant (roeh heshbon).
license: MIT
allowed-tools: Bash(python:*)
compatibility: Works with all major AI coding agents
---


# Israeli Bookkeeping Automation

## Legal notice

This is a free information tool operated by an AI model. It explains the tax rules and helps you organise your own figures. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by a tax adviser or accountant. The output is not a tax opinion, not a return prepared by a licensed representative, and not professional advice, but a general calculation and explanation only: it does not examine the full extent of your income or your complete documents. An AI model may err, omit data, or present a wrong conclusion.

Any form or text this tool produces is an automatic draft for your personal preparation only, and is not a filed return. Responsibility for reporting and for paying the tax is yours, the binding computation is the Tax Authority's, and representation before the Tax Authority is reserved to those permitted by law. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person. Consult a tax adviser or accountant before filing or paying. All use of its output is the user's sole responsibility.


## Instructions

### Step 1: Identify the Transaction Type

Determine which type of bookkeeping entry is needed:

- **Payroll (mashkoret)**: Salary payments with all Israeli statutory deductions
- **VAT (maam)**: Input VAT, output VAT, or VAT clearing entries
- **Asset purchase (rechishat rechush kavua)**: Fixed asset acquisition and depreciation
- **Revenue (hachnasot)**: Revenue recognition for services or goods
- **Loan (halvaa)**: Loan receipt, repayment, and interest entries
- **Expenses (hotsa'ot)**: General business expense entries

### Step 2: Determine the Business Type

Check whether the business is:

- **Osek Murshe (authorized dealer)**: Uses double-entry bookkeeping (hanhala kfula). Must charge and report VAT. Uses a full double-entry account structure.
- **Osek Patur (exempt dealer)**: Uses single-entry bookkeeping (hanhala pshuta). Revenue under the annual threshold (122,833 ILS for 2026). Does not charge VAT on its ordinary supplies, **but "never charges VAT" is too strong**: an osek patur must charge and remit VAT on a sale of real estate, and on a sale of equipment where it deducted the VAT on acquiring that equipment. Note also that certain professions cannot register as osek patur at all regardless of turnover, and the list includes a bookkeeper (menahel cheshbonot), lawyer, accountant, tax adviser, engineer, architect and doctor among others, so check the profession before assuming the status is available.

### Step 3: Apply the Israeli Chart of Accounts (Matkonet Heshbonot)

There is no single national chart of accounts that businesses must number their ledgers by. Bookkeeping software (Hashavshevet, Rivhit, and others) lets each business define its own card codes. What the numbering does have to support is classification: the bookkeeping directives and the OPENFORMAT export expect the ledger to map cleanly onto the Form 6111 sections in the annual report, so pick codes that map, rather than codes that merely look tidy. The table below is therefore an illustrative convention used consistently throughout this skill. Map it onto the kartesset the business actually uses, and onto its Form 6111 codes, rather than renumbering a live ledger to match it:

| Range | Category | Examples |
|-------|----------|----------|
| 100-199 | Fixed Assets (rechush kavua) | 110 Computers, 120 Furniture, 130 Vehicles, 140 Leasehold improvements, 150 Machinery. Each asset account has a matching accumulated-depreciation contra account at +1 (111, 121, 131, 141, 151); always credit the contra, never the asset itself |
| 200-299 | Current Assets (rechush shotef) | 210 Bank (bank), 220 Cash (kupa), 230 Accounts receivable (hiyuvei lekuhot), 240 Input VAT (maam tsurot) |
| 300-399 | Equity & Liabilities (hon va-hatvot) | 310 Owner equity (hon ba'alim), 320 Retained earnings (ruvhim tsvurim), 330 Bank loans (halvaa bank), 340 Accounts payable (zka'ei sapkim) |
| 400-499 | Revenue (hachnasot) | 400 Service revenue (hachnasot misherutim), 410 Product revenue (hachnasot mimkarim), 420 Other income (hachnasot aherot) |
| 500-599 | Cost of Goods (olut hamkhar) | 500 Materials (homrei gelem), 510 Direct labor (avoda yeshira) |
| 600-699 | Operating Expenses (hotsa'ot tnuha) | 600 Salaries (hotsa'ot sachar), 601-604 Employer payroll costs (BL / pension / severance / KH ma'asik), 610 Rent (schar dira), 620 Insurance (bituah), 630 Depreciation (phat), 640 Office supplies (tsiyud misradi), 650 Professional services (sherutim miktso'iyim) |
| 700-799 | Payroll Liabilities (hatvot sachar) | 710 Income tax payable (mas hachnasa leshalem), 720 Bituach leumi payable (BL leshalem), 730 Health insurance payable (mas briut leshalem), 740 Pension payable (pension leshalem), 750 Keren hishtalmut payable (KH leshalem), 760 Severance fund payable (kupat pitsuyim), 770 Salary payable (mascoret leshalem), 715 Withholding tax at source payable (nikui bamakor leshalem) |
| 800-899 | Tax Accounts | 810 Output VAT (maam etsot), 820 VAT clearing (maam leshalem), 830 Corporate tax provision (hafrashat mas) |

### Step 4: Generate the Journal Entry

Create a properly formatted journal entry (pkudat yoman) with:

1. **Date (taarich)**: Transaction date
2. **Reference (asmachta)**: Invoice number, receipt number, or payroll period
3. **Description (teur)**: Clear description of the transaction
4. **Debit entries (hova)**: Accounts being debited with amounts
5. **Credit entries (zchut)**: Accounts being credited with amounts
6. **Verification**: Total debits must equal total credits

Always verify the entry balances (hova = zchut).

### Step 5: Handle Payroll Entries (Pkudat Sachar)

For salary journal entries, calculate all components using tiered rates. The split between the reduced and full rate is a fixed statutory bracket ceiling (7,703 ILS/month for 2026), set in the Bituach Leumi regulations and updated annually. It is the published bracket ceiling, not a figure you compute live from the average wage.

**2026 rates (threshold: 7,703 ILS/month, max insurable income: 51,910 ILS/month):**

| Component | Reduced (up to 7,703) | Full (7,703 to 51,910) |
|-----------|----------------------|------------------------|
| Bituach leumi employee (BL oved) | 1.04% | 7.00% |
| Health insurance employee (mas briut) | 3.23% | 5.17% |
| **Total employee deduction** | **4.27%** | **12.17%** |
| Bituach leumi employer (BL ma'asik) | 4.51% | 7.60% |

Rates are tiered: the reduced rate applies to the portion of salary up to the threshold, and the full rate applies to the portion above. Do NOT apply a flat rate to the entire salary.

**Rates by employee category (2026).** The table above is the standard resident employee aged 18 to retirement who is not a pensioner. Bituach leumi and health rates differ by category. A posting must use the row that matches the employee, never apply the standard row to everyone (a wrong row silently over-deducts and posts a wrong net pay and 720 liability):

| Employee category | Employee (reduced, up to 7,703) | Employee (full, 7,703 to 51,910) | Employer (reduced / full) |
|---|---|---|---|
| Standard resident, 18 to retirement | 4.27% (BL 1.04% + health 3.23%) | 12.17% (BL 7.00% + health 5.17%) | 4.51% / 7.60% |
| Minor under 18 | 0% (employer-borne) | 0% (employer-borne) | 0.61% / 2.12% |
| Working pensioner receiving old-age pension | 0% (collected from the pension, not the wage) | 0% | 0.61% / 2.12% |
| Aged 67 to 70, not yet receiving old-age pension | 3.93% | 10.03% | 4.13% / 6.96% |
| Disability-pension recipient (with annual NII certificate) | 3.23% (health only, BL waived) | 5.17% (health only) | 0.61% / 2.12% |
| **Controlling shareholder in a close company (baal shlita)** | **4.25%** | **11.96%** | **4.46% / 7.38%** |
| Woman between her retirement age and the male retirement age, not receiving old-age pension | 3.95% | 10.24% | 4.17% / 7.12% |

The controlling-shareholder row matters more than its position suggests: an owner-manager drawing a salary from their own company is one of the most common payroll cases in exactly the audience this skill serves, and routing them through the standard row over-deducts. The woman-between-retirement-ages row exists because retirement age differs by sex; sending that population through the "aged 67 to 70" row, which is the male path, is the other easy mistake. The official table also carries rows for new residents first resident after age 62, and for soldiers in regular service, organ donors and treaty-country foreign residents. **Look up the row; do not default.**

No BL or health is charged on the portion of salary above the maximum insurable income of 51,910 NIS/month, so a 60,000 NIS salary is tiered as 7,703 reduced, 44,207 full, and 8,090 exempt, not 7,703 reduced and 52,297 full.

Source: National Insurance Institute salaried-employee rates (btl.gov.il/Insurance/Rates, 2026). For a working pensioner the health component is collected from the old-age pension, so nothing is deducted from the wage; the employer still pays the residual rate shown. The reduced/full split point (7,703) and the tiered rule apply to every category.

**Additional payroll components (not tiered):**
- Pension employee contribution (pension oved): 6% of pensionable salary
- Pension employer contribution (pension ma'asik): 6.5% of pensionable salary
- Severance provision (pitsuyim): up to 8.33% (1/12 of annual salary). 8.33% is the full-liability rate and is common, but it is not automatic: the employer's actual severance rate is set by the applicable extension order, collective agreement or employment contract, and is often lower. Confirm the rate rather than assuming 8.33%. Whether it accumulates as a liability depends on the arrangement: under a section 14 arrangement (hesder lefi seif 14) the deposits come in place of the severance payment, so 760 should not accumulate a growing balance. Two caveats that decide real cases: the relief only reaches the portion actually deposited, so an employer depositing at less than the full-liability rate still carries the gap (hashlamat pitsuyim) as a liability; and section 14 depends on the signed arrangement meeting the general-permit conditions, not merely on money being deposited. Ask which arrangement applies, and at what rate, before posting.
- Minimum wage (sachar minimum): 6,443.85 ILS/month for a full-time post and 35.40 ILS/hour, from 1 April 2026. A gross salary below this in a payroll entry is a red flag: stop and confirm the employee is genuinely part-time or on an hourly count rather than posting it.
- Keren hishtalmut employee (KH oved): 2.5% of salary (optional, common)
- Keren hishtalmut employer (KH ma'asik): 7.5% of salary, deductible up to the 15,712 ILS/month salary ceiling; employer KH on salary above that ceiling becomes a taxable benefit to the employee
- Convalescence pay (dmei havraa): annual entitlement = daily rate (set by extension order, supply the current rate as an input) times entitled days by seniority. Post as a salary-expense line; this skill does not hard-code the daily rate.

**Income tax (mas hachnasa) is an input, not computed here.** This skill does NOT calculate PAYE withholding. The withheld income tax depends on the employee's annual tax brackets and credit points (nekudot zikui), which the payroll system or the user must supply. The income-tax figure shown in the examples below is an illustrative placeholder, not a computed value. Post the supplied tax amount to the income-tax-payable account (710) and let it reduce net pay; never invent a tax figure.

### Step 6: Handle VAT Entries

For Osek Murshe businesses:

- **Sales invoice**: Debit Accounts Receivable (230), Credit Revenue (400) + Credit Output VAT (810)
- **Purchase invoice**: Debit Expense + Debit Input VAT (240), Credit Accounts Payable (340)
- **VAT clearing (monthly/bi-monthly)**: Debit Output VAT (810), Credit Input VAT (240), Credit/Debit VAT Payable (820)

Current VAT rate: 18% (since January 2025).

**VAT timing (do not default to invoice date).** The rule above posts output VAT when the invoice is issued, which is correct for a sale of goods and for any business reporting on the accrual basis. Many service providers, however, report VAT on the CASH basis (basis mezuman): the VAT liability arises when payment is received, not when the invoice is issued, and what they issue up front is a heshbonit iska (proforma / demand for payment), with the heshbonit mas raised on receipt. Posting output VAT at invoice date for a cash-basis service provider over-reports VAT in that period. Establish which basis the business is on before generating any sales entry, and treat it as an input you must ask for rather than assume.

### Step 7: Handle Asset Depreciation (Phat)

Apply Israeli Tax Authority (rashut hamisim) depreciation rates:

| Asset Type | Annual Rate | Account |
|-----------|-------------|---------|
| Personal computers (mahshevim ishiyim) | 33% | 110 |
| Other computers, including servers | 25% | 110 |
| Electronic and computerised equipment (not computers) | 15% | 110 |
| Office furniture (rihut misradi) | 6% | 120 |
| Vehicles (rehev), M1/N1/L/O default class | 15% | 130 |
| Vehicles, other classes (taxi, driving-school, bus, rental, truck) | 16-25%, class-dependent | 130 |
| Leasehold improvements (shiputsim) | See note below, NOT in the regulation | 140 |
| Machinery, general (mekhonot) | 7% | 150 |

**Note on leasehold improvements.** The 10% rate this skill previously stated is **not in the depreciation regulations**: Tosefta Bet has no leasehold-improvements line at all. Standard practice is to write them off over the shorter of the lease term (including option periods the tenant is likely to exercise) or the improvement's useful life, so the rate depends on the specific lease and there is no single number to quote. Ask for the lease term rather than applying a flat rate, and do not present a leasehold rate as an ITA-published figure.

**Note on furniture and vehicles.** Furniture is 6% general, but 9% in hotels and guesthouses and 12% in cafes, restaurants and public entertainment venues. Vehicles are 15% only in the default M1/N1/L/O class; taxis and driving-school vehicles, buses and tour vehicles, rental-registered vehicles, and heavier N2/N3 classes each carry their own higher rate. Look up the class rather than defaulting to the headline row.

Machinery is the general 7% rate; the depreciation regulations set higher per-type rates for specific machinery (for example tractors and self-propelled equipment 20%), so check the regulation appendix (tosefet bet) when the asset is a specialized machine. Depreciation is calculated on a straight-line basis (shitat hakav hayashar), so the base is always original cost, never the written-down balance. Monthly depreciation = Cost * Annual rate / 12, run from the date the asset was placed in service and stopped once accumulated depreciation reaches cost. For the first period, follow the convention the business's accountant already uses (a full month in the month of entry into service, or a pro-rata share of it) and state which convention the entry assumes. Do not subtract accumulated depreciation from the base: that is the reducing-balance method and it is not what these rates are.

## Examples

### Example 1: Monthly Payroll Entry

User says: "Create a journal entry for January 2026 salary payment for an employee earning 15,000 ILS gross"

**Calculation breakdown (2026 rates, threshold 7,703 ILS):**

Employee gross salary: 15,000 ILS

Employee deductions:
- Income tax (mas hachnasa): 1,500 ILS (illustrative placeholder only, not computed by this skill; supply the real withheld amount from the employee's brackets and credit points)
- Bituach leumi employee: 7,703 x 1.04% + 7,297 x 7.00% = 80 + 511 = 591 ILS
- Health insurance (mas briut): 7,703 x 3.23% + 7,297 x 5.17% = 249 + 377 = 626 ILS
- Pension employee: 900 ILS (6%)
- Keren hishtalmut employee: 375 ILS (2.5%)
- Total deductions: 3,992 ILS
- Net salary (sachar neto): 11,008 ILS

Employer costs:
- Bituach leumi employer: 7,703 x 4.51% + 7,297 x 7.60% = 347 + 555 = 902 ILS
- Pension employer: 975 ILS (6.5%)
- Severance provision: 1,250 ILS (8.33%)
- Keren hishtalmut employer: 1,125 ILS (7.5%)
- Total employer cost on top of gross: 4,252 ILS

**Journal entry (pkudat yoman):**

```
Date: 31/01/2026
Reference: PAYROLL-2026-01
Description: January 2026 salary - Employee Name

Debit (hova):
  600  Salary expense (hotsa'ot sachar)              15,000.00
  601  BL employer expense (BL ma'asik)                 902.00
  602  Pension employer expense (pension ma'asik)        975.00
  603  Severance expense (pitsuyim)                   1,250.00
  604  KH employer expense (KH ma'asik)               1,125.00
                                          Total:     19,252.00

Credit (zchut):
  770  Salary payable (mascoret leshalem)            11,008.00
  710  Income tax payable (mas hachnasa)              1,500.00
  720  BL payable (employee + employer)               1,493.00
  730  Health insurance payable (mas briut)              626.00
  740  Pension payable (employee + employer)           1,875.00
  750  KH payable (employee + employer)               1,500.00
  760  Severance fund payable (pitsuyim)              1,250.00
                                          Total:     19,252.00
```

Assumptions this entry states explicitly: the employer has NO section 14 arrangement and provides severance at the full 8.33%, so 760 accumulates. (8.33% x 15,000 is 1,249.50; it is shown rounded to 1,250 on both sides, so the entry still balances.)

Salary is accrued on 31/01 but paid in February, so the net goes to salary payable, not to Bank. The payment itself is a second, separate entry on the actual value date:

```
Date: 09/02/2026
Description: Payment of January 2026 net salary

Debit (hova):
  770  Salary payable (mascoret leshalem)            11,008.00
Credit (zchut):
  210  Bank (bank)                                   11,008.00
```

The statutory liabilities (710 to 760) are likewise cleared on their own remittance dates, not on the accrual date. Crediting Bank on the accrual date is the most common payroll-posting error: it understates the bank balance for a whole month and makes the bank reconciliation impossible to tie.

Result: Balanced double-entry journal entry with all Israeli payroll components properly allocated. BL and health are calculated using tiered rates (reduced up to 7,703 ILS, full above). The entry separates employee deductions from employer costs and creates proper liabilities for statutory payments.

### Example 2: Sales Invoice with VAT

User says: "Record a sales invoice for consulting services, 10,000 ILS plus VAT"

**Calculation:**
- Service amount (before VAT): 10,000 ILS
- VAT at 18% (maam): 1,800 ILS
- Total invoice amount: 11,800 ILS

**Journal entry:**

```
Date: 15/01/2026
Reference: INV-2026-0042
Allocation no. (mispar haktsa'a): 4471-8823-0091
Description: Consulting services invoice - Client Name

Debit (hova):
  230  Accounts receivable (hiyuvei lekuhot)         11,800.00

Credit (zchut):
  400  Service revenue (hachnasot misherutim)         10,000.00
  810  Output VAT (maam etsot)                         1,800.00
                                          Total:     11,800.00
```

Result: Revenue recognized net of VAT with output VAT liability recorded separately for the monthly/bi-monthly VAT report (doch maam).

### Example 3: Asset Purchase and Monthly Depreciation

User says: "We bought a computer server for 24,000 ILS plus VAT. Show the purchase entry and the first month's depreciation."

**Purchase entry:**

```
Date: 05/01/2026
Reference: PO-2026-008
Description: Server purchase - Vendor Name

Debit (hova):
  110  Computers (mahshevim)                         24,000.00
  240  Input VAT (maam tsurot)                        4,320.00

Credit (zchut):
  340  Accounts payable (zka'ei sapkim)              28,320.00
                                          Total:     28,320.00
```

**Monthly depreciation entry (25% annual rate, see below):**

```
Date: 31/01/2026
Reference: DEP-2026-01
Description: Monthly depreciation - Server

Debit (hova):
  630  Depreciation expense (hotsa'ot phat)             500.00

Credit (zchut):
  111  Accumulated depreciation - computers (phat nitsberet)  500.00
                                          Total:       500.00
```

Calculation: 24,000 * 25% / 12 = 500 ILS per month. **The rate matters here and it is easy to get wrong.** The depreciation regulations split computers in two: personal computers depreciate at 33%, and *other* computers, which is where a server sits, at 25%. Using the personal-computer rate on a server overstates the monthly charge by a third, every month, for the life of the asset. Convention stated: a full month is taken in the month the asset was placed in service. If the business's accountant pro-rates instead, the January charge would be 500 * 27/31 = 435.48 and the schedule shifts accordingly. State whichever convention the entry uses.

Result: Asset recorded at cost excluding RECOVERABLE VAT. Where the input VAT is blocked (a passenger car, for example, see the input-VAT table), the blocked VAT is part of the asset cost: capitalize it and depreciate it, do not expense it. Depreciation at 25%, the rate for computers other than personal computers.

### Example 4: VAT Clearing Entry

User says: "Prepare the bi-monthly VAT clearing entry. Output VAT collected: 45,000 ILS. Input VAT paid: 32,000 ILS."

```
Date: 28/02/2026
Reference: VAT-2026-0102
Description: VAT clearing for January-February 2026

Debit (hova):
  810  Output VAT (maam etsot)                       45,000.00

Credit (zchut):
  240  Input VAT (maam tsurot)                       32,000.00
  820  VAT payable (maam leshalem)                   13,000.00
                                          Total:     45,000.00
```

Result: Output VAT liability cleared against input VAT credit. Net VAT payable of 13,000 ILS to be remitted to the tax authority (rashut hamisim).

## SHAAM allocation number on B2B sales-invoice journal entries

When you record a B2B sales-invoice pkudat yoman, the source invoice must carry a SHAAM allocation number (mispar haktza'a, 9 digits) once it crosses the threshold in force on the invoice issue date. **You need the WHOLE table, because bookkeeping routinely touches earlier years through migrations, catch-up posting and audit periods.** Thresholds are VAT-exclusive:

| Invoice issue date | Allocation number required above |
|---|---|
| Before May 2024 | Never. The regime did not exist |
| May 2024 - Dec 2024 | NIS 25,000 |
| Jan 2025 - Dec 2025 | NIS 20,000 |
| Jan 2026 - May 2026 | NIS 10,000 |
| **Jun 1, 2026 onwards (in effect)** | **NIS 5,000** |

The June 2026 step-down took effect as scheduled, accelerated from the originally planned 2028 date. Use the invoice issue date, not the bookkeeping-entry date, when picking the threshold, and never apply today's NIS 5,000 threshold to a 2025 invoice that only needed a number above NIS 20,000, or to a 2024 invoice whose threshold was NIS 25,000.

**Two separate rules are in play here, and conflating them is the classic error.**

**The SELLER'S duty to obtain a number** is s.47(א2)(1). It arises only at the buyer's demand and does not reach a zero-rated transaction: `ובעסקה שסכומה, בלא המס, עולה על הסכום האמור בסעיף 38(א1), חייב הוא לעשות כן לפי דרישת הקונה; הוראות סעיף קטן זה יחולו לעניין חשבונית מס שהוצאה בשל עסקה שהמס שחל לגביה אינו בשיעור אפס`.

**The BUYER'S loss of the deduction** is s.38(א1), and it has NO buyer-request condition: `לא יותר ניכוי מס התשומות הכלול בחשבונית מס שסכומה, בלא המס, עולה על 5,000 שקלים חדשים (מינואר 2026 ועד מאי 2026: 10,000 שקלים חדשים) ושאינה כוללת מספר שהקצה לה המנהל`. Note the subsection carries the January-to-May 2026 figure itself, so the schedule is confirmable from the statute rather than only from vendor summaries, and that it says `עולה על` (EXCEEDS), so an invoice sitting exactly on a band figure is outside the rule.

**The posting test is therefore THREE conditions, not four:**
1. the amount EXCEEDS the threshold in force on that invoice's date;
2. the invoice carries a VAT component. A zero-rated invoice, or one covering only exempt transactions, is outside the rule, so do not flag export or zero-rated invoices;
3. the recipient is an osek murshe. A sale to a private consumer, or to an osek patur, is out of scope, because there is no deduction to lose.

**"The buyer never asked" is NOT a fourth condition and must never gate the posting rule.** It decides whether the SELLER breached a duty; it has nothing to do with whether the BUYER can deduct. Treating it as a gate is how input VAT gets debited to 240 on an invoice whose deduction s.38(א1) has already disallowed, which over-claims the period.

Applying condition 1 alone is the opposite failure and is equally real: it strands deductible input VAT in a suspense account on B2C sales and on pre-regime invoices that never needed a number. Conditions 2 and 3 are the guards against that.

The allocation number itself does not change the journal-entry shape, but the source invoice must include it (typically captured as a custom field on the AR journal line). Carry it on both sides. On the buyer's side there is a hard posting rule, but check the three conditions first: if a purchase invoice **that meets all three** carries no number, do NOT debit input VAT to 240, whether or not anyone demanded one. Post that VAT to a separate non-deductible suspense account, flag it to the user, and move it to 240 only once the supplier reissues the invoice with a number. Silently debiting 240 produces a VAT report that is over-claimed in that period, not merely a problem discovered at year-end. Note the precise effect of a missing number: it blocks the RECIPIENT's input-VAT deduction. It does not, by itself, void the invoice. If a supplier's request for a number was refused, reverse charge (hipuch chiyuv) is one of the routes open to them, so a refusal is not a dead end.

## VAT input deduction and filing formats

Input VAT is not always fully recoverable, and the Israeli filing formats (OPENFORMAT, PCN 874, Form 6111) have their own scoping rules. Both are reference data you consult while posting rather than steps in the workflow, so they live in `references/vat-input-and-filing-formats.md`. Consult it before posting any input VAT on a vehicle, hospitality or refreshments line, and before telling a client whether a filing obligation applies to them.

## Gotchas

- There is no single Israeli chart of accounts, so do not assume one. Different packages use different card codes and widths (3-digit, 4-digit, or alphanumeric), and the numbering in this skill is an illustrative convention. Always read the business's existing kartesset before posting, and never renumber it to match an example. Agents may apply US GAAP numbering, or treat an example chart as if it were statutory.
- Payroll journal entries in Israel must include separate lines for pension (6%+6.5%), keren hishtalmut (2.5%+7.5%), Bituach Leumi (employer+employee), and health tax. Agents may produce simplified entries missing mandatory statutory components.
- BL and health rates are tiered, not flat. The reduced rate applies only to the portion of salary up to the threshold (7,703 ILS for 2026), with the full rate on income above that. Agents may apply a flat rate to the entire salary, producing incorrect amounts.
- Israeli double-entry bookkeeping requires VAT input (maam tsurot) and VAT output (maam etsot) to be tracked in separate accounts for bi-monthly reporting. Agents may combine them into a single VAT account.
- The Israeli fiscal year can differ from the calendar year for companies. Agents may assume January-December when the company uses a different fiscal year-end.
- Withholding tax (nikui bamakhor) rules differ based on whether the payee has a tax exemption certificate (ptor nikui bamakhor). Agents may apply withholding universally without checking for exemptions.
- BL/health rates and thresholds change annually (tied to average wage). Always verify current year figures before generating entries. Using prior-year rates produces incorrect deduction amounts.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Bituach Leumi employer circular | btl.gov.il (Igeret LeMa'asik annual circular) | BL and health rates, thresholds, max insurable income |
| Kolzchut - BL for salaried workers | kolzchut.org.il/he/דמי_ביטוח_לאומי_לעובד_שכיר | Employee/employer rate breakdown, threshold amounts |
| Depreciation regulations (Tosefta Bet) | https://he.wikisource.org/wiki/תקנות_מס_הכנסה_(פחת) | The full rate schedule by asset class. Note: the domain `mas.gov.il` cited by an earlier edition of this skill does not exist (NXDOMAIN); the Tax Authority is on taxes.gov.il and gov.il |
| Kolzchut - Osek Patur | kolzchut.org.il/he/עוסק_פטור | Annual revenue threshold, VAT exemption rules |
| Pensuni - tax ceilings | pensuni.com | Pension ceilings, keren hishtalmut limits, tax brackets |

## Troubleshooting

### Error: "Journal entry does not balance"

Cause: The sum of debit amounts does not equal the sum of credit amounts. This commonly happens when VAT is forgotten on one side of the entry, or when employer payroll costs are debited without corresponding credits.

Solution: Verify each line item. For payroll, ensure every deduction from the employee has a matching credit to a liability account, and every employer cost is debited to an expense account with a credit to the corresponding payable. Use the formula: Total debits (salary expense + employer costs) = Net pay (bank) + all liability accounts.

### Error: "Incorrect VAT treatment for Osek Patur"

Cause: Attempting to record input or output VAT entries for an exempt dealer (Osek Patur). Exempt dealers do not charge or reclaim VAT.

Solution: For Osek Patur businesses, record ordinary revenue at the gross amount without separating VAT. Purchases are recorded at the full amount including VAT (the VAT is a cost, not recoverable). Two exceptions where an osek patur DOES have output VAT to post: a sale of real estate, and a sale of equipment on which it previously deducted input VAT. Use single-entry bookkeeping: record income and expenses in a simple ledger (pinkas) without double-entry accounts.

### Error: "Depreciation rate mismatch"

Cause: Using a depreciation rate that does not match the Israeli Tax Authority approved rates. Common mistakes include using US GAAP rates or confusing monthly and annual rates.

Solution: Always reference the depreciation regulations themselves (Tosefta Bet to Takanot Mas Hachnasa (Pchat)), not a remembered rate. Key rates: personal computers 33% but other computers including servers 25%, general electronic and computerised equipment 15%, furniture 6% general (9% hotels, 12% cafes and restaurants), passenger vehicles 15% in the default M1/N1 class only, machinery 7% (general rate, higher per-type rates exist), leasehold improvements 10%. Calculate monthly by dividing the annual rate by 12. The method is straight-line (shitat hakav hayashar) unless specifically approved otherwise.

### Error: "Missing employer bituach leumi contribution"

Cause: Recording only the employee's bituach leumi deduction without the separate employer contribution. The employer portion is an additional cost above gross salary.

Solution: Always record both portions. The employee BL (1.04%/7.00%) is deducted from gross salary and reduces net pay. The employer BL (4.51%/7.60%) is an additional expense above gross salary. Both are credited to the same BL payable account (720) for remittance to Bituach Leumi.
