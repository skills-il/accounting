---
name: israeli-receipt-scanner
description: >-
  OCR and parse Israeli receipts and invoices with Hebrew and English text extraction.
  Extracts merchant name, date, total amount in NIS, VAT amount, receipt or invoice number,
  payment method, and VAT registration number (osek murshe). Handles common Israeli retail
  formats including supermarkets, gas stations, restaurants, and online purchases.
  Auto-categorizes expenses into standard Israeli accounting categories and outputs
  structured JSON or CSV ready for import into accounting software.
  Use when you need to digitize, extract data from, or categorize Israeli receipts and
  tax invoices. Do NOT use for non-Israeli receipt formats, handwritten notes without
  printed text, or bank statement reconciliation.
license: MIT
allowed-tools: "Bash(python:*) Read Edit Write WebFetch"
compatibility: "Requires Claude Code with vision capabilities for image-based OCR"
metadata:
  author: skills-il
  version: 1.0.0
  category: accounting
  tags:
    he:
      - סורק-קבלות
      - זיהוי-תווים
      - עברית-אופטי
      - מעקב-הוצאות
      - חשבוניות
      - חשבונאות
    en:
      - receipt-scanner
      - ocr
      - hebrew-ocr
      - expense-tracking
      - invoices
      - accounting
  display_name:
    he: "סורק קבלות ישראלי"
    en: "Israeli Receipt Scanner"
  display_description:
    he: "סריקה וניתוח קבלות וחשבוניות ישראליות עם חילוץ טקסט בעברית ואנגלית"
    en: "OCR and parse Israeli receipts and invoices with Hebrew and English text extraction"
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
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

### Step 3: Extract Core Fields

Parse the following fields from the receipt text:

1. **Merchant Name (שם העסק)**: Usually the first line, in Hebrew. May also include an English transliteration or brand name.
2. **VAT Registration Number (מספר עוסק מורשה / ח.פ.)**: A 9-digit number, often prefixed with "עוסק מורשה" or "ח.פ.". Located near the merchant header.
3. **Branch/Address (כתובת)**: Street address, city. Useful for expense location tracking.
4. **Date (תאריך)**: Israeli receipts use DD/MM/YYYY format. Look for "תאריך" label or a date near the top.
5. **Time (שעה)**: Often adjacent to the date.
6. **Receipt/Invoice Number (מספר חשבונית / מספר קבלה)**: A sequential number, look for "מס' חשבונית", "מספר קבלה", or "מס' אסמכתא".
7. **Line Items**: Product name (Hebrew), quantity, unit price, and line total. Supermarket receipts list items with barcodes.
8. **Subtotal (סכום לפני מע"מ)**: Amount before VAT.
9. **VAT Amount (מע"מ)**: Currently 18% in Israel (as of 2026). Look for "מע"מ" label.
10. **Total Amount (סה"כ)**: The final amount paid, in NIS. Look for "סה"כ", "סה"כ לתשלום", or "סכום כולל".
11. **Payment Method (אמצעי תשלום)**: Credit card (last 4 digits), cash (מזומן), digital wallet, or bank transfer.
12. **Number of Payments (תשלומים)**: If paid in installments, the number and amount per installment.

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
    "branch": "סניף רמת אביב",
    "address": "רחוב איינשטיין 15, תל אביב"
  },
  "document_number": "12345678",
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
  "vat_amount": 37.44,
  "total": 289.69,
  "currency": "ILS",
  "payment": {
    "method": "credit_card",
    "card_last_four": "4532",
    "installments": 1
  },
  "category": "groceries",
  "category_he": "מזון ומכולת"
}
```

For CSV output, flatten the structure with these columns:
`date, document_type, document_number, merchant_name, vat_registration, subtotal, vat_amount, total, payment_method, category`

### Step 7: Validate Extracted Data

Perform validation checks on the extracted data:

1. **VAT Calculation**: Verify that `total = subtotal + vat_amount` (tolerance of 0.05 NIS for rounding). Current Israeli VAT rate is 18%.
2. **Date Format**: Ensure the date is valid and not in the future.
3. **VAT Registration**: Validate that the osek murshe number is exactly 9 digits.
4. **Line Item Totals**: Verify that sum of line items equals the subtotal (within rounding tolerance).
5. **Currency**: Confirm amounts are in NIS. Flag if foreign currency symbols are detected.

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
7. Extracts totals: subtotal 312.80, VAT 47.66, total 369.10
8. Payment: credit card ending 4532, 1 installment
9. Auto-categorizes as "groceries" (מזון ומכולת)
10. Outputs structured JSON with all fields populated

Result: Complete JSON output with all 12 items, validated totals (VAT check passed), and category assignment.

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
7. Outputs structured JSON with split categorization

Result: JSON with split expense categories and a note that the receipt covers two expense types.

### Example 3: Restaurant Tax Invoice

User says: "I have a restaurant receipt from a business lunch. Extract the details for tax deduction purposes."

The user provides a restaurant receipt. The agent:

1. Reads the receipt and identifies it as "חשבונית מס / קבלה"
2. Extracts merchant: "מסעדת רפאל, תל אביב"
3. Extracts VAT registration number for tax deduction eligibility
4. Parses food items, drinks, and a 12% service charge
5. Flags that for business meal deductions in Israel, only a portion of restaurant expenses is deductible for VAT purposes
6. Outputs JSON with a `tax_notes` field: "Business meal VAT deduction is subject to Israeli tax authority limitations"

Result: Complete JSON with tax-relevant notes for the accountant.

## Bundled Resources

### Scripts
- `scripts/receipt_parser.py` -- Python utility for batch processing receipt images. Run: `python scripts/receipt_parser.py --help`
- `scripts/export_csv.py` -- Convert JSON receipt data to CSV format for accounting software import. Run: `python scripts/export_csv.py --input receipts.json --output expenses.csv`

### References
- `references/israeli-vat-rates.md` -- Historical Israeli VAT rates and thresholds. Consult when validating VAT calculations on older receipts.
- `references/receipt-field-glossary.md` -- Hebrew-English glossary of common receipt fields and terms. Consult when encountering unfamiliar Hebrew terms on receipts.

## Troubleshooting

### Error: "Unable to read Hebrew text from image"

Cause: The receipt image may be low resolution, poorly lit, or the Hebrew text may be in a decorative font that is difficult to parse. Thermal receipt paper often fades, making text barely visible.

Solution:
1. Request a higher-resolution image (at least 300 DPI for scanned documents)
2. If the receipt is faded, ask the user to adjust contrast or take the photo under bright, even lighting
3. Try rotating the image if text appears sideways or upside down
4. For partially readable receipts, extract what is possible and mark unreadable fields as `null` with a warning

### Error: "VAT calculation mismatch"

Cause: The calculated VAT (subtotal * 0.18) does not match the VAT amount printed on the receipt. This can happen due to rounding across many line items, mixed VAT-exempt and VAT-inclusive items, or items with reduced VAT rates.

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
