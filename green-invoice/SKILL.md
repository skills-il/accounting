---
name: green-invoice
description: Not tax advice and not a filed return. Integrate Green Invoice (Morning) API for Israeli invoicing, receipts, client management, and payment processing. Use when user asks to create invoices via Green Invoice, generate hashbonit mas through Morning API, manage clients in Green Invoice, set up webhook automation for document creation, query documents or expenses, or mentions "Green Invoice", "Morning", "hashbonit yeruka", "greeninvoice API", Israeli cloud invoicing, or needs to create tax invoice-receipt (cheshbonit mas/kabala). Covers all 15 document types, 8 payment types, client CRUD, item catalog, and webhook integration. Do NOT use for SHAAM allocation numbers or Tax Authority e-invoice compliance (use israeli-e-invoice), Cardcom payment processing (use cardcom-payment-gateway), or Tranzila integration (use tranzila-payment-gateway).
license: MIT
compatibility: Requires network access for Green Invoice API calls (api.greeninvoice.co.il). API access and webhooks require a Best plan or higher. API credentials obtained from the dashboard (Personal Area, Developer Tools, API Keys). Works with Claude Code, Claude.ai, Cursor.
---


# Green Invoice (Morning)

## Legal notice

This skill is a free information tool operated by an AI model. It explains the Green Invoice (Morning) API and issues documents through it in your own account, with a general explanation of the VAT rules for each document type. Its output is produced automatically, without the involvement, review or approval of an accountant, tax adviser or lawyer. It is not tax advice and not a professional opinion: it is general information and a technical tool for issuing documents. It does not check how the tax authorities classify your business, does not decide whether a transaction qualifies for the zero rate or an exemption, and does not verify your Tax Authority authorization or donation reporting. An AI model can make mistakes, omit data or reach a wrong conclusion. Every document issued through it is issued in your name and on your responsibility: reporting and paying the tax is your responsibility, the binding calculation is the Tax Authority's, and representation before the Tax Authority is reserved to those permitted by law. The tool is not a substitute for advice that takes into account each person's particular data and needs, and any use of its output is the user's sole responsibility.

## Instructions

### Step 1: Authentication and Plan Requirements

Green Invoice uses JWT Bearer token authentication. Obtain API credentials from the Green Invoice dashboard: Personal Area (אזור אישי) > Developer Tools (כלים למפתחים) > API Keys (מפתחות API).

**Plan gating (verified May 2026):**
- API access (any endpoint): requires the **Best** plan or higher (`זמין למנויי Best ומעלה`).
- Webhooks (Step 11): also **Best** or higher (`זמין במסלול Best ומעלה`); a 2023 article said Extra.

Lower-tier accounts will not see the "API Keys" or "Webhooks" menu items at all. If a user reports a missing menu item, check their plan first.

**Rebrand note.** The product is now "Morning של חשבונית ירוקה". The API and dashboard hosts (`api.greeninvoice.co.il`, `app.greeninvoice.co.il`) are unchanged and `api.morning.co.il` does not exist, but the OAuth token endpoint is on `api.morning.co`.

**Two authentication flows exist (re-probed 2026-10-18). Use OAuth 2.0 for new work; on sandbox it is now the only one.**

The published documentation at `developers.morning.co` (versioned "morning API Documentation (2.0.0)") now states: "Our APIs use the OAuth 2.0 protocol for authentication and authorization." The older API-key flow still answers on production, so existing integrations are not broken, but its sandbox route now returns 404 and it is no longer the documented path. Treat it as legacy.

| | OAuth 2.0 (documented, use this) | Legacy API-key flow |
|---|---|---|
| Token endpoint | `POST https://api.morning.co/idp/v1/oauth/token` | `POST https://api.greeninvoice.co.il/api/v1/account/token` |
| Sandbox token endpoint | `https://api.sandbox.morning.dev/idp/v1/oauth/token` | Removed: `sandbox.d.greeninvoice.co.il/api/v1/account/token` returns 404 (it answered on 2026-08-27) |
| Body | JSON: `grant_type` (`client_credentials`), `client_id`, `client_secret` | JSON: `id`, `secret` |
| Response | `accessToken` (signed JWT), `tokenType`, `expiresAt` (Unix seconds) | `token` (JWT) |
| Token lifetime | 1 hour | treat as short-lived; refresh on 401 |
| Errors | OAuth 2.0 / RFC 6749 format (`invalid_client`, `unauthorized_client`, ...) | Green Invoice error object (`errorCode` / `errorMessage`) |

Both return a bearer token used the same way against the same API base URL, so the only thing that changes is how you obtain it. If you are writing new code, use the OAuth endpoint; if you are maintaining an integration on `/account/token`, it still works today but plan the migration.

Two OAuth errors are account state, not bad credentials (`invalid_grant`, `unauthorized_client`); see Troubleshooting.

**Base URLs:**

| Environment | Base URL |
|-------------|----------|
| Production | `https://api.greeninvoice.co.il/api/v1` |
| Sandbox | `https://sandbox.d.greeninvoice.co.il/api/v1` |

**Get a token (OAuth 2.0, the documented path):**

```bash
curl -X POST https://api.morning.co/idp/v1/oauth/token \
  -H "Content-Type: application/json" \
  -d '{"grant_type": "client_credentials", "client_id": "YOUR_API_KEY_ID", "client_secret": "YOUR_API_KEY_SECRET"}'
```

The response carries `accessToken`, a signed JWT valid for 1 hour, and `expiresAt`. Refresh before that time.

**Get a token (legacy API-key flow, production only):**

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
| May 2024 (regime begins) | NIS 25,000 |
| Jan 1, 2025 | NIS 20,000 |
| Jan 1, 2026 | NIS 10,000 |
| Jun 1, 2026 onward (final step) | **NIS 5,000 (in force now)** |

No further step was officially announced as of October 2026; check the Tax Authority before assuming 5,000 still applies in 2027. Documents dated before May 2024 predate the regime and never needed a number. The threshold is date-dependent: when validating or migrating historical documents, test each against the threshold in force on ITS OWN date, not today's.

Two rules apply and conflating them is the classic error. The SELLER'S duty to obtain a number (s.47(a2)(1)) arises only when the buyer demands it, and does not apply to a zero-rated invoice. The BUYER'S loss of the deduction (s.38(a1)) has NO buyer-request condition: input VAT is disallowed on any qualifying invoice lacking a number, asked for or not.

**So when validating, do NOT treat "the buyer never asked" as a pass.** Flag every tax invoice to an osek murshe or company buyer that is above that date's threshold, carries VAT and has no allocation number; a B2C invoice or one to an osek patur needs none. Decide this from the buyer's VAT status, not from whether `taxId` is filled: a ת.ז. is not an osek number, and a business saved without its number cannot get one requested. The statute says `עולה על` (exceeds), so an invoice at exactly the threshold is outside it. The number is 9 digits (store it as a string), and a missing one blocks the recipient's deduction without voiding the invoice. Statute text in `references/api-reference.md`.

Above the threshold, a B2B tax invoice must carry a `מספר הקצאה` (allocation number) issued by שע"מ. Without it your customer cannot deduct the input VAT they paid you.

**Morning attaches the allocation number automatically, BUT ONLY AFTER a one-time authorization grant in the user's Morning account.** This is NOT automatic on signup. The user must:

1. In the Morning dashboard, navigate to: `אזור אישי > רשות המיסים > הוספת הרשאה` (Personal Area > Tax Authority > Add Authorization)
2. The dashboard redirects to the Tax Authority gov.il portal for identity verification
3. After authorization, the browser returns automatically to Morning, and the connection becomes active

Once active, Morning attaches the allocation number to the tax invoice through its own system, with no second platform to log into ("מספר ההקצאה מתנהל אוטומטית").

**Critical: the authorization expires every 3 months and must be renewed manually.** Morning's help centre states the connection is valid for 3 months with an in-system alert 10 days before expiry. Do not rely on an email; check the connection from your own runbook. If it lapses, qualifying invoices still succeed at HTTP level but ship WITHOUT an allocation number.

**What to do in code:**
1. Surface this requirement to the user before their first large B2B invoice. The create response (201) carries `taxAuthorityConfirmationInitiated` and `taxAuthorityConfirmationLastError` (`0` no error, non-zero such as `400`/`406` a failure); log both and alert on a non-zero error.
2. After creating a qualifying B2B invoice, fetch the resulting document with `GET /v1/documents/{id}` and check the PDF / response for an allocation number. If missing, the user's authorization is lapsed or was never set up.
3. The field is `allocationNumber`, documented in the Morning OpenAPI on `Document`, `UpdatedDocument`, `Expense` and `ExpenseRequest`. It is omitted when no number was assigned, so a qualifying invoice returning without it means the authorization lapsed. See `references/api-reference.md`.

For end-to-end SHAAM compliance use the `israeli-e-invoice` skill alongside this one.

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

**Key rule:** For Israeli clients who pay immediately, use type `320` (Tax Invoice-Receipt). When payment comes later, issue type `300` (Transaction Invoice) as the payment demand; an osek murshe then issues a `320` linked to it on payment, because a business buyer can deduct input VAT only from a tax invoice (s.38(a)) and any buyer may demand one (s.47(a)). When an osek murshe's sale qualifies for the zero rate, issue a tax invoice (type `305` or `320`) with each income row at `vatRate: 0`. A service to a foreign resident is generally zero-rated (0%) under VAT Law s.30(a)(5) when its conditions are met, which is NOT exempt, so keep the rows at `vatType: 0` with the rate set to zero; never set the document `vatType` to 1 or the row `vatType` to 2 (both mean exempt). Whether a sale qualifies is for whoever prepares the VAT return. Check totals in sandbox first. For an osek murshe, type `400` (Receipt) only records a payment against an issued invoice; for an osek patur it is the normal document on each payment.

### Step 4: Create Documents

**POST** `/v1/documents`

Required fields: `type`, `lang`, `currency`, `vatType`, `income`; each income row needs `description`, `quantity`, `price`, `currency`, `vatType`, and each payment row `date`, `type`, `price`, `currency`. `client` is optional but needed to email the PDF.

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
      "price": 5900,
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
| 0 | Default (VAT added based on business type) |
| 1 | Included (VAT is INCLUDED in the price you send) |
| 2 | Exempt (VAT-free) |

### Step 5: Payment Types

When adding payment records to a document, use these type codes:

| Code | Hebrew | English |
|------|--------|---------|
| 0 | ניכוי במקור | Withholding Tax |
| 1 | מזומן | Cash |
| 2 | המחאה | Check |
| 3 | כרטיס אשראי | Credit Card |
| 4 | העברה בנקאית | Bank Transfer |
| 5 | פייפאל | PayPal |
| 10 | אפליקציית תשלום | Payment App (Bit, PayBox) |
| 11 | אחר | Other |

Card types (`CreditCardType`) and deal types (`CreditCardDealType`, including 6 Recurring) are in `references/api-reference.md`.

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
  "labels": ["3777a6ef-0000-0000-0000-000000000000"]
}
```

**Payment terms:** `PaymentTerm` is -1 (מיידי) and 0/10/15/30/45/60/75/90/120 for שוטף +N. Full table in `references/api-reference.md`. These are שוטף+N, not end-of-month+N.

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
  "page": 1,
  "pageSize": 25
}
```

### Step 7: Search and Query Documents

**POST** `/v1/documents/search`

```json
{
  "page": 1,
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

**Download document PDF:** `GET /v1/documents/{id}/download/links` returns the Hebrew and original-language URLs, plus English only when an English copy exists.

### Step 8: Link Documents

Documents can be linked to create workflows. Use `linkedDocumentIds` when creating a new document.

Common linking patterns:

| Scenario | Steps |
|----------|-------|
| Invoice then payment | Create type 300, then on payment a 320 (osek murshe) or 400 (osek patur) with `linkedDocumentIds: ["invoice-id"]` |
| Credit note for invoice | Create type 330 (credit note) with `linkedDocumentIds: ["original-id"]` and `linkType: "cancel"` |
| Quote to order to invoice | Create type 10 (quote), then type 100 (order), then type 300 (invoice), linking each |

When a receipt is linked to an invoice with full payment, the invoice automatically closes.

### Step 9: Item Catalog

Reusable items: `POST /v1/items`, `GET`/`PUT`/`DELETE` `/v1/items/{id}`, `POST /v1/items/search`. Use `itemId` in income line items to reference catalog items instead of manually specifying description and price each time.

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

**Non-profits and `עוסק זעיר`.** A type 405 receipt can come back 201 while the donation is not reported to the Tax Authority's digital donations system (mandatory since 2026), so confirm with Morning that reporting is connected. `עוסק זעיר` is an income-tax status, not a business type here: ask whether the user is an osek patur or murshe. Details in `references/document-workflows.md`.

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

**Input VAT rules for the buyer side.** VAT Law s.38(a) allows the deduction only from a tax invoice (305/320; net of any 330 credit), an import declaration or another document the Director approved, within six months of its issue, so a supplier's ordinary 20 or 400 carries no deductible VAT. A supplier tax invoice above the threshold in force on its own date also needs its allocation number (Step 2). `ExpenseRequest` requires `documentType`, `number`, `date`, `reportingDate` (first of the month, which sets the VAT period), `supplier` and `accountingClassification`; the classification carries the recoverable-VAT and business-use percentages. A payment held to breach the Cash Law, where a sanction was imposed, also loses its input VAT unless the Director is satisfied the tax was paid (s.38(a2)), so flag large cash supplier payments for the accountant. Field table in `references/api-reference.md`; for recoverable-VAT % and the VAT return use `israeli-vat-reporting`.

### Step 11: Webhooks

**Tier requirement:** webhooks require the **Best** plan or higher (current help centre). Lower-tier accounts will not see the menu item.

Configure webhooks in the dashboard at: Personal Area (אזור אישי) > Developer Tools (כלים למפתחים) > Webhooks. The older "Settings > Developer Tools" path is no longer correct.

For `document/created` the payload is the document (`id`, `type`, `number`, `total`, `recipient`, `items`, `allocationNumber`, `files.downloadLinks` and more, with empty fields omitted rather than sent as `null`). The full example payload is in `references/api-reference.md`. This is one of ten event topics (`x-webhook-topic`); the full list, including the expense-draft events, is in `references/api-reference.md`.

### Step 12: Currencies and Exchange Rates

Green Invoice supports 27 document currencies. The spec says `currencyRate` defaults to 1, so on a foreign-currency document pass the rate explicitly (for example the Bank of Israel representative rate).

For multi-currency invoices, each income row can specify its own `currency` and `currencyRate`.

### Step 13: Sandbox Testing

Test in sandbox first. It needs its own account and API keys, the base URL `https://sandbox.d.greeninvoice.co.il/api/v1`, and a token from the sandbox OAuth endpoint (Step 1); the legacy token route is gone there. Verify totals, payment rows and linking before production.

## Examples

### Example 1: Create Tax Invoice-Receipt for Israeli Client

User says: "Create a hashbonit mas kabala for a client paying by bank transfer"

Actions:
1. Create the client if new (POST `/v1/clients`)
2. Create document type 320 (Tax Invoice-Receipt) with payment type 4 (bank transfer)
3. The document goes to `client.emails`; `attachment: true` attaches the PDF

Result: a signed 320 sent to the client.

### Example 2: Monthly Recurring Invoices

User says: "I need to send monthly invoices to 3 retainer clients"

Actions:
1. Search existing clients: POST `/v1/clients/search` with client names
2. For each client, create document type 300 (Transaction Invoice) with description "Monthly Retainer - March 2026"
3. Set `dueDate` to payment terms date, `lang` based on client preference
4. Documents are sent to each client's `emails`

Result: three invoices sent with the right terms and language.

### Example 3: Issue Credit Note for Partial Refund

User says: "Refund half the amount on invoice #12345"

Actions:
1. Get original document: GET `/v1/documents/{id}`
2. Calculate refund amount (half of original total)
3. Create document type 330 (Credit Note) with `linkedDocumentIds: ["original-id"]` and `linkType: "cancel"`
4. Put the refunded amount in the income row. The spec does not document whether a 330 row takes a positive or negative price, so confirm the sign on a sandbox credit note first

Result: Credit note issued, linked to original invoice, with partial refund amount.

### Example 4: Webhook Automation for Document Filing

User says: "Set up automatic filing when Green Invoice creates a document"

Actions:
1. Configure the webhook URL and a secret in the dashboard
2. Verify `x-webhook-signature`, then route on `type`
3. Download `files.downloadLinks.he` and file it by type and date

Result: All new documents automatically downloaded and organized by type and month.

## Bundled Resources

### Scripts
- `scripts/green-invoice-client.py` -- Python helper: authenticate (OAuth 2.0 by default, `--legacy` for production `/account/token`), create documents, search clients, and list documents (`--all-pages` for full-period reconciliation; HTTP 429 is retried with backoff). Run: `python3 scripts/green-invoice-client.py --help`

### References
- `references/api-reference.md` -- Complete Green Invoice API endpoint reference with request/response schemas, all enum codes, and payload examples. Consult when building API integrations or debugging request formats.
- `references/document-workflows.md` -- Common Israeli business document workflows: freelancer billing, retainer invoicing, refund flows, multi-currency billing, and e-commerce integration patterns. Consult when designing invoicing automation or choosing the correct document type sequence.

## Recommended MCP Servers

| MCP | What It Adds |
|-----|-------------|
| [BOI Exchange Rates](https://agentskills.co.il/he/mcp/boi-exchange) | Official Bank of Israel exchange rates to pass as `currencyRate` on foreign-currency documents (the API default is 1). |

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Morning API Documentation (canonical) | https://developers.morning.co | "morning API 2.0.0": enum meanings, field names, required fields, the OAuth flow. `greeninvoice.co.il/api-docs/` redirects here. |
| Apiary Interactive Reference (RETIRED) | https://greeninvoice.docs.apiary.io/ | HTTP 404 since 2026-07-27. Do not send agents here. |
| Green Invoice In-App API Explorer | https://app.greeninvoice.co.il/api | Interactive API explorer (requires sign-in). Authoritative for current request/response field names. |
| Tax Authority Connection Guide | https://www.greeninvoice.co.il/help-center/developers/tax-auth-connect/ | How to enable the gov.il authorization required for SHAAM allocation numbers (see Step 2) |
| Generating API Key Guide | https://www.greeninvoice.co.il/help-center/generating-api-key/ | Current dashboard menu path and plan-tier requirements for API access |
| Webhooks Setup | https://www.greeninvoice.co.il/help-center/creating-webhook/ | Current plan tier (Best and up) and configuration steps |
| Israel Tax Authority (VAT rates) | https://www.gov.il/he/departments/israel_tax_authority | Current VAT rate, business type rules |
| SHAAM E-Invoice System (Tax Authority) | https://www.gov.il/he/service/request-assignment-number-for-tax-invoice | Allocation number requirements for B2B invoices. Current threshold: NIS 5,000 net, in force since Jun 1, 2026 (final step of the rollout). |
| Bank of Israel Exchange Rates | https://www.boi.org.il/en/economic-roles/financial-markets/exchange-rates/ | Daily representative rates to pass as `currencyRate` |

## Gotchas

- After the Morning rebrand the API base is still `api.greeninvoice.co.il/api/v1`, but the OAuth token endpoint lives on `api.morning.co`. Only `api.morning.co.il` does not resolve, so never tell a user "the Morning API does not exist" (Step 1).
- The most common document type for Israeli clients paying immediately is type 320 (Tax Invoice-Receipt), not type 305 (Tax Invoice). Agents may default to 305 because it sounds like the standard invoice type.
- Osek Patur (exempt dealer) businesses cannot issue Tax Invoices (type 305). Agents may not check the business type before selecting a document type, causing API errors.
- VAT rate in Israel is 18% as of 2026, not 17%. The rate changed in January 2025 and agents trained on older data may use the outdated 17% figure in calculations.
- Payment type code 10 covers Israeli payment apps (Bit, PayBox), which are extremely common in Israel. Agents may not know these apps exist and default to bank transfer or credit card only. The app is named by `appType` (PaymentAppType): 1 Bit, 2 Pay, 3 PayBox, 5 Google Pay, 6 Apple Pay. There is no `subAppType` field, and code 2 is Pay, not Pepper Pay (which is not in the enum at all).
- **SHAAM allocation numbers need a one-time gov.il authorization in the user's Morning account (Step 2), renewed every 3 months.** It is the usual reason an integration "looks correct" while the customer's accountant rejects the invoices. Threshold NIS 5,000 net since Jun 1, 2026 (NIS 10,000 from Jan 1 to May 31, 2026), so code written earlier in 2026 skips the 5,000 to 10,000 band. Pair with `israeli-e-invoice`.
- **Plan tiers gate features.** API and webhooks need Best or higher; a missing "API Keys" or "Webhooks" menu item is the gate, not a bug.
- **Webhook signature verification.** When the webhook has a secret, every delivery carries `x-webhook-signature`: the HMAC-SHA256 of the RAW body, keyed with your secret, hex-encoded. Capture the raw bytes before JSON parsing and compare in constant time, since re-serializing changes the digest. With no secret there is no signature, and the safety net is a server-to-server `GET /v1/documents/{id}` before trusting any payload field. Full header list in `references/api-reference.md`.
- **The Apiary reference is gone (HTTP 404 since 2026-07-27); use `developers.morning.co`.** Older guidance still points at Apiary. When a field name is unclear, confirm it in the Morning docs or the signed-in explorer at `https://app.greeninvoice.co.il/api` rather than guessing.
- **Fiscal documents cannot be deleted, so preview first and never blind-retry.** `POST /documents/preview` renders a document without issuing it. There is no idempotency key: after a timed-out `POST /documents`, search for the document before retrying, or you issue a duplicate tax invoice that only a 330 can cancel.
- **Rate limits.** The ceiling is not published, so do not code against a specific requests-per-second number. Treat HTTP 429 as a soft, expected error: back off exponentially and retry rather than failing the job. For batch operations put the calls behind a queue with a concurrency limit you can tune down when you see 429s.

## Troubleshooting

### Error: "401 Unauthorized" on API calls
Cause: JWT token expired or invalid credentials
Solution: Tokens expire. An OAuth access token is valid for exactly 1 hour, so a long batch run WILL hit this mid-way and must re-authenticate rather than fail. Re-authenticate against whichever flow you use: `POST https://api.morning.co/idp/v1/oauth/token` with `grant_type: client_credentials` (the documented path), or, on production only, the legacy `POST /v1/account/token` with your API key ID and secret. A 404 from the legacy route on sandbox means it was removed there: switch to OAuth. On the OAuth endpoint, note that `invalid_grant` means the key is expired/revoked/pending and `unauthorized_client` means the subscription does not include API access; neither is fixed by retrying. Verify credentials in the Green Invoice dashboard under Personal Area (אזור אישי) > Developer Tools (כלים למפתחים) > API Keys. If the menu item is missing, the account is on a lower-tier plan; API access requires Best or higher.

### Error: "Document type not supported for your business type"
Cause: an osek patur cannot issue a tax invoice. s.47(a) of the VAT Law gives the right to issue one only to an osek murshe (`עוסק מורשה רשאי להוציא לגבי עסקה חייבת במס חשבונית מס`).
Solution: this rules out BOTH 305 (חשבונית מס) and 320 (חשבונית מס/קבלה), since 320 is a tax invoice with a receipt attached. An osek patur issues 300 (חשבון עסקה), 400 (קבלה) or 20 (חשבון / אישור תשלום). Routing an osek patur to 320 makes them issue a document that purports to charge VAT they are not registered to collect, and the recipient's input VAT is disallowed. Osek murshe and Ltd. companies can use all document types.

### Error: "VAT calculation mismatch"
Cause: Mixing vatType settings between document level and income row level
Solution: Set `vatType: 0` at document level to use defaults. Only override at the income row level when a line's VAT treatment differs from the document. To apply a specific rate to a line (e.g. 0% on a zero-rated export line), set the row's `vatRate` (decimal), not `vatType`.

### Issue: document not emailed to the client
Cause: sending is driven by `client.emails` (up to 5 addresses), not by `attachment`, which only attaches the PDF and defaults to `false`. Error 1009 (`יש לבחור כתובות מייל`) asks for email addresses.
Solution: Supply `client.emails` when the document should be sent, and set `attachment: true` if the PDF should ride along.

### Issue: B2B invoice over the threshold missing allocation number / customer's accountant rejected it
Cause: The Tax Authority authorization in the Morning dashboard was never set up, or it expired (3-month TTL). The API call succeeded (HTTP 201) but the resulting invoice has no `מספר הקצאה`. The recipient business cannot deduct input VAT without it.
Solution: Direct the user to `אזור אישי > רשות המיסים > הוספת הרשאה` in the Morning dashboard, complete the gov.il redirect, then request a number for the EXISTING invoice: s.47(a2)(4) allows a request after issue. Never issue a second invoice for the same sale unless the first is cancelled with a 330. If the Tax Authority refuses, s.47(a2)(3) gives a hearing within two business days and lets the buyer assume the tax or take the invoice without a number (then the buyer cannot deduct). If the Tax Authority's own systems failed, the Director may allow the deduction anyway (s.40B), so record the outage date rather than re-issuing. Check `taxAuthorityConfirmationLastError` on new documents, and re-check the 5,000 to 10,000 band if the integration predates June 2026. See Step 2.

### Issue: "API Keys" or "Webhooks" menu items missing in dashboard
Cause: The user's plan does not include this feature. API access and webhooks require Best or higher.
Solution: Check the plan in Personal Area > Account/Subscription. Upgrade is required to proceed - there is no workaround at the API level.
