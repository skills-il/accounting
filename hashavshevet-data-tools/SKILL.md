---
name: hashavshevet-data-tools
description: Not tax advice and not a filed return. Import and export data between Hashavshevet accounting software and modern formats (JSON, CSV, Excel). Use when you need to extract journal entries, chart of accounts, trial balances, or customer/supplier lists from Hashavshevet, import bank transactions and invoices into Hashavshevet format, migrate data from Hashavshevet to cloud-based solutions (iCount, Rivhit, Invoice4U), handle Hebrew encoding conversions (Windows-1255 to UTF-8), or produce and validate the Tax Authority uniform-structure file (BKMV, kovetz ahid) and PCN874 from Hashavshevet data, with date-scoped allocation-number checks. Supports legacy Hashavshevet Windows installations (Gold, 2000+), H-ERP and H-WEB (Hashavshevet in the cloud). Validates data integrity during import/export operations. Do NOT use for real-time Hashavshevet API integrations, direct database modifications, or live bookkeeping within Hashavshevet.
license: MIT
allowed-tools: Bash(python:*) Read Edit Write
compatibility: Requires Python 3.9+ with openpyxl and chardet libraries
---


# Hashavshevet Data Tools

## Legal notice

This is a free information tool operated by an AI model. It helps export, import, convert and technically validate bookkeeping data from Hashavshevet, including uniform-structure (BKMV) files and PCN874 files, without the involvement, review or approval of an accountant (CPA) or tax adviser. The output is not tax advice, not a return filed with the Israel Tax Authority, and not an audit or certification of financial statements; it is technical processing of data the user supplies. The tool does not decide questions of input-VAT deductibility, VAT classification of a transaction, deferral of detailed-reporting duty, or a binding Form 6111 mapping, and an AI model can err, drop records or reach a wrong conclusion. Do not submit any file or report to the Tax Authority without checking it in the ITA simulator and with a professional. Responsibility for reporting and paying tax is yours, the binding calculation is the Tax Authority's, and representation before the Tax Authority is reserved to those permitted by law. This tool is not a substitute for advice that takes into account each person's particular data and needs, and any use of the output is at the user's sole responsibility.

## Instructions

> **Important: use the official OPENFORMAT/BKMV export, not direct binary parsing.**
>
> Hashavshevet does NOT publish public per-byte offsets for its internal `.dat` / `.hsh` / `.mdb` files. The publicly documented and ITA-mandated export from any Israeli bookkeeping software is **OPENFORMAT (קובץ אחיד / BKMV)**. The export produces a ZIP of three files: `INI.TXT` (production summary, holds the leading `A000` record plus per-record-type control-count summary records), `BKMVDATA.TXT` (the business data, with one `A100` opening record, then `C100`, `D110`, `D120`, `B100`, `B110`, `M100` records, then one `Z900` closing record), and `README.TXT` (general production details for the user). Only `INI.TXT` and `BKMVDATA.TXT` are sent to the ITA or the CPA. Spec: the ITA "הוראות להפקת קבצים" document, current version 1.31, at <https://www.gov.il/BlobFolder/service/registration-software-designed-managing-computerized-accounting-system/he/Service_Pages_Income_tax_horaot-131.pdf>. Hashavshevet's BKMV export guide: <https://downloads.h-erp.co.il/files/general/bkmv7-erp.pdf>. Validate output against the ITA simulator: <https://secapp.taxes.gov.il/TmbakmmsmlNew/frmCheckFiles.aspx>. The simulator states it accepts version 1.31 files only.
>
> The fixed-width column maps below (HESHIN_COLUMNS / PKUDOT_COLUMNS) are **best-guess heuristics for legacy Windows installations**, not authoritative specifications. Use them only as a fallback when no OPENFORMAT export is available; never claim them as the canonical Hashavshevet format. For any ITA filing, CPA handoff, or PCN874 / Form 6111 generation, export via OPENFORMAT instead.

> **Hashavshevet בענן (H-WEB / Wizcloud) public REST API.** The cloud version of Hashavshevet exposes a public REST API. The API reference lives at <https://docs.wizcloud.co.il/docs/intro> (current version 2.0.0), covering resources such as documents, journal, mainaccount, receipts, bankstatements, currencies and triggers. Use this for ongoing two-way sync with Green Invoice / Rivhit / iCount instead of one-shot file dumps where possible.

> **SHAAM allocation-number context (2026).** Sales-invoice journal entries created/imported through Hashavshevet for B2B amounts exceeding the current threshold must carry an allocation number (mispar haktza'a). The number is NOT a fixed 9 digits: the full number is up to 30 characters (the ITA's examples are 26 digits), and the SHORT allocation number is its rightmost 9, which is what the invoice prints prominently and what PCN874 carries. Accept either shape, match two numbers on their rightmost 9 digits, and store the value as text (a 26-digit number does not survive a float or Excel numeric cell). See `references/ita-filings.md`. The regime began on 5 May 2024. Thresholds (VAT excluded), and you need the WHOLE table because migrated data spans several years: NIS 25,000 from 5 May 2024, NIS 20,000 from January 2025, NIS 10,000 from January 2026, NIS 5,000 from June 2026. Invoices dated before 5 May 2024 predate the regime entirely and never needed an allocation number. The requirement is date-dependent (phased in with a descending threshold), so when validating HISTORICAL or migrated invoices, scope the check to each invoice's own DOCUMENT date (in a BKMV file, C100 field 1230, never the system production date 1205) against the threshold in force on that date, and skip invoices dated before the requirement began. Do NOT blanket-reject older invoices that never needed an allocation number, and do NOT apply today's NIS 5,000 threshold to a 2025 invoice that only needed one above NIS 20,000, or to a 2024 invoice whose threshold was NIS 25,000.
>
> **Where each row comes from:** the two 2026 rows are in the consolidated text of s.38(א1) itself, the 2025 row is on the Tax Authority's own service page, and only the NIS 25,000 row rests on the amendment history plus independent secondary sources. Say so when you cite it; the full provenance note is in `references/ita-filings.md`.
>
> **Two separate rules govern the allocation number, and conflating them is the classic error.** The SELLER'S duty to obtain a number is s.47(א2)(1): it arises only at the buyer's demand and does not reach a zero-rated transaction, "ובעסקה שסכומה, בלא המס, עולה על הסכום האמור בסעיף 38(א1), חייב הוא לעשות כן לפי דרישת הקונה; הוראות סעיף קטן זה יחולו לעניין חשבונית מס שהוצאה בשל עסקה שהמס שחל לגביה אינו בשיעור אפס". The BUYER'S loss of the input-VAT deduction is s.38(א1), and it has NO buyer-request condition at all, "לא יותר ניכוי מס התשומות הכלול בחשבונית מס שסכומה, בלא המס, עולה על 5,000 שקלים חדשים (מינואר 2026 ועד מאי 2026: 10,000 שקלים חדשים) ושאינה כוללת מספר שהקצה לה המנהל". So NEVER treat "the buyer never asked" as a pass: flag every tax invoice above that date's threshold that carries a VAT component and has no allocation number, because the recipient loses the deduction either way. The buyer's demand decides whether the SELLER breached a duty; it has nothing to do with whether the BUYER can deduct. Note also that s.38(א1) says `עולה על` (EXCEEDS), so an invoice sitting exactly on a band figure is outside the rule. Zero-rated and exempt-only invoices ARE outside the requirement, so do not flag an export invoice however large. Treat a missing allocation number on a qualifying invoice as a hard validation error, not a soft "incomplete" warning. The precise effect: it blocks the RECIPIENT's input-VAT deduction. It does not, by itself, make the invoice void. On the buying side, capture and retain the allocation number printed on each qualifying supplier invoice and carry it into the ledger and PCN874, that is what protects your client's own input-VAT deduction. The OPENFORMAT/BKMV uniform file (spec 1.31) has NO allocation-number field at all, so a migration through BKMV silently drops every allocation number: extract them separately and load them into a dedicated field in the target. Hashavshevet בענן has built-in real-time SHAAM integration; the Windows version may need a separate workflow.
>
> **VAT rate is date-dependent too, so scope it the same way.** The standard Israeli VAT rate is currently 18% and there is no reduced rate; the 2026 budget kept it at 18%, and a proposed cut to 17% was rejected. The rate was 17% through 31 December 2024 and 18% from 1 January 2025, so a dataset spanning 2024-2026 crosses a rate change. When deriving net-from-gross or VAT-from-gross on migrated documents, apply the rate in force at the DOCUMENT date, never a single hardcoded rate (for a supply that straddles 31 December 2024, such as a January 2025 invoice for a December 2024 delivery, FLAG the line rather than recompute it, since the tax point can differ from the document date); otherwise the עסקאות and תשומות totals in a PCN874 built from that data will be wrong, and the ITA cross-references those against the counterparty.

> **When a request for an allocation number is REJECTED**, it is not a dead end: the osek has four options (cancel, proceed without a number so the recipient loses the deduction and the invoice must say so, reverse charge, or a hearing; the hearing and any objection carry deemed-granted deadlines). Surface them; the options and timeline are in `references/ita-filings.md`.

### Step 1: Identify the Hashavshevet version and file format

Determine which version of Hashavshevet the user is working with and identify the relevant file formats:

- **Legacy Hashavshevet (Windows, on-prem)**: Stores data in a proprietary ISAM or SQL backend. Direct binary parsing is unsupported and brittle; use the built-in OPENFORMAT export instead.
- **Hashavshevet H-ERP (current Windows ERP)**: Standard product line as of 2026; the current release is designated mahadura 2026a rather than a numeric version. Exports OPENFORMAT/BKMV for ITA + CPA workflows; legacy `.dat` / `.hsh` files may still appear in archives.
- **Hashavshevet בענן (H-WEB / Wizcloud, SaaS)**: Cloud-native, exports OPENFORMAT directly, plus a public REST API for live integration.
- "Gold" / "2000+" naming is from 1990s/2000s legacy product lines; H-ERP / H-WEB are the current names.

Common Hashavshevet data files:

| File / Table | Hebrew Name | Description | Typical Format |
|---|---|---|---|
| `HESHIN.dat` | מאזן חשבונות | Chart of accounts | Fixed-width, Windows-1255 |
| `PKUDOT.dat` | פקודות יומן | Journal entries | Fixed-width, Windows-1255 |
| `MANOT.dat` | מנות | Batches | Fixed-width, Windows-1255 |
| `KARTIS.dat` | כרטיסי חשבון | Account cards / ledger | Fixed-width, Windows-1255 |
| `HESHBON.dat` | חשבונות | Account master list | Fixed-width, Windows-1255 |
| `MATZAV.dat` | מצב חשבון | Account balances | Fixed-width, Windows-1255 |
| `TNUOT.dat` | תנועות | Transactions | Fixed-width, Windows-1255 |

### Step 2: Handle Hebrew encoding

Legacy Hashavshevet files and its CSV/Excel exports typically use Windows-1255 (Hebrew). Convert to UTF-8 before processing. For a BKMV file do not guess: read A000 field 1029 (see Example 4).

Read the bytes and decode as `windows-1255`. `chardet` can confirm it, but do not trust its guess over the domain rule: if detection returns `windows-1255`, `iso-8859-8`, `hebrew`, or nothing at all, use `windows-1255`. Decode with `errors='replace'` only when inspecting a suspect file; never when generating data you will import.


Common encoding pitfalls:
- Hashavshevet Gold always uses Windows-1255
- Some exports may use ISO-8859-8 (visual Hebrew) instead of logical Hebrew
- Mixed encoding files occur when data was copy-pasted from other sources
- BOM (Byte Order Mark) may be present in newer CSV exports

### Step 3: Parse legacy fixed-width files (fallback only)

If, and only if, no OPENFORMAT/BKMV export is available, see `references/legacy-fixed-width.md`
for the legacy `.dat` column maps and the parse/generate helpers. That file carries the safety
rules that go with them: the offsets are heuristics that vary by version, the parser must assert
an expected record length rather than silently truncating a short line, generated import files
need CRLF terminators and a constant record length, and encoding must be strict so an
out-of-CP1255 Hebrew character fails loudly instead of becoming `?` inside a customer name.
Never write a generated file into a live company; test against a copy.

### Step 4: Export data to modern formats

Convert parsed Hashavshevet data to JSON, CSV, or Excel:

Use the standard library and `openpyxl` for this; there is nothing Hashavshevet-specific about the writing step. Two Israeli-specific details that DO matter:

- **CSV for Excel must be `utf-8-sig`** (UTF-8 with BOM). Without the BOM Excel renders Hebrew as gibberish.
- **Set the worksheet to RTL** when writing XLSX: `ws.sheet_properties = WorksheetProperties(rightToLeft=True)` (from `openpyxl.worksheet.properties`), and use `ensure_ascii=False` for JSON so Hebrew stays readable.

### Step 6: Data migration to cloud solutions

When migrating from Hashavshevet to cloud-based accounting solutions:

**Before you start (read this first):**
- Migrating or exporting off Hashavshevet does NOT discharge the ניהול פנקסים retention duty. The accounting system and records must be retained 7 years from the end of the relevant tax year (or 6 years from the date the return was filed, whichever is later). Do NOT decommission or wipe the source Hashavshevet system after the cutover; keep it (or a complete archived copy) accessible for that full period. Retention is not merely keeping bytes: you must be able to PRODUCE the uniform-structure file on an inspector's demand, so archived `.dat` files whose reader has been decommissioned do not satisfy it, a backup copy must be kept separately from the production copy, and the external documentation (תיעוד חוץ: invoices, receipts, delivery notes) is covered as well as the ledger. The safe practical step is to produce and archive a validated BKMV export for every retained tax year AT the cutover, while the licence is still live.
- Where the target system supports it, import the native BKMV uniform file directly (יבוא נתונים מקובץ במבנה אחיד). Rivhit and other cloud systems accept the uniform file as-is. This is preferred over hand-mapped CSV/Excel because it preserves document-number continuity and the ITA-defined field structure.
- Preserve document-numbering continuity (מספר עוקב) across the cutover so each document type keeps an unbroken running number.
- Reconcile the new system's opening trial balance to the old system's closing trial balance before going live; investigate any difference rather than rounding it away.
- Payroll is not the only continuity trap. Withholding (תיק ניכויים) is a SEPARATE ITA file with its own monthly 102 deposits and two annual reconciliations, טופס 126 (employees) and טופס 856 (suppliers subject to ניכוי במקור). Both are cumulative full-year reports filed by 30 April of the following year, and form 126 must reconcile to the monthly 102 forms and is filed with the National Insurance Institute as well, so a mid-year cutover leaves the new system holding only part of the year and the reconciliation will not tie. Extract the year-to-date withholding register per employee and per supplier and load it as opening cumulative data, or file the transition year from the old system.
- Extract these too, none of which travel in a trial balance: the fixed-asset register with cost, accumulated depreciation and rates (needed for the depreciation annex and the 6111 balance sheet, and many cloud targets cannot hold a depreciation register at all, in which case it must be maintained outside the system); closing inventory and its valuation basis; prior-year comparatives (the annual return and 6111 require them); foreign-currency open balances with their ORIGINAL-currency amounts and revaluation basis; and postdated cheques (שיקים דחויים) held and issued, which are ledger balances in Israeli practice.
- Preserve the per-account 6111 / kod-miyun mapping field. Israeli packages including Hashavshevet store it on the account card precisely so the mapping is done once; in a BKMV file it is B110 field 1417 (4 digits, mandatory when the taxpayer must report 6111). A hand-mapped CSV migration drops it unless the mapping file carries it, which forces the whole 6111 mapping to be rebuilt by hand.
- Migrate each supplier's withholding-at-source rate and its validity dates with the supplier master (the assessing officer sets the rate per osek, and it can be checked online by osek number), and configure the same withholding file number (BKMV A000 field 1016). Otherwise the first post-cutover payment run withholds at the wrong rate.
- Re-establish the ITA token in the target before the first post-cutover VAT filing if PCN874 is transmitted from the software.
- Confirm the TARGET system can itself produce a conforming uniform-structure (BKMV) file before cutting over. If it cannot, the client will be unable to satisfy an inspector's demand, which also defeats the retention plan below.
- The OPENFORMAT/BKMV uniform file does NOT contain payroll/salary records, only the bookkeeping and document data. A full company migration must separately extract payroll history (via Hashavshevet's payroll module / the annual payroll-reporting workflow); relying on the uniform file alone silently drops payroll.

**iCount migration:**
- Export chart of accounts, then map account numbers to iCount categories
- Export open invoices and customer/supplier balances
- iCount accepts CSV imports with specific column headers

**Rivhit migration:**
- Export full journal for the current fiscal year
- Map Hashavshevet account types to Rivhit's account classification
- Rivhit accepts Excel imports with predefined templates

**Invoice4U migration:**
- Focus on customer/supplier master data and open balances
- Export invoice history for reference (Invoice4U does not import historical journals)
- Use Invoice4U's API for programmatic data import

**Green Invoice migration:**
- Map customer/supplier master data and open balances, then import via Green Invoice's CSV templates or its API
- For an ongoing two-way sync (rather than a one-shot dump), prefer the cloud REST APIs on both sides and see the companion `green-invoice` skill

### Step 6.5: ITA filings (PCN874 and Form 6111)

Two ITA filings are commonly produced from Hashavshevet data. Both are software-independent specs, so generate them from an OPENFORMAT export rather than from heuristic binary parsing:

- **PCN874 (דוח מפורט מע"מ, detailed VAT report)**: a fixed-structure text file, NOT a flat invoice list: an opening record, then transaction records keyed by type (sales עסקאות vs inputs תשומות), then a closing record. In each transaction record amounts are whole shekels, the invoice amount is the amount EXCLUDING VAT (the full amount even where only part of the input VAT is deductible), always positive, with the sign in a separate `+`/`-` field (credits always minus), and the 9-digit short allocation number has its own mandatory field on both the sales and the input side. Building it from gross document totals overstates every line by the VAT rate. For an input transaction the supplier's osek number is mandatory or the input VAT cannot be deducted. The duty is NOT a single turnover test on individuals: companies with turnover above NIS 500,000 from the September 2025 period, an individual osek above NIS 500,000 from 1 January 2026, with reliefs for individuals only (a combined total for invoices of NIS 5,000 or less with placeholder 777777772, and deferral to 1 January 2027 on application). Becoming a detailed filer also moves the business to MONTHLY reporting, due by the 23rd for online filing. Hashavshevet has a built-in PCN874 export and, from mahadura 2026a, can transmit it to the ITA directly. The record layout, the reliefs and their two alternative 90% tests are in `references/ita-filings.md`.
- **Form 6111 (טופס 6111, דוח התאמה למס, tax-adjustment report)**: an annex to the annual tax return carrying profit-and-loss, balance-sheet, and tax-adjustment data, filed online. Map each account to the year-specific 6111 line codes (see Reference Links).

### Step 7: Validate data integrity

After any import or export operation, validate data integrity. **Caveat on `validate_trial_balance` (in `references/legacy-fixed-width.md`):** in the paired debit+credit-per-row PKUDOT format it sums the same `amount` into both totals, so it is balanced by construction and CANNOT catch sign flips, wrong amounts, transposed digits, or a missing counter-leg. Treat it as a coarse smoke test only. Real balancing must come from the ITA file-check simulator (for an OPENFORMAT export) or a B100 debit-vs-credit movement check, not from this function, and do not present its "balanced" result to an auditor as assurance.

The `validate_trial_balance` and `validate_account_references` helpers are in `references/legacy-fixed-width.md`. `validate_account_references` (every referenced account exists in the chart of accounts) is the more useful of the two.

## Examples

### Example 1: Export journal entries from Hashavshevet to Excel

User says: "I have a PKUDOT.dat file from an old Hashavshevet Windows installation. I need to export all journal entries from 2025 to an Excel file for my auditor."

Actions:
1. Read the `PKUDOT.dat` file and detect encoding (Windows-1255)
2. Convert content from Windows-1255 to UTF-8
3. Parse the fixed-width data using the PKUDOT column layout
4. Filter records where `entry_date` falls within 01/01/2025 to 31/12/2025
5. Export filtered records to Excel with RTL formatting and Hebrew column headers
6. Do NOT run `validate_trial_balance` here and present its result as assurance: in this paired debit+credit-per-row format it is balanced by construction (see the Step 7 caveat). If the auditor needs a balance assertion, produce it from an OPENFORMAT export checked in the ITA simulator, or from a B100 debit-vs-credit movement check

Result: An Excel file `pkudot_2025.xlsx` with all 2025 journal entries, properly formatted with Hebrew headers and RTL sheet direction.

### Example 2: Import bank transactions into Hashavshevet format

User says: "I downloaded bank transactions from Leumi as a CSV. I need to convert them into a format I can import into Hashavshevet 2000+."

Actions:
1. Read the Bank Leumi CSV file (UTF-8 with BOM)
2. Map bank CSV columns to Hashavshevet PKUDOT fields: date to `entry_date`, description to `description`, amount to `amount`, reference number to `reference`
3. Assign debit/credit accounts based on transaction direction, but do NOT treat the bank-line sign as a reliable income/expense classifier. A deposit is often a customer receipt against A/R (or a loan, VAT refund, owner capital, inter-account transfer), and a withdrawal is often a supplier payment against A/P (or salary, drawings, loan repayment), not P&L. Post receipts and payments against the open A/R / A/P sub-ledger unless the line is verified as income or expense; blindly crediting income on every deposit double-counts revenue for any accrual-basis business and misstates income tax
4. Generate sequential entry numbers and assign to the current batch
5. Format dates from YYYY-MM-DD (bank format) to DD/MM/YYYY (Hashavshevet format)
6. Write the output as a fixed-width `.dat` file in Windows-1255 encoding
7. Validate all generated entries for data integrity

Result: A `bank_import.dat` file ready for import into Hashavshevet 2000+, with 47 transactions properly formatted, encoded in Windows-1255, and validated.

### Example 3: Migrate chart of accounts from Hashavshevet to Rivhit

User says: "We're moving from Hashavshevet Gold to Rivhit. I need to export our chart of accounts and opening balances in a format Rivhit can import."

Actions:
1. Read and parse `HESHIN.dat` (chart of accounts) and `MATZAV.dat` (account balances) from Hashavshevet
2. Convert encoding from Windows-1255 to UTF-8
3. Map Hashavshevet account types (1-5) to Rivhit account classifications
4. Merge account balances with account master data
5. Generate a Rivhit-compatible Excel template with columns: account number, account name, account type, opening balance, currency
6. Apply Rivhit's naming conventions and validation rules
7. Create a mapping reference document showing old Hashavshevet account numbers alongside new Rivhit account IDs

Result: A Rivhit-compatible Excel import file with 234 accounts, a mapping reference document, and a summary of 12 accounts that need manual review due to type classification differences.

### Example 4: Produce an OPENFORMAT (BKMV) export for an ITA filing or CPA handoff

User says: "My CPA asked for a BKMV / kovetz ahid (uniform structure) export from Hashavshevet for the 2025 tax year. How do I produce it and confirm it is valid before I send it?"

Actions:
1. Run Hashavshevet's built-in BKMV export (H-ERP: the uniform-structure export wizard; H-WEB / Wizcloud: the BKMV export screen) for the 2025 date range. One file covers one year. The wizard asks for the PURPOSE: the ITA purpose cuts journal entries by reference date OR value date, the CPA purpose by reference date only, so use the ITA purpose for an inspector or a retention archive, and set the batch 9998 (income-transfer) cut deliberately. This produces a ZIP of three files: `INI.TXT` (production summary, with the `A000` leading record and the per-record-type control-count summary records), `BKMVDATA.TXT` (the business data), and `README.TXT` (general production details). Only `INI.TXT` and `BKMVDATA.TXT` are sent onward.
2. Read the character-set field (1029) of the `A000` record in `INI.TXT` first: 1 = ISO-8859-8-i (Windows, decode as `windows-1255`), 2 = CP-862 (DOS, decode as `cp862`). Convert to UTF-8 before any inspection. Dates inside the file are YYYYMMDD, and the document-type codes (305 tax invoice, 330 credit tax invoice, 400 receipt and the rest) are listed in `references/ita-filings.md`; net 330 against sales rather than adding it.
3. Walk the record types in `BKMVDATA.TXT`: `A100` opening record, `C100` document headers, `D110` document line details, `D120` receipt/deposit details, `B100` accounting journal transactions, `B110` accounting accounts, `M100` inventory items, and `Z900` closing record (record-type code in the first field of each line). Note: `A000` is NOT in this file, it lives in `INI.TXT`.
4. Sanity-check the structure: the 15-digit primary identifier must be identical in A000 field 1004, A100 field 1103 and Z900 field 1153; every record must have its fixed length (for example C100 444, B100 317; full table and a worked count check in `references/ita-filings.md`); invoice-type `C100` documents should have matching `D110` lines and receipts `D120` lines; A000 field 1002 must equal Z900 field 1155, the total record count INCLUDING the A100 opening and Z900 closing records, while the `INI.TXT` summary records count only the other record types present (so they sum to 1155 minus 2) and must match what you actually count, and `B100` debit and credit movements should balance.
5. Validate the ZIP against the ITA file-check simulator (see Reference Links) and save the simulator's feedback report.
6. Hand the validated `INI.TXT` plus `BKMVDATA.TXT` (with the simulator report) to the CPA, or attach them to the relevant ITA submission.

Result: A validated BKMV export for the 2025 tax year (`INI.TXT` + `BKMVDATA.TXT`, drawn from the three-file ZIP) that passes the ITA simulator, ready for the CPA or ITA.

## Gotchas

- Hashavshevet files use Windows-1255 encoding, not UTF-8. Agents will almost always attempt to read these files as UTF-8, causing UnicodeDecodeError on the first Hebrew character encountered.
- Hashavshevet date format is DD/MM/YYYY (Israeli standard). Bank exports may use YYYY-MM-DD (ISO) or MM/DD/YYYY (US). Agents may not detect the format mismatch, causing dates like 03/04/2025 to be interpreted incorrectly.
- Fixed-width column positions vary between Hashavshevet versions (Gold vs. 2000+ vs. newer). Agents may apply column layouts from one version to data from another, producing garbled output.
- Hashavshevet uses internal numeric currency codes that differ from ISO 4217 (the OPENFORMAT file itself uses ISO 4217). The exact mapping varies by installation, so confirm it against your installation's currency table rather than assuming fixed values. Agents that blindly use ISO 4217 codes will produce values Hashavshevet rejects on import.
- When exporting to CSV for Excel, files must use UTF-8 with BOM (utf-8-sig) encoding. Without the BOM, Excel will not display Hebrew characters correctly, showing gibberish instead.
- In OPENFORMAT, for a foreign-currency movement the record should carry both the NIS amount and the original-currency amount (the spec provides currency fields for this), so do not drop the original-currency value when converting. Very large `BKMVDATA.TXT` files may be rejected by the simulator or downstream importer and need splitting into smaller date ranges.
- Hashavshevet 2026a's "minimum amount for allocation" setting holds the minimum VAT amount (900 at NIS 5,000 and 18%), not the pre-VAT threshold. Compare it with an invoice's VAT, never its net amount.


## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Hashavshevet H-ERP official | https://www.h-erp.co.il | Hashavshevet product versions (current Windows release: mahadura 2026a), file format guides |
| Wizcloud REST API reference | https://docs.wizcloud.co.il/ | Endpoint reference for Hashavshevet בענן (v2.0.0): documents, journal, receipts, bankstatements |
| ITA notice pa280825-1 | https://www.gov.il/he/pages/pa280825-1 | PCN874 individual-osek reliefs: the two alternative 90% deferral tests, the 777777772 placeholder, and the company / already-filing carve-outs |
| ITA allocation-number service page | https://www.gov.il/he/service/request-assignment-number-for-tax-invoice | Current threshold and the 2025 / Jan 2026 / Jun 2026 rows |
| ITA Israel Invoice API spec (ed. 2.0) | https://www.gov.il/BlobFolder/generalpage/hor-software-other/he/vat_software-houses-180724.pdf | Full (A30) vs short (rightmost 9) allocation number; PCN874 transaction-record fields |
| Allocation-number conditions + rejection path | https://www.grantthornton.co.il/insights1/tax-insignths/2026/From_June_the_allocation_number/ | The conditions, and the four options when a request is refused |
| Israel Tax Authority | https://www.gov.il/en/departments/israel_tax_authority | Digital bookkeeping directive, required journal fields |
| ITA OPENFORMAT / מבנה אחיד spec (v1.31) | https://www.gov.il/BlobFolder/service/registration-software-designed-managing-computerized-accounting-system/he/Service_Pages_Income_tax_horaot-131.pdf | All 9 BKMV record types (A000 in INI.TXT; A100, B100, B110, C100, D110, D120, M100, Z900 in BKMVDATA.TXT), field offsets. The old misim.gov.il direct link redirects into the ITA login and serves HTML |
| Hashavshevet H-ERP BKMV guide | https://downloads.h-erp.co.il/files/general/bkmv7-erp.pdf | How to run the uniform-structure export, INI.TXT + BKMVDATA.TXT |
| ITA file-check simulator | https://secapp.taxes.gov.il/TmbakmmsmlNew/frmCheckFiles.aspx | Validate a BKMV ZIP before CPA / ITA handoff; accepts version 1.31 files only |
| Form 6111 (tax-adjustment report) | https://www.gov.il/he/service/itc6111 | Annual-return annex line codes (P&L, balance sheet, tax adjustment) |
| openpyxl documentation | https://openpyxl.readthedocs.io/en/stable/ | Writing XLSX files from Python, styled export |
| pandas I/O reference | https://pandas.pydata.org/docs/reference/io.html | CSV/Excel import and export, encoding handling |
| CP1255 encoding table (unicode.org) | https://unicode.org/Public/MAPPINGS/VENDORS/MICSFT/WINDOWS/CP1255.TXT | Windows-1255 to UTF-8 Hebrew character mapping |

## Troubleshooting

### Error: "UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9"
Cause: The file is encoded in Windows-1255 (Hebrew) but is being read as UTF-8. This is the most common error when working with Hashavshevet files, as the software uses Windows-1255 by default.
Solution: Explicitly specify `encoding='windows-1255'` when reading the file. If unsure about the encoding, use the `chardet` library to auto-detect it. For files with mixed encoding, use `errors='replace'` to substitute undecodable characters.

### Error: "Trial balance is not balanced (difference: X.XX)"
Cause: Rounding differences from currency conversions, partial exports (missing entries from a batch), or corrupted data in the source file. Hashavshevet sometimes stores amounts with extra decimal places internally.
Solution: First check if the difference is a small rounding error (less than one shekel). If so, create an adjustment entry. For larger differences, verify the export includes all batches for the period. Re-export from Hashavshevet using the "full export" option rather than filtered export.

### Error: "Account number not found in chart of accounts"
Cause: Journal entries reference accounts that were deleted or renumbered in Hashavshevet, or the chart of accounts export is from a different fiscal year than the journal entries.
Solution: Export both the chart of accounts and journal entries from the same Hashavshevet database and fiscal year. If accounts were renumbered, create a mapping table and update references before import. Check for leading zeros being stripped during conversion.

### Error: "Date format mismatch during import"
Cause: Hashavshevet expects DD/MM/YYYY (Israeli format) but the source data uses MM/DD/YYYY (American format) or YYYY-MM-DD (ISO format). This commonly occurs when importing bank data or data from international systems.
Solution: Normalize all dates to DD/MM/YYYY before generating the import file. Check for ambiguous dates where day and month could be swapped (e.g., 03/04/2025 could be March 4 or April 3) and verify against the source system's format.
