# Domain Coverage Checklist — Israeli Bank Reconciliation (התאמת בנק)

Canonical coverage contract for a skill that reconciles an Israeli business bank
account (and linked credit cards) against the accounting records. Used as the
adversarial review baseline. "Must cover" = a competent Israeli bookkeeper
performing התאמת בנק would consider its absence a correctness defect.

---

## Must cover

1. **Statement / transaction import per bank** — pull the bank side either by
   scraping (`israeli-bank-scrapers`) or by importing an exported statement, with
   correct bank identifiers and per-bank format/encoding handling.
   *Cite:* israeli-bank-scrapers `CompanyTypes` enum — https://github.com/eshaham/israeli-bank-scrapers ; Association of Banks in Israel member/bank-code list — https://www.ibank.org.il/en/

2. **Israeli date + amount parsing** — DD/MM/YYYY dates, comma/period decimal
   separators, Windows-1255/UTF-8 + BOM, semicolon CSV delimiters.
   *Cite:* Income Tax (Bookkeeping) Directives 1973 — computerized-records amendment (Circular 24/2004) requires legible, reconstructible computerized records — https://www.gov.il/he/departments/israel_tax_authority

3. **Matching strategies** — exact (reference + amount), fuzzy (date window +
   amount tolerance + payee similarity), recurring-pattern, AND standing-order
   detection (הוראת קבע / הו"ק): stable amount on the same day each month from the
   same payee.
   *Cite:* Bank of Israel Proper Conduct of Banking Business / payment standards — https://www.boi.org.il/en/economic-roles/supervision-and-regulation/ (standing orders are a regulated, named debit instrument)

4. **Three-bucket categorization** — matched / unmatched-bank / unmatched-books,
   with the unmatched-bank bucket split into "missing invoice" (investigate vs.
   create a document) vs. "bank-originated entry" (post a journal entry).
   *Cite:* Income Tax (Bookkeeping) Directives 1973 — every entry must trace to a
   supporting document or journal entry — https://www.nevo.co.il/law_html/law01/255_179.htm

5. **Bank fees + debit interest (עמלות + ריבית חובה)** — bank-originated charges
   that have no invoice and must be posted to the books, not chased. Debit
   interest (ריבית חובה) on overdraft is its own line distinct from credit
   interest.
   *Cite:* Bank of Israel banking-fees regulation (תעריפון עמלות / כללי הבנקאות (שירות ללקוח)) — https://www.boi.org.il/en/economic-roles/supervision-and-regulation/

6. **Outstanding checks vs. deposits in transit (המחאות שטרם נפרעו / הפקדות בדרך)** —
   timing differences that must be listed explicitly in a reconciliation bridge
   so the book balance and bank balance tie out to zero.
   *Cite:* standard bank-reconciliation procedure; Income Tax (Bookkeeping)
   Directives 1973 reconciliation requirement — https://www.nevo.co.il/law_html/law01/255_179.htm

7. **Post-dated checks (שיקים דחויים / המחאות דחויות)** — written/received now but
   dated in the future; a distinct reconciling item that rolls forward by due
   date until it clears, separate from ordinary outstanding checks. Both received
   (from customers) and issued (to vendors).
   *Cite:* common Israeli commercial practice (שיק דחוי is a standard instrument);
   Checks Without Cover Law context — https://www.gov.il/he/departments/israel_tax_authority

8. **Reconciliation bridge + cumulative roll-forward** — produce an explicit
   bridge (book balance ± reconciling items = bank balance), and carry unresolved
   reconciling items forward into the next period's opening reconciliation.
   *Cite:* standard period-close reconciliation; bookkeeping directive
   reconstructibility — https://www.nevo.co.il/law_html/law01/255_179.htm

9. **Foreign-currency valuation (שער יציג)** — value foreign-currency book entries
   at the Bank of Israel representative rate for the date; the gap to the bank's
   actual conversion rate is a real FX gain/loss, not an unexplained discrepancy.
   *Cite:* Bank of Israel representative exchange rates + explanatory notes —
   https://www.boi.org.il/en/economic-roles/financial-markets/explanatory-notes-to-the-representative-exchange-rates/

10. **Credit-card settlement matching** — card-company charges (Isracard, Cal,
    Max) hit the bank as a lump-sum settlement, not per-purchase; reconcile the
    settlement total, and reconcile the card statement separately against the
    purchase ledger.
    *Cite:* Income Tax (Bookkeeping) Directives 1973 — credit-card settlement
    documents must be retained as part of the books — https://www.nevo.co.il/law_html/law01/255_179.htm

11. **Record retention (ניהול ספרים — 7 years)** — bank statements, reconciliation
    reports, and supporting documents must be kept 7 years from the end of the tax
    year, or 6 years from the date the return was filed, whichever is later.
    *Cite:* Income Tax (Bookkeeping) Directives 1973, issued under §130 of the
    Income Tax Ordinance — https://www.nevo.co.il/law_html/law01/255_179.htm ;
    overview — https://www.kolzchut.org.il/he/ניהול_ספרי_החשבונות_של_העסק

12. **Reconciliation cadence** — reconcile at least monthly (period close), and at
    year-end before the annual tax return; tie the cadence to closing/VAT-period
    boundaries.
    *Cite:* Israel Tax Authority bookkeeping + VAT reporting periodicity —
    https://www.gov.il/he/departments/israel_tax_authority

---

## Should cover

1. **Suspicious-item flagging** — duplicate amounts same date, oversized
   transactions, weekend/holiday postings (Sun–Thu business week, Israeli
   calendar).
   *Cite:* Israeli banking business week is Sunday–Thursday — https://www.boi.org.il/en/economic-roles/supervision-and-regulation/

2. **Check float / clearing period** — 1–3 business-day clearing creates timing
   mismatches between bank date and recorded date.
   *Cite:* Israeli check-clearing practice — https://www.boi.org.il/en/economic-roles/supervision-and-regulation/

3. **VAT reconciliation tie-out (מע"מ)** — bank amounts are VAT-inclusive while the
   ledger may split net + VAT; current VAT rate is 18% (since 1 Jan 2025). A
   systematic ~18%/15.25% gap signals a VAT split mismatch, not an error.
   *Cite:* Israel Tax Authority VAT rate 18% from 2025-01-01 — https://www.gov.il/he/departments/israel_tax_authority

4. **Installment splits (תשלומים)** — a single bank/card charge may correspond to
   multiple booked installment rows (or vice versa); reconcile the split.
   *Cite:* credit-card installment practice; israeli-bank-scrapers
   `combineInstallments` option — https://github.com/eshaham/israeli-bank-scrapers

5. **Credential / secrets hygiene** — never hardcode bank credentials; use env
   vars; respect OTP/2FA scraper config.
   *Cite:* israeli-bank-scrapers security guidance — https://github.com/eshaham/israeli-bank-scrapers

6. **MCP / data-source abstraction** — prefer an MCP transaction source when
   available, fall back to the scraper script.
   *Cite:* skill architecture choice (no external authority needed)

---

## Out of scope

- International (non-Israeli) bank accounts.
- Cryptocurrency wallets / on-chain reconciliation.
- Investment-portfolio / securities reconciliation.
- Full double-entry ledger posting (the skill flags what to post; the GL system
  records it).
- Payroll-specific reconciliation (separate domain).
- Tax-return preparation itself (the skill feeds it; does not file).

---

## Authoritative sources

- Income Tax (Bookkeeping) Directives, 1973 (הוראות מס הכנסה (ניהול פנקסי חשבונות), תשל"ג-1973) — https://www.nevo.co.il/law_html/law01/255_179.htm
- Israel Tax Authority (bookkeeping + VAT) — https://www.gov.il/he/departments/israel_tax_authority
- Kol-Zchut — keeping the business's books (retention overview) — https://www.kolzchut.org.il/he/ניהול_ספרי_החשבונות_של_העסק
- Bank of Israel — supervision & regulation (Proper Conduct, fees, payments) — https://www.boi.org.il/en/economic-roles/supervision-and-regulation/
- Bank of Israel — representative exchange rates (explanatory notes) — https://www.boi.org.il/en/economic-roles/financial-markets/explanatory-notes-to-the-representative-exchange-rates/
- Association of Banks in Israel — https://www.ibank.org.il/en/
- israeli-bank-scrapers — https://github.com/eshaham/israeli-bank-scrapers
