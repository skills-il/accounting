# Domain checklist: hashavshevet-data-tools

Researched 2026-10-25. Primary sources were read directly: the ITA unified-file spec 1.31 PDF (pdftotext), the ITA "Israel Invoices" API spec 2.0 / 7.2024 (work/pdf/sh.txt), the ITA PCN874 software-houses circular (English), Hashavshevet's BKMV guide (bkmv7-erp.pdf) and 2026a release notes, plus the existing work/research.md (gov.il pages read through a browser). Statute wording for s.38(א1) and s.47(א2) is as quoted in the current SKILL.md and was not re-fetched here.

Items marked **[GAP]** are not covered, or are covered incorrectly, in the current SKILL.md / references/legacy-fixed-width.md.

---

## Must cover (core)

### A. Unified file (קובץ במבנה אחיד / OPENFORMAT / BKMV), spec "הוראות להפקת קבצים במבנה אחיד" v1.31 (dated 01/05/2009 on every page)

Source for every item in A unless noted: ITA spec 1.31, https://www.gov.il/BlobFolder/service/registration-software-designed-managing-computerized-accounting-system/he/Service_Pages_Income_tax_horaot-131.pdf . Legal basis: amendment of 2 August 2006 to הוראות מס הכנסה (ניהול פנקסי חשבונות), התשל"ג-1973, cited in the spec's introduction (section 1).

1. **Two files, not three.** The spec defines only INI.TXT and BKMVDATA.TXT (s.2.1(א), s.2.5(א)). README.TXT is a Hashavshevet addition for the user (bkmv7-erp.pdf, "קובץ המכיל אינפורמציה למשתמש"). Only INI.TXT and BKMVDATA.TXT are sent.
2. **BKMVDATA.TXT is compressed into an archive named BKMVDATA** whose extension depends on the compression tool (s.2.2(ד), s.2.5(ד)). INI.TXT is not compressed. Field 1030 in A000 records the compression program's name.
3. **Mandatory folder path** `<drive>:\OPENFRMT\<first 8 digits of the osek number, without check digit>.<2-digit year of production>\<MMDDhhmm of production>` (s.2.2(א) to (ג); worked example `F:\OPENFRMT\00223344.08\09111025`). Two runs in the same minute: bump the minute. The audited tax year is NOT in the path; it is in INI.TXT. On Linux/Unix, build elsewhere and move into this path (s.2.2(ה)). Hashavshevet example: `C:\OPENFRMT\51109427.16\03021139` (bkmv7-erp.pdf). **[GAP]**
4. **Primary identifier (מזהה ראשי):** a random 15-digit number, unique per production and per company, repeated identically in fields 1004 (A000), 1103 (A100) and 1153 (Z900) (s.2.4(א), clarification 2). A validator must check that all three match. **[GAP]**
5. **Character set is stated in the file, field 1029: 1 = ISO-8859-8-i (logical Hebrew, Windows), 2 = CP-862 (DOS)** (s.2.4(ח), A000 field 1029 at col 396). The skill currently says "Windows-1255" everywhere. Hebrew letters (0xE0 to 0xFA) are identical in ISO-8859-8 and CP1255, but the two differ outside the letters (for example 0xA4 is the ₪ sign in CP1255 and the generic currency sign in ISO-8859-8; CP1255 also carries niqqud at 0xC0 to 0xD2). CP-862 puts the letters at 0x80 to 0x9A, so decoding a CP-862 file as CP1255 produces garbage. Read field 1029 and decode accordingly. Also distinguish logical ISO-8859-8-i from visual ISO-8859-8 (reversed text). **[GAP]**
6. **Language code, field 1028:** 0 = Hebrew, 1 = Arabic, 2 = other.
7. **Fixed record lengths (excluding CR LF), table s.2.5(ה), one item per row:**
   - 7a. A000 (INI.TXT, leading record): 466
   - 7b. B100 summary (INI.TXT): 19
   - 7c. B110 summary (INI.TXT): 19
   - 7d. C100 summary (INI.TXT): 19
   - 7e. D110 summary (INI.TXT): 19
   - 7f. D120 summary (INI.TXT): 19
   - 7g. M100 summary (INI.TXT): 19
   - 7h. A100 opening (BKMVDATA.TXT): 95
   - 7i. B100 journal transaction line: 317
   - 7j. B110 account: 376
   - 7k. C100 document header: 444
   - 7l. D110 document line: 339
   - 7m. D120 receipt / deposit line: 222
   - 7n. M100 inventory item: 298
   - 7o. Z900 closing: 110
   A parser must assert these exact lengths per record code, not truncate or pad silently. **[GAP: the lengths are not in the skill]**
8. **Every record ends with CR (ASCII 13) + LF (ASCII 10); the record length excludes them** (s.2.4(ט)(2)).
9. **INI.TXT summary records (fields 1050 record code, 1051 count, X(4) + 9(15)) exist only for record types actually present in BKMVDATA.TXT** (s.2.5(ב), s.3.2). There is no summary row for A100 or Z900.
10. **Control totals:** A000 field 1002 (total records in BKMVDATA) must equal Z900 field 1155 (total including opening and closing). Field "מספר רשומה בקובץ" (second field of every BKMVDATA record, cols 5 to 13) is a running sequence number (s.2.4(י)). A validator checks continuity of that sequence.
11. **Field padding:** numeric fields right-aligned with leading zeros; alphanumeric left-aligned, padded with spaces or with "!" (s.2.3(ה), (ז)). Unused / "future data" areas filled with spaces or "!" (s.2.4(ט)(1)). A parser must strip trailing "!" as well as spaces. **[GAP]**
12. **Signed amounts `X9(12)v99`:** sign character then digits with implied decimals, no decimal point. Spec examples: -12345.65 is `-1234565`; 1245.65 is `+0124565` (s.2.3(ו)). Quantity uses `X9(12)v9999` (D110 field 1264). VAT rate per line field 1268 is `9(2)v99` (17% is `1700`, 18% is `1800`).
13. **Sign semantics differ by record type** (s.2.4(יא), (יב), clarifications 1, 4, 5, 8):
    - B100: amounts in 1368/1369 are positive; debit/credit comes from field 1366 (1 = debit/expense, 2 = credit/income). A negative amount reduces that side.
    - B110 field 1414 (opening balance at the cut): debit balance positive, credit balance negative, zero shown as "+".
    - C100 / D110: always positive except fields that reduce the document (document discount 1220 and line discount 1266 are negative); withholding 1224 is positive.
    - The accounting meaning of a document comes from its document TYPE, not its sign (a positive credit note 330 reduces income).
14. **Dates are `YYYYMMDD` numeric(8), times `hhmm` numeric(4)** (s.2.4(ב), (ג)). Skill currently teaches DD/MM/YYYY for Hashavshevet; inside the unified file it is YYYYMMDD. **[GAP]**
15. **Three distinct dates, clarification 12:** C100 1205 production date (system-set, not editable), 1216 value date, 1230 document date (the date printed on it); B100 1362 date, 1363 value date, 1375 entry date (system-set). Allocation-threshold and VAT-rate scoping must use the right one (document date 1230 for the invoice). **[GAP]**
16. **Date cut rules** (s.2.1(ג)(3)): multi-year software (A000 1011 = 2) cuts documents by document date and journal entries by value date AND/OR entry date (an entry recorded 20/12/2001 with value date 02/01/2002 belongs in a 2002 to 2003 cut). Single-year software (1011 = 1) has no cut and fills 1023 tax year; multi-year fills 1024/1025 range. **[GAP]**
17. **Document number format:** up to 20 chars; numeric with or without leading zeros; a series prefix of up to 5 characters left-justified (`AA123` or `AA000000000000000123`), and it must be consistent across C100 1204, D110 1254/1257, D120 1304, B100 1357/1359 (s.2.4(ד)). Migration must keep these joins intact.
18. **Header/line linkage:** C100 1234 and D110/D120 1273/1323 are the internal link fields (clarification 11); D110 1256/1257 carry the base document (invoice based on delivery note etc., clarification 6).
19. **Currency codes in the unified file are ISO 4217** (Appendix 2, s.2.4(ו)); A000 1032 leading currency defaults to ILS; country codes are ISO 3166-1 (Appendix 3). The skill's gotcha says Hashavshevet uses internal non-ISO codes: true internally, but the BKMV export must emit ISO codes, and Hashavshevet errors on export if a user-added currency has no international code mapped (bkmv7-erp.pdf Appendix A). **[GAP: clarify the distinction]**
20. **Accounting method, A000 1013: 0 = not relevant, 1 = single-entry, 2 = double-entry; 1014 balance required at 1 = transaction level, 2 = batch level (mandatory for double-entry).** In single-entry, VAT and withholding are flattened into the B100 line (s.4.6 example).
21. **One B100 record per journal line:** a 3-line entry (customer 117 debit, VAT 17 credit, income 100 credit) is 3 records with the same transaction number 1353 and line numbers 1 to 3 (s.4.6). B100 1364 and 1365 must reference an existing B110 1403 key.
22. **B110 field 1417 "קוד בסיווג החשבונאי" (4 digits) is the Form 6111 classification code**, mandatory when the taxpayer must report 6111. B110 1405/1406 trial-balance code and description; 1419 counterparty osek number mandatory in double-entry. This is the field that carries the 6111 mapping through a migration (s.4.7). **[GAP: skill says "preserve the mapping" but does not name field 1417]**
23. **Withholding at document level:** C100 1224 "סכום הניכוי במקור" (clarification 4 example: debt 1,250, withheld 250, fields 1219/1221/1223 = 1,000, 1224 = 250).
24. **Cancelled document flag:** C100 1228 = 1. Cancelled documents stay in the file.
25. **Branches:** A000 1034 = 1 makes branch IDs (1231, 1270, 1320, 1374, 1421, 1274) mandatory (clarification 3).
26. **Software registration fields:** A000 1005 constant `&OF1.31&`, 1006 ITA software registration certificate number, 1007/1008 software name/version, 1009/1010 producer. A migration target that has no registration number cannot produce a valid file (ties to retention, item F).
27. **D120 payment-method code, field 1306 (each value):** 1 cash; 2 cheque; 3 credit card; 4 bank transfer; 5 gift vouchers; 6 exchange slip; 7 promissory note (שטר); 8 standing order; 9 other. Cheque requires bank/branch/account/cheque number (1307 to 1310); 1311 is cheque due date or card payment date.
28. **D120 card acquirer, field 1313:** 1 Isracard, 2 Cal, 3 Diners, 4 American Express, 6 Leumi Card (code 5 is not defined in 1.31; Leumi Card is now Max, map by code not by name). Field 1315 credit type: 1 regular, 2 instalments, 3 credit, 4 deferred charge, 5 other.
29. **D110 transaction type, field 1258:** 1 service, 2 sale, 3 service and sale.
30. **M100 (s.4.8):** 1455 internal SKU must be unique; 1461 total in, 1462 total out (both positive); 1463 / 1464 cost price outside / inside bonded warehouses (clarifications 9, 10).
31. **Document type codes, Appendix 1 of spec 1.31 (only listed values are allowed, s.2.4(ה)), each row:**
    - 31.1 100 order (הזמנה)
    - 31.2 200 delivery note (תעודת משלוח)
    - 31.3 205 agent delivery note
    - 31.4 210 return note (תעודת החזרה)
    - 31.5 300 invoice / transaction invoice (חשבונית / חשבונית עסקה)
    - 31.6 305 tax invoice (חשבונית מס)
    - 31.7 310 summary invoice (חשבונית ריכוז)
    - 31.8 320 tax invoice / receipt
    - 31.9 330 credit tax invoice (חשבונית מס זיכוי)
    - 31.10 340 armoured / reserve invoice (חשבונית שריון)
    - 31.11 345 agent invoice (חשבונית סוכן)
    - 31.12 400 receipt (קבלה)
    - 31.13 405 donation receipt (קבלה על תרומות, s.46 receipts)
    - 31.14 410 cash-out (יציאה מקופה)
    - 31.15 420 bank deposit (הפקדת בנק)
    - 31.16 500 purchase order
    - 31.17 600 purchase delivery note
    - 31.18 610 purchase return
    - 31.19 700 purchase tax invoice
    - 31.20 710 purchase credit
    - 31.21 800 opening balance (יתרת פתיחה)
    - 31.22 810 general stock-in
    - 31.23 820 general stock-out
    - 31.24 830 inter-warehouse transfer
    - 31.25 840 stock-count adjustment
    - 31.26 900 production report, in
    - 31.27 910 production report, out
    Note: when the document value is negative, the effect is reversed (Appendix 1 notes).
32. **Temporal: the unified file 1.31 has NO allocation-number field** (no occurrence of "הקצאה" in the spec). Allocation numbers for 2024+ invoices travel only in the source system, in PCN874, and in the ITA's own records. A migration that relies on BKMV alone silently drops them; carry them as a separate column / custom field. **[GAP]**
33. **Temporal: the allocation API's document-type table adds codes not in Appendix 1 of 1.31:** 332 transaction account / proforma (allocation: yes), 345 marked "new", 348 journal entry (allocation: yes, so a bookkeeper can obtain numbers for invoices recorded only as a journal entry), and future "I" codes 305-I / 331-I for Palestinian customers "not yet in the unified file". Per the API table: 300 no, 305 yes, 310 yes, 320 yes, 330 no, 332 yes, 345 yes, 348 yes. Source: ITA "מודל חשבוניות ישראל, תיאור ה-API's, מהדורה 7.2024 / 2.0", table 2.5, https://www.gov.il/BlobFolder/generalpage/hor-software-other/he/vat_software-houses-180724.pdf . A validator on 1.31 data must not reject 332/348 found in the source system, and must not expect them in BKMV. **[GAP]**
34. **ITA simulator accepts 1.31 only.** https://secapp.taxes.gov.il/TmbakmmsmlNew/frmCheckFiles.aspx ("יש לטעון קבצים בגירסה 1.31 בלבד"). Archived files produced under an older spec version must be regenerated, not uploaded as-is (research.md item 6).
35. **Hashavshevet-specific export choices** (bkmv7-erp.pdf): purpose must be chosen (CPA vs ITA); the ITA cut uses reference date OR value date (CPA cut uses reference date only); companies that close the year by "תאריך 3" are cut by that date; batch 9998 (income transfer to retained earnings) is exported only up to a chosen date; one file covers one year; only a super-user (מורשה על) can run it; journal lines are exported one-sided with the counter account. Running the wrong purpose for a migration archive changes which lines appear. **[GAP]**

### B. Allocation numbers (מספר הקצאה, "חשבוניות ישראל")

36. **Two rules, two sections:** buyer's deduction bar s.38(א1) of the VAT Law (no buyer-request condition) vs seller's duty s.47(א2)(1) (on buyer demand; not for zero-rated). Inserted by חוק ההתייעלות הכלכלית (תיקוני חקיקה להשגת יעדי התקציב לשנות התקציב 2023 ו-2024), התשפ"ג-2023 (cited in the API spec s.1.1.1). Already in the skill; keep.
37. **Threshold table by INVOICE DATE (pre-VAT, "עולה על" = strictly exceeds), each row:**
    - 37.1 Before 5 May 2024: no allocation requirement at all (start postponed twice, to 1.4.2024 then 5.5.2024; Shibolet, https://www.shibolet.com/?p=17694 ). **[GAP: skill says "May 2024", should give 5.5.2024]**
    - 37.2 5 May 2024 to 31 Dec 2024: above NIS 25,000.
    - 37.3 1 Jan 2025 to 31 Dec 2025: above NIS 20,000 (צו ההתייעלות, end of 2024).
    - 37.4 1 Jan 2026 to 31 May 2026: above NIS 10,000 (in the consolidated s.38(א1) text: "מינואר 2026 ועד מאי 2026: 10,000").
    - 37.5 From 1 Jun 2026: above NIS 5,000 (gov.il service page, updated 01.06.2026, https://www.gov.il/he/service/request-assignment-number-for-tax-invoice ).
    - Superseded schedule to flag as WRONG if found in sources: 15,000 (2026), 10,000 (2027), 5,000 (2028) from the August 2024 ITA directive; and Sovos's "10,000 Jan to Jul 2026, 5,000 from Aug 2026" ((gov.il / vendor document, URL omitted; see the title) ), which contradicts gov.il and the statute.
38. **Number format:** confirmation_number is A30 (26-digit examples); print and report the rightmost 9 digits ("הקצאה מספר:"); the 9-digit short number goes into the PCN874 transaction record on both sales and input side (API spec s.6, field "מספר הקצאה קצר", N(9), mandatory). Skill says "9 digits" only. **[GAP: store all 26 digits, derive the 9]**
39. **ITA MinimumAmount service returns the minimum VAT amount, not the pre-VAT amount** (`minimum_amount` = 3600 = 20,000 x 18%; 900 at the 5,000 band). Hashavshevet 2026a's "סכום מינימלי להקצאה" field also now holds the VAT amount. Source: vat_software-houses-260825.pdf, HashERP2026.pdf. **[GAP]**
40. **Rejected / withheld invoice handling in the data:** if the seller cancels, neither the invoice nor its storno is reported in PCN874; if the seller proceeds without a number, the invoice must carry "אין לנכות מס תשומות בגין חשבונית זו" prominently; a later approval after hearing re-uses the same Invoice_Id. Buyer side: an input invoice rejected for allocation mismatch is removed together with its storno from PCN874 (API spec s.6, pp. 29 to 30). The four options and timelines are in the skill; the data-file consequences are not. **[GAP]**
41. **Zero-rated and exempt invoices are outside the requirement;** exactly-on-threshold invoices are outside it (strictly "exceeds"). Already in the skill.

### C. VAT rate by date

42. **Rate table by tax point, each row within the retention window:**
    - 42.1 1 Oct 2015 to 31 Dec 2024: 17% (D110 1268 = `1700`).
    - 42.2 From 1 Jan 2025: 18% (`1800`).
    A pending bill to cut to 17% is opposed by the Finance Ministry and has not passed (research.md item 3). Source: VAT Law s.2 and the rate orders; gov.il VAT rate page. Skill states 18% and the 2025 change, but not the 17% row or its start date. **[GAP: give the full row]**

### D. PCN874 detailed VAT report

Source: ITA circular to software houses, "Deployment for PCN874 File Generation", Appendices A to C, (gov.il / vendor document, URL omitted; see the title) ; legal basis VAT Law s.69א(א) and s.67א(א).

43. **File name PCN874.TXT; fixed structure, zero-padded; one header, N transaction records, one closing record.** Default period is the calendar month before production.
44. **Header record "O"** fields: osek number N(9), report month YYYYMM, report type, generation date, signed totals (taxable sales, VAT on sales, zero/exempt sales, VAT on other inputs, VAT on equipment inputs, net VAT to pay/receive), record counts for sales and inputs.
45. **Transaction record fields:** entry type A(1); counterparty VAT number N(9) (customer for sales, supplier for inputs); invoice date YYYYMMDD; reference group A(4); reference number N(9), rightmost 9 positions; VAT N(9) rounded to the nearest shekel, always positive; sign A(1) (credit/cancellation always minus); invoice total before VAT N(10), rounded, always positive; last N(9) field now carries the short allocation number.
46. **Closing record "X"** with the submitter's osek number.
47. **Entry-type codes, each row (Appendix A table + Appendix C):**
    - 47.1 S, regular sale to identified customer (also zero-rated/exempt non-export, with VAT zeros)
    - 47.2 L, sale to unidentified/private customer (aggregated; counterparty zeros; date of aggregation; number of invoices in reference field)
    - 47.3 M, sale, self-invoice (counterparty = supplier)
    - 47.4 Y, export (counterparty = export entry number or 999999999; export entry date)
    - 47.5 I, sale to Palestinian Authority customer
    - 47.6 T, input, regular Israeli supplier
    - 47.7 K, input, petty cash (counterparty zeros; reference = number of invoices)
    - 47.8 R, input, import entry (counterparty = import entry number; reference zeros)
    - 47.9 P, input, Palestinian Authority supplier
    - 47.10 H, input, other document by law (import entry, bank document etc.)
    - 47.11 C, input, self-invoice
48. **Representative multi-client wrapper (Appendix B):** "A" initial record (representative VAT number, month), per-client blocks, "Z" summary (number of users, number of entries).
49. **Who must file, by period (temporal):** companies with turnover above NIS 500,000 from the September 2025 period; individual osek with turnover above NIS 500,000 from period 1/2026; deferral to 1.1.2027 on application if either 90% test (by amount, or by count, of input invoices each up to NIS 5,000 in the 2025 returns) is met; reliefs not available to companies or to those already filing. Placeholder 777777772 for aggregated input invoices up to NIS 5,000. Source: ITA notice pa280825-1, https://www.gov.il/he/pages/pa280825-1 . The deferral ends 1.1.2027, about two months from now: deferred individuals report in detail from period 1/2027. **[GAP: the end-date consequence]**
50. **Becoming a detailed filer moves the business to monthly reporting (s.67א(א)) with online filing due by the 23rd.** Already in the skill.
51. **Hashavshevet 2026a can transmit PCN874 directly to the ITA** (token from ITA required; simulator view available), and has a VAT payment report for representatives. Source: HashERP2026.pdf; (gov.il / vendor document, URL omitted; see the title) . A migration must re-establish the token/transmission in the target system. **[GAP]**

### E. Form 6111

52. **6111 is the standardized financial-statement annex to the annual return** (P&L, balance sheet, tax adjustments), filed online; its codes are year-specific. Source: https://www.gov.il/he/service/itc6111 . In the unified file the code sits in B110 field 1417 (item 22). Prior-year comparatives are required.

### F. Bookkeeping retention (הוראות ניהול פנקסים)

53. **Retention period:** 7 years from the end of the tax year to which the records relate, or 6 years from filing the return for that year, whichever is later. Source: הוראות מס הכנסה (ניהול פנקסי חשבונות), התשל"ג-1973, s.25. Already in the skill; cite the section number. **[GAP: section not cited]**
54. **Producing the unified file on demand is part of the duty** for any computerized system that must be registered (spec 1.31 introduction; registration service page (gov.il / vendor document, URL omitted; see the title) ). Practical rule: produce and validate one BKMV per retained year at cutover, while the Hashavshevet licence is live; Hashavshevet notes the file "usually replaces the demand to hand over a backup of the original data" (bkmv7-erp.pdf).
55. **Temporal retention window for a 2026 cutover:** tax years from 2019 onward are typically still inside the window (2019 + 7 = end of 2026), so the archive spans BOTH VAT rates (17% and 18%) and all allocation-threshold bands (none, 25k, 20k, 10k, 5k). Validators must apply each row by document date.

### G. Withholding continuity in a migration

56. **102** (monthly employer report and deposit of income tax and NII withholding), **Form 126** (annual per-employee report, reconciles to the 102s, also reported to NII), **Form 856** (annual report of payments to suppliers subject to withholding). Annual reports due 30 April of the following year (verify the current year's date on gov.il before relying on it). Source: ITA withholding services, (gov.il / vendor document, URL omitted; see the title) . Load year-to-date per-payee cumulative data, or file the transition year from the old system. Already in the skill.
57. **Withholding certificates (אישור ניכוי במקור) per supplier, with rate and validity dates, must migrate** together with the supplier master; without them the new system withholds at the default rate. Source: ITA online withholding-approval service (שאילתת ניכוי במקור). **[GAP]**
58. **A000 field 1016 is the withholding file number (תיק ניכויים);** the target system must be configured with the same number. **[GAP]**

### H. Migration targets (each row)

59. **iCount:** CSV import with its own headers; confirm the target can itself produce a 1.31 unified file and is ITA-registered (item 26).
60. **Rivhit:** accepts the unified file (יבוא נתונים מקובץ במבנה אחיד) and Excel templates; prefer the unified file to keep document numbering.
61. **Invoice4U:** master data and open balances; no historical journal import; API for programmatic load.
62. **Green Invoice (Morning):** customer/supplier master and open balances via CSV or API; it is an invoicing system, so the general ledger must live elsewhere.
63. **H-WEB / WizCloud API v2.0.0** as the source for live extraction: https://docs.wizcloud.co.il/docs/intro (resources documents, journal, mainaccount, receipts, bankstatements, currencies, triggers); token page https://home.wizcloud.co.il/help/apidocument/ .
For each target the cutover checks are: opening trial balance = closing trial balance, document-number continuity per document type, allocation numbers carried (item 32), 6111 code carried (item 22), ISO currency codes and original-currency amounts (item 19).

### I. Hebrew handling outside the unified file

64. **Legacy .dat files and Hashavshevet CSV/Excel exports are CP1255; Excel CSV output must be utf-8-sig; XLSX sheets RTL; JSON ensure_ascii=False.** Already in the skill.
65. **Visual vs logical Hebrew:** ISO-8859-8 (visual) text arrives reversed; ISO-8859-8-i is logical. Detect by checking whether common words read backwards.

---

## Should cover (advanced)

1. **Coming ITA requirement: transmit the unified file via API right after production** ("תוספת מס 1", edition 1.0 3.2026, GetUrlsForUploadingFiles V1.0 beta, INI and BKMVDATA uploaded through signed URLs; a condition of software registration; sandbox only, production date not announced). https://www.gov.il/BlobFolder/generalpage/hor-software-other/he/IncomeTax_software-houses-100326-1.pdf
2. **File status API** (edition 1.0, 09-2026), for files sent through that upload API. (gov.il / vendor document, URL omitted; see the title)
3. **Advance-tax (מקדמות) reporting and payment API** (edition 1.1, 7.2026) used by representative-linked software; Hashavshevet 2026a's "הגדרות למייצגים" and the 9-character representative number. (gov.il / vendor document, URL omitted; see the title) ; HashERP2026.pdf.
4. **Allocation-API supplementary services:** "invoices received from suppliers for a period" (6.2025) can reconcile the buyer's ledger against ITA-issued numbers during migration. (gov.il / vendor document, URL omitted; see the title)
5. **Allocation number on journal-only invoices (document type 348)**: the bookkeeper can obtain numbers by entering supplier osek, reference type and number, date, customer osek, VAT and pre-VAT amount (API spec, note to table 2.5).
6. **Cash-register (Z) neutralization:** a tax invoice issued through a cash register must be removed from the register total so it is not reported twice (PCN874 circular, remark 7a).
7. **Mixed invoices** (taxable + exempt/zero lines) are reported as taxable or split into two records (PCN874 circular remarks).
8. **Tax point vs document date for rate selection** across the 2024/2025 boundary (VAT Law s.28 timing rules): an invoice dated January 2025 for a December 2024 supply needs explicit handling; flag rather than guess.
9. **Instalment receipts:** one C100 plus one D120 per cheque / card instalment (spec s.4.5 examples: 5 cheques, 3 card payments); B100 entry date vs value date per instalment (clarification 12 example).
10. **Very large BKMVDATA:** split by date range; each split is a separate production with its own primary ID and its own OPENFRMT subfolder.
11. **Branches/sub-ledgers (1034 = 1):** multiple branch IDs must survive the migration.
12. **Postdated cheques, foreign-currency open balances (B100 1367/1369 original-currency amount), fixed-asset register, inventory valuation (M100 1463/1464)** as non-trial-balance data to extract.
13. **Payroll is not in BKMV;** extract from the payroll module separately (already in the skill).
14. **Legacy fixed-width .dat parsing** as fallback only, with record-length assertions and strict encoding (references/legacy-fixed-width.md).
15. **Hashavshevet product naming:** current Windows release "2026a" (H-ERP); cloud H-WEB; H-CLOUD (hosted Windows); legacy Gold/2000+ names. https://www.h-erp.co.il ; https://downloads.h-erp.co.il/files/improvements/HashERP2026.pdf
16. **Data import into WizCount from other programs** (h-erp.co.il link) for reverse migrations into Hashavshevet.

---

## Out of scope (explicit)

1. Direct writes into a live Hashavshevet company database or reverse-engineering its binary/ISAM storage.
2. Requesting allocation numbers from SHAAM on the user's behalf (requires the business's ITA credentials and registered software).
3. Filing PCN874, 6111, 102/126/856 or the annual return with the ITA, or paying VAT.
4. Tax advice: deciding deductibility, VAT classification of a transaction, choosing a turnover deferral, or arguing a rejected-allocation hearing. Point to a CPA / tax adviser.
5. Payroll calculation and payslips (separate payroll skill).
6. Building or registering accounting software with the ITA (software-house registration).
7. Bank reconciliation logic beyond mapping fields (separate bank-reconciliation skill).
8. Non-Israeli formats (SAF-T for other countries, DATEV, QuickBooks IIF) except as a generic CSV/Excel target.
9. Legal opinions on retention disputes or on destroying records early.

---

## Authoritative sources

| # | Source | URL | Used for |
|---|---|---|---|
| 1 | ITA, הוראות להפקת קבצים במבנה אחיד, v1.31 (01/05/2009) | https://www.gov.il/BlobFolder/service/registration-software-designed-managing-computerized-accounting-system/he/Service_Pages_Income_tax_horaot-131.pdf | A1 to A31, A34 |
| 2 | ITA software registration service page | (gov.il / vendor document, URL omitted; see the title) | A26, F54 |
| 3 | ITA unified-file simulator (1.31 only) | https://secapp.taxes.gov.il/TmbakmmsmlNew/frmCheckFiles.aspx | A34 |
| 4 | ITA, מודל חשבוניות ישראל API spec 2.0 / 7.2024 | https://www.gov.il/BlobFolder/generalpage/hor-software-other/he/vat_software-houses-180724.pdf | A33, B38, B40, Should 5 |
| 5 | ITA MinimumAmount service add-on 8.2025 | (gov.il / vendor document, URL omitted; see the title) | B39 |
| 6 | ITA suppliers' invoices service add-on 6.2025 | (gov.il / vendor document, URL omitted; see the title) | Should 4 |
| 7 | gov.il, request allocation number (updated 01.06.2026) | https://www.gov.il/he/service/request-assignment-number-for-tax-invoice | B37 |
| 8 | VAT Law s.38(א1), s.47(א2)(1), s.67א(א), s.69א(א), s.28 (as amended by חוק ההתייעלות הכלכלית התשפ"ג-2023) | Nevo / gov.il consolidated text | B36, B37, D49, D50, Should 8 |
| 9 | Shibolet, second extension of the invoice model (start 5.5.2024) | https://www.shibolet.com/?p=17694 | B37.1 |
| 10 | ITA notice pa280825-1 (individual osek detailed reporting) | https://www.gov.il/he/pages/pa280825-1 | D49 |
| 11 | ITA PCN874 software-houses circular, Appendices A to C | (gov.il / vendor document, URL omitted; see the title) | D43 to D48, Should 6, 7 |
| 12 | Form 6111 service | https://www.gov.il/he/service/itc6111 | E52 |
| 13 | הוראות מס הכנסה (ניהול פנקסי חשבונות), התשל"ג-1973, s.25 | Nevo consolidated text | F53 |
| 14 | ITA withholding topic page | (gov.il / vendor document, URL omitted; see the title) | G56, G57 |
| 15 | ITA unified-file transmission API addendum 1.0 3.2026 | https://www.gov.il/BlobFolder/generalpage/hor-software-other/he/IncomeTax_software-houses-100326-1.pdf | Should 1 |
| 16 | ITA file-status API 1.0 09-2026 | (gov.il / vendor document, URL omitted; see the title) | Should 2 |
| 17 | ITA advance-tax API 1.1 7.2026 | (gov.il / vendor document, URL omitted; see the title) | Should 3 |
| 18 | Hashavshevet H-ERP BKMV export guide | https://downloads.h-erp.co.il/files/general/bkmv7-erp.pdf | A1, A3, A19, A35, F54 |
| 19 | Hashavshevet 2026a release notes | https://downloads.h-erp.co.il/files/improvements/HashERP2026.pdf | B39, D51, Should 3, 15 |
| 20 | Hashavshevet PCN874 transmission guide | (gov.il / vendor document, URL omitted; see the title) | D51 |
| 21 | WizCloud API reference v2.0.0 | https://docs.wizcloud.co.il/docs/intro | H63 |
| 22 | Sovos release note (cited only as a WRONG schedule to reject) | (gov.il / vendor document, URL omitted; see the title) | B37 |
| 23 | Unicode CP1255 mapping | https://unicode.org/Public/MAPPINGS/VENDORS/MICSFT/WINDOWS/CP1255.TXT | A5 |

Counts: Must cover 65 numbered items (with 15 record-length rows, 27 document-type rows, 5 threshold rows, 2 VAT-rate rows and 11 PCN874 entry-type rows enumerated inside them), Should cover 16, Out of scope 9, Sources 23.
