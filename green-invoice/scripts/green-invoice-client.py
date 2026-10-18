#!/usr/bin/env python3
"""
Green Invoice API Client

A helper script for common Green Invoice (Morning) API operations:
- Authenticate and get JWT token
- Create documents (invoices, receipts, credit notes)
- Search and list documents
- Manage clients (create, search, list)

Usage:
    python3 green-invoice-client.py auth --key-id YOUR_KEY_ID --key-secret YOUR_SECRET
    python3 green-invoice-client.py auth --legacy --key-id YOUR_KEY_ID --key-secret YOUR_SECRET   (production only)
    python3 green-invoice-client.py create-document --token TOKEN --type 320 --client-name "Name" --client-email "email@example.com" --description "Service" --amount 5000
    python3 green-invoice-client.py search-documents --token TOKEN --from-date 2026-01-01 --to-date 2026-03-31 [--all-pages]
    python3 green-invoice-client.py create-client --token TOKEN --name "Client Name" --email "email@example.com"
    python3 green-invoice-client.py search-clients --token TOKEN --name "Client"
    python3 green-invoice-client.py get-document --token TOKEN --id DOCUMENT_ID

Environment:
    Set GREEN_INVOICE_ENV=sandbox to use sandbox environment.
    Default is production.
"""

import argparse
import datetime
import json
import sys
import time
from decimal import Decimal, ROUND_HALF_UP
import urllib.request
import urllib.error
import os

PROD_BASE = "https://api.greeninvoice.co.il/api/v1"
SANDBOX_BASE = "https://sandbox.d.greeninvoice.co.il/api/v1"

# OAuth 2.0 token endpoints (the documented flow in "morning API Documentation 2.0.0").
# The token is used against the same api/v1 base URLs above.
PROD_OAUTH = "https://api.morning.co/idp/v1/oauth/token"
SANDBOX_OAUTH = "https://api.sandbox.morning.dev/idp/v1/oauth/token"

DOCUMENT_TYPES = {
    10: "Price Quote",
    20: "Bill / Payment Confirmation",
    100: "Order",
    200: "Delivery Note",
    210: "Return Note",
    300: "Transaction Invoice",
    305: "Tax Invoice",
    320: "Tax Invoice-Receipt",
    330: "Credit Note",
    400: "Receipt",
    405: "Donation Receipt",
    410: "Donation Cancellation",
    500: "Purchase Order",
    600: "Deposit Receipt",
    610: "Deposit Withdrawal",
}

PAYMENT_TYPES = {
    0: "Withholding Tax",
    1: "Cash",
    2: "Check",
    3: "Credit Card",
    4: "Bank Transfer",
    5: "PayPal",
    10: "Payment App",
    11: "Other",
}


def is_sandbox():
    return os.environ.get("GREEN_INVOICE_ENV", "production") == "sandbox"


def get_base_url():
    return SANDBOX_BASE if is_sandbox() else PROD_BASE


MAX_RETRIES = 4


def http_json(method, url, token=None, data=None):
    """POST/GET JSON. Retries HTTP 429 with exponential backoff (the rate limit is
    not published, so treat 429 as expected rather than fatal)."""
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    body = json.dumps(data).encode("utf-8") if data is not None else None

    for attempt in range(MAX_RETRIES + 1):
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req) as resp:
                response_data = resp.read().decode("utf-8")
                return json.loads(response_data) if response_data else {}
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8")
            if e.code == 429 and attempt < MAX_RETRIES:
                wait = 2 ** attempt
                print(f"HTTP 429, retrying in {wait}s", file=sys.stderr)
                time.sleep(wait)
                continue
            print(f"Error {e.code}: {error_body}", file=sys.stderr)
            sys.exit(1)
        except urllib.error.URLError as e:
            print(f"Network error: {e.reason}", file=sys.stderr)
            sys.exit(1)


def api_request(method, path, token=None, data=None):
    return http_json(method, f"{get_base_url()}{path}", token=token, data=data)


def cmd_auth(args):
    """Obtain a bearer token. OAuth 2.0 by default; --legacy for /account/token."""
    if args.legacy:
        if is_sandbox():
            # Probed 2026-10-18: sandbox /account/token returns the same 404 as a path
            # that was never defined, while production still answers it.
            print("The legacy /account/token route is gone on sandbox (HTTP 404).\n"
                  "Drop --legacy to use the OAuth 2.0 flow.", file=sys.stderr)
            sys.exit(1)
        result = api_request("POST", "/account/token", data={
            "id": args.key_id,
            "secret": args.key_secret,
        })
        # Not in the current OpenAPI; existing clients read the body "token" field.
        token = result.get("token", "")
        expires = None
    else:
        url = SANDBOX_OAUTH if is_sandbox() else PROD_OAUTH
        result = http_json("POST", url, data={
            "grant_type": "client_credentials",
            "client_id": args.key_id,
            "client_secret": args.key_secret,
        })
        token = result.get("accessToken", "")
        expires = result.get("expiresAt")  # Unix seconds; tokens last 1 hour

    if not token:
        print("Authentication failed. Check your credentials.", file=sys.stderr)
        sys.exit(1)
    print(f"Token: {token}")
    if expires:
        when = datetime.datetime.fromtimestamp(int(expires), datetime.timezone.utc)
        print(f"Expires: {when.isoformat()} (re-authenticate after this)")
    print(f"\nUse with: --token {token[:20]}...")


# Allocation-number thresholds (NET, before VAT; the statute says "exceeds") by the
# DOCUMENT's own date. The regime began in May 2024; the whole month is treated as in
# scope, since over-warning is harmless and under-warning loses the buyer's deduction.
ALLOCATION_THRESHOLDS = [  # (first date in force, threshold)
    ("2024-05-01", Decimal("25000")),
    ("2025-01-01", Decimal("20000")),
    ("2026-01-01", Decimal("10000")),
    ("2026-06-01", Decimal("5000")),
]
TAX_INVOICE_TYPES = {305, 320}


def allocation_threshold(doc_date):
    """Threshold in force on doc_date (YYYY-MM-DD), or None before the regime."""
    current = None
    for start, amount in ALLOCATION_THRESHOLDS:
        if doc_date >= start:
            current = amount
    return current


def needs_allocation(doc_type, net, doc_date, b2b_buyer, zero_rated):
    """True when a number is needed: a tax invoice to an osek murshe / company buyer,
    carrying VAT, above the threshold in force on the document date. The buyer's VAT
    status decides it, not whether a taxId is filled (a private ID number is not an
    osek number, and an osek patur buyer cannot deduct anyway)."""
    if doc_type not in TAX_INVOICE_TYPES or not b2b_buyer or zero_rated:
        return False
    threshold = allocation_threshold(doc_date)
    return threshold is not None and net > threshold


def _today() -> str:
    """Payment rows require a date; default to today in ISO form."""
    return datetime.date.today().isoformat()


def cmd_create_document(args):
    """Create a new document."""
    doc_type = args.type
    if doc_type not in DOCUMENT_TYPES:
        print(f"Invalid document type: {doc_type}", file=sys.stderr)
        print(f"Valid types: {json.dumps(DOCUMENT_TYPES, indent=2)}", file=sys.stderr)
        sys.exit(1)

    payload = {
        "type": doc_type,
        "lang": args.lang,
        "currency": args.currency,
        "vatType": args.vat_type,
        "signed": True,
        "attachment": True,
        "client": {
            "name": args.client_name,
            "emails": [args.client_email],
            "add": True,
        },
        "income": [
            {
                "description": args.description,
                "quantity": args.quantity,
                "price": args.amount,
                "currency": args.currency,
                # Required by IncomeRowRequest. This is ItemVatType (0 default,
                # 1 VAT INCLUDED in price, 2 exempt), a different enum from the
                # document-level vatType above.
                "vatType": args.row_vat_type,
            }
        ],
    }

    if args.currency_rate is not None:
        payload["income"][0]["currencyRate"] = args.currency_rate
    elif args.currency.upper() != "ILS":
        # currencyRate defaults to 1 per the spec, which would book USD 1,000 as ILS 1,000.
        print("ERROR: a foreign-currency document needs --currency-rate (rate to ILS,\n"
              "       e.g. the Bank of Israel representative rate for the document date).",
              file=sys.stderr)
        sys.exit(1)

    vat_rate = 18.0 if args.vat_rate is None else args.vat_rate
    if args.vat_rate is not None:
        # An explicit rate is sent on the row as vatRate (a decimal fraction), which is
        # how a zero-rated export line is expressed. Without it the server applies the
        # business default and a "--vat-rate 0" payment would undershoot the total.
        payload["income"][0]["vatRate"] = float(Decimal(str(vat_rate)) / Decimal("100"))

    if args.date:
        payload["date"] = args.date
    if args.due_date:
        payload["dueDate"] = args.due_date
    if args.tax_id:
        payload["client"]["taxId"] = args.tax_id
    if args.payment_type is not None:
        # The payment lines MUST sum to the DOCUMENT total, which is the gross amount.
        # The income line carries the NET price, and with vatType 0 the server adds VAT
        # on top according to the business type. A payment that does not match the total
        # is rejected (error 2422) or leaves a balance, so compute the gross unless the
        # caller states it.
        net = Decimal(str(args.amount)) * Decimal(str(args.quantity))
        if args.payment_amount is not None:
            gross = Decimal(str(args.payment_amount))
        elif args.vat_type == 1 or args.row_vat_type == 2 or vat_rate == 0:
            # exempt document, exempt row, or an explicitly zero-rated row
            gross = net
        elif args.row_vat_type == 1:
            # ItemVatType 1: VAT is already INCLUDED in the price sent, so the price
            # is the gross. Multiplying again over-pays by the VAT.
            gross = net
        elif args.osek_patur:
            # An osek patur charges no VAT, so the server adds none and the
            # payment must equal the net. Deriving a gross here over-paid every
            # osek-patur document by the VAT.
            gross = net
        else:
            rate = Decimal(str(vat_rate)) / Decimal("100")
            gross = (net * (Decimal("1") + rate)).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            if args.vat_type == 2:
                print(
                    "WARNING: vatType 2 (mixed) means only part of the document is\n"
                    "         VAT-bearing, so the gross cannot be derived from a single\n"
                    f"         rate. Assuming {vat_rate}% on the whole amount. Pass\n"
                    "         --payment-amount with the real document total instead.",
                    file=sys.stderr,
                )
        payload["payment"] = [{
            "type": args.payment_type,
            "price": float(gross),
            "currency": args.currency,
        }]
        if gross == net and args.row_vat_type == 1:
            note = " (price already includes VAT)"
        elif gross == net:
            note = " (no VAT added)"
        elif args.payment_amount is not None:
            note = " (caller-supplied gross)"
        else:
            note = f" (net {net} + VAT at {vat_rate}%)"
        print(f"Payment line: {gross} {args.currency}{note}", file=sys.stderr)
        # date is required on a payment row (PaymentRowRequest.required).
        payload["payment"][0]["date"] = args.date or _today()
        if args.currency_rate is not None:
            payload["payment"][0]["currencyRate"] = args.currency_rate

    # The threshold is a NET amount in shekels: strip VAT from a VAT-inclusive row and
    # convert a foreign-currency document at its rate before comparing.
    net_total = Decimal(str(args.amount)) * Decimal(str(args.quantity))
    if args.row_vat_type == 1:
        net_total = net_total / (Decimal("1") + Decimal(str(vat_rate)) / Decimal("100"))
    if args.currency.upper() != "ILS" and args.currency_rate is not None:
        net_total = net_total * Decimal(str(args.currency_rate))
    doc_date = args.date or _today()
    zero_rated = args.vat_type == 1 or args.row_vat_type == 2 or vat_rate == 0 or args.osek_patur
    allocation_needed = needs_allocation(doc_type, net_total, doc_date, args.b2b, zero_rated)
    if allocation_needed and not args.tax_id:
        print("WARNING: this tax invoice needs an allocation number, but the business buyer has\n"
              "         no --tax-id. Morning cannot request a number without the buyer's VAT\n"
              "         number, and without one the buyer cannot deduct the input VAT.",
              file=sys.stderr)

    result = api_request("POST", "/documents", token=args.token, data=payload)
    print(f"Document created successfully!")
    print(f"  Type: {DOCUMENT_TYPES.get(doc_type, doc_type)}")
    print(f"  ID: {result.get('id', 'N/A')}")
    print(f"  Number: {result.get('number', 'N/A')}")
    print(f"  VAT rate applied: {result.get('vatRate', 'N/A')}")
    # Allocation-number (SHAAM) confirmation status, returned on the 201 response.
    # A non-zero error means the Tax Authority confirmation failed; check the
    # Morning Tax Authority connection before sending the invoice on.
    if "taxAuthorityConfirmationInitiated" in result:
        print(f"  Tax Authority confirmation initiated: {result['taxAuthorityConfirmationInitiated']}")
    err = result.get("taxAuthorityConfirmationLastError")
    if err:
        print(f"  WARNING: Tax Authority confirmation error {err}", file=sys.stderr)
    elif allocation_needed and not result.get("taxAuthorityConfirmationInitiated"):
        # No request was made although one was needed: the usual sign of a lapsed or
        # never-granted Tax Authority authorization in the Morning account.
        print("  WARNING: no Tax Authority confirmation was initiated for a document that\n"
              "           needs an allocation number. Check the Morning Tax Authority\n"
              "           authorization, then request a number for THIS document.",
              file=sys.stderr)


def cmd_search_documents(args):
    """Search documents. Pages are 1-based; --all-pages walks every page."""
    payload = {
        "page": args.page,
        "pageSize": args.page_size,
    }
    if args.from_date:
        payload["fromDate"] = args.from_date
    if args.to_date:
        payload["toDate"] = args.to_date
    if args.type:
        payload["type"] = [args.type]
    if args.status is not None:
        payload["status"] = [args.status]

    page = args.page
    while True:
        payload["page"] = page
        result = api_request("POST", "/documents/search", token=args.token, data=payload)
        items = result.get("items", [])
        total = result.get("total", 0)
        pages = result.get("pages", 1) or 1

        print(f"Found {total} documents (page {page} of {pages}):\n")
        for doc in items:
            print(format_document_row(doc))
        if not args.all_pages or page >= pages or not items:
            break
        page += 1


def format_document_row(doc):
    # Search results use documentDate and amount (the document total), not date/total.
    doc_type = DOCUMENT_TYPES.get(doc.get("type", 0), "Unknown")
    client = (doc.get("client") or {}).get("name", "N/A")
    return (f"  #{doc.get('number', 'N/A')} | {doc_type} | {client} | "
            f"{doc.get('amount', 'N/A')} {doc.get('currency', 'ILS')} | "
            f"{doc.get('documentDate', 'N/A')}")


def cmd_get_document(args):
    """Get a single document by ID."""
    result = api_request("GET", f"/documents/{args.id}", token=args.token)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_create_client(args):
    """Create a new client."""
    payload = {
        "name": args.name,
        "emails": [args.email],
    }
    if args.tax_id:
        payload["taxId"] = args.tax_id
    if args.city:
        payload["city"] = args.city
    if args.address:
        payload["address"] = args.address
    if args.phone:
        payload["phone"] = args.phone
    if args.payment_terms is not None:
        payload["paymentTerms"] = args.payment_terms

    result = api_request("POST", "/clients", token=args.token, data=payload)
    print(f"Client created successfully!")
    print(f"  ID: {result.get('id', 'N/A')}")
    print(f"  Name: {result.get('name', 'N/A')}")


def cmd_search_clients(args):
    """Search clients."""
    payload = {
        "page": args.page,
        "pageSize": args.page_size,
    }
    if args.name:
        payload["name"] = args.name
    if args.email:
        payload["email"] = args.email

    result = api_request("POST", "/clients/search", token=args.token, data=payload)
    items = result.get("items", [])
    total = result.get("total", 0)

    print(f"Found {total} clients (showing page {args.page}):\n")
    for client in items:
        emails = ", ".join(client.get("emails", []))
        print(f"  {client.get('name', 'N/A')} | {emails} | "
              f"Tax ID: {client.get('taxId', 'N/A')}")


def main():
    parser = argparse.ArgumentParser(
        description="Green Invoice (Morning) API Client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Set GREEN_INVOICE_ENV=sandbox to use sandbox environment."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # auth
    auth_parser = subparsers.add_parser("auth", help="Get a bearer token (OAuth 2.0 by default)")
    auth_parser.add_argument("--key-id", required=True, help="API Key ID (OAuth client_id)")
    auth_parser.add_argument("--key-secret", required=True, help="API Key Secret (OAuth client_secret)")
    auth_parser.add_argument("--legacy", action="store_true",
        help="Use the legacy POST /account/token flow (production only; removed on sandbox)")

    # create-document
    doc_parser = subparsers.add_parser("create-document", help="Create a new document")
    doc_parser.add_argument("--token", required=True, help="JWT token")
    doc_parser.add_argument("--type", type=int, required=True, help="Document type code")
    doc_parser.add_argument("--client-name", required=True, help="Client name")
    doc_parser.add_argument("--client-email", required=True, help="Client email")
    doc_parser.add_argument("--description", required=True, help="Item description")
    doc_parser.add_argument("--amount", type=float, required=True, help="Item price")
    doc_parser.add_argument("--quantity", type=float, default=1, help="Item quantity")
    doc_parser.add_argument("--currency", default="ILS", help="Currency code")
    doc_parser.add_argument("--currency-rate", type=float,
        help="Rate to ILS for a foreign-currency document (required unless --currency is ILS; the API default is 1)")
    doc_parser.add_argument("--lang", default="he", choices=["he", "en"])
    doc_parser.add_argument("--vat-type", type=int, default=0, help="VAT type (0=default, 1=exempt, 2=mixed)")
    doc_parser.add_argument("--vat-rate", type=float, default=None,
        help="VAT percent. When given, it is sent on the income row as vatRate (e.g. 0 for a zero-rated export line) and used for the payment; when omitted the business default applies and 18 is assumed for the payment")
    doc_parser.add_argument("--row-vat-type", type=int, default=0,
        help="ItemVatType on the income row (0=default, 1=VAT INCLUDED in price, 2=exempt). Required by the API; different enum from --vat-type.")
    doc_parser.add_argument("--osek-patur", action="store_true",
        help="Issuer is an osek patur: no VAT is added, so the payment line equals the net.")
    doc_parser.add_argument("--payment-amount", type=float, help="Explicit GROSS payment amount. Use this when the document total is not net*(1+vat-rate), e.g. vatType 2 (mixed).")
    doc_parser.add_argument("--date", help="Document date (YYYY-MM-DD)")
    doc_parser.add_argument("--due-date", help="Due date (YYYY-MM-DD)")
    doc_parser.add_argument("--tax-id", help="Client tax ID")
    doc_parser.add_argument("--payment-type", type=int, help="Payment type code")
    doc_parser.add_argument("--b2b", action="store_true",
        help="The buyer is an osek murshe or a company (enables allocation-number checks)")

    # search-documents
    search_doc_parser = subparsers.add_parser("search-documents", help="Search documents")
    search_doc_parser.add_argument("--token", required=True, help="JWT token")
    search_doc_parser.add_argument("--from-date", help="From date (YYYY-MM-DD)")
    search_doc_parser.add_argument("--to-date", help="To date (YYYY-MM-DD)")
    search_doc_parser.add_argument("--type", type=int, help="Document type filter")
    search_doc_parser.add_argument("--status", type=int, help="Document status filter")
    search_doc_parser.add_argument("--page", type=int, default=1, help="Page number")
    search_doc_parser.add_argument("--page-size", type=int, default=25, help="Page size")
    search_doc_parser.add_argument("--all-pages", action="store_true",
        help="Fetch every page (use for full-period reconciliation)")

    # get-document
    get_doc_parser = subparsers.add_parser("get-document", help="Get document by ID")
    get_doc_parser.add_argument("--token", required=True, help="JWT token")
    get_doc_parser.add_argument("--id", required=True, help="Document ID")

    # create-client
    client_parser = subparsers.add_parser("create-client", help="Create a new client")
    client_parser.add_argument("--token", required=True, help="JWT token")
    client_parser.add_argument("--name", required=True, help="Client name")
    client_parser.add_argument("--email", required=True, help="Client email")
    client_parser.add_argument("--tax-id", help="Client tax ID")
    client_parser.add_argument("--city", help="Client city")
    client_parser.add_argument("--address", help="Client address")
    client_parser.add_argument("--phone", help="Client phone")
    client_parser.add_argument("--payment-terms", type=int, help="Payment terms code")

    # search-clients
    search_client_parser = subparsers.add_parser("search-clients", help="Search clients")
    search_client_parser.add_argument("--token", required=True, help="JWT token")
    search_client_parser.add_argument("--name", help="Client name filter")
    search_client_parser.add_argument("--email", help="Client email filter")
    search_client_parser.add_argument("--page", type=int, default=1, help="Page number")
    search_client_parser.add_argument("--page-size", type=int, default=25, help="Page size")

    args = parser.parse_args()

    commands = {
        "auth": cmd_auth,
        "create-document": cmd_create_document,
        "search-documents": cmd_search_documents,
        "get-document": cmd_get_document,
        "create-client": cmd_create_client,
        "search-clients": cmd_search_clients,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
