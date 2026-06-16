# Domain coverage checklist, Israeli bookkeeping journal-entry automation

Scope: generating double-entry (and Osek Patur single-entry) journal entries (pkudot yoman)
for Israeli businesses, payroll, VAT, depreciation, revenue, B2B invoicing. This is the
coverage anchor: every "Must cover" item should be enumerated explicitly in SKILL.md, not
deferred to an external "check the official site" pointer, because a journal-entry skill that
omits a status/rate row silently produces a wrong posting.

Year baseline: 2026. Threshold (reduced/full split) 7,703 ₪/month; max insurable income
51,910 ₪/month. VAT 18% (since 01.01.2025).

---

## Must cover (core)

### Bituach Leumi / health-insurance rate table, EVERY employee category as its own row

The skill must enumerate each category below as a separate rate line, because each produces a
different deduction and a different employer cost. Showing only the regular-employee row and
adding a "rates vary, check btl.gov.il" note is NOT sufficient for a posting tool.
(Source: National Insurance Institute, "שיעורי וסכומי דמי ביטוח, לעובדים שכירים",
btl.gov.il/Insurance/Rates; BTL employer circular "שינוי בתשלום דמי ביטוח לאומי ודמי ביטוח
בריאות לשנת 2026"; National Insurance Law [Consolidated Version] 5755-1995.)

- **Standard resident employee, age 18 to retirement (עובד רגיל):**
  reduced (≤7,703) employee 4.27% (BL 1.04% + health 3.23%), employer 4.51%;
  full (7,703–51,910) employee 12.17% (BL 7.00% + health 5.17%), employer 7.60%.
  (Source: btl.gov.il salaried-employee rates page, 2026.)
- **Minor / youth under 18 (קטין / נער מתחת לגיל 18):**
  reduced total 0.61%, full total 2.12% (employer-borne; no employee health line). Youth pay
  a sharply reduced BL rate and the employer carries it, a flat regular-employee rate over-deducts.
  (Source: btl.gov.il salaried-employee rates page, 2026.)
- **Working pensioner past retirement age (פנסיונר עובד מעל גיל פרישה), CRITICAL, very common:**
  this is a high-frequency Israeli payroll case (employees over 67 who keep working). Two sub-cases:
  - Receiving old-age pension (מקבל קצבת זקנה): the working-pensioner income is exempt from the
    national-insurance (BL) component and bears the **health-insurance component only**, a regular-
    employee rate badly over-deducts.
  - Ages 67–70 not yet receiving old-age pension: reduced employee ~3.93% / employer ~4.13%,
    full employee ~10.03% / employer ~6.96% (verify exact split against the current circular).
  (Source: btl.gov.il salaried-employee rates page; kolzchut "דמי ביטוח לאומי לעובד שכיר".)
- **Disability-pension recipient with annual NII certification (מקבל קצבת נכות):**
  reduced employee 3.23% / employer 0.61%; full employee 5.17% / employer 2.12%, i.e. the BL
  component is waived and only the health component is deducted from the employee.
  (Source: btl.gov.il salaried-employee rates page, 2026.)
- **Tiered application rule:** reduced rate applies only to the salary portion up to 7,703 ₪,
  full rate to the portion above; never a flat rate on the whole salary.
  (Source: National Insurance Law, reduced-collection-bracket definition, 2026 amendment.)
- **Max insurable income cap (תקרת הכנסה מבוטחת):** no BL/health on salary above 51,910 ₪/month.
  (Source: btl.gov.il, 2026.)

### Payroll income tax (מס הכנסה), the deduction, not a plug number

- Compute employee income-tax withholding from the 2026 brackets and the employee's credit
  points (נקודות זיכוי, ≈242 ₪/point/month in 2026), not a hard-coded "estimated" figure.
  Posting a guessed tax line produces a wrong net-pay and a wrong 710 liability.
  (Source: Income Tax Ordinance [New Version]; ITA annual brackets/credit-point value.)
- Recognise that the tax line on the payroll pkuda is the withheld PAYE amount remitted to the
  ITA, separate from the BL/health remitted to BTL.

### Payroll statutory provisions and their journal lines

- Mandatory pension: employee 6%, employer tagmulim 6.5%, employer severance up to 8.33%
  of pensionable salary, separate liability/fund lines.
  (Source: Extension Order for Mandatory Pension; kolzchut "חובת ביטוח פנסיוני לעובדים".)
- Keren hishtalmut (common, not statutory for all): employee 2.5% / employer 7.5%, with the
  employer exemption ceiling (≈15,712 ₪/month) above which employer KH becomes taxable benefit.
  (Source: Income Tax Ordinance / ITA keren-hishtalmut ceiling.)
- Convalescence pay (דמי הבראה / havraa): the metadata/description claims the skill handles it,
  it must therefore appear as a payroll line (per-day rate × entitled days), or be dropped from
  the description. (Source: General convalescence-pay extension order.)
- Severance fund vs. provision: distinguish the monthly 8.33% provision/deposit from a
  severance payout entry on termination.

### VAT (מע"מ)

- Output VAT on sales invoice (810), input VAT on purchase (240), kept in separate accounts
  for the bi-monthly report; clearing entry to 820. VAT 18%.
  (Source: VAT Law 5736-1976; kolzchut "מס ערך מוסף".)
- **Input-VAT deductibility by expense class** (a posting must apply the right fraction):
  passenger-car purchase 0% (blocked); car operating costs 2/3 (mainly business) or 1/4
  (mainly private); hospitality/business meals in Israel (אירוח) 0%; light refreshments
  (כיבוד קל) input VAT 2/3 (the 80% figure is the separate income-tax expense cap, not input VAT);
  standard business goods/services 100%.
  (Source: VAT Regulations reg. 14 / reg. 15A; ITA practice.)
- Cash-basis vs accrual VAT timing for services vs goods (חשבונית מס on supply vs receipt).
  (Source: VAT Law, time-of-supply rules.)

### B2B invoicing, SHAAM allocation number (חשבונית ישראל / מספר הקצאה)

- Net-amount thresholds by invoice issue date: 2025 > 20,000 ₪; Jan–May 2026 > 10,000 ₪;
  **from 01.06.2026 > 5,000 ₪** (step-down in effect). Without the allocation number the
  buyer's input VAT is not deductible at year-end, surface on any large B2B AR entry.
  (Source: ITA "חשבונית ישראל" rollout schedule; Economic Arrangements Law.)

### Depreciation (פחת)

- ITA straight-line rates: computers/software 33%, office furniture 6%, vehicles 15%,
  machinery general 7% (varies by type, e.g. tractors/self-propelled 20%), leasehold
  improvements 10%. Monthly = annual/12. Asset booked at cost excluding recoverable VAT;
  accumulated-depreciation contra account.
  (Source: Income Tax (Depreciation) Regulations 1941, tosefet bet.)

### Osek Patur (עוסק פטור)

- Single-entry (hanhala pshuta); no output/input VAT; purchases booked VAT-inclusive (VAT is a
  cost). 2026 turnover ceiling 122,833 ₪. Must still issue receipts and file the annual
  declaration; exceeding the ceiling forces a switch to Osek Murshe.
  (Source: VAT Law exempt-dealer provisions; kolzchut "עוסק פטור".)

### Withholding tax at source (ניכוי מס במקור)

- When the business PAYS a supplier subject to withholding, post the withheld amount to a
  "withholding payable" liability, net the supplier payment, unless the payee holds a valid
  exemption certificate (אישור פטור מניכוי מס במקור). Check the certificate before posting.
  (Source: Income Tax Ordinance s.164; withholding regulations by payment type.)

### Entry mechanics

- Debits = credits enforced on every pkuda. Israeli chart-of-accounts numbering (1xxx = assets,
  not US-GAAP revenue). Date / asmachta / teur fields.

---

## Should cover (advanced)

- Employer keren-hishtalmut and pension ceilings creating a taxable-benefit line when exceeded.
- Group-life / disability (ביטוח אובדן כושר) employer component within the pension 6.5%.
- Foreign-worker and Palestinian-worker payroll (different BL branches/rates).
- Vacation-pay and sick-pay accruals (חופשה / מחלה) as balance-sheet provisions.
- Reverse-charge / import VAT (רשימון יבוא) and VAT on imported services (s.15 self-invoice).
- Bituach Leumi on non-salary income and the monthly employer-report reconciliation.
- Fiscal-year-end accruals and the company tax provision (830); non-calendar fiscal years.
- Multi-currency invoices and exchange-rate differences (הפרשי שער).
- Bad-debt VAT relief (חוב אבוד) credit-note mechanics.
- Export of OPENFORMAT (קובץ אחיד / BKMV), PCN 874, Form 6111, file shapes the books feed.
- Vocational-trainee BL surcharge (raised for 2026, verify the current rate in the circular).

---

## Out of scope (explicit)

- Filing/submitting returns to ITA/BTL (the skill generates entries, it does not file).
- Annual financial-statement audit and signing (roeh heshbon territory).
- Legal tax-planning advice or ruling-dependent positions.
- Full payslip (tlush) generation with all labor-law line items beyond the bookkeeping pkuda.
- Determining an employee's exact income-tax credit-point entitlement (HR/tax-coordination task)
 , though the skill must accept it as an input rather than guess.

---

## Authoritative sources

- National Insurance Institute, salaried-employee rates: btl.gov.il/Insurance/Rates
  (page "לעובדים שכירים, שיעורי וסכומי דמי ביטוח").
- BTL employer circular, "שינוי בתשלום דמי ביטוח לאומי ודמי ביטוח בריאות לשנת 2026"
  and "אגרת למעסיק לשנת 2026" (btl.gov.il/Insurance/HozrimBituah).
- National Insurance Law [Consolidated Version] 5755-1995 (reduced-collection bracket, ceilings).
- VAT Law 5736-1976 + VAT Regulations (reg. 14/15A input-deduction blocks).
- Income Tax Ordinance [New Version], withholding (s.164), credit points, keren-hishtalmut ceiling.
- Income Tax (Depreciation) Regulations 1941.
- Israel Tax Authority, "חשבונית ישראל" allocation-number rollout (SHAAM); Form 6111; OPENFORMAT
  spec (misim.gov.il/TmbakmmsmlNew, horaot_131).
- Extension Order for Mandatory Pension; convalescence-pay extension order.
- Kol-Zchut, "דמי ביטוח לאומי לעובד שכיר", "עוסק פטור", "חובת ביטוח פנסיוני לעובדים",
  "מס ערך מוסף".
- Institute of Certified Public Accountants in Israel, annual National Insurance tables
  (icpas.org.il), for cross-checking the per-category rate rows.
