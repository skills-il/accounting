# Bituach Leumi (National Insurance) Rates (2026)

Amendment 252 to the National Insurance Law (effective 1.1.2026) raised the reduced-tier employee rate from 0.4% to 1.04% and the reduced-tier employer rate from 3.55% to 4.51%, and it set the reduced-tier threshold at 7,703 NIS/month (the reduced-tier ceiling published by Bituach Leumi for 2026, a separately-set figure, not a plain 60% of any single average-wage number). Full-bracket rates also edged up via health-tax re-basing.

## Employee Rates

### Reduced Bracket (up to 7,703 NIS/month)
| Component | Employee | Employer |
|-----------|----------|----------|
| National Insurance | 1.04% | 4.51% |
| Health Tax | 3.23% | 0.00% |
| **Total** | **4.27%** | **4.51%** |

### Full Bracket (7,704 - 51,910 NIS/month)
| Component | Employee | Employer |
|-----------|----------|----------|
| National Insurance | 7.00% | 7.60% |
| Health Tax | 5.17% | 0.00% |
| **Total** | **12.17%** | **7.60%** |

Note: Health tax is an employee-only deduction in Israel. Employers do not contribute to health tax (mas briut).

### Maximum Insurable Salary (2026)
- **51,910 NIS/month** (unchanged from 2025)
- Salary above this amount: no additional NI or health deductions.
- The reduced-tier threshold (7,703) is published by Bituach Leumi and updates each January 1 by CPI through 2028, then by average-wage growth from 2029. Kol-Zchut describes it as 60% of the average wage, but do not derive it that way: 60% of the 2026 average wage (13,769) is 8,261, not 7,703.

### What Changed vs. 2025
| Parameter | 2025 | 2026 |
|-----------|------|------|
| Reduced-tier threshold | 7,522 | 7,703 |
| Employee NI (reduced) | 0.40% | 1.04% |
| Employer NI (reduced) | 3.55% | 4.51% |
| Employee health (reduced) | 3.10% | 3.23% |
| Employee health (full) | 5.00% | 5.17% |
| Employee NI (full) | 7.00% | 7.00% (unchanged) |
| Employer NI (full) | 7.60% | 7.60% (unchanged) |
| Max insurable | 50,695 | 51,910 |

### Worked Example (2026)
Employee, monthly gross 12,000 NIS, no shovi rechev:
- Reduced portion: 7,703 x 4.27% = 329 NIS
- Full portion: (12,000 - 7,703) x 12.17% = 4,297 x 12.17% = 523 NIS
- Total employee NI + health: ~852 NIS/month

(2025 equivalent: 7,522 x 3.5% + 4,478 x 12.0% = 263 + 537 = 800 NIS/month. The shift of 52 NIS/month roughly matches the Calcalist "576 NIS/year extra for employees" figure.)

## Self-Employed Rates (2026)
Self-employed pay the whole amount themselves (no employer share) in two brackets, split at the reduced-tier threshold (7,703 NIS/month in 2026, the same threshold as for employees) up to the maximum insurable income of 51,910 NIS/month. The reduced-tier rates rose under Amendment 252. The National Insurance rates below are self-employed NI only; health tax is a separate line. Re-verify against btl.gov.il before computing atzmai payroll.

### Reduced Bracket (up to 7,703 NIS/month)
- National Insurance: 4.47%
- Health Tax: ~3.23%

### Full Bracket (7,704 - 51,910 NIS/month)
- National Insurance: 12.83%
- Health Tax: ~5.17%

## Employee Rate Varies by Category (2026, full official table)

The 4.27% / 12.17% above is ONLY column 1 of the official table: an Israeli resident aged 18 to
retirement age. The amount actually deducted changes with age, old-age-pension status,
controlling-shareholder status, residency history and a few special statuses. Applying the standard
rate to a minor, a pensioner or an owner-director is a material error. Every owner-director of an
Israeli micro-company sits in column 2, not column 1.

**This table is reachable from code.** `scripts/calculate_payroll.py` encodes the same rows in
`NI_CATEGORIES`; pass `--ni-category <key>` to compute with one, or `--list-ni-categories` to print
the table. Do not compute a payslip for a non-standard employee without selecting the category.

The employee figures below are the TOTAL employee rate (National Insurance plus health tax), which
is how Bituach Leumi publishes them. Where a National-Insurance-only figure is needed, subtract the
health rate (3.23% reduced / 5.17% full) for any category that pays health tax; the last row pays
National Insurance only.

| `--ni-category` key | Employee category | Employee reduced (to 7,703) | Employee full (7,703 to 51,910) | Employer reduced | Employer full |
|---|---|---|---|---|---|
| `standard` | Israeli resident aged 18 to retirement age (column 1) | **4.27%** | **12.17%** | 4.51% | 7.60% |
| `controlling-shareholder` | בעל שליטה בחברת מעטים, 18 to retirement age (column 2) | **4.25%** | **11.96%** | 4.46% | 7.38% |
| `under-18` | Under 18 | **0%** | **0%** | 0.61% | 2.12% |
| `under-18-shareholder` | Under 18, controlling shareholder | **0%** | **0%** | 0.60% | 2.06% |
| `old-age-pension` | Receiving an old-age pension (kitzbat ezrach vatik), any age | **0%** | **0%** | 0.61% | 2.12% |
| `old-age-pension-shareholder` | Receiving an old-age pension, controlling shareholder | **0%** | **0%** | 0.60% | 2.06% |
| `age-67-70-no-pension` | Women AND men aged 67 to 70 not receiving an old-age pension | **3.93%** | **10.03%** | 4.13% | 6.96% |
| `age-67-70-no-pension-shareholder` | Same, controlling shareholder | **3.93%** | **10.03%** | 4.12% | 6.90% |
| `woman-retirement-to-67-no-pension` | Woman between her retirement age and the men's retirement age (67), not receiving an old-age pension | **3.95%** | **10.24%** | 4.17% | 7.12% |
| `new-resident-over-62-under-retirement` | Became an Israeli resident for the first time after age 62, below retirement age | **3.60%** | **7.45%** | 1.04% | 2.95% |
| `new-resident-over-62-woman-to-67` | Woman between her retirement age and the men's retirement age, first became a resident after 62 | **3.28%** | **5.52%** | 0.70% | 2.47% |
| `new-resident-over-62-67-to-70` | Man or woman between the men's retirement age and 70, first became a resident after 62 | **3.26%** | **5.31%** | 0.66% | 2.31% |
| `new-resident-over-62-over-70` | Over 70 (old-age-pension eligibility age), first became a resident after 62 | **3.23%** | **5.17%** | 0.61% | 2.12% |
| `new-resident-over-62-over-70-shareholder` | Same, controlling shareholder | **3.23%** | **5.17%** | 0.60% | 2.06% |
| `disability-pension` | Receiving a work-injury or general-disability pension, with an annual Bituach Leumi confirmation | **3.23%** | **5.17%** | 0.61% | 2.12% |
| `disability-pension-shareholder` | Same, controlling shareholder | **3.23%** | **5.17%** | 0.60% | 2.06% |
| `soldier-organ-donor-treaty-resident` | Soldier in regular service, organ donor, or foreign resident from a social-security treaty country. National Insurance only, NO health tax | **1.04%** | **7.00%** | 4.51% | 7.60% |
| `soldier-organ-donor-treaty-resident-shareholder` | Same, controlling shareholder | **1.02%** | **6.79%** | 4.46% | 7.38% |

Notes:
- **Controlling shareholder (בעל שליטה בחברת מעטים)** means holding at least 10% of the company's
  shares or the right to appoint a director. A separate shareholder sub-row exists under every age
  and status row, which is why the shareholder keys above shadow the ordinary ones.
- The employer share does NOT vary with the employee's age within column 1, but it DOES differ
  between columns: for a minor or a pensioner the employee pays nothing while the employer still
  pays its 0.61% / 2.12%.
- The last row is the only one with no health-tax component, which is why 1.04% / 7.00% there are
  the bare National Insurance rates. A foreign caregiver from a treaty country sits in this row.
- New immigrants (oleh chadash) have a 12-month exemption from National Insurance; health tax still
  applies. That is an exemption layered on top of the table, not a row of it.
- A resident with no income still owes the minimum non-working payment (266 NIS/month in 2026), see
  the israeli-bituach-leumi skill for the full non-working / passive-income rules.
- Source: btl.gov.il employee rate table (2026 figures effective 01.01.2026).

## Shovi Rechev (Company Car Use Value)
- Shovi rechev is subject to NI and health tax on the employee side (employee pays NI and health on the taxable gross = cash + shovi rechev).
- Employer NI also applies to shovi rechev.
- Shovi rechev is NOT part of the pension-insurable salary.

## Payment
- Employee: Deducted from salary by employer
- Self-employed: Quarterly advance payments, annual reconciliation
- Late payment: Interest and linkage differentials apply

## Source
- https://www.btl.gov.il/Insurance/Rates/Pages/%D7%9C%D7%A2%D7%95%D7%91%D7%93%D7%99%D7%9D%20%D7%A9%D7%9B%D7%99%D7%A8%D7%99%D7%9D.aspx (authoritative)
