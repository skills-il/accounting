---
name: icount
description: מומחה ל-iCount API לעסקים ישראליים. השתמש בסקיל זה בכל פעם שעובדים עם iCount — יצירת חשבוניות, ניהול לקוחות, תיעוד הוצאות, חיפוש תשלומים, סנכרון נתונים פיננסיים, או אינטגרציה של iCount עם מערכות אחרות. הפעל בכל אזכור של iCount, חשבוניות ישראליות, icount API, סנכרון פיננסי, או יצירת מסמך כלשהו (חשבונית/קבלה/הצעת מחיר). הפעל גם כשהמשתמש מזכיר "צור חשבונית", "הוסף לקוח", "תעד תשלום", או כל אוטומציה פיננסית לעסק ישראלי.
license: MIT
compatibility: דורש גישת רשת ל-iCount API. מפתח API מתקבל מלוח הבקרה של iCount תחת הגדרות ← API. עובד עם Claude Code, Claude.ai, Cursor.
---

# סקיל iCount API

iCount היא פלטפורמת הנהלת חשבונות ישראלית בענן. ה-API שלה מאפשר יצירת מסמכים (חשבוניות, קבלות, הצעות מחיר), ניהול לקוחות, תיעוד הוצאות ועוד.

> כל המידע מטה **אומת מול ה-API האמיתי** של iCount — מרץ 2026.

---

## אימות

**כתובת בסיס:** `https://api.icount.co.il/api/v3.php/<מודול>/<מתודה>`

**אימות:** Bearer token בכותרת `Authorization`. אין צורך ב-`cid` (מזהה חברה).

```
POST https://api.icount.co.il/api/v3.php/<מודול>/<מתודה>
Authorization: Bearer YOUR_API_KEY
Content-Type: application/x-www-form-urlencoded
```

הגדר `ICOUNT_API_KEY` בקובץ `.env`. מצא את מפתח ה-API שלך ב-iCount תחת הגדרות ← API.

**מגבלת קצב:** 30 בקשות/דקה. כל התגובות הן JSON.

---

## מבנה ה-URL

כל הנקודות קצה עוקבות אחר התבנית: `/api/v3.php/<מודול>/<מתודה>`

| מודול | מתודות |
|-------|--------|
| `client` | `get_list`, `create`, `delete`, `info`, `update` |
| `doc` | `types`, `create`, `search`, `get` |
| `expense` | `types`, `search`, `create` |
| `supplier` | `get_list`, `add`, `info`, `update` |

---

## נקודות קצה עיקריות

### לקוחות

```
POST /client/get_list      → רשימת כל הלקוחות
POST /client/create        → יצירת לקוח חדש (דרוש: client_name)
POST /client/delete        → מחיקת לקוח (דרוש: client_id)
POST /client/info          → פרטי לקוח בודד (דרוש: client_id)
POST /client/update        → עדכון לקוח (דרוש: client_id + שדות)
```

**שדות יצירת לקוח:**
```
client_name       (חובה)
phone
mobile
email
address
city
zip
country           (ברירת מחדל: IL)
vat_id            (ת.ז. ישראלי)
custom_client_id  (לקישור למערכות חיצוניות — שמור כאן מזהה מהמערכת החיצונית)
notes
```

### מסמכים

```
POST /doc/types            → סוגי מסמכים זמינים
POST /doc/create           → יצירת מסמך (חשבונית, קבלה, וכו׳)
POST /doc/search           → חיפוש מסמכים לפי תאריך/לקוח/סוג
POST /doc/get              → קבלת מסמך בודד (דרוש: doc_id)
```

**סוגי מסמכים מאומתים:**

| doctype | עברית | שימוש |
|---------|-------|-------|
| `invrec` | חשבונית מס קבלה | חשבונית + קבלה (הנפוץ ביותר — לקוח משלם מיד) |
| `invoice` | חשבונית מס | חשבונית בלבד (תשלום יגיע לאחר מכן) |
| `receipt` | קבלה | קבלה בלבד (מול חשבונית קיימת) |
| `refund` | זיכוי | הערת זיכוי / החזר |
| `offer` | הצעת מחיר | הצעת מחיר |
| `order` | הזמנה | הזמנה |
| `delcert` | תעודת משלוח | תעודת משלוח |
| `deal` | עסקה | עסקה/טרנזקציה |
| `po` | הזמנת רכש | הזמנת רכש |

**פורמט בקשת doc/create (form-encoded, לא JSON):**
```
doctype=invrec
client_id=7                    # מועדף: שימוש בלקוח קיים
# או: client_name=ישראל ישראלי  # חלופה: יוצר לקוח זמני

doc_date=20260322              # פורמט YYYYMMDD (לא YYYY-MM-DD)
currency=NIS                   # NIS, USD, EUR, GBP וכו׳
vattype=1                      # ראה ערכי vattype למטה

# פריטי שורה — סימון אינדקס:
desc[0]=שירותי ייעוץ - מרץ
unitprice[0]=1000
quantity[0]=1

desc[1]=דמי רישום              # פריט שני אופציונלי
unitprice[1]=100
quantity[1]=1

comment=מנוי חודשי             # אופציונלי
```

**ערכי vattype:**
| vattype | משמעות |
|---------|--------|
| `0` | ברירת מחדל של החשבון |
| `1` | מע"מ רגיל (18% נכון ל-2025 בישראל) |
| `2` | פטור ממע"מ |

### הוצאות

```
POST /expense/types        → רשימת סוגי הוצאות
POST /expense/search       → חיפוש הוצאות (פרמטרים: start_date, end_date)
POST /expense/create       → תיעוד הוצאה
```

### ספקים

```
POST /supplier/get_list    → רשימת כל הספקים
POST /supplier/add         → הוספת ספק (פרמטרים: supplier_name, vat_id)
POST /supplier/info        → פרטי ספק (פרמטרים: supplier_id)
POST /supplier/update      → עדכון ספק
```

---

## טיפול בשגיאות

כל תגובה מכילה `"status": true/false`. תמיד בדוק לפני המשך:

```python
import requests

def icount_post(endpoint, data):
    resp = requests.post(
        f"https://api.icount.co.il/api/v3.php/{endpoint}",
        headers={"Authorization": f"Bearer {ICOUNT_API_KEY}"},
        data=data  # form-encoded, לא json=
    )
    result = resp.json()
    if not result.get("status"):
        raise Exception(f"iCount [{result.get('reason')}]: {result.get('error_description', '')}")
    return result
```

ערכי `reason` נפוצים: `auth_required`, `bad_method`, `bad_doctype`, `missing_client_name`, `required_parameters_missing`, `client_deleted`.

---

## דוגמאות Python

### יצירת לקוח

```python
result = icount_post("client/create", {
    "client_name": "משה כהן",
    "phone": "050-1234567",
    "email": "moshe@example.com",
    "custom_client_id": "מזהה_מהמערכת_החיצונית"  # אופציונלי
})
client_id = result["client_id"]
```

### יצירת חשבונית מס קבלה (הנפוץ ביותר)

```python
import datetime

result = icount_post("doc/create", {
    "doctype": "invrec",
    "client_id": client_id,
    "doc_date": datetime.date.today().strftime("%Y%m%d"),
    "vattype": 1,
    "desc[0]": "שירותי ייעוץ - מרץ",
    "unitprice[0]": 1000,
    "quantity[0]": 1,
    "comment": "מנוי חודשי",
})
doc_id = result["doc_id"]
```

### חיפוש מסמכים אחרונים

```python
results = icount_post("doc/search", {
    "start_date": "20260101",
    "end_date": "20260331",
})
for doc in results.get("results_list", []):
    print(doc["doc_id"], doc["client_name"], doc["total"])
```

---

## דפוס סנכרון עם מערכות חיצוניות

שדה `custom_client_id` ב-iCount משמש כגשר לסנכרון עם מערכות חיצוניות (CRM, כלי ניהול פרויקטים וכו׳):

```
כשלקוח חדש נוסף במערכת החיצונית:
  1. POST /client/create → { client_name, phone, email, custom_client_id: <מזהה_חיצוני> }
  2. שמור את client_id שהוחזר בחזרה במערכת החיצונית

כשאירוע חיוב חוזר מופעל (למשל טריגר n8n/webhook):
  1. חפש client_id של iCount מהשדה "iCount ID" במערכת החיצונית
  2. POST /doc/create → { doctype: "invrec", client_id: ..., items: [...] }

כשתשלום מאושר ב-iCount:
  1. Webhook או פולינג על /doc/search למסמכים ששולמו
  2. עדכן את הרשומה המתאימה במערכת החיצונית
```

---

## סקריפטים

שני סקריפטי עזר מצורפים בתיקיית `scripts/`:

- **`scripts/test_connection.py`** — מאמת שמפתח ה-API תקין, מדפיס מספר לקוחות וסוגי מסמכים. הרץ אותו ראשון לאימות ההגדרה.
- **`scripts/list_doctypes.py`** — מושך את רשימת סוגי המסמכים הזמינים בחשבון שלך ומדפיס אותה בטבלה.

שניהם דורשים `pip install requests` ו-`ICOUNT_API_KEY` מוגדר בסביבה או בקובץ `.env`.

---

## הערות חשובות

- כל הסכומים הם בשקלים (₪) כברירת מחדל
- **פורמט תאריך:** `YYYYMMDD` (למשל `20260322`) — לא `YYYY-MM-DD`
- **גוף הבקשה:** תמיד form-encoded (`data=...`), לא JSON (`json=...`)
- לערכי שדה בעברית, ודא קידוד UTF-8
- ה-API כלול בכל מנויי iCount
- נקודת הקצה `doc/types` נותנת את הרשימה החיה לחשבון שלך — קרא אותה כדי לגלות סוגים ייחודיים לחשבון
