---
name: israeli-payroll-calculator
description: Calculate Israeli payroll including income tax, Bituach Leumi (National Insurance), health tax, pension contributions, shovi rechev (company-car use value), and net salary. Use when user asks to calculate salary, "tlush maskoret", payroll deductions, "bruto to neto", employer cost, tax credits (nekudot zikui), company car impact on salary, or needs help understanding Israeli payslip items. Covers employees, freelancers (atzmai), and employer cost calculations. This skill starts from an AGREED GROSS. Do NOT use it to work out what gross is owed from a timesheet, or to check overtime, weekly-rest premium or a missing hours record (use israeli-attendance-wage-checker), and do NOT use it for US, UK, or other countries' payroll calculations.
license: MIT
allowed-tools: Bash(python:*)
compatibility: Works with Claude Code, Claude.ai, Cursor. No network access required.
---

# Israeli Payroll Calculator

## Legal notice

This skill is a free information tool operated by an AI model. It estimates payroll deductions from the figures the user supplies and the published 2026 rates; no certified accountant (רואה חשבון), tax advisor (יועץ מס) or payroll professional reviews its output. The output is not tax advice, not a professional opinion and not a payslip, but an estimate: it does not see the employee's full tax file, form 101, tax coordination, other income or employer-specific agreements. An AI model may err, omit data or reach a wrong conclusion. "האחריות לדיווח ולתשלום המס היא שלכם, החישוב המחייב הוא של רשות המסים, וייצוג מול רשות המסים שמור למי שרשאי לכך לפי דין." It "אינו מהווה תחליף לייעוץ המתחשב בנתונים ובצרכים המיוחדים של כל אדם", and relying on it is the user's sole responsibility.

## Instructions

**Scope check before anything else.** This skill converts an AGREED GROSS into net. If the user does not yet know the gross, because the question is really about hours worked, overtime tiers, Shabbat premium, paid versus unpaid breaks, or an employer who kept no attendance record, that is a different computation and it comes first: `israeli-attendance-wage-checker` produces the gross owed from a timesheet, and this skill takes it from there.


### Step 0: Sanity-check the gross against the minimum wage

Before computing anything, check the gross is legal. The monthly minimum wage is
6,247.67 NIS from 1.4.2025 and 6,443.85 NIS from 1.4.2026, with an hourly
minimum of 35.40 NIS from 1.4.2026. A full-time gross below the figure in force
for the month being computed is either a part-time position, an error in the
input, or an underpayment worth flagging to the user before the arithmetic
starts.

### Step 1: Gather Employee Information
Collect from user:
- **Gross monthly salary** (bruto, cash) in NIS
- **Tax credit points** (nekudot zikui): Default 2.25 for male resident, 2.75 for female; one more for an employee aged 16 or 17 (s.40B)
- **Shovi rechev** (company-car use value, if any): Monthly NIS value. See Step 1.5.
- **Other taxable allowances** (shovi telephone, meals above exemption, etc.). Dmei havraa is taxable pay too: 451.5 NIS/day for recuperation year 2026 under the extension order published on 18.8.2026, which covers private-sector employees but not those paid under public-service agreements or linked to them; where 418 was paid for 1.7.2025 to 30.6.2026, the difference is owed
- **Pension arrangement:** Yes/No, contribution percentages
- **Employment type:** Employee (sachir), Freelancer (atzmai)
- **Bituach Leumi insurance category:** Age, whether an old-age pension is already
  being drawn, whether the employee is a controlling shareholder (בעל שליטה) in
  their own close company, whether they first became an Israeli resident after
  age 62, and whether they are a soldier in regular service, an organ donor or a
  treaty-country foreign resident. This picks the rate row and is NOT optional
  for anyone who is not a plain 18-to-retirement resident employee. A low earner aged 67 to 70
  usually passes the income test and IS drawing the old-age pension, so ask. See Step 3.

### Step 1.5: Identify Taxable Imputed Income (shovi rechev, etc.)

Shovi rechev and other employer-provided benefits are **taxable imputed income**, not a perk. They increase the tax and NI base but are NOT received as cash. This is the single most common source of wrong payroll calculations.

Taxable base for income tax and bituach leumi:
```
taxable_gross = cash_gross + shovi_rechev + other_imputed_income
```

Pension base (does NOT include shovi rechev):
```
pension_base = cash_gross
```

Cash received (net):
```
net_cash = cash_gross - income_tax(taxable_gross)
                     - bituach_leumi(taxable_gross)
                     - health_tax(taxable_gross)
                     - pension_employee(cash_gross)
```

**Common error:** Treating shovi rechev as a benefit that increases net salary. In reality it is the opposite: because it adds to the tax base while not being received as cash, shovi rechev *decreases* net pay. The employee is effectively paying tax on the use of the car.

Reference: shovi rechev is defined in Income Tax Regulations (Shovi Rechev Hatamad). Value is published monthly by the Tax Authority based on the vehicle's list price and group.

### Step 2: Calculate Income Tax
Apply progressive tax brackets to the **taxable gross** (cash gross + shovi rechev + other imputed income):

1. Calculate annual equivalent: `taxable_gross * 12`
2. Apply brackets progressively (see references/tax-brackets.md). Amendment 288 (published 31.3.2026, retroactive to 1.1.2026) widened only the 20% and 31% brackets: 20% now runs to 19,000 NIS/month, 31% to 25,100, so 35% starts at 25,101. Every other threshold, and the 242 credit point, is the same as in 2025.
3. Subtract tax credit points value: `credit_points * 242 NIS/month`
4. Subtract pension tax credit (zikui gemel), see Step 2.5.
5. Monthly tax = `max(0, bracketed_tax - credit_points_value - pension_credit)`

IMPORTANT: Tax credits cannot create negative tax (no refund through payroll).

### Step 2.5: Calculate Pension Tax Credit (Zikui Gemel, Section 45a)

Employees who contribute to a pension fund get a **35% tax credit on their pension contribution**, separate from credit points. This is a frequently missed item: skipping it overstates tax by up to ~238 NIS/month.

Rule (2026):
```
eligible_contribution = min(
    actual_employee_pension_contribution,
    7% * min(insured_salary, 9,700 NIS/month)
)
pension_credit = 35% * eligible_contribution
```

- Qualifying-salary ceiling (2026): **9,700 NIS/month**
- Max qualifying contribution: 7% × 9,700 = **679 NIS/month**
- Max monthly credit: 35% × 679 = **237.65 NIS/month**
- Applied alongside credit points. Tax cannot go below zero.

Example (15,000 NIS gross, 6% pension): actual contribution 900 NIS; capped at 679 (since 7% × 9,700 = 679); credit = 237.65 NIS/month.

Example (8,000 NIS gross, 6% pension): actual contribution 480 NIS; cap here is 7% × 8,000 = 560 (below 679); eligible = 480; credit = 168 NIS/month.

See `references/credit-points.md` for the full rule, including the additional 5% / 485 NIS option for uninsured salary.

### Step 3: Calculate Bituach Leumi (National Insurance)

NI and health tax apply to the **taxable gross** (cash gross + shovi rechev + other imputed income), capped at the max insurable salary. Two brackets: a reduced tier up to a separately published threshold (7,703 NIS/month in 2026, not a derived percentage of the average wage), and a full tier from there up to the ceiling.

For the standard employee, an Israeli resident aged 18 to retirement age (2026 thresholds; the rates have applied since Amendment 252 took effect on 1.1.2025, as a temporary provision for 2025-2026 that may be extended by order):
- On first 7,703 NIS: 1.04% NI + 3.23% health = **4.27%**
- On amount 7,704 to 51,910 NIS: 7.0% NI + 5.17% health = **12.17%**
- Maximum insurable salary: 51,910 NIS/month
- Salary above the ceiling is not subject to NI or health tax.

**Pick the insurance category before computing.** The 4.27% / 12.17% is only column 1 of the
official Bituach Leumi rate table. The employee deduction is **0%** for an employee under 18 or one
already receiving an old-age pension, **4.25% / 11.96%** for a controlling shareholder in their own
close company (every owner-director on their own payroll), **3.93% / 10.03%** for women and men aged
67 to 70 not yet receiving the pension, **3.95% / 10.24%** for a woman between her own retirement age
and the men's, **3.60% / 7.45%** for someone who first became an Israeli resident after age 62 and is
below retirement age, **3.23% / 5.17%** for a recipient of a work-injury or general-disability
pension holding an annual Bituach Leumi confirmation, and **1.04% / 7.00%** with NO health tax for a
soldier in regular service, an organ donor or a treaty-country foreign resident. Applying the
standard rate to a minor or a pensioner over-charges them by the entire deduction.

The script encodes the whole table and will compute any row for you:

```
python scripts/calculate_payroll.py --list-ni-categories
python scripts/calculate_payroll.py --gross 12000 --ni-category controlling-shareholder
```

See `references/bituach-leumi-rates.md` for the full table in prose, including the
controlling-shareholder sub-row that exists under every age and status row.

**Pick the year by the month being paid.** The rates above are the same in 2025 and 2026; only the thresholds moved on 1.1.2026. A 2025 payslip uses a reduced tier up to 7,522 and a ceiling of 50,695 (and 5.00% full-tier health tax in January 2025 only). The 3.5% / 12.0% rates often quoted are the 2024 ones, from before Amendment 252. See `references/bituach-leumi-rates.md` for the year-by-year table.

### Step 4: Calculate Pension Deductions

Pension applies to the **cash gross only** (not to shovi rechev). Mandatory for most employees since 2017:
- Employee: 6% of cash gross (up to pension ceiling)
- Employer: 6.5% + 6% severance (6% is the mandatory minimum severance under the pension expansion order; an employer under a full Section 14 arrangement deposits 8.33% instead, which fully discharges the statutory severance liability)

The employee's contribution also generates the 35% tax credit computed in Step 2.5.

**High earners: employer deposits above the exempt ceiling are taxable (2026).** The employer's
pension deposit is exempt only up to 7.5% of a salary capped at 34,423 NIS/month, and the
severance deposit only up to 3,798 NIS/month (8.33% of the 45,600 severance ceiling). The excess
is imputed to the employee as taxable income: it enters the income-tax AND the National Insurance
and health base like shovi rechev (Bituach Leumi circular 1460 / employers 1479, item 5),
but is never received as cash. With the default 6.5% / 6% it starts at roughly 39,700 NIS gross;
under a full Section 14 arrangement (8.33%) the severance excess starts near 45,600. Skipping it
overstates net pay by about 3% at a 70,000 gross. The script does this automatically (pass
`--severance-rate 0.0833` for Section 14).

**Keren hishtalmut (ask about it, do not silently omit it).** Where the employer
offers a study fund, the employee side is typically 2.5% of salary and the
employer side 7.5%, and the employee 2.5% is a real cash deduction that lands on
the payslip. It is the largest ordinary deduction the default net calculation
leaves out, so a net computed without it reads high for anyone who has one. It is
not statutory, so do not assume it: ask whether the employee has a keren
hishtalmut, and if so include the 2.5% in Step 5 and say that you did (the script
takes `--keren-hishtalmut`). Employer
deposits are tax-exempt up to a salary of 15,712 NIS/month in 2026 (the ceiling
changes annually); above it the excess employer deposit becomes taxable income to
the employee. Most employers deposit only on salary up to that ceiling, which is
what the script models; ask, because an employer that deposits on the full salary
creates taxable income on the excess, for income tax and National Insurance alike
(`--keren-full-salary`, which also turns the keren on).

### Step 5: Calculate Net Salary (Neto)
```
Net Cash = Cash Gross
         - Income Tax (on taxable_gross)
         - Bituach Leumi (on taxable_gross)
         - Health Tax (on taxable_gross)
         - Pension (6% of cash gross)
         - Keren hishtalmut (2.5% of cash gross up to 15,712, ONLY if the employee has one)
         - Other deductions (union dues, loans, etc.)
```

Shovi rechev does NOT appear as an addend here. The employee never received it as cash; only the tax effect flows through.

### Step 6: Calculate Employer Total Cost (if requested)

Employer NI applies to the taxable gross (includes shovi rechev). Pension and severance apply to cash gross.

```
Employer Cost = Cash Gross
              + Employer NI (4.51% reduced / 7.6% full, on taxable_gross capped at 51,910)
              + Employer Pension (6.5% of cash gross)
              + Employer Severance (6% of cash gross)
              + Vacation accrual
              + Sick leave accrual
```

Note: In Israel, health tax is an employee-only deduction; there is no separate employer health component in the mandatory payroll stack.

### Step 7: Present Clear Breakdown
Present results as a payslip-style table. When shovi rechev is present, show the taxable gross row so the user understands why the deductions look larger than cash-gross alone would imply.

| Item | Amount (NIS) |
|------|-------------|
| Gross Salary (cash) | XX,XXX |
| Shovi Rechev (taxable, not cash) | +X,XXX |
| **Taxable Gross** | **XX,XXX** |
| Income Tax | -X,XXX |
| Bituach Leumi | -XXX |
| Health Tax | -XXX |
| Pension (employee) | -X,XXX |
| **Net Salary (cash)** | **XX,XXX** |

CAVEAT: Always note "This is an estimate. Actual amounts may vary based on specific tax rulings, additional credits, employer agreements, or collective bargaining terms. Consult a certified Israeli accountant (roeh cheshbon) for exact figures."

## Examples

### Example 1: Standard Employee, No Company Car
User says: "Calculate net salary for 20,000 NIS gross, male, no special credits"
Result: Detailed breakdown showing 14,530.69 NIS net using 2026 rates (20,000 gross, 2.25 credit points, 6% pension).

### Example 2: Employer Cost
User says: "How much does it cost an employer to pay 15,000 NIS gross?"
Result: Total employer cost approximately 17,500-18,500 NIS including NI, pension, and severance.

### Example 3: Gross + Company Car (shovi rechev)
User says: "I earn 22,000 NIS + company car with shovi rechev of 3,500. What's my net?"

Correct flow:
1. Taxable gross = 22,000 + 3,500 = 25,500 NIS
2. Income tax applies to 25,500 (progressive brackets per Amendment 288, less 2.25 credit points and 35% pension credit)
3. Bituach Leumi applies to 25,500 (two brackets: 4.27% reduced + 12.17% full)
4. Pension 6% applies to 22,000 only (not to shovi rechev)
5. Net cash = 22,000 - income_tax - NI - health - pension ≈ 14,000 NIS (with gemel credit), or about 13,783 NIS if the 237.65 gemel credit is omitted (common error)

Wrong answer to avoid: adding the 3,500 shovi rechev to net. The employee never receives it as cash; the employer provides the car. Car value raises deductions, it does NOT raise take-home pay.

## Bundled Resources

### Scripts
- `scripts/calculate_payroll.py`, Calculates Israeli gross-to-net salary with progressive income tax brackets, Bituach Leumi, health tax, pension contributions, and shovi rechev (company-car use value) as taxable imputed income. Supports employee and employer cost views. Run: `python scripts/calculate_payroll.py --help`. Use `--shovi-rechev <NIS>` to model a company car, and `--ni-category <key>` to compute for a non-standard Bituach Leumi category (`--list-ni-categories` prints the whole official table).

### References
- `references/tax-brackets.md`, Israeli income tax brackets (annual and monthly) with progressive rates from 10% to 50%. Amendment 288 (published 31.3.2026, retroactive to 1.1.2026) widened the 20% and 31% brackets for 2026. Also referenced in Step 2 and Troubleshooting below. Consult when computing income tax or verifying bracket thresholds.
- `references/bituach-leumi-rates.md`, Bituach Leumi (National Insurance) and health tax rates for employees and employers for 2026, covering the reduced and full brackets, the monthly insurable salary ceiling, and the full official rate table by insurance category (age, old-age pension, controlling shareholder, new resident over 62, soldier/organ donor/treaty resident), keyed to the script's `--ni-category` values. Always verify the current-year values against btl.gov.il before relying on exact amounts.
- `references/credit-points.md`, Israeli tax credit points (nekudot zikui) value and full eligibility table covering base credits, gender, new immigrants, children, single parents, and disability. Also documents the Section 45a pension tax credit (zikui gemel, 35% of pension contribution up to 679 NIS/month in 2026). Consult when determining total credits beyond the defaults in Step 1.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| רשות המיסים (Tax Authority) | https://www.gov.il/he/service/income-tax-calculator | Official income tax calculator (authoritative for current-year rates) |
| Income Tax brackets (Kolzchut) | https://www.kolzchut.org.il/he/%D7%9E%D7%93%D7%A8%D7%92%D7%95%D7%AA_%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94 | Current monthly and annual brackets, sourced from legislation |
| Bituach Leumi employee rates | https://www.btl.gov.il/Insurance/Rates/Pages/%D7%9C%D7%A2%D7%95%D7%91%D7%93%D7%99%D7%9D%20%D7%A9%D7%9B%D7%99%D7%A8%D7%99%D7%9D.aspx | Employee/employer NI and health tax rates, ceilings, and the full rate table by insurance category (form-102 columns 1, 2 and 3) |
| Credit points (Nekudot Zikui) | https://www.kolzchut.org.il/he/%D7%A0%D7%A7%D7%95%D7%93%D7%95%D7%AA_%D7%96%D7%99%D7%9B%D7%95%D7%99_%D7%9E%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94 | Credit point value and eligibility tables |
| Shovi rechev (Hilan FAQ) | https://www.hilan.co.il/%D7%9E%D7%A8%D7%9B%D7%96-%D7%99%D7%93%D7%A2/%D7%91%D7%A1%D7%99%D7%A1-%D7%99%D7%93%D7%A2/%D7%A9%D7%90%D7%9C%D7%95%D7%AA-%D7%A0%D7%A4%D7%95%D7%A6%D7%95%D7%AA/%D7%A8%D7%9B%D7%91-%D7%A6%D7%9E%D7%95%D7%93/ | How shovi rechev is applied to the payslip (tax base impact, not pension base) |

## Gotchas

- **Shovi rechev is taxable imputed income, not a benefit.** A company car adds to the income-tax and bituach-leumi base but is NOT received in cash. Agents commonly add shovi rechev to net salary instead of adding it to the tax base. This flips the sign of the impact and can overstate net pay by thousands of shekels. Pension base does NOT include shovi rechev.
- **Amendment 288 (March 2026) widened two brackets.** Older references that print the 2025 brackets are out of date for 2026: the 20% bracket runs to 19,000 (was 16,150), 31% to 25,100 (was 22,440), 35% from 25,101. Values in training data that cite 16,150/22,440 as ceilings are wrong for 2026. Do not attribute the Bituach Leumi rates to 2026 either: Amendment 252 raised the reduced-tier rates (employee 0.4% → 1.04%, employer 3.55% → 4.51%) from 1.1.2025. Only the reduced threshold (7,522 → 7,703) and the ceiling (50,695 → 51,910) changed in 2026.
- **Zikui gemel (pension tax credit, sec. 45a) is frequently forgotten.** A 35% credit on the employee pension contribution (up to 7% × min(salary, 9,700) = 679 NIS/month) is applied on the payslip. Most payroll software computes it automatically, but agents hand-calculating tax often omit it and overstate monthly tax by up to ~238 NIS.
- **Keren Hishtalmut** (2.5% employee + 7.5% employer) is tax-exempt on salary up to 15,712 NIS/month in 2026. Not in the default flow because it is not statutory: pass `--keren-hishtalmut` when the employee has one.
- **Mandatory pension since 2017:** 6% employee + 6.5% employer minimum. Agents may skip pension or use pre-2017 rates (5%+5%).
- **The Bituach Leumi rate is not one number.** The official table has 11 employee categories plus a controlling-shareholder sub-row under each. An owner-director of a one-person Israeli company pays 4.25% / 11.96%, not 4.27% / 12.17%; a minor or a pensioner pays nothing; a soldier in regular service, an organ donor or a treaty-country foreign resident pays National Insurance only, with no health tax. Agents default to the standard row and silently over-charge everyone else. Pass `--ni-category` to the script.
- **Bituach Leumi ceiling caps deductions.** Salary above 51,910 NIS/month (2026) is not subject to NI or health tax. Agents may apply the full rate to the entire salary instead of capping.
- **Credit points (nekudot zikui):** Base 2.25 for a resident; women get +0.5. Children add a lot and are age-banded per child (year of birth 2.5; ages 1-2 4.5; age 3 3.5; ages 4-5 2.5; ages 6-17 2 for the mother and 1 for the father), and new immigrants, single parents and academic degrees add more. Disability is NOT a credit point: a blind employee, or one with 100% or qualifying 90%+ disability, has an income-tax exemption under s.9(5) instead, with a ceiling of 684,000 or 445,200 a year depending on the route (see `references/credit-points.md`). Agents may omit them entirely and overstate the tax burden. These are separate from and stack with the pension credit above. See `references/credit-points.md` for the full per-age, per-parent table.

## Troubleshooting

### Error: "Net salary is way off for an employee with a company car"
Cause: Shovi rechev was treated as a benefit added to net, or was omitted from the tax base.
Solution: Shovi rechev adds to the taxable gross (for income tax and NI), not to cash received. Use `--shovi-rechev <NIS>` when running `calculate_payroll.py`. See Step 1.5 and Example 3.

### Error: "Tax brackets may be outdated"
Cause: Brackets do update, and sometimes mid-year. Amendment 288 (published 31.3.2026, retroactive to 1.1.2026) widened the 20% and 31% brackets; the other thresholds and the credit point value did not move. Bituach Leumi rates have not changed since Amendment 252 (1.1.2025); its thresholds update every January.
Solution: Verify current brackets at the Tax Authority website (gov.il/he/service/income-tax-calculator). Bituach Leumi tiers and the max insurable salary update annually and should be cross-checked against btl.gov.il, see `references/bituach-leumi-rates.md` and `references/tax-brackets.md` for the values used in this skill.

### Error: "Tax is higher than my payslip shows"
Cause: Zikui gemel (pension credit, sec. 45a) was omitted from the calculation. Payroll software applies this automatically; manual calculators usually forget it.
Solution: Subtract the pension tax credit after bracket-based tax and credit points. See Step 2.5 and `references/credit-points.md`. Max ~238 NIS/month in 2026.

### Error: "Credit points don't match"
Cause: Various life circumstances affect credit points.
Solution: Review the full credit point table. Common additions: female (+0.5), new immigrant (up to +3), each child by age (year of birth 2.5, ages 1-2 4.5, age 3 3.5, ages 4-5 2.5, ages 6-17 2 for the mother / 1 for the father), single parent (+1), disabled child (+2). See `references/credit-points.md`.
