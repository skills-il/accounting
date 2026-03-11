---
name: israeli-shaam-e-invoice-builder
description: >-
  Build SHAAM-compliant electronic invoices with allocation numbers (mispar haktsa'a)
  per Israeli Tax Authority (ITA) requirements. Use when generating tax invoices,
  credit notes, or receipts that require ITA allocation numbers for VAT deduction
  eligibility. Handles OAuth2 authentication, JSON payload construction per ITA technical
  specs v2.0, buyer VAT validation, and batch submission. Supports the phased threshold
  rollout (20K NIS Jan 2025, 10K NIS Jan 2026, 5K NIS June 2026). Do NOT use for bookkeeping,
  expense categorization, bank reconciliation, or non-Israeli tax jurisdictions.
license: MIT
allowed-tools: Bash(node:*,npx:*,curl:*) WebFetch Edit Read
compatibility: Requires network access for SHAAM API calls and OAuth2 token exchange
metadata:
  author: skills-il
  version: 1.0.0
  category: accounting
  tags:
    he:
    - חשבונית-דיגיטלית
    - שע"ם
    - רשות-המסים
    - ציות
    - מע"מ
    - חשבונאות
    en:
    - e-invoice
    - shaam
    - tax-authority
    - compliance
    - vat
    - accounting
  display_name:
    he: בונה חשבוניות דיגיטליות - שע"ם
    en: Israeli SHAAM E-Invoice Builder
  display_description:
    he: בניית חשבוניות אלקטרוניות תואמות שע"ם עם מספרי הקצאה לפי דרישות רשות המסים
    en: >-
      Build SHAAM-compliant electronic invoices with allocation numbers (mispar haktsa'a)
      per Israeli Tax Authority (ITA) requirements. Use when generating tax invoices,
      credit notes, or receipts that require ITA allocation numbers for VAT deduction
      eligibility. Handles OAuth2 authentication, JSON payload construction per ITA
      technical specs v2.0, buyer VAT validation, and batch submission. Supports the
      phased threshold rollout (20K NIS Jan 2025, 10K NIS Jan 2026, 5K NIS June 2026).
      Do NOT use for bookkeeping, expense categorization, bank reconciliation, or
      non-Israeli tax jurisdictions.
  supported_agents:
  - claude-code
  - cursor
  - github-copilot
  - windsurf
  - opencode
  - codex
---


# Israeli SHAAM E-Invoice Builder

## Overview

The SHAAM (Shnot Asmachta Mekuvenet -- שע"ם) system is the Israeli Tax Authority's platform for electronic invoice allocation numbers. Starting January 2025, invoices above certain thresholds require an allocation number (mispar haktsa'a -- מספר הקצאה) for the buyer to deduct input VAT. This skill automates the end-to-end process: authentication, invoice construction, validation, submission, and allocation number retrieval.

### Compliance Timeline

| Date | Threshold | Scope |
|------|-----------|-------|
| January 2025 | 25,000 NIS (incl. VAT) | Invoices above threshold require allocation number |
| January 2026 | 10,000 NIS (incl. VAT) | Lowered threshold |
| June 2026 | 5,000 NIS (incl. VAT) | Final planned threshold |

Without a valid allocation number, the buyer cannot deduct input VAT on the transaction.

## Instructions

### Step 1: Configure SHAAM API Credentials

Set up OAuth2 credentials for the SHAAM platform. You need a client ID and client secret issued by the Israeli Tax Authority after registering your software with them.

Store credentials in environment variables:

```bash
export SHAAM_CLIENT_ID="your-client-id"
export SHAAM_CLIENT_SECRET="your-client-secret"
export SHAAM_ENV="production"  # or "sandbox" for testing
```

API base URLs:
- **Sandbox**: `https://ita-api-sandbox.taxes.gov.il/shaam/api/v2`
- **Production**: `https://ita-api.taxes.gov.il/shaam/api/v2`

OAuth2 token endpoint:
- **Sandbox**: `https://ita-api-sandbox.taxes.gov.il/auth/oauth2/token`
- **Production**: `https://ita-api.taxes.gov.il/auth/oauth2/token`

### Step 2: Authenticate via OAuth2

Obtain a bearer token using the client credentials grant:

```bash
curl -X POST "${SHAAM_TOKEN_URL}" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  -d "client_id=${SHAAM_CLIENT_ID}" \
  -d "client_secret=${SHAAM_CLIENT_SECRET}" \
  -d "scope=invoice:write invoice:read"
```

The response returns an access token valid for 60 minutes:

```json
{
  "access_token": "eyJ...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "invoice:write invoice:read"
}
```

Cache the token and refresh it before expiry. Do not request a new token for every API call.

### Step 3: Construct the Invoice JSON Payload

Build the invoice object per ITA technical specs v2.0. The required JSON structure:

```json
{
  "invoice_type": "hashbonit_mas",
  "invoice_number": "INV-2026-001234",
  "invoice_date": "2026-03-08",
  "supplier": {
    "tax_id": "123456789",
    "name": "Supplier Ltd",
    "address": {
      "street": "Rothschild Blvd 1",
      "city": "Tel Aviv",
      "postal_code": "6688101"
    }
  },
  "buyer": {
    "tax_id": "987654321",
    "name": "Buyer Corp",
    "address": {
      "street": "Herzl St 10",
      "city": "Jerusalem",
      "postal_code": "9423201"
    }
  },
  "line_items": [
    {
      "description": "Software Development Services",
      "quantity": 1,
      "unit_price": 15000.00,
      "vat_rate": 17,
      "total_before_vat": 15000.00,
      "vat_amount": 2550.00,
      "total_with_vat": 17550.00
    }
  ],
  "totals": {
    "total_before_vat": 15000.00,
    "total_vat": 2550.00,
    "total_with_vat": 17550.00
  },
  "currency": "ILS",
  "payment_terms": "net30"
}
```

**Supported invoice types:**

| Type | Hebrew | Description |
|------|--------|-------------|
| `hashbonit_mas` | חשבונית מס | Tax invoice (standard) |
| `hashbonit_mas_kabala` | חשבונית מס / קבלה | Tax invoice with receipt |
| `hashbonit_zikuy` | חשבונית זיכוי | Credit note |
| `kabala` | קבלה | Receipt |

### Step 4: Validate the Invoice Before Submission

Before submitting, validate the invoice locally:

1. **Buyer VAT number validation**: Verify the buyer's tax ID (osek murshe number) is a valid 9-digit Israeli VAT number. The check digit algorithm uses a weighted sum modulo 10 with weights [1,2,1,2,1,2,1,2,1].

2. **Threshold check**: Determine if the invoice total (including VAT) exceeds the current threshold. If below threshold, an allocation number is not required but can still be requested.

3. **Required fields**: Ensure all mandatory fields are populated: `invoice_type`, `invoice_number`, `invoice_date`, `supplier.tax_id`, `buyer.tax_id`, line items with valid VAT calculations.

4. **VAT calculation verification**: Confirm that `vat_amount` equals `total_before_vat * vat_rate / 100` for each line item, and totals are consistent.

5. **Date validation**: `invoice_date` must not be in the future and must not be more than 6 months in the past.

### Step 5: Submit the Invoice for Allocation Number

Submit the validated invoice to the SHAAM API:

```bash
curl -X POST "${SHAAM_BASE_URL}/invoices" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d @invoice.json
```

Successful response (HTTP 201):

```json
{
  "allocation_number": "IL-2026-0308-A1B2C3D4",
  "invoice_reference": "INV-2026-001234",
  "status": "approved",
  "valid_until": "2026-04-07T23:59:59Z",
  "qr_code_data": "https://www.invoice.gov.il/verify/IL-2026-0308-A1B2C3D4"
}
```

The `allocation_number` (mispar haktsa'a) must be printed on the invoice. The `qr_code_data` URL allows the buyer to verify the invoice online.

### Step 6: Handle Batch Submissions

For high-volume invoicing, use the batch endpoint:

```bash
curl -X POST "${SHAAM_BASE_URL}/invoices/batch" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "invoices": [
      { ... },
      { ... }
    ]
  }'
```

Batch response:

```json
{
  "batch_id": "BATCH-20260308-001",
  "total_submitted": 15,
  "accepted": 13,
  "rejected": 2,
  "results": [
    {
      "invoice_reference": "INV-2026-001234",
      "status": "approved",
      "allocation_number": "IL-2026-0308-A1B2C3D4"
    },
    {
      "invoice_reference": "INV-2026-001235",
      "status": "rejected",
      "error_code": "BUYER_TAX_ID_INVALID",
      "error_message": "Buyer tax ID failed validation"
    }
  ]
}
```

Maximum batch size is 100 invoices per request. For larger volumes, split into multiple batches with a 1-second delay between requests.

### Step 7: Query Allocation Number Status

Check the status of a previously submitted invoice:

```bash
curl -X GET "${SHAAM_BASE_URL}/invoices/{invoice_reference}/status" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

Response:

```json
{
  "invoice_reference": "INV-2026-001234",
  "allocation_number": "IL-2026-0308-A1B2C3D4",
  "status": "approved",
  "created_at": "2026-03-08T10:30:00Z",
  "valid_until": "2026-04-07T23:59:59Z"
}
```

### Step 8: Handle Credit Notes

When issuing a credit note (hashbonit zikuy), reference the original invoice:

```json
{
  "invoice_type": "hashbonit_zikuy",
  "invoice_number": "CN-2026-000045",
  "invoice_date": "2026-03-08",
  "original_invoice_reference": "INV-2026-001234",
  "original_allocation_number": "IL-2026-0308-A1B2C3D4",
  "reason": "Partial service cancellation",
  "line_items": [
    {
      "description": "Software Development Services - Credit",
      "quantity": -1,
      "unit_price": 5000.00,
      "vat_rate": 17,
      "total_before_vat": -5000.00,
      "vat_amount": -850.00,
      "total_with_vat": -5850.00
    }
  ],
  "totals": {
    "total_before_vat": -5000.00,
    "total_vat": -850.00,
    "total_with_vat": -5850.00
  }
}
```

Credit notes receive their own allocation number and must reference the original.

## Examples

### Example 1: Generate a Standard Tax Invoice Above Threshold

User says: "Create an e-invoice for 30,000 NIS plus VAT to buyer with tax ID 514788338 for consulting services"

Actions:
1. Authenticate with SHAAM API using stored OAuth2 credentials
2. Validate buyer tax ID 514788338 using check digit algorithm (weights [1,2,1,2,1,2,1,2,1], sum mod 10 = 0)
3. Calculate VAT: 30,000 * 0.17 = 5,100 NIS, total = 35,100 NIS
4. Confirm total 35,100 NIS exceeds current threshold, allocation number required
5. Construct invoice JSON with `invoice_type: "hashbonit_mas"`
6. Submit to `POST /invoices` endpoint
7. Receive allocation number `IL-2026-0308-X7Y8Z9W0`
8. Return formatted invoice with allocation number and QR code URL

Result: Tax invoice created with allocation number IL-2026-0308-X7Y8Z9W0. Buyer can deduct 5,100 NIS input VAT.

### Example 2: Batch Submit Monthly Invoices

User says: "Submit all 25 invoices from March 2026 billing cycle to SHAAM"

Actions:
1. Authenticate with SHAAM API
2. Read all 25 invoice records from the billing system
3. Validate each invoice: buyer tax IDs, VAT calculations, required fields
4. Flag 2 invoices with invalid buyer tax IDs, set aside for manual review
5. Submit 23 valid invoices in a single batch via `POST /invoices/batch`
6. Process batch response: 22 approved, 1 rejected (duplicate invoice number)
7. Report results: 22 allocation numbers received, 1 duplicate to fix, 2 pending manual review

Result: 22 invoices received allocation numbers. 3 invoices require attention (2 invalid tax IDs, 1 duplicate number).

### Example 3: Issue a Credit Note for a Partial Refund

User says: "Issue a credit note for 8,000 NIS against invoice INV-2026-000789"

Actions:
1. Authenticate with SHAAM API
2. Query original invoice status via `GET /invoices/INV-2026-000789/status`
3. Confirm original has allocation number IL-2026-0215-M3N4P5Q6
4. Build credit note JSON with `invoice_type: "hashbonit_zikuy"`, negative amounts
5. Include `original_invoice_reference` and `original_allocation_number`
6. Submit to `POST /invoices`
7. Receive credit note allocation number

Result: Credit note CN-2026-000120 issued with its own allocation number, referencing original invoice.

## Troubleshooting

### Error: "BUYER_TAX_ID_INVALID"

Cause: The buyer's 9-digit VAT number (osek murshe) failed the check digit validation, or the tax ID is not registered as an active VAT-registered business with the Tax Authority.

Solution:
1. Verify the tax ID using the check digit algorithm: multiply each digit by weights [1,2,1,2,1,2,1,2,1], sum the digits of each product, total mod 10 must equal 0
2. Check that the business is actively registered at `https://www.misim.gov.il/mm-hofashosek/`
3. If the buyer is a non-VAT-registered business (osek patur), an allocation number is not required

### Error: "DUPLICATE_INVOICE_NUMBER"

Cause: An invoice with the same `invoice_number` was already submitted to SHAAM by your supplier tax ID.

Solution:
1. Query the existing invoice via `GET /invoices/{invoice_number}/status`
2. If the original was approved, use the existing allocation number
3. If you need to resubmit a corrected version, issue a credit note against the original and create a new invoice with a different number

### Error: "TOKEN_EXPIRED" or "UNAUTHORIZED"

Cause: The OAuth2 access token has expired (tokens are valid for 60 minutes) or credentials are invalid.

Solution:
1. Request a new token from the OAuth2 endpoint using client credentials
2. Verify `SHAAM_CLIENT_ID` and `SHAAM_CLIENT_SECRET` are correct
3. Check that your software registration with ITA is still active
4. For sandbox, ensure you are using the sandbox token endpoint, not production

### Error: "VAT_CALCULATION_MISMATCH"

Cause: The submitted VAT amounts do not match the expected calculation based on the line item totals and VAT rate.

Solution:
1. Recalculate: `vat_amount = total_before_vat * vat_rate / 100`
2. Ensure rounding is consistent (round to 2 decimal places, use banker's rounding)
3. Verify that `totals.total_vat` equals the sum of all line item `vat_amount` values
4. Verify that `totals.total_with_vat` equals `totals.total_before_vat + totals.total_vat`

### Error: "INVOICE_DATE_OUT_OF_RANGE"

Cause: The invoice date is either in the future or more than 6 months in the past.

Solution:
1. Set `invoice_date` to today's date or the actual transaction date
2. For backdated invoices older than 6 months, contact ITA support for manual processing
3. Ensure the date format is ISO 8601: `YYYY-MM-DD`
