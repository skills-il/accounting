---
name: israeli-bank-reconciliation
description: Not accounting or tax advice. Automates bank reconciliation for Israeli banks and credit-card issuers (Leumi, Hapoalim, Discount, Mizrahi Tefahot, Beinleumi/FIBI, Otsar Hahayal, Mercantile, Massad, Yahav, OneZero, and the card issuers Isracard, Max, Visa Cal, Amex) using the israeli-bank-scrapers library. Matches scraped or imported transactions to invoices and receipts, detects discrepancies, and generates reconciliation reports with matched, unmatched, and suspicious entries. Handles shekel amounts, Hebrew merchant names, and Israeli date formats. Use when you need to reconcile bank statements against your accounting records, identify missing invoices, or prepare monthly closing reports for Israeli business accounts. Do NOT use for international bank accounts, cryptocurrency wallets, or investment portfolio reconciliation.
license: MIT
---


# Israeli Bank Reconciliation

Automate the process of reconciling Israeli bank transactions against your accounting records. This skill leverages the open-source `israeli-bank-scrapers` library to fetch transactions and provides a structured workflow for matching, discrepancy detection, and report generation.

## Legal notice

This is a free information tool operated by an AI model. It matches bank lines against accounting records and explains the bookkeeping and VAT rules involved. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by a tax adviser or accountant. A reconciliation it produces is not an audited reconciliation, not a tax opinion, and not professional advice, but a general working paper only: it does not examine the full extent of your income or your complete documents. An AI model may err, omit data, or present a wrong conclusion.

Any classification it makes, including whether an expense's input VAT may be deducted or whether an invoice required an allocation number, is an automatic draft for your own preparation and is not a determination. Responsibility for reporting and for paying the tax is yours, the binding computation is the Tax Authority's, and representation before the Tax Authority is reserved to those permitted by law. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person. Have a tax adviser or accountant review the reconciliation before you rely on it for filing. All use of its output is the user's sole responsibility.


## Instructions

### Step 1: Set Up the Environment

Install the required dependencies for bank scraping and data processing.

```bash
npm init -y
npm install israeli-bank-scrapers csv-parse csv-stringify dayjs
```

If you plan to import a file instead of scraping, note what Israeli banks actually
export. In practice they offer Excel (.xls/.xlsx) and CSV downloads; OFX is not a
native export format at the Israeli retail banks, so treat CSV/Excel as the default
file path and reach for OFX only if the user already has an aggregator or accounting
package that emits it:

```bash
# CSV is the realistic import path (csv-parse is already installed above)
# For an Excel download, have the user "Save As" CSV in Excel or Sheets first,
# which avoids pulling in an extra spreadsheet parser.

# Only if the user genuinely has OFX files from an aggregator
npm install ofx-js
```

For reference, the core scraping library is maintained at: https://github.com/eshaham/israeli-bank-scrapers

For users who want automated budget tracking alongside reconciliation, consider Caspion: https://github.com/brafdlog/caspion

### Step 2: Configure Bank Credentials

**Credential fields differ per provider.** There is no single shape. Using Hapoalim's fields against Leumi will simply fail to log in, and repeated failed logins can lock the online-banking account, so get this right before the first run:

| Provider | Credential fields |
|---|---|
| `hapoalim` | `userCode`, `password` |
| `leumi`, `mizrahi`, `otsarHahayal`, `beinleumi`, `massad`, `max`, `visaCal`, `union`, `pagi` | `username`, `password` |
| `behatsdaa`, `beyahadBishvilha` | `id`, `password` |
| `discount`, `mercantile` | `id`, `password`, `num` |
| `isracard` | `id`, `card6Digits`, `password` |
| `amex` | `id`, `card6Digits`, `password` |
| `yahav` | `username`, `password`, `nationalID` |

`oneZero` is the exception: it takes five fields (`email`, `password`, `otpCodeRetriever`, `phoneNumber`, `otpLongTermToken`), and `otpCodeRetriever` is a FUNCTION rather than a string, so it cannot be built from env vars and must not fall through to the default. **Never guess the shape for a provider that is not in the table**: sending `username` to a provider expecting `id` produces a well-formed but wrong request, the login fails, and it counts toward account lockout. Throw instead of guessing. Check the library README for the provider you actually use before running, since these can change between major versions.

**Read the credentials from the environment at runtime.** A JSON file does NOT expand `${VAR}`: if you write `"password": "${BANK_PASSWORD}"` the scraper sends the literal string `${BANK_PASSWORD}` to the bank as your password, which fails and counts against the lockout threshold. Keep only non-secret routing in the config file:

```json
{
  "accounts": [
    { "id": "main-business", "companyId": "hapoalim", "credentialsEnvPrefix": "HAPOALIM" }
  ]
}
```

The full 19-provider credential table, the fail-closed credential builder, and the `ScraperOptions` that affect a reconciliation are in `references/bank-scrapers-credentials.md`. Never guess the field shape for a provider that is not listed there.


The loop throws on a missing field rather than sending an empty or literal placeholder value to the bank. Stop after a single authentication failure rather than retrying in a loop: Israeli banks lock online-banking access after a small number of failed attempts.

Supported bank identifiers (these strings must match the `CompanyTypes` enum in `israeli-bank-scrapers` exactly; the enum uses camelCase, so a kebab-case value like `otsar-hahayal` throws at runtime when passed to `createScraper`):
- `hapoalim` - Bank Hapoalim
- `leumi` - Bank Leumi
- `discount` - Discount Bank
- `mizrahi` - Mizrahi Tefahot
- `otsarHahayal` - Otsar Ha-Hayal
- `beinleumi` - First International Bank (FIBI / Beinleumi)
- `mercantile` - Mercantile Discount Bank
- `max` - Max (formerly Leumi Card)
- `visaCal` - Visa Cal
- `isracard` - Isracard

- `amex` - American Express
- `massad` - Massad
- `yahav` - Bank Yahav
- `oneZero` - OneZero (marked experimental in the library)

Card issuers matter as much as banks here: a single bank line is usually the monthly aggregate charge from Isracard, Max, Visa Cal or Amex, and reconciling it means pulling that issuer's own transaction list and matching the sum. Always copy the identifier verbatim from the enum rather than guessing the casing, and check the library's README for the current list, since providers are added and occasionally deprecated.

Store actual credentials in environment variables, not in the config file.

### Step 2a: Understand what scraping costs you, and consider the licensed route first

Before setting any of this up, tell the user plainly what the scraping path involves, because it is not a read-only token:

- **You are handing full online-banking credentials to a script** that logs in as you through a headless browser. That is not the same as an API key, and it cannot be scoped or revoked independently of your own access.
- **Bank terms of service.** Israeli online-banking agreements generally restrict disclosing credentials to third parties and automated access. Doing it anyway can shift liability for fraudulent activity onto the customer. This is a contractual and risk question, not a criminal one, but it is real and the user should make the decision knowingly.
- **Lockout.** Repeated failed logins lock the account. Validate credentials before the run and stop on the first authentication failure.
- **Two-factor authentication.** Where the bank enforces 2FA on every login, unattended scraping largely does not work. There is no generic OTP option in the scraper configuration; support is per-provider and limited. Do not promise the user a config flag that does not exist.
- **The scraped data is sensitive at rest.** A full period of business transactions with counterparty names lands in local CSV/JSON. Keep it out of version control, restrict file permissions, and delete working copies when the reconciliation is signed off. For a business handling counterparty data this also engages Privacy Protection Law obligations.

**There is a licensed alternative, and for a business account it is the better production path.** Israel's Financial Information Service Law established a regulated open-banking regime, supervised by the Israel Securities Authority, under which a licensed provider accesses account data through open interfaces **without the customer exposing their banking credentials**. Business accounts have been in scope since December 2023, and the regulator has since issued implementation directives to payment companies. If the user is setting this up for an ongoing business process rather than a one-off, point them at a licensed aggregator before pointing them at a scraper.

### Step 3: Fetch Bank Transactions

Create a scraping script that fetches transactions for a configurable date range.

```javascript
const { createScraper } = require('israeli-bank-scrapers');

async function fetchTransactions(bankId, credentials, startDate) {
  const scraper = createScraper({
    companyId: bankId,
    startDate: startDate,
    combineInstallments: false,
    showBrowser: false
  });

  const result = await scraper.scrape(credentials);

  if (!result.success) {
    throw new Error(`Scrape failed: ${result.errorType} - ${result.errorMessage}`);
  }

  return result.accounts.flatMap(account =>
    account.txns.map(txn => ({
      date: txn.date,                     // value date
      processedDate: txn.processedDate,   // posting date: THIS is the bank-side key
      amount: txn.chargedAmount,
      originalAmount: txn.originalAmount,
      originalCurrency: txn.originalCurrency,
      description: txn.description,
      memo: txn.memo || '',
      // identifier is a NUMBER (or undefined) in the library. Coerce to string,
      // because the accounting side holds a string reference and a raw === between
      // a number and a string is always false, which silently kills exact matching.
      reference: txn.identifier != null ? String(txn.identifier) : '',
      status: txn.status,                 // 'completed' | 'pending'
      accountNumber: account.accountNumber
    }))
  );
}
```

Two filters you must apply before reconciling, or the period will never tie out:

```javascript
// 1. Posted only. Pending rows are not on the statement balance.
const posted = txns.filter(t => t.status === 'completed');

// 2. Close the period. createScraper takes startDate but NOT an endDate, so the
//    scrape runs to today and will drag next month's rows into a closed period.
const inPeriod = posted.filter(t => {
  const d = new Date(t.processedDate || t.date);
  return d >= periodStart && d <= periodEnd;
});
```

### Step 4: Import Accounting Records

Load your invoices and receipts from CSV, or connect to your accounting system. The reconciliation expects records in a normalized format.

Expected accounting record format:

| Field | Type | Description |
|-------|------|-------------|
| `date` | `YYYY-MM-DD` | Transaction date |
| `amount` | `number` | Amount in ILS (negative for expenses) |
| `reference` | `string` | Invoice/receipt number |
| `vendor` | `string` | Vendor or payee name |
| `category` | `string` | Accounting category |

For CSV import, handle Israeli-specific formatting:
- Shekel amounts may use comma as decimal separator (1,234.56 or 1.234,56)
- Dates may appear as DD/MM/YYYY (Israeli format) rather than YYYY-MM-DD
- Hebrew merchant names require UTF-8 encoding

### Step 5: Define Matching Rules

Define the rules that pair a bank line with an accounting record, in this order of confidence:

1. **Exact**: same date and same amount.
2. **Fuzzy date**: same amount within a small date window, for value-date drift.
3. **Tolerance**: same date, amount within tolerance (1.00 ILS for shekel lines, 5.00 ILS where a currency conversion is involved).
4. **Grouped**: one bank line settling several accounting records, and the card-settlement case where one debit covers a whole statement.
5. **Reference**: match on cheque number, transaction identifier or asmachta where both sides carry one.

Apply them highest-confidence first and never let a lower-confidence rule overwrite a match a higher one already made. The full rule definitions, the field-by-field normalisation (Hebrew descriptions, date formats, sign conventions) and the grouped and card-settlement matchers are in `references/matching-rules.md`.

### Step 6: Run the Reconciliation Engine

Execute the matching process and categorize results into three buckets:
1. **Matched** - Bank transaction paired with an accounting record
2. **Unmatched bank** - Bank transactions with no corresponding accounting record
3. **Unmatched accounting** - Accounting records with no corresponding bank transaction (pending deposits or errors)

The unmatched-bank bucket splits into two distinct cases that need different handling:

- **Missing invoice**: a real business expense or income the user simply has not booked yet (a vendor charge with no recorded invoice, a client payment with no recorded invoice). These need to be *investigated* - the user must locate or create the supporting document.

  The two directions carry different duties. On an unmatched DEBIT you are the recipient, and s.38(a1) is what bites: without an allocation number you lose the input VAT. On an unmatched CREDIT you are the ISSUER, and s.47(a2) is what bites: above the same threshold you must obtain the allocation number from the Tax Authority platform when the customer demands it, and an osek murshe issuing a tax invoice must do so. Do not apply only the recipient-side rule to a receipts reconciliation.
- **Un-booked bank-originated entry**: an entry the bank itself generated that legitimately never had an invoice - bank fees (amlot), standing orders (hora'ot keva), interest, returned-check charges, currency-conversion fees. These are not missing documents. They must be *posted* directly to the books as the appropriate expense or income, not chased as missing invoices.

Tag each unmatched bank entry as one of these two before reporting, so the user knows whether to search for a document or simply record a journal entry.

Additionally flag suspicious transactions:
- Duplicate amounts on the same date
- Unusually large transactions (above a configurable threshold)
- Transactions on weekends or holidays (Israeli calendar)

### Step 7: Build the Reconciliation Bridge

A bank reconciliation is not just a count of matched and unmatched items, it must explain the gap between the book balance and the bank balance with an explicit bridge that ties to zero.

**Get the three balances first.** The bridge is unbuildable without them, and the scraper will not give them to you:
- **Book opening and closing balance** come from the accounting system for the period being reconciled, not from the bank.
- **Bank closing balance** must come from the period-end statement (the PDF/CSV the bank issues for that month). Note `account.balance` returned by `israeli-bank-scrapers` is the CURRENT balance at scrape time, not the closing balance of a past period, so it is the wrong number for a month-end reconciliation. Ask the user for the statement closing balance explicitly.

Prove the book side moves as expected before bridging:

```
Book opening balance + receipts booked - payments booked = Book closing balance
```

Then bridge from the books to the bank:

```
Book balance (closing, per the ledger)
  + outstanding checks (hamcha'ot she-terem nifr'u): written and booked, so already deducted
    in the books, but not yet debited by the bank, so the bank is still higher by this amount
  - deposits in transit (hafkadot ba-derech): booked as received, so already added in the books,
    but not yet credited by the bank, so the bank is still lower by this amount
  - bank fees (amlot) not yet posted to the books: the bank has already taken them
  + bank interest not yet posted to the books: the bank has already credited it
  = Bank balance (closing, per the statement)
```

Sanity-check the direction rather than memorising signs: apply every reconciling item to whichever balance does not yet reflect it. A cheque you wrote has left your books but not the bank, so the bank still holds that cash and reads higher. A deposit you recorded has not reached the bank, so the bank reads lower. If your bridge does not land exactly on the statement balance, the difference is itself a finding: do not force it.

The two timing items above are differences in when, not errors (the books are right, the bank has not caught up). Un-posted fees and interest are the reverse: the bank is right and the books need a journal entry (see Step 6).

Treat post-dated checks (shekim dehuyim) as a distinct reconciling item, separate from ordinary outstanding checks. A post-dated check is written and booked now but carries a future date and cannot clear until that date arrives, so it is not merely "in flight" for a day or two - it stays a reconciling item until its date passes and the bank actually debits it. List post-dated checks received (from customers) and post-dated checks issued (to vendors) on their own lines, keyed by their due date, and roll each one forward across periods until it clears. Mixing them into the outstanding-checks bucket understates how long the item will sit unreconciled.

The report should include:
- **Summary section**: Total matched, unmatched counts and amounts on each side
- **Matched transactions table**: Bank entry paired with its accounting record
- **Unmatched bank transactions**: Split into "missing invoice" and "un-booked bank-originated entry", sorted by amount descending. Chasing a missing invoice is not enough on its own: above the allocation-number threshold an invoice needs a `מספר הקצאה`, and without one s.38(a1) disallows the input VAT. Flag such debits as "obtain an invoice CARRYING a valid allocation number".

  **Reconciliation is retrospective, so use the whole threshold table.** Before VAT: NIS 25,000 from May 2024, 20,000 from January 2025, 10,000 from January 2026, 5,000 from June 2026, nothing before May 2024. Test each unmatched debit against the threshold in force on ITS OWN date; today's 5,000 applied to a 2025 period raises a pile of false findings.

  The statute says `עולה על` (EXCEEDS), so an invoice exactly at the threshold is out, and s.47(a2)(1) excludes zero-rated and exempt-only invoices, so do not flag an export. A missing number blocks only the recipient's input-VAT deduction; the expense still books
- **Unmatched accounting records**: Records to investigate, including outstanding checks, post-dated checks (listed separately, keyed by due date), and deposits in transit
- **Suspicious items**: Flagged entries requiring manual review
- **Reconciliation bridge**: Book balance, the outstanding-checks / deposits-in-transit / fees / interest adjustments, and the resulting bank balance - the two sides must tie out to zero difference once all reconciling items are listed

A reconciliation is cumulative: the prior period's closing reconciled balance is this period's opening balance, and any outstanding checks or deposits in transit that did not clear roll forward into the next period's reconciling items until they do.

Output formats:
- CSV for import into spreadsheet software
- JSON for programmatic consumption
- Console summary for quick review

### Step 8: Handle Foreign-Currency Accounts

When reconciling a foreign-currency account or foreign-currency transactions, value the book entries using the Bank of Israel representative rate (sha'ar yatzig). State your rate-date convention explicitly, because two different ones give two different answers: use the transaction date for valuing an individual entry, and the period-end date for revaluing the closing foreign-currency balance. Say which you used in the report.

Two facts about the representative rate that trip up reconciliations on the Israeli calendar. It is calculated on foreign-currency business days only. The Bank of Israel names the no-rate days as Saturdays, Sundays, Israeli holidays, Christmas Day, New Year's Day and Easter; Friday is NOT among them, so do not carry Thursday's rate onto a Friday transaction. On days that genuinely have no rate, carry the last published one forward. And it is published only after the sampling window closes in the afternoon, so a same-day booking cannot use a same-day rate in real time. The Bank of Israel also states the representative rates carry no official or legal standing in themselves; they bind a transaction only if the parties stipulated them, and the valuation rule for tax purposes comes from the Income Tax rules rather than from the rate publication. Be aware that the bank books its own conversion at its own rate on the settlement date, which will differ from the representative rate. The gap between the representative rate and the bank's actual conversion rate is a real exchange-rate difference - post it as an exchange-rate gain or loss, do not treat it as an unexplained discrepancy. Widen the matching tolerance for foreign-currency transactions accordingly.

### Step 9: Retain the Reconciliation and Its Supporting Documents

Account books, records, and the supporting documents tied to running the business (including the bank statements you reconciled against and the reconciliation reports themselves) must be kept for 7 years. Some of these flows feed an annual tax return (see Example 3), and the retention window runs from the end of the tax year, or 6 years from the date the return was filed, whichever is later. Archive each period's reconciliation report together with the bank statement and the matched accounting export that produced it, so the trail is reconstructible if the Tax Authority asks.

## Examples

### Example 1: Monthly Reconciliation for a Small Business

User says: "Reconcile my Hapoalim business account for January 2026 against my QuickBooks export."

Actions:
1. Fetch transactions from Bank Hapoalim for January 1-31, 2026 using `israeli-bank-scrapers`
2. Parse the QuickBooks CSV export, normalizing dates from DD/MM/YYYY to YYYY-MM-DD and amounts to ILS
3. Run matching rules: exact reference match first, then fuzzy date+amount match
4. Identify 142 matched transactions, 8 unmatched bank transactions, and 3 unmatched accounting records

Result: A reconciliation report showing a 94.7% bank-side match rate (142 of 150 bank lines). Always say which denominator you used: bank lines, accounting lines and all items give three different numbers. The 8 unmatched bank entries are petty cash ATM withdrawals missing receipts. The 3 unmatched accounting records are checks not yet cleared. The report highlights one suspicious duplicate charge of 2,450 ILS at the same vendor on the same date.

### Example 2: Multi-Bank Reconciliation with Credit Cards

User says: "I need to reconcile both my Leumi checking account and my Max credit card against my accounting system for Q4 2025."

Actions:
1. Fetch transactions from Bank Leumi (October-December 2025) and Max credit card for the same period
2. Load accounting records from a CSV export filtered to Q4
3. Run reconciliation separately for each account, then produce a combined summary
4. Flag credit card installment transactions (split payments) that appear as single entries in accounting

Result: Combined reconciliation report covering both accounts. Leumi checking shows 97% match rate with 12 unmatched items. Max credit card shows 91% match rate, with most unmatched items being installment splits. Report includes a recommendation to split 4 accounting entries to match the installment pattern. Residual difference: 127.50 ILS, traced to the gap between the representative rate and the bank's own conversion rate on a settlement. That is an exchange-rate difference, not a rounding tolerance, so it does not stay in the residual: post it as an exchange-rate gain or loss and the bridge then ties out to zero. A reconciliation that ends on a non-zero residual is not finished.

### Example 3: Detecting Missing Invoices Before Tax Filing

User says: "I need to find all bank transactions from 2025 that don't have matching invoices before I file my annual tax return."

Actions:
1. Fetch full year of transactions from Discount Bank for 2025
2. Load the complete invoice register exported from the accounting system
3. Match all transactions, focusing on identifying unmatched bank debits (expenses without invoices)
4. Group unmatched transactions by vendor and category

Result: Found 34 expense transactions totaling 18,200 ILS without matching invoices. The largest gaps are: office supplies from a vendor billed in cash (6 transactions, 3,400 ILS), software subscriptions charged in USD and converted (8 transactions, 5,100 ILS), and parking/toll charges (20 small transactions, 9,700 ILS). Provides a prioritized list for the accountant to locate or create missing invoices.

## Recommended MCP Servers

These MCP servers can supply the transaction data this skill reconciles, so the agent does not have to write and run a scraper script directly:

- **`israeli-bank`**, **`il-bank`**, **`asher`** - MCP servers that wrap the `israeli-bank-scrapers` library and expose bank and credit-card transaction fetching as MCP tools. Use one of these to pull the bank side of the reconciliation (Leumi, Hapoalim, Discount, Mizrahi Tefahot, and the card companies) instead of maintaining a local scraping script.
- **`boi-exchange`** - an MCP server for Bank of Israel representative exchange rates (sha'ar yatzig). Use it for the foreign-currency reconciliation case in Step 8 to value foreign-currency book entries at the correct representative rate.

If an MCP server is available, prefer it for fetching transactions; fall back to the `israeli-bank-scrapers` library script (Step 3) when no MCP server is configured.

## Bundled Resources

### References
- `israeli-bank-scrapers` library documentation: https://github.com/eshaham/israeli-bank-scrapers - Consult when adding support for new bank types or troubleshooting scraper configuration.
- Caspion automated budget tracking: https://github.com/brafdlog/caspion - Consult when users want to combine reconciliation with ongoing budget tracking and categorization.

## Gotchas

- A bank fee, standing order, interest credit, or returned-check charge that appears on the statement but not in the books is not a missing invoice. It is a bank-originated entry that must be posted to the books with a journal entry, not investigated as a lost document. Agents may waste the user's time hunting for an invoice that never existed.
- Outstanding checks and deposits in transit are timing differences, not errors. A reconciliation that does not list them explicitly will show a false discrepancy. Agents may report the raw book-vs-bank gap without building the bridge.
- A reconciliation is cumulative. Outstanding checks and deposits in transit that do not clear roll forward as reconciling items into the next period. Agents may treat each month as independent and lose track of items in transit.
- Israeli banks (Leumi, Hapoalim, Discount, Mizrahi-Tefahot, FIBI) each have different transaction export formats and date conventions. Agents may assume a uniform CSV structure across all banks.
- Israeli bank transaction dates use DD/MM/YYYY format. Agents may parse dates as MM/DD/YYYY, silently swapping day and month for dates like 05/03/2026.
- Check (hamchaa) clearing does not work the way "1-3 days of float" suggests, and the difference matters for reconciliation. A deposited cheque is credited on the clearing day itself, but that credit is PROVISIONAL and only becomes final after a further three business days, during which the drawee bank can still refuse it. So the credit appears on the statement immediately and can then be reversed. Practical consequence: a returned cheque can un-do a deposit you already matched in a prior period, which means re-opening that match, re-debiting the customer, and treating the reversal as more than a fee line.
- Israeli banks use the Sunday-Thursday business week. Transactions on Friday or Saturday are processed on Sunday. Agents may apply Monday-Friday processing assumptions.
- Credit card settlements in Israel arrive as lump-sum charges from card companies (Isracard, Cal, Max), not individual transactions. Agents may try to match individual purchases against bank statements instead of matching the settlement total.


## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Bank of Israel | https://www.boi.org.il/en/economic-roles/supervision-and-regulation/ | Proper Conduct Directives, payment standards, bank statement formats |
| Israel Tax Authority - bookkeeping | https://www.gov.il/he/departments/israel_tax_authority | Bookkeeping directive, VAT reconciliation rules, required journal fields |
| Association of Banks in Israel | https://www.ibank.org.il/en/ | Member banks list, standard bank codes, payment file formats |
| pandas I/O reference | https://pandas.pydata.org/docs/reference/io.html | CSV/Excel import for bank statements, date parsing, encoding |
| openpyxl documentation | https://openpyxl.readthedocs.io/en/stable/ | Writing reconciliation reports in XLSX with styled output |

## Troubleshooting

### Error: "Scrape failed: INVALID_PASSWORD"
Cause: The bank credentials are incorrect, expired, or the account requires a password reset. Some Israeli banks also enforce periodic password changes.
Solution: Verify credentials by logging into the bank's website manually. If the password was recently changed, update the environment variables. For banks requiring OTP or two-factor authentication, ensure the scraper configuration includes the required additional fields.

### Error: "No transactions found for the specified date range"
Cause: The date range may be too narrow, the account may have no activity, or the bank's scraper may require a different date format.
Solution: Expand the date range and verify that the `startDate` is a valid JavaScript Date object. Check that the bank account has transactions in the specified period by logging into the bank's website. Some scrapers return transactions from the start date to today, not to a specified end date.

### Error: "CSV parsing failed: unexpected character at position N"
Cause: Israeli accounting software often exports CSV with Windows-1255 (Hebrew) encoding or includes BOM markers that trip up UTF-8 parsers.
Solution: Convert the file to UTF-8 before parsing: `iconv -f WINDOWS-1255 -t UTF-8 input.csv > output.csv`. Alternatively, specify the encoding in the CSV parser options. Also check for semicolon delimiters (common in Israeli Excel exports) instead of commas.

### Error: "Amount mismatch: bank shows -X but accounting shows -Y"
Cause: Rounding differences in currency conversion, VAT calculations, or installment splitting can cause small discrepancies between bank amounts and accounting entries.
Solution: Configure the matching tolerance threshold. For shekel amounts, a tolerance of 1.00 ILS handles most rounding cases. For transactions involving foreign currency conversion, increase tolerance to 5.00 ILS. If discrepancies are systematic, check whether VAT is included in bank amounts but excluded in accounting entries, using the rate in force on the TRANSACTION's date: 18% from 1 January 2025, 17% before. A 2024 period tested at 18% flags every correct pair, since its signature is 17/117 (14.53%), not 15.25%.
