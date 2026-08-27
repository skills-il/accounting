# Healthcare tosafot (additions) and how each is paid

The additions on a healthcare slip sit on top of the combined-salary cell. Some
are a percentage of the base, some are named fixed-shekel lines, and shift and
on-call pay follow their own rules. Amounts change with agreements and CPI, so
read the current figure from the union or the Wage Commissioner. The figures
below are the ones this skill has sourced; treat them as the current known values
and re-check the year on the slip.

## Nurses (nurses' dirug)

| Addition | How it is paid |
|----------|----------------|
| Gmul hishtalmut (professional development) | A pensionable percentage of the combined salary credited in recognized-study-hour units (committee-approved). One of the largest levers on a veteran nurse's base pay. Read the current per-unit rate and unit cap from the nursing committee. |
| Tosefet achayot 2024 | Named supplement for state-employed nurses: 250 NIS per full-time position from 1.10.2024, updated to 500 NIS per full-time position from 1.4.2025. Scale for part-time. |
| Shift-responsibility supplement (tosefet achrayut mishmarot) | A per-entitled-shift amount paid to the nurse taking responsibility for a shift (a ward nurse, not only a manager). The agreement increases it over time. Changes month to month with shifts worked. |
| Rotating-shift supplement | Paid to two-shift and three-shift workers, distinct from the per-shift responsibility line and from statutory night pay. Read the current amount. |
| Charge-nurse / role and academic-degree lines | A charge-nurse-of-the-shift (achot achrait mishmeret) role line, an academic-degree supplement (tosefet toar), and an employer-specific management supplement (tosefet minhal / nihul) for management roles. |
| Legacy fold-in shekel supplements | Named monthly shekel supplements from past agreements that fold into the base; veteran slips still show them. |

## Allied health (occupational therapy, physiotherapy, para-medical)

| Addition | How it is paid |
|----------|----------------|
| Tosefet hachsharot (in place of gmul hishtalmut), from 1.4.2025 | A percentage of the combined salary ONLY, banded by professional seniority with exclusive upper bounds: 3.50% for 0 to 7 years, 9.00% for 7 to 17 years, 9.50% from 17 years. Replaces gmul hishtalmut rather than adding to it; the worker receives the higher of the two, never both. Render the band that matches the worker's professional seniority (counted from licence date, excluding army and national service). |
| Monthly incentive (tamritz) | A capped monthly performance line. The ceiling rose from 4,125 NIS to 5,400 NIS per full-time position per month from 1.4.2025. Variable, not part of the fixed base. |
| Retention and recruitment grant | Up to 10,000 NIS per full-time position for eligible workers in specified settings (for example psychiatric hospitals and child-development units). Conditional and setting-specific. |

## Doctors (IMA agreement)

Pin the career stage first: a resident (mitmach), a specialist (mumche), and a
senior physician sit on different base tracks. Residents split into darga alef
(before the written board exam, 45 weekly hours) and darga bet (after it, 42
hours). Doctors' pay is dominated by duty and on-call, both paid in workday
equivalents and NOT part of base salary. Toranut is an on-site duty shift (in the
hospital); kononut is on-call standby from home. A toranut pays roughly double a
kononut for the same weekday, so the two must be tabled separately. Both are
valued off the doctor's day-value (erech yom), a defined figure that is higher
for a specialist than a resident.

Toranut (on-site duty, IMA section 42):

| Toranut timing | Payment |
|----------------|---------|
| Weekday | One workday plus three more (four day-equivalents) |
| Friday eve or holiday eve | One workday plus four more (five day-equivalents) |
| Sabbath or holiday daytime | Two workdays plus half (two and a half day-equivalents) |

Kononut (on-call standby, IMA section 49):

| Kononut timing | Payment |
|----------------|---------|
| Weekday, 16:00 to 08:00 next morning | Two workdays |
| Weekday, summoned in after 19:30 for 4.5 hours or more | Three workdays |
| Emergency-department, by a specialist | Three and a quarter workdays |
| Sabbath or holiday daytime, 08:00 to 16:00 | One workday |
| Holiday eve, 13:00 to 16:00 | Half a workday |

Compute a duty or on-call amount as its workday-equivalent count times the
doctor's day-value (erech yom), not a plain daily rate. As a department-level
magnitude check (not an individual's line), a rota runs about 20 to 30 on-call
slots a month, about 60 in psychiatric hospitals. Residents also carry a
presence/stay supplement (tosefet shehiya) among their standing lines.

Because these lines are not base salary, they do not raise the pension and
severance base. Three more doctor lines sit outside the base: shortage-specialty
premium (miktzo'ot bemtzuka) at about 12.5% of salary for neonatology,
anesthesia, cardiology, and general/pediatric/cardiac intensive care; a one-time
periphery recruitment grant (ma'anak periferia) of 300,000 NIS (500,000 NIS for
residents and shortage-specialty specialists) plus an ongoing periphery premium
that ramped from 10% (2011) to 25% (from 2013) of salary; and global additional
hours (sha'ot nosafot globaliyot) for senior doctors. Read the current ongoing
rate for the periphery premium and the global-hours amount.

## Shared, non-healthcare-specific lines

- Havraa (recreation pay): paid like other employees.
- Clothing allowance (ktzuvat bigud): an annual public-sector payment, usually
  once a year around July, set by grade level. It appears on one slip a year, not
  evenly each month.
- Statutory night and overtime pay: standard labor law (a night shift and the
  overtime tiers above it) rather than a collective-agreement healthcare line.
  Keep it separate from the shift-responsibility supplement, and defer the
  mechanics to the israeli-payroll-calculator skill.


The toranut table gives day-type only, with no clock window per band, while the
kononut table anchors each band to a clock window. That asymmetry is a property
of the source agreements (the 2011 base agreement and the 2.10.2023 agreement),
not an omission here: no authoritative source publishes toranut clock windows.


## Doctors: career stage, the agreement stack, and tosefet mesima leumit

**Doctors.** First pin the career stage, because the base track differs by it: a
resident (mitmach) sits on a different base track from a specialist (mumche), who
differs again from a senior or attending physician. Residents are themselves split
by the board exams: darga alef, before passing the written board exam (bechinat
shlav alef), works a 45-hour week; darga bet, after it, works 42 hours. Each stage
carries its own lines and a different on-call profile. Do not model "a doctor" as
one base cell.

Doctors have their own agreement (signed 30.9.2024, covering the state, Clalit,
Hadassah and municipal hospitals) on top of the general framework, replacing the
previous agreement of 25.8.2011. It raises the combined-salary table in three
legs, each stated cumulatively against the pre-agreement table: 4.88% from
1.1.2025, 1.62% more from 1.7.2025 for 6.5% cumulative, and 1% more from 1.1.2026
for 7.5% cumulative. That agreement has been amended several times since
(among them 23.1.2025 and 31.3.2025, plus a monitoring-committee decision of
30.6.2025), so "the doctors' agreement" is a stack, not one document; name the
amendment you are relying on.

A separate tosefet mesima leumit is paid to entitled doctors for five years,
1.1.2025 to 31.12.2029, then stops. Its base was 3,000 NIS per full position, was
due to double to 6,000 from 1.7.2025, and the 31.3.2025 agreement instead staged
it at 4,500 NIS for 1.7.2025 to 30.11.2025 and 6,000 NIS from 1.12.2025, while
pension contributions are computed as though 6,000 applied throughout. It is
salary for severance and carries keren hishtalmut, but is NOT in the mashkoret
koveat.

**The amount is a base figure multiplied by a coefficient (mekadem)** set by
specialty and role in a table inside the agreement, so the headline base is NOT
what an individual doctor receives. Read the worker's own coefficient from the
Wage Commissioner circular; we could not source the coefficient range, so do not
state one. Do not confuse this supplement with tosefet mar'ag, which is a
separate shekel supplement with its own eligibility test.



## רופאים: שלב הקריירה, ערימת ההסכמים ותוספת משימה לאומית (עברית)

**רופאים.** לרופאים יש הסכם משלהם שנחתם ב-30.9.2024 וחל על המדינה, כללית, הדסה
ובתי חולים עירוניים, מעל הסכם המסגרת הכללי, והוא מחליף את ההסכם הקודם מ-25.8.2011.
ההסכם מעלה את טבלת השכר המשולב בשלוש פעימות, כל אחת מצטברת מול הטבלה שקדמה
להסכם: 4.88% מ-1.1.2025, עוד 1.62% מ-1.7.2025 ובסך הכול 6.5%, ועוד 1% מ-1.1.2026
ובסך הכול 7.5%. ההסכם תוקן כמה פעמים מאז (בהם 23.1.2025 ו-31.3.2025, והחלטת ועדת
מעקב מ-30.6.2025), כך ש"הסכם הרופאים" הוא ערימה ולא מסמך אחד; כדאי לנקוב בתיקון
שמסתמכים עליו.

תוספת משימה לאומית נפרדת משולמת לרופאים זכאים למשך חמש שנים, מ-1.1.2025 עד
31.12.2029, ונפסקת אחרי החלון הזה. הבסיס שלה היה 3,000 ש"ח למשרה מלאה, היה אמור
לעלות ל-6,000 ש"ח מ-1.7.2025, והסכם 31.3.2025 קבע במקום זאת 4,500 ש"ח מ-1.7.2025
עד 30.11.2025 ו-6,000 ש"ח מ-1.12.2025, בעוד ההפרשות לפנסיה מחושבות כאילו הבסיס
עמד על 6,000 ש"ח לאורך כל התקופה. היא נחשבת שכר לעניין פיצויי פיטורים ומופרשת
בגינה קרן השתלמות, אבל היא אינה נכללת במשכורת הקובעת לגמלאות. סכום הכותרת עדיין
אינו מה שרופא בודד מקבל.

**הסכום הוא סכום בסיס מוכפל במקדם** שנקבע לפי מקצוע ותפקיד בטבלה שבתוך ההסכם,
ולכן סכום הכותרת אינו מה שרופא בודד מקבל. קראו את המקדם הספציפי של העובד מחוזר
הביצוע של הממונה על השכר. לא הצלחנו לאמת את טווח המקדמים, ולכן אין לנקוב בטווח.
אין לבלבל בין התוספת הזו לבין תוספת מר"ג, שהיא תוספת שקלית נפרדת עם מבחן זכאות
משלה.

התוספת אינה נכללת במשכורת הקובעת לגמלאות והיא מוגבלת בזמן ואינה קבועה.

קודם קבעו את שלב הקריירה, כי מסלול הבסיס שונה לפיו: מתמחה יושב על מסלול
בסיס שונה ממומחה, וזה שונה שוב מרופא בכיר. מתמחים עצמם מחולקים לפי בחינות ההתמחות:
דרג א', לפני מעבר בחינת שלב א' בכתב, עובד שבוע של 45 שעות; דרג ב', אחריה, עובד 42
שעות. לכל שלב שורות משלו ופרופיל כוננות שונה. אל תמדלו רופא כתא בסיס אחד.

