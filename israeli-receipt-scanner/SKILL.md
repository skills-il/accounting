---
name: israeli-receipt-scanner
description: OCR and parse Israeli receipts and invoices with Hebrew and English text extraction. Extracts merchant name, date, total amount in NIS, VAT amount, receipt or invoice number, payment method, and VAT registration number (osek murshe). Handles common Israeli retail formats including supermarkets, gas stations, restaurants, and online purchases. Auto-categorizes expenses into standard Israeli accounting categories and outputs structured JSON or CSV ready for import into accounting software. Use when you need to digitize, extract data from, or categorize Israeli receipts and tax invoices. Do NOT use for non-Israeli receipt formats, handwritten notes without printed text, or bank statement reconciliation.
license: MIT
allowed-tools: Bash(python:*) Read Edit Write WebFetch
compatibility: Requires Claude Code with vision capabilities for image-based OCR
---


# Israeli Receipt Scanner

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

The document type drives input-VAT deductibility, but the document type alone is NOT sufficient. Only a **tax invoice (חשבונית מס)** or **tax invoice / receipt (חשבונית מס / קבלה)** issued by an osek murshe with a valid 9-digit osek number can support an input-VAT deduction, AND it must be an original invoice issued **in the buyer's name** ("על שמו כדין"). Above the small-sum threshold set by ITA regulations the buyer's name and the buyer's VAT/osek number are mandatory invoice fields. A generic retail slip with no printed buyer (a typical supermarket חשבונית מס / קבלה handed to a walk-in customer) does NOT entitle that customer to deduct input VAT. A plain receipt (קבלה), a proforma invoice (חשבונית עסקה), or any document from an osek patur also cannot.

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
`date, document_type, document_number, allocation_number, merchant_name, vat_registration, supplier_type, buyer_name, buyer_vat_number, subtotal, vat_amount, vat_deductible, total, payment_method, category`

Set `vat_deductible` to `true` ONLY when ALL of these hold: (a) the document is a חשבונית מס or חשבונית מס / קבלה issued by an osek murshe with a valid 9-digit osek number; (b) the purchase is FOR THE BUSINESS (לצורכי העסק), not private consumption; (c) the invoice is issued in the buyer's name matching the business's own osek number, EXCEPT that a small-sum tax invoice or a cash-register (קופה-רושמת) slip below the ITA small-sum threshold may lawfully omit the buyer's VAT number and is still deductible for a genuine business purchase, so do NOT hard-deny a small no-buyer slip, set `needs_review: true` for the bookkeeper to confirm business use; and (d) when the net amount is above the SHAAM allocation threshold for the invoice's date, an allocation number is present. Set it to `false` (and `needs_review: true`) for an inherently-private category (groceries, personal clothing, personal medical, and the like), a plain קבלה, a חשבונית עסקה (proforma), an osek-patur supplier, a passenger-vehicle / fuel document (see Step 7), any foreign document, or a LARGE invoice (above the small-sum threshold) with no matching buyer.

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
9. **Deductibility Flag**: Set `vat_deductible: true` only when ALL hold: a חשבונית מס / חשבונית מס / קבלה from an osek murshe with a valid 9-digit osek number; the purchase is for the business, not private consumption; an allocation number when above the date-aware threshold; the buyer condition in item 7 (with its small-sum carve-out); and the category is not blocked. For a PASSENGER-vehicle document (private car and its running costs, including fuel) input VAT is restricted: a mixed business/private input deducts only two-thirds when use is mainly for the business (and as little as one-quarter when use is mainly private), so set `vat_deductible: false` with `needs_review: true`. A COMMERCIAL / work vehicle (רכב מסחרי, truck, taxi, driving-school or rental) is different: its fuel and running-cost input VAT is FULLY deductible, so flag `needs_review: true` for the bookkeeper to confirm the vehicle class rather than hard-coding the passenger-car restriction. Set `false` for an inherently-private-consumption item, a plain קבלה, a חשבונית עסקה (proforma), an osek-patur supplier, or a foreign document.

10. **Cash-payment cap (Cash Law)**: under the Law for Reducing the Use of Cash (חוק לצמצום השימוש במזומן), a business transaction generally may not be paid in cash above NIS 6,000. If `payment.method` is cash and `total` exceeds NIS 6,000, emit a warning that the cash payment may breach the cash-law cap, which can disallow the expense / input VAT and expose the business to a monetary penalty. Flag for the bookkeeper rather than silently accepting it.

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
7. Sets `vat_deductible: false` and `needs_review: true` because input VAT on passenger-vehicle fuel is restricted (mixed business/private use deducts only two-thirds when use is mainly for the business), and flags the mixed-use split for the bookkeeper rather than claiming full deduction
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

When scanning a B2B tax invoice, extract `allocation_number: string|null` and flag missing values on invoices that exceed the band that applies to the invoice's own date (not today's date). Without an allocation number, the buyer loses input-VAT deduction. A plain receipt (קבלה) and a proforma invoice (חשבונית עסקה) do not require allocation numbers, but a חשבונית מס / קבלה (tax invoice / receipt) above the threshold DOES require one, just like a plain חשבונית מס.

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
