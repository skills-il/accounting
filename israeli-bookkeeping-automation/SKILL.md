---
name: israeli-bookkeeping-automation
description: Generate proper double-entry journal entries (pkudat yoman) for common Israeli business transactions including payroll with all statutory components, VAT handling, asset depreciation, and revenue recognition. Use when you need to create accurate bookkeeping entries following the Israeli chart of accounts (matkonet heshbonot) standard numbering system. Supports both Osek Murshe (authorized dealer) double-entry and Osek Patur (exempt dealer) single-entry bookkeeping. Handles salary payments with income tax, bituach leumi, health insurance, pension, keren hishtalmut, and convalescence pay. Do NOT use for tax filing submissions, annual financial statement audits, or replacing a certified public accountant (roeh heshbon).
license: MIT
allowed-tools: Bash(python:*)
compatibility: Works with all major AI coding agents
---


# Israeli Bookkeeping Automation

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

- **Osek Murshe (authorized dealer)**: Uses double-entry bookkeeping (hanhala kfula). Must charge and report VAT. Uses the full Israeli chart of accounts.
- **Osek Patur (exempt dealer)**: Uses single-entry bookkeeping (hanhala pshuta). Does not charge VAT. Revenue under the annual threshold (122,833 ILS for 2026).

### Step 3: Apply the Israeli Chart of Accounts (Matkonet Heshbonot)

Use the standard Israeli account numbering system:

| Range | Category | Examples |
|-------|----------|----------|
| 100-199 | Fixed Assets (rechush kavua) | 110 Computers, 120 Furniture, 130 Vehicles, 140 Leasehold improvements |
| 200-299 | Current Assets (rechush shotef) | 210 Bank (bank), 220 Cash (kupa), 230 Accounts receivable (hiyuvei lekuhot), 240 Input VAT (maam tsurot) |
| 300-399 | Equity & Liabilities (hon va-hatvot) | 310 Owner equity (hon ba'alim), 320 Retained earnings (ruvhim tsvurim), 330 Bank loans (halvaa bank), 340 Accounts payable (zka'ei sapkim) |
| 400-499 | Revenue (hachnasot) | 400 Service revenue (hachnasot misherutim), 410 Product revenue (hachnasot mimkarim), 420 Other income (hachnasot aherot) |
| 500-599 | Cost of Goods (olut hamkhar) | 500 Materials (homrei gelem), 510 Direct labor (avoda yeshira) |
| 600-699 | Operating Expenses (hotsa'ot tnuha) | 600 Salaries (hotsa'ot sachar), 601-604 Employer payroll costs (BL / pension / severance / KH ma'asik), 610 Rent (schar dira), 620 Insurance (bituah), 630 Depreciation (phat), 640 Office supplies (tsiyud misradi), 650 Professional services (sherutim miktso'iyim) |
| 700-799 | Payroll Liabilities (hatvot sachar) | 710 Income tax payable (mas hachnasa leshalem), 720 Bituach leumi payable (BL leshalem), 730 Health insurance payable (mas briut leshalem), 740 Pension payable (pension leshalem), 750 Keren hishtalmut payable (KH leshalem), 760 Severance fund payable (kupat pitsuyim) |
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

Source: National Insurance Institute salaried-employee rates (btl.gov.il/Insurance/Rates, 2026). For a working pensioner the health component is collected from the old-age pension, so nothing is deducted from the wage; the employer still pays the residual rate shown. The reduced/full split point (7,703) and the tiered rule apply to every category.

**Additional payroll components (not tiered):**
- Pension employee contribution (pension oved): 6% of pensionable salary
- Pension employer contribution (pension ma'asik): 6.5% of pensionable salary
- Severance provision (pitsuyim): 8.33% (1/12 of annual salary)
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

### Step 7: Handle Asset Depreciation (Phat)

Apply Israeli Tax Authority (rashut hamisim) depreciation rates:

| Asset Type | Annual Rate | Account |
|-----------|-------------|---------|
| Computers & software (mahshevim) | 33% | 110 |
| Office furniture (rihut misradi) | 6% | 120 |
| Vehicles (rehev) | 15% | 130 |
| Leasehold improvements (shiputsim) | 10% | 140 |
| Machinery, general (mekhonot) | 7% | 150 |

Machinery is the general 7% rate; the depreciation regulations set higher per-type rates for specific machinery (for example tractors and self-propelled equipment 20%), so check the regulation appendix (tosefet bet) when the asset is a specialized machine. Depreciation is calculated on a straight-line basis (shitat hakav hayashar). Monthly depreciation = (Cost - Accumulated depreciation) * Annual rate / 12.

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
  210  Bank (bank) - net payment                     11,008.00
  710  Income tax payable (mas hachnasa)              1,500.00
  720  BL payable (employee + employer)               1,493.00
  730  Health insurance payable (mas briut)              626.00
  740  Pension payable (employee + employer)           1,875.00
  750  KH payable (employee + employer)               1,500.00
  760  Severance fund payable (pitsuyim)              1,250.00
                                          Total:     19,252.00
```

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

**Monthly depreciation entry (33% annual rate):**

```
Date: 31/01/2026
Reference: DEP-2026-01
Description: Monthly depreciation - Server

Debit (hova):
  630  Depreciation expense (hotsa'ot phat)             660.00

Credit (zchut):
  111  Accumulated depreciation - computers (phat nitsberet)  660.00
                                          Total:       660.00
```

Calculation: 24,000 * 33% / 12 = 660 ILS per month.

Result: Asset recorded at cost (excluding VAT which is recoverable). Depreciation at the Israeli Tax Authority rate of 33% for computer equipment.

### Example 4: VAT Clearing Entry

User says: "Prepare the bi-monthly VAT clearing entry. Output VAT collected: 45,000 ILS. Input VAT paid: 32,000 ILS."

```
Date: 15/03/2026
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

When you record a B2B sales-invoice pkudat yoman in 2026, the source invoice must carry a SHAAM allocation number (mispar haktza'a) once it crosses the threshold in force on the invoice issue date:
- Jan 2025 - Dec 2025: net amount > NIS 20,000
- Jan 2026 - May 2026: net amount > NIS 10,000
- **Jun 1, 2026 onwards (in effect): net amount > NIS 5,000**

The June 2026 step-down took effect as scheduled, accelerated from the originally planned 2028 date. Use the invoice issue date, not the bookkeeping-entry date, when picking the threshold.

The allocation number itself does not change the journal-entry shape, but the source invoice must include it (typically captured as a custom field on the AR journal line). Without it on the buyer's side, the input-VAT entry is not deductible at year-end. Surface this to the user when posting any large B2B invoice entry.

## VAT input deduction by expense class

Not every input VAT line is fully recoverable. Common Israeli VAT rules to apply when posting input-VAT entries:

| Expense | Input VAT recoverable | Notes |
|---|---|---|
| Passenger-car purchase | 0% | Vehicle itself is fully blocked |
| Passenger-car operating costs (fuel, repairs, parking) | 2/3 | Standard "mostly-business" rule per gov.il / VAT Law reg. 14 |
| Passenger-car operating costs, mostly-private | 1/4 | Stricter rule when business use is incidental |
| Hospitality / business meals in Israel | 0% | Disallowed input VAT (אירוח בארץ) |
| Light refreshments at workplace (כיבוד קל) | 2/3 | Input VAT only. The income-tax expense deduction for כיבוד is a separate 80% cap, do not confuse the two |
| Standard goods + services for business | 100% | Full deduction with valid tax invoice |

Verify the per-expense rule before posting input-VAT in journal entries; over-deduction creates audit exposure.

## OPENFORMAT / PCN 874 / Form 6111

Israeli bookkeeping software must be able to export:
- **OPENFORMAT (קובץ אחיד / BKMV)**: ITA-mandated unified file (INI.TXT + BKMVDATA.TXT) for audits and CPA handoffs. Spec (v1.31): <https://www.gov.il/BlobFolder/service/registration-software-designed-managing-computerized-accounting-system/he/Service_Pages_Income_tax_horaot-131.pdf>. File checker: <https://secapp.taxes.gov.il/TmbakmmsmlNew/frmCheckFiles.aspx>.
- **PCN 874**: bi-monthly detailed VAT return file (different from OPENFORMAT but related), generated by Hashavshevet, Rivhit, iCount, etc.
- **Form 6111**: annual digital P&L / balance-sheet schedule for incorporated businesses, required as appendix to the corporate annual return.

When automating bookkeeping, plan the export pipeline against these formats. Agents should know the file shapes exist even when not generating them directly.

## Gotchas

- Israeli bookkeeping uses a specific chart of accounts convention that differs from US GAAP chart numbering. Account numbers in the 1xxx range typically represent assets in Israeli systems, not revenue. Agents may apply US-style account numbering.
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
| Israeli Tax Authority - depreciation | mas.gov.il | Approved depreciation rates by asset type |
| Kolzchut - Osek Patur | kolzchut.org.il/he/עוסק_פטור | Annual revenue threshold, VAT exemption rules |
| Pensuni - tax ceilings | pensuni.com | Pension ceilings, keren hishtalmut limits, tax brackets |

## Troubleshooting

### Error: "Journal entry does not balance"

Cause: The sum of debit amounts does not equal the sum of credit amounts. This commonly happens when VAT is forgotten on one side of the entry, or when employer payroll costs are debited without corresponding credits.

Solution: Verify each line item. For payroll, ensure every deduction from the employee has a matching credit to a liability account, and every employer cost is debited to an expense account with a credit to the corresponding payable. Use the formula: Total debits (salary expense + employer costs) = Net pay (bank) + all liability accounts.

### Error: "Incorrect VAT treatment for Osek Patur"

Cause: Attempting to record input or output VAT entries for an exempt dealer (Osek Patur). Exempt dealers do not charge or reclaim VAT.

Solution: For Osek Patur businesses, record revenue at the gross amount without separating VAT. Purchases should be recorded at the full amount including VAT (the VAT is a cost, not recoverable). Use single-entry bookkeeping: record income and expenses in a simple ledger (pinkas) without double-entry accounts.

### Error: "Depreciation rate mismatch"

Cause: Using a depreciation rate that does not match the Israeli Tax Authority approved rates. Common mistakes include using US GAAP rates or confusing monthly and annual rates.

Solution: Always reference the Israeli Tax Authority (rashut hamisim) depreciation schedule. Key rates: computers 33%, furniture 6%, vehicles 15%, machinery 7% (general rate, higher per-type rates exist), leasehold improvements 10%. Calculate monthly by dividing the annual rate by 12. The method is straight-line (shitat hakav hayashar) unless specifically approved otherwise.

### Error: "Missing employer bituach leumi contribution"

Cause: Recording only the employee's bituach leumi deduction without the separate employer contribution. The employer portion is an additional cost above gross salary.

Solution: Always record both portions. The employee BL (1.04%/7.00%) is deducted from gross salary and reduces net pay. The employer BL (4.51%/7.60%) is an additional expense above gross salary. Both are credited to the same BL payable account (720) for remittance to Bituach Leumi.
