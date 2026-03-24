---
name: icount
description: iCount accounting API expert for Israeli businesses. Use this skill whenever working with iCount — creating invoices, managing clients, recording expenses, looking up payments, syncing financial data, or integrating iCount with other systems. Trigger on any mention of iCount, Israeli invoices, חשבוניות, icount API, financial sync, or creating any document (invoice/receipt/quote). Also trigger when the user mentions "create an invoice", "add a client", "record a payment", or any financial automation task for an Israeli business.
license: MIT
compatibility: Requires network access for iCount API calls (api.icount.co.il). API key obtained from iCount dashboard under Settings → API. Works with Claude Code, Claude.ai, Cursor.
metadata:
  author: Tura2
  version: 1.0.0
  category: accounting
  tags:
    he:
      - איקאונט
      - חשבוניות
      - הנהלת-חשבונות
      - מע״מ
      - ישראל
      - חשבונאות
    en:
      - icount
      - invoicing
      - accounting
      - vat
      - israel
      - finance
  display_name:
    he: iCount
    en: iCount
  display_description:
    he: מומחה לאינטגרציה עם iCount API — יצירת חשבוניות, ניהול לקוחות, תיעוד הוצאות ואוטומציה פיננסית לעסקים ישראליים
    en: iCount accounting API expert for Israeli businesses — create invoices, manage clients, record expenses, and automate financial workflows
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
---

# iCount API Skill

iCount is an Israeli cloud accounting platform. Its REST API lets you create documents (invoices, receipts, quotes), manage clients, record expenses, and more.

> All information below is **live-verified** against the actual API as of March 2026.

---

## Authentication

**Base URL:** `https://api.icount.co.il/api/v3.php/<module>/<method>`

**Auth method:** Bearer token in the `Authorization` header. No `cid` (company ID) needed.

```
POST https://api.icount.co.il/api/v3.php/<module>/<method>
Authorization: Bearer YOUR_API_KEY
Content-Type: application/x-www-form-urlencoded
```

Set `ICOUNT_API_KEY` in your `.env` file. Find your API key in iCount under Settings → API.

**Rate limit:** 30 requests/minute. All responses are JSON.

---

## URL Structure

All endpoints follow the pattern: `/api/v3.php/<module>/<method>`

| Module | Methods |
|--------|---------|
| `client` | `get_list`, `create`, `delete`, `info`, `update` |
| `doc` | `types`, `create`, `search`, `get` |
| `expense` | `types`, `search`, `create` |
| `supplier` | `get_list`, `add`, `info`, `update` |

---

## Key Endpoints

### Clients

```
POST /client/get_list      → list all clients
POST /client/create        → create new client (requires: client_name)
POST /client/delete        → delete client (requires: client_id)
POST /client/info          → get single client (requires: client_id)
POST /client/update        → update client (requires: client_id + fields)
```

**client/get_list response:**
```json
{
  "status": true,
  "clients_count": "2",
  "clients": {
    "7": {
      "client_id": "7",
      "custom_client_id": "",
      "vat_id": "",
      "company_name": "Acme Ltd",
      "client_name": "John Doe",
      "email": "john@example.com"
    }
  }
}
```

**client/create — full field list:**
```
client_name       (required)
phone
mobile
email
address
city
zip
country           (default: IL)
vat_id            (Israeli tax ID / ת.ז.)
custom_client_id  (use this to link iCount clients to external systems: store an external system's ID here)
notes
```

### Documents

```
POST /doc/types            → get available document types
POST /doc/create           → create a document (invoice, receipt, etc.)
POST /doc/search           → search documents by date/client/type
POST /doc/get              → get single document (requires: doc_id)
```

**Verified doctype values** (from live `doc/types` call):

| doctype | Hebrew | Use case |
|---------|--------|----------|
| `invrec` | חשבונית מס קבלה | Tax invoice + receipt (most common — client pays immediately) |
| `invoice` | חשבונית מס | Tax invoice only (payment to follow) |
| `receipt` | קבלה | Receipt only (against existing invoice) |
| `refund` | זיכוי | Credit note / refund |
| `offer` | הצעת מחיר | Quote / price offer |
| `order` | הזמנה | Order |
| `delcert` | תעודת משלוח | Delivery note |
| `deal` | עסקה | Deal/transaction |
| `po` | הזמנת רכש | Purchase order |

**doc/create — request format (form-encoded, NOT JSON):**
```
doctype=invrec
client_id=7                    # preferred: use existing client
# OR: client_name=John Doe     # alternative: creates inline (no persistent client)

doc_date=20260322              # YYYYMMDD format (not YYYY-MM-DD)
currency=NIS                   # NIS, USD, EUR, GBP, etc.
vattype=1                      # see vattype values below

# Line items — indexed notation:
desc[0]=Consulting services - March
unitprice[0]=1000
quantity[0]=1

desc[1]=Registration fee       # optional second item
unitprice[1]=100
quantity[1]=1

comment=Monthly retainer       # optional
```

**vattype values:**
| vattype | Meaning |
|---------|---------|
| `0` | Use account default |
| `1` | Standard VAT (18% as of 2025 in Israel) |
| `2` | Zero-rated / Exempt (פטור ממע"מ) |

### Expenses

```
POST /expense/types        → get expense type list
POST /expense/search       → search expenses (params: start_date, end_date)
POST /expense/create       → record expense
```

### Suppliers

```
POST /supplier/get_list    → list all suppliers
POST /supplier/add         → add supplier (params: supplier_name, vat_id)
POST /supplier/info        → get supplier (params: supplier_id)
POST /supplier/update      → update supplier
```

---

## Error Handling

Every response has `"status": true/false`. Always check before proceeding:

```python
import requests

def icount_post(endpoint, data):
    resp = requests.post(
        f"https://api.icount.co.il/api/v3.php/{endpoint}",
        headers={"Authorization": f"Bearer {ICOUNT_API_KEY}"},
        data=data  # form-encoded, NOT json=
    )
    result = resp.json()
    if not result.get("status"):
        raise Exception(f"iCount [{result.get('reason')}]: {result.get('error_description', '')}")
    return result
```

Common error `reason` values: `auth_required`, `bad_method`, `bad_doctype`, `missing_client_name`, `required_parameters_missing`, `client_deleted`.

---

## Python Examples

### Create a Client

```python
result = icount_post("client/create", {
    "client_name": "משה כהן",
    "phone": "050-1234567",
    "email": "moshe@example.com",
    "custom_client_id": "external_system_id_here"  # optional: link to external system
})
client_id = result["client_id"]
```

### Create an Invoice-Receipt (most common)

```python
import datetime

result = icount_post("doc/create", {
    "doctype": "invrec",
    "client_id": client_id,
    "doc_date": datetime.date.today().strftime("%Y%m%d"),
    "vattype": 1,
    "desc[0]": "Consulting services - March",
    "unitprice[0]": 1000,
    "quantity[0]": 1,
    "comment": "Monthly retainer",
})
doc_id = result["doc_id"]
```

### Search Recent Documents

```python
results = icount_post("doc/search", {
    "start_date": "20260101",
    "end_date": "20260331",
})
for doc in results.get("results_list", []):
    print(doc["doc_id"], doc["client_name"], doc["total"])
```

### List All Clients

```python
result = icount_post("client/get_list", {})
for client_id, client in result["clients"].items():
    print(client_id, client["client_name"], client.get("email"))
```

---

## Third-Party System Sync Pattern

The `custom_client_id` field in iCount is useful as a bridge when syncing with external systems (CRM, project management tools, etc.):

```
When a new client is added in your external system:
  1. POST /client/create → { client_name, phone, email, custom_client_id: <external_id> }
  2. Store returned iCount client_id back in your external system

When a recurring billing event fires (e.g. n8n/webhook trigger):
  1. Look up iCount client_id from your external system's stored "iCount ID"
  2. POST /doc/create → { doctype: "invrec", client_id: ..., items: [...] }

When payment is confirmed in iCount:
  1. Webhook or poll /doc/search for paid docs
  2. Update the corresponding record in your external system
```

---

## Scripts

Two helper scripts are bundled in `scripts/`:

- **`scripts/test_connection.py`** — verifies the API key is valid, prints client count and a sample of document types. Run this first to confirm the setup works.
- **`scripts/list_doctypes.py`** — fetches the full live list of document types for the user's account and prints them in a table.

Both require `pip install requests` and `ICOUNT_API_KEY` set in the environment or `.env`.

---

## Notes

- All amounts are in ILS (₪) by default
- **Date format:** `YYYYMMDD` (e.g., `20260322`) — NOT `YYYY-MM-DD`
- **Request body:** always use form-encoded (`data=...`), not JSON (`json=...`)
- For Hebrew field values, ensure UTF-8 encoding
- The API is included with all iCount subscriptions
- `doc/types` endpoint gives the live list for your account — call it to discover account-specific types
