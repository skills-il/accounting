---
name: green-invoice
description: Integrate Green Invoice (Morning) API for Israeli invoicing, receipts, client management, and payment processing. Use when user asks to create invoices via Green Invoice, generate hashbonit mas through Morning API, manage clients in Green Invoice, set up webhook automation for document creation, query documents or expenses, or mentions "Green Invoice", "Morning", "hashbonit yeruka", "greeninvoice API", Israeli cloud invoicing, or needs to create tax invoice-receipt (cheshbonit mas/kabala). Covers all 13 document types, 8 payment types, client CRUD, item catalog, and webhook integration. Do NOT use for SHAAM allocation numbers or Tax Authority e-invoice compliance (use israeli-e-invoice), Cardcom payment processing (use cardcom-payment-gateway), or Tranzila integration (use tranzila-payment-gateway).
license: MIT
compatibility: Requires network access for Green Invoice API calls (api.greeninvoice.co.il). API access requires a Best plan or higher; webhooks require Extra plan. API credentials obtained from the dashboard (Personal Area, Developer Tools, API Keys). Works with Claude Code, Claude.ai, Cursor.
---


# Green Invoice (Morning)

## Instructions

### Step 1: Authentication and Plan Requirements

Green Invoice uses JWT Bearer token authentication. Obtain API credentials from the Green Invoice dashboard: Personal Area (אזור אישי) > Developer Tools (כלים למפתחים) > API Keys (מפתחות API).

**Plan gating (verified May 2026):**
- API access (any endpoint): requires the **Best** plan or higher (`זמין למנויי Best ומעלה`).
- Webhooks (Step 11): require the **Extra** plan or higher (`זמין למנויים במסלול Extra`).

Lower-tier accounts will not see the "API Keys" or "Webhooks" menu items at all. If a user reports a missing menu item, check their plan first.

**Rebrand note.** The product was rebranded from "חשבונית ירוקה" to "Morning של חשבונית ירוקה" but the API host (`api.greeninvoice.co.il`), dashboard host (`app.greeninvoice.co.il`), and account credentials are unchanged. There is no separate `api.morning.co.il` host - DNS does not resolve there. If an agent finds documentation pointing to a Morning-only host, it is wrong.

**Base URLs:**

| Environment | Base URL |
|-------------|----------|
| Production | `https://api.greeninvoice.co.il/api/v1` |
| Sandbox | `https://sandbox.d.greeninvoice.co.il/api/v1` |

**Get a token:**

```bash
curl -X POST https://api.greeninvoice.co.il/api/v1/account/token \
  -H "Content-Type: application/json" \
  -d '{"id": "YOUR_API_KEY_ID", "secret": "YOUR_API_KEY_SECRET"}'
```

The response includes a JWT token. Use it in all subsequent requests:

```
Authorization: Bearer <token>
Content-Type: application/json
```

Always start by verifying credentials work:

```bash
curl -s https://api.greeninvoice.co.il/api/v1/users/me \
  -H "Authorization: Bearer <token>" | python3 -m json.tool
```

### Step 2: Tax Authority Authorization (Required for B2B Invoices Over the Threshold)

**This step is mandatory for any user issuing B2B `חשבונית מס` (Tax Invoice, type 305) or `חשבונית מס/קבלה` (Tax Invoice-Receipt, type 320) over the SHAAM allocation-number threshold. Skipping it silently breaks VAT deduction for the buyer.**

The threshold schedule (amounts are NET, before VAT):

| Effective from | Threshold |
|----------------|-----------|
| Jan 1, 2026 | NIS 10,000 |
| Jun 1, 2026 onward (final step) | NIS 5,000 |

Above the threshold, every B2B tax invoice must carry a `מספר הקצאה` (allocation number) issued by שע"מ (the Tax Authority). Without it, the recipient business cannot deduct input VAT - meaning your customer cannot legally reclaim the VAT they paid you.

**Morning attaches the allocation number automatically, BUT ONLY AFTER a one-time authorization grant in the user's Morning account.** This is NOT automatic on signup. The user must:

1. In the Morning dashboard, navigate to: `אזור אישי > רשות המיסים > הוספת הרשאה` (Personal Area > Tax Authority > Add Authorization)
2. The dashboard redirects to the Tax Authority gov.il portal for identity verification
3. After authorization, the browser returns automatically to Morning, and the connection becomes active

Vendor quote on what happens once active:
> "מספר ההקצאה מתנהל אוטומטית" - the allocation number is managed automatically.
> "מספר הקצאה לחשבונית מס יוצמד לחשבונית באמצעות המערכת שלנו, מבלי שצריך יהיה להיכנס לעוד פלטפורמות" - the allocation number is attached to the tax invoice via our system, without needing to enter another platform.

**Critical: the authorization expires every 3 months and must be renewed manually.** Morning sends a reminder email 10 days before expiry and displays a banner in the dashboard. If the authorization lapses, qualifying invoices created via the API still succeed at HTTP level, but ship WITHOUT an allocation number - your customer's accountant will reject them.

**What to do in code:**
1. Surface this requirement to the human user before they create their first large B2B invoice - the API does not currently expose a `tax_authority_connection_active` flag in public docs.
2. After creating a qualifying B2B invoice, fetch the resulting document with `GET /v1/documents/{id}` and check the PDF / response for an allocation number. If missing, the user's authorization is lapsed or was never set up.
3. The exact response-body field name carrying the allocation number is not documented publicly. Inspect a real authorized invoice via the in-app API explorer (`https://app.greeninvoice.co.il/api`) to learn the field for your account.

This skill does not cover SHAAM compliance end-to-end (allocation-number lifecycle, IRS-Israel filing). For that, use the `israeli-e-invoice` skill alongside this one.

### Step 3: Understand Document Types

Green Invoice supports 13 document types. Each has a numeric code used in API calls.

| Code | Hebrew | English | Common Use |
|------|--------|---------|------------|
| 10 | הצעת מחיר | Price Quote | Pre-sale proposals |
| 100 | הזמנה | Order | Confirmed orders |
| 200 | תעודת משלוח | Delivery Note | Shipment documentation |
| 210 | תעודת החזרה | Return Note | Product returns |
| 300 | חשבון עסקה | Transaction Invoice | Invoice without payment |
| 305 | חשבונית מס | Tax Invoice | Standalone tax invoice |
| 320 | חשבונית מס / קבלה | Tax Invoice-Receipt | Most common for Israeli clients |
| 330 | חשבונית זיכוי | Credit Note | Refunds and corrections |
| 400 | קבלה | Receipt | Payment confirmation |
| 405 | קבלה על תרומה | Donation Receipt | Non-profit donations |
| 500 | הזמנת רכש | Purchase Order | Procurement |
| 600 | קבלת פיקדון | Deposit Receipt | Security deposits |
| 610 | משיכת פיקדון | Deposit Withdrawal | Deposit returns |

**Key rule:** For Israeli clients who pay immediately, use type `320` (Tax Invoice-Receipt). For invoices where payment comes later, use type `300` (Transaction Invoice). For an export sale to a foreign client (osek murshe), issue a tax invoice (type `305` or `320`) with each income row zero-rated via `vatRate: 0`. Export of services is zero-rated (0%) under VAT Law Section 30, NOT exempt, so keep the rows taxable (`vatType: 0`) and set the rate to zero rather than marking them `vatType: 1` (Exempt). Use type `400` (Receipt) only to record a payment against an already-issued invoice, never as the sole document for a sale.

### Step 4: Create Documents

**POST** `/v1/documents`

Required fields: `type`, `client` (with `name` and `emails`), `income` (line items array).

```json
{
  "type": 320,
  "date": "2026-03-05",
  "lang": "he",
  "currency": "ILS",
  "vatType": 0,
  "rounding": true,
  "signed": true,
  "attachment": true,
  "client": {
    "name": "Moshe Cohen",
    "emails": ["moshe@example.com"],
    "taxId": "123456789",
    "add": true
  },
  "income": [
    {
      "description": "Web Development Services",
      "quantity": 1,
      "price": 5000,
      "currency": "ILS",
      "vatType": 0
    }
  ],
  "payment": [
    {
      "type": 4,
      "date": "2026-03-05",
      "price": 5000,
      "currency": "ILS"
    }
  ]
}
```

**VAT types (document level):**

| Code | Meaning |
|------|---------|
| 0 | Default (VAT added based on business type) |
| 1 | Exempt (no VAT) |
| 2 | Mixed (some items exempt, some not) |

**VAT types (income row level):** the income-row `vatType` uses the SAME enum as the document level. To set a specific rate on a line (e.g. 0% for a zero-rated export line), use the separate `vatRate` field, a decimal fraction (`0` for 0%, `0.18` for 18%). There is no "VAT included in price" value; verify field names against the canonical docs at `developers.morning.co`.

| Code | Meaning |
|------|---------|
| 0 | Default (follows document VAT setting) |
| 1 | Exempt (VAT-free) |
| 2 | Mixed |

### Step 5: Payment Types

When adding payment records to a document, use these type codes:

| Code | Hebrew | English |
|------|--------|---------|
| -1 | לא שולם | Unpaid |
| 0 | ניכוי במקור | Withholding Tax |
| 1 | מזומן | Cash |
| 2 | המחאה | Check |
| 3 | כרטיס אשראי | Credit Card |
| 4 | העברה בנקאית | Bank Transfer |
| 5 | פייפאל | PayPal |
| 10 | אפליקציית תשלום | Payment App (Bit, PayBox) |
| 11 | אחר | Other |

**Credit card types** (when payment type is 3):

| Code | Card |
|------|------|
| 1 | Isracard |
| 2 | Visa |
| 3 | Mastercard |
| 4 | American Express |
| 5 | Diners |

**Credit card deal types:**

| Code | Type |
|------|------|
| 1 | Regular (ragil) |
| 2 | Installments (tashlumim) |
| 3 | Credit |
| 4 | Deferred (chiyuv nidche) |

### Step 6: Manage Clients

**Create client:** `POST /v1/clients`

```json
{
  "name": "Startup Ltd.",
  "emails": ["billing@startup.co.il"],
  "taxId": "515123456",
  "country": "IL",
  "city": "Tel Aviv",
  "address": "Rothschild 45",
  "paymentTerms": 30,
  "labels": ["tech", "monthly"]
}
```

**Payment terms:**

| Code | Meaning |
|------|---------|
| -1 | Immediate (shotef) |
| 0 | End of month (shotef sof chodesh) |
| 30 | End of month + 30 (shotef plus 30) |
| 60 | End of month + 60 |
| 90 | End of month + 90 |

**Other client endpoints:**

| Method | Path | Description |
|--------|------|-------------|
| GET | `/v1/clients/{id}` | Get client by ID |
| PUT | `/v1/clients/{id}` | Update client |
| DELETE | `/v1/clients/{id}` | Delete client |
| POST | `/v1/clients/search` | Search clients |

**Search clients:**

```json
{
  "name": "Startup",
  "active": true,
  "page": 0,
  "pageSize": 25
}
```

### Step 7: Search and Query Documents

**POST** `/v1/documents/search`

```json
{
  "page": 0,
  "pageSize": 25,
  "type": [320, 305],
  "status": [0, 1],
  "fromDate": "2026-01-01",
  "toDate": "2026-03-31",
  "sort": "documentDate"
}
```

**Document statuses:**

| Code | Meaning |
|------|---------|
| 0 | Open |
| 1 | Closed |
| 2 | Manually closed |
| 3 | Canceling another document |
| 4 | Canceled |

**Get document:** `GET /v1/documents/{id}`

**Close document:** `POST /v1/documents/{id}/close`

**Download document PDF:** `GET /v1/documents/{id}/download/links` returns URLs in Hebrew, English, and original language.

### Step 8: Link Documents

Documents can be linked to create workflows. Use `linkedDocumentIds` when creating a new document.

Common linking patterns:

| Scenario | Steps |
|----------|-------|
| Invoice then receipt | Create type 300 (invoice), later create type 400 (receipt) with `linkedDocumentIds: ["invoice-id"]` |
| Credit note for invoice | Create type 330 (credit note) with `linkedDocumentIds: ["original-id"]` and `linkType: "cancel"` |
| Quote to order to invoice | Create type 10 (quote), then type 100 (order), then type 300 (invoice), linking each |

When a receipt is linked to an invoice with full payment, the invoice automatically closes.

### Step 9: Item Catalog

Manage reusable product/service items:

| Method | Path | Description |
|--------|------|-------------|
| POST | `/v1/items` | Create item |
| GET | `/v1/items/{id}` | Get item |
| PUT | `/v1/items/{id}` | Update item |
| POST | `/v1/items/search` | Search items |

Use `itemId` in income line items to reference catalog items instead of manually specifying description and price each time.

### Step 10: Business Types and VAT Rules

Green Invoice handles VAT automatically based on business type:

| Code | Hebrew | English | VAT Behavior |
|------|--------|---------|-------------|
| 1 | עוסק מורשה | Licensed Dealer (Osek Murshe) | VAT added (18% as of 2026) |
| 2 | חברה בע"מ | Ltd. Company | VAT added |
| 3 | עוסק פטור | Exempt Dealer (Osek Patur) | No VAT |
| 4 | עמותה | Non-Profit (Amuta) | No VAT |
| 5 | חברה לתועלת הציבור | Public Benefit Company | No VAT |
| 6 | שותפות | Partnership | VAT added |

Set `vatType: 0` on documents and the system applies the correct VAT based on your business type. Override with `vatType: 1` for exempt transactions or `vatType: 2` for mixed documents.

### Step 11: Webhooks

**Tier requirement:** webhook configuration requires the **Extra** plan or higher. Lower-tier accounts will not see the menu item.

Configure webhooks in the dashboard at: Personal Area (אזור אישי) > Developer Tools (כלים למפתחים) > Webhooks. The earlier "Settings > Developer Tools" path is no longer correct after the 2025 dashboard restructure.

Webhooks fire on document creation. The payload includes the full document object:

```json
{
  "id": "document-uuid",
  "type": 320,
  "number": 12345,
  "currency": "ILS",
  "date": "2026-03-05",
  "total": 5850,
  "recipient": {
    "name": "Client Name",
    "emails": ["client@example.com"]
  },
  "items": [
    {
      "description": "Service",
      "quantity": 1,
      "price": 5000
    }
  ],
  "files": {
    "signed": true,
    "downloadLinks": {
      "he": "https://www.greeninvoice.co.il/api/v1/documents/download?d=...",
      "en": "https://www.greeninvoice.co.il/api/v1/documents/download?d=..."
    }
  }
}
```

Common webhook automations:
- Save PDF to Google Drive or Dropbox on invoice creation
- Update CRM when a receipt is issued
- Send Slack notification for new documents
- Sync invoices to external accounting systems

Consult `references/api-reference.md` for the complete webhook payload schema.

### Step 12: Currencies and Exchange Rates

Green Invoice supports 27 document currencies. If `currencyRate` is not specified, the system uses Bank of Israel (BOI) exchange rates for the document date.

Common currencies: ILS, USD, EUR, GBP, JPY, CHF, CAD, AUD.

For multi-currency invoices, each income line item can specify its own `currency` and `currencyRate`. The totals are always calculated in the document's base currency.

### Step 13: Sandbox Testing

Always test in the sandbox environment before going to production:

1. Register for a sandbox account at the Green Invoice sandbox
2. Use base URL: `https://sandbox.d.greeninvoice.co.il/api/v1`
3. Generate sandbox API credentials
4. Test all document creation, client management, and webhook flows
5. Verify VAT calculations and document linking work correctly
6. Switch to production URL when ready

## Examples

### Example 1: Create Tax Invoice-Receipt for Israeli Client

User says: "Create a hashbonit mas kabala for a client paying by bank transfer"

Actions:
1. Authenticate with Green Invoice API
2. Create client if new (POST `/v1/clients` with name, email, taxId)
3. Create document type 320 (Tax Invoice-Receipt) with payment type 4 (bank transfer)
4. Set `signed: true` for digital signature, `attachment: true` to email PDF

Result: Tax invoice-receipt created, digitally signed, and emailed to client as PDF.

### Example 2: Monthly Recurring Invoices

User says: "I need to send monthly invoices to 3 retainer clients"

Actions:
1. Search existing clients: POST `/v1/clients/search` with client names
2. For each client, create document type 300 (Transaction Invoice) with description "Monthly Retainer - March 2026"
3. Set `dueDate` to payment terms date, `lang` based on client preference
4. Documents are emailed automatically when `attachment: true`

Result: Three invoices created and sent, each with correct payment terms and language.

### Example 3: Issue Credit Note for Partial Refund

User says: "Refund half the amount on invoice #12345"

Actions:
1. Get original document: GET `/v1/documents/{id}`
2. Calculate refund amount (half of original total)
3. Create document type 330 (Credit Note) with `linkedDocumentIds: ["original-id"]` and `linkType: "cancel"`
4. Set income amount to negative refund value

Result: Credit note issued, linked to original invoice, with partial refund amount.

### Example 4: Webhook Automation for Document Filing

User says: "Set up automatic filing when Green Invoice creates a document"

Actions:
1. Configure webhook URL in Green Invoice dashboard
2. Implement webhook endpoint that receives document payload
3. Extract `type` field to route document (invoice vs receipt vs credit note)
4. Use `files.downloadLinks.he` to download the Hebrew PDF
5. File to appropriate folder based on document type and date

Result: All new documents automatically downloaded and organized by type and month.

## Bundled Resources

### Scripts
- `scripts/green-invoice-client.py` -- Python helper for common Green Invoice API operations: authenticate, create documents, search clients, and list recent documents. Run: `python3 scripts/green-invoice-client.py --help`

### References
- `references/api-reference.md` -- Complete Green Invoice API endpoint reference with request/response schemas, all enum codes, and payload examples. Consult when building API integrations or debugging request formats.
- `references/document-workflows.md` -- Common Israeli business document workflows: freelancer billing, retainer invoicing, refund flows, multi-currency billing, and e-commerce integration patterns. Consult when designing invoicing automation or choosing the correct document type sequence.

## Recommended MCP Servers

| MCP | What It Adds |
|-----|-------------|
| [BOI Exchange Rates](https://agentskills.co.il/he/mcp/boi-exchange) | Official Bank of Israel exchange rates for multi-currency invoice calculations. Green Invoice uses BOI rates by default when `currencyRate` is not specified. |

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Morning API Documentation (canonical) | https://developers.morning.co | Current "morning API v2.0.0" docs. Authoritative for enum MEANINGS (vatType, document type codes, payment types) and field names. Supersedes Apiary for semantics. |
| Green Invoice Developer Docs | https://www.greeninvoice.co.il/api-docs/ | Endpoint schemas, request/response formats. Public portal to the live Apiary interactive reference. |
| Apiary Interactive Reference | https://greeninvoice.docs.apiary.io/ | Most detailed API reference: JWT token flow, add-document body schema, all enum tables (document types, payment types). |
| Green Invoice In-App API Explorer | https://app.greeninvoice.co.il/api | Interactive API explorer (requires sign-in). Authoritative for current request/response field names. |
| Tax Authority Connection Guide | https://www.greeninvoice.co.il/help-center/developers/tax-auth-connect/ | How to enable the gov.il authorization required for SHAAM allocation numbers (see Step 2) |
| Generating API Key Guide | https://www.greeninvoice.co.il/help-center/generating-api-key/ | Current dashboard menu path and plan-tier requirements for API access |
| Webhooks Overview | https://www.greeninvoice.co.il/magazine/webhooks/ | Plan-tier requirement (Extra) and configuration walkthrough |
| Israel Tax Authority (VAT rates) | https://www.gov.il/he/departments/israel_tax_authority | Current VAT rate, business type rules |
| SHAAM E-Invoice System (Tax Authority) | https://www.gov.il/he/service/invoice-allocation-number | Allocation number requirements for B2B invoices. Current threshold: NIS 10,000 net (since Jan 1, 2026), drops to NIS 5,000 net on Jun 1, 2026 (final step). |
| Bank of Israel Exchange Rates | https://www.boi.org.il/en/economic-roles/financial-markets/exchange-rates/ | Daily representative rates used by Green Invoice for multi-currency documents |

## Gotchas

- Green Invoice was rebranded to "Morning" but the API domain remains `api.greeninvoice.co.il`. Agents may search for a "Morning API" that does not exist under that name.
- The most common document type for Israeli clients paying immediately is type 320 (Tax Invoice-Receipt), not type 305 (Tax Invoice). Agents may default to 305 because it sounds like the standard invoice type.
- Osek Patur (exempt dealer) businesses cannot issue Tax Invoices (type 305). Agents may not check the business type before selecting a document type, causing API errors.
- VAT rate in Israel is 18% as of 2026, not 17%. The rate changed in January 2025 and agents trained on older data may use the outdated 17% figure in calculations.
- Payment type code 10 covers Israeli payment apps (Bit, PayBox), which are extremely common in Israel. Agents may not know these apps exist and default to bank transfer or credit card only. Note: Pepper Pay shut down on Apr 10, 2022; do not present it as a payment option. The historical enum value `subAppType: 2` may still exist for legacy rows but should not be used for new payments.
- **SHAAM allocation number requires a one-time gov.il authorization in the user's Morning account.** This is the most common reason API integrations "look correct" but produce invoices the customer's accountant rejects. The integration is NOT automatic on signup. See Step 2 for the full setup, the 3-month expiry, and the renewal workflow. The threshold is currently NIS 10,000 net (since Jan 1, 2026) and drops to NIS 5,000 net on Jun 1, 2026 (final step in the rollout). Pair with the `israeli-e-invoice` skill for end-to-end SHAAM compliance.
- **Plan tiers gate features in the dashboard.** API access requires the Best plan; webhooks require the Extra plan. A user on a lower tier will not see "API Keys" or "Webhooks" in the dashboard menu - this is not a bug, it is the gate. Check the plan before debugging missing menu items.
- **Webhook signature verification.** Treat any unverified webhook payload as suspect. The current signature header name and hashing algorithm are NOT documented in the public help-center articles as of May 2026 - inspect the headers on a real test webhook delivery to your endpoint (sandbox or production), or sign in to the in-app API explorer to learn the current scheme. As a safety net, on receipt of a webhook always do a server-to-server `GET /v1/documents/{id}` lookup with your authenticated API token before trusting any field on the payload.
- **Use the Apiary interactive reference for exact schemas.** `https://greeninvoice.docs.apiary.io/` is live and is the most detailed API reference: it documents the JWT token flow, the add-document request body, and every enum table. The `https://www.greeninvoice.co.il/api-docs/` portal (public) and `https://app.greeninvoice.co.il/api` (signed-in explorer) surface the same content. When a field name is unclear, confirm it against Apiary rather than guessing.
- **Rate limits.** The API allows roughly 3 requests per second per token before returning HTTP 429. The exact ceiling is not published; treat 429 as a soft error and back off exponentially. For batch operations, add a queue.

## Troubleshooting

### Error: "401 Unauthorized" on API calls
Cause: JWT token expired or invalid credentials
Solution: Tokens expire periodically. Re-authenticate by calling POST `/v1/account/token` with your API key ID and secret. Verify credentials in the Green Invoice dashboard under Personal Area (אזור אישי) > Developer Tools (כלים למפתחים) > API Keys. If the menu item is missing, the account is on a lower-tier plan; API access requires Best or higher.

### Error: "Document type not supported for your business type"
Cause: Osek Patur (exempt dealer) cannot issue Tax Invoices (type 305)
Solution: Check your business type. Osek Patur should use type 320 (Tax Invoice-Receipt) or type 400 (Receipt). Osek Murshe and Ltd. companies can use all document types.

### Error: "VAT calculation mismatch"
Cause: Mixing vatType settings between document level and income row level
Solution: Set `vatType: 0` at document level to use defaults. Only override at the income row level when a line's VAT treatment differs from the document. To apply a specific rate to a line (e.g. 0% on a zero-rated export line), set the row's `vatRate` (decimal), not `vatType`.

### Error: "Client email required"
Cause: Creating a document without providing client email
Solution: The `client.emails` array must contain at least one valid email when `attachment: true`. For documents that should not be emailed, set `attachment: false`.

### Issue: B2B invoice over NIS 10,000 missing allocation number / customer's accountant rejected it
Cause: The Tax Authority authorization in the Morning dashboard was never set up, or it expired (3-month TTL). The API call succeeded (HTTP 200) but the resulting invoice has no `מספר הקצאה`. The recipient business cannot deduct input VAT without it.
Solution: Direct the user to: `אזור אישי > רשות המיסים > הוספת הרשאה` in the Morning dashboard, complete the gov.il redirect, then re-issue or re-send the invoice. If the connection had been active and just expired, Morning sent a reminder email 10 days before expiry. Add this authorization-status check to your runbook before any qualifying B2B invoice creation. Threshold: NIS 10,000 net through May 31, 2026; NIS 5,000 net from Jun 1, 2026 onward. See Step 2 for full setup.

### Issue: "API Keys" or "Webhooks" menu items missing in dashboard
Cause: The user's plan does not include this feature. API access requires Best+; webhooks require Extra+.
Solution: Check the plan in Personal Area > Account/Subscription. Upgrade is required to proceed - there is no workaround at the API level.
