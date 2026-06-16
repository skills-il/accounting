# Israeli SHAAM Document Type Codes

These are the official "Israel Invoice" document type codes from Table 2.5 of the Tax Authority API spec (v2.0, 7/2024). The allocation-number column reflects the spec; it applies only when the net amount is above the current threshold.

## Standard Types

| Code | Hebrew | English | VAT | Allocation # |
|------|--------|---------|-----|--------------|
| 300 | heshbon / heshbon iska | Transaction Invoice | Demand for payment, not a tax invoice | Not required |
| 305 | hashbonit mas | Tax Invoice | Yes (18%) | Required above threshold |
| 310 | hashbonit mas tkufatit | Periodic Tax Invoice | Yes (18%) | Required above threshold |
| 320 | hashbonit mas / kabala | Tax Invoice / Receipt | Yes (18%) | Required above threshold |
| 330 | hashbonit mas zikui | Credit Invoice | Yes (reversal) | Not required |
| 332 | heshbon iska / proforma | Proforma Invoice | No (not a tax document) | Required (cash-basis special, see spec article 3.5) |

## v2 Additions (7/2024)

| Code | Hebrew | English | Allocation # |
|------|--------|---------|--------------|
| 340 | hashbonit mas hazmana | Reservation Tax Invoice | Required above threshold |
| 345 | hashbonit mas sochen | Agent Tax Invoice | Required above threshold |
| 348 | pkudat yoman | Log Command (lets a bookkeeper submit mandatory fields and receive allocation numbers) | Required above threshold |

There is no code 400 and no "self-billing" code in this taxonomy. A plain payment receipt (kabala) is not part of the allocation document set and never requires an allocation number; code 320 is specifically a combined tax-invoice-plus-receipt, not a standalone receipt.

## Required Fields by Type

### Type 305 / 320 (Tax Invoice / Tax Invoice + Receipt)
- Seller: Name, TIN, address
- Buyer: Name, TIN (if business), address
- Invoice number (sequential)
- Date
- Item descriptions, quantities, unit prices
- VAT amount (separate line)
- Total amount
- Allocation number (if above threshold)
- Payment method (for 320 only)

### Type 310 (Periodic Tax Invoice)
- Same fields as a tax invoice, aggregating a period's transactions
- Allocation number (if above threshold)

### Type 330 (Credit Invoice)
- All fields from the original invoice
- Reference to the original invoice number (mandatory linkage)
- Reason for credit
- Credit amount with VAT reversal
- No allocation number required

### Type 300 (Transaction Invoice)
- A demand for payment, not a tax invoice; does not entitle the buyer to deduct input VAT
- No allocation number required

### Type 332 (Proforma)
- Not a legal tax document; used for quotes and pre-billing
- Interacts with allocation only under the cash-basis special case (spec article 3.5)
