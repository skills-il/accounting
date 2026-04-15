---
name: hashavshevet-data-tools
description: >-
  ייבוא וייצוא נתונים בין תוכנת חשבשבת לפורמטים מודרניים (JSON, CSV, Excel).
  Use when צריך לחלץ פקודות יומן, מטקונת חשבונות, מאזן בוחן או רשימות לקוחות/ספקים
  מחשבשבת, לייבא תנועות בנק וחשבוניות לפורמט חשבשבת, להעביר נתונים מחשבשבת למערכות
  ענן (iCount, רווחית, Invoice4U), או לטפל בהמרות קידוד עברית (Windows-1255 ל-UTF-8).
  תומך בחשבשבת גולד, חשבשבת 2000+ וגרסאות חדשות יותר. מאמת שלמות נתונים בפעולות
  ייבוא/ייצוא. Do NOT use for אינטגרציות API בזמן אמת עם חשבשבת, שינויים ישירים
  בבסיס הנתונים, או הנהלת חשבונות שוטפת בתוך חשבשבת.
license: MIT
allowed-tools: "Bash(python:*) Read Edit Write"
compatibility: "דורש Python 3.9+ עם ספריות openpyxl ו-chardet"
metadata:
  author: skills-il
  version: 1.0.0
  category: accounting
  tags:
    he:
      - חשבשבת
      - העברת-נתונים
      - ייבוא-ייצוא
      - תוכנת-הנהלת-חשבונות
      - אינטגרציה
      - חשבונאות
    en:
      - hashavshevet
      - data-migration
      - import-export
      - accounting-software
      - integration
      - accounting
  display_name:
    he: "כלי נתונים לחשבשבת"
    en: "Hashavshevet Data Tools"
  display_description:
    he: "ייבוא וייצוא נתונים בין תוכנת חשבשבת לפורמטים מודרניים כמו JSON, CSV ו-Excel, כולל המרת קידוד עברית והעברת נתונים למערכות ענן"
    en: "Import and export data between Hashavshevet accounting software and modern formats like JSON, CSV, and Excel, including Hebrew encoding conversion and cloud migration"
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
---

# כלי נתונים לחשבשבת

## הוראות

### שלב 1: זיהוי גרסת חשבשבת ופורמט הקבצים

יש לזהות באיזו גרסה של חשבשבת המשתמש עובד ולזהות את פורמטי הקבצים הרלוונטיים:

- **חשבשבת גולד**: משתמשת בפורמט בינארי קנייני `.hsh` וייצוא טקסט ברוחב קבוע (`.dat`, `.txt`)
- **חשבשבת 2000+**: משתמשת בבסיסי נתונים `.mdb` (Access) או `.accdb`, עם יכולת ייצוא ל-CSV/רוחב קבוע
- **גרסאות חדשות**: תומכות בייצוא ישיר ל-CSV ו-XML דרך אשפי ייצוא מובנים

קבצי נתונים נפוצים של חשבשבת:

| קובץ / טבלה | שם עברי | תיאור | פורמט אופייני |
|---|---|---|---|
| `HESHIN.dat` | מאזן חשבונות | מטקונת חשבונות | רוחב קבוע, Windows-1255 |
| `PKUDOT.dat` | פקודות יומן | פקודות יומן | רוחב קבוע, Windows-1255 |
| `MANOT.dat` | מנות | מנות | רוחב קבוע, Windows-1255 |
| `KARTIS.dat` | כרטיסי חשבון | כרטיסי חשבון / ספר חשבונות | רוחב קבוע, Windows-1255 |
| `HESHBON.dat` | חשבונות | רשימת חשבונות ראשית | רוחב קבוע, Windows-1255 |
| `MATZAV.dat` | מצב חשבון | יתרות חשבונות | רוחב קבוע, Windows-1255 |
| `TNUOT.dat` | תנועות | תנועות | רוחב קבוע, Windows-1255 |

### שלב 2: טיפול בקידוד עברית

קבצי חשבשבת משתמשים בדרך כלל בקידוד Windows-1255 (עברית). יש להמיר ל-UTF-8 לפני עיבוד:

```python
import chardet

def detect_and_convert(file_path: str) -> str:
    """זיהוי קידוד והמרת קובץ חשבשבת ל-UTF-8."""
    with open(file_path, 'rb') as f:
        raw_data = f.read()

    detected = chardet.detect(raw_data)
    encoding = detected['encoding']

    # חשבשבת כמעט תמיד משתמשת ב-Windows-1255
    if encoding and encoding.lower() in ('windows-1255', 'iso-8859-8', 'hebrew'):
        encoding = 'windows-1255'
    elif encoding is None:
        encoding = 'windows-1255'  # ברירת מחדל בטוחה לנתוני הנהלת חשבונות בעברית

    return raw_data.decode(encoding, errors='replace')
```

מלכודות קידוד נפוצות:
- חשבשבת גולד תמיד משתמשת ב-Windows-1255
- חלק מהייצואים עשויים להשתמש ב-ISO-8859-8 (עברית חזותית) במקום עברית לוגית
- קבצים עם קידוד מעורב מתרחשים כאשר נתונים הועתקו ממקורות אחרים
- BOM (סימן סדר בתים) עשוי להיות נוכח בייצואי CSV חדשים יותר

### שלב 3: פענוח קבצי נתונים ברוחב קבוע של חשבשבת

קבצי `.dat` של חשבשבת משתמשים בפריסת עמודות ברוחב קבוע. רוחב העמודות משתנה לפי סוג הקובץ:

```python
# פריסת עמודות HESHIN.dat (מטקונת חשבונות)
HESHIN_COLUMNS = {
    'account_number': (0, 15),     # מספר חשבון
    'account_name': (15, 65),      # שם חשבון
    'account_type': (65, 67),      # סוג חשבון (1=נכס, 2=התחייבות, 3=הון, 4=הכנסה, 5=הוצאה)
    'parent_account': (67, 82),    # חשבון אב
    'sort_code': (82, 92),         # קוד מיון
    'is_active': (92, 93),         # פעיל (1=כן, 0=לא)
    'opening_balance': (93, 113),  # יתרת פתיחה
    'currency': (113, 116),        # מטבע
}

# פריסת עמודות PKUDOT.dat (פקודות יומן)
PKUDOT_COLUMNS = {
    'entry_number': (0, 10),       # מספר פקודה
    'batch_number': (10, 18),      # מספר מנה
    'entry_date': (18, 28),        # תאריך (DD/MM/YYYY)
    'account_debit': (28, 43),     # חשבון חובה
    'account_credit': (43, 58),    # חשבון זכות
    'amount': (58, 73),            # סכום
    'currency': (73, 76),          # מטבע
    'reference': (76, 96),         # אסמכתא
    'description': (96, 146),      # תיאור
    'value_date': (146, 156),      # תאריך ערך
}
```

פענוח הקבצים באמצעות מיקומי העמודות:

```python
def parse_fixed_width(content: str, columns: dict) -> list[dict]:
    """פענוח קובץ נתונים ברוחב קבוע של חשבשבת."""
    records = []
    for line in content.strip().split('\n'):
        if not line.strip():
            continue
        record = {}
        for field_name, (start, end) in columns.items():
            value = line[start:end].strip() if len(line) > start else ''
            record[field_name] = value
        records.append(record)
    return records
```

### שלב 4: ייצוא נתונים לפורמטים מודרניים

המרת נתונים מפוענחים של חשבשבת ל-JSON, CSV או Excel:

```python
import csv
import json

def export_to_csv(records: list[dict], output_path: str):
    """ייצוא רשומות מפוענחות ל-CSV בקידוד UTF-8 עם BOM לתאימות Excel."""
    if not records:
        return
    with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

def export_to_json(records: list[dict], output_path: str):
    """ייצוא רשומות מפוענחות ל-JSON עם תמיכה בעברית."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

def export_to_excel(records: list[dict], output_path: str, sheet_name: str = 'Data'):
    """ייצוא רשומות מפוענחות ל-Excel עם עיצוב RTL תקין."""
    from openpyxl import Workbook
    from openpyxl.worksheet.properties import WorksheetProperties

    wb = Workbook()
    ws = wb.active
    ws.title = sheet_name
    ws.sheet_properties = WorksheetProperties(rightToLeft=True)

    # כתיבת כותרות
    headers = list(records[0].keys())
    for col, header in enumerate(headers, 1):
        ws.cell(row=1, column=col, value=header)

    # כתיבת נתונים
    for row_idx, record in enumerate(records, 2):
        for col_idx, header in enumerate(headers, 1):
            ws.cell(row=row_idx, column=col_idx, value=record.get(header, ''))

    wb.save(output_path)
```

### שלב 5: ייבוא נתונים לפורמט חשבשבת

בעת ייבוא נתונים לחשבשבת, יש ליצור קבצים ברוחב קבוע התואמים את הפריסה הצפויה:

```python
def generate_hashavshevet_import(records: list[dict], columns: dict, output_path: str):
    """יצירת קובץ ברוחב קבוע לייבוא לחשבשבת."""
    lines = []
    for record in records:
        line = ''
        sorted_cols = sorted(columns.items(), key=lambda x: x[1][0])
        for field_name, (start, width_end) in sorted_cols:
            width = width_end - start
            value = str(record.get(field_name, ''))
            # ריפוד או חיתוך לרוחב מדויק
            if len(value) > width:
                value = value[:width]
            else:
                value = value.ljust(width)
            line += value
        lines.append(line)

    with open(output_path, 'w', encoding='windows-1255', errors='replace') as f:
        f.write('\n'.join(lines))
```

כללי אימות ייבוא:
- מספרי חשבון חייבים להתקיים במטקונת החשבונות
- תאריכים חייבים להיות בפורמט DD/MM/YYYY (פורמט תאריך ישראלי)
- סכומים חייבים להשתמש בנקודה כמפריד עשרוני (לא פסיק)
- חשבון חובה וחשבון זכות לא יכולים להיות זהים
- מספרי מנות חייבים להיות רציפים בתוך שנת מס
- קודי מטבע חייבים להתאים לקודים הפנימיים של חשבשבת (ILS=1, USD=2, EUR=3)

### שלב 6: העברת נתונים למערכות ענן

בעת מעבר מחשבשבת לפתרונות הנהלת חשבונות מבוססי ענן:

**מעבר ל-iCount:**
- ייצוא מטקונת חשבונות, ואז מיפוי מספרי חשבון לקטגוריות iCount
- ייצוא חשבוניות פתוחות ויתרות לקוחות/ספקים
- iCount מקבלת ייבוא CSV עם כותרות עמודות ספציפיות

**מעבר לרווחית:**
- ייצוא יומן מלא לשנת המס הנוכחית
- מיפוי סוגי חשבון של חשבשבת לסיווג החשבונות של רווחית
- רווחית מקבלת ייבוא Excel עם תבניות מוגדרות מראש

**מעבר ל-Invoice4U:**
- התמקדות בנתוני לקוחות/ספקים ויתרות פתוחות
- ייצוא היסטוריית חשבוניות לעיון (Invoice4U לא מייבאת יומנים היסטוריים)
- שימוש ב-API של Invoice4U לייבוא נתונים תכנותי

### שלב 7: אימות שלמות נתונים

לאחר כל פעולת ייבוא או ייצוא, יש לאמת את שלמות הנתונים:

```python
def validate_trial_balance(records: list[dict]) -> dict:
    """אימות שחובות שווים לזכויות בפקודות יומן."""
    total_debit = 0
    total_credit = 0
    errors = []

    for i, record in enumerate(records):
        try:
            amount = float(record.get('amount', 0))
            if record.get('account_debit'):
                total_debit += amount
            if record.get('account_credit'):
                total_credit += amount
        except ValueError:
            errors.append(f"שורה {i+1}: סכום לא תקין '{record.get('amount')}'")

    balanced = abs(total_debit - total_credit) < 0.01
    return {
        'balanced': balanced,
        'total_debit': round(total_debit, 2),
        'total_credit': round(total_credit, 2),
        'difference': round(total_debit - total_credit, 2),
        'errors': errors,
    }

def validate_account_references(entries: list[dict], accounts: list[dict]) -> list[str]:
    """אימות שכל החשבונות המוזכרים קיימים במטקונת החשבונות."""
    valid_accounts = {a['account_number'] for a in accounts}
    errors = []
    for i, entry in enumerate(entries):
        debit_acc = entry.get('account_debit', '').strip()
        credit_acc = entry.get('account_credit', '').strip()
        if debit_acc and debit_acc not in valid_accounts:
            errors.append(f"שורה {i+1}: חשבון חובה '{debit_acc}' לא נמצא במטקונת החשבונות")
        if credit_acc and credit_acc not in valid_accounts:
            errors.append(f"שורה {i+1}: חשבון זכות '{credit_acc}' לא נמצא במטקונת החשבונות")
    return errors
```

## דוגמאות

### דוגמה 1: ייצוא פקודות יומן מחשבשבת ל-Excel

המשתמש אומר: "יש לי קובץ PKUDOT.dat מחשבשבת גולד. אני צריך לייצא את כל פקודות היומן מ-2025 לקובץ Excel עבור רואה החשבון שלי."

פעולות:
1. קריאת קובץ `PKUDOT.dat` וזיהוי קידוד (Windows-1255)
2. המרת תוכן מ-Windows-1255 ל-UTF-8
3. פענוח הנתונים ברוחב קבוע באמצעות פריסת העמודות של PKUDOT
4. סינון רשומות שבהן `entry_date` נופל בטווח 01/01/2025 עד 31/12/2025
5. ייצוא רשומות מסוננות ל-Excel עם עיצוב RTL וכותרות עמודות בעברית
6. אימות שסך החובות שווה לסך הזכויות בנתונים המיוצאים

תוצאה: קובץ Excel `pkudot_2025.xlsx` עם כל פקודות היומן של 2025, מעוצב כראוי עם כותרות בעברית, כיוון גיליון RTL, וסיכום אימות המאשר שמאזן הבוחן מאוזן.

### דוגמה 2: ייבוא תנועות בנק לפורמט חשבשבת

המשתמש אומר: "הורדתי תנועות בנק מלאומי כ-CSV. אני צריך להמיר אותן לפורמט שאפשר לייבא לחשבשבת 2000+."

פעולות:
1. קריאת קובץ CSV של בנק לאומי (UTF-8 עם BOM)
2. מיפוי עמודות CSV של הבנק לשדות PKUDOT של חשבשבת: תאריך ל-`entry_date`, תיאור ל-`description`, סכום ל-`amount`, מספר אסמכתא ל-`reference`
3. הקצאת חשבונות חובה/זכות על פי כיוון התנועה (חיובי = חובה חשבון בנק / זכות הכנסה, שלילי = זכות חשבון בנק / חובה הוצאה)
4. יצירת מספרי פקודה רציפים והקצאה למנה הנוכחית
5. המרת תאריכים מפורמט YYYY-MM-DD (פורמט בנק) ל-DD/MM/YYYY (פורמט חשבשבת)
6. כתיבת הפלט כקובץ `.dat` ברוחב קבוע בקידוד Windows-1255
7. אימות שלמות כל הרשומות שנוצרו

תוצאה: קובץ `bank_import.dat` מוכן לייבוא לחשבשבת 2000+, עם 47 תנועות מעוצבות כראוי, מקודדות ב-Windows-1255 ומאומתות.

### דוגמה 3: העברת מטקונת חשבונות מחשבשבת לרווחית

המשתמש אומר: "אנחנו עוברים מחשבשבת גולד לרווחית. אני צריך לייצא את מטקונת החשבונות ויתרות הפתיחה שלנו בפורמט שרווחית יכולה לייבא."

פעולות:
1. קריאה ופענוח `HESHIN.dat` (מטקונת חשבונות) ו-`MATZAV.dat` (יתרות חשבונות) מחשבשבת
2. המרת קידוד מ-Windows-1255 ל-UTF-8
3. מיפוי סוגי חשבון של חשבשבת (1-5) לסיווגי חשבון של רווחית
4. מיזוג יתרות חשבון עם נתוני החשבון הראשיים
5. יצירת תבנית Excel תואמת רווחית עם עמודות: מספר חשבון, שם חשבון, סוג חשבון, יתרת פתיחה, מטבע
6. יישום כללי שמות ואימות של רווחית
7. יצירת מסמך מיפוי התייחסות המציג מספרי חשבון ישנים של חשבשבת לצד מזהי חשבון חדשים של רווחית

תוצאה: קובץ ייבוא Excel תואם רווחית עם 234 חשבונות, מסמך מיפוי התייחסות, וסיכום של 12 חשבונות הדורשים בדיקה ידנית עקב הבדלים בסיווג סוגי חשבון.

## משאבים מצורפים

### סקריפטים
- `scripts/encoding_converter.py` -- המרה אצוותית של קבצי חשבשבת מ-Windows-1255 ל-UTF-8. הרצה: `python scripts/encoding_converter.py --help`
- `scripts/dat_parser.py` -- פענוח קבצי .dat ברוחב קבוע של חשבשבת ל-JSON/CSV. הרצה: `python scripts/dat_parser.py --help`

### הפניות
- `references/hashavshevet-file-formats.md` -- פריסות עמודות מפורטות לכל סוגי קבצי .dat של חשבשבת. יש לעיין כאשר נתקלים בסוג קובץ לא מוכר או כשמיקומי עמודות נראים שגויים.
- `references/cloud-migration-mappings.md` -- מיפויי סוגי חשבון ושדות למעברים ל-iCount, רווחית ו-Invoice4U. יש לעיין בעת תכנון מעבר לפתרון מבוסס ענן.

## מלכודות נפוצות

- קבצי חשבשבת משתמשים בקידוד Windows-1255, לא UTF-8. סוכנים כמעט תמיד ינסו לקרוא את הקבצים כ-UTF-8, מה שיגרום ל-UnicodeDecodeError על התו העברי הראשון.
- פורמט התאריך בחשבשבת הוא DD/MM/YYYY (סטנדרט ישראלי). ייצואי בנק עשויים להשתמש ב-YYYY-MM-DD (ISO) או MM/DD/YYYY (ארה"ב). סוכנים עלולים לא לזהות אי-התאמת הפורמט.
- מיקומי עמודות ברוחב קבוע שונים בין גרסאות חשבשבת (גולד מול 2000+ מול חדשות יותר). סוכנים עלולים להחיל פריסת עמודות של גרסה אחת על נתונים מגרסה אחרת.
- קודי מטבע פנימיים בחשבשבת שונים מקודי ISO: ILS=1, USD=2, EUR=3. סוכנים עלולים להשתמש בקודי ISO 4217, שחשבשבת לא תזהה בייבוא.
- בייצוא ל-CSV עבור Excel, קבצים חייבים להיות בקידוד UTF-8 עם BOM (utf-8-sig). בלי BOM, Excel לא יציג תווים עבריים כראוי ויראה ג'יבריש.


## קישורי עזר

| מקור | כתובת | מה לבדוק |
|------|-------|----------|
| חשבשבת H-ERP אתר רשמי | https://www.h-erp.co.il | גרסאות חשבשבת, מדריכי פורמט קבצים |
| רשות המסים | https://www.gov.il/he/departments/israel_tax_authority | הוראות ניהול ספרים ממוחשב, שדות חובה ביומן |
| תיעוד openpyxl | https://openpyxl.readthedocs.io/en/stable/ | כתיבת XLSX מפייתון, ייצוא עם עיצוב |
| pandas I/O reference | https://pandas.pydata.org/docs/reference/io.html | ייבוא וייצוא CSV/Excel, טיפול בקידוד |
| טבלת קידוד CP1255 (unicode.org) | https://unicode.org/Public/MAPPINGS/VENDORS/MICSFT/WINDOWS/CP1255.TXT | מיפוי תווי עברית Windows-1255 ל-UTF-8 |

## פתרון בעיות

### שגיאה: "UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9"
סיבה: הקובץ מקודד ב-Windows-1255 (עברית) אך נקרא כ-UTF-8. זוהי השגיאה הנפוצה ביותר בעבודה עם קבצי חשבשבת, מכיוון שהתוכנה משתמשת ב-Windows-1255 כברירת מחדל.
פתרון: יש לציין במפורש `encoding='windows-1255'` בעת קריאת הקובץ. אם לא בטוחים לגבי הקידוד, יש להשתמש בספריית `chardet` לזיהוי אוטומטי. עבור קבצים עם קידוד מעורב, יש להשתמש ב-`errors='replace'` להחלפת תווים שלא ניתן לפענח.

### שגיאה: "מאזן הבוחן לא מאוזן (הפרש: X.XX)"
סיבה: הפרשי עיגול מהמרות מטבע, ייצואים חלקיים (פקודות חסרות ממנה), או נתונים פגומים בקובץ המקור. חשבשבת לפעמים מאחסנת סכומים עם ספרות עשרוניות נוספות באופן פנימי.
פתרון: ראשית יש לבדוק אם ההפרש הוא שגיאת עיגול קטנה (פחות מ-1 ש"ח). אם כן, יש ליצור פקודת התאמה. להפרשים גדולים יותר, יש לוודא שהייצוא כולל את כל המנות לתקופה. יש לייצא מחדש מחשבשבת באמצעות אפשרות "ייצוא מלא" במקום ייצוא מסונן.

### שגיאה: "מספר חשבון לא נמצא במטקונת החשבונות"
סיבה: פקודות יומן מתייחסות לחשבונות שנמחקו או שונה מספרם בחשבשבת, או שייצוא מטקונת החשבונות הוא משנת מס שונה מפקודות היומן.
פתרון: יש לייצא הן את מטקונת החשבונות והן את פקודות היומן מאותו בסיס נתונים ושנת מס בחשבשבת. אם חשבונות מוספרו מחדש, יש ליצור טבלת מיפוי ולעדכן הפניות לפני הייבוא. יש לבדוק אם אפסים מובילים הוסרו במהלך ההמרה.

### שגיאה: "אי-התאמה בפורמט תאריך בעת ייבוא"
סיבה: חשבשבת מצפה ל-DD/MM/YYYY (פורמט ישראלי) אך נתוני המקור משתמשים ב-MM/DD/YYYY (פורמט אמריקאי) או YYYY-MM-DD (פורמט ISO). זה קורה בדרך כלל בעת ייבוא נתוני בנק או נתונים ממערכות בינלאומיות.
פתרון: יש לנרמל את כל התאריכים ל-DD/MM/YYYY לפני יצירת קובץ הייבוא. יש לבדוק תאריכים דו-משמעיים שבהם יום וחודש יכולים להתחלף (למשל, 03/04/2025 יכול להיות 3 באפריל או 4 במרץ) ולאמת מול פורמט מערכת המקור.
