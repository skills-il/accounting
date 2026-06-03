# Domain Checklist: Israeli Financial Reports

Scope: producing financial statements (P&L, balance sheet, trial balance, cash flow) and VAT
summary reports for Israeli osek patur / osek murshe / chevra. Used to grade whether the skill's
output would be CORRECT and submission-appropriate for a real small business or small company.

## Must cover (statutory correctness, getting these wrong produces a wrong/non-compliant output)

1. **Correct VAT filing cadence threshold.** Monthly vs bi-monthly is set by annual turnover.
   For 2026 the threshold is **1,775,000 NIS** (up to that figure → bi-monthly; above → monthly).
   (2025 was 1,725,000 NIS.) A hardcoded 1.5M figure mislabels every business between ~1.5M and
   1.775M as a monthly filer.
   Source: https://www.kolzchut.org.il/he/הגשת_דוחות_תקופתיים_ותשלום_מס_ערך_מוסף ; gov.il VAT reporting service.
2. **Correct VAT due dates.** Paper: 15th of following month. Online (mekuvan): 19th. Detailed
   (PCN874) filers: 23rd.
   Source: https://www.gov.il/he/service/reporting-or-payment-of-vat-reports
3. **Correct standard VAT rate.** 18% since January 2025.
   Source: https://www.gov.il/he/pages/vat-rate-amount-new
4. **Osek patur identification + ceiling + obligation.** 2026 ceiling 122,833 NIS; files an annual
   declaration (הצהרת עוסק פטור) by 31 January, NOT periodic VAT reports; exceeding ceiling forces
   conversion to osek murshe. Must NOT produce a VAT-payable report for an osek patur.
   Source: https://www.kolzchut.org.il/he/עוסק_פטור
5. **Correct accounting-standards regime.** Full IFRS mandatory only for entities under the
   Securities Law (public/listed); private companies may use Israeli GAAP or IFRS; SMEs may use
   IFRS for SMEs. Must not claim "Israel uses IFRS" flatly.
   Source: https://www.ifrs.org/use-around-the-world/use-of-ifrs-standards-by-jurisdiction/view-jurisdiction/israel/
6. **Correct corporate tax rate for chevra.** 23% in 2026.
   Source: https://taxsummaries.pwc.com/israel/corporate/taxes-on-corporate-income
7. **Form 6111 as the real submission vehicle for statement figures.** Mandatory online when annual
   turnover > 300,000 NIS incl. VAT; three sections (balance sheet, P&L, tax-adjustment report).
   Source: https://www.gov.il/he/service/itc6111
8. **Trial balance must balance (debits = credits) before deriving statements.**
   Source: standard double-entry accounting (Israeli Income Tax bookkeeping directives, הוראות ניהול ספרים).

## Should cover (improves correctness / completeness, but absence won't actively mislead a filer)

1. **PCN874 detailed-reporting scope.** Self-employed > 500,000 NIS from 1.1.2026; companies/
   partnerships with corporate partner since 9/2025; per-invoice detail (serial no., date, amount,
   VAT, counterparty registration number); 23rd deadline. Small-invoice de-minimis relief
   (invoices < 5,000 NIS pre-VAT may be aggregated, with total stated) is a real easing worth noting.
   Source: https://www.gov.il/he/service/detailed-vat-reporting ; https://www.amir-cpa.net/post/דיווח-מפורט-למע-מ-לעצמאי-מ-2026-חובות-והקלות
2. **Whether becoming a detailed filer changes cadence.** Sources conflict: some (amir-cpa) say a
   self-employed detailed filer moves from bi-monthly to monthly; gov.il notices reference bi-monthly
   detailed periods (ינו-פבר 2026). The skill should hedge this rather than assert monthly flatly.
   Source: https://www.gov.il/he/pages/pa280825-1 (bi-monthly) vs amir-cpa (monthly).
3. **Income-tax brackets + mas yasaf for non-corporate owners.** Profit of osek/sole prop flows to
   personal brackets; pull live figures, don't hardcode. Surtax applies above the high-income threshold.
   Source: https://www.kolzchut.org.il/he/מדרגות_מס_הכנסה
4. **Advance tax payments (מקדמות מס הכנסה).** Most osek murshe / chevra pay monthly/bi-monthly
   income-tax advances as a percentage of turnover, a periodic obligation alongside VAT that a
   reporting skill should at least name so the user isn't surprised.
   Source: https://www.gov.il/he/departments/israel_tax_authority (advance-payments service).
5. **National Insurance (ביטוח לאומי) for the self-employed.** Periodic obligation distinct from
   VAT/income tax; out of statement scope but adjacent for a "periodic reports" skill.
   Source: https://www.btl.gov.il
6. **Bilingual term precision** (revach golmi / tifuli / naki) and RTL balance-sheet layout.

## Out of scope (correctly excluded by the skill)

- Actual VAT/tax filing submission (the skill says "Do NOT use for tax filing submissions").
- Payroll processing and bank reconciliation (explicitly excluded).
- Audit opinion issuance / statutory audit sign-off.
- Detailed depreciation schedules and tax-depreciation rates (תקנות פחת).

## Authoritative sources

- Israel Tax Authority: VAT reporting/payment: https://www.gov.il/he/service/reporting-or-payment-of-vat-reports
- Israel Tax Authority: VAT amounts & rates: https://www.gov.il/he/pages/vat-rate-amount-new
- Israel Tax Authority: detailed VAT (PCN874): https://www.gov.il/he/service/detailed-vat-reporting
- Israel Tax Authority: Form 6111: https://www.gov.il/he/service/itc6111
- Kol Zchut: periodic VAT reporting (cadence threshold): https://www.kolzchut.org.il/he/הגשת_דוחות_תקופתיים_ותשלום_מס_ערך_מוסף
- Kol Zchut: osek patur: https://www.kolzchut.org.il/he/עוסק_פטור
- Kol Zchut: income-tax brackets: https://www.kolzchut.org.il/he/מדרגות_מס_הכנסה
- IFRS Foundation: Israel jurisdiction profile: https://www.ifrs.org/use-around-the-world/use-of-ifrs-standards-by-jurisdiction/view-jurisdiction/israel/
- ICPAS (לשכת רואי חשבון בישראל): https://www.icpas.org.il
- National Insurance Institute: https://www.btl.gov.il
