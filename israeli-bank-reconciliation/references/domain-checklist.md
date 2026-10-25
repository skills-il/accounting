# Domain Coverage Checklist: Israeli Bank Reconciliation (התאמת בנק)

Canonical coverage contract for a skill that reconciles an Israeli business bank
account (and linked credit cards) against the accounting records. Used as the
adversarial review baseline. "Must cover" = a competent Israeli bookkeeper
performing התאמת בנק would consider its absence a correctness defect.

---

## Must cover

1. **Statement / transaction import per bank**, pull the bank side either by
   scraping (`israeli-bank-scrapers`) or by importing an exported statement, with
   correct bank identifiers and per-bank format/encoding handling.
   *Cite:* israeli-bank-scrapers `CompanyTypes` enum, https://github.com/eshaham/israeli-bank-scrapers ; Association of Banks in Israel member/bank-code list, https://www.ibank.org.il/en/

2. **Israeli date + amount parsing**, DD/MM/YYYY dates, comma/period decimal
   separators, Windows-1255/UTF-8 + BOM, semicolon CSV delimiters.
   *Cite:* Income Tax (Bookkeeping) Directives 1973, computerized-records amendment (Circular 24/2004) requires legible, reconstructible computerized records, https://www.gov.il/he/departments/israel_tax_authority

3. **Matching strategies**, reference first, then exact (date + amount), fuzzy
   (date window + amount tolerance + payee similarity), grouped, and
   recurring-debit detection by PAYEE (a line labelled הוראת קבע / הו"ק may be a
   debit under an authorisation or a standing transfer; confirm the type before
   applying Directive 439 rights).
   *Cite:* BOI Proper Conduct Directive 439 (debits under an authorisation),
   https://boi.org.il/media/opue4bvf/439.pdf ; see `matching-rules.md`

4. **Three-bucket categorization**, matched / unmatched-bank / unmatched-books,
   with the unmatched-bank bucket split into "missing invoice" (investigate vs.
   create a document) vs. "bank-originated entry" (post a journal entry).
   *Cite:* Income Tax (Bookkeeping) Directives 1973, every entry must trace to a
   supporting document or journal entry, https://www.nevo.co.il/law_html/law01/255_179.htm

5. **Bank fees + debit interest (עמלות + ריבית חובה)**, bank-originated charges
   that have no invoice and must be posted to the books, not chased. Debit
   interest (ריבית חובה) on overdraft is its own line distinct from credit
   interest.
   *Cite:* Bank of Israel banking-fees regulation (תעריפון עמלות / כללי הבנקאות (שירות ללקוח)), https://www.boi.org.il/en/economic-roles/supervision-and-regulation/

6. **Outstanding checks vs. deposits in transit (המחאות שטרם נפרעו / הפקדות בדרך)** ,
   timing differences that must be listed explicitly in a reconciliation bridge
   so the book balance and bank balance tie out to zero.
   *Cite:* standard bank-reconciliation procedure; Income Tax (Bookkeeping)
   Directives 1973 reconciliation requirement, https://www.nevo.co.il/law_html/law01/255_179.htm

7. **Post-dated checks (שיקים דחויים / המחאות דחויות)**, written/received now but
   dated in the future; a distinct reconciling item that rolls forward by due
   date until it clears, separate from ordinary outstanding checks. Both received
   (from customers) and issued (to vendors).
   *Cite:* common Israeli commercial practice (שיק דחוי is a standard instrument);
   Checks Without Cover Law context, https://www.gov.il/he/departments/israel_tax_authority

8. **Reconciliation bridge + cumulative roll-forward**, produce an explicit
   bridge (book balance ± reconciling items = bank balance), and carry unresolved
   reconciling items forward into the next period's opening reconciliation.
   *Cite:* standard period-close reconciliation; bookkeeping directive
   reconstructibility, https://www.nevo.co.il/law_html/law01/255_179.htm

9. **Foreign-currency valuation (שער יציג)**, value foreign-currency book entries
   at the Bank of Israel representative rate for the date; the gap to the bank's
   actual conversion rate is a real FX gain/loss, not an unexplained discrepancy.
   *Cite:* Bank of Israel representative exchange rates + explanatory notes ,
   https://www.boi.org.il/en/economic-roles/financial-markets/explanatory-notes-to-the-representative-exchange-rates/

10. **Credit-card settlement matching**, card-company charges (Isracard, Cal,
    Max) hit the bank as a lump-sum settlement, not per-purchase; reconcile the
    settlement total, and reconcile the card statement separately against the
    purchase ledger.
    *Cite:* Income Tax (Bookkeeping) Directives 1973, credit-card settlement
    documents must be retained as part of the books, https://www.nevo.co.il/law_html/law01/255_179.htm

11. **Record retention (ניהול ספרים, 7 years)**, bank statements, reconciliation
    reports, and supporting documents must be kept 7 years from the end of the tax
    year, or 6 years from the date the return was filed, whichever is later.
    *Cite:* Income Tax (Bookkeeping) Directives 1973, issued under §130 of the
    Income Tax Ordinance, https://www.nevo.co.il/law_html/law01/255_179.htm ;
    overview, https://www.kolzchut.org.il/he/ניהול_ספרי_החשבונות_של_העסק

12. **Reconciliation cadence**, reconcile at least monthly (period close), and at
    year-end before the annual tax return; tie the cadence to closing/VAT-period
    boundaries: bi-monthly for an osek murshe with turnover up to NIS 1,775,000,
   monthly above it, annual declaration for an osek patur.
   *Cite:* VAT Law s.67(a2)(1) and the VAT (Registration) Regulations reg.15,
   https://he.wikisource.org/wiki/חוק_מס_ערך_מוסף ; see `vat-and-fx-rules.md`

---

## Should cover

1. **Suspicious-item flagging**, duplicate amounts same date, oversized
   transactions, Saturday/holiday postings. Banks and ZAHAV work Sunday to
   Friday, with Friday a short day ending 14:00; only the TASE moved to
   Monday to Friday (5 January 2026).
   *Cite:* Banking (Customer Service) rules on cheque credit and debit timing
   (definition of a banking business day), https://he.wikisource.org/wiki/הוראות_הבנקאות_(שירות_ללקוח)_(מועד_זיכוי_וחיוב_בשיקים) ;
   see `period-close.md`

2. **Cheque clearing and reversal**, credit on the clearing day is provisional
   for three further banking business days; a returned cheque re-opens a prior
   match. The rules do not key the credit day on deposit channel; a bank may set
   an earlier cut-off for a branch or deposit type on notice.
   *Cite:* same rules, s.2(a) and s.3(a); see `period-close.md`

3. **VAT reconciliation tie-out (מע"מ)**, bank amounts are VAT-inclusive while the
   ledger may split net + VAT; VAT rate is 18% since 1 Jan 2025 and was 17% before. A
   systematic ~18%/15.25% gap signals a VAT split mismatch, not an error.
   *Cite:* Israel Tax Authority VAT rate 18% from 2025-01-01, https://www.gov.il/he/departments/israel_tax_authority

4. **Installment splits (תשלומים)**, a single bank/card charge may correspond to
   multiple booked installment rows (or vice versa); reconcile the split.
   *Cite:* credit-card installment practice; israeli-bank-scrapers
   `combineInstallments` option, https://github.com/eshaham/israeli-bank-scrapers

5. **Credential / secrets hygiene**, never hardcode bank credentials; use env
   vars; respect OTP/2FA scraper config.
   *Cite:* israeli-bank-scrapers security guidance, https://github.com/eshaham/israeli-bank-scrapers

6. **MCP / data-source abstraction**, prefer an MCP transaction source when
   available, fall back to the scraper script.
   *Cite:* skill architecture choice (no external authority needed)

7. **Direct debit (חיוב על פי הרשאה) vs standing order**, variable amount,
   cancellable by the customer within 3 business days after the debit.
   *Cite:* BOI Proper Conduct Directive 439, https://boi.org.il/media/opue4bvf/439.pdf

8. **Allocation number per invoice, dated threshold table, short form of the 9 rightmost digits (full number up to 30 characters).**
   *Cite:* VAT Law s.38(a1), s.47(a2)(1); see `vat-and-fx-rules.md`

9. **Scraper history window and sign-off, ageing and materiality.**
   *Cite:* israeli-bank-scrapers README; see `period-close.md`

10. **Consequences of a missing allocation number and of a late invoice**: the
    income-tax disallowance of the expense (Ordinance s.32(18), from 1.8.2025),
    the late-request route (VAT Law s.47(a2)(4)), and the six-month input-VAT
    window (s.38(a)); only a tax invoice issued to the dealer supports the
    deduction.
    *Cite:* https://he.wikisource.org/wiki/חוק_מס_ערך_מוסף ; https://he.wikisource.org/wiki/פקודת_מס_הכנסה

11. **Receipts side**: an unmatched credit may be unreported output VAT; payments
    net of income tax withheld at source; card-acquirer settlements net of the
    clearing fee and in installment tranches.
    *Cite:* structural; see `matching-rules.md`

---

## Out of scope

- International (non-Israeli) bank accounts.
- Cryptocurrency wallets / on-chain reconciliation.
- Investment-portfolio / securities reconciliation.
- Full double-entry ledger posting (the skill flags what to post; the GL system
  records it).
- Payroll-specific reconciliation (separate domain).
- Tax-return preparation itself (the skill feeds it; does not file).
- Auditing bank fees against the regulated tariff, including the reduced
  small-business schedule (reviewed 2026-10-25: a user may ask "was this fee
  right?", but the reconciliation's job is to post the fee the bank actually
  took; challenging a fee is a consumer-dispute workflow, handled by
  `israeli-consumer-fee-fighter`).
- A general income-tax rule for translating foreign-currency entries for an
  ordinary business (reviewed 2026-10-25: no primary text could be verified;
  the skill names only the elective 1986 dollar regulations and routes the
  question to the accountant).
- Payer-side withholding compliance (whether the user withheld and remitted tax
  on payments to suppliers): a withholding workflow, not a bank reconciliation
  (reviewed 2026-10-25; the receipts side, payments received net of
  withholding, IS covered).
- Re-litigated 2026-10-25, all rows above stay out of scope: none is a question
  a reconciliation user ordinarily asks of this tool, and none became
  capturable.

---

## Authoritative sources

- Income Tax (Bookkeeping) Directives, 1973 (הוראות מס הכנסה (ניהול פנקסי חשבונות), תשל"ג-1973), https://www.nevo.co.il/law_html/law01/255_179.htm
- Israel Tax Authority (bookkeeping + VAT), https://www.gov.il/he/departments/israel_tax_authority
- Kol-Zchut, keeping the business's books (retention overview), https://www.kolzchut.org.il/he/ניהול_ספרי_החשבונות_של_העסק
- Bank of Israel, supervision & regulation (Proper Conduct, fees, payments), https://www.boi.org.il/en/economic-roles/supervision-and-regulation/
- Bank of Israel, representative exchange rates (explanatory notes), https://www.boi.org.il/en/economic-roles/financial-markets/explanatory-notes-to-the-representative-exchange-rates/
- Association of Banks in Israel, https://www.ibank.org.il/en/
- israeli-bank-scrapers, https://github.com/eshaham/israeli-bank-scrapers
