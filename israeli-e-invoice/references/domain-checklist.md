# Domain Coverage Checklist, israeli-e-invoice

Generated: 2026-09-15 by a fresh-context research subagent (update-skill Phase 5.8 bootstrap), then reviewed by the updating agent. Rows the subagent could not confirm on a primary source are marked (unverified). The Tax Authority Israel-Invoice FAQ (gov.il) blocked the author's WebFetch, curl and browser attempts, but the independent Judge read it in a browser on 2026-09-15 with the URL asserted. The FAQ is administrative guidance and is not used as the rule; the skill follows the statute.

## Must cover (core)

### Threshold schedule (VAT Law s.38(א1), accelerated schedule)

- [ ] M1 Pilot year 2024: every invoice receives an allocation number except for technical errors. Source: ITA API Description v2.0 (7.2024) s.1.1.1.
- [ ] M2 From May 2024: invoice amount before VAT above NIS 25,000 (exact start day 4 May 2024 unverified). Source: API doc s.1.2; Green Invoice.
- [ ] M3 From 1 Jan 2025: above NIS 20,000. Source: API doc s.1.2; Green Invoice.
- [ ] M4 From 1 Jan 2026: above NIS 10,000 (accelerated). The API doc's original 2026/2027/2028 table (15,000 / 10,000 / 5,000) is SUPERSEDED and must not be used. Source: Green Invoice; API doc s.1.2.
- [ ] M5 From 1 Jun 2026 (in force): above NIS 5,000 before VAT. Source: VAT Law s.38(א1) on Nevo; Grant Thornton Israel; Ziv-Weinstein CPA.
- [ ] M6 Test basis: the statute (s.38(א1), s.47(א2)(1)) tests the amount before VAT only. VAT-amount figures and a mixed-invoice relief appear only in the ITA FAQ (read 2026-09-15). They are administrative guidance, not in the statute, and are NOT used in the skill.
- [ ] M7 Temporal rule: which date selects the threshold. Sources key on the invoice issue date ("שתוצא החל מיום 1.6.2026"). A tax-point or transaction-date override is (unverified). The API carries both invoice_date and invoice_issuance_date; which governs is not stated.
- [ ] M8 Conditions for the duty (API doc s.1.2): amount before VAT above the threshold; non-zero VAT; the customer is an osek murshe; the customer requested a number. A number may be requested for any amount.
- [ ] M9 No lawful allocation number means the buyer cannot deduct input tax. Source: s.38(א1).

### Document types (API doc Table 2.5)

- [ ] M10 300 transaction invoice: no number.
- [ ] M11 305 tax invoice, 310 periodic, 320 tax invoice/receipt, 340 reservation: number.
- [ ] M12 330 credit tax invoice: no number.
- [ ] M13 332 pro forma: number under spec article 3.5 (cash-basis) only.
- [ ] M14 345 agent tax invoice and 348 log command: allocation Yes. Source: ITA API spec v2.0 Table 2.5 (evidence shaam-document-type-codes-table-2-5, verified 2026-09-15).
- [ ] M15 Receipts, self-invoices, exempt-dealer documents: no number (secondary source).

### SHAAM API

- [ ] M16 v2 sandbox and production Approval endpoints on ita-api.taxes.gov.il; v1 ended 31/12/2024. Source: API doc s.1.1.2, s.2.3.
- [ ] M17 OAuth2 "User Restricted". Token lifetime and renewal: vendor sources report a three-month connection validity (unverified on an ITA source).
- [ ] M18 Mandatory v2 fields, lowercase names (API Table 2.1), including invoice_reference_number; reverse charge sends action=3 with VAT 0.
- [ ] M19 Print the 9 right-most digits under "Allocation Number"; report them in PCN874. Source: API doc s.2.2.1.

### Refusals and failures

- [ ] M20 Held invoice, four documented choices reported through the decision service: revoke; continue without a number with the printed caption; reverse charge with the customer's consent (same invoice_id, action=3, special number); hearing via the portal. Source: API doc s.2.2.2.
- [ ] M21 Hearing and objection timetable: hearing within 2 business days of the online notice, decision within 1 business day or deemed approved, objection within 30 days of the hearing, decision within 21 business days or deemed accepted, then appeal to the District Court. Source: VAT Law s.47(a2)(3)(b) and s.47(a4)(4) to (6) on Nevo (evidence refusal-hearing-timetable).
- [ ] M22 Outage handling: emergency numbers cover an ITA system failure only; the local-failure options. Source: ITA FAQ (browser read 2026-07-26).

### Validator

- [ ] M23 Type code against Table 2.5; threshold by issue date; non-zero VAT; 9-digit dealer numbers; payment_amount + vat_amount = payment_amount_including_vat.

## Should cover (advanced)

- [ ] S1 Line categories and credited lines as negative quantity (API Table 2.2).
- [ ] S2 Periodic invoice from delivery notes (API s.2.4 notes).
- [ ] S3 Dealers' union and authorized third-party corporation fields (API Table 2.1 notes).
- [ ] S4 Manual invoice books: request through the ITA app or personal area.
- [ ] S5 Buyer-side retrieval service (API s.3).
- [ ] S6 Automating requests in invoicing software (Green Invoice guide).
- [ ] S7 A promoted but unlegislated move to remove the threshold entirely (vendor source only): mention only as unscheduled.

## Out of scope (explicit)

Reviewed 2026-09-15.

- VAT return filing and full PCN874 generation: a separate reporting workflow.
- Income-tax treatment: outside the allocation regime.
- Configuring a specific invoicing product: vendor-specific.
- ITA software registration certificates: a software-house process.
- Litigating a refusal: needs a licensed representative (legal gate).
- Palestinian-customer "I" invoices: not yet in the uniform file.
- Customs and import documents: customs rules, not s.38(א1).
- Rate limits, MultiApproval batch cap, idempotency after timeout, cancelling an already-allocated invoice: an ordinary integrator WOULD ask, but no ITA source publishes them as of 2026-09-15. The skill should say so rather than stay silent.

## Authoritative sources

- VAT Law 1975 ss.38(א1), 47(א1), Nevo: https://www.nevo.co.il/law_html/law00/72813.htm
- ITA API Description v2.0 (7.2024): https://www.gov.il/BlobFolder/generalpage/israel-invoice-160723/he/vat_software-houses-180724-en.pdf
- ITA Israel-Invoice FAQ: https://www.gov.il/he/pages/faq_israel_invoice
- Grant Thornton Israel: https://www.grantthornton.co.il/insights1/tax-insignths/2026/From_June_the_allocation_number/
- Green Invoice (secondary): https://www.greeninvoice.co.il/magazine/israel-invoice/
