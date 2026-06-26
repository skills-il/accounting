# Domain Coverage Checklist: Israeli Small-Business Bookkeeping Sheet

Canonical coverage contract for a skill that builds a Google Sheets income/expense
bookkeeping tracker for an Israeli freelancer or small business. Used to judge whether
the skill covers what a competent Israeli CPA would expect, and to keep frozen
facts in sync on each update.

Currency is NIS (ש"ח). All thresholds are as of 2026 unless noted. Verify any
contested figure against the authoritative source before relying on it.

---

## Must (a correct bookkeeping sheet for Israel cannot omit these)

- **Income vs. expense tracking** with date, description, amount, category, type
  (income/expense), and an invoice/reference number. Source: Income Tax Regulations
  (Bookkeeping) 1973 — record-keeping for the self-employed.
  https://www.kolzchut.org.il/he/%D7%A0%D7%99%D7%94%D7%95%D7%9C_%D7%A1%D7%A4%D7%A8%D7%99_%D7%94%D7%97%D7%A9%D7%91%D7%95%D7%A0%D7%95%D7%AA_%D7%A9%D7%9C_%D7%94%D7%A2%D7%A1%D7%A7
- **VAT rate 18%** (since 1 January 2025; previously 17%). Net / VAT / gross columns
  for an osek murshe. Source: Israel Tax Authority / CPA pages.
  https://www.gov.il/he/departments/israel_tax_authority
- **Osek patur vs. osek murshe distinction**, driving sheet structure: osek patur
  does not charge or reclaim VAT; osek murshe does. Patur ceiling NIS 120,000 (2025) /
  NIS 122,833 (2026), CPI-linked; some professions must register murshe regardless.
  https://www.kolzchut.org.il/he/%D7%A2%D7%95%D7%A1%D7%A7_%D7%A4%D7%98%D7%95%D7%A8
- **Bi-monthly VAT reporting periods** (6 periods, due the 15th of the following
  month), NOT quarterly. Source: Tax Authority VAT reporting schedule.
  https://www.gov.il/he/departments/israel_tax_authority
- **Monthly-VAT filer exception**: turnover over ~NIS 2.5M files VAT monthly, not
  bi-monthly. https://keep.co.il/blog/nihul-maam-2026.html
- **חשבונית מס (tax invoice) requirements** and the sheet-vs-legal-invoice boundary:
  the sheet is a tracking record; the legal invoice is issued by approved software.
  Required fields: header, running number, seller name + business/VAT ID, customer
  name (+ ID above threshold), date, description, pre-VAT / VAT / total.
- **מספר הקצאה (allocation number)** under the Israel Invoice CTC mandate: required on
  tax invoices >= NIS 10,000 (before VAT) from 1 Jan 2026, dropping to >= NIS 5,000
  from 1 Jun 2026; without it the buyer cannot deduct input VAT. Capture it in a column.
  https://www.greeninvoice.co.il/magazine/israel-invoice/
- **Deductible-expense categories with the caps that actually differ from 100%**:
  meals & hospitality 80%; car/vehicle ~45% (or fixed, lower of); phone/internet/home
  office proportional to business use. Full-rate categories (rent, equipment,
  professional services, software, marketing, insurance, travel) at 100%.
  https://www.kolzchut.org.il/he/%D7%94%D7%95%D7%A6%D7%90%D7%94_%D7%9E%D7%95%D7%9B%D7%A8%D7%AA_%D7%9C%D7%A6%D7%95%D7%A8%D7%9A_%D7%97%D7%99%D7%A9%D7%95%D7%91_%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94_(%D7%94%D7%95%D7%A6%D7%90%D7%94_%D7%9E%D7%95%D7%AA%D7%A8%D7%AA_%D7%91%D7%A0%D7%99%D7%9B%D7%95%D7%99)
- **DD/MM/YYYY date format** (not US MM/DD/YYYY) — affects every dated row and the
  period filter logic.
- **Bookkeeping retention period**: books and supporting documents must be kept
  **7 years** from the end of the tax year (or 6 years from filing the return,
  whichever is later). A bookkeeping skill must state this so users do not discard
  receipts early. Source: Income Tax Regulations (Bookkeeping) 1973, ITA circular.
  https://www.greeninvoice.co.il/magazine/accounting/saving_invoices/

## Should (a competent CPA would expect these; their absence is a gap, not a defect)

- **ניכוי במקור (withholding tax at source)** column: some payers must withhold income
  tax and pay net; the business needs its own אישור ניכוי מס במקור (withholding-rate
  certificate). Track withheld amounts so they can be credited against the annual
  income-tax liability and reconciled with the payer's Form 856.
  https://www.kolzchut.org.il/he/%D7%A0%D7%99%D7%9B%D7%95%D7%99_%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94_%D7%91%D7%9E%D7%A7%D7%95%D7%A8_%D7%A2%D7%9C-%D7%99%D7%93%D7%99_%D7%9C%D7%A7%D7%95%D7%97_%D7%A9%D7%9C_%D7%A2%D7%A1%D7%A7_%D7%A2%D7%A6%D7%9E%D7%90%D7%99
- **Form 856** (annual supplier/non-salary withholding return, due ~31 March / 30 April
  of the following year): the withholding column feeds the payer's 856; the receiving
  business uses 856 certificates to claim credit. Distinguish from Form 126.
  https://www.gov.il/he/service/report126
- **Equipment / depreciation (פחת)** handling: low-value assets (commonly cited
  threshold ~NIS 1,700, historically ~NIS 1,200 in older guidance) may be expensed in
  year 1; assets above it are depreciable (e.g. computers 33%/yr) and should not be
  fully expensed when bought. A bookkeeping sheet should at least flag equipment as a
  depreciable asset rather than a 100% same-year expense.
  https://www.kolzchut.org.il/he/%D7%94%D7%95%D7%A6%D7%90%D7%94_%D7%9E%D7%95%D7%9B%D7%A8%D7%AA_%D7%9C%D7%A6%D7%95%D7%A8%D7%9A_%D7%97%D7%99%D7%A9%D7%95%D7%91_%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94_(%D7%94%D7%95%D7%A6%D7%90%D7%94_%D7%9E%D7%95%D7%AA%D7%A8%D7%AA_%D7%91%D7%A0%D7%99%D7%9B%D7%95%D7%99)
- **Osek zair (micro-dealer) 2026 track**: automatic 30% expense deduction off turnover
  with no receipt itemization, simplified annual report, no advance payments; ceiling
  CPI-linked (~NIS 122,833 for 2026). Confirm eligibility with accountant before opting in.
  https://www.gov.il/he/pages/sa090523-2
- **מקדמות מס הכנסה (income-tax advance payments)** cadence in the tax calendar — a CPA
  expects the sheet/summary to support the periodic advance-payment basis (% of turnover).
- **Gifts and other capped non-100% items** (e.g. business gifts capped at NIS 220
  per recipient/year; fines and penalties non-deductible).
- **Foreign-currency conversion** via Bank of Israel representative rates for any
  non-NIS transaction. https://www.boi.org.il/roles/markets/exchangerates/

## Out of scope (correctly excluded; a sheet skill should NOT do these)

- **Payroll processing and Form 126** (annual employer salary-withholding reconciliation):
  126 only applies to a business with employees; a freelancer income/expense sheet is
  not a payroll system. Naming it as context is fine; building it is out of scope.
- **Filing returns with the Tax Authority** (VAT report submission, annual income-tax
  return submission) — the sheet prepares data for the accountant, it does not file.
- **Direct bank-API / open-banking integrations.**
- **Bituach Leumi (National Insurance) contribution calculation** — related but a
  separate computation; mentioning it is a bonus, not required.
- **Issuing the legal invoice itself** — done by Morning/iCount/Rivhit/approved software,
  not by the sheet.

## Authoritative sources

- Israel Tax Authority (VAT rate, patur ceiling, allocation thresholds, schedules):
  https://www.gov.il/he/departments/israel_tax_authority
- Bookkeeping regulations + retention (Income Tax Regulations (Bookkeeping) 1973):
  https://www.kolzchut.org.il/he/%D7%A0%D7%99%D7%94%D7%95%D7%9C_%D7%A1%D7%A4%D7%A8%D7%99_%D7%94%D7%97%D7%A9%D7%91%D7%95%D7%A0%D7%95%D7%AA_%D7%A9%D7%9C_%D7%94%D7%A2%D7%A1%D7%A7
- Retention period (7 years): https://www.greeninvoice.co.il/magazine/accounting/saving_invoices/
- Osek patur / murshe: https://www.kolzchut.org.il/he/%D7%A2%D7%95%D7%A1%D7%A7_%D7%A4%D7%98%D7%95%D7%A8
- Israel Invoice / allocation number: https://www.greeninvoice.co.il/magazine/israel-invoice/
- Withholding at source + Form 856: https://www.kolzchut.org.il/he/%D7%A0%D7%99%D7%9B%D7%95%D7%99_%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94_%D7%91%D7%9E%D7%A7%D7%95%D7%A8_%D7%A2%D7%9C-%D7%99%D7%93%D7%99_%D7%9C%D7%A7%D7%95%D7%97_%D7%A9%D7%9C_%D7%A2%D7%A1%D7%A7_%D7%A2%D7%A6%D7%9E%D7%90%D7%99
- Forms 126/856 (Tax Authority): https://www.gov.il/he/service/report126
- Deductible expenses + caps: https://www.kolzchut.org.il/he/%D7%94%D7%95%D7%A6%D7%90%D7%94_%D7%9E%D7%95%D7%9B%D7%A8%D7%AA_%D7%9C%D7%A6%D7%95%D7%A8%D7%9A_%D7%97%D7%99%D7%A9%D7%95%D7%91_%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94_(%D7%94%D7%95%D7%A6%D7%90%D7%94_%D7%9E%D7%95%D7%AA%D7%A8%D7%AA_%D7%91%D7%A0%D7%99%D7%9B%D7%95%D7%99)
- Osek zair reform: https://www.gov.il/he/pages/sa090523-2
- Bank of Israel exchange rates: https://www.boi.org.il/roles/markets/exchangerates/
