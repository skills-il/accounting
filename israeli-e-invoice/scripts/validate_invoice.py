#!/usr/bin/env python3
"""Validate Israeli e-invoice structure and fields.

Checks invoice JSON against SHAAM (Israeli Tax Authority) requirements:
- Required fields presence
- TIN (mispar osek) format and check digit
- Invoice type validity
- VAT calculation accuracy
- Allocation number requirement based on amount threshold

Usage:
    python scripts/validate_invoice.py <invoice.json>
    python scripts/validate_invoice.py --example
"""

import sys
import json
import re
from datetime import datetime, date
from typing import Optional


# Valid SHAAM document type codes (Israel Invoice Model API, Table 2.5)
VALID_INVOICE_TYPES = {
    300: "Transaction Invoice (Heshbon Iska)",
    305: "Tax Invoice (Hashbonit Mas)",
    310: "Periodic Tax Invoice (Hashbonit Mas Tkufatit)",
    320: "Tax Invoice / Receipt (Hashbonit Mas / Kabala)",
    330: "Credit Invoice (Hashbonit Mas Zikui)",
    332: "Proforma Invoice",
    340: "Reservation Tax Invoice",
    345: "Agent Tax Invoice",
    348: "Log Command (Pkudat Yoman)",
}

# Allocation number thresholds by date range, as (net_threshold, vat_threshold).
# Requirement under the Economic Arrangements Law 2023-2024 (amending VAT Law
# section 47).
#
# IMPORTANT: the headline figures (25,000 / 20,000 / 10,000 / 5,000) are stated in
# the law as NET amounts, but the ITA's operative test is the VAT AMOUNT derived
# from them. Per the ITA FAQ: "נדרש מספר הקצאה רק כאשר סכום המע"מ גבוה מ-900 ₪"
# from 1.6.2026 (and 1,800 from 1.1.2026, 3,600 for 2025).
#
# For a wholly standard-rated invoice the two tests coincide, since
# 5,000 * 18% = 900. They DIVERGE on a mixed invoice that is partly exempt or
# zero-rated: such an invoice can exceed the net threshold while its VAT stays
# under the VAT threshold, in which case NO allocation number is required.
# Testing the net amount alone raises false "allocation required" errors for
# customs agents, lawyers and car dealers, whose invoices are mostly pass-through.
ALLOCATION_THRESHOLDS = [
    ("2024-05-04", "2024-12-31", 25000, 4250),  # VAT was 17% until 31.12.2024
    ("2025-01-01", "2025-12-31", 20000, 3600),
    ("2026-01-01", "2026-05-31", 10000, 1800),
    ("2026-06-01", None, 5000, 900),
]

# Document types that require allocation numbers (305 tax invoice, 310 periodic,
# 320 tax invoice/receipt, 332 proforma cash-basis, and the v2 codes 340/345/348).
# Transaction invoices (300) and credit invoices (330) do NOT require allocation.
ALLOCATION_REQUIRED_TYPES = {305, 310, 320, 332, 340, 345, 348}

VAT_RATE = 0.18  # 18% effective 2025-01-01 (raised from 17%); held in 2026 budget


def validate_tin(tin: str) -> bool:
    """Validate Israeli TIN (mispar osek) - 9 digits with Luhn-like check digit.

    Args:
        tin: String of 9 digits representing the Israeli business TIN.

    Returns:
        True if the TIN has valid format and check digit.
    """
    if not re.match(r"^\d{9}$", tin):
        return False
    digits = [int(d) for d in tin]
    weights = [1, 2, 1, 2, 1, 2, 1, 2, 1]
    total = 0
    for d, w in zip(digits, weights):
        product = d * w
        total += product // 10 + product % 10
    return total % 10 == 0


def get_allocation_vat_threshold(invoice_date: str) -> Optional[int]:
    """Get the VAT-amount allocation threshold for a given date.

    This is the ITA's operative test. See ALLOCATION_THRESHOLDS.
    """
    for start, end, _net_threshold, vat_threshold in ALLOCATION_THRESHOLDS:
        if invoice_date >= start:
            if end is None or invoice_date <= end:
                return vat_threshold
    return None


def get_allocation_threshold(invoice_date: str) -> Optional[int]:
    """Get the allocation number threshold for a given date.

    Args:
        invoice_date: Date string in YYYY-MM-DD format.

    Returns:
        Threshold amount in NIS, or None if no threshold applies.
    """
    for start, end, threshold, _vat_threshold in ALLOCATION_THRESHOLDS:
        if invoice_date >= start:
            if end is None or invoice_date <= end:
                return threshold
    return None


def validate_invoice(invoice: dict) -> list:
    """Validate invoice structure against SHAAM requirements.

    Args:
        invoice: Dictionary with invoice fields.

    Returns:
        List of error strings. Empty list means valid.
    """
    errors = []

    # Check required fields
    required_fields = ["seller_tin", "invoice_type", "date", "total_amount"]
    for field in required_fields:
        if field not in invoice:
            errors.append(f"Missing required field: {field}")

    # Validate seller TIN
    if "seller_tin" in invoice:
        if not validate_tin(str(invoice["seller_tin"]).zfill(9)):
            errors.append(
                f"Invalid seller TIN format: {invoice['seller_tin']}. "
                "Must be 9 digits with valid check digit."
            )

    # Validate buyer TIN (optional but must be valid if present)
    if "buyer_tin" in invoice and invoice["buyer_tin"]:
        if not validate_tin(str(invoice["buyer_tin"])):
            errors.append(
                f"Invalid buyer TIN format: {invoice['buyer_tin']}. "
                "Must be 9 digits with valid check digit."
            )

    # Validate invoice type
    if "invoice_type" in invoice:
        if invoice["invoice_type"] not in VALID_INVOICE_TYPES:
            errors.append(
                f"Invalid invoice type: {invoice['invoice_type']}. "
                f"Valid types: {list(VALID_INVOICE_TYPES.keys())}"
            )

    # Validate date
    if "date" in invoice:
        try:
            inv_date = datetime.strptime(invoice["date"], "%Y-%m-%d").date()
            # A forward-dated invoice is not automatically invalid: the Tax
            # Authority accepts allocation requests for invoices dated ahead of
            # the request. The exact window was not confirmed against an
            # authoritative source, so no hard future-date limit is enforced
            # here. Validate the date is parseable and leave the window to the
            # caller.
            _ = inv_date
        except ValueError:
            errors.append(
                f"Invalid date format: {invoice['date']}. Use YYYY-MM-DD."
            )

    # Validate VAT calculation
    # Not every invoice is wholly standard-rated. If the caller supplies
    # taxable_amount (the standard-rated portion), check against that; otherwise
    # assume the whole net is standard-rated. Charging MORE VAT than the
    # standard-rated base allows is always an error; charging less is only an
    # error when the invoice is declared fully standard-rated, because an exempt
    # or zero-rated component legitimately reduces the VAT.
    if "net_amount" in invoice and "vat_amount" in invoice:
        base = invoice.get("taxable_amount", invoice["net_amount"])
        if "taxable_amount" in invoice and not (
            0 <= base <= invoice["net_amount"] + 0.01
        ):
            errors.append(
                f"taxable_amount {base} NIS must be between 0 and the net "
                f"amount {invoice['net_amount']} NIS"
            )
        expected_vat = round(base * VAT_RATE, 2)
        actual_vat = invoice["vat_amount"]
        if actual_vat - expected_vat > 0.01:
            errors.append(
                f"VAT overstated: {actual_vat} NIS exceeds 18% of the "
                f"standard-rated base ({base} NIS = {expected_vat} NIS)"
            )
        elif expected_vat - actual_vat > 0.01:
            errors.append(
                f"VAT mismatch: expected {expected_vat} NIS (18% of "
                f"{invoice['net_amount']}), got {actual_vat} NIS. If part of "
                f"this invoice is exempt or zero-rated, supply taxable_amount "
                f"covering only the standard-rated portion."
            )

    # A credit note must reference the invoice it reverses.
    if invoice.get("invoice_type") == 330 and not invoice.get(
        "original_invoice_number"
    ):
        errors.append(
            "Credit invoice (330) must reference the original invoice number"
        )

    # Check allocation number requirement.
    # The operative ITA test is the VAT amount, not the net amount (they differ on
    # mixed invoices). Fall back to the net test only when no VAT figure is given.
    if (
        "invoice_type" in invoice
        and "date" in invoice
        and ("net_amount" in invoice or "total_amount" in invoice)
    ):
        inv_type = invoice["invoice_type"]
        if inv_type in ALLOCATION_REQUIRED_TYPES:
            # total_amount is GROSS. Comparing it against a NET threshold
            # over-states every gross-only payload by the VAT rate, so derive
            # the net figure instead.
            if "net_amount" in invoice:
                net = invoice["net_amount"]
            elif invoice.get("total_amount") is not None:
                net = invoice["total_amount"] / (1 + VAT_RATE)
            else:
                net = None
            vat = invoice.get("vat_amount")
            try:
                threshold = get_allocation_threshold(invoice["date"])
                vat_threshold = get_allocation_vat_threshold(invoice["date"])
                required = False
                reason = ""
                # A zero VAT figure does not settle the question: a zero-rated
                # reverse-charge invoice still carries an allocation number. Fall
                # back to the net test in that case.
                if vat is not None and vat != 0 and vat_threshold is not None:
                    required = vat > vat_threshold
                    reason = (
                        f"VAT amount {vat} NIS > VAT threshold "
                        f"{vat_threshold} NIS"
                    )
                elif threshold and net is not None:
                    required = net > threshold
                    reason = (
                        f"net amount {net} NIS > threshold {threshold} NIS "
                        f"(no vat_amount supplied, so the net test was used; "
                        f"supply vat_amount for a mixed invoice)"
                    )
                alloc = invoice.get("allocation_number")
                if required and not alloc:
                    errors.append(
                        f"Allocation number required: {reason} "
                        f"for date {invoice['date']}"
                    )
                elif alloc and not re.fullmatch(r"\d{9}", str(alloc)):
                    errors.append(
                        f"Allocation number must be the 9 right-most digits of "
                        f"the confirmation number, got {alloc!r}"
                    )
            except (ValueError, TypeError):
                pass  # Date validation already handled above

    return errors


def generate_example_invoice() -> dict:
    """Generate an example valid invoice for testing."""
    return {
        "seller_tin": "123456782",
        "seller_name": "Example Business Ltd",
        "buyer_tin": "987654324",
        "buyer_name": "Client Company Ltd",
        "invoice_type": 305,
        "invoice_number": "INV-2026-0001",
        "date": "2026-01-15",
        "net_amount": 15000,
        "vat_amount": 2700,
        "total_amount": 17700,
        "currency": "ILS",
        "allocation_number": "178091822",
        "items": [
            {
                "description": "Web development services",
                "quantity": 1,
                "unit_price": 15000,
                "amount": 15000,
            }
        ],
    }


def main():
    """Main entry point for invoice validation."""
    if len(sys.argv) < 2:
        print("Usage: python validate_invoice.py <invoice.json>")
        print("       python validate_invoice.py --example")
        print()
        print("Validates Israeli e-invoice JSON against SHAAM requirements.")
        sys.exit(1)

    if sys.argv[1] == "--example":
        example = generate_example_invoice()
        print("Example invoice:")
        print(json.dumps(example, indent=2))
        print()
        errors = validate_invoice(example)
        if errors:
            print("VALIDATION FAILED:")
            for e in errors:
                print(f"  - {e}")
        else:
            print("VALIDATION PASSED")
        sys.exit(0)

    try:
        with open(sys.argv[1]) as f:
            invoice = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {sys.argv[1]}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}")
        sys.exit(1)

    errors = validate_invoice(invoice)
    if errors:
        print("VALIDATION FAILED:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("VALIDATION PASSED")
        sys.exit(0)


if __name__ == "__main__":
    main()
