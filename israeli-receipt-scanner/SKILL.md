---
name: israeli-receipt-scanner
description: OCR and parse Israeli receipts and invoices with Hebrew and English text extraction. Extracts merchant, date, NIS total, VAT amount, document and allocation numbers, payment method, and VAT registration number (osek murshe). Handles supermarket, gas station, restaurant and online-purchase formats, categorizes expenses, and outputs JSON or CSV for accounting software. Classifies each document's input VAT as deductible, needs review, or not deductible, applying the allocation-number band and six-month window by the invoice's own date, and catches duplicates, card vouchers and credit notes in a batch. Explains how long paper originals must be kept and when a scan may replace them. Use when you need to digitize, extract data from, categorize, or check the VAT deductibility of Israeli receipts and tax invoices, including a box of accumulated paper. Do NOT use for non-Israeli receipt formats, handwritten notes without printed text, or bank statement reconciliation.
license: MIT
allowed-tools: Bash(python:*) Read Edit Write WebFetch
compatibility: Requires Claude Code with vision capabilities for image-based OCR
---


# Israeli Receipt Scanner

## Legal notice

This is a free information tool operated by an AI model. It explains the rules and calculates from the figures you enter, but it does not examine your full circumstances and does not constitute tax advice. All of its outputs are produced automatically, with no involvement, review, or approval by a tax adviser or accountant, and an AI model may err, omit data, or present a wrong conclusion. The binding computation is the Tax Authority's and responsibility for reporting is yours. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person, and all use of its output is the user's sole responsibility.


## Instructions

### Step 0: Ask About the Claimant Once per Batch

Whether input VAT is deductible depends on who is claiming it, not only on the document. Before scanning a batch, ask once and store the answers in a `claimant` block:

- **VAT status** (`vat_status`): `osek_murshe`, `company`, `osek_patur`, `amuta`, `financial_institution`, or `no_business`. An osek patur, a person with no business, a non-profit (מלכ"ר) and a financial institution (מוסד כספי) deduct no input VAT: section 1 of the VAT Law defines an "עוסק" as excluding a מלכ"ר or מוסד כספי, and section 38(א) gives the deduction only to an עוסק. For them, say so plainly, still extract the data (it matters for income tax and for records), and set every record to `decision: "denied"` with `deductibility_basis: "claimant cannot deduct input VAT"`. An amuta that is also registered as an osek for a business activity goes to `review`.
- **Own VAT number** (`vat_number`): drives the buyer-identity test. Without it the buyer test cannot pass, so records stay `needs_review`.
- **Business type** (`business_type`): a caterer's groceries or a kindergarten's food are business inputs. The "inherently private" categories below are a default, not a rule, and this field overrides them.
- **Exempt supplies** (`makes_exempt_supplies`): does the claimant also make transactions on which input VAT is not deductible (residential rent alongside a taxable business, for example)? Section 41 bars input VAT on inputs that do not serve a taxable transaction, and regulation 18(א) apportions shared inputs.
- **Reporting period** (`reporting_period`: `monthly` or `bimonthly`) and the END DATE of the last period already filed (`periods_filed_through`, for example `2026-08-31`). This drives the double-claim check and the deadline triage in Step 8.

If the user will not answer, proceed with `vat_status: "unknown"` and leave every record at `decision: "review"`.

### Step 1: Prepare the Receipt Image or Text

The receipt may be a photographed or scanned image (JPEG, PNG, PDF), raw OCR text from another tool, or a digital receipt in plain text or HTML.

For an image, use vision capabilities. Israeli receipts mix Hebrew (right-to-left) and English or numbers (left-to-right) on the same line, so check that each amount sits next to its own line item.

Many small tradespeople still issue tax invoices from pre-printed invoice books: the header and supplier details are printed, and the amounts and buyer are handwritten. These are ordinary tax invoices and are in scope. Read them, set `handwritten_fields: true`, and set `needs_review: true` on any amount you are not certain of. Only free-form notes with no printed issuer are out of scope.

### Step 2: Identify the Document Type

- **Tax Invoice (חשבונית מס)**: VAT registration number, itemized VAT, header "חשבונית מס". Issued by an osek murshe.
- **Tax Invoice / Receipt (חשבונית מס / קבלה)**: a combined document, common in retail.
- **Receipt (קבלה)**: proof of payment only, header "קבלה".
- **Proforma Invoice (חשבונית עסקה)**: a demand before payment, not valid for VAT deduction.
- **Credit-card voucher (שובר אשראי)**: proof of payment only, never a tax invoice.
- **Credit note (חשבונית מס זיכוי / הודעת זיכוי)**: reduces a previous tax invoice. It is never a positive input, even though its header says "חשבונית מס". Record `document_type: "credit_note"` with negative amounts and the original invoice's number if printed.

Only a חשבונית מס or חשבונית מס / קבלה issued by an osek murshe can support an input-VAT deduction, and it must be issued to the claimant "כדין". Section 47(ב)(1) of the VAT Law requires a tax invoice to show the buyer's registration number, unless a Director's permit exempts a class of dealers or transactions; the general amount of any such permit is not openly published, so never state one. A plain קבלה, a חשבונית עסקה, or any document from an osek patur cannot support a deduction. An osek patur is a dealer whose turnover does not exceed NIS 122,833 a year (the 2026 figure; it is indexed every 1 January) and issues no tax invoice.

A foreign document (US sales tax, EU VAT) is never an Israeli tax invoice: its tax line never populates `vat_amount` or `vat_deductible`.

### Step 3: Extract Core Fields

1. **Merchant Name (שם העסק)**: usually the first line, in Hebrew.
2. **Supplier VAT Number (מספר עוסק מורשה / ח.פ.)**: near the header. A tax invoice carries the dealer's ID number, the corporate registration number, or failing those the VAT registration number. Classify `supplier_type` as `osek_murshe`, `osek_patur`, or `unknown`.
3. **Buyer Name and Buyer VAT Number** (`buyer_name`, `buyer_vat_number`): the party the invoice was issued TO. `null` when no buyer is printed (typical for walk-in slips).
4. **Branch/Address (כתובת)**.
5. **Date (תאריך)**: DD/MM/YYYY.
6. **Time (שעה)**.
7. **Document Number (מספר חשבונית / מספר קבלה / מס' אסמכתא)**.
8. **Allocation Number (מספר הקצאה)**: a 9-digit number printed under an "מספר הקצאה" label, usually beneath the document number. It is random with no check digit, so never checksum it. If a longer string is printed instead, keep it verbatim in `allocation_number_raw`, leave `allocation_number` null and set `decision: "review"`; do not guess which digits count. `null` if absent.
9. **Line Items**: description, quantity, unit price, line total.
10. **Subtotal (סכום לפני מע"מ)**.
11. **VAT Amount (מע"מ)**.
12. **Total (סה"כ / סה"כ לתשלום)**.
13. **Payment Method (אמצעי תשלום)**: card (last 4 digits), cash (מזומן), wallet, or transfer.
14. **Installments (תשלומים)**: the number of installments and the amount of each, when printed.

### Step 4: Handle Common Israeli Retailer Formats

**Supermarkets (Shufersal, Rami Levy, Yochananof, Osher Ad)**: barcode-based items, club discounts as negative lines, weighed produce, bottle deposits (פיקדון), a "חסכת" summary line. Unprocessed fruit and vegetables of listed kinds are zero-rated, so a supermarket subtotal may mix 18% and 0% lines.

**Gas Stations (Paz, Sonol, Delek, Ten)**: fuel type (95, 98, סולר), liters, price per liter, sometimes the odometer, store items as separate lines. A pump slip and a later monthly fuel-card tax invoice may describe the same fuel.

**Restaurants and Cafes**: service charge (שירות), tip line, table number.

**Online Purchases**: PDF invoices, shipping (משלוח) lines, an order number besides the invoice number.

### Step 5: Auto-Categorize the Expense

| Category | Hebrew | Common Merchants/Items |
|----------|--------|----------------------|
| Groceries | מזון ומכולת | Shufersal, Rami Levy, Osher Ad |
| Fuel | דלק | Paz, Sonol, Delek, Ten |
| Office Supplies | ציוד משרדי | Office Depot, Kravitz |
| Meals & Entertainment | ארוחות ואירוח | Restaurants, cafes |
| Transportation | תחבורה | Parking, tolls, public transit |
| Software & SaaS | תוכנה ושירותי ענן | Digital subscriptions |
| Professional Services | שירותים מקצועיים | Consultants, lawyers |
| Telecommunications | תקשורת | Cellcom, Partner, HOT |
| Insurance | ביטוח | Insurance premiums |
| Maintenance | תחזוקה | Repairs, cleaning |
| Medical | רפואה | Pharmacies, clinics |
| Travel | נסיעות | Hotels, flights |

Use the merchant and the items. If ambiguous, use "General Expenses (הוצאות כלליות)" and set `needs_review: true`.

### Step 6: Output Structured Data

Default to JSON. The `claimant` block is written once per batch; each record looks like this (the VAT number below is illustrative; `items` is abbreviated to one line):

```json
{
  "document_type": "tax_invoice_receipt",
  "merchant": {
    "name_he": "שופרסל דיל",
    "name_en": "Shufersal Deal",
    "vat_registration": "123456782",
    "supplier_type": "osek_murshe",
    "branch": "סניף רמת אביב"
  },
  "buyer_name": null,
  "buyer_vat_number": null,
  "document_number": "12345678",
  "allocation_number": null,
  "date": "2026-09-08",
  "items": [
    {"description": "חלב תנובה 3% 1 ליטר", "quantity": 2, "unit_price": 6.90, "total": 13.80}
  ],
  "subtotal": 245.50,
  "vat_rate": 0.18,
  "vat_amount": 44.19,
  "total": 289.69,
  "currency": "ILS",
  "payment": {"method": "credit_card", "card_last_four": "4532", "installments": 1},
  "category": "groceries",
  "category_he": "מזון ומכולת",
  "decision": "denied",
  "vat_deductible": false,
  "deductible_fraction": 0,
  "candidate_fraction": null,
  "deductibility_basis": "no buyer printed; inherently private category",
  "business_use": null,
  "vehicle": null,
  "reverse_charge_required": false,
  "deduction_deadline": "2027-03-08",
  "dedupe_key": "123456782|tax_invoice_receipt|רמת אביב|12345678",
  "payment_evidence_for": null,
  "handwritten_fields": false,
  "needs_review": false,
  "warnings": ["No buyer printed on the invoice; not an input-VAT invoice for any specific business"]
}
```

For CSV, flatten with these columns, and never drop the reasoning columns on export:
`date, document_type, document_number, allocation_number, merchant_name, vat_registration, supplier_type, buyer_name, buyer_vat_number, subtotal, vat_rate, vat_amount, total, payment_method, category, decision, vat_deductible, deductible_fraction, candidate_fraction, deductibility_basis, deduction_deadline, reverse_charge_required, dedupe_key, payment_evidence_for, needs_review, warnings`

- `decision`: `deductible`, `review`, or `denied`. It is the single source for the Step 8 buckets. `vat_deductible` is `true` only when `decision` is `deductible`.
- `deductible_fraction`: the share of the VAT that is claimed, meaningful only when `decision` is `deductible`: `1` for a wholly business input, otherwise the partial-use fraction. `0` for `denied`.
- `needs_review`: `true` on every `review` record, and on a `denied` record whose bar has an exception worth checking (hosting a person from abroad), and on a `deductible` record whose fraction rests on the claimant's stated use basis.
- `candidate_fraction`: for a `review` record, the fraction that would apply if the bookkeeper approves (for example two-thirds on private-car fuel); `null` when unknown. Never add it to the deductible total.
- A known business share (90% of a phone) is that ratio under regulation 18(א); two-thirds and one-quarter apply only when the share is indeterminate (regulation 18(ב)). When lines differ (fuel and a shop item on one slip), put the fraction on each line in `items[]` and the VAT-weighted result on the record.
- `business_use`: `{basis, ratio}` with basis `wholly_business`, `reg18a_actual_ratio`, `reg18b_director`, `reg18b_mainly_business`, or `reg18b_mainly_private`.
- `vehicle`: `{class, document_kind}`, see Step 7.
- `deduction_deadline`: the invoice date plus six months.

`decision` is set ONLY by the canonical list in Step 7. Do not decide it anywhere else.

### Step 7: Validate and Decide Deductibility

**Data checks.**

1. **VAT arithmetic, date-aware**: `total = subtotal + vat_amount` within 0.05 NIS, or up to 0.10 NIS on a slip with many lines or a cash rounding line (עיגול). Select the expected rate by the invoice's own date: 18% from 1 January 2025, 17% from 1 October 2015 to 31 December 2024 (older documents: `review`). A 2024 invoice at 17% is correct, not an error. A rate that does not fit the date may still have a reason the tool cannot see, so a mismatch is `review` with the reason, never an extraction error. On a slip that mixes standard-rated and zero-rated lines, test the VAT against the standard-rated lines only; on VAT-inclusive lines the VAT is the gross amount times 18/118 (17/117 at 17%), not 18% of it. An osek patur slip has no VAT line and skips this check. Eilat Free-Trade-Zone and zero-rated supplies (exports, and unprocessed fruit and vegetables of the kinds the Finance Minister listed under section 30(א)(13)) legitimately show no VAT: set `vat_rate: 0`, note why, skip the mismatch check, and do not assume osek patur.
2. **Date**: valid and not in the future.
3. **Supplier VAT number**: 9 digits; left-pad an 8-digit number with a zero before checking. An individual dealer's number is their ID number, whose check digit is computed by the Luhn algorithm (weights 1, 2, 1, 2 from the left): validate it. For a company or other registration number no check-digit rule is relied on here; check the 9 digits only. A failed check usually means an OCR misread: re-read, then `review`, never `denied` on that ground alone.
4. **Line items**: first decide whether the lines are printed net or VAT-inclusive. Israeli retail slips (supermarkets, fuel, pharmacies, restaurants) usually print VAT-inclusive prices, so their lines sum to the TOTAL; net-priced B2B invoices sum to the subtotal. Include discount and deposit lines.
5. **Currency**: NIS. A foreign document gets `decision: "denied"` as an input-VAT invoice and a foreign-vendor warning. Where the transaction is made in Israel by a foreign-resident supplier (typically an imported service), regulation 6ד makes the BUYER liable for the tax unless it holds an invoice, so set `reverse_charge_required: true` for the bookkeeper. Imported goods are deducted through the customs import entry instead.
6. **Allocation band, by the invoice's own date**: none for invoices dated up to 4 May 2024; above NIS 25,000 net from 5 May 2024, 20,000 in 2025, 10,000 from January to May 2026, 5,000 from June 2026. "Above" means exceeds: an invoice exactly on the figure is outside. Zero-rated invoices are exempt. A 2024 invoice must not be tested against today's band.
7. **Six-month window**: compute `deduction_deadline` as the same day six months later, or the last day of that month when it has no such day (31 August gives 28 or 29 February). The deduction is made in a periodic return, so today's date is only a screen: if the deadline falls after the end of the next unfiled reporting period, it passes (pass zone); if it fell before the end of the last filed period, the invoice needs an extension (extension zone) from the Director under section 116(א) of the VAT Law, which can never reach beyond five years from the invoice date; anything in between is `review` ("confirm which return still accepts it"). Getting an allocation number later does not restart the clock.
8. **Cash cap**: only when the transaction price exceeds NIS 6,000 and a business is a party, cash may be at most the lower of 10% of the price and NIS 6,000. Below that price there is no cash limit. Warn, do not deny: the input VAT is disallowed only where a breach was decided AND a penalty imposed (section 38(א2)).

**The canonical deductibility list.** Set `decision: "deductible"` ONLY when ALL hold:

- (a) `claimant.vat_status` is `osek_murshe` or `company` (not `osek_patur`, `amuta`, `financial_institution`, `no_business`, or `unknown`);
- (b) the document is a חשבונית מס or חשבונית מס / קבלה (not a credit note) from an osek murshe whose number passes Check 3 (an import entry or a self-invoice is also a deduction document: route it to `review`);
- (c) the purchase is for the business, not private consumption (judged against `claimant.business_type`);
- (d) the invoice is issued to the claimant, with `buyer_vat_number` matching `claimant.vat_number`, subject to the exceptions below;
- (e) an allocation number is present when the net amount exceeds the band for the invoice's date;
- (f) Check 7 places the deadline in its pass zone;
- (g) the invoice has not already been claimed (Step 8) and is not a payment-evidence copy of another record;
- (h) none of the bars below applies;
- (i) no data check (1 to 8) left the record in `review`.

When deductible because of a partial-use rule, set `deductible_fraction` to the fraction, never to 1. A failed hard condition or a hard bar gives `denied`, except where Step 0, Check 3 or Check 7 routes the record to `review`. A soft rule gives `review`. An invoice in Check 7's extension zone is `denied` with `needs_review: true` (an extension under section 116(א) is possible).

**Hard bars (check them first; they defeat an otherwise perfect invoice; `decision: "denied"`).**

- **Hosting (regulation 16)**: no deduction on hosting expenses (restaurants, catering, hospitality), except hosting a person from abroad. Note the exception for the bookkeeper.
- **Employee benefits (regulation 15א)**: meals, housing, gifts, entertainment for an employee are not deductible unless supplied to the employee as a reported taxable transaction. "Employee" includes an owner or manager of the business, so a sole trader's own meal is caught too.
- **Buying or importing a private car (regulation 14(א))**: no deduction at all, outside the regulation 14(ב) carve-outs (a vehicle dealer's stock, driving instruction, rental, passenger transport, organised tours).
- **The dealer's own home (regulation 15)**: no deduction on buying or building the dealer's residential apartment, or on services for that purchase or construction, even if it is also the place of business. Ordinary running costs of a home office stay under regulation 18.

**Mixed use (regulation 18) sets a fraction; it is not a review by itself.** A known business share is that ratio. An indeterminate share is two-thirds when the claimant says use is mainly for the business and one-quarter when mainly private, unless the Director fixed a proportion. When the claimant has given that basis, the record can be `deductible` at the fraction (the other conditions holding), with `needs_review: true` so the bookkeeper can confirm the basis; only an unknown basis makes it `review`, with the fraction in `candidate_fraction`. When `claimant.makes_exempt_supplies` is true, inputs that serve only the exempt side get fraction 0 (section 41) and shared inputs go to the 18(א) ratio.

**Private-looking categories** (groceries, clothing, personal medical) are `denied` by default; they become `review` when `claimant.business_type` plausibly makes them business inputs.

**Softer rules (`decision: "review"`, do not hard-deny).**

- **Small slips with no buyer**: the buyer's number is required by default, but Director's permits exempt some classes. Under regulation 9א(ג)(1) of the VAT Bookkeeping Regulations, a cash-register slip is treated as a tax invoice for a service up to NIS 309 including VAT from dealers covered by section 4 of the eleventh schedule. Do not hard-deny a small no-buyer slip; defer to the bookkeeper. A large invoice with no matching buyer is `denied`.
- **Utilities not in the claimant's name (regulation 12ג)**: telephone, water, gas, electricity and similar may be allowed where business use is proved, typically by the lease. Note what proof is needed.
- **Vehicle running costs**: fuel, repairs and leasing are a regulation 18 question (see mixed use above); an `unknown` vehicle class is `review`. Record `vehicle.class` (`private`, `commercial`, `reg14b_exempt_use`, `unknown`) and `vehicle.document_kind` (`purchase`, `import`, `lease`, `fuel`, `repair`, `other`). A commercial vehicle outside the private-car definition (truck, taxi) follows the ordinary rules.

The statutory detail behind each item is in `references/vat-deduction-rules.md`.

### Step 8: Batch Pass (Run After All Documents Are Read)

A shoebox holds the same transaction more than once. Input VAT is deducted once per tax invoice, so summing records naively over-claims.

1. **De-duplicate.** Key each record by `supplier VAT number | document type | branch or register | document number`, because suppliers number each document type separately and chains number per branch. The same document photographed twice keeps one record. When supplier and number agree but the type or branch is missing or reads differently on one copy (a cropped photo, an emailed PDF, a "העתק"), mark both `review` as possible duplicates; never count both as deductible. When the number is unreadable, a match on date, total and card last 4 is only a POSSIBLE duplicate: mark both `review`, never merge them, since two equal parking fees on one day are lawful twins.
2. **Link payment evidence.** A קבלה, a שובר אשראי or a pump slip that pays a tax invoice is not a new expense: set `payment_evidence_for` to the invoice's key and fraction 0, and leave the deduction on the invoice. Match by supplier and amount first (several vouchers may together pay one invoice, so a sum of vouchers can match), with the nearest date only as a tie-break; each voucher links to one invoice. A monthly or consolidated tax invoice (חשבונית מרכזת, a fuel-card statement invoice) covers every slip from that supplier in its billing period: link them by period and card, and flag a gap between the slips' sum and the invoice total. Ties go to `review`.
3. **Credit notes.** The buyer reduces input VAT in the period the credit note is received (regulation 24(ב)), by the difference in the tax it deducted (section 43). So link each credit note to its original and follow the original: a `deductible` original is reduced by the credit's VAT times its `deductible_fraction`; a `review` original has its review amount reduced; a `denied` original changes nothing. A credit note whose original is not in the batch (deducted in an earlier return) still reduces input tax: show it as its own negative line, `review`, so the bookkeeper applies the original's fraction.
4. **Already-filed periods.** Records dated on or before `claimant.periods_filed_through` may already be in a filed return. Mark them `review` with "check whether already claimed; if it was not in that return, it can still go in a later one inside the window". Never add them to the deductible total until confirmed.
5. **Deadline triage.** Sort the still-deductible records by `deduction_deadline`. Tell the user in plain words how many are in Check 7's extension zone (and need an extension request), and list the ones expiring soonest for the next return.
6. **Summary.** Report three buckets by `decision`, with counts and input-VAT totals: deductible (VAT multiplied by `deductible_fraction`, after the credit-note reductions in 3), review (show the VAT and, separately, the amount at `candidate_fraction`), and denied. Group the deductible bucket by invoice month so the bookkeeper can map it to returns.
7. **VAT is not income tax.** Say once: a document that is not deductible for VAT may still be a deductible expense for income tax, which this skill does not decide. Keep it. For expense classification, `israeli-expense-categorizer` covers that.

### Step 9: Answer "Can I Throw the Paper Away?"

The default answer is no, and the skill must say so whenever it finishes a batch:

- Keep originals for the later of: seven years from the last book entry or the purchase invoice's date (VAT Law, section 75), and seven years from the end of the tax year or six years from filing that year's return (Bookkeeping Directives, section 25(ג)).
- This skill's photos, JSON and CSV are working copies. A scan replaces the paper only when it meets annex F of section 36 of the Directives: entered in the books, marked "מסמך סרוק", signed with an approved electronic signature by the taxpayer AND checked and signed by a second person, protected, and held in an annex G digital archive.
- Even then, paper for a tax year may be destroyed only after that year's return is filed and the other annex F conditions hold. Current-year paper can never go.

Full rules and suggested wording are in `references/retention-and-scanning.md`.

## Examples

### Example 1: Supermarket Receipt

User says: "Scan this Shufersal receipt and extract the data." The claimant is a consultant, osek murshe.

1. Reads the image and identifies "חשבונית מס / קבלה".
2. Extracts the merchant, the supplier number, 12 line items and a club discount "הנחת מועדון: -15.40".
3. Totals: subtotal 312.80, VAT 56.30, total 369.10 (all lines standard-rated in this slip; 312.80 x 0.18 = 56.30).
4. Groceries for a consultant, with no buyer printed: `decision: "denied"`, fraction 0.

Result: a complete record, arithmetic checked, not deductible for this claimant.

### Example 2: Gas Station Receipt with Two Items

User says: "Parse this Sonol receipt for my expense report." The claimant drives a private car, mainly for work, with no fixed business share.

1. Lines: 95 octane, 35.2 L at 7.45 = 262.24, and water 8.90. Totals: subtotal 229.78, VAT 41.36, total 271.14 (271.14 / 1.18 = 229.78).
2. Two category assignments: fuel 262.24, general 8.90.
3. Records `vehicle: {class: "private", document_kind: "fuel"}` and `business_use: {basis: "reg18b_mainly_business"}`, so `candidate_fraction` on the fuel line is two-thirds. No buyer is printed, so `decision: "review"` for the bookkeeper.
4. Step 8 later finds the month's fuel-card tax invoice in the claimant's name, covering this fill-up among others. The pump slip becomes `payment_evidence_for` that invoice with fraction 0, and the two-thirds is applied to the invoice's fuel lines instead.

### Example 3: Restaurant Tax Invoice

User says: "I have a receipt from a business lunch. Extract the details for tax deduction."

1. Identifies "חשבונית מס / קבלה" from "מסעדת רפאל, תל אביב" with a 12% service charge.
2. Hosting bar (regulation 16): `decision: "denied"`, noting the single exception for hosting a person from abroad.
3. Adds: "Not deductible for VAT does not mean irrelevant for income tax; keep the receipt."

### Example 4: Shoebox Batch

User says: "Here are 200 receipts from the last 18 months. What can I deduct, and can I throw the paper away?"

1. Step 0: asks the VAT status, VAT number, business type, reporting period and last filed period.
2. Reads every document, then runs Step 8: removes duplicates, links card vouchers to their invoices, flags periods already filed, and reports how many invoices are past `deduction_deadline`.
3. Prints the three-bucket summary, credit notes netted.
4. Step 9: "Do not throw them away. Keep the originals for at least seven years. These scans are working copies, not legal substitutes."

## Bundled Resources

- `references/vat-deduction-rules.md`: statutory detail for Step 7 (allocation number format, scope and remedies; the six-month window and its extension; the buyer number; regulation 18; vehicles; hosting; the Cash Law; foreign vendors).
- `references/retention-and-scanning.md`: retention periods and the annex F and G conditions for replacing and destroying paper.
- `references/domain-checklist.md`: the coverage checklist this skill is reviewed against.

This skill ships no scripts. For batch OCR use a vision-capable model with your own wrapper.

## Gotchas

- Bidirectional text: OCR may reverse reading order. Verify each amount sits on its own line item.
- Dates are DD/MM/YYYY; thermal printers may use DD/MM/YY. Do not read 01/03/26 as January 3.
- Osek patur receipts carry no VAT breakdown. Do not compute VAT from them.
- Thermal paper fades in summer heat. Scan early as a working copy; do not destroy the original.
- A credit-card voucher (שובר אשראי) is never a tax invoice, and next to its invoice it is a duplicate, not a second expense.
- A credit note's header also says "חשבונית מס". Its VAT reduces input tax; never add it as a positive input.
- Do not apply today's 18% rate or today's allocation band to a 2024 invoice.
- A 9-digit number near the document number is not an allocation number unless it is labelled as one.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| VAT Law (consolidated) | https://www.nevo.co.il/law_html/law01/271_001.htm | Sections 38, 47, 75, 116 |
| VAT Regulations | https://www.nevo.co.il/law_html/law01/271_005.htm | Regulations 12ג, 14, 15א, 16, 18 |
| Bookkeeping Directives | https://www.nevo.co.il/law_html/law01/255_179.htm | Section 25, annexes F and G of section 36 |
| Tax Authority, Israel Invoices FAQ | https://www.gov.il/he/pages/faq_israel_invoice | Allocation number format and bands |
| Tax Authority, amounts and rates | https://www.gov.il/he/pages/vat-rate-amount-new | Osek patur ceiling, small-sum figures |
| Tesseract OCR | https://github.com/tesseract-ocr/tesseract | Hebrew language data |

## Troubleshooting

### Error: "Unable to read Hebrew text from image"

Cause: low resolution, poor light, a decorative font, or faded thermal paper.

Solution:
1. Request a higher-resolution image (at least 300 DPI for scans).
2. Ask for even, bright light, or adjusted contrast.
3. Rotate the image if the text is sideways.
4. Extract what is readable and mark unreadable fields `null` with a warning.

### Error: "VAT calculation mismatch"

Cause: rounding across many lines, a mix of 18% and zero-rated lines (fresh produce, for example), or an invoice from before 2025 at 17%. Israel has no reduced positive rate: a supply is standard-rated, zero-rated, or exempt.

Solution:
1. Check the invoice date and use 17% from 1 October 2015 to 31 December 2024.
2. Look for zero-rated lines and exclude them from the 18% check.
3. Apply the Step 7 tolerance (0.05 NIS, up to 0.10 NIS with many lines or a cash rounding line).
4. Beyond tolerance, mark `review` and keep the printed values.

### Error: "Unknown merchant, cannot auto-categorize"

Cause: a small business or a trade name that differs from the registered name.

Solution:
1. Categorize from the line items.
2. Look for keywords ("מסעדה", "תדלוק").
3. Default to "General Expenses (הוצאות כלליות)" with `needs_review: true`.

### Error: "Date format ambiguous"

Cause: dates with no separators, such as "080326".

Solution:
1. Assume DD/MM/YYYY.
2. Cross-check the printed weekday or Hebrew date.
3. When still ambiguous, output both readings and flag for confirmation.
