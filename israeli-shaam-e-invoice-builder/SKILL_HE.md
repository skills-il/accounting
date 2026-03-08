---
name: israeli-shaam-e-invoice-builder
description: >-
  Build SHAAM-compliant electronic invoices with allocation numbers (mispar haktsa'a) per Israeli Tax Authority (ITA) requirements.
  Use when generating tax invoices, credit notes, or receipts that require ITA allocation numbers for VAT deduction eligibility.
  Handles OAuth2 authentication, JSON payload construction per ITA technical specs v2.0, buyer VAT validation,
  and batch submission. Supports the phased threshold rollout (20K NIS Jan 2025, 10K NIS Jan 2026, 5K NIS June 2026).
  Do NOT use for bookkeeping, expense categorization, bank reconciliation, or non-Israeli tax jurisdictions.
license: MIT
allowed-tools: "Bash(node:*,npx:*,curl:*) WebFetch Edit Read"
compatibility: "Requires network access for SHAAM API calls and OAuth2 token exchange"
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
    he: "בונה חשבוניות דיגיטליות - שע\"ם"
    en: "Israeli SHAAM E-Invoice Builder"
  display_description:
    he: "בניית חשבוניות אלקטרוניות תואמות שע\"ם עם מספרי הקצאה לפי דרישות רשות המסים"
    en: "Build SHAAM-compliant electronic invoices with allocation numbers per Israeli Tax Authority requirements"
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
---

# בונה חשבוניות דיגיטליות - שע"ם

## סקירה כללית

מערכת שע"ם (שנות אסמכתא מקוונת) היא הפלטפורמה של רשות המסים בישראל להנפקת מספרי הקצאה לחשבוניות אלקטרוניות. החל מינואר 2025, חשבוניות מעל סכומים מסוימים מחייבות מספר הקצאה כדי שהקונה יוכל לנכות מס תשומות. מיומנות זו מבצעת אוטומציה של התהליך מקצה לקצה: אימות, בניית חשבונית, ולידציה, הגשה וקבלת מספר הקצאה.

### לוח זמנים לציות

| תאריך | סף מינימלי | היקף |
|--------|-------------|------|
| ינואר 2025 | 25,000 ש"ח (כולל מע"מ) | חשבוניות מעל הסף מחייבות מספר הקצאה |
| ינואר 2026 | 10,000 ש"ח (כולל מע"מ) | הורדת הסף |
| יוני 2026 | 5,000 ש"ח (כולל מע"מ) | הסף הסופי המתוכנן |

ללא מספר הקצאה תקף, הקונה אינו יכול לנכות מס תשומות בעסקה.

## הוראות

### שלב 1: הגדרת פרטי גישה לממשק שע"ם

הגדרת פרטי OAuth2 לפלטפורמת שע"ם. נדרשים מזהה לקוח וסוד לקוח שהונפקו על ידי רשות המסים לאחר רישום התוכנה.

שמירת פרטי הגישה במשתני סביבה:

```bash
export SHAAM_CLIENT_ID="your-client-id"
export SHAAM_CLIENT_SECRET="your-client-secret"
export SHAAM_ENV="production"  # או "sandbox" לבדיקות
```

כתובות בסיס של הממשק:
- **סביבת בדיקות**: `https://ita-api-sandbox.taxes.gov.il/shaam/api/v2`
- **סביבת ייצור**: `https://ita-api.taxes.gov.il/shaam/api/v2`

נקודת קצה לטוקן OAuth2:
- **סביבת בדיקות**: `https://ita-api-sandbox.taxes.gov.il/auth/oauth2/token`
- **סביבת ייצור**: `https://ita-api.taxes.gov.il/auth/oauth2/token`

### שלב 2: אימות באמצעות OAuth2

קבלת טוקן גישה באמצעות client credentials grant:

```bash
curl -X POST "${SHAAM_TOKEN_URL}" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  -d "client_id=${SHAAM_CLIENT_ID}" \
  -d "client_secret=${SHAAM_CLIENT_SECRET}" \
  -d "scope=invoice:write invoice:read"
```

התגובה מחזירה טוקן גישה תקף ל-60 דקות:

```json
{
  "access_token": "eyJ...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "invoice:write invoice:read"
}
```

יש לשמור את הטוקן במטמון ולרענן אותו לפני פקיעת התוקף. אין לבקש טוקן חדש עבור כל קריאת API.

### שלב 3: בניית מבנה JSON של החשבונית

בניית אובייקט החשבונית לפי המפרט הטכני v2.0 של רשות המסים. מבנה ה-JSON הנדרש:

```json
{
  "invoice_type": "hashbonit_mas",
  "invoice_number": "INV-2026-001234",
  "invoice_date": "2026-03-08",
  "supplier": {
    "tax_id": "123456789",
    "name": "ספק בע\"מ",
    "address": {
      "street": "שדרות רוטשילד 1",
      "city": "תל אביב",
      "postal_code": "6688101"
    }
  },
  "buyer": {
    "tax_id": "987654321",
    "name": "קונה בע\"מ",
    "address": {
      "street": "רחוב הרצל 10",
      "city": "ירושלים",
      "postal_code": "9423201"
    }
  },
  "line_items": [
    {
      "description": "שירותי פיתוח תוכנה",
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

**סוגי חשבוניות נתמכים:**

| סוג | עברית | תיאור |
|-----|-------|-------|
| `hashbonit_mas` | חשבונית מס | חשבונית מס רגילה |
| `hashbonit_mas_kabala` | חשבונית מס / קבלה | חשבונית מס עם קבלה |
| `hashbonit_zikuy` | חשבונית זיכוי | חשבונית זיכוי |
| `kabala` | קבלה | קבלה |

### שלב 4: ולידציה של החשבונית לפני ההגשה

לפני ההגשה, יש לבצע ולידציה מקומית של החשבונית:

1. **אימות מספר עוסק מורשה של הקונה**: אימות שמספר העוסק הוא מספר בן 9 ספרות תקף. אלגוריתם ספרת הביקורת משתמש בסכום משוקלל מודולו 10 עם משקלות [1,2,1,2,1,2,1,2,1].

2. **בדיקת סף**: קביעה האם סכום החשבונית (כולל מע"מ) חורג מהסף הנוכחי. אם מתחת לסף, מספר הקצאה אינו נדרש אך ניתן עדיין לבקש אותו.

3. **שדות חובה**: וידוא שכל השדות החובה מאוכלסים: `invoice_type`, `invoice_number`, `invoice_date`, `supplier.tax_id`, `buyer.tax_id`, פריטי שורה עם חישובי מע"מ תקינים.

4. **אימות חישוב מע"מ**: אישור ש-`vat_amount` שווה ל-`total_before_vat * vat_rate / 100` עבור כל פריט שורה, ושהסיכומים עקביים.

5. **אימות תאריך**: `invoice_date` לא יכול להיות בעתיד ולא יותר מ-6 חודשים בעבר.

### שלב 5: הגשת החשבונית לקבלת מספר הקצאה

הגשת החשבונית המאומתת לממשק שע"ם:

```bash
curl -X POST "${SHAAM_BASE_URL}/invoices" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d @invoice.json
```

תגובה מוצלחת (HTTP 201):

```json
{
  "allocation_number": "IL-2026-0308-A1B2C3D4",
  "invoice_reference": "INV-2026-001234",
  "status": "approved",
  "valid_until": "2026-04-07T23:59:59Z",
  "qr_code_data": "https://www.invoice.gov.il/verify/IL-2026-0308-A1B2C3D4"
}
```

`allocation_number` (מספר הקצאה) חייב להיות מודפס על החשבונית. כתובת ה-`qr_code_data` מאפשרת לקונה לאמת את החשבונית מקוון.

### שלב 6: טיפול בהגשות מרוכזות

לחשבוניות בנפח גבוה, יש להשתמש בנקודת הקצה למשלוח מרוכז:

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

תגובת משלוח מרוכז:

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
      "error_message": "מספר עוסק מורשה של הקונה לא עבר אימות"
    }
  ]
}
```

גודל מרבי של משלוח מרוכז הוא 100 חשבוניות לבקשה. לנפחים גדולים יותר, יש לפצל למשלוחים מרובים עם השהייה של שנייה אחת בין הבקשות.

### שלב 7: שאילתת סטטוס מספר הקצאה

בדיקת סטטוס של חשבונית שהוגשה קודם:

```bash
curl -X GET "${SHAAM_BASE_URL}/invoices/{invoice_reference}/status" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

תגובה:

```json
{
  "invoice_reference": "INV-2026-001234",
  "allocation_number": "IL-2026-0308-A1B2C3D4",
  "status": "approved",
  "created_at": "2026-03-08T10:30:00Z",
  "valid_until": "2026-04-07T23:59:59Z"
}
```

### שלב 8: טיפול בחשבוניות זיכוי

בעת הנפקת חשבונית זיכוי, יש להפנות לחשבונית המקורית:

```json
{
  "invoice_type": "hashbonit_zikuy",
  "invoice_number": "CN-2026-000045",
  "invoice_date": "2026-03-08",
  "original_invoice_reference": "INV-2026-001234",
  "original_allocation_number": "IL-2026-0308-A1B2C3D4",
  "reason": "ביטול חלקי של שירות",
  "line_items": [
    {
      "description": "שירותי פיתוח תוכנה - זיכוי",
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

חשבוניות זיכוי מקבלות מספר הקצאה משלהן וחייבות להפנות לחשבונית המקורית.

## דוגמאות

### דוגמה 1: הנפקת חשבונית מס רגילה מעל הסף

המשתמש אומר: "צור חשבונית אלקטרונית על 30,000 ש"ח בתוספת מע"מ לקונה עם מספר עוסק 514788338 עבור שירותי ייעוץ"

פעולות:
1. אימות מול ממשק שע"ם באמצעות פרטי OAuth2 שמורים
2. אימות מספר עוסק 514788338 באמצעות אלגוריתם ספרת ביקורת (משקלות [1,2,1,2,1,2,1,2,1], סכום מודולו 10 = 0)
3. חישוב מע"מ: 30,000 * 0.17 = 5,100 ש"ח, סה"כ = 35,100 ש"ח
4. אישור שסה"כ 35,100 ש"ח חורג מהסף הנוכחי, נדרש מספר הקצאה
5. בניית JSON של חשבונית עם `invoice_type: "hashbonit_mas"`
6. הגשה לנקודת קצה `POST /invoices`
7. קבלת מספר הקצאה `IL-2026-0308-X7Y8Z9W0`
8. החזרת חשבונית מעוצבת עם מספר הקצאה וכתובת QR

תוצאה: חשבונית מס נוצרה עם מספר הקצאה IL-2026-0308-X7Y8Z9W0. הקונה יכול לנכות 5,100 ש"ח מס תשומות.

### דוגמה 2: הגשת חשבוניות חודשיות במרוכז

המשתמש אומר: "הגש את כל 25 החשבוניות ממחזור החיוב של מרץ 2026 לשע"ם"

פעולות:
1. אימות מול ממשק שע"ם
2. קריאת כל 25 רשומות החשבוניות ממערכת החיוב
3. ולידציה של כל חשבונית: מספרי עוסק של קונים, חישובי מע"מ, שדות חובה
4. סימון 2 חשבוניות עם מספרי עוסק לא תקינים, הפנייה לטיפול ידני
5. הגשת 23 חשבוניות תקינות במשלוח מרוכז אחד דרך `POST /invoices/batch`
6. עיבוד תגובת המשלוח: 22 אושרו, 1 נדחתה (מספר חשבונית כפול)
7. דיווח תוצאות: 22 מספרי הקצאה התקבלו, 1 כפולה לתיקון, 2 ממתינות לטיפול ידני

תוצאה: 22 חשבוניות קיבלו מספרי הקצאה. 3 חשבוניות דורשות טיפול (2 מספרי עוסק לא תקינים, 1 מספר כפול).

### דוגמה 3: הנפקת חשבונית זיכוי להחזר חלקי

המשתמש אומר: "הנפק חשבונית זיכוי על 8,000 ש"ח כנגד חשבונית INV-2026-000789"

פעולות:
1. אימות מול ממשק שע"ם
2. שאילתת סטטוס חשבונית מקורית דרך `GET /invoices/INV-2026-000789/status`
3. אישור שלחשבונית המקורית יש מספר הקצאה IL-2026-0215-M3N4P5Q6
4. בניית JSON חשבונית זיכוי עם `invoice_type: "hashbonit_zikuy"`, סכומים שליליים
5. כלילת `original_invoice_reference` ו-`original_allocation_number`
6. הגשה לנקודת קצה `POST /invoices`
7. קבלת מספר הקצאה לחשבונית הזיכוי

תוצאה: חשבונית זיכוי CN-2026-000120 הונפקה עם מספר הקצאה משלה, עם הפנייה לחשבונית המקורית.

## פתרון בעיות

### שגיאה: "BUYER_TAX_ID_INVALID"

סיבה: מספר העוסק המורשה בן 9 הספרות של הקונה נכשל באימות ספרת הביקורת, או שמספר העוסק אינו רשום כעסק פעיל הרשום במע"מ ברשות המסים.

פתרון:
1. אמת את מספר העוסק באמצעות אלגוריתם ספרת ביקורת: הכפל כל ספרה במשקלות [1,2,1,2,1,2,1,2,1], סכם את ספרות כל מכפלה, הסכום מודולו 10 חייב להיות 0
2. בדוק שהעסק רשום באופן פעיל בכתובת `https://www.misim.gov.il/mm-hofashosek/`
3. אם הקונה הוא עוסק פטור, מספר הקצאה אינו נדרש

### שגיאה: "DUPLICATE_INVOICE_NUMBER"

סיבה: חשבונית עם אותו `invoice_number` כבר הוגשה לשע"ם על ידי מספר העוסק שלך.

פתרון:
1. שאילתת החשבונית הקיימת דרך `GET /invoices/{invoice_number}/status`
2. אם המקורית אושרה, יש להשתמש במספר ההקצאה הקיים
3. אם יש צורך להגיש מחדש גרסה מתוקנת, יש להנפיק חשבונית זיכוי כנגד המקורית וליצור חשבונית חדשה עם מספר שונה

### שגיאה: "TOKEN_EXPIRED" או "UNAUTHORIZED"

סיבה: טוקן הגישה של OAuth2 פג (הטוקנים תקפים ל-60 דקות) או שפרטי הגישה שגויים.

פתרון:
1. בקש טוקן חדש מנקודת הקצה של OAuth2 באמצעות client credentials
2. ודא ש-`SHAAM_CLIENT_ID` ו-`SHAAM_CLIENT_SECRET` נכונים
3. בדוק שרישום התוכנה שלך ברשות המסים עדיין פעיל
4. לסביבת בדיקות, ודא שאתה משתמש בנקודת הקצה של סביבת הבדיקות ולא של הייצור

### שגיאה: "VAT_CALCULATION_MISMATCH"

סיבה: סכומי המע"מ שהוגשו אינם תואמים לחישוב הצפוי על בסיס סיכומי פריטי השורה ושיעור המע"מ.

פתרון:
1. חשב מחדש: `vat_amount = total_before_vat * vat_rate / 100`
2. ודא שהעיגול עקבי (עיגול ל-2 ספרות אחרי הנקודה, שימוש בעיגול בנקאי)
3. ודא ש-`totals.total_vat` שווה לסכום כל ערכי `vat_amount` של פריטי השורה
4. ודא ש-`totals.total_with_vat` שווה ל-`totals.total_before_vat + totals.total_vat`

### שגיאה: "INVOICE_DATE_OUT_OF_RANGE"

סיבה: תאריך החשבונית הוא בעתיד או לפני יותר מ-6 חודשים.

פתרון:
1. הגדר את `invoice_date` לתאריך של היום או לתאריך העסקה בפועל
2. לחשבוניות עם תאריך מוקדם ביותר מ-6 חודשים, יש לפנות לתמיכה של רשות המסים לעיבוד ידני
3. ודא שפורמט התאריך הוא ISO 8601: `YYYY-MM-DD`
