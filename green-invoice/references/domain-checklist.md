# Domain checklist: `green-invoice` (accounting)

Canonical coverage list for an agent skill that integrates the Green Invoice / Morning
(חשבונית ירוקה / מורנינג) REST API on behalf of an Israeli business. Compiled 2026-10-18 from the
Morning OpenAPI 2.0.0 bundle, the VAT Law text on he.wikisource,
the Income Tax Ordinance text, and the existing skill's `evidence.json` (source check
clean on 2026-10-18).

Abbreviations: OAS = Morning OpenAPI bundle (https://developers.morning.co/docs/openapi.bundled.json);
VATL = חוק מס ערך מוסף, התשל"ו-1975; ITO = פקודת מס הכנסה.

## Must cover (core)

### A. Environments and authentication

| # | Item | What the skill must state | Authority |
|---|------|---------------------------|-----------|
| A1 | Two environments, separate keys | Production and sandbox each need their own API key pair; build in sandbox first. | OAS `info.description` ("Each environment requires its own set of API keys") |
| A2 | Resource base URLs | Production `https://api.greeninvoice.co.il/api/v1`; sandbox `https://sandbox.d.greeninvoice.co.il/api/v1`. | OAS root `servers` |
| A3 | OAuth 2.0 token URL, production | `POST https://api.morning.co/idp/v1/oauth/token` (different host from the resource API). | OAS `/idp/v1/oauth/token` operation `servers` |
| A4 | OAuth 2.0 token URL, sandbox | `POST https://api.sandbox.morning.dev/idp/v1/oauth/token`. | OAS same operation `servers` |
| A5 | Token request shape | JSON body, `grant_type: client_credentials`, `client_id`, `client_secret`. | OAS `obtainAccessToken` code samples and request schema |
| A6 | Token response and TTL | `accessToken` (signed JWT), `tokenType`, `expiresAt` (Unix seconds); valid 1 hour; expiry yields 401 on protected endpoints, so cache and refresh before `expiresAt`. | OAS `obtainAccessToken` description |
| A7 | Token is business-scoped | One token acts for the single business tied to the keys; multi-business needs the partner flow (B-section, Should). | OAS `obtainAccessToken` notes |
| A8 | Token-endpoint error map (RFC 6749 format) | `invalid_request`, `unsupported_grant_type`, `invalid_client`, `invalid_grant` (key expired, revoked or pending), `unauthorized_client` (no active subscription, or plan lacks API access). The last two are account-state problems, not code bugs. | OAS `obtainAccessToken` error table |
| A9 | Bearer usage | `Authorization: Bearer <accessToken>` plus `Content-Type: application/json` on every call. | OAS `/documents` POST request-headers table |
| A10 | Legacy API-key flow (`POST /api/v1/account/token` with `{id, secret}`) | Still answers on production (401 on bad credentials, 405 on GET) but is removed on sandbox (404). Document it only as a migration path to OAuth, never as the default. | Live probes recorded in `evidence.json` (`legacy-account-token-still-live-2026-07`, `legacy-sandbox-base-host`); absent from OAS 2.0.0 |
| A11 | Retired reference | `greeninvoice.docs.apiary.io` no longer serves the reference; the canonical spec is developers.morning.co. Prevents the agent from citing stale Apiary field names. | `evidence.json` `apiary-reference-retired-2026-07` |
| A12 | Credential smoke test | `GET /documents/info` (needs bearer, 401 Hebrew message without it). `/v1/users/me` does not exist. | OAS `/documents/info`; live probe |
| A13 | Secret hygiene | Keys from env vars or a secret store, never in prompts, logs or committed files; sandbox and production keys never mixed. | General, plus A1 |

### B. Document types (one row per type, the enum varies by type)

`DocumentType` has exactly 15 codes. Each must be listed with its purpose and who may issue it.

| # | Code | Document | Core point the skill must carry | Authority |
|---|------|----------|----------------------------------|-----------|
| B1 | 10 | הצעת מחיר | Non-fiscal; no VAT liability, no allocation number. | OAS `DocumentType` |
| B2 | 20 | חשבון / אישור תשלום | Non-fiscal payment demand; also an expense document type. | OAS `DocumentType`, `ExpenseDocumentType` |
| B3 | 100 | הזמנה | Non-fiscal order. | OAS `DocumentType` |
| B4 | 200 | תעודת משלוח | Delivery note. | OAS `DocumentType` |
| B5 | 210 | תעודת החזרה | Return note. | OAS `DocumentType` |
| B6 | 300 | חשבון עסקה | Transaction invoice (VATL s.45); not a tax invoice, buyer cannot deduct input VAT from it. | OAS; VATL s.45 and s.38(a) |
| B7 | 305 | חשבונית מס | Reserved to an osek murshe; issued at buyer demand; only type accepting `linkedPaymentId`; only type allowed with `client.self` (self-invoice, error 2412). | VATL s.47(a); OAS `/documents` POST notes; OAS error 2412 |
| B8 | 320 | חשבונית מס / קבלה | A tax invoice that is also a receipt, so equally reserved to an osek murshe; must carry payment rows. | VATL s.47(a); OAS `PaidDocumentType` |
| B9 | 330 | חשבונית זיכוי | Credit note; links to the original with `linkType: cancel`; buyer must reduce previously deducted input VAT. | OAS `DocumentLinkType`; VATL s.43 |
| B10 | 400 | קבלה | Receipt; link to the paid invoice via `linkedDocumentIds` so the invoice auto-closes. The receipt type used by osek patur. | OAS `/documents` POST notes |
| B11 | 405 | קבלה על תרומה | Donation receipt for an institution approved under ITO s.46; gives the donor a tax credit (35% for an individual). | ITO s.46(a); OAS `DocumentType` |
| B12 | 410 | ביטול תרומה | Cancels a 405. | OAS `DocumentType` |
| B13 | 500 | הזמנת רכש | Purchase order (buy side, non-fiscal). | OAS `DocumentType` |
| B14 | 600 | קבלת פיקדון | Deposit received. | OAS `DocumentType`, `PaidDocumentType` |
| B15 | 610 | משיכת פיקדון | Deposit withdrawal. | OAS `DocumentType` |
| B16 | Discovery endpoints | `GET /documents/types`, `/documents/statuses`, `/documents/templates`; the localised name follows `lang`. | OAS |

### C. Document type allowed per business type (one row per `BusinessType`)

Error 2403 ("סוג מסמך לא נשלח או אינו נתמך עבור סוג עסק זה") is returned when the type does not match
the business, so the matrix is core.

| # | `BusinessType` | Tax-invoice types 305 / 320 / 330 | Notes | Authority |
|---|----------------|-----------------------------------|-------|-----------|
| C1 | 1 עוסק מורשה | Allowed | Charges VAT at the standard rate by default. | VATL s.47(a); OAS `BusinessType` |
| C2 | 2 חברה בע"מ | Allowed | Registered as osek murshe for VAT. | VATL s.47(a) |
| C3 | 3 עוסק פטור | Not allowed | Issues 400 receipts (and 300 if needed) without VAT; annual turnover ceiling NIS 122,833 for 2026 (CPI-linked, re-check each January). | VATL s.47(a), s.1 definition; Morning ceiling page |
| C4 | 4 עמותה | Generally not | A malkar charges no output VAT; issues 400 and, if s.46-approved, 405. Commercial activity registered as osek is the exception. | VATL s.1 ("מלכ"ר"); ITO s.46 |
| C5 | 5 חברה לתועלת הציבור | As for C4 unless registered as osek | Same malkar logic. | VATL s.1 |
| C6 | 6 שותפות | Allowed when registered as osek murshe | | VATL s.47(a) |
| C7 | Osek zair is not a `BusinessType` | It is an income-tax status (ITO Amendment 265) independent of VAT classification; never map it to an API enum. | `evidence.json` `osek-zair-income-tax-status-amendment-265` |

### D. VAT handling (one row per business type x transaction type combination that changes the value)

| # | Case | API expression | Authority |
|---|------|----------------|-----------|
| D1 | Standard rate | 18% since 1.1.2025; returned as decimal `vatRate: 0.18` (never 18). Never hard-code: read `vatRate` from the response. | VATL s.2 via CPA summary (cpahadera); OAS `Document.vatRate` |
| D2 | Document-level `vatType` | `DocumentVatType`: 0 default (by business type), 1 exempt, 2 mixed. | OAS `DocumentVatType` |
| D3 | Row-level `vatType` | `ItemVatType`: 0 VAT added on top, 1 VAT included in price, 2 exempt. A different enum from D2; confusing them is the most common pricing bug. | OAS `ItemVatType` |
| D4 | Osek murshe, domestic taxable sale | doc `vatType` 0, rows 0 or 1. | VATL s.2 |
| D5 | Osek murshe, zero-rated export of goods or services | Zero rate under VATL s.30 (e.g. s.30(a)(1) goods export, s.30(a)(5) services to a foreign resident); legally distinct from exempt; set via row `vatRate` 0 / client `country` not IL. Zero-rated invoices are outside the allocation regime. | VATL s.30, s.47(a2)(1) last clause |
| D6 | Osek murshe, exempt transaction (s.31, e.g. residential rent) | Row `vatType` 2, doc `vatType` 2 if mixed with taxable rows; no input VAT on related inputs (s.41). | VATL s.31, s.41 |
| D7 | Osek patur, any sale | No VAT charged; doc default resolves to exempt; cannot issue 305/320. | VATL s.47(a) |
| D8 | Amuta / malkar | No output VAT (wage and payroll tax instead); receipts only. | VATL s.1, s.4 |
| D9 | Reverse-charge flag | `reverseCharge` boolean on search results, document info and the webhook payload. Moved to Out of scope (explicit), see below. | OAS `SearchDocument`, `WebhookDocumentCreated` |
| D10 | Discount and rounding | `discount {amount, type: sum|percentage}` is applied before VAT; `rounding` boolean. | OAS `DiscountRequest`, `rounding` |
| D11 | Totals returned | `taxableTotal`, `vatTaxableTotal`, `revenueTaxableTotal`, `exemptTotal` for reconciliation. | OAS webhook/document schema |

### E. Allocation number (מספר הקצאה, חשבוניות ישראל)

| # | Item | Content | Authority |
|---|------|---------|-----------|
| E1 | Seller duty | An osek murshe issuing a tax invoice may request an allocation number and MUST do so at the buyer's demand when the pre-VAT amount exceeds the s.38(a1) threshold; applies only where VAT is not at the zero rate. | VATL s.47(a2)(1) |
| E2 | Buyer consequence | Input VAT on a tax invoice above the threshold with no allocated number is not deductible (no buyer-request condition on this side). | VATL s.38(a1) |
| E3 | Threshold, invoices dated before May 2024 | No requirement. | Regime start, Morning "חשבוניות ישראל" page |
| E4 | Threshold, May 2024 to Dec 2024 | Above NIS 25,000 before VAT. | Morning and iCount schedule pages |
| E5 | Threshold, Jan 2025 to Dec 2025 | Above NIS 20,000. | Same |
| E6 | Threshold, Jan 2026 to May 2026 | Above NIS 10,000. | VATL s.38(a1) parenthetical ("מינואר 2026 ועד מאי 2026: 10,000") |
| E7 | Threshold, from June 2026 | Above NIS 5,000. No further step announced as of 2026-10-18. | VATL s.38(a1) main text |
| E8 | Threshold is keyed to invoice date and pre-VAT amount, "exceeds" (strictly greater) | Code must compare `amount before VAT > threshold(documentDate)`. | VATL s.38(a1) wording "עולה על" |
| E9 | Cumulative conditions | Above threshold, VAT component present (not zero-rated, not exempt-only), recipient is an osek murshe, recipient asked. | VATL s.47(a2)(1); Grant Thornton Israel 2026 note |
| E10 | Document types concerned | 305 and 320; Morning states no allocation number is issued for other document types. | VATL s.38(a1) ("חשבונית מס") |
| E11 | API fields | `allocationNumber` on `Document`, `UpdatedDocument`, `Expense`, `ExpenseRequest`, webhook `document/created` (omitted when none); `taxConfirmationEligible`, `taxAuthorityConfirmationInitiated`, `data.taxAuthorityConfirmationNumber`, `taxAuthorityConfirmationLastError` (0 ok, non-zero failure). | OAS schemas |
| E12 | Account-level connection | Morning obtains numbers through a business-level Tax Authority connection valid 3 months, renewal alert 10 days before expiry; an expired connection silently stops allocation. | Morning help centre `reconnect-tax-auth` |
| E13 | Refusal and hearing path | Director may refuse (preliminary decision), hearing within 2 business days, decision within 1 business day after it, default grant if silent; buyer may assume the tax (s.47(a3)). The skill must surface a missing number, not retry blindly. | VATL s.47(a2)(3), (a3), (a4) |
| E14 | Late request | A number may be requested after issue (s.47(a2)(4)); does not move the s.38(a) deduction date. | VATL s.47(a2)(4) |
| E15 | Outage exception | Director may allow deduction without a number when Tax Authority systems failed. | VATL s.40B |
| E16 | Input side check | When recording a supplier expense above threshold, capture its `allocationNumber`; without it the input VAT is at risk. | VATL s.38(a1); OAS `ExpenseRequest.allocationNumber` |

### F. Creating, linking and lifecycle of documents

| # | Item | Authority |
|---|------|-----------|
| F1 | `POST /documents` required: `type`, `lang`, `currency`, `vatType`, `income[]` (each row: description, quantity, price, currency, vatType); `client`, `date` (defaults to today) and `dueDate` are optional. | OAS `IncomeRowRequest`, `CreateDocumentRequest` |
| F2 | Preview before issuing: `POST /documents/preview` (fiscal documents cannot be deleted once issued). | OAS `/documents/preview` |
| F3 | Linking: `linkedDocumentIds` + `linkType` `link` or `cancel` (`copy` appears in responses); receipt linked to invoice auto-closes the invoice. | OAS `/documents` notes, `DocumentLinkType`, error 2404 |
| F4 | Status enum: 0 open, 1 closed, 2 manually closed, 3 cancelling, 4 cancelled; `/v1/documents/{id}/close` and `/open` (only reopen a manually closed one, error 2401). | OAS `DocumentStatus`, errors 2400/2401 |
| F5 | Cancellation is by a cancelling document (330 credit note, 410 for donations), never deletion. | OAS `DocumentLinkType`; VATL s.43 |
| F6 | Date rules: future or too-early date rejected per type (2405); payment date cannot be future (2426). | OAS errors 2405, 2426 |
| F7 | Limits: max 200 income/payment rows per document (2431); quantity and amount validation (2416-2418, 2430). | OAS error table |
| F8 | Retrieval: `GET /documents/{id}`, `/linked`, `/download/links`; `url.origin`/`he`/`en`. | OAS |
| F9 | Search: `/v1/documents/search`, 1-based `page`, default `pageSize` 25, response `total/page/pageSize/from/to/pages/items`, uses `documentDate` and `amount`. | OAS `SearchDocumentsRequest/Response` |
| F10 | Email delivery requires a digitally signed document (2427); `signed`, `emailContent`, `attachment` flags. | OAS error 2427 |
| F11 | Idempotency: the API has no idempotency key, so the integration must dedupe (search for the document by its own reference fields) before retrying a POST that timed out. | OAS (absence); webhook `custom` |

### G. Payments (receipt side)

| # | Item | Authority |
|---|------|-----------|
| G1 | `PaymentRowRequest` required: `date`, `type`, `price`, `currency`. | OAS |
| G2 | `PaymentGroup` (one row each): 0 withholding at source (ניכוי במקור), 1 cash, 2 cheque (bank fields required), 3 credit card, 4 bank transfer, 5 PayPal, 10 payment app, 11 other (needs `subType`). No -1 here. | OAS `PaymentGroup` |
| G3 | Withholding: a 0 row must be accompanied by at least one real payment row (2428); total of rows equals document total. | OAS error 2428; ITO s.164 and withholding regulations |
| G4 | Credit card detail: `CreditCardType` 0-5, `CreditCardDealType` 1-6, `numPayments` 1-36 (2425 range), `firstPayment`. | OAS enums, error table |
| G5 | `PaymentAppType`: 1 Bit, 2 Pay, 3 PayBox, 5 Google Pay, 6 Apple Pay. | OAS |
| G6 | `OtherSubType`: 1 Bitcoin, 2 money equivalent, 3 V-Check, 4 gift voucher, 5 employee NI deduction, 6 Ethereum, 7 BUYME, 9 other deduction. | OAS |
| G7 | Cash-law ceiling awareness: a cash payment row above the limits of חוק לצמצום השימוש במזומן risks the buyer's input VAT (VATL s.38(a2)). | VATL s.38(a2); Cash Law 2018 |
| G8 | Payment terms `PaymentTerm`: -1 immediate, 0 שוטף, 10/15/30/45/60/75/90/120 = שוטף+N. | OAS |
| G9 | Payments search `POST /documents/payments/search` over 320/400/405/600/610. | OAS |

### H. Clients, items, suppliers, expenses

| # | Item | Authority |
|---|------|-----------|
| H1 | Clients CRUD + search + merge + `assoc` + `balance`; `client.add` to save a one-off client; `country` ISO alpha-2 (default IL); `taxId` (ח.פ / ע.מ / ת.ז). `labels` are label IDs (max 3). | OAS `/clients*`, `ClientRequest` |
| H2 | Items CRUD + search (catalog numbers, default price, VAT type). | OAS `/items*` |
| H3 | Suppliers CRUD + search + merge; only `name` required, `taxId` accepted; supplier `labels` are names (asymmetric with clients). | OAS `SupplierRequest` |
| H4 | Expense create: required `documentType`, `number`, `date`, `reportingDate`, `supplier`, `accountingClassification`. | OAS `ExpenseRequest` |
| H5 | `ExpenseDocumentType` (one row each): 20, 305, 320, 330, 400, 405. Input VAT is claimable only on 305/320 (minus 330); 20/400 carry none. | OAS; VATL s.38(a) |
| H6 | `amount` includes VAT, `vat` is the VAT part and cannot exceed amount. | OAS |
| H7 | `reportingDate` is the VAT reporting month, `YYYY-MM-01`; date 2010-01-01 or later, not future. | OAS |
| H8 | `pcnClassification` for PCN874 (one row each): T regular input, R import entry (רשומון), K petty-cash supplier, P Palestinian Authority supplier, C self-invoice input, H other. | OAS `ExpensePcnClassifications` |
| H9 | `ExpenseStatus` 10/20/30/40/100 and `ExpensePaymentType` (includes -1 not paid). | OAS |
| H10 | File-attached expense becomes a draft first (`/expenses/drafts/search`, statuses 10/50/200); no approval endpoint in the API. Upload is two-step via `https://api.morning.co/file-upload/v1/url`. | OAS |
| H11 | Input allocation number captured on expenses (see E16). | OAS; VATL s.38(a1) |

### I. Webhooks

| # | Item | Authority |
|---|------|-----------|
| I1 | Configured in the Morning UI (Developer Tools, Webhooks), not by API. | OAS Webhooks tag |
| I2 | Ten topics: `document/created`, `client/created`, `supplier/created`, `payment/received`, `sale-pages/page-contacted`, `sale-pages/order-paid`, `expense-draft/parsed`, `expense-draft/declined`, `expense/file-updated`, `file/infected`; topic in `x-webhook-topic` header. | OAS `x-webhooks` |
| I3 | Verification: `x-webhook-signature` = hex HMAC-SHA256 of the raw body keyed with the secret; constant-time compare over raw bytes; present only when a secret is set. | OAS Webhooks tag |
| I4 | Payload rules: absent fields are omitted, not null; treat everything as optional; item VAT arrives as `tax[{name, rate}]`, not `vatRate`. | OAS webhook schemas |
| I5 | Delivery hygiene: respond 2xx fast, process async, dedupe on payload `id` + `x-correlation-id`. | OAS headers table; general |

### J. Multi-currency

| # | Item | Authority |
|---|------|-----------|
| J1 | `Currency` enum (27 ISO codes); document currency vs row currency with `currencyRate` relative to ILS (default 1). | OAS `Currency`, `IncomeRowRequest` |
| J2 | Payment forms and token charges accept only ILS, USD, EUR, GBP (`PaidCurrency`). | OAS `PaidCurrency` |
| J3 | `GET /currency-exchange/v1/latest` gives `spot` and `closing` rates; VAT reporting uses the Bank of Israel representative rate, so record which rate was used. | OAS; VAT regulations on converting foreign-currency consideration (verify the exact provision before citing) |

### K. Errors and operations

| # | Item | Authority |
|---|------|-----------|
| K1 | API error object (`errorCode`, `errorMessage`, Hebrew text); document error codes 2400-2435 mapped to fixes. | OAS error table |
| K2 | 401 means token expired, refresh once then fail; 403 inactive partner; 429 handling with backoff (no published rate limit, so be conservative). | OAS; general |
| K3 | Amounts are decimal shekels, not agorot. | OAS examples |

## Should cover (advanced)

| # | Item | Authority |
|---|------|-----------|
| S1 | Partner (multi-business) flow: Basic auth `Base64(id:secret)`, `GET /partners/users`, `POST /partners/users/connection` (user approval, callback signed with `X-Data-Signature` HMAC-SHA256), `DELETE` to disconnect. | OAS Partners tag, `basicAuth` scheme |
| S2 | Payment form: `POST /payments/form` returns a hosted URL (iframe or redirect) creating 320/400/405/600 on success, groups 100/110/120/150/160, `maxPayments`. | OAS `PaymentFormRequest` |
| S3 | Saved card tokens: `POST /payments/tokens/search`, `POST /payments/tokens/{id}/charge`; token statuses 0-4; PCI scope stays with Morning. | OAS |
| S4 | `paymentRequestData.plugins` on a document (PluginType 12010 PayPal, 12100 Cardcom, 12120 Max, 12130 Grow, 12200 Morning). | OAS `PluginType`, `PaymentPluginGroup` |
| S5 | Self-invoice (חשבונית עצמית) for purchases from a non-issuing seller: `client.self: true`, type 305 only; input classified `C` in PCN874. | OAS error 2412; OAS `ExpensePcnClassifications` (C); VAT regulations on self-invoicing (verify the regulation number before citing) |
| S6 | Donation receipts and the 2026 digital donations reporting duty for s.46 institutions (receipt software reports automatically). | ITO s.46; Tax Authority digital donations system |
| S7 | Sale pages webhooks (`order-paid`, `page-contacted`) for e-commerce flows. | OAS |
| S8 | Reference data: `/geo-location/v1/countries`, `/cities`, `/businesses/v1/occupations`. | OAS |
| S9 | Expense draft parsing events (`expense-draft/parsed`, `declined`) for OCR pipelines. | OAS |
| S10 | Infected-file webhook handling (quarantine, do not retry upload). | OAS `file/infected` |
| S11 | Undocumented paths (`/businesses`) exist live but are outside the contract; do not depend on them. | Live probe in `evidence.json` |
| S12 | Accounting export hand-off: `accountingKey`, `accountingClassification` (`irsCode`) for the bookkeeper. | OAS |
| S13 | Osek patur ceiling monitoring (annual CPI update; crossing it forces osek murshe registration and changes allowed document types). | VATL s.1; Tax Authority annual notice |
| S14 | Sandbox data hygiene: sandbox documents carry no legal weight and are never reported. | OAS `info` |

## Out of scope (explicit)

| Item | Rationale |
|------|-----------|
| G7 cash-law ceilings on cash payment rows | A payment-law compliance question, not an API behaviour; the skill records what was paid. Route to the user's accountant. (2026-10-18) |
| D9 reverse charge, S5 / B7 self-invoice (`client.self`) | Niche flows (purchases from a non-issuing seller, reverse-charge services) that an ordinary sales integration does not hit; the fields are named in the API reference. (2026-10-18) |
| Input-VAT period mechanics beyond the s.38(a) six-month rule (recoverable-% computation, PCN874 filing) | VAT-return preparation belongs to `israeli-vat-reporting`; this skill records expenses with the right fields. (2026-10-18) |
| Direct SHAAM / Tax Authority allocation API (OAuth to ITA, `Invoices/v1/Approval`) | Handled by sibling skill `israeli-e-invoice`; this skill only reads what Morning returns. |
| Cardcom, Tranzila, Pelecard, Meshulam/Grow gateway APIs | Each has its own skill; here only the Morning plugin IDs are named. |
| Bookkeeping, PCN874 file generation, periodic VAT return filing | `israeli-bookkeeping-automation` and accountant workflows; the skill only sets classifications. |
| Annual income-tax reports and form 1301/6111 | `israeli-annual-reports`. |
| Payroll, wage slips, malkar wage tax | Payroll skills (`israeli-payroll-calculator`). |
| Receipt OCR on device | `israeli-receipt-scanner`. |
| Bank reconciliation | `israeli-bank-reconciliation`. |
| Choosing a business classification (patur vs murshe vs company) for the user | A decision for the user and their accountant; the skill explains API consequences only. |
| Hashavshevet, iCount, Rivhit and other invoicing vendors | Different APIs; `hashavshevet-data-tools` covers one. |
| Amuta governance (registrar filings, proper-management certificate) | `israeli-amuta-compliance`. |

## Authoritative sources

1. Morning API OpenAPI 2.0.0 bundle: https://developers.morning.co/docs/openapi.bundled.json (45 paths, 10 webhook topics).
2. Morning developer portal: https://developers.morning.co/
3. Morning help centre, generating an API key: https://www.greeninvoice.co.il/help-center/generating-api-key/
4. Morning help centre, Tax Authority connection renewal: https://www.greeninvoice.co.il/help-center/reconnect-tax-auth/
5. Morning help centre, Tax Authority connect for developers: https://www.greeninvoice.co.il/help-center/developers/tax-auth-connect/
6. Morning magazine, חשבוניות ישראל schedule: https://www.greeninvoice.co.il/magazine/israel-invoice/
7. Morning magazine, webhooks: https://www.greeninvoice.co.il/magazine/webhooks/
8. Morning, osek patur ceiling 2026: https://www.greeninvoice.co.il/magazine/%D7%AA%D7%A7%D7%A8%D7%AA-%D7%A2%D7%95%D7%A1%D7%A7-%D7%A4%D7%98%D7%95%D7%A8/
9. VAT Law (חוק מס ערך מוסף), ss.1, 2, 4, 30, 31, 38(a), 38(a1), 38(a2), 40B, 41, 43, 45, 47(a), 47(a1), 47(a2), 47(a3), 47(a4): https://he.wikisource.org/wiki/%D7%97%D7%95%D7%A7_%D7%9E%D7%A1_%D7%A2%D7%A8%D7%9A_%D7%9E%D7%95%D7%A1%D7%A3
10. Income Tax Ordinance (פקודת מס הכנסה), s.46 and Amendment 265 (osek zair): https://he.wikisource.org/wiki/%D7%A4%D7%A7%D7%95%D7%93%D7%AA_%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94
11. Israel Tax Authority online service, request an allocation number: https://www.gov.il/he/service/request-assignment-number-for-tax-invoice
12. Israel Tax Authority home: https://www.gov.il/he/departments/israel_tax_authority
13. Grant Thornton Israel, allocation number from June 2026: https://www.grantthornton.co.il/insights1/tax-insignths/2026/From_June_the_allocation_number/
14. iCount, חשבוניות ישראל schedule (independent corroboration): https://www.icount.co.il/blog/invoice-israel/
15. VAT at 18% from 1.1.2025, via CPA summary: https://cpahadera.co.il/%D7%9E%D7%A2%D7%9E/
16. Bank of Israel representative exchange rates: https://www.boi.org.il/en/economic-roles/financial-markets/exchange-rates/
17. חוק לצמצום השימוש במזומן, התשע"ח-2018 (cash ceilings).
18. Existing skill evidence file (live probes for legacy auth, sandbox removal, `/users/me` absence): `evidence.json` in this skill folder
