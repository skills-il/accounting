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
- **Required if:** the VAT amount is above the current VAT threshold AND the document type requires allocation: tax invoice (305), periodic tax invoice (310), tax invoice/receipt (320), proforma (332), and the v2 codes (340, 345, 348).
- **Test the VAT amount, not the net amount.** The law states the headline figures as net amounts, but the ITA's operative criterion is the VAT derived from them: "נדרש מספר הקצאה רק כאשר סכום המע"מ גבוה מ-900 ₪" from 1 June 2026 (1,800 from 1 January 2026, 3,600 for 2025). For a wholly standard-rated invoice the two tests coincide, because 5,000 x 18% = 900. They diverge on a MIXED invoice with an exempt or zero-rated component, which can sit above the net threshold while its VAT stays below the VAT threshold, in which case no allocation number is required. The Tax Authority states this directly for the customs-agent case, where the taxable service or commission component is small next to the invoice total, and says the same answer applies to other dealers operating similarly. It nonetheless recommends requesting a number on every invoice where your software already supports it, so the process stays uniform.
- **Threshold timeline** (allocation-number requirement under the Economic Arrangements Law 2023-2024 amending VAT Law section 47, accelerated schedule):
  - From 4 May 2024 to Dec 2024: net > 25,000 NIS (VAT > 4,500)
  - Jan 2025 to Dec 2025: net > 20,000 NIS (VAT > 3,600)
  - Jan 2026 to May 2026: net > 10,000 NIS (VAT > 1,800)
  - **June 1, 2026 onwards (in effect): net > 5,000 NIS (VAT > 900)**
  - No further reduction has been legislated or announced. Commentary speculates about a 2027 step, but nothing official supports it, so do not tell a user a further cut is scheduled.
- **Not required for:** transaction invoices (300), credit invoices (330), plain receipts (kabala), and any invoice at or below the threshold. The ITA has confirmed several cases that trip people up:
  - Credit notes (330) never need one, at any amount and for any reason.
  - An ordinary self-invoice (heshbonit atsmit) does not need one.
  - Debit notes (hoda'at hiyuv) do not need one, because they reduce the input-VAT claim.
  - A cancellation document for a payment demand does not need one.
  - A customer who does not deduct input VAT (a private individual, or a malkar or financial institution that is not offsetting) does not oblige the supplier to request one. You may still request one for such a customer, and the Tax Authority recommends requesting on every invoice for process uniformity; in that case put the sentinel 999999998 in the customer-number field.
  - Note the reverse-charge exception in the other direction: in that flow the supplier issues a zero-rated invoice that DOES carry an allocation number, so an invoice with no VAT charged on it does not automatically mean no allocation number is needed.

**June 2026 transition warning:** The threshold dropped from 10,000 NIS to 5,000 NIS on June 1, 2026. Any allocation-required invoice (305/310/320) issued on or after June 1, 2026 with VAT above 900 NIS (net above 5,000 NIS on a wholly standard-rated invoice) MUST carry an allocation number, otherwise the buyer cannot deduct input VAT. Verify the invoice issue date when checking the threshold, not the transaction date.

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
6. Allocation number present if above threshold

If validation fails, report specific errors and how to fix them.

## When the request fails or is refused

The allocation number is returned immediately in the normal case. Two failure modes have documented procedures, and they are handled differently.

**The Tax Authority refuses (substantive refusal).** Since 2025 the ITA may refuse a request where there is reasonable ground to suspect the invoice would be issued unlawfully. The issuer then has four documented alternatives: cancel the request; continue the transaction WITHOUT an allocation number; continue and offer the buyer a reverse charge (available only where the buyer is a registered osek murshe); or apply to the control unit and set a hearing. The reverse-charge route has a specific mechanic: cancel the refused invoice, issue a new one with identical details except a VAT value of zero and a different reference number, and that new invoice receives a special allocation number and is reported as a zero-rated transaction. If you continue without a number instead, the invoice must carry a prominent sentence stating that input tax may not be deducted against it. Report the chosen alternative back through the invoice-decision service (Cancel / Continue / FurtherObjection).

**The system is down (technical failure).** The emergency-number arrangement covers a significant failure of the Tax Authority's own systems, NOT a local connectivity problem. For a local failure the issuer has three options: request the number through the standalone web application; wait for the fault to clear, within the period the law allows for issuing the invoice; or issue the invoice without a number and request one retroactively once the fault is fixed. The waiting option is bounded by the period the law allows for issuing the invoice, up to 14 days from the tax point.

**Request timing.** The Tax Authority accepts allocation requests for invoices dated ahead of the request, and retroactive requests once a fault is cleared, so a validator that rejects every future-dated invoice is wrong. Confirm the exact forward and retroactive windows against the Tax Authority's current guidance before relying on a specific number of days.

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
1. Identify: Tax Invoice (type 305), above threshold -- allocation needed
2. Collect: Seller and buyer details
3. Calculate: Net 15,000 + VAT 2,700 = Total 17,700 NIS
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
| Israel Tax Authority - e-invoice | https://www.gov.il/he/departments/israel_tax_authority | Allocation number rules, invoice format, rollout schedule |
| SHAAM API (sandbox + production) | https://ita-api.taxes.gov.il | Allocation-number API endpoints |
| Tax Authority Israel-Invoice FAQ | https://www.gov.il/he/pages/faq_israel_invoice | Authoritative answers on thresholds, refusals, exemptions |
| Knesset - VAT Law | https://main.knesset.gov.il/Activity/Legislation/Laws/Pages/default.aspx | Value Added Tax Law, invoice obligations |
| ITA invoicing guidance | https://www.gov.il/he/departments/publications/reports/invoices_israel | Types of invoices (300/305/310/320/330), required fields |
| Kol Zchut - invoice rules | https://www.kolzchut.org.il/he | Plain-language duties for small businesses |

## Troubleshooting

### Error: "Invalid TIN format"
Cause: Israeli TIN (mispar osek) must be exactly 9 digits with valid check digit
Solution: Verify the number with the check digit algorithm. Run scripts/validate_invoice.py for validation.

### Error: "Allocation number required"
Cause: the invoice's VAT amount exceeds the current VAT threshold for mandatory allocation
Solution: Request allocation number from SHAAM API before issuing invoice. See Step 4.

### Error: "VAT rate mismatch"
Cause: Using incorrect VAT rate (rate changes periodically)
Solution: Verify current rate at the Tax Authority website. Standard rate is 18%, unchanged for 2026.

### Error: "Invoice type not suitable"
Cause: Wrong invoice type selected for the transaction
Solution: Review the invoice type table in Step 1. Common mistake: using type 305 (tax invoice) when 320 (tax invoice/receipt) is needed for immediate payment.