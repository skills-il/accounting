---
name: israeli-payroll-calculator
description: Calculate Israeli payroll including income tax, Bituach Leumi (National Insurance), health tax, pension contributions, shovi rechev (company-car use value), and net salary. Use when user asks to calculate salary, "tlush maskoret", payroll deductions, "bruto to neto", employer cost, tax credits (nekudot zikui), company car impact on salary, or needs help understanding Israeli payslip items. Covers employees, freelancers (atzmai), and employer cost calculations. Do NOT use for US, UK, or other countries' payroll calculations.
license: MIT
allowed-tools: Bash(python:*)
compatibility: Works with Claude Code, Claude.ai, Cursor. No network access required.
---

# Israeli Payroll Calculator

## Instructions

### Step 1: Gather Employee Information
Collect from user:
- **Gross monthly salary** (bruto, cash) in NIS
- **Tax credit points** (nekudot zikui): Default 2.25 for male resident, 2.75 for female
- **Shovi rechev** (company-car use value, if any): Monthly NIS value. See Step 1.5.
- **Other taxable allowances** (shovi telephone, meals above exemption, etc.)
- **Pension arrangement:** Yes/No, contribution percentages
- **Employment type:** Employee (sachir), Freelancer (atzmai)
- **Age:** Affects NI rates (under/over 18, retirement age)

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
2. Apply brackets progressively (see references/tax-brackets.md). Brackets are frozen 2025-2027 by legislation.
3. Subtract tax credit value: `credit_points * 242 NIS/month`
4. Monthly tax = `max(0, calculated_tax - credits)`

IMPORTANT: Tax credits cannot create negative tax (no refund through payroll).

### Step 3: Calculate Bituach Leumi (National Insurance)

NI and health tax apply to the **taxable gross** (cash gross + shovi rechev + other imputed income), capped at the max insurable salary.

For employees (2026):
- On first 7,522 NIS: 0.4% NI + 3.1% health = 3.5%
- On amount 7,523 to 51,910 NIS: 7.0% NI + 5.0% health = 12.0%
- Maximum insurable salary: 51,910 NIS/month
- Salary above the ceiling is not subject to NI or health tax.

### Step 4: Calculate Pension Deductions

Pension applies to the **cash gross only** (not to shovi rechev). Mandatory for most employees since 2017:
- Employee: 6% of cash gross (up to pension ceiling)
- Employer: 6.5% + 6% severance

This deduction comes out of cash gross and provides tax benefits.

### Step 5: Calculate Net Salary (Neto)
```
Net Cash = Cash Gross
         - Income Tax (on taxable_gross)
         - Bituach Leumi (on taxable_gross)
         - Health Tax (on taxable_gross)
         - Pension (6% of cash gross)
         - Other deductions (union dues, loans, etc.)
```

Shovi rechev does NOT appear as an addend here. The employee never received it as cash; only the tax effect flows through.

### Step 6: Calculate Employer Total Cost (if requested)

Employer NI applies to the taxable gross (includes shovi rechev). Pension and severance apply to cash gross.

```
Employer Cost = Cash Gross
              + Employer NI (3.45% reduced / 7.6% full, on taxable_gross capped at 51,910)
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
Result: Detailed breakdown showing approximately 14,500-15,000 NIS net using 2026 rates.

### Example 2: Employer Cost
User says: "How much does it cost an employer to pay 15,000 NIS gross?"
Result: Total employer cost approximately 17,500-18,500 NIS including NI, pension, and severance.

### Example 3: Gross + Company Car (shovi rechev)
User says: "I earn 22,000 NIS + company car with shovi rechev of 3,500. What's my net?"

Correct flow:
1. Taxable gross = 22,000 + 3,500 = 25,500 NIS
2. Income tax applies to 25,500 (progressive brackets)
3. Bituach Leumi applies to 25,500
4. Pension 6% applies to 22,000 only (not to shovi rechev)
5. Net cash = 22,000 - income_tax - NI - health - pension ≈ 13,400-13,500 NIS

Wrong answer to avoid: adding the 3,500 shovi rechev to net. The employee never receives it as cash; the employer provides the car. Car value raises deductions, it does NOT raise take-home pay.

## Bundled Resources

### Scripts
- `scripts/calculate_payroll.py` — Calculates Israeli gross-to-net salary with progressive income tax brackets, Bituach Leumi, health tax, pension contributions, and shovi rechev (company-car use value) as taxable imputed income. Supports employee and employer cost views. Run: `python scripts/calculate_payroll.py --help`. Use `--shovi-rechev <NIS>` to model a company car.

### References
- `references/tax-brackets.md` — Israeli income tax brackets (annual and monthly) with progressive rates from 10% to 50%. The 2025-2027 brackets are frozen per Knesset legislation. Also referenced in Step 2 and Troubleshooting below. Consult when computing income tax or verifying bracket thresholds.
- `references/bituach-leumi-rates.md` — Bituach Leumi (National Insurance) and health tax rates for employees and employers for 2026, covering the reduced and full brackets and the monthly insurable salary ceiling. Always verify the current-year values against btl.gov.il before relying on exact amounts.
- `references/credit-points.md` — Israeli tax credit points (nekudot zikui) value and full eligibility table covering base credits, gender, new immigrants, children, single parents, and disability. Consult when determining a taxpayer's total credit points beyond the defaults in Step 1.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| רשות המיסים (Tax Authority) | https://www.gov.il/he/service/income-tax-calculator | Official income tax calculator (authoritative for current-year rates) |
| Income Tax brackets (Kolzchut) | https://www.kolzchut.org.il/he/%D7%9E%D7%93%D7%A8%D7%92%D7%95%D7%AA_%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94 | Current monthly and annual brackets, sourced from legislation |
| Bituach Leumi employee rates | https://www.btl.gov.il/Insurance/Rates/Pages/%D7%9C%D7%A2%D7%95%D7%91%D7%93%D7%99%D7%9D%20%D7%A9%D7%9B%D7%99%D7%A8%D7%99%D7%9D.aspx | Employee/employer NI and health tax rates, ceilings |
| Credit points (Nekudot Zikui) | https://www.kolzchut.org.il/he/%D7%A0%D7%A7%D7%95%D7%93%D7%95%D7%AA_%D7%96%D7%99%D7%9B%D7%95%D7%99_%D7%9E%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94 | Credit point value and eligibility tables |
| Shovi rechev (Hilan FAQ) | https://www.hilan.co.il/%D7%9E%D7%A8%D7%9B%D7%96-%D7%99%D7%93%D7%A2/%D7%91%D7%A1%D7%99%D7%A1-%D7%99%D7%93%D7%A2/%D7%A9%D7%90%D7%9C%D7%95%D7%AA-%D7%A0%D7%A4%D7%95%D7%A6%D7%95%D7%AA/%D7%A8%D7%9B%D7%91-%D7%A6%D7%9E%D7%95%D7%93/ | How shovi rechev is applied to the payslip (tax base impact, not pension base) |

## Gotchas

- **Shovi rechev is taxable imputed income, not a benefit.** A company car adds to the income-tax and bituach-leumi base but is NOT received in cash. Agents commonly add shovi rechev to net salary instead of adding it to the tax base. This flips the sign of the impact and can overstate net pay by thousands of shekels. Pension base does NOT include shovi rechev.
- **Tax brackets, NI rates, and credit values update annually.** Income tax brackets are frozen 2025-2027 by legislation but NI ceilings, health tax splits, and the credit point value adjust each January 1. Agents may use last year's NI ceiling and silently undercount deductions near the top of the reduced tier.
- **Keren Hishtalmut** (2.5% employee + 7.5% employer) is tax-exempt up to a ceiling that changes yearly. Not included in this calculator's default flow. Add manually if the employer offers it.
- **Mandatory pension since 2017:** 6% employee + 6.5% employer minimum. Agents may skip pension or use pre-2017 rates (5%+5%).
- **Bituach Leumi ceiling caps deductions.** Salary above 51,910 NIS/month (2026) is not subject to NI or health tax. Agents may apply the full rate to the entire salary instead of capping.
- **Credit points (nekudot zikui):** Base 2.25 for a resident; women get +0.5. New immigrants, single parents, children under 5 (for mothers), disabled status, and academic degrees add more. Agents may omit them entirely and overstate the tax burden.

## Troubleshooting

### Error: "Net salary is way off for an employee with a company car"
Cause: Shovi rechev was treated as a benefit added to net, or was omitted from the tax base.
Solution: Shovi rechev adds to the taxable gross (for income tax and NI), not to cash received. Use `--shovi-rechev <NIS>` when running `calculate_payroll.py`. See Step 1.5 and Example 3.

### Error: "Tax brackets may be outdated"
Cause: Tax brackets update annually (usually January 1). Israeli income tax brackets were frozen by legislation for 2025-2027.
Solution: Verify current brackets at the Tax Authority website (gov.il/he/service/income-tax-calculator). Bituach Leumi tiers and the max insurable salary update annually and should be cross-checked against btl.gov.il — see references/bituach-leumi-rates.md for the values used in this skill.

### Error: "Credit points don't match"
Cause: Various life circumstances affect credit points.
Solution: Review the full credit point table. Common additions: female (+0.5), new immigrant (up to +3), child under 18 (+1), child under 5 for women (+1.5), single parent (+1), disabled (+2).
