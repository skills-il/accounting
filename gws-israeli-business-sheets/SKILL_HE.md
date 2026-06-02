---
name: gws-israeli-business-sheets
license: MIT
---

# גיליונות עסקיים ישראליים עם GWS

## הוראות

כלי ה-Google Workspace CLI (הפקודה `gws`, החבילה `@googleworkspace/cli`) בונה את מערך הפקודות שלו באופן דינמי מ-Discovery API של גוגל. כל קריאה ל-Sheets לובשת אחת משתי צורות:

צורה ראשונה, שיטות API גולמיות: `gws sheets spreadsheets <method> --params '<JSON>' [--json '<body JSON>']`. ה-JSON שב-`--params` נושא את פרמטרי הנתיב והשאילתה (`spreadsheetId`, `range`, `valueInputOption` וכדומה). הדגל `--json` נושא את גוף הבקשה לשיטות POST/PUT/PATCH.

צורה שנייה, קיצורי עזר: `gws sheets +read` ו-`gws sheets +append` עוטפים את הקריאות וההוספות הנפוצות ביותר בדגלים פשוטים.

דגלים גלובליים שימושיים: `--dry-run` (בדיקה מקומית, בלי קריאה ל-API), `--format json|table|yaml|csv` (פורמט פלט, ברירת מחדל `json`). כשלא בטוחים לגבי הפרמטרים המדויקים של שיטה, תריצו `gws sheets --help`, `gws sheets spreadsheets --help`, או `gws schema sheets.spreadsheets.values.append`.

### שלב 1: התקנה ואימות של GWS CLI

לפני שעושים פעולות בגיליונות Google, תוודאו ש-Google Workspace CLI מותקן ושאתם מחוברים.

```bash
# בדיקה אם gws מותקן
gws --version

# אם לא מותקן, התקנה גלובלית
npm install -g @googleworkspace/cli

# אימות מול Google OAuth
gws auth login

# בדיקת סטטוס ההתחברות
gws auth status
```

אם המשתמש לא הגדיר אישורי OAuth, הובילו אותו דרך `gws auth login` עם פרויקט Google Cloud שבו ה-Sheets API מופעל. אפשרויות נוספות לאישורים נמצאות ב-`gws auth --help`.

### שלב 2: בירור מעמד המע"מ של המשתמש

לפני שבונים גיליון, תשאלו אם המשתמש הוא **עוסק מורשה** (גובה ומקזז מע"מ) או **עוסק פטור** (לא גובה ולא מקזז מע"מ). זה משנה את מבנה הגיליון:

עוסק מורשה: כוללים את עמודות המע"מ המלאות (נטו, מע"מ, סה"כ) ומחשבים חבות מע"מ.

עוסק פטור: עוסק פטור לא גובה מע"מ על הכנסות ולא יכול לקזז מע"מ תשומות על הוצאות. תורידו את עמודת המע"מ לגמרי (או תשאירו אותה 0), תרשמו סכומים ברוטו בלבד, ותדלגו על חישוב חבות המע"מ. עוסק פטור עדיין עוקב אחרי הכנסות והוצאות לצורך הדוח השנתי למס הכנסה.

עוסק פטור שמחזור ההכנסות השנתי שלו חוצה את התקרה (120,000 ש"ח ל-2025, 122,833 ש"ח ל-2026) חייב לעבור לעוסק מורשה. אם משתמש קרוב לתקרה, תסבו את תשומת לבו לכך.

### שלב 3: יצירת גיליון מעקב פיננסי חדש

כשהמשתמש רוצה להקים גיליון מעקב הכנסות/הוצאות חדש, תיצרו אותו עם מבנה פיננסי ישראלי תקין.

**מבנה הגיליון לעוסק מורשה:**

| עמודה | כותרת (EN) | כותרת (HE) | פורמט | ייעוד |
|-------|------------|-------------|-------|-------|
| A | Date | תאריך | DD/MM/YYYY | תאריך העסקה |
| B | Description | תיאור | טקסט | מהות העסקה |
| C | Category | קטגוריה | טקסט | קטגוריית ניכוי מס |
| D | Amount (excl. VAT) | סכום (ללא מע"מ) | מטבע ILS | סכום נטו |
| E | VAT (18%) | מע"מ (18%) | מטבע ILS | מע"מ מחושב |
| F | Total (incl. VAT) | סכום כולל מע"מ | מטבע ILS | סכום ברוטו |
| G | Type | סוג | הכנסה/הוצאה | כיוון הכסף |
| H | Invoice # | מספר חשבונית | טקסט | הפניה לחשבונית |
| I | Payment Method | אמצעי תשלום | טקסט | בנק/PayPal/מזומן |
| J | Notes | הערות | טקסט | פרטים נוספים |

לעוסק פטור, תורידו את עמודות D ו-E ותשנו את שם עמודה F ל-`Amount` / `סכום` (ברוטו בלבד), כי אין מע"מ.

**קטגוריות ניכוי מס לעסקים ישראליים:**

| קטגוריה (EN) | קטגוריה (HE) | שיעור ניכוי |
|---------------|---------------|-------------|
| Office Rent | שכירות משרד | 100% |
| Equipment | ציוד | 100% |
| Phone & Internet | טלפון ואינטרנט | 100% (אם לשימוש עסקי בלבד) |
| Professional Services | שירותים מקצועיים | 100% |
| Car Expenses | הוצאות רכב | מוגבל (45% או קבוע) |
| Meals & Entertainment | ארוחות ואירוח | 80% |
| Travel | נסיעות | 100% |
| Software & Subscriptions | תוכנה ומנויים | 100% |
| Marketing | שיווק | 100% |
| Insurance | ביטוח | 100% |

יצירת הגיליון וכתיבת שורת הכותרות:

```bash
# יצירת גיליון חדש (תגובת ה-JSON כוללת את "spreadsheetId")
gws sheets spreadsheets create --json '{"properties":{"title":"Business Tracker 2026"}}'

# כתיבת שורת הכותרות לשורה הראשונה (השתמשו ב-spreadsheetId מתגובת היצירה)
gws sheets spreadsheets values update \
  --params '{"spreadsheetId":"SPREADSHEET_ID","range":"Sheet1!A1:J1","valueInputOption":"RAW"}' \
  --json '{"values":[["Date","Description","Category","Amount (excl. VAT)","VAT (18%)","Total (incl. VAT)","Type","Invoice #","Payment Method","Notes"]]}'
```

### שלב 4: הוספת רשומות הכנסה והוצאה

כשהמשתמש רוצה לרשום עסקה, תחשבו את המע"מ אוטומטית (לעוסק מורשה בלבד) ותוסיפו את השורה.

**לרשומות הכנסה (המשתמש קיבל תשלום):**

```bash
# חישוב: אם המשתמש קיבל 5,900 ש"ח סה"כ, הפירוט הוא:
# סכום ללא מע"מ = סה"כ / 1.18 = 5,000 ש"ח
# מע"מ = סכום * 0.18 = 900 ש"ח
gws sheets spreadsheets values append \
  --params '{"spreadsheetId":"SPREADSHEET_ID","range":"Sheet1!A:J","valueInputOption":"USER_ENTERED"}' \
  --json '{"values":[["15/01/2026","Web Development Project","Professional Services","5000","900","5900","Income","INV-2026-001","Bank Transfer",""]]}'
```

קיצור העזר `+append` הוא מקבילה קצרה יותר לשורה בודדת ופשוטה:

```bash
gws sheets +append --spreadsheet SPREADSHEET_ID \
  --json-values '[["15/01/2026","Web Development Project","Professional Services","5000","900","5900","Income","INV-2026-001","Bank Transfer",""]]'
```

**לרשומות הוצאה:**

```bash
# דוגמה: חשבון אינטרנט בזק של 236 ש"ח (200 + 36 מע"מ)
gws sheets spreadsheets values append \
  --params '{"spreadsheetId":"SPREADSHEET_ID","range":"Sheet1!A:J","valueInputOption":"USER_ENTERED"}' \
  --json '{"values":[["20/01/2026","Bezeq Internet","Phone & Internet","200","36","236","Expense","","Direct Debit",""]]}'
```

**נוסחאות חישוב מע"מ (לעוסק מורשה בלבד):**

| תרחיש | נוסחה | דוגמה |
|--------|-------|-------|
| יש סכום כולל מע"מ, צריך פירוט | סכום = סה"כ / 1.18, מע"מ = סה"כ - סכום | 1180 / 1.18 = 1000, מע"מ = 180 |
| יש סכום נטו, צריך סה"כ | מע"מ = סכום * 0.18, סה"כ = סכום + מע"מ | 1000 * 0.18 = 180, סה"כ = 1180 |
| הוצאת ארוחה (80% מוכר) | מוכר = סכום * 0.80 | 500 * 0.80 = 400 |

### שלב 5: קריאה וסיכום של נתונים פיננסיים

כשהמשתמש צריך סקירה פיננסית, תקראו את הנתונים ותחשבו סיכומים.

```bash
# קריאת כל הרשומות מהגיליון עם קיצור העזר (מחזיר את מערך הערכים הגולמי)
gws sheets +read --spreadsheet SPREADSHEET_ID --range "Sheet1!A:J"

# קריאת API גולמית מקבילה (התגובה היא ValueRange עם שדה "values" שהוא מערך של מערכים)
gws sheets spreadsheets values get --params '{"spreadsheetId":"SPREADSHEET_ID","range":"Sheet1!A:J"}'
```

שתי הצורות מחזירות JSON עם שדה `values`: מערך של שורות, כל שורה היא מערך של מחרוזות תאים. השורה הראשונה היא הכותרת. אחרי שקראתם את הנתונים, תחשבו ותציגו:
- סה"כ הכנסות לתקופה
- סה"כ הוצאות לתקופה
- רווח נקי (הכנסות פחות הוצאות)
- סה"כ מע"מ שנגבה (על הכנסות) - לעוסק מורשה בלבד
- סה"כ מע"מ ששולם (על הוצאות, מע"מ תשומות) - לעוסק מורשה בלבד
- חבות מע"מ (נגבה פחות ששולם, הסכום לדיווח לרשות המיסים) - לעוסק מורשה בלבד

לעוסק פטור, תציגו הכנסות, הוצאות ורווח נקי בלבד.

**תקופות דיווח מע"מ דו-חודשיות (ישראל):**

| תקופה | חודשים | מועד אחרון לדיווח |
|--------|--------|-------------------|
| 1 | ינואר-פברואר | 15 במרץ |
| 2 | מרץ-אפריל | 15 במאי |
| 3 | מאי-יוני | 15 ביולי |
| 4 | יולי-אוגוסט | 15 בספטמבר |
| 5 | ספטמבר-אוקטובר | 15 בנובמבר |
| 6 | נובמבר-דצמבר | 15 בינואר |

### שלב 6: הפקת דוחות סיכום לתקופות מס

כשהמשתמש צריך להכין נתונים לרואה החשבון או לדיווח מע"מ, תיצרו גיליון סיכום.

```bash
# קריאת כל הנתונים
gws sheets +read --spreadsheet SPREADSHEET_ID --range "Sheet1!A:J"
```

אחרי הקריאה, תשתמשו ב-Python (דרך `scripts/vat-summary.py`) כדי:
1. לסנן עסקאות לפי התקופה הדו-חודשית
2. לקבץ להכנסות מול הוצאות
3. לחשב סה"כ מע"מ שנגבה ומע"מ תשומות (לעוסק מורשה בלבד)
4. להפיק סיכום מותאם לרואה חשבון

אחר כך תכתבו את הסיכום ללשונית חדשה. קודם תוסיפו את הלשונית עם `batchUpdate`, ואז תכתבו את השורות:

```bash
# הוספת לשונית חדשה בשם "VAT-Period-1"
gws sheets spreadsheets batchUpdate \
  --params '{"spreadsheetId":"SPREADSHEET_ID"}' \
  --json '{"requests":[{"addSheet":{"properties":{"title":"VAT-Period-1"}}}]}'

# כתיבת כותרות ושורות הסיכום
gws sheets spreadsheets values update \
  --params '{"spreadsheetId":"SPREADSHEET_ID","range":"VAT-Period-1!A1:D1","valueInputOption":"RAW"}' \
  --json '{"values":[["Category","Total Amount","Total VAT","Transaction Count"]]}'

gws sheets spreadsheets values append \
  --params '{"spreadsheetId":"SPREADSHEET_ID","range":"VAT-Period-1!A:D","valueInputOption":"USER_ENTERED"}' \
  --json '{"values":[["Total Income","50000","9000","15"],["Total Expenses","20000","3600","25"],["VAT Liability","","5400",""],["Net Profit","30000","",""]]}'
```

### שלב 7: גיבוי גיליונות כ-CSV

כשהמשתמש רוצה גיבויים מקומיים או לשתף נתונים עם רואה החשבון, תייצאו ל-CSV עם הדגל `--format csv`.

```bash
# ייצוא גיליון המעקב הראשי כ-CSV
gws sheets spreadsheets values get \
  --params '{"spreadsheetId":"SPREADSHEET_ID","range":"Sheet1!A:J"}' --format csv > business-tracker-2026.csv

# ייצוא תקופת מע"מ ספציפית
gws sheets spreadsheets values get \
  --params '{"spreadsheetId":"SPREADSHEET_ID","range":"VAT-Period-1!A:D"}' --format csv > vat-period-1-2026.csv
```

אפשר להשתמש בסקריפט `scripts/backup-sheets.py` כדי לגבות כמה לשוניות אוטומטית:

```bash
python scripts/backup-sheets.py --spreadsheet-id SPREADSHEET_ID --output-dir ./backups/2026-01 --tabs "Sheet1,VAT-Period-1"
```

### שלב 8: רישום אוטומטי של תשלומים מקלט מובנה

כשהמשתמש נותן לכם נתוני עסקאות בכמות (דף חשבון בנק או רשימת חשבוניות), תנתחו ותוסיפו כמה שורות בקריאה אחת.

```bash
# הוספת כמה שורות בקריאה אחת
gws sheets spreadsheets values append \
  --params '{"spreadsheetId":"SPREADSHEET_ID","range":"Sheet1!A:J","valueInputOption":"USER_ENTERED"}' \
  --json '{"values":[
    ["01/02/2026","Client A - Monthly Retainer","Professional Services","10000","1800","11800","Income","INV-2026-010","Bank Transfer",""],
    ["03/02/2026","AWS Hosting","Software & Subscriptions","450","81","531","Expense","","Credit Card",""],
    ["05/02/2026","Business Lunch - Client B","Meals & Entertainment","300","54","354","Expense","","Credit Card","80% deductible"]
  ]}'
```

### שלב 9: שימוש ב-Dry-Run לאימות

לפני שמבצעים שינויים, תציעו למשתמש תצוגה מקדימה. הדגל `--dry-run` מאמת את הבקשה מקומית בלי לשלוח אותה ל-API.

```bash
# תצוגה מקדימה של מה שיתווסף בלי לכתוב בפועל
gws sheets spreadsheets values append \
  --params '{"spreadsheetId":"SPREADSHEET_ID","range":"Sheet1!A:J","valueInputOption":"USER_ENTERED"}' \
  --json '{"values":[["15/03/2026","Test Entry","Office Rent","5000","900","5900","Expense","","Bank Transfer",""]]}' \
  --dry-run
```

### שלב 10: הפקת חשבונית מס תקינה

כשהמשתמש צריך להפיק חשבונית מס ללקוח, הגיליון הוא רשומת המעקב, לא החשבונית החוקית. החשבונית החוקית עצמה מופקת בשירות חשבוניות (מורנינג, iCount, רווחית ודומיהם) או בתבנית מאושרת. חשבונית מס ישראלית תקינה חייבת לכלול:

- את הכותרת "חשבונית מס" ומספר חשבונית רץ
- את שם העסק של המוכר ואת מספר העוסק (מספר עוסק מורשה, או מספר עסק לעוסק פטור שמפיק חשבונית עסקה או קבלה)
- את שם הלקוח (ומספר זהות לחשבוניות מעל הסף)
- תאריך חשבונית
- תיאור, כמות ומחיר יחידה של הסחורה או השירות
- סכום לפני מע"מ, סכום המע"מ, וסה"כ כולל מע"מ (לעוסק מורשה). עוסק פטור מפיק קבלה או חשבונית עסקה בלי שורת מע"מ.

מספר הקצאה ומנדט החשבונית הדיגיטלית. מודל הבקרה הרציפה של ישראל מחייב מספר הקצאה מפלטפורמת רשות המיסים לחשבוניות מס מסכום סף ומעלה, לפני שהקונה יכול לקזז מע"מ תשומות. נכון ל-2026 הסף יורד בהדרגה: חשבוניות של 10,000 ש"ח ומעלה (לפני מע"מ) מ-1 בינואר 2026, ו-5,000 ש"ח ומעלה (לפני מע"מ) מ-1 ביוני 2026. כשרושמים חשבונית גדולה, תזכירו למשתמש להוציא את מספר ההקצאה דרך תוכנת החשבוניות שלו ולרשום אותו לצד מספר החשבונית.

## דוגמאות

### דוגמה 1: פרילנסר ישראלי מקים מעקב חודשי

המשתמש אומר: "תיצור לי גיליון Google למעקב הכנסות והוצאות עם מע"מ"

פעולות:
1. שאלו אם המשתמש הוא עוסק מורשה או עוסק פטור (זה קובע אם כוללים עמודות מע"מ)
2. הריצו `gws sheets spreadsheets create --json '{"properties":{"title":"Freelance Tracker 2026"}}'` וקראו את ה-`spreadsheetId` מהתגובה
3. כתבו את שורת הכותרות עם `gws sheets spreadsheets values update` (10 עמודות לעוסק מורשה, פחות לעוסק פטור)
4. הציגו למשתמש את מזהה הגיליון והקישור, והסבירו את מבנה העמודות

תוצאה: גיליון Google חדש עם המבנה הישראלי הנכון למעמד המע"מ של המשתמש, מוכן לרשומות.

### דוגמה 2: הפקת סיכום מע"מ דו-חודשי לרואה חשבון

המשתמש אומר: "תכין סיכום מע"מ לינואר-פברואר 2026 ותייצא כ-CSV"

פעולות:
1. הריצו `gws sheets +read --spreadsheet SPREADSHEET_ID --range "Sheet1!A:J"` כדי למשוך את כל הרשומות
2. הריצו `python scripts/vat-summary.py` כדי לסנן עסקאות ינואר-פברואר ולחשב סיכומים
3. הוסיפו לשונית "VAT-Period-1-2026" עם `gws sheets spreadsheets batchUpdate` וכתבו את הסיכום עם `gws sheets spreadsheets values update`
4. ייצאו את לשונית הסיכום עם `gws sheets spreadsheets values get --format csv`
5. הציגו את הסיכום: סה"כ הכנסות, סה"כ הוצאות, מע"מ שנגבה, מע"מ תשומות, חבות מע"מ נטו

תוצאה: סיכום תקופת מע"מ נקי, גם בגיליון Google וגם כקובץ CSV מקומי מוכן לשליחה לרואה החשבון.

### דוגמה 3: רישום אוטומטי של העברות בנקאיות לגיליון הוצאות

המשתמש אומר: "קיבלתי החודש תשלומים: לקוח א' שילם 11,800 על ייעוץ, שילמתי 531 על אחסון, ו-354 על ארוחה עסקית"

פעולות:
1. נתחו כל עסקה, חשבו את פירוט המע"מ (חלוקת סה"כ ב-1.18)
2. סווגו: ייעוץ = שירותים מקצועיים (הכנסה), אחסון = תוכנה ומנויים (הוצאה), ארוחה = ארוחות ואירוח (הוצאה, 80% מוכר)
3. השתמשו ב-`gws sheets spreadsheets values append` עם מערך `values` של כמה שורות ב-`--json`
4. אשרו שכל הרשומות נרשמו עם חישובי מע"מ נכונים

תוצאה: שלוש שורות חדשות נוספו לגיליון המעקב עם קטגוריזציה נכונה, פירוט מע"מ, והערות ניכוי.

## משאבים מצורפים

### סקריפטים
- `scripts/vat-summary.py` -- הפקת דוחות סיכום מע"מ דו-חודשיים מנתוני הגיליון. הרצה: `python scripts/vat-summary.py --help`
- `scripts/backup-sheets.py` -- גיבוי לשוניות Google Sheets כקבצי CSV מקומיים. הרצה: `python scripts/backup-sheets.py --help`

### מסמכי עזר
- `references/israeli-tax-categories.md` -- רשימה מלאה של קטגוריות הוצאות מוכרות למס בישראל עם שיעורי ניכוי, בתוספת כללי מע"מ ועוסק פטור/מורשה. פתחו אותו כשאתם מסווגים הוצאה עסקית או מאמתים עובדת מס.
- `references/gws-sheets-recipes.md` -- מתכונים נפוצים ל-gws CLI לפעולות Google Sheets. פתחו אותו כשאתם עושים פעולות גיליון מעבר לקריאה/הוספה בסיסית.

## מלכודות נפוצות

- תקופות דיווח מע"מ בישראל הן דו-חודשיות (כל חודשיים), לא רבעוניות כמו בהרבה מדינות אחרות. סוכנים עלולים לבנות סיכומים על בסיס רבעוני, וזה לא מתאים לדרישות רשות המיסים.
- פורמט התאריך הישראלי הוא DD/MM/YYYY, לא MM/DD/YYYY. סוכנים עלולים להשתמש בפורמט האמריקאי, וזה גורם לבלבול כשתאריכים כמו 03/04/2026 יכולים להיות 3 באפריל או 4 במרץ.
- עוסק פטור לא גובה מע"מ על הכנסות ולא יכול לקזז מע"מ תשומות על הוצאות. סוכנים עלולים להוסיף עמודות מע"מ ולחשב חבות מע"מ לעוסק פטור, וזה שגוי. תמיד תבררו קודם את מעמד המע"מ של המשתמש.
- הוצאות ארוחות ואירוח מוכרות רק ב-80% בישראל. סוכנים עלולים לסווג אותן כמוכרות ב-100%, וזה מנפח את ניכויי המס.
- להוצאות רכב יש כללי ניכוי מורכבים בישראל (45% או סכום חודשי קבוע, הנמוך מביניהם). סוכנים עלולים להחיל ניכוי של 100%, שיהיה שגוי לרוב העסקים.
- המע"מ בישראל הוא 18% (מאז ינואר 2025). סוכנים שאומנו על מידע ישן עלולים להשתמש ב-17%, שהיה השיעור הקודם, ולגרום לחישובים שגויים בכל הגיליון.
- מערך הפקודות של `gws` נבנה מ-Discovery API של גוגל. אין פקודה ברמה העליונה `gws sheets create` או `gws sheets read`. תשתמשו ב-`gws sheets spreadsheets <method>` עם `--params`/`--json`, או בקיצורי העזר `+read` / `+append`. כשלא בטוחים, תריצו `gws sheets --help`.


## קישורי עזר

| מקור | כתובת | מה לבדוק |
|------|-------|----------|
| Google Workspace CLI | https://github.com/googleworkspace/cli | מערך הפקודות האמיתי של gws, פקודות עזר, הגדרת אימות |
| Google Sheets API | https://developers.google.com/sheets/api | Sheets REST API, שיטות spreadsheets.values, batchUpdate |
| Google Apps Script | https://developers.google.com/apps-script | SpreadsheetApp API, פונקציות מותאמות, טריגרים |
| רשות המסים | https://www.gov.il/he/departments/israel_tax_authority | שיעור מע"מ נוכחי (18%), תקרת עוסק פטור, ספי מספר הקצאה, לוחות דיווח |
| בנק ישראל - שערי חליפין | https://www.boi.org.il/roles/markets/exchangerates/ | שערים יציגים יומיים, נתונים היסטוריים לדוחות |

## פתרון בעיות

### שגיאה: "gws: command not found"
סיבה: Google Workspace CLI לא מותקן או לא נמצא ב-PATH.
פתרון: התקנה עם `npm install -g @googleworkspace/cli`. כשמשתמשים ב-npx, תוסיפו `npx @googleworkspace/cli` לפני הפקודות.

### שגיאה: "Authentication required" או "Token expired"
סיבה: המשתמש לא התחבר או שטוקן ה-OAuth פג תוקף.
פתרון: הרצת `gws auth login` כדי להתחבר מחדש. אפשרויות לקובץ אישורים ולטוקן נמצאות ב-`gws auth --help`.

### שגיאה: "Unknown service" או ארגומנט לא צפוי
סיבה: שימוש בצורת פקודה מומצאת כמו `gws sheets create` או `gws sheets read`.
פתרון: תשתמשו במערך האמיתי: `gws sheets spreadsheets <method> --params '<JSON>'` (עם `--json '<body>'` לכתיבות), או בקיצורי העזר `+read` / `+append`. תריצו `gws sheets --help` ו-`gws sheets spreadsheets --help` כדי לראות שיטות אמיתיות.

### שגיאה: "Spreadsheet not found" או "404"
סיבה: מזהה הגיליון שגוי או שלמשתמש אין גישה.
פתרון: תוודאו את מזהה הגיליון מהכתובת של Google Sheets (המחרוזת שבין /d/ ל-/edit). תוודאו שלחשבון Google המחובר יש הרשאת עריכה לגיליון.

### שגיאה: "VAT calculation mismatch"
סיבה: הבדלי עיגול בין חישוב ידני לנוסחאות הגיליון.
פתרון: תמיד תעגלו מע"מ ל-2 ספרות אחרי הנקודה. תשתמשו בנוסחה `Math.round(amount * 18) / 100` לחישובי שקלים מדויקים. רשות המיסים מקבלת עיגול לאגורה הקרובה.
