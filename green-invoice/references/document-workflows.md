# Green Invoice Document Workflows

Common Israeli business document workflows using the Green Invoice (Morning) API.

## Workflow 1: Freelancer Monthly Billing

A freelancer (osek murshe or osek patur) billing clients monthly.

**Flow:**
1. Search for client: `POST /v1/clients/search` with client name
2. Create Tax Invoice-Receipt (type 320) with monthly service description
3. Include payment record matching how the client paid

**Osek Murshe (Licensed Dealer):**
- Use type 320 with `vatType: 0` (VAT automatically added at 18%)
- Total = subtotal + VAT
- Example: NIS 10,000 service = NIS 11,800 total

**Osek Patur (Exempt Dealer):**
- Use type 300 (חשבון עסקה), 400 (קבלה) or 20 (חשבון / אישור תשלום) with `vatType: 0` (no VAT added)
- Total = subtotal (no VAT)
- Cannot issue a tax invoice at all. s.47(a) of the VAT Law reserves that to an osek murshe, so BOTH 305 (חשבונית מס) and 320 (חשבונית מס/קבלה) are out, 320 being a tax invoice with a receipt attached
- Annual revenue limit: NIS 122,833 (as of 2026; the ceiling is CPI-adjusted annually)

**Best Practice:** Use labels on clients (e.g., "monthly", "retainer") to easily search and batch-process recurring invoices.

---

## Workflow 2: Quote to Invoice to Receipt

A full sales cycle from price quote to final receipt.

**Step 1 - Price Quote:**
```
POST /v1/documents
type: 10 (Price Quote)
```
Send to client for approval. Quote has no tax implications.

**Step 2 - Order Confirmation:**
```
POST /v1/documents
type: 100 (Order)
linkedDocumentIds: ["quote-id"]
```
Links back to the original quote.

**Step 3 - Invoice:**
```
POST /v1/documents
type: 300 (Transaction Invoice)
linkedDocumentIds: ["order-id"]
```
Client has not paid yet. Invoice is open.

**Step 4 - On payment:**
```
POST /v1/documents
type: 320 (Tax Invoice-Receipt) for an osek murshe, 400 (Receipt) for an osek patur
linkedDocumentIds: ["invoice-id"]
payment: [{ type: 4, date: "YYYY-MM-DD", price: full_amount, currency: "ILS" }]
```
When payment is received. A 300 is only a payment demand: a business buyer can deduct input
VAT only from a tax invoice (VAT Law s.38(a)) and may demand one (s.47(a)), so an osek murshe
closes the 300 with a linked 320 (or a 305 plus a 400). Linking with full payment closes the
300.

**Shortcut:** For immediate payment, skip steps 1-3 and issue type 320 (Tax Invoice-Receipt) directly.

---

## Workflow 3: Credit Note (Refund)

Issuing a refund or correction for an existing invoice.

**Full Refund:**
```
POST /v1/documents
type: 330 (Credit Note)
linkedDocumentIds: ["original-invoice-id"]
linkType: "cancel"
income: [{ same items as original, same amounts }]
```

**Partial Refund:**
```
POST /v1/documents
type: 330 (Credit Note)
linkedDocumentIds: ["original-invoice-id"]
linkType: "cancel"
income: [{ description: "Partial refund", price: refund_amount }]
```

**Important:** Credit notes must reference the original document. The `linkType: "cancel"` marks the relationship as a cancellation. For partial refunds, only include the refunded amount in the income lines. The spec does not document whether a 330 income row takes a positive or negative price, so confirm the sign on a sandbox credit note before production.

---

## Workflow 4: Multi-Currency International Billing

Billing international clients in foreign currencies.

**Create Document** (zero-rated export tax invoice-receipt, paid immediately):
```json
{
  "type": 320,
  "currency": "USD",
  "lang": "en",
  "vatType": 0,
  "client": {
    "name": "International Corp",
    "country": "US",
    "emails": ["billing@intl.com"]
  },
  "income": [
    {
      "description": "Consulting Services",
      "quantity": 10,
      "price": 150,
      "currency": "USD",
      "currencyRate": 3.7,
      "vatType": 0,
      "vatRate": 0
    }
  ],
  "payment": [
    {
      "type": 5,
      "date": "2026-03-05",
      "price": 1500,
      "currency": "USD",
      "currencyRate": 3.7
    }
  ]
}
```

**Key Points:**
- For an export SALE, issue a tax invoice (type 305 or 320), not a bare Receipt. Use type 400 (Receipt) only to record a payment against an already-issued invoice.
- Set document `lang: "en"` for English
- Set `currency` to the client's currency (USD, EUR, GBP, etc.)
- The spec says `currencyRate` defaults to 1, so pass the rate explicitly (for example the Bank of Israel representative rate); the 3.7 above is illustrative only
- A service to a foreign resident is generally zero-rated (0%) under VAT Law s.30(a)(5) when its conditions are met, NOT exempt. The section excludes, among others, a service also given in practice to an Israeli resident in Israel, so whether a sale qualifies is a classification for whoever prepares the VAT return, not something to infer from the client's country alone. Keep rows at `vatType: 0` and set `vatRate: 0` per income row. Do NOT set the document `vatType` to 1 or the row `vatType` to 2 (both mean exempt): exemption (פטור) is legally distinct from zero-rating and blocks input-VAT recovery, and they are reported in different boxes of the VAT return.

---

## Workflow 5: E-Commerce Order Processing

Automating invoice generation for online store orders.

**On Order Completion:**
1. Create or find client by email: `POST /v1/clients/search`
2. If new client, create with `add: true` in the document's client object
3. Create Tax Invoice-Receipt (type 320) with order items
4. Payment type depends on payment method used:
   - Credit card: type 3, with cardType and dealType
   - Bit: type 10, appType: 1
   - PayPal: type 5

**Batch Processing:**
For high-volume stores, queue orders and create documents in batches. Green Invoice API has rate limits, so space requests appropriately.

**Webhook Integration:**
Set up a webhook to receive document creation confirmations. Use the `files.downloadLinks` from the webhook payload to archive PDFs.

---

## Workflow 6: Retainer Client with Monthly Advance Invoices

Sending invoices at the start of each month for ongoing services.

**Monthly Flow:**
1. Create Transaction Invoice (type 300) at month start
2. Set `dueDate` based on client's payment terms
3. When payment is received, create a 320 (osek murshe) or 400 (osek patur) linked to the invoice
4. The linked document closes the invoice

**With Deposit:**
1. Receive deposit: Create Deposit Receipt (type 600)
2. Monthly invoicing: Create Transaction Invoice (type 300)
3. Apply deposit: Create Deposit Withdrawal (type 610) linked to invoice
4. Collect remaining balance: a 320 (osek murshe) or 400 (osek patur) for the difference

---

## Workflow 7: Withholding Tax (Nikui Bamkor)

When clients withhold tax at source before paying.

**Example (osek murshe):** A NIS 10,000 service is NIS 11,800 with 18% VAT. The client withholds NIS 2,000 (the rate and base come from the client's withholding certificate, אישור ניכוי מס במקור, often computed on the net base) and pays NIS 9,800 by bank transfer. The payment lines MUST sum to the document total (11,800): 9,800 received + 2,000 withheld.

```json
{
  "type": 320,
  "lang": "he",
  "currency": "ILS",
  "vatType": 0,
  "income": [
    { "description": "Service", "quantity": 1, "price": 10000, "currency": "ILS", "vatType": 0 }
  ],
  "payment": [
    { "type": 4, "date": "2026-03-05", "price": 9800, "currency": "ILS" },
    { "type": 0, "date": "2026-03-05", "price": 2000, "currency": "ILS" }
  ]
}
```

Payment type 0 (Withholding Tax) records the amount withheld. The document total is NIS 11,800 (10,000 net + 18% VAT), and the two payment lines must sum to exactly that: NIS 9,800 actually received by bank transfer plus NIS 2,000 withheld and remitted to the Tax Authority by the client. If the payment lines do not match the document total the API may reject it (error 2422, mismatch between receipts and payments) or leave a balance open; verify in sandbox. A withholding row cannot stand alone (error 2428 asks for at least one other receipt row), and the bundled script writes a single payment row, so build withholding documents as raw JSON.

---

## Workflow 8: Donation Receipts for Non-Profits

For amutot (non-profits) issuing donation receipts under Section 46.

**Create Donation Receipt:**
```json
{
  "type": 405,
  "lang": "he",
  "currency": "ILS",
  "vatType": 1,
  "client": {
    "name": "Donor Name",
    "taxId": "donor-tz",
    "emails": ["donor@example.com"]
  },
  "income": [
    { "description": "Donation", "quantity": 1, "price": 5000, "currency": "ILS", "vatType": 2 }
  ],
  "payment": [
    { "type": 4, "date": "2026-03-05", "price": 5000, "currency": "ILS" }
  ]
}
```

**Key Points:**
- Type 405 (Donation Receipt) is not gated to one business type in the spec. What matters is the Section 46 approval, which turns on being a מוסד ציבורי under s.9(2) of the Income Tax Ordinance, defined as a חבר בני אדם, so a חברה לתועלת הציבור (business type 5) is not excluded
- Set `vatType: 1` (exempt) as donations are not subject to VAT
- Include donor's `taxId` (Teudat Zehut) for Section 46 credit eligibility
- The receipt lets the donor claim a Section 46 זיכוי (a CREDIT against tax, not a deduction from income) at 35% of the donation for an individual, and at the s.126(a) rate for a company. There is an annual floor and a ceiling, and unused credit carries forward, so state the mechanism and route the donor to their accountant for the current figures

---

## Business-Type Notes

**Non-profits: donation receipts carry a 2026 reporting obligation.** Since 1 January
2026 an amuta holding Section 46 authorization must report credit-granting donations to the
Tax Authority's digital donations system, and the reporting is meant to happen automatically
from receipt-issuing software that is connected to it (organisations on unconnected software
or paper receipts file through a dedicated Tax Authority application instead). This is the
same shape of trap as the SHAAM allocation number in Step 2 of SKILL.md: issuing a type 405 receipt
through the API can return HTTP 201 while the donation is not reported, and the donor's
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

---

## Common Patterns

### Auto-Save Client on Document Creation
Set `client.add: true` in the document creation payload. This automatically adds a new client to your client list when creating a document, avoiding a separate API call.

### Close Document Without Payment
Use `POST /v1/documents/{id}/close` to manually mark a document as closed without creating a linked receipt. Use for write-offs or adjustments.

### Currency Rate Override
When you have a specific exchange rate (e.g., from the contract), set `currencyRate` explicitly. The rate is always relative to ILS, and the spec default is 1, so never omit it on a foreign-currency document.

### Document Language Per Client
Set `lang` based on client preference. Israeli clients typically get "he", international clients get "en". The Hebrew and original links are always returned; the English link only when an English copy exists.
