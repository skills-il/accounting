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

# Allocation number thresholds by date range, as (start, end, net_threshold).
#
# The STATUTE keys the duty to the amount BEFORE VAT: VAT Law s.47(a2)(1) obliges
# the dealer to request a number "בעסקה שסכומה, בלא המס, עולה על הסכום האמור
# בסעיף 38(א1)", at the buyer's demand and not for a zero-rated transaction, and
# s.38(a1) bars deducting input VAT on such an invoice without a number. The net
# threshold is therefore the test this script applies.
#
# No VAT-amount figure is used: the statute tests only the amount before VAT.
ALLOCATION_THRESHOLDS = [
    ("2024-05-04", "2024-12-31", 25000),
    ("2025-01-01", "2025-12-31", 20000),
    ("2026-01-01", "2026-05-31", 10000),
    ("2026-06-01", None, 5000),
]

# Document types that require allocation numbers (305 tax invoice, 310 periodic,
# 320 tax invoice/receipt, 332 proforma cash-basis, and the v2 codes 340/345/348).
# Transaction invoices (300) and credit invoices (330) do NOT require allocation.
ALLOCATION_REQUIRED_TYPES = {305, 310, 320, 332, 340, 345, 348}

VAT_RATE = 0.18  # 18% effective 2025-01-01 (raised from 17%); held in 2026 budget


def vat_rate_for(date_str) -> float:
    """Standard VAT rate for an invoice date: 17% until 31.12.2024, 18% from 1.1.2025."""
    if isinstance(date_str, str) and date_str < "2025-01-01":
        return 0.17
    return VAT_RATE


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


def get_allocation_threshold(invoice_date: str) -> Optional[int]:
    """Get the allocation number threshold for a given date.

    Args:
        invoice_date: Date string in YYYY-MM-DD format.

    Returns:
        Threshold amount in NIS, or None if no threshold applies.
    """
    for start, end, threshold in ALLOCATION_THRESHOLDS:
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
    # Accept a date object as well as a YYYY-MM-DD string.
    if isinstance(invoice.get("date"), (date, datetime)):
        invoice = dict(invoice, date=invoice["date"].strftime("%Y-%m-%d"))

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
        if not validate_tin(str(invoice["buyer_tin"]).zfill(9)):
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
        except (ValueError, TypeError):
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
        rate = vat_rate_for(invoice.get("date"))
        expected_vat = round(base * rate, 2)
        actual_vat = invoice["vat_amount"]
        if actual_vat - expected_vat > 0.01:
            errors.append(
                f"VAT overstated: {actual_vat} NIS exceeds {round(rate * 100)}% of the "
                f"standard-rated base ({base} NIS = {expected_vat} NIS)"
            )
        elif expected_vat - actual_vat > 0.01:
            errors.append(
                f"VAT mismatch: expected {expected_vat} NIS ({round(rate * 100)}% of "
                f"{invoice['net_amount']}), got {actual_vat} NIS. If part of "
                f"this invoice is exempt or zero-rated, supply taxable_amount "
                f"covering only the standard-rated portion (taxable_amount 0 for a "
                f"wholly zero-rated invoice)."
            )

    # A credit note must reference the invoice it reverses.
    if invoice.get("invoice_type") == 330 and not invoice.get(
        "original_invoice_number"
    ):
        errors.append(
            "Credit invoice (330) must reference the original invoice number"
        )

    # Check allocation number requirement.
    # Optional booleans: customer_is_licensed_dealer, customer_requested_allocation.
    # Absent = assumed true (the conservative reading for a B2B tax invoice).
    # The statute (VAT Law s.38(a1), s.47(a2)(1)) tests the amount BEFORE VAT only.
    # net_amount is used when given; otherwise it is derived as total - vat_amount,
    # or as total / (1 + rate) when no VAT figure is given.
    if (
        "invoice_type" in invoice
        and "date" in invoice
        and ("net_amount" in invoice or "total_amount" in invoice)
    ):
        inv_type = invoice["invoice_type"]
        # A 332 proforma carries allocation only in the cash-basis case (spec Table 2.5,
        # article 3.5); require it only when the caller says so.
        proforma_not_cash_basis = inv_type == 332 and not invoice.get("proforma_cash_basis")
        if inv_type in ALLOCATION_REQUIRED_TYPES and not proforma_not_cash_basis:
            # total_amount is GROSS. Comparing it against a NET threshold
            # over-states every gross-only payload by the VAT rate, so derive
            # the net figure instead.
            if "net_amount" in invoice:
                net = invoice["net_amount"]
            elif invoice.get("total_amount") is not None and invoice.get("vat_amount") is not None:
                rate_t = vat_rate_for(invoice["date"])
                max_vat = invoice["total_amount"] * rate_t / (1 + rate_t)
                if abs(invoice["vat_amount"]) - abs(max_vat) > 0.01:
                    errors.append(
                        f"VAT overstated: {invoice['vat_amount']} NIS exceeds the most VAT a total "
                        f"of {invoice['total_amount']} NIS can carry at {round(rate_t * 100)}% "
                        f"({round(max_vat, 2)} NIS)"
                    )
                    # Test the duty on the larger, fully standard-rated net.
                    net = invoice["total_amount"] / (1 + rate_t)
                else:
                    net = invoice["total_amount"] - invoice["vat_amount"]
            elif invoice.get("total_amount") is not None:
                net = invoice["total_amount"] / (1 + vat_rate_for(invoice["date"]))
            else:
                net = None
            if net is not None:
                net = round(net, 2)
            vat = invoice.get("vat_amount")
            try:
                threshold = get_allocation_threshold(invoice["date"])
                required = False
                reason = ""
                # Tax Authority API spec v2.0 s.1.2: the duty applies only when ALL
                # of: amount above threshold, a NON-ZERO VAT component, the customer
                # is a licensed dealer, and the customer requested a number. A
                # zero-rated or wholly exempt invoice therefore carries no duty. The
                # special number on a reverse-charge replacement (action=3) arises
                # only inside the refusal procedure, not as a general requirement.
                customer_not_dealer = invoice.get("customer_is_licensed_dealer") is False
                customer_did_not_request = invoice.get("customer_requested_allocation") is False
                # 999999998 is the sentinel for a customer who does not deduct input VAT.
                sentinel_customer = str(invoice.get("buyer_tin", "")).zfill(9) == "999999998"
                if vat == 0:
                    required = False
                elif customer_not_dealer or customer_did_not_request or sentinel_customer:
                    required = False
                elif threshold and net is not None:
                    # VAT Law s.38(a1) and s.47(a2)(1) key the duty to the amount BEFORE VAT.
                    required = net > threshold
                    reason = (
                        f"amount before VAT {round(net, 2)} NIS > threshold {threshold} NIS "
                        f"(VAT Law s.38(a1), s.47(a2)(1)); this assumes the customer is a "
                        f"licensed dealer who requested a number"
                    )
                alloc = invoice.get("allocation_number")
                if required and not alloc:
                    errors.append(
                        f"Allocation number required: {reason} "
                        f"for date {invoice['date']}"
                    )
                elif alloc and not re.fullmatch(
                    r"\d{9}", str(alloc).zfill(9) if isinstance(alloc, int) else str(alloc)
                ):
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
