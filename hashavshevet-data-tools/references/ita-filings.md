# ITA filings and allocation-number detail

Detail moved out of SKILL.md (Step 6.5 and the allocation-number notes) to keep the body under
the 5,000-word cap. SKILL.md carries the rules an agent must never miss; this file carries the
record layouts, procedures and timelines behind them.

## 1. Allocation number (מספר הקצאה) format

Source: the Tax Authority's API spec for software houses, "מודל חשבוניות ישראל, תיאור ה API's,
מהדורה 7.2024 / 2.0" (<https://www.gov.il/BlobFolder/generalpage/hor-software-other/he/vat_software-houses-180724.pdf>).

- The full number (`Confirmation_Number`) is an alphanumeric field of up to 30 characters
  (`A30`). The spec's examples are 26 digits, e.g. `"Confirmation_Number": "20240704061109183186068226"`.
- The SHORT allocation number is the rightmost 9 characters: `"מספר הקצאה קצר" – 9 תווים אחרונים של מספר ההקצאה`.
  It is what the invoice prints prominently and what PCN874 carries (section 3 below). The API
  also accepts the short form where it asks for the number (`ניתן לשלוח מספר מקוצר`).
- So a validator must accept EITHER shape and compare two numbers by their rightmost 9 digits.
  Rejecting a 26-digit value as "not 9 digits", or truncating it on import, is a bug.
- Store it as TEXT end to end. A 26-digit value exceeds float precision, so a numeric DB column, a
  float parse, or a CSV opened in Excel silently rounds it. Write it to XLSX as a string cell.
- A related secondary-source shorthand, "a 9-digit allocation number", describes the short form
  only. Do not let it drive a length check.

## 1b. Where each threshold row comes from

The CONSOLIDATED text of section 38(א1) states only `עולה על 5,000 שקלים חדשים (מינואר 2026 ועד מאי 2026: 10,000 שקלים חדשים)`,
so the two 2026 rows are confirmable directly from the statute. The NIS 20,000 (2025) row is not in
the consolidated text (a superseded band leaves no trace in it) but is on the Tax Authority's own
service page (<https://www.gov.il/he/service/request-assignment-number-for-tax-invoice>), which
states 20,000 for 2025, 10,000 from 1 January 2026 and 5,000 from 1 June 2026. The NIS 25,000 row
and its start date of 5 May 2024 rest on the amendment history and on independent secondary
sources (Shibolet, iCount, Green Invoice). The same ITA page says numbers have been issued since
1.1.2024, so a January to April 2024 invoice may carry one although none was required; that is not
an anomaly. A reader who opens the statute, fails to find 25,000, and was told all four rows sit
in 38(א1) will conclude the whole schedule is invented, so say where each row comes from.

## 2. Hashavshevet's "minimum amount" field is a VAT amount

The ITA's minimum-amount service (an add-on to the API spec, edition 2.0 / 8.2025,
<https://www.gov.il/BlobFolder/generalpage/hor-software-other/he/vat_software-houses-260825.pdf>)
returns `minimum_amount`, described as `סכום המע"מ המינימלי המחייב הקצאת חשבונית`, the minimum VAT
amount that triggers the duty, not the pre-VAT threshold. Hashavshevet mahadura 2026a changed its company-settings field to match:
`בשדה סכום מינימלי להקצאה יופיע מעתה סכום המע"מ המינימלי בחשבונית, עבורו חלה חובה לקבל מספר הקצאה`
(<https://downloads.h-erp.co.il/files/improvements/HashERP2026.pdf>). At the NIS 5,000 pre-VAT
threshold and 18% VAT the field reads 900. An agent comparing invoices against that field must
compare the invoice's VAT component, not its net amount; comparing the net amount to it flags
almost every invoice.

## 3. PCN874 transaction record (allocation-number fields)

Section 6 of the same API spec ("שינויים בדיווח המפורט (קובץ PCN874)") states that the short
allocation number is reported in the invoice (transaction) record on BOTH the sales and the input
side: `ברשומת החשבונית (רשומת התנועה) הן בצד העסקה הן בצד התשומה יש לדווח את מספר ההקצאה הקצר`.
The record fields it lists, in order:

| Field | Format | Note in the spec |
|---|---|---|
| Record type (document type) | A(1) | entry-type code, table below |
| Counterparty VAT file number | N(9) | sales record: the customer; input record: the supplier |
| Invoice / reference date | N(8) | YYYYMMDD |
| Reference group | A(4) | |
| Reference number | N(9) | the 9 rightmost positions |
| VAT amount on the invoice | N(9) | rounded to the nearest shekel (the 2010 circular adds: for inputs, the VAT allowed for deduction, 1/4, 2/3) |
| Sign | A(1) | `+`/`-`; a cancellation or credit to a supplier or customer is always minus |
| Invoice amount EXCLUDING VAT | N(10) | always the full (100%) pre-VAT amount, always positive, rounded to the nearest shekel |
| Short allocation number | N(9) | mandatory |

The invoice amount is the amount EXCLUDING VAT. The ITA's English circular to software houses
(Appendix A, <https://www.gov.il/BlobFolder/generalpage/tax-vat-online-invoice-reporting/en/IncomeTax_IncomeTaxSoftwareHousesInfo_874-eng.pdf>)
names the field `Invoice total not incl. VAT` with the note `Always the 100%, always a positive value`:
"the 100%" means the whole pre-VAT amount even where only a share of the input VAT (1/4, 2/3) is
deductible, not a VAT-inclusive total. Built from gross document totals, every line is overstated by
the VAT rate.

The same circular gives the rest of the file:

- Header record `O`: the osek number, the report month (YYYYMM), report type, generation date,
  then signed totals: taxable sales and their VAT, zero-rated / exempt sales, the number of sales
  records, VAT on "other" inputs and VAT on "equipment" inputs SEPARATELY, the number of input
  records, and the VAT to pay or receive.
- Closing record `X` with the submitter's osek number.
- Entry-type codes: sales S (regular), L (unidentified / private customer, aggregated), M (self
  invoice), Y (export), I (Palestinian Authority customer); inputs T (regular, Israeli supplier),
  K (petty cash), R (import), P (Palestinian Authority supplier), H (single document by law, such as
  an import entry or bank document), C (self invoice).
- Per-code conventions: L carries zeros as the counterparty, the aggregation date, and the number
  of aggregated sales in the reference field; Y carries the export-entry number (or `999999999` for
  services and intangibles) and zero VAT; K carries zeros as the counterparty and the number of
  invoices as the reference, and petty-cash VAT must stay under 2% of the file's VAT or NIS 2,000,
  the greater of them (the circular notes such parameters change by memo); R carries the import-entry
  number and date.
- A mixed invoice (taxable plus zero-rated or exempt lines) is reported as one taxable record, or
  as two records with the same type, customer, date and reference.
- When an amount is zero its sign field is `+`.
- Correcting an invoice already reported: report it again with the opposite sign and identical
  details, then report it once more with the correct details.

That circular is 2010-era: it shows the last field as reserved zeros. The 2024 API spec turned it
into the mandatory short allocation number. For a line that has no number (below the threshold,
aggregated L or K entries, before 5 May 2024), confirm the current fill rule with the ITA or the
software's PCN874 export rather than inventing one.

Storno rule from the same page: if a client wants to cancel an input invoice that was included in
the PCN file and "rejected" for an allocation-number mismatch, omit BOTH the input invoice and the
storno record from the file.

Practical consequences for data built from Hashavshevet: amounts in PCN874 are whole shekels, so a
reconciliation against the ledger will differ by rounding per line; the sign lives in its own field
and the amount is unsigned, so a parser that reads the amount alone counts credit notes as sales.
Hashavshevet 2026a can transmit PCN874 directly to the ITA once an ITA token is downloaded
(`ניתן מעתה לשדר את דו"ח מע"מ מקוון PCN874 מתוכנת חשבשבת ישירות לרשות המיסים`, HashERP2026.pdf).

## 4. Who must file PCN874, and the individual-osek reliefs

- Companies whose turnover exceeds NIS 500,000 were obligated from the September 2025 period. An
  individual osek (עוסק שהוא יחיד) whose annual turnover exceeds NIS 500,000 is obligated from
  1 January 2026 (ITA notice <https://www.gov.il/he/pages/pa280825-1>). Section 69א(א) of the VAT Law
  defines what the detailed report must contain.
- Becoming a detailed filer switches the business from bi-monthly to MONTHLY reporting and payment
  under section 67א(א); for online filing the return and payment are due by the 23rd of the
  following month, not the 15th.
- Relief (a): an individual osek may report tax invoices whose pre-VAT amount is NIS 5,000 or less
  as a single combined total; for those aggregated input invoices the supplier number is replaced by
  the fixed placeholder 777777772.
- Relief (b): the individual osek may apply to the regional VAT office to defer the duty to
  1 January 2027 if, on the 2025 returns, EITHER at least 90% of the total AMOUNT of input tax
  invoices came from invoices each NIS 5,000 or less, OR at least 90% of the NUMBER of input tax
  invoices were each NIS 5,000 or less. The application is accompanied by a declaration and
  supporting documents if required. A deferred individual reports in detail from period 1/2027.
- Neither relief applies to a company, or to an osek who had already started filing detailed
  returns before the notice was published.

## 5. When an allocation-number request is REJECTED

Source: Grant Thornton summary of the hora'at bitzua
(<https://www.grantthornton.co.il/insights1/tax-insignths/2026/From_June_the_allocation_number/>).
If the Director has reasonable grounds to suspect the invoice was issued unlawfully, the osek has
four options: (1) cancel the request; (2) proceed without an allocation number, in which case the
recipient cannot deduct the input VAT; (3) reverse charge (hipuch chiyuv), where the seller receives
a special allocation number and issues a zero-rated invoice, and the buyer (an osek murshe) issues a
self-invoice carrying that number, reports and pays the output VAT, and deducts input VAT as far as
the law allows; (4) apply to the control room for a hearing.

If the seller proceeds without a number, the API spec requires the invoice to carry, prominently,
the sentence `אין לנכות מס תשומות בגין חשבונית זו`; if a later hearing allows the invoice, the seller
requests the number again with the SAME `Invoice_Id` as the original
(<https://www.gov.il/BlobFolder/generalpage/hor-software-other/he/vat_software-houses-180724.pdf>).
So a migrated above-threshold invoice with neither a number nor that sentence is a separate red flag.

Timeline (only the hearing and the objection carry deemed-granted deadlines): the hearing is scheduled within 2 business days of the online notice, and the Director
must decide within 1 business day of its end, failing which the request is deemed granted. A refusal
can be objected to online within 30 days of the date of the hearing; the Director must decide within
21 business days, failing which the objection is deemed accepted. A decision on the objection may be
appealed to the District Court.

## 6. Unified-file (BKMV) facts that bite in a migration

From the ITA spec "הוראות להפקת קבצים במבנה אחיד", version 1.31
(<https://www.gov.il/BlobFolder/service/registration-software-designed-managing-computerized-accounting-system/he/Service_Pages_Income_tax_horaot-131.pdf>):

- **Integrity keys.** A random 15-digit primary identifier, new for every production, must be
  identical in A000 field 1004, A100 field 1103 and Z900 field 1153. Record lengths are fixed
  (excluding CR LF): A000 466, A100 95, B100 317, B110 376, C100 444, D110 339, D120 222, M100 298,
  Z900 110, and 19 for each INI.TXT summary record. An empty alphanumeric field may be padded with
  spaces or with `!`, so a parser must strip both. The files sit under
  `<drive>:\OPENFRMT\<first 8 digits of the osek number>.<2-digit PRODUCTION year>\<MMDDhhmm of production>`
  (the spec's example: `F:\ OPENFRMT \00223344.08\09111025`).
- **Record-count check, worked.** A000 field 1002 (records in BKMVDATA.TXT) must equal Z900
  field 1155, which counts ALL records including the A100 opening and the Z900 closing record.
  INI.TXT carries a summary record (field 1050 record code, 1051 count) only for each OTHER record
  type actually present, so: sum of summary counts + 2 = Z900 1155 = A000 1002. Illustrative file:
  summaries C100 120, D110 340, D120 45, B100 900, B110 210 sum to 1615; add 2 for A100 and Z900
  and 1155 must read 1617, and 1002 must read 1617. A validator that compares the summary sum
  directly with 1155 fails every valid file by exactly 2. Also check that the running record
  number (the second field of every BKMVDATA record) runs without gaps.
- **Which date.** C100 carries three dates: 1205 production date (set by the system, not
  editable), 1216 value date, and 1230 document date (the date printed on the document). B100
  carries 1362 date, 1363 value date and 1375 entry date (set by the system). Scope allocation
  thresholds and the VAT rate on 1230, never on 1205.
- **6111 code and counterparty.** B110 field 1417 `קוד בסיווג החשבונאי` (4 digits) is the 6111
  classification code, mandatory when the taxpayer must report 6111; 1405 is the trial-balance code;
  1419 is the supplier / customer osek number, mandatory in double-entry bookkeeping. A000 field
  1016 is the withholding file number (מספר תיק ניכויים).
- **Hashavshevet export purpose.** The H-ERP wizard asks whether the file is for the CPA or for the
  ITA. For the ITA, journal entries are cut by reference date OR value date; for the CPA by reference
  date only. One file covers one year, and batch 9998 (income transfer) has its own cut-off date
  (<https://downloads.h-erp.co.il/files/general/bkmv7-erp.pdf>).
- **No allocation-number field.** The word `הקצאה` does not occur anywhere in the 1.31 spec. A
  migration that relies on the uniform file alone drops every allocation number. Extract them
  separately from the source system's documents (or from the PCN874 files already filed) and load
  them into a dedicated field in the target.
- **Character set is declared in A000 field 1029** (in INI.TXT, column 396): `1 =ISO-8859-8-i; 2 = CP-862`.
  The spec: Windows output is logical Hebrew ISO-8859-8-i, DOS output is CP-862. Read the field
  before decoding: ISO-8859-8-i Hebrew decodes correctly as `windows-1255`, but a CP-862 file must
  be decoded as `cp862` or every Hebrew letter is garbled.
- **Dates are numeric YYYYMMDD** (`שדות מסוג תאריך יהיו שדות נומריים באורך 8 תווים ובמבנה YYYYMMDD`),
  not the DD/MM/YYYY that Hashavshevet screens and legacy files use.
- **Currency codes follow ISO 4217** (Appendix 2), unlike Hashavshevet's internal numeric codes.
- **Document type codes, Appendix 1** (only listed values are allowed): 100 order, 200 delivery
  note, 205 agent delivery note, 210 return note, 300 invoice / transaction invoice, 305 tax
  invoice, 310 summary invoice, 320 tax invoice / receipt, 330 credit tax invoice, 340 reserve
  invoice, 345 agent invoice, 400 receipt, 405 donation receipt, 410 cash withdrawal, 420 bank
  deposit, 500 purchase order, 600 purchase delivery note, 610 purchase return, 700 purchase tax
  invoice, 710 purchase credit, 800 opening balance, 810 general stock-in, 820 general stock-out,
  830 inter-warehouse transfer, 840 stock-count adjustment, 900 production report in, 910
  production report out. The appendix notes that when a document's value is negative the effect is
  reversed. A revenue parser must net 330 against 305 / 320, and must not add 400 receipts to
  revenue when the matching 305 is already counted. The allocation API's own document table adds
  codes that are NOT in Appendix 1 (332 proforma / transaction account and 348 journal entry, both
  eligible for an allocation number, with 345 marked new) and marks 330 credit invoices as not
  needing one, so do not reject source data carrying 332 or 348 just because the 1.31 list lacks them.
- **Coming (not yet in production):** the ITA published "תוספת מס 1" to the 1.31 instructions
  (edition 1.0, 3.2026), requiring registered software to transmit the uniform file to the ITA via a
  dedicated API immediately after producing it; only the sandbox is exposed so far
  (<https://www.gov.il/BlobFolder/generalpage/hor-software-other/he/IncomeTax_software-houses-100326-1.pdf>).
  Check whether it is live before telling a user it is required.

## 7. Form 6111

An annex to the annual tax return carrying profit-and-loss, balance-sheet and tax-adjustment data,
filed online (<https://www.gov.il/he/service/itc6111>). A bookkeeper or CPA exports the trial
balance from Hashavshevet, maps each account to the 6111 line codes, and submits the annex. Confirm
the current line codes against the ITA's year-specific 6111 spec.
