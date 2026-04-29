# SHAAM API Reference (Israeli Tax Authority)

> **Verify against official sources before using.** The Israel Tax Authority's OpenAPI portal is the authoritative source. Sandbox: <https://openapi-portal.taxes.gov.il/sandbox/>. Production allocation endpoint base: `https://openapi.taxes.gov.il/shaam/`. Endpoint paths and authentication shape have changed across rollout phases — always confirm against the current ITA OpenAPI v2.0 spec before integrating. The values below are illustrative and may be stale.

## Authentication
- **Method:** Digital certificate + Client ID / Client Secret issued via the gov.il national-identification certification flow. NOT bare OAuth2 client_credentials — the ITA requires a digital certificate as part of the auth bundle.
- **Sandbox developer portal:** <https://openapi-portal.taxes.gov.il/sandbox/>
- **Production base:** <https://openapi.taxes.gov.il/shaam/>
- **Allocation request endpoint pattern (sandbox example):** `POST {base}/Invoices/v1/Approval`
- Token lifetime, refresh, and certificate-renewal cadence: verify in the current spec PDF.

## Endpoints

### Request Allocation Number
```
POST /api/tax/e-invoice/allocation
Content-Type: application/json
Authorization: Bearer {token}

{
  "seller_tin": "123456782",
  "buyer_tin": "987654328",
  "invoice_type": 300,
  "invoice_date": "2026-01-15",
  "total_amount": 17550,
  "net_amount": 15000,
  "vat_amount": 2550,
  "currency": "ILS"
}

Response:
{
  "allocation_number": "SHAAM-2026-123456",
  "valid_until": "2026-02-15T00:00:00Z",
  "status": "approved"
}
```

### Validate Invoice Structure
```
POST /api/tax/e-invoice/validate
Content-Type: application/json
Authorization: Bearer {token}

{invoice_object}

Response:
{
  "valid": true,
  "errors": [],
  "warnings": ["Consider adding buyer email for digital delivery"]
}
```

### Check Allocation Status
```
GET /api/tax/e-invoice/status/{allocation_number}
Authorization: Bearer {token}

Response:
{
  "allocation_number": "SHAAM-2026-123456",
  "status": "used",
  "invoice_number": "INV-2026-0001",
  "used_date": "2026-01-15"
}
```

## Error Codes
| Code | Meaning |
|------|---------|
| 400 | Invalid request structure |
| 401 | Authentication failed |
| 403 | Not authorized for this TIN |
| 409 | Allocation already used |
| 422 | Validation errors in invoice data |
| 429 | Rate limited (max 100 requests/minute) |
| 500 | SHAAM server error |

## Developer Portal
- Registration: https://openapi-portal.taxes.gov.il/sandbox/ (sandbox + developer registration)
- Sandbox environment available for testing
- Documentation primarily in Hebrew
