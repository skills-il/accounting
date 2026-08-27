# Green Invoice API Reference

Complete reference for all Green Invoice (Morning) API endpoints, request/response schemas, and enum codes.

## Base URLs

| Environment | URL |
|-------------|-----|
| Production | `https://api.greeninvoice.co.il/api/v1` |
| Sandbox | `https://sandbox.d.greeninvoice.co.il/api/v1` |

## Authentication

Two flows are live (both verified 2026-07-27). OAuth 2.0 is the documented path for new
work; the API-key flow below still functions and is what existing integrations use.

### OAuth 2.0 (documented, use for new work)

**Token endpoint:**

| Environment | URL |
|-------------|-----|
| Production | `https://api.morning.co/idp/v1/oauth/token` |
| Sandbox | `https://api.sandbox.morning.dev/idp/v1/oauth/token` |

**Request:** form-encoded, `grant_type=client_credentials`, plus `client_id` and
`client_secret` (your API key ID and secret).

**Response:** `accessToken`, a signed JWT valid for **1 hour**. Use it as
`Authorization: Bearer <accessToken>`. After an hour, protected endpoints return 401 and a
new token must be requested, so any long-running job needs a refresh path.

**Errors** follow the OAuth 2.0 / RFC 6749 format. Two are business state, not credentials:

| Status | Error | Meaning |
|--------|-------|---------|
| 400 | `invalid_request` | Missing `grant_type` |
| 400 | `unsupported_grant_type` | `grant_type` is not `client_credentials` |
| 400 | `invalid_grant` | API key privilege expired, revoked, or pending |
| 400 | `unauthorized_client` | No active subscription, or subscription lacks API access |
| 401 | `invalid_client` | Missing or incorrect client credentials |

### POST /v1/account/token (legacy, still functional)

**Request:**
```json
{
  "id": "api_key_id",
  "secret": "api_key_secret"
}
```

**Response:**
Returns JWT token in `X-Authorization-Bearer` header and in response body `token` field.

Use in all subsequent requests: `Authorization: Bearer <token>`

**Plan tier:** API access requires the Best plan or higher. The token endpoint exists and accepts the call on lower-tier accounts, but issued tokens will fail authorization on most endpoints. Verify the plan in the Morning dashboard before debugging 401/403 cascades.

---

## Tax Authority (SHAAM) Authorization

Required for B2B tax invoices over the SHAAM allocation-number threshold. The API does NOT currently expose endpoints to manage this authorization - it is a human-in-the-loop dashboard action.

**Setup (one-time, must be performed in the dashboard):**
1. Sign in to https://app.greeninvoice.co.il/
2. Navigate to: `אזור אישי > רשות המיסים > הוספת הרשאה` (Personal Area > Tax Authority > Add Authorization)
3. The dashboard redirects to the gov.il Tax Authority portal for verification
4. After successful verification, the browser returns to Morning automatically and the connection becomes active

**Expiration:** the authorization is valid for 3 months and must be renewed. Morning's help centre states that an alert appears in the system 10 days before the connection expires ("10 ימים לפני תום התוקף תופיע התראה במערכת לחידוש החיבור"). Renewal requires repeating steps 1-4.

**Threshold schedule (net amounts, before VAT):**

| Effective from | Threshold |
|----------------|-----------|
| May 2024 (regime begins) | NIS 25,000 (superseded) |
| Jan 1, 2025 | NIS 20,000 (superseded) |
| Jan 1, 2026 | NIS 10,000 (superseded) |
| Jun 1, 2026 onward (final step) | **NIS 5,000 (in force now, as of 2026-08-27)** |

Documents dated before May 2024 predate the regime. Scope any historical validation to each document's own date.

**The two allocation-number rules (statute text).**

*Seller's duty*, s.47(a2)(1) of חוק מס ערך מוסף: an osek murshe issuing a tax invoice above the s.38(a1) amount `חייב הוא לעשות כן לפי דרישת הקונה`, and the subsection applies only `לעניין חשבונית מס שהוצאה בשל עסקה שהמס שחל לגביה אינו בשיעור אפס` (so a zero-rated invoice is out of scope).

*Buyer's loss of the deduction*, s.38(a1): `לא יותר ניכוי מס התשומות הכלול בחשבונית מס שסכומה, בלא המס, עולה על 5,000 שקלים חדשים (מינואר 2026 ועד מאי 2026: 10,000 שקלים חדשים) ושאינה כוללת מספר שהקצה לה המנהל`. There is no buyer-request condition here, so a validator must flag a qualifying invoice with no number even when nobody asked for one. Note `עולה על`: an invoice at exactly the threshold is outside the rule.

**API field for the allocation number:** `allocationNumber`, documented in the Morning OpenAPI on `Document`, `UpdatedDocument`, `Expense` and `ExpenseRequest` as "Allocation Number issued by the Israeli Tax Authority". It is omitted when no number was assigned, so a qualifying B2B invoice coming back WITHOUT `allocationNumber` means the user's Tax Authority authorization has lapsed or was never set up. Note the two documented example shapes differ in length (`166056573` on the expense schemas, a much longer value on `Document`), so read it as an opaque string rather than validating it to 9 characters.

Reference: https://www.greeninvoice.co.il/magazine/israel-invoice/ and https://www.greeninvoice.co.il/help-center/developers/tax-auth-connect/

---

## Documents API

### POST /v1/documents (Create Document)

**Full Request Schema:**
```json
{
  "description": "string",
  "remarks": "string",
  "footer": "string",
  "emailContent": "string",
  "type": 320,
  "date": "YYYY-MM-DD",
  "dueDate": "YYYY-MM-DD",
  "lang": "he|en",
  "currency": "ILS",
  "vatType": 0,
  "discount": {
    "amount": 10,
    "type": "sum|percentage"
  },
  "rounding": true,
  "signed": true,
  "attachment": true,
  "maxPayments": 1,
  "client": {
    "id": "string (optional, use for existing client)",
    "name": "string (required for new)",
    "emails": ["string"],
    "taxId": "string",
    "department": "string",
    "address": "string",
    "city": "string",
    "zip": "string",
    "country": "IL",
    "phone": "string",
    "mobile": "string",
    "contactPerson": "string",
    "accountingKey": "string",
    "paymentTerms": -1,
    "labels": ["string"],
    "add": true,
    "self": false
  },
  "income": [
    {
      "catalogNum": "SKU-001",
      "description": "string (required)",
      "quantity": 1,
      "price": 100.00,
      "currency": "ILS",
      "currencyRate": 1.0,
      "vatRate": 0.18,
      "vatType": 0,
      "itemId": "string (optional, reference to catalog)"
    }
  ],
  "payment": [
    {
      "type": 3,
      "subType": 0,
      "date": "YYYY-MM-DD",
      "price": 100.00,
      "currency": "ILS",
      "currencyRate": 1.0,
      "quantity": 1,
      "bankName": "string",
      "bankBranch": "string",
      "bankAccount": "string",
      "chequeNum": "string",
      "cardType": 2,
      "cardNum": "string",
      "dealType": 1,
      "numPayments": 1,
      "firstPayment": 100.00,
      "appType": 0
    }
  ],
  "linkedDocumentIds": ["string"],
  "linkedPaymentId": "string",
  "linkType": "link|cancel",
  "paymentRequestData": {
    "maxPayments": 12,
    "plugins": [
      {
        "id": "plugin-uuid",
        "group": 100,
        "type": 12100
      }
    ]
  }
}
```

### GET /v1/documents/{id}

Returns full document object.

### POST /v1/documents/search

**Request:**
```json
{
  "page": 1,
  "pageSize": 25,
  "number": 12345,
  "type": [320, 305, 300],
  "status": [0, 1],
  "paymentTypes": [3, 4],
  "fromDate": "YYYY-MM-DD",
  "toDate": "YYYY-MM-DD",
  "clientId": "string",
  "clientName": "string",
  "description": "string",
  "download": false,
  "sort": "documentDate|creationDate"
}
```

### POST /v1/documents/{id}/close

Closes an open document.

### GET /v1/documents/{id}/download/links

**Response:**
```json
{
  "he": "https://www.greeninvoice.co.il/api/v1/documents/download?d=...",
  "en": "https://www.greeninvoice.co.il/api/v1/documents/download?d=...",
  "origin": "https://www.greeninvoice.co.il/api/v1/documents/download?d=..."
}
```

---

## Clients API

### POST /v1/clients (Create)

```json
{
  "name": "string (required)",
  "emails": ["string (required)"],
  "active": true,
  "department": "string",
  "taxId": "string",
  "accountingKey": "string",
  "paymentTerms": 30,
  "bankName": "string",
  "bankBranch": "string",
  "bankAccount": "string",
  "address": "string",
  "city": "string",
  "zip": "string",
  "country": "IL",
  "category": 0,
  "subCategory": 0,
  "phone": "string",
  "fax": "string",
  "mobile": "string",
  "remarks": "string",
  "contactPerson": "string",
  "labels": ["string"]
}
```

### GET /v1/clients/{id}

### PUT /v1/clients/{id}

### DELETE /v1/clients/{id}

### POST /v1/clients/search

```json
{
  "name": "string",
  "active": true,
  "email": "string",
  "contactPerson": "string",
  "labels": ["string"],
  "taxId": "string",
  "page": 1,
  "pageSize": 25
}
```

### POST /v1/clients/{id}/assoc

Associates documents to a client.

---

## Items API

### POST /v1/items (Create)
### GET /v1/items/{id}
### PUT /v1/items/{id}
### POST /v1/items/search

---

## Businesses API

### GET /v1/businesses
### GET /v1/businesses/search

Note: this path and `/v1/businesses` are absent from the Morning OpenAPI. Probed live 2026-08-27: GET returns 401 (route exists, auth required) while POST returns 405 Method Not Allowed, and an invented sibling on the same host returns 404, so GET is the method and these are undocumented-upstream routes. Treat them as unsupported.

---

## Credential Smoke Test

### GET /v1/documents/info

Returns the issuing defaults for the authenticated business (next document numbers,
the VAT rate that will apply, and the business type). It requires a valid bearer
token, so it is the cheapest way to prove that authentication actually worked:
an unauthenticated call returns `401` with
`{"errorCode":401,"errorMessage":"גישה נדחתה, נא להתחבר מחדש"}`.

There is no `GET /v1/users/me` endpoint. It appears in no version of the Morning
API documentation and the host answers it with the same `{"errorCode":404}` body
it returns for a path that was never defined, so do not use it as a health check.

---

## Enum Reference

### Document Types

| Code | Name (he) | Name (en) |
|------|-----------|-----------|
| 10 | הצעת מחיר | Price Quote |
| 20 | חשבון / אישור תשלום | Account / Payment Confirmation |
| 100 | הזמנה | Order |
| 200 | תעודת משלוח | Delivery Note |
| 210 | תעודת החזרה | Return Note |
| 300 | חשבון עסקה | Transaction Invoice |
| 305 | חשבונית מס | Tax Invoice |
| 320 | חשבונית מס / קבלה | Tax Invoice-Receipt |
| 330 | חשבונית זיכוי | Credit Note |
| 400 | קבלה | Receipt |
| 405 | קבלה על תרומה | Donation Receipt |
| 410 | ביטול תרומה | Donation Cancellation |
| 500 | הזמנת רכש | Purchase Order |
| 600 | קבלת פיקדון | Deposit Receipt |
| 610 | משיכת פיקדון | Deposit Withdrawal |

### Document Statuses

| Code | Meaning |
|------|---------|
| 0 | Open |
| 1 | Closed |
| 2 | Manually Closed |
| 3 | Canceling Other Document |
| 4 | Canceled |

### Payment Types

| Code | Name (he) | Name (en) |
|------|-----------|-----------|
| 0 | ניכוי במקור | Withholding Tax |
| 1 | מזומן | Cash |
| 2 | המחאה | Check |
| 3 | כרטיס אשראי | Credit Card |
| 4 | העברה בנקאית | Bank Transfer |
| 5 | פייפאל | PayPal |
| 10 | אפליקציית תשלום | Payment App |
| 11 | אחר | Other |

### Payment Sub-Types (OtherSubType, required when payment type is 'other')

| Code | Name |
|------|------|
| 1 | Bitcoin (ביטקוין) |
| 2 | Money Equivalent (שווה כסף) |
| 3 | V-Check |
| 4 | Gift voucher (שובר מתנה) |
| 5 | Employee National Insurance deduction (ניכוי חלק עובד ביטוח לאומי) |
| 6 | Ethereum (אתריום) |
| 7 | BUYME voucher |
| 9 | Other deduction (ניכוי אחר) |

### Payment App Types

| Code | Name | Status |
|------|------|--------|
| 1 | Bit | Active (Bank Hapoalim) |
| 2 | Pay | |
| 5 | Google Pay | |
| 6 | Apple Pay | |
| 3 | PayBox | Active (Discount Bank) |

### Credit Card Types

| Code | Name |
|------|------|
| 0 | Unknown |
| 1 | Isracard |
| 2 | Visa |
| 3 | Mastercard |
| 4 | American Express |
| 5 | Diners |

### Credit Card Deal Types

| Code | Name (he) | Name (en) |
|------|-----------|-----------|
| 1 | רגיל | Regular |
| 2 | תשלומים | Installments |
| 3 | קרדיט | Credit |
| 4 | חיוב נדחה | Deferred |
| 5 | אחר | Other |
| 6 | הוראת קבע | Recurring |

### Payment Plugin Types

| Code | Name |
|------|------|
| 12010 | PayPal |
| 12100 | Cardcom |
| 12120 | Max (Leumi Card) |
| 12130 | Digital Payments (Grow) תשלומים דיגיטליים (גרו) |
| 12200 | Digital Payments (Morning) |

### VAT Types (Document Level)

| Code | Meaning |
|------|---------|
| 0 | Default (based on business type) |
| 1 | Exempt |
| 2 | Mixed |

### VAT Types (Income Row)

The income-row `vatType` is a DIFFERENT enum from the document-level one. The
document uses `DocumentVatType`; an income row uses `ItemVatType`, where `1`
means "VAT included in price" and `2` means exempt. The two enums collide on the
value `1`, so copying a document-level `vatType: 1` onto a row does not make the
row exempt, it makes the row VAT-inclusive and changes the amount charged.

| Code | Meaning |
|------|---------|
| 0 | Default (VAT added based on business type) |
| 1 | Included (VAT included in price) |
| 2 | Exempt (VAT-free) |

Set a specific rate on a line with the separate `vatRate` field (decimal: `0` for
0%, `0.18` for 18%).

### Business Types

| Code | Name (he) | Name (en) |
|------|-----------|-----------|
| 1 | עוסק מורשה | Licensed Dealer |
| 2 | חברה בע"מ | Ltd. Company |
| 3 | עוסק פטור | Exempt Dealer |
| 4 | עמותה | Non-Profit |
| 5 | חברה לתועלת הציבור | Public Benefit Company |
| 6 | שותפות | Partnership |

### Payment Terms

| Code | Meaning |
|------|---------|
| -1 | מיידי (immediate) |
| 0 | שוטף |
| 10 | שוטף +10 |
| 15 | שוטף +15 |
| 30 | שוטף +30 |
| 45 | שוטף +45 |
| 60 | שוטף +60 |
| 75 | שוטף +75 |
| 90 | שוטף +90 |
| 120 | שוטף +120 |

These are the spec's own labels. Note they are שוטף+N, not "end of month + N": שוטף+30 runs from the invoice's payment period, which is a different due date from end-of-month-plus-30.

### Supported Currencies

ILS, USD, EUR, GBP, JPY, CHF, CNY, AUD, CAD, RUB, BRL, HKD, SGD, THB, MXN, TRY, NZD, SEK, NOK, DKK, KRW, INR, IDR, PLN, RON, ZAR, HRK

### Business Categories

| Code | Category |
|------|----------|
| 0 | Other |
| 1 | Internet and Computers |
| 2 | Accounting |
| 3 | Engineering |
| 4 | Marketing |
| 5 | Leisure and Sports |
| 6 | Health and Mind |
| 7 | Agriculture |
| 8 | Art |
| 9 | Education |
| 10 | Communication and Journalism |
| 11 | Religion |
| 12 | Law |
| 13 | Architecture and Design |
| 14 | Finance |
| 15 | Television and Stage |
| 16 | Coaching and Consulting |
| 17 | Hosting and Catering |
| 18 | Delivery |
| 19 | Real Estate |
| 21 | Administration and Logistics |

---

## Webhook Payload

Full webhook payload structure on document creation:

```json
{
  "id": "uuid",
  "type": 300,
  "number": 98765,
  "businessId": "uuid",
  "businessType": 1,
  "currency": "ILS",
  "country": "IL",
  "date": "2026-03-05",
  "createdAt": 1748284806000,
  "subtotal": 1000,
  "taxableTotal": 0,
  "vatTaxableTotal": 0,
  "revenueTaxableTotal": 1000,
  "exemptTotal": 0,
  "rounding": false,
  "bill": {
    "url": "https://pages.greeninvoice.co.il/en/payments/bills/..."
  },
  "tax": [{"name": "VAT", "rate": 0.18, "total": 180}],
  "total": 1180,
  "description": "",
  "remarks": "",
  "reverseCharge": false,
  "recipient": {
    "id": "uuid",
    "name": "Client Name",
    "department": "",
    "address": "",
    "city": "",
    "zip": "",
    "country": "IL",
    "phone": "",
    "mobile": "",
    "emails": ["client@example.com"]
  },
  "items": [
    {
      "description": "Service",
      "sku": "SKU-001",
      "quantity": 1,
      "price": 1000,
      "currency": "ILS",
      "taxIncludedInPrice": false,
      "tax": [{"name": "VAT", "rate": 0.18}]
    }
  ],
  "transactions": [],
  "files": {
    "signed": true,
    "downloadLinks": {
      "he": "https://www.greeninvoice.co.il/api/v1/documents/download?d=...",
      "en": "https://www.greeninvoice.co.il/api/v1/documents/download?d=...",
      "origin": "https://www.greeninvoice.co.il/api/v1/documents/download?d=..."
    }
  }
}
```

## SDKs and Libraries

| Language | Package | Install |
|----------|---------|---------|
| Python | green-invoice | `pip install green-invoice` |
| PHP | greeninvoice/greeninvoice | `composer require greeninvoice/greeninvoice` (repo: github.com/MordiSacks/greeninvoice) |
| PHP | bariew/greeninvoice | `composer require bariew/greeninvoice` |

## Official Documentation

- API Docs (Hebrew): https://www.greeninvoice.co.il/api-docs/
- In-app API Explorer (requires sign-in, authoritative for current field names): https://app.greeninvoice.co.il/api
- Tax Authority connection guide (required for SHAAM allocation numbers): https://www.greeninvoice.co.il/help-center/developers/tax-auth-connect/
- API key generation + plan-tier requirements: https://www.greeninvoice.co.il/help-center/generating-api-key/
- Webhooks overview (Extra plan required): https://www.greeninvoice.co.il/magazine/webhooks/

Note: the `greeninvoice.docs.apiary.io` Apiary interactive reference has been RETIRED. As of 2026-07-27 it returns HTTP 404 ("Apiary - Page not found"), verified in a browser; it was still live on 2026-06-28. The canonical reference is now `https://developers.morning.co` ("morning API Documentation (2.0.0)"), which is also where the current OAuth 2.0 authentication flow is documented.

## Suppliers and Expenses (purchase side)

The purchase side is where input VAT is reclaimed, and these endpoints sit outside the
document flow so they are easy to miss.

### POST /v1/suppliers

Creates a supplier (a business or individual you buy from) for the current business.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `name` | string | Yes | Supplier name, e.g. ישראל ישראלי |
| `active` | boolean | No | Defaults to true |
| `department` | string | No | |

### POST /v1/expenses

Creates an expense. **The file-attachment behaviour is the trap:** an expense created
WITHOUT a file is created immediately and is ready to use, while an expense created WITH a
file (a receipt or supplier invoice) first becomes an expense DRAFT. A draft is a pending
expense awaiting approval and is NOT counted as an actual expense until approved. Bulk
importers that upload scanned supplier invoices and never approve the drafts will under-report
expenses and under-claim input VAT.

Headers for both: `Content-Type: application/json`, `Authorization: Bearer <accessToken>`.
