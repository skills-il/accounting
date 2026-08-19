# Domain coverage checklist: Israeli payroll calculator

Persona anchor: Israeli CPA (רואה חשבון) with payroll and small-business experience.

## Must cover (core)

- **Income tax by progressive bracket, monthly and annual.** Amendment 288 (published 31.3.2026,
  retroactive to 1.1.2026) widened brackets 3 to 5. Seven bracket rows, top marginal 50%
  (47% statutory plus the 3% surtax, counted once).
- **Tax credit points (nekudot zikui).** Point value, base entitlement, gender, children by age band,
  single parent, new immigrant, disability.
- **Section 45a pension tax credit (zikui gemel).** 35% of the eligible contribution, capped at 7%
  of the insured salary with the insured salary itself capped.
- **Employee Bituach Leumi and health tax BY INSURANCE CATEGORY, not as a single rate.** The
  official rate table (btl.gov.il, organised by the columns of the employee-reporting form) has
  ELEVEN employee categories, each with a controlling-shareholder sub-row. A one-line "employee pays
  4.27% / 12.17%" entry is the exact defect this row exists to prevent. The rate must vary by:
  - age band (under 18; 18 to retirement age; a woman between her retirement age and the men's;
    67 to 70; over 70)
  - whether an old-age pension is already being drawn
  - controlling-shareholder status in a close company (בעל שליטה בחברת מעטים)
  - residency history (first became an Israeli resident after age 62)
  - special status (soldier in regular service, organ donor, treaty-country foreign resident:
    National Insurance only, NO health tax)
  - disability-pension receipt with an annual Bituach Leumi confirmation
  Each of those is its own Must-cover row, and each must be selectable from the bundled script,
  not only described in prose. A rate table a caller cannot reach from code is not covered.
- **Employer Bituach Leumi by the same categories.** The employer share differs between columns even
  where the employee share is nil (a minor and a pensioner still cost the employer 0.61% / 2.12%).
- **Reduced-tier threshold and maximum insurable salary**, and the fact that the threshold is
  published separately rather than derived as a percentage of the average wage.
- **Mandatory pension**: employee and employer minimum rates and the severance component, including
  the Section 14 arrangement.
- **Shovi rechev as taxable imputed income**: in the income-tax and National Insurance base, out of
  the pension base, never added to net cash.
- **Minimum-wage sanity check** on the gross before computing.

## Should cover (advanced)

- **Keren hishtalmut** (employee 2.5% / employer 7.5%): not statutory, so it must be asked about
  rather than assumed, but it is the largest ordinary deduction a default net calculation omits.
- **New-immigrant National Insurance exemption** for the first 12 months, with health tax still due.
  This is an exemption layered on top of the category table, not a row of it.
- **Employer accruals** beyond the payroll stack: vacation and sick-leave provisioning.
- **Self-employed rates**, which are a separate two-tier schedule with no employer share.

## Out of scope (explicit)

- Working out the gross owed from a timesheet, overtime tiers, weekly-rest premium and the burden
  shift where no attendance record exists. `israeli-attendance-wage-checker` does that and runs
  first; this skill starts from an agreed gross.
- The full non-working / passive-income National Insurance rules, which belong to
  `israeli-bituach-leumi`.
- Public-sector collective wage agreements and their dirug wage tables, which belong to the
  sector-specific payroll skills.
- Non-Israeli payroll.

## Authoritative sources

- btl.gov.il employee rate table (the full category table, effective 01.01.2026).
- kolzchut.org.il income-tax bracket, credit-point and pension-credit pages.
- gov.il Israel Tax Authority income-tax calculator.
