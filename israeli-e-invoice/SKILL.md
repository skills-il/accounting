---
name: israeli-e-invoice
description: Generate, validate, and manage Israeli e-invoices (hashbonit electronit) per Tax Authority (SHAAM) standards. Use when user asks to create Israeli invoices, request allocation numbers, validate invoice compliance, or asks about "hashbonit", "e-invoice", "SHAAM", "allocation number", or Israeli invoicing requirements. Uses the official SHAAM document type codes: transaction invoice (300), tax invoice (305), periodic tax invoice (310), tax invoice/receipt (320), credit invoice (330), and proforma (332). Do NOT use for general accounting, bookkeeping, or non-Israeli invoice formats.
license: MIT
compatibility: Requires network access for SHAAM API calls. Works with Claude Code, Claude.ai, Cursor.
---

# Israeli E-Invoice

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
- Standard Israeli VAT rate: **18%** (as of 2025, verify current rate)
- VAT calculation: `vat_amount = net_amount * 0.18`
- Total: `gross_amount = net_amount + vat_amount`
- For VAT-exempt transactions (osek patur), no VAT line -- use receipt (320) instead

### Step 4: Check Allocation Number Requirement
Determine if an allocation number is needed:
- **Required if:** the net amount is above the current threshold AND the document type requires allocation: tax invoice (305), periodic tax invoice (310), tax invoice/receipt (320), proforma (332), and the v2 codes (340, 345, 348).
- **Threshold timeline** (allocation-number requirement under the Economic Arrangements Law 2023-2024 amending VAT Law section 47, accelerated schedule):
  - May 2024 - Dec 2024: > 25,000 NIS (excluding VAT)
  - Jan 2025 - Dec 2025: > 20,000 NIS (excluding VAT)
  - Jan 2026 - May 2026: > 10,000 NIS (excluding VAT)
  - **June 1, 2026 onwards (in effect): > 5,000 NIS (excluding VAT)**
  - Final stage (date TBD): full coverage
- **Not required for:** transaction invoices (300), credit invoices (330), plain receipts (kabala), and any invoice at or below the threshold.

**June 2026 transition warning:** The threshold dropped from 10,000 NIS to 5,000 NIS on June 1, 2026 (accelerated from the originally scheduled 2028 date). Any allocation-required invoice (305/310/320) issued on or after June 1, 2026 with a net amount above 5,000 NIS MUST carry an allocation number, otherwise the buyer cannot deduct input VAT. Verify the invoice issue date when checking the threshold, not the transaction date.

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
5. Date not in the future
6. Allocation number present if above threshold

If validation fails, report specific errors and how to fix them.

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
- `references/compliance-timeline.md` -- Progressive e-invoice mandate timeline under the Economic Arrangements Law 2023-2024 (amending the VAT Law), showing threshold reductions from 25,000 NIS down to all invoices. Consult when checking current allocation number thresholds.

## Gotchas

- Israel's e-invoice system is managed by SHAAM (the Tax Authority's technology arm), which assigns allocation numbers (mispar haktzaa) for each invoice. Agents may generate invoices without SHAAM allocation, which would not be valid for tax purposes.
- Israeli TIN (Tax Identification Number) for individuals is 9 digits with a check digit algorithm. Agents may not validate the check digit and accept invalid TINs.
- The distinction between cheshbonit mas (tax invoice, type 305) and cheshbonit mas/kabala (tax invoice-receipt, type 320) is critical. Agents may use them interchangeably, but they have different legal implications for payment timing.
- Israeli e-invoice XML schemas follow SHAAM-specific standards, not the European Peppol or UBL formats. Agents may attempt to use international e-invoice standards that are not accepted by the Israeli Tax Authority.
- Credit notes (cheshbonit zikui) in Israel must reference the original invoice number. Agents may generate standalone credit notes without the required linkage.


## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Israel Tax Authority – e-invoice | https://www.gov.il/he/departments/israel_tax_authority | Allocation number rules, invoice format, rollout schedule |
| SHAAM technical portal | https://www.misim.gov.il | Allocation number API, technical specs |
| Knesset – VAT Law | https://main.knesset.gov.il/Activity/Legislation/Laws/Pages/default.aspx | Value Added Tax Law, invoice obligations |
| ITA invoicing guidance | https://www.gov.il/he/departments/publications/reports/invoices_israel | Types of invoices (300/305/310/320/330), required fields |
| Kol Zchut – invoice rules | https://www.kolzchut.org.il/he | Plain-language duties for small businesses |

## Troubleshooting

### Error: "Invalid TIN format"
Cause: Israeli TIN (mispar osek) must be exactly 9 digits with valid check digit
Solution: Verify the number with the check digit algorithm. Run scripts/validate_invoice.py for validation.

### Error: "Allocation number required"
Cause: Invoice amount exceeds current threshold for mandatory allocation
Solution: Request allocation number from SHAAM API before issuing invoice. See Step 4.

### Error: "VAT rate mismatch"
Cause: Using incorrect VAT rate (rate changes periodically)
Solution: Verify current rate at the Tax Authority website. Standard rate is 18% as of 2025.

### Error: "Invoice type not suitable"
Cause: Wrong invoice type selected for the transaction
Solution: Review the invoice type table in Step 1. Common mistake: using type 305 (tax invoice) when 320 (tax invoice/receipt) is needed for immediate payment.