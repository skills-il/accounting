# VAT and foreign-currency rules a reconciliation depends on

Every rule here is date-dependent, and a reconciliation is retrospective, so always
apply the rule in force on the date of the line being tested, never today's.

## Allocation numbers (מספר הקצאה, "Israel Invoices")

**Two sides, two sections of the VAT Law.**

- **Recipient, s.38(a1):** no input-VAT deduction on a tax invoice whose amount
  before tax EXCEEDS (`עולה על`) the threshold and that does not carry a number
  allocated by the Director. This is what bites on an unmatched DEBIT.
- **Issuer, s.47(a2)(1):** an osek murshe issuing a tax invoice may ask for an
  allocation number, and in a transaction whose amount before tax exceeds the
  s.38(a1) amount it must do so when the buyer demands it. The subsection does not
  apply to a transaction taxed at the zero rate. This is what bites on an
  unmatched CREDIT.

Keep the two rules apart. The buyer's demand decides only whether the SELLER
breached its s.47(a2) duty; s.38(a1) has no request condition, so the recipient
loses the deduction on a qualifying invoice whether or not anyone asked for a
number. Flag every unmatched debit whose invoice qualifies, asked or not. What
does narrow the rule: the Tax Authority's API specification issues numbers only
for an invoice with a non-zero VAT component to a licensed dealer (עוסק מורשה), so
zero-rated invoices and invoices containing only exempt transactions need none.
Do not flag an export or an exempt supply, and a private consumer has no
deduction to lose.

**Threshold table (amount before VAT, invoice must exceed it):**

| Invoice date | Threshold |
|---|---|
| Before 5 May 2024 | none (the model was not yet enforced) |
| 5 May 2024 to 31 Dec 2024 | NIS 25,000 |
| 1 Jan 2025 to 31 Dec 2025 | NIS 20,000 |
| 1 Jan 2026 to 31 May 2026 | NIS 10,000 |
| From 1 Jun 2026 | NIS 5,000 |

The statute's 2024 window opened on 1 January 2024, but the Tax Authority deferred
enforcement to 5 May 2024. NIS 5,000 is the permanent figure written into s.38(a1)
itself; the earlier rows were temporary overrides. As of October 2026 no further
step has been enacted. Vendor blogs that predict a lower figure cite no source, so
do not apply one. Re-check the Tax Authority service page before relying on 5,000
for a later period. Do not take thresholds from the Tax Authority's API
specification PDFs: they still print an obsolete schedule that later
legislation superseded.

**The threshold is per INVOICE, not per bank line.** Test the invoice amount before
VAT, never the bank debit. If the books hold only the gross amount, derive the
net at the rate for the invoice's own date (gross x 100/117 before 2025, x
100/118 from 2025): a NIS 5,800 gross invoice in July 2026 is about NIS 4,915
net and needs no number. One debit of NIS 12,000 can settle three invoices of
NIS 4,000, none of which needs a number; a debit of NIS 4,000 can be a part payment
of a NIS 30,000 invoice, which does. A card-company settlement line is never tested
against the threshold at all: the test runs on the invoices behind the card
purchases.

**Format.** The specification (edition 2.0, 7.2024) defines the allocation number
as a field of up to 30 characters, and its published examples are 26 digits
long. It recommends printing only the 9 rightmost digits on the invoice under the
heading "מספר הקצאה", and the 9 rightmost digits are what goes into the detailed
report. So match an allocation number on its rightmost 9 digits, do not reject a
short-form number as truncated, and do not enforce a fixed full length.

**Effect.** A missing number disallows the recipient's input-VAT deduction, and
from 1 August 2025 the Income Tax Ordinance s.32(18) also disallows the expense
itself for income tax where its input VAT was disallowed under s.38(a1). It does
not void the invoice. The supplier may ask for a number even after issuing the
invoice (s.47(a2)(4)), but that does not move the deadline in s.38(a): input VAT
must be deducted within six months of the invoice date. So an above-threshold
invoice without a number is urgent, not cosmetic.

**Cash payments.** s.38(a2) also disallows input VAT on a tax invoice whose
consideration was a payment found to breach the Law for Reducing the Use of
Cash, where a monetary sanction was imposed for it. A cash-paid supplier
invoice in the unmatched list is worth flagging for the accountant. On the
income-tax side, Ordinance s.32(16a) likewise disallows payments found to breach
that law where such a sanction was imposed.

**Which document counts.** s.38(a) allows input VAT on a tax invoice issued to
the dealer (חשבונית מס שהוצאה לו כדין). A receipt, a transaction invoice
(חשבונית עסקה) or a proforma does not support the deduction, and an osek patur
supplier charges no VAT, so finding one of those does not close a missing-invoice
item for VAT purposes.

## VAT rate by date

17% until 31 December 2024, 18% from 1 January 2025. The VAT share of a
VAT-inclusive amount is therefore 17/117 (14.53%) for a 2024 line and 18/118
(15.25%) from 2025. Testing a 2024 period at 18% flags every correct pair.

## VAT reporting periods

Close the reconciliation on the user's VAT-period boundary, so an input-VAT
finding lands before the report that would claim it:

- **Osek murshe, by turnover**: s.67(a2)(1) makes the period two months for a
  dealer whose turnover does not exceed NIS 1,775,000 (the CPI-adjusted figure
  from 1 September 2025), and one month above it.
- **Detailed-report filers report monthly regardless.** A dealer obliged to file
  the detailed VAT report (PCN874) moves to monthly reporting and payment under
  s.67A(a). That duty covers companies with turnover above NIS 500,000 from the
  September 2025 period, and individual dealers above NIS 500,000 from 1 January
  2026 (some individuals may apply to defer it to 1 January 2027). So a dealer
  well under NIS 1,775,000 can still be on a monthly period: ask, do not infer.
- **Osek patur**: no periodic VAT report; an annual turnover declaration by 31
  January for the year that ended.

## Bank of Israel representative rate (שער יציג)

- **No-rate days.** The Bank of Israel's explanatory notes name Saturdays, Sundays,
  Israeli holidays, Christmas Day, New Year's Day and Easter. Friday is NOT among
  them. The Bank's annual list of dates without a rate is longer than that
  sentence: in 2026 it also includes holiday eves (Eve of Pesach, Eve of Rosh
  Hashanah), foreign "Holiday Abroad" dates and the Knesset election day (27
  October 2026). Read the year's list or the rates feed rather than hard-coding the
  categories, and on a genuine no-rate day carry the last published rate forward.
- **Timing.** The rate is sampled at a random moment between 13:15 and 15:15 and
  published soon after 15:15; on Fridays, holiday eves and some other Jewish
  holidays the window is 10:15 to 12:15 and publication follows 12:15.
- **Standing.** The Bank states the rates have no official or legal standing and
  bind a transaction only if the parties stipulated them in advance.
- **Tax side.** The one income-tax regime that names the rate is the 1986 "dollar
  regulations" for companies that elected to keep their books under them: there
  the dollar rate for a date is the representative rate the Bank of Israel set on
  that date, or the last one it set before it, and taxable income is translated at
  the rate of the last day of the tax year. That regime is elective and narrow.
  For an ordinary business the skill does not state a tax translation rule: ask
  the accountant which convention the books use.
