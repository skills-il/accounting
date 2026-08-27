---
name: israeli-receipt-scanner
description: OCR and parse Israeli receipts and invoices with Hebrew and English text extraction. Extracts merchant name, date, total amount in NIS, VAT amount, receipt or invoice number, payment method, and VAT registration number (osek murshe). Handles common Israeli retail formats including supermarkets, gas stations, restaurants, and online purchases. Auto-categorizes expenses into standard Israeli accounting categories and outputs structured JSON or CSV ready for import into accounting software. Use when you need to digitize, extract data from, or categorize Israeli receipts and tax invoices. Do NOT use for non-Israeli receipt formats, handwritten notes without printed text, or bank statement reconciliation.
license: MIT
allowed-tools: Bash(python:*) Read Edit Write WebFetch
compatibility: Requires Claude Code with vision capabilities for image-based OCR
---


# Israeli Receipt Scanner

## Legal notice

This is a free information tool operated by an AI model. It explains the rules and calculates from the figures you enter, but it does not examine your full circumstances and does not constitute tax advice. All of its outputs are produced automatically, with no involvement, review, or approval by a tax adviser or accountant, and an AI model may err, omit data, or present a wrong conclusion. The binding computation is the Tax Authority's and responsibility for reporting is yours. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person, and all use of its output is the user's sole responsibility.


## Instructions

### Step 1: Prepare the Receipt Image or Text

Identify the input format. The receipt may be provided as:

- A photographed or scanned image (JPEG, PNG, PDF)
- Raw OCR text already extracted by another tool
- A digital receipt in plain text or HTML format

If the input is an image, use vision capabilities to read the text. Israeli receipts typically contain a mix of Hebrew (right-to-left) and English (left-to-right) text, along with numbers. Pay attention to bidirectional text rendering, as merchant names are usually in Hebrew while product codes and amounts use Latin numerals.

### Step 2: Identify the Document Type

Determine whether the document is:

- **Tax Invoice (חשבונית מס)**: Contains a VAT registration number, itemized VAT amount, and the header "חשבונית מס" or "חשבונית מס / קבלה". These are issued by authorized businesses (osek murshe) and are required for VAT deduction claims.
- **Receipt (קבלה)**: A simpler proof of payment without detailed VAT breakdown. Header typically says "קבלה" only.
- **Tax Invoice / Receipt combo (חשבונית מס / קבלה)**: A combined document serving as both invoice and receipt, common in retail. Look for the dual header.
- **Proforma Invoice (חשבונית עסקה)**: A preliminary invoice before payment, not valid for VAT deduction.

Look for the document type indicator near the top of the receipt, usually printed in bold or larger font immediately below the merchant header.

The document type drives input-VAT deductibility, but the document type alone is NOT sufficient. Only a **tax invoice (חשבונית מס)** or **tax invoice / receipt (חשבונית מס / קבלה)** issued by an osek murshe with a valid 9-digit osek number can support an input-VAT deduction, AND it must be an original invoice issued **in the buyer's name** ("על שמו כדין"). Above the small-sum threshold set by ITA regulations the buyer's name and the buyer's VAT/osek number are mandatory invoice fields. A generic retail slip with no printed buyer (a typical supermarket חשבונית מס / קבלה handed to a walk-in customer) does NOT entitle that customer to deduct input VAT. A plain receipt (קבלה), a proforma invoice (חשבונית עסקה), or any document from an osek patur also cannot. An osek patur is defined in section 1 of the VAT Law as a dealer whose turnover across all their businesses does not exceed NIS 122,833 a year (or a higher figure set by the Finance Minister), and by definition issues no tax invoice.

A foreign document (US sales tax, EU VAT, etc.) is never an Israeli tax invoice: its tax line must NEVER populate `vat_amount` or `vat_deductible`. Israeli input VAT does not exist on such a document (reverse-charge self-reporting applies instead).

### Step 3: Extract Core Fields

Parse the following fields from the receipt text:

1. **Merchant Name (שם העסק)**: Usually the first line, in Hebrew. May also include an English transliteration or brand name.
2. **VAT Registration Number (מספר עוסק מורשה / ח.פ.)**: A 9-digit number, often prefixed with "עוסק מורשה" or "ח.פ.". Located near the merchant header.
   - **Supplier Type (`supplier_type`)**: classify the issuer as `osek_murshe` (charges and itemizes VAT), `osek_patur` (exempt dealer, no VAT breakdown), or `unknown`. An osek-patur invoice carries no deductible input VAT.
3. **Buyer Name (שם הקונה / שם הלקוח)** and **Buyer VAT Number (`buyer_name`, `buyer_vat_number`)**: The name (and, above the small-sum threshold, the VAT/osek number) of the party the invoice was issued TO. Set both to `null` when the document carries no printed buyer (typical for walk-in retail slips). These drive deductibility: input VAT is deductible only when the invoice is in the buyer's name and that buyer matches the business claiming the deduction.
4. **Branch/Address (כתובת)**: Street address, city. Useful for expense location tracking.
5. **Date (תאריך)**: Israeli receipts use DD/MM/YYYY format. Look for "תאריך" label or a date near the top.
6. **Time (שעה)**: Often adjacent to the date.
7. **Receipt/Invoice Number (מספר חשבונית / מספר קבלה)**: A sequential number, look for "מס' חשבונית", "מספר קבלה", or "מס' אסמכתא".
8. **Allocation Number (מספר הקצאה)**: A SHAAM-issued number printed on B2B tax invoices above the current threshold (`allocation_number: string|null`). Set to `null` if absent. See the Allocation Number section for the threshold timeline.
9. **Line Items**: Product name (Hebrew), quantity, unit price, and line total. Supermarket receipts list items with barcodes.
10. **Subtotal (סכום לפני מע"מ)**: Amount before VAT.
11. **VAT Amount (מע"מ)**: Currently 18% in Israel (as of 2026). Look for "מע"מ" label.
12. **Total Amount (סה"כ)**: The final amount paid, in NIS. Look for "סה"כ", "סה"כ לתשלום", or "סכום כולל".
13. **Payment Method (אמצעי תשלום)**: Credit card (last 4 digits), cash (מזומן), digital wallet, or bank transfer.
14. **Number of Payments (תשלומים)**: If paid in installments, the number and amount per installment.

### Step 4: Handle Common Israeli Retailer Formats

Different Israeli retailers use distinct receipt layouts:

**Supermarkets (Shufersal, Rami Levy, Yochananof, Osher Ad)**:
- Barcode-based item listing with Hebrew product names
- Club member discounts shown as negative line items
- Separate sections for produce (weighed items) vs packaged goods
- Deposit charges (פיקדון) for bottles
- Look for "חסכת" (you saved) summary line

**Gas Stations (Paz, Sonol, Delek, Ten)**:
- Fuel type (95, 98, diesel/סולר) and liters
- Price per liter
- Odometer reading (sometimes)
- Car wash or convenience store items as separate line items

**Restaurants and Cafes**:
- Service charge (שירות) as a percentage, usually 10-12%
- Tip line (טיפ) may be blank or filled
- Table number and server name
- Split bill indicators

**Online Purchases (invoices from Israeli e-commerce)**:
- Digital format, often PDF
- Shipping charges (משלוח) as separate line item
- Order number in addition to invoice number

### Step 5: Auto-Categorize the Expense

Map the merchant and items to standard Israeli accounting categories commonly used in bookkeeping:

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

Use the merchant name and item descriptions to determine the most likely category. If ambiguous, default to "General Expenses (הוצאות כלליות)" and flag for manual review.

### Step 6: Output Structured Data

Generate the extracted data in a structured format. Default to JSON:

```json
{
  "document_type": "tax_invoice_receipt",
  "merchant": {
    "name_he": "שופרסל דיל",
    "name_en": "Shufersal Deal",
    "vat_registration": "520044078",
    "supplier_type": "osek_murshe",
    "branch": "סניף רמת אביב",
    "address": "רחוב איינשטיין 15, תל אביב"
  },
  "buyer_name": null,
  "buyer_vat_number": null,
  "document_number": "12345678",
  "allocation_number": null,
  "date": "2026-03-08",
  "time": "14:32",
  "items": [
    {
      "description": "חלב תנובה 3% 1 ליטר",
      "quantity": 2,
      "unit_price": 6.90,
      "total": 13.80
    }
  ],
  "subtotal": 245.50,
  "vat_rate": 0.18,
  "vat_amount": 44.19,
  "vat_deductible": false,
  "total": 289.69,
  "currency": "ILS",
  "payment": {
    "method": "credit_card",
    "card_last_four": "4532",
    "installments": 1
  },
  "category": "groceries",
  "category_he": "מזון ומכולת",
  "needs_review": true,
  "warnings": ["No buyer printed on the invoice; not deductible as an input-VAT invoice for any specific business without an invoice issued in the buyer's name"]
}
```

For CSV output, flatten the structure with these columns:
`date, document_type, document_number, allocation_number, merchant_name, vat_registration, supplier_type, buyer_name, buyer_vat_number, subtotal, vat_amount, vat_deductible, deductible_fraction, deductibility_basis, needs_review, warnings, total, payment_method, category`

`vat_deductible` is a boolean, but regulation 18(ב) produces two-thirds and one-quarter outcomes that a boolean cannot carry, and collapsing them either over-claims or under-claims. So carry three companion fields and never drop them on export:

- `deductible_fraction`: `1`, `0.667`, `0.25`, `0` or `null` when unknown.
- `deductibility_basis`: the provision relied on, for example `"reg 14(a) - private car purchase, no deduction"` or `"reg 18(b)(2) - mainly business use"`.
- `needs_review` and `warnings`: every caveat the decision path generated. These must appear in the CSV too; exporting `vat_deductible` without them silently destroys the reasoning behind it.

Set `vat_deductible` to `true` ONLY when ALL of these hold: (a) the document is a חשבונית מס or חשבונית מס / קבלה issued by an osek murshe with a valid 9-digit osek number; (b) the purchase is FOR THE BUSINESS (לצורכי העסק), not private consumption; (c) the invoice is issued in the buyer's name matching the business's own osek number, EXCEPT that a small-sum tax invoice or a cash-register (קופה-רושמת) slip below the ITA small-sum threshold may lawfully omit the buyer's VAT number and is still deductible for a genuine business purchase, so do NOT hard-deny a small no-buyer slip, set `needs_review: true` for the bookkeeper to confirm business use; and (d) when the net amount is above the SHAAM allocation threshold for the invoice's date, an allocation number is present. Set it to `false` (and `needs_review: true`) for an inherently-private category (groceries, personal clothing, personal medical, and the like), **any hosting or entertainment expense (הוצאות אירוח: restaurants, catering, hospitality)**, **any employee benefit (טובת הנאה לעובד: a staff meal, gift, housing or entertainment)**, a plain קבלה, a חשבונית עסקה (proforma), an osek-patur supplier, a vehicle document (Step 7 item 9 decides which of the three vehicle outcomes applies; do not decide it here), any foreign document, or a LARGE invoice (above the small-sum threshold) with no matching buyer.

### Step 7: Validate Extracted Data

Perform validation checks on the extracted data:

1. **VAT Calculation**: Verify that `total = subtotal + vat_amount` (tolerance of 0.05 NIS for rounding). Current Israeli VAT rate is 18%. Not every Israeli receipt carries VAT: Eilat Free-Trade-Zone transactions and zero-rated supplies (exports, some fresh produce) legitimately show no VAT line. Do NOT treat a VAT-less Israeli receipt as an extraction error or automatically as an osek-patur, set `vat_rate: 0`, `vat_amount: 0`, note the zero-rated/Eilat reason, and skip the 18% mismatch check for it.
2. **Date Format**: Ensure the date is valid and not in the future.
3. **VAT Registration**: Validate that the osek murshe number is exactly 9 digits. The 9-digit number also carries a check digit, which should be validated with the Luhn mod-10 algorithm (the same scheme Israeli ID-type numbers use). Do NOT invent any other checksum formula.
4. **Line Item Totals**: Verify that sum of line items equals the subtotal (within rounding tolerance).
5. **Currency**: Confirm amounts are in NIS. Flag if foreign currency symbols are detected. A foreign document's tax line (US sales tax, EU VAT, etc.) must NEVER populate `vat_amount` or `vat_deductible`; it is not Israeli input VAT (reverse-charge applies). Set `vat_deductible: false` and add a foreign-vendor warning.
6. **Allocation Number Threshold (date-aware)**: If the document is a tax invoice (חשבונית מס or חשבונית מס / קבלה), select the threshold band from the INVOICE's own date (not today): NIS 20,000 for invoices dated in 2025, NIS 10,000 for January through May 2026, NIS 5,000 from 1 June 2026 onward. If the subtotal (net) exceeds the band for that date AND `allocation_number` is null, emit a warning that without an allocation number the input VAT is not deductible. Digitizing an older shoebox invoice must not throw a false warning under today's lower band.
7. **Buyer Identity (with small-sum carve-out)**: Confirm the invoice is issued in the buyer's name and that `buyer_vat_number` matches the business's own osek number. If a LARGE invoice (above the ITA small-sum threshold) has no printed buyer, or the buyer does not match, set `vat_deductible: false` and `needs_review: true`, and warn that the supplier side is valid but the invoice is not in the buyer's name. BELOW the small-sum threshold, however, a valid חשבונית מס or קופה-רושמת slip may lawfully omit the buyer's VAT number, so do NOT hard-deny it: set `needs_review: true` and defer to the bookkeeper to confirm the purchase is for the business.
8. **Six-Month Deduction Window**: Input VAT must be claimed within 6 months of the invoice issue date. If the invoice date is more than 6 months in the past, emit a warning that the invoice may be past the deduction window.
9. **Deductibility Flag**: Set `vat_deductible: true` only when ALL hold: a חשבונית מס / חשבונית מס / קבלה from an osek murshe with a valid 9-digit osek number; the purchase is for the business, not private consumption; the invoice is within the six-month window; an allocation number when above the date-aware threshold; the buyer condition in item 7 (with its small-sum carve-out); and the category is not blocked. Set `false` for an inherently-private-consumption item, a plain קבלה, a חשבונית עסקה (proforma), an osek-patur supplier, or a foreign document.

   **Two absolute bars that no business-purpose argument overcomes. Check them BEFORE anything else, because they defeat an otherwise perfect invoice.**

   - **Hosting and entertainment (regulation 16).** "לא יהא ניתן לניכוי מס תשומות בשל הוצאות אירוח, פרט לניכוי מס תשומות על הוצאה לאירוח אדם מחוץ לארץ." Input VAT on hosting expenses is not deductible, with the single exception of hosting a person from abroad. A restaurant חשבונית מס issued to the company, from an osek murshe, under the allocation band and inside the six-month window satisfies every other condition in this list and is STILL barred. Set `vat_deductible: false` and `needs_review: true` so the bookkeeper can consider the from-abroad exception.
   - **Employee benefits (regulation 15א).** Input VAT on a benefit provided to an employee (a meal, housing, a gift, entertainment) is not deductible unless it is proved to the Director's satisfaction that the input was sold or supplied to the employee as a service AND that sale is included in the dealer's periodic return as a taxable transaction. Treat as `false` with `needs_review: true`.

   **One bar that is softer than it looks (regulation 12ג).** An invoice NOT in the dealer's name is normally fatal, but the Director may nonetheless allow the deduction where it is proved the inputs served the business and the input tax is for telephone, water, gas, electricity "or expenses of that kind". A utility bill still in a landlord's or a previous tenant's name is one of the commonest items in a real shoebox, so do NOT hard-deny it: set `vat_deductible: false` with `needs_review: true` and note that regulation 12ג may apply.

   **Vehicles: separate the PURCHASE of the car from its RUNNING COSTS. They have different rules and the difference is total, not marginal.**

   - **Buying or importing a private car (רכב פרטי) is a complete bar.** Regulation 14(א) of the VAT Regulations: the tax imposed on the sale of a private car to a dealer, or on its import by a dealer, **is not deductible at all**. Not two-thirds, not a quarter, nothing. Regulation 14(ב) carves out only a dealer whose main business is selling vehicles (holding the car solely for resale), and a car used exclusively for driving instruction, for rental by a rental business, for passenger transport by a transport business, or for organised tours. For a car-purchase invoice outside those carve-outs, set `vat_deductible: false` without needing any further test.
   - **Running costs, including fuel, are a mixed-use question, not a vehicle rule.** Regulation 18(ב) sets the general default for ANY input used partly for the business and partly not, vehicles included: if the Director has fixed the non-business proportion, that determination governs and is treated as an assessment; if not, the dealer may deduct **two-thirds** where use is mainly for the business and **one-quarter** where it is mainly private. Do not present those fractions as a vehicle-specific rule, and do not apply them to a car purchase.
   - **A commercial or work vehicle outside the private-car definition** (truck, taxi, driving-school or rental vehicle) is not caught by regulation 14 at all, so its input VAT follows the ordinary rules and is fully deductible where the use is wholly for the business.

   For any vehicle or fuel document, set `needs_review: true` and let the bookkeeper confirm the vehicle class and the use split rather than hard-coding one outcome.

10. **Cash-payment cap (Cash Law)**: under the Law for Reducing the Use of Cash (חוק לצמצום השימוש במזומן), a transaction where one party is a business may not be paid in cash above NIS 6,000, **or 10% of the transaction value if that is lower**, so on a large invoice the binding cap is often well under 6,000. Between two private individuals the cap is NIS 15,000, and NIS 50,000 for a vehicle sale. If `payment.method` is cash and the amount exceeds the applicable cap, warn the bookkeeper rather than silently accepting it. The consequence is not merely a penalty: under section 38(א2) of the VAT Law, input VAT on that invoice is **disallowed** where it was decided the payment breached the Cash Law AND a monetary penalty was imposed under section 9 of that law, unless the dealer satisfies the Director that tax was duly paid on the transaction. If a penalty appeal succeeds, the over-paid tax is refunded with linkage and interest. State those conditions: a cash payment above the cap does not by itself void the deduction.

11. **Six-month deduction window (section 38(א) of the VAT Law), the authoritative statement of the rule flagged in item 8**: input VAT may be deducted only **within six months of the date the invoice was issued**. This tool exists to digitize shoeboxes of accumulated paper, so it will routinely meet invoices already outside the window. Compare the invoice's own date with today's and, when more than six months have passed, set `needs_review: true` and warn that the deduction window has closed, whatever the other conditions say. Obtaining an allocation number retroactively does NOT restart it: section 47(א2)(4) says a number allocated later changes nothing about the section 38(א) date.

If validation fails, include a `warnings` array in the output with specific issues found.

## Examples

### Example 1: Supermarket Receipt

User says: "Scan this Shufersal receipt and extract the data."

The user provides an image of a Shufersal receipt. The agent:

1. Reads the receipt image using vision capabilities
2. Identifies the document as "חשבונית מס / קבלה" (tax invoice / receipt)
3. Extracts merchant: "שופרסל דיל, סניף רמת אביב"
4. Extracts VAT registration: "520044078"
5. Parses 12 line items including produce, dairy, and packaged goods
6. Identifies club discount line: "הנחת מועדון: -15.40"
7. Extracts totals: subtotal 312.80, VAT 56.30, total 369.10
8. Payment: credit card ending 4532, 1 installment
9. Auto-categorizes as "groceries" (מזון ומכולת)
10. No buyer is printed on this walk-in slip, so sets vat_deductible: false and needs_review: true with a "no buyer printed" warning
11. Outputs structured JSON with all fields populated

Result: Complete JSON output with all 12 items, validated totals (VAT check passed), category assignment, and vat_deductible: false (needs_review) because the supermarket slip was not issued in the business's name.

### Example 2: Gas Station Receipt with Multiple Items

User says: "Parse this Sonol gas station receipt. I need it for my expense report."

The user provides a Sonol receipt image. The agent:

1. Reads the receipt and identifies it as a tax invoice
2. Extracts merchant: "סונול, תחנת שירות הרצליה"
3. Parses two line items: fuel (95 octane, 35.2 liters at 7.45/L = 262.24) and a convenience store purchase (water bottle, 8.90)
4. Extracts totals: subtotal 229.78, VAT 41.36, total 271.14
5. Payment: credit card ending 8891
6. Since the receipt contains both fuel and a store item, creates two category assignments:
   - Fuel (דלק): 262.24 NIS
   - General (כללי): 8.90 NIS
7. Sets `vat_deductible: false` and `needs_review: true` because private-car fuel is a mixed-use input under regulation 18(ב) (two-thirds when use is mainly for the business, a quarter when mainly private), and flags the use split for the bookkeeper rather than claiming full deduction
8. Outputs structured JSON with split categorization

Result: JSON with split expense categories, a vehicle/fuel deductibility flag, and a note that the receipt covers two expense types.

### Example 3: Restaurant Tax Invoice

User says: "I have a restaurant receipt from a business lunch. Extract the details for tax deduction purposes."

The user provides a restaurant receipt. The agent:

1. Reads the receipt and identifies it as "חשבונית מס / קבלה"
2. Extracts merchant: "מסעדת רפאל, תל אביב"
3. Extracts VAT registration number for tax deduction eligibility
4. Parses food items, drinks, and a 12% service charge
5. Flags that input VAT on business meals and hosting (אירוח) is generally NOT deductible in Israel (narrow exceptions aside, e.g. hosting guests from abroad), so `vat_deductible` should usually be `false` for this receipt, and advises confirming with the bookkeeper
6. Outputs JSON with a `tax_notes` field: "Input VAT on business meals/hosting is generally non-deductible in Israel; consult your bookkeeper for any exception"

Result: Complete JSON with tax-relevant notes for the accountant.

## Bundled Resources

> **Pending.** Earlier versions of this skill listed `scripts/receipt_parser.py`, `scripts/export_csv.py`, `references/israeli-vat-rates.md`, and `references/receipt-field-glossary.md`, but those files were never shipped. They are noted here for traceability and pending real implementations. For batch OCR today, use vision-LLM (Claude Sonnet vision, GPT-4o, Gemini 2.x) over Tesseract/EasyOCR, with your own shell or Python wrapper.

## Allocation Number Field

For B2B tax invoices at or above the current SHAAM threshold, the printed invoice must include an **allocation number (mispar haktza'a)** alongside the standard tax-invoice fields. Threshold timeline:

- Jan 2025 - Dec 2025: required when net amount > NIS 20,000
- Jan - May 2026: required when net amount > NIS 10,000
- **Jun 2026 onwards (current): required when net amount > NIS 5,000**

When scanning a B2B tax invoice, extract `allocation_number: string|null` and flag missing values on invoices that exceed the band that applies to the invoice's own date (not today's date). A plain receipt (קבלה) and a proforma invoice (חשבונית עסקה) do not require allocation numbers, but a חשבונית מס / קבלה (tax invoice / receipt) above the threshold DOES require one, just like a plain חשבונית מס.

**Zero-rated transactions are exempt.** Section 47(א2)(1) applies the allocation mechanism only to a tax invoice issued for a transaction whose rate of tax is not zero. So do NOT raise a missing-allocation warning on a large zero-rated invoice, which is the same population as the Eilat and export branch above.

**What a missing number actually costs, and who bears it.** Section 38(א1) sits in the input-tax chapter and disallows the BUYER's deduction. It does not make the invoice invalid: the document remains a lawful tax invoice, the seller still owes output tax on it, and section 47(א2)(3)(ג)(2) expressly contemplates a seller issuing an invoice with no allocated number and attaches only the section 38(א1) consequence. Invalidity is a different provision (section 50, double tax on a document issued unlawfully) and missing allocation numbers are not in it. Say "the buyer cannot deduct", never "the invoice is invalid".

**The seller is only obliged to ask when the buyer demands it.** Section 47(א2)(1) makes the request mandatory "לפי דרישת הקונה" on an above-threshold transaction. A buyer who never demanded a number and later cannot deduct has no complaint about the invoice itself, so if the field is empty the practical advice is to go back to the supplier and demand allocation, not to reject the document.

**The number can also have been refused.** Section 47(א2)(3) lets the Director decline to allocate where there is reasonable ground to suspect the invoice would be issued unlawfully, with a hearing and objection procedure. An empty field may mean the supplier never asked, or that allocation was refused; those are different problems and only the supplier can say which.

## Foreign-Vendor Receipts

App Store / Google Play / AWS / Azure / GCP / Stripe / OpenAI / Anthropic and similar foreign-issued receipts are NOT Israeli tax invoices and **cannot be used for VAT input deduction in Israel** without a separate reverse-charge workflow: the importer of services issues a self-invoice (חשבונית עצמית), self-reports the output tax (mas asakot), and (if a fully-deducting osek murshe) simultaneously claims it as input tax; an osek patur / non-profit / financial institution that cannot fully offset bears the self-reported tax as a real cost. This self-invoice path is for imported SERVICES / SaaS. Imported physical GOODS are different: their Israeli VAT is paid at customs and deducted via the import entry (rashimon yevu), not via a self-invoice, so do not tag a foreign goods receipt as a services reverse-charge. The skill should auto-tag foreign receipts and surface the reverse-charge / self-invoice (or customs-import) requirement, not categorize them as standard SaaS expenses.

## Gotchas

- Israeli receipts contain a mix of Hebrew (RTL) and English/numbers (LTR) text on the same line. OCR engines may reverse the reading order or scramble bidirectional text. Always verify that amounts appear next to the correct line items.
- The Hebrew date format on receipts is DD/MM/YYYY, but some thermal printers use abbreviated formats like DD/MM/YY. Agents may misparse 01/03/26 as January 3 instead of March 1 (or 2026).
- Israeli receipts from osek patur (exempt dealers) do not contain VAT breakdowns. Agents may attempt to extract VAT from these receipts and produce incorrect calculations.
- Thermal receipt paper degrades quickly in Israeli summer heat. OCR quality on faded receipts drops significantly, especially for Hebrew characters that are smaller and denser than Latin text.
- Israeli business numbers (mispar osek) on receipts are 9 digits with a check digit. Agents may extract partial numbers or not validate the check digit, leading to incorrect business identification. Validate the check digit with the Luhn mod-10 algorithm (the scheme Israeli ID-type numbers use); do not invent any other formula.
- A credit-card voucher / slip (שובר אשראי) alone is NOT a tax invoice and cannot support an input-VAT deduction, even for a business. It only proves payment. If the scanned document is a card voucher rather than a חשבונית מס, set `vat_deductible: false` and advise the user to obtain the tax invoice.


## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Tesseract OCR | https://github.com/tesseract-ocr/tesseract | Hebrew language data, OCR quality tuning |
| EasyOCR | https://github.com/JaidedAI/EasyOCR | No Hebrew model, not usable for Hebrew receipts; use Tesseract `heb` or a vision-LLM |
| Israel Tax Authority | https://www.gov.il/he/departments/israel_tax_authority | Tax invoice fields, osek murshe validation, VAT rules |
| Kol Zchut | https://www.kolzchut.org.il/he | Required receipt fields, small business obligations |
| Pillow (PIL) | https://pillow.readthedocs.io/en/stable/ | Image preprocessing for OCR (rotation, deskew) |

## Troubleshooting

### Error: "Unable to read Hebrew text from image"

Cause: The receipt image may be low resolution, poorly lit, or the Hebrew text may be in a decorative font that is difficult to parse. Thermal receipt paper often fades, making text barely visible.

Solution:
1. Request a higher-resolution image (at least 300 DPI for scanned documents)
2. If the receipt is faded, ask the user to adjust contrast or take the photo under bright, even lighting
3. Try rotating the image if text appears sideways or upside down
4. For partially readable receipts, extract what is possible and mark unreadable fields as `null` with a warning

### Error: "VAT calculation mismatch"

Cause: The calculated VAT (subtotal * 0.18) does not match the VAT amount printed on the receipt. This can happen due to rounding across many line items or a mix of standard-rated (18%), zero-rated (0%), and exempt items. Israel has no reduced positive VAT rate, a supply is 18%, zero-rated, or exempt, so do not assume a middle rate.

Solution:
1. Check if some items are VAT-exempt (e.g., fruits and vegetables in some contexts)
2. Verify the VAT rate used, the standard rate is 18% but confirm against the receipt
3. Allow a rounding tolerance of up to 0.10 NIS for receipts with many line items
4. If the mismatch exceeds tolerance, flag it in the output warnings but still include the as-printed values

### Error: "Unknown merchant, cannot auto-categorize"

Cause: The merchant name does not match any known retailer in the categorization database. This is common with small businesses, market stalls, or businesses using trade names different from their registered names.

Solution:
1. Attempt categorization based on the line items instead of the merchant name
2. Check if the VAT registration number maps to a known business category
3. Look for keywords in the receipt (e.g., "מסעדה" for restaurant, "תדלוק" for fuel)
4. Default to "General Expenses (הוצאות כלליות)" and include a `needs_review: true` flag

### Error: "Date format ambiguous"

Cause: Some receipts print dates without clear separators or use inconsistent formats. For example, "080326" could be interpreted as 08/03/2026 (DD/MM/YYYY) or 03/08/2026 (MM/DD/YYYY).

Solution:
1. Israeli receipts use DD/MM/YYYY format by default, apply this assumption
2. Cross-reference with the day of week if printed on the receipt
3. If the receipt includes a Hebrew date, use it as a secondary validation
4. When truly ambiguous, output both possible dates and flag for manual confirmation
