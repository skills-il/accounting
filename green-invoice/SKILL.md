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

**Rebrand note.** The product was rebranded from "חשבונית ירוקה" to "Morning של חשבונית ירוקה". The API host (`api.greeninvoice.co.il`) and dashboard host (`app.greeninvoice.co.il`) are unchanged, and there is still no `api.morning.co.il`. But do NOT extend that to "no Morning host exists": the current documentation puts the OAuth token endpoint on `api.morning.co`, which is a different hostname from the one that does not resolve.

**Two authentication flows are live right now (both verified 2026-07-27). Use OAuth 2.0 for new work.**

The published documentation at `developers.morning.co` (versioned "morning API Documentation (2.0.0)") now states: "Our APIs use the OAuth 2.0 protocol for authentication and authorization." The older API-key flow still answers, so existing integrations are not broken, but it is no longer the documented path and should be treated as legacy.

| | OAuth 2.0 (documented, use this) | Legacy API-key flow |
|---|---|---|
| Token endpoint | `POST https://api.morning.co/idp/v1/oauth/token` | `POST https://api.greeninvoice.co.il/api/v1/account/token` |
| Sandbox token endpoint | `https://api.sandbox.morning.dev/idp/v1/oauth/token` | same host as production, sandbox base URL |
| Grant | `client_credentials` | JSON body with `id` + `secret` |
| Response field | `accessToken` (a signed JWT) | JWT token |
| Token lifetime | 1 hour | treat as short-lived; refresh on 401 |
| Errors | OAuth 2.0 / RFC 6749 format (`invalid_client`, `unauthorized_client`, ...) | Green Invoice error object (`errorCode` / `errorMessage`) |

Both return a bearer token used the same way against the same API base URL, so the only thing that changes is how you obtain it. If you are writing new code, use the OAuth endpoint; if you are maintaining an integration on `/account/token`, it still works today but plan the migration.

Note the error mapping on the OAuth endpoint, because two of its codes are business-state rather than credential problems: `invalid_grant` means the API key is expired, revoked or pending, and `unauthorized_client` means there is no active subscription or the subscription does not include API access. Neither is fixed by re-issuing keys.

**Base URLs:**

| Environment | Base URL |
|-------------|----------|
| Production | `https://api.greeninvoice.co.il/api/v1` |
| Sandbox | `https://sandbox.d.greeninvoice.co.il/api/v1` |

**Get a token (OAuth 2.0, the documented path):**

```bash
curl -X POST https://api.morning.co/idp/v1/oauth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'grant_type=client_credentials' \
  -d 'client_id=YOUR_API_KEY_ID' \
  -d 'client_secret=YOUR_API_KEY_SECRET'
```

The response carries `accessToken`, a signed JWT valid for 1 hour.

**Get a token (legacy API-key flow, still functional):**

```bash
curl -X POST https://api.greeninvoice.co.il/api/v1/account/token \
  -H "Content-Type: application/json" \
  -d '{"id": "YOUR_API_KEY_ID", "secret": "YOUR_API_KEY_SECRET"}'
```

Either way you end up with a JWT. Use it in all subsequent requests:

```
Authorization: Bearer <token>
Content-Type: application/json
```

Always start by verifying credentials work:

```bash
curl -s https://api.greeninvoice.co.il/api/v1/documents/info \
  -H "Authorization: Bearer <token>" | python3 -m json.tool
```

### Step 2: Tax Authority Authorization (Required for B2B Invoices Over the Threshold)

**This step is mandatory for any user issuing B2B `חשבונית מס` (Tax Invoice, type 305) or `חשבונית מס/קבלה` (Tax Invoice-Receipt, type 320) over the SHAAM allocation-number threshold. Skipping it silently breaks VAT deduction for the buyer.**

The threshold schedule (amounts are NET, before VAT):

| Effective from | Threshold |
|----------------|-----------|
| Jan 1, 2026 | NIS 10,000 |
| Jun 1, 2026 onward (final step) | **NIS 5,000 (in force now)** |

Above the threshold, every B2B tax invoice must carry a `מספר הקצאה` (allocation number) issued by שע"מ (the Tax Authority). Without it, the recipient business cannot deduct input VAT - meaning your customer cannot legally reclaim the VAT they paid you.

**Morning attaches the allocation number automatically, BUT ONLY AFTER a one-time authorization grant in the user's Morning account.** This is NOT automatic on signup. The user must:

1. In the Morning dashboard, navigate to: `אזור אישי > רשות המיסים > הוספת הרשאה` (Personal Area > Tax Authority > Add Authorization)
2. The dashboard redirects to the Tax Authority gov.il portal for identity verification
3. After authorization, the browser returns automatically to Morning, and the connection becomes active

Vendor quote on what happens once active:
> "מספר ההקצאה מתנהל אוטומטית" - the allocation number is managed automatically.
> "מספר הקצאה לחשבונית מס יוצמד לחשבונית באמצעות המערכת שלנו, מבלי שצריך יהיה להיכנס לעוד פלטפורמות" - the allocation number is attached to the tax invoice via our system, without needing to enter another platform.

**Critical: the authorization expires every 3 months and must be renewed manually.** Morning's help centre states the connection is valid for 3 months and that an alert appears in the system 10 days before it expires. Do not rely on an email arriving: treat the 10-day in-system alert as the notice and check the connection status from your own runbook. If the authorization lapses, qualifying invoices created via the API still succeed at HTTP level, but ship WITHOUT an allocation number - your customer's accountant will reject them.

**What to do in code:**
1. Surface this requirement to the human user before they create their first large B2B invoice - the API does not currently expose a `tax_authority_connection_active` flag in public docs.
2. After creating a qualifying B2B invoice, fetch the resulting document with `GET /v1/documents/{id}` and check the PDF / response for an allocation number. If missing, the user's authorization is lapsed or was never set up.
3. The exact response-body field name carrying the allocation number is not documented publicly. Inspect a real authorized invoice via the in-app API explorer (`https://app.greeninvoice.co.il/api`) to learn the field for your account.

This skill does not cover SHAAM compliance end-to-end (allocation-number lifecycle, IRS-Israel filing). For that, use the `israeli-e-invoice` skill alongside this one.

### Step 3: Understand Document Types

Green Invoice supports 15 document types. Each has a numeric code used in API calls.

| Code | Hebrew | English | Common Use |
|------|--------|---------|------------|
| 10 | הצעת מחיר | Price Quote | Pre-sale proposals |
| 20 | חשבון / אישור תשלום | Account / Payment Confirmation | Non-tax payment acknowledgement |
| 100 | הזמנה | Order | Confirmed orders |
| 200 | תעודת משלוח | Delivery Note | Shipment documentation |
| 210 | תעודת החזרה | Return Note | Product returns |
| 300 | חשבון עסקה | Transaction Invoice | Invoice without payment |
| 305 | חשבונית מס | Tax Invoice | Standalone tax invoice |
| 320 | חשבונית מס / קבלה | Tax Invoice-Receipt | Most common for Israeli clients |
| 330 | חשבונית זיכוי | Credit Note | Refunds and corrections |
| 400 | קבלה | Receipt | Payment confirmation |
| 405 | קבלה על תרומה | Donation Receipt | Non-profit donations |
| 410 | ביטול תרומה | Donation Cancellation | Reversing a donation receipt |
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

**VAT types (income row level):** the income-row `vatType` is a DIFFERENT enum from the document-level one. A document uses `DocumentVatType` (`0` default, `1` exempt, `2` mixed); an income row uses `ItemVatType` (`0` default, `1` VAT included in price, `2` exempt). The two collide on the value `1`, so copying a document-level `vatType: 1` onto a row does not make the row exempt, it makes it VAT-inclusive and changes the amount charged. To set a specific rate on a line (e.g. 0% for a zero-rated export line), use the separate `vatRate` field, a decimal fraction (`0` for 0%, `0.18` for 18%).

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

**Non-profits: donation receipts carry a 2026 reporting obligation.** Since 1 January
2026 an amuta holding Section 46 authorization must report credit-granting donations to the
Tax Authority's digital donations system, and the reporting is meant to happen automatically
from receipt-issuing software that is connected to it (organisations on unconnected software
or paper receipts file through a dedicated Tax Authority application instead). This is the
same shape of trap as the SHAAM allocation number in Step 2: issuing a type 405 receipt
through the API can return HTTP 200 while the donation is not reported, and the donor's
Section 46 credit is what is at stake. If you are integrating for an amuta, confirm with
Morning whether donation reporting is connected for that account before assuming the API
call is the whole of compliance. Do not tell a non-profit they are compliant just because
the receipt was created.

**Do not confuse `עוסק זעיר` with any of the codes above.** Since Amendment 265 to the
Income Tax Ordinance a business can elect "micro-dealer" status, and users increasingly
describe themselves that way. It is an INCOME TAX classification governing how income is
computed, and it is independent of the VAT classification in this table. It is not a Green
Invoice business type, it does not appear in this enum, and it changes nothing about which
document type you issue or how VAT is applied. A business can be an osek patur for VAT and
a micro-dealer for income tax at the same time, or either one alone. If a user says they
are an עוסק זעיר, ask separately whether they are an osek patur or an osek murshe, because
that is the answer that determines the document type.

Set `vatType: 0` on documents and the system applies the correct VAT based on your business type. Override with `vatType: 1` for exempt transactions or `vatType: 2` for mixed documents.

### Step 10.5: Suppliers and Expenses (the purchase side)

Everything above is the sales side. An Israeli business also has to record what it BUYS,
because input VAT is only reclaimable against recorded supplier documents, and an exporter
or any osek murshe lives on that deduction. The API covers this and the endpoints are easy
to miss because they sit outside the document flow.

| Purpose | Endpoint |
|---------|----------|
| Create a supplier (a business or individual you buy from) | `POST /v1/suppliers` |
| Create an expense | `POST /v1/expenses` |

Two behaviours matter here. **An expense created WITH an attached file becomes a draft, not
an expense.** Uploading a receipt or supplier invoice produces an expense draft that has to
be reviewed and approved before it counts; until approval it is not an actual expense and
will not appear in your totals. An expense created without a file is live immediately. If
you are bulk-importing scanned supplier invoices and your reported expenses look far too
low, unapproved drafts are the first thing to check.

**Pair this with the allocation-number rule from Step 2 in the other direction.** When YOU
are the buyer, a supplier's tax invoice above the NIS 5,000 threshold needs its allocation
number for you to deduct the input VAT. Record it when the document arrives rather than at
period close.

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
| Morning API Documentation (canonical) | https://developers.morning.co | Current "morning API v2.0.0" docs. Authoritative for enum MEANINGS (vatType, document type codes, payment types), field names, and the current OAuth 2.0 auth flow. This is now the only live reference. |
| Green Invoice Developer Docs | https://www.greeninvoice.co.il/api-docs/ | Endpoint schemas, request/response formats. |
| Apiary Interactive Reference (RETIRED) | https://greeninvoice.docs.apiary.io/ | Dead as of 2026-07-27: returns HTTP 404, "Apiary - Page not found". It was live at the previous review on 2026-06-28. Do not send agents here. Use developers.morning.co instead. |
| Green Invoice In-App API Explorer | https://app.greeninvoice.co.il/api | Interactive API explorer (requires sign-in). Authoritative for current request/response field names. |
| Tax Authority Connection Guide | https://www.greeninvoice.co.il/help-center/developers/tax-auth-connect/ | How to enable the gov.il authorization required for SHAAM allocation numbers (see Step 2) |
| Generating API Key Guide | https://www.greeninvoice.co.il/help-center/generating-api-key/ | Current dashboard menu path and plan-tier requirements for API access |
| Webhooks Overview | https://www.greeninvoice.co.il/magazine/webhooks/ | Plan-tier requirement (Extra) and configuration walkthrough |
| Israel Tax Authority (VAT rates) | https://www.gov.il/he/departments/israel_tax_authority | Current VAT rate, business type rules |
| SHAAM E-Invoice System (Tax Authority) | https://www.gov.il/he/service/request-assignment-number-for-tax-invoice | Allocation number requirements for B2B invoices. Current threshold: NIS 5,000 net, in force since Jun 1, 2026 (final step of the rollout). |
| Bank of Israel Exchange Rates | https://www.boi.org.il/en/economic-roles/financial-markets/exchange-rates/ | Daily representative rates used by Green Invoice for multi-currency documents |

## Gotchas

- Green Invoice was rebranded to "Morning". The API base URL is still `api.greeninvoice.co.il/api/v1`, but a Morning host DOES now exist and is where the current OAuth token endpoint lives: `api.morning.co/idp/v1/oauth/token`. The hostname that does not resolve is `api.morning.co.il`. Do not tell a user that "the Morning API does not exist"; see Step 1 for both auth flows.
- The most common document type for Israeli clients paying immediately is type 320 (Tax Invoice-Receipt), not type 305 (Tax Invoice). Agents may default to 305 because it sounds like the standard invoice type.
- Osek Patur (exempt dealer) businesses cannot issue Tax Invoices (type 305). Agents may not check the business type before selecting a document type, causing API errors.
- VAT rate in Israel is 18% as of 2026, not 17%. The rate changed in January 2025 and agents trained on older data may use the outdated 17% figure in calculations.
- Payment type code 10 covers Israeli payment apps (Bit, PayBox), which are extremely common in Israel. Agents may not know these apps exist and default to bank transfer or credit card only. Note: Pepper Pay shut down on Apr 10, 2022; do not present it as a payment option. The historical enum value `subAppType: 2` may still exist for legacy rows but should not be used for new payments.
- **SHAAM allocation number requires a one-time gov.il authorization in the user's Morning account.** This is the most common reason API integrations "look correct" but produce invoices the customer's accountant rejects. The integration is NOT automatic on signup. See Step 2 for the full setup, the 3-month expiry, and the renewal workflow. The threshold is NIS 5,000 net, in force since Jun 1, 2026 and the final step of the rollout. It was NIS 10,000 between Jan 1 and May 31, 2026, so treat any integration written earlier in 2026 as skipping allocation numbers on invoices between 5,000 and 10,000, which silently breaks the customer's input-VAT deduction. Pair with the `israeli-e-invoice` skill for end-to-end SHAAM compliance.
- **Plan tiers gate features in the dashboard.** API access requires the Best plan; webhooks require the Extra plan. A user on a lower tier will not see "API Keys" or "Webhooks" in the dashboard menu - this is not a bug, it is the gate. Check the plan before debugging missing menu items.
- **Webhook signature verification.** Treat any unverified webhook payload as suspect. The current signature header name and hashing algorithm are NOT documented in the public help-center articles as of May 2026 - inspect the headers on a real test webhook delivery to your endpoint (sandbox or production), or sign in to the in-app API explorer to learn the current scheme. As a safety net, on receipt of a webhook always do a server-to-server `GET /v1/documents/{id}` lookup with your authenticated API token before trusting any field on the payload.
- **The Apiary reference is gone; use `developers.morning.co`.** `https://greeninvoice.docs.apiary.io/` now returns HTTP 404 ("Apiary - Page not found"), verified in a browser on 2026-07-27. It was live at the previous review a month earlier, so older guidance, including earlier versions of this skill, still points there. The canonical reference is now `https://developers.morning.co` ("morning API Documentation (2.0.0)"), with `https://app.greeninvoice.co.il/api` as the signed-in explorer. When a field name is unclear, confirm it there rather than guessing.
- **Rate limits.** The ceiling is not published, so do not code against a specific requests-per-second number. Treat HTTP 429 as a soft, expected error: back off exponentially and retry rather than failing the job. For batch operations put the calls behind a queue with a concurrency limit you can tune down when you see 429s.

## Troubleshooting

### Error: "401 Unauthorized" on API calls
Cause: JWT token expired or invalid credentials
Solution: Tokens expire. An OAuth access token is valid for exactly 1 hour, so a long batch run WILL hit this mid-way and must re-authenticate rather than fail. Re-authenticate against whichever flow you use: `POST https://api.morning.co/idp/v1/oauth/token` with `grant_type=client_credentials` (the documented path), or the legacy `POST /v1/account/token` with your API key ID and secret. On the OAuth endpoint, note that `invalid_grant` means the key is expired/revoked/pending and `unauthorized_client` means the subscription does not include API access; neither is fixed by retrying. Verify credentials in the Green Invoice dashboard under Personal Area (אזור אישי) > Developer Tools (כלים למפתחים) > API Keys. If the menu item is missing, the account is on a lower-tier plan; API access requires Best or higher.

### Error: "Document type not supported for your business type"
Cause: Osek Patur (exempt dealer) cannot issue Tax Invoices (type 305)
Solution: Check your business type. Osek Patur should use type 320 (Tax Invoice-Receipt) or type 400 (Receipt). Osek Murshe and Ltd. companies can use all document types.

### Error: "VAT calculation mismatch"
Cause: Mixing vatType settings between document level and income row level
Solution: Set `vatType: 0` at document level to use defaults. Only override at the income row level when a line's VAT treatment differs from the document. To apply a specific rate to a line (e.g. 0% on a zero-rated export line), set the row's `vatRate` (decimal), not `vatType`.

### Error: "Client email required"
Cause: Creating a document without providing client email
Solution: The `client.emails` array must contain at least one valid email when `attachment: true`. For documents that should not be emailed, set `attachment: false`.

### Issue: B2B invoice over the threshold missing allocation number / customer's accountant rejected it
Cause: The Tax Authority authorization in the Morning dashboard was never set up, or it expired (3-month TTL). The API call succeeded (HTTP 200) but the resulting invoice has no `מספר הקצאה`. The recipient business cannot deduct input VAT without it.
Solution: Direct the user to: `אזור אישי > רשות המיסים > הוספת הרשאה` in the Morning dashboard, complete the gov.il redirect, then re-issue or re-send the invoice. If the connection had been active and just expired, an in-system alert would have appeared 10 days before expiry. Add this authorization-status check to your runbook before any qualifying B2B invoice creation. Threshold: NIS 5,000 net, in force since Jun 1, 2026. If the integration was built earlier in 2026 against the NIS 10,000 figure, invoices between 5,000 and 10,000 are now going out without allocation numbers; re-check that band specifically. See Step 2 for full setup.

### Issue: "API Keys" or "Webhooks" menu items missing in dashboard
Cause: The user's plan does not include this feature. API access requires Best+; webhooks require Extra+.
Solution: Check the plan in Personal Area > Account/Subscription. Upgrade is required to proceed - there is no workaround at the API level.
