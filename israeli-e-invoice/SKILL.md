---
name: israeli-e-invoice
description: Generate, validate, and manage Israeli e-invoices (hashbonit electronit) per Tax Authority (SHAAM) standards. Use when user asks to create Israeli invoices, request allocation numbers, validate invoice compliance, or asks about "hashbonit", "e-invoice", "SHAAM", "allocation number", or Israeli invoicing requirements. Uses the official SHAAM document type codes including transaction invoice (300), tax invoice (305), periodic tax invoice (310), tax invoice/receipt (320), credit invoice (330), and proforma (332). Do NOT use for general accounting, bookkeeping, or non-Israeli invoice formats.
license: MIT
compatibility: Requires network access for SHAAM API calls. Works with Claude Code, Claude.ai, Cursor.
---

# Israeli E-Invoice

## Legal notice

This is a free information tool operated by an AI model. It explains the tax rules and helps you organise your own figures. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by a tax adviser or accountant. The output is not a tax opinion, not a return prepared by a licensed representative, and not professional advice, but a general calculation and explanation only: it does not examine the full extent of your income or your complete documents. An AI model may err, omit data, or present a wrong conclusion.

Any form or text this tool produces is an automatic draft for your personal preparation only, and is not a filed return. Responsibility for reporting and for paying the tax is yours, the binding computation is the Tax Authority's, and representation before the Tax Authority is reserved to those permitted by law. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person. Consult a tax adviser or accountant before filing or paying. All use of its output is the user's sole responsibility.


## Instructions

### Step 1: Determine Invoice Type
Ask the user what type of document they need:

These are the official SHAAM "Israel Invoice" document type codes (Table 2.5 of the Tax Authority API spec). Do NOT guess codes; the numbers below are the canonical ones.

| Code | Hebrew | English | Allocation # | When to Use |
|------|--------|---------|--------------|-------------|
| 300 | heshbon / heshbon iska | Transaction Invoice | No | Demand for payment, not a tax invoice |
| 305 | hashbonit mas | Tax Invoice | Yes (above threshold) | B2B sales, services |
| 310 | hashbonit mas tkufatit | Periodic Tax Invoice | Yes (above threshold) | Aggregated periodic billing |
| 320 | hashbonit mas / kabala | Tax Invoice / Receipt | Yes (above threshold) | Sale with immediate payment |
| 330 | hashbonit mas zikui | Credit Invoice | No | Refunds, corrections, returns |
| 332 | heshbon iska / proforma | Proforma Invoice | Yes (cash-basis, see references) | Quotes, pre-billing |

A plain payment receipt (kabala) is not part of the allocation document set and never needs an allocation number. The v2 spec adds reservation tax invoice (340), agent tax invoice (345), and the log command (348). There is no code 400 and no "self-billing" code in this taxonomy.

### Step 2: Collect Required Fields
For all invoice types, gather:
- **Seller details:** Business name, TIN (mispar osek), address, phone
- **Buyer details:** Business name (or individual), TIN (if B2B), address
- **Transaction:** Date, item descriptions, quantities, unit prices
- **Payment:** Method (cash, transfer, check, credit card), terms

### Step 3: Calculate VAT
- Standard Israeli VAT rate: **18%** (unchanged for 2026)
- VAT calculation: `vat_amount = net_amount * 0.18`
- Total: `gross_amount = net_amount + vat_amount`
- For an osek patur there is no VAT line. Issue a plain receipt (kabala). Do NOT use 320: that code is "tax invoice / receipt", a tax-invoice type that requires an allocation number, and an osek patur may not issue a tax invoice at all

### Step 4: Check Allocation Number Requirement
Determine if an allocation number is needed:
- **Required if ALL FOUR conditions hold** (Tax Authority API spec, section 1.2; in the statute, VAT Law s.47(a2)(1) obliges the dealer to request one "לפי דרישת הקונה", at the buyer's demand, and not for a zero-rated transaction): (1) the amount BEFORE VAT is above the current threshold; (2) the invoice includes a NON-ZERO VAT component, so a zero-rated invoice or one covering only exempt transactions needs no number; (3) the customer is an osek murshe (licensed dealer); (4) the customer has requested an allocation number. The document type must also be one that carries allocation: tax invoice (305), periodic tax invoice (310), tax invoice/receipt (320), proforma (332), and the v2 codes (340, 345, 348). A number MAY still be requested for any amount and any customer, including credits.
- **Test the amount BEFORE VAT, as the statute does.** Both the duty to request a number (VAT Law s.47(a2)(1): a transaction "שסכומה, בלא המס, עולה" on the threshold) and the bar on deducting input VAT (s.38(a1)) are measured on the amount before VAT, not on the VAT amount. Do not convert the threshold into a VAT-amount figure and test that instead: on a mixed invoice with an exempt component the two give different answers, and the statute uses only the amount before VAT. Some guidance describes a relief for mixed invoices; it was read on the Tax Authority FAQ on 2026-09-15, but it is administrative guidance that the statute does not contain, and the skill does not rely on it, so where the amount before VAT is over the threshold, tell the user a number is required if the customer is an osek murshe who asks for one, and that requesting a number is the safe course in any doubtful case. Always ask whether a quoted figure includes VAT, since a VAT-inclusive figure can sit above the threshold while the amount before VAT does not.
- **Threshold timeline** (allocation-number requirement under the Economic Arrangements Law 2023-2024 amending VAT Law section 47, accelerated schedule):
  - From 4 May 2024 to Dec 2024: net > 25,000 NIS
  - Jan 2025 to Dec 2025: net > 20,000 NIS
  - Jan 2026 to May 2026: net > 10,000 NIS
  - **June 1, 2026 onwards (in effect): net > 5,000 NIS**
  - No further reduction has been legislated or announced. Commentary speculates about a 2027 step, but nothing official supports it, so do not tell a user a further cut is scheduled.
- **Not required for:** transaction invoices (300), credit invoices (330), plain receipts (kabala), and any invoice at or below the threshold. The ITA has confirmed several cases that trip people up:
  - Credit notes (330) never need one, at any amount and for any reason.
  - An ordinary self-invoice (heshbonit atsmit) does not need one.
  - Debit notes (hoda'at hiyuv) do not need one, because they reduce the input-VAT claim.
  - A cancellation document for a payment demand does not need one.
  - A customer who does not deduct input VAT (a private individual, or a malkar or financial institution that is not offsetting) does not oblige the supplier to request one. You may still request one for such a customer, and the Tax Authority recommends requesting on every invoice for process uniformity; in that case put the sentinel 999999998 in the customer-number field.
  - A zero-rated or wholly exempt invoice carries no duty. The one zero-rated invoice that DOES carry a number is the reverse-charge replacement issued inside the refusal procedure (see below), which receives a SPECIAL allocation number; do not generalise it to ordinary zero-rated sales.

**June 2026 transition warning:** The threshold dropped from 10,000 NIS to 5,000 NIS on June 1, 2026. Any allocation-required invoice (305/310/320/340/345/348) issued on or after June 1, 2026 whose amount before VAT is above 5,000 NIS, where the buyer is an osek murshe who requests a number, MUST carry one, otherwise the buyer cannot deduct input VAT (s.38(a1)). Sources key the step to invoices issued from that date; no source read states which date governs a transaction that straddles the change, so flag it rather than guess.

If allocation number IS required:
1. Inform user they must request from SHAAM before issuing
2. Provide the API call structure (see references/shaam-api-reference.md)
3. The allocation number must appear on the printed/sent invoice

### Step 5: Generate Invoice Document
Create the invoice with all fields formatted per Israeli standards:
- Date in both Gregorian (DD/MM/YYYY) and Hebrew calendar
- Amounts in NIS (New Israeli Shekel)
- VAT breakdown as separate line
- Sequential invoice number from seller's series
- Allocation number (if applicable)

### Step 6: Validate
Run validation checks:
1. All required fields present
2. TIN format valid (9 digits with check digit)
3. VAT calculation correct
4. Invoice number sequential
5. Date is parseable and consistent with the transaction
6. Allocation number present where all four conditions hold (amount before VAT above the threshold, non-zero VAT, an osek murshe customer who requested one)

If validation fails, report specific errors and how to fix them.

## When the request fails or is refused

The allocation number is returned immediately in the normal case. Two failure modes have documented procedures, and they are handled differently.

**The Tax Authority refuses (substantive refusal).** Under VAT Law s.47(a2)(3) the Tax Authority may refuse a request where there is reasonable ground to suspect the invoice would be issued unlawfully. The issuer then has four documented alternatives: cancel the request; continue the transaction WITHOUT an allocation number; continue and offer the buyer a reverse charge (available only where the buyer is a registered osek murshe); or apply to the control unit and set a hearing. The reverse-charge route has a specific mechanic. The supplier cancels the held invoice by storno and re-requests with a zero-rate invoice that keeps the SAME invoice_id as the original, a different reference number, and the value 3 in the action field; that request returns a special allocation number, and the printout carries the caption "Customer must self-report this invoice" (API spec s.2.2.2). In the statute's terms (s.47(a3)), the buyer issues a tax invoice in its own name bearing that number and reports the transaction, while the supplier's zero-rate invoice states that it was issued under that subsection. If you continue without a number instead, the invoice must carry a prominent sentence stating that input tax may not be deducted against it. Report the chosen alternative back through the invoice-decision service (Cancel / Continue / FurtherObjection). The hearing timetable is set by statute (VAT Law s.47(a2)(3)(b) and s.47(a4)): the hearing is set within 2 business days of the online notice; a decision not given within 1 business day of the hearing counts as approval; a refusal can be objected to within 30 days of the hearing; the director must decide the objection within 21 business days or it counts as accepted; the decision on the objection can be appealed to the District Court.

**The system is down (technical failure).** The emergency-number arrangement covers a significant failure of the Tax Authority's own systems, NOT a local connectivity problem. For a local failure the issuer has three options: request the number through the standalone web application; wait for the fault to clear, within the period the law allows for issuing the invoice; or issue the invoice without a number and request one retroactively once the fault is fixed. The waiting option is bounded by the period the law allows for issuing the invoice, up to 14 days from the tax point.

**Request timing.** The Tax Authority accepts allocation requests for invoices dated ahead of the request, and retroactive requests once a fault is cleared, so a validator that rejects every future-dated invoice is wrong. Confirm the exact forward and retroactive windows against the Tax Authority's current guidance before relying on a specific number of days. A number can also be requested after the invoice is issued (VAT Law s.47(a2)(4)), but that does not change the deadline in s.38(a) for the buyer to deduct the input VAT within six months of the invoice date.

## Integration details that commonly break

- **Customer number is mandatory.** Omitting the customer's osek or company number returns error 432 ("מספר הלקוח אינו תקין"). The same error is returned if the supplier's own number is placed in the customer field.
- **Customers who do not deduct input VAT** are represented by the sentinel value `999999998` in the customer-number field.
- **460 is not an HTTP status.** The Approval service returns HTTP 200 even when the invoice is not approved. Check the `approved` field and the `confirmation_number`: an application error code such as 460 means the data was well-formed but the invoice was not approved. Treating 460 as a transport error will make an integration retry a request that will never succeed.
- **Print the last 9 digits.** The confirmation number returned is long; what goes on the invoice is the shortened allocation number, its 9 right-most characters, under a clear heading.
- **The allocation number's real destination is the PCN 874 detailed report**, on both the output and the input side. Printing it on the invoice is necessary but not sufficient.

## Examples

### Example 1: Simple B2B Tax Invoice
User says: "Create a tax invoice for a web development project, 15,000 NIS to ABC Ltd"
Actions:
1. Identify: Tax Invoice (type 305). Confirm the 15,000 is before VAT; it is above the 5,000 threshold, so an allocation number is needed if ABC Ltd is an osek murshe and asks for one, which a business customer usually does
2. Collect: Seller and buyer details
3. Calculate: Net NIS 15,000 + VAT NIS 2,700 = Total NIS 17,700
4. Guide: Request allocation number from SHAAM
5. Generate: Formatted invoice document
Result: Complete tax invoice with all required fields and allocation number guidance

### Example 2: Small B2C Receipt
User says: "I need a receipt for a 500 NIS cash payment"
Actions:
1. Identify: a plain receipt (kabala) confirming payment. Receipts are not part of the allocation document set, so no allocation number is needed (and the 320 tax-invoice/receipt code is only for a combined tax-invoice-plus-receipt, not a standalone receipt).
2. Collect: Seller and buyer details
3. Generate: Receipt document
Result: Simple receipt, no allocation number required

### Example 3: Credit Invoice for Refund
User says: "I need to issue a credit note for invoice #1234, partial refund of 3,000 NIS"
Actions:
1. Identify: Credit Invoice (type 330)
2. Reference: Original invoice #1234
3. Calculate: Credit amount with VAT reversal
4. Note: credit invoices (330) do not require an allocation number, but they must reference the original invoice
Result: Credit invoice referencing original, with correct VAT reversal

## Bundled Resources

### Scripts
- `scripts/validate_invoice.py` -- Validates Israeli e-invoice JSON against SHAAM requirements: checks required fields, TIN (mispar osek) format and check digit, invoice type codes, VAT calculation accuracy, and allocation number thresholds. Also referenced in Troubleshooting below. Run: `python scripts/validate_invoice.py --help`

### References
- `references/shaam-api-reference.md` -- SHAAM (Tax Authority) API endpoints for requesting allocation numbers, OAuth2 authentication setup, and request/response formats. Consult when integrating with the SHAAM e-invoice API. Also referenced in Step 4 above.
- `references/invoice-types.md` -- Complete listing of the SHAAM document type codes (300, 305, 310, 320, 330, 332, and the v2 codes 340/345/348) with required fields per type, VAT applicability, and allocation number requirements. Consult when determining which invoice type to use.
- `references/compliance-timeline.md` -- Progressive e-invoice mandate timeline under the Economic Arrangements Law 2023-2024 (amending the VAT Law), showing the threshold reductions from 25,000 NIS down to 5,000 NIS. Consult when checking current allocation number thresholds.

## Gotchas

- Israel's e-invoice system is managed by SHAAM (the Tax Authority's technology arm), which assigns allocation numbers (mispar haktzaa) for each invoice. Agents may generate invoices without SHAAM allocation, which would not be valid for tax purposes.
- Israeli TIN (Tax Identification Number) for individuals is 9 digits with a check digit algorithm. Agents may not validate the check digit and accept invalid TINs.
- The distinction between cheshbonit mas (tax invoice, type 305) and cheshbonit mas/kabala (tax invoice-receipt, type 320) is critical. Agents may use them interchangeably, but they have different legal implications for payment timing.
- Israeli e-invoice XML schemas follow SHAAM-specific standards, not the European Peppol or UBL formats. Agents may attempt to use international e-invoice standards that are not accepted by the Israeli Tax Authority.
- Credit notes (cheshbonit zikui) in Israel must reference the original invoice number. Agents may generate standalone credit notes without the required linkage.


## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Israel Tax Authority - Israel Invoice API spec v2.0 (PDF) | https://www.gov.il/BlobFolder/generalpage/israel-invoice-160723/he/vat_software-houses-180724-en.pdf | Allocation conditions, document type codes, refusal alternatives, endpoints |
| SHAAM API (sandbox + production) | https://ita-api.taxes.gov.il | Allocation-number API endpoints |
| Tax Authority Israel-Invoice FAQ | https://www.gov.il/he/pages/faq_israel_invoice | Authoritative answers on thresholds, refusals, exemptions |
| VAT Law (Nevo) | https://www.nevo.co.il/law_html/law00/72813.htm | Sections 38(a1) and 47(a2) to (a4): the threshold, the duty at the buyer's demand, refusals, hearings |
| Kol Zchut - invoice rules | https://www.kolzchut.org.il/he | Plain-language duties for small businesses |

## Troubleshooting

### Error: "Invalid TIN format"
Cause: Israeli TIN (mispar osek) must be exactly 9 digits with valid check digit
Solution: Verify the number with the check digit algorithm. Run scripts/validate_invoice.py for validation.

### Error: "Allocation number required"
Cause: the invoice's amount before VAT exceeds the current threshold for mandatory allocation, and the other conditions also hold (non-zero VAT, a licensed-dealer customer who requested a number)
Solution: Request allocation number from SHAAM API before issuing invoice. See Step 4.

### Error: "VAT rate mismatch"
Cause: Using incorrect VAT rate (rate changes periodically)
Solution: Verify current rate at the Tax Authority website. Standard rate is 18% from 1 January 2025 (17% until 31 December 2024), unchanged for 2026.

### Error: "Invoice type not suitable"
Cause: Wrong invoice type selected for the transaction
Solution: Review the invoice type table in Step 1. Common mistake: using type 305 (tax invoice) when 320 (tax invoice/receipt) is needed for immediate payment.