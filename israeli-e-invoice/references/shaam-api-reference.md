# SHAAM Allocation API Reference (Israeli Tax Authority)

> **Always confirm against the current ITA spec before integrating.** Authoritative source: the "Israel Invoice Model API" spec (v2.0, 7/2024) and the ITA OpenAPI User Guide at <https://secapp.taxes.gov.il/OpenApiUserGuide/OpenApiUserGuide.pdf>. Endpoint paths and field casing changed between v1 and v2; the values below match v2.

## Hosts (note the split)
- **Allocation calls (Approval / MultiApproval):** `https://ita-api.taxes.gov.il`
- **OAuth token + invoice-information lookups:** `https://openapi.taxes.gov.il`

This split is real: the allocation request runs on `ita-api.taxes.gov.il`, while the OAuth token exchange and the lookup endpoints run on `openapi.taxes.gov.il`.

## Authentication
- **Method:** OAuth2 "User Restricted" (token-based). There is NO per-request TLS client certificate.
- **Token endpoint:** `https://openapi.taxes.gov.il/shaam/{tsandbox|production}/longtimetoken/oauth2/token` (standard authorize then token code flow; see the OpenAPI User Guide).
- **Software identity travels in the request body, not the auth header:**
  - `accounting_software_number` (mandatory): the registration certificate number of the accounting software in the ITA software registry. If no registration certificate exists, send the company number / ID of the document producer.
  - `client_software_key` (optional): the invoice issuer's client key with the software publisher.

## Endpoints

| Service | Sandbox | Production |
|---------|---------|------------|
| Allocation (single) | `POST https://ita-api.taxes.gov.il/shaam/tsandbox/Invoices/v2/Approval` | `POST https://ita-api.taxes.gov.il/shaam/production/Invoices/v2/Approval` |
| Allocation (batch) | `POST https://ita-api.taxes.gov.il/shaam/tsandbox/Multi-invoices/v2/MultiApproval` | `POST https://ita-api.taxes.gov.il/shaam/production/Multi-invoices/v2/MultiApproval` |
| Lookup by allocation # | `GET https://ita-api.taxes.gov.il/shaam/tsandbox/invoice-information/v1/details` | `GET https://openapi.taxes.gov.il/shaam/production/invoice-information/v1/details` |

V1 (`Invoices/v1/Approval`) was the transitional version and is superseded by V2. All v2 input field names are lowercase.

### Request Allocation Number
```
POST https://ita-api.taxes.gov.il/shaam/production/Invoices/v2/Approval
Content-Type: application/json
Authorization: Bearer {oauth2_user_restricted_token}

{
  "invoice_id": "INV-2026-0001",
  "invoice_type": 305,
  "vat_number": "123456782",
  "invoice_reference_number": "2026-0001",
  "customer_vat_number": "987654324",
  "invoice_date": "2026-01-15",
  "invoice_issuance_date": "2026-01-15",
  "accounting_software_number": 4324243,
  "amount_before_discount": 15000,
  "discount": 0,
  "payment_amount": 15000,
  "vat_amount": 2700,
  "payment_amount_including_vat": 17700
}

Success response:
{
  "status": 200,
  "message": "Invoice approved",
  "confirmation_number": "20240627231846297178091822",
  "approved": true
}
```

The allocation number is the `confirmation_number` field, a long numeric string (not a "SHAAM-2026-..." token). Print the **9 right-most digits** on the invoice under the heading "Allocation Number" (Mispar Haktzaa). A not-approved response returns `"confirmation_number": "0"`, `"approved": false`, with error details in `message.errors[]`.

## Error Codes
| Code | Meaning |
|------|---------|
| 400 | Bad request structure |
| 401 | Authentication failed (token invalid or expired) |
| 403 | Not authorized for this VAT number |
| 422 | Validation errors in invoice data |
| 460 / 461 / 462 | Allocation-specific rejection reasons (see message.errors[]) |
| 500 | SHAAM server error |

## Developer Resources
- OpenAPI User Guide (auth + onboarding): <https://secapp.taxes.gov.il/OpenApiUserGuide/OpenApiUserGuide.pdf>
- Official ITA OpenAPI demo (reference implementation): <https://github.com/dsaddan/Israel-Tax-Authority-OpenAPI-Taxes-Demo>
- Documentation is primarily in Hebrew.
