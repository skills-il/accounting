# Israeli E-Invoice Mandate Timeline

## Legal Basis
The allocation-number requirement was enacted by the Economic Arrangements Law for budget
years 2023-2024 (Chok HaHitiyalut HaKalkalit, 5783-2023), which amended the VAT Law (Chok Maam):
section 47 governs the duty to obtain an allocation number on issuing a tax invoice, and section 38
makes the allocation number a condition for the buyer to deduct input VAT. It is a graduated
requirement that lowers the threshold year by year. (There is no "Amendment 157"; that citation was
incorrect.) The June 2026 step-down to 5,000 NIS took effect on schedule; the original
non-accelerated plan reached 5,000 NIS only in 2028.

## Progressive Threshold Reduction

| Effective Date | Threshold | Applies To |
|---------------|-----------|------------|
| May 4, 2024 | net > 25,000 NIS | Tax invoices (305, 310, 320, 340, 345, 348) |
| January 1, 2025 | net > 20,000 NIS | Tax invoices (305, 310, 320, 340, 345, 348) |
| January 1, 2026 | net > 10,000 NIS | Tax invoices (305, 310, 320, 340, 345, 348) |
| June 1, 2026 | net > 5,000 NIS | Tax invoices (305, 310, 320, 340, 345, 348) (in effect) |

NOTE: No further reduction is legislated or announced. Commentary speculates about
a 2027 step or eventual full coverage, but no official source supports it, so do
not present a further cut as scheduled. Sources: the gov.il allocation-number
service page and the Tax Authority's Israel-Invoice FAQ, both current as of
mid-2026.

## What "Above Threshold" Means
- The statute tests the **amount before VAT** (VAT Law s.38(a1) for the deduction bar, s.47(a2)(1) for the duty to request at the buyer's demand): it is measured on the amount before VAT, not on the VAT amount. Do not convert the threshold into a VAT-amount figure. A relief for mixed invoices described in some guidance appears in the Tax Authority FAQ (read 2026-09-15) but is administrative guidance, not in the statute, and is not used by the skill; on a mixed invoice above the before-VAT threshold the safe course is to request a number
- Credit invoices (330) do not require an allocation number
- Multiple items on one invoice: total is what matters

## Penalties for Non-Compliance
- Invoice without required allocation number: May be disqualified as tax invoice
- Buyer cannot claim input VAT on non-compliant invoice
- The disallowed input VAT is deducted automatically from the inputs reported in the detailed report
- Deducting input VAT on a tax invoice with no allocation number is an offence under the VAT Law
- (No published schedule of administrative fines specific to this requirement was found; do not quote a fine amount)

## Exemptions
- The duty applies only when four conditions ALL hold (Tax Authority API spec v2.0, section 1.2): the amount before VAT is above the threshold; the invoice includes a non-zero VAT component; the customer is a licensed dealer (osek murshe); and the customer has requested an allocation number. A number may still be requested for any amount and any customer, including credits.
- Zero-rated invoices, and invoices covering only exempt transactions: no allocation required (no VAT component). The special number on a reverse-charge replacement invoice arises only inside the refusal procedure.
- Plain payment receipts (kabala): Never require allocation (not part of the allocation document set)
- Transaction invoices (type 300): Never require allocation (a demand for payment, not a tax invoice)
- Credit invoices (type 330): Do not require allocation
- Transactions below current threshold: No allocation required
- Certain government entities: Special procedures apply
