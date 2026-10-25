# Closing a period: business days, reversals, history window, sign-off

## Banking business days

- **Friday is a banking business day.** Under the banking rules on the timing of
  credit and debit for cheques, a banking business day is every day except
  Saturday, holidays and a short list of named days; it ends at 18:30, and at 14:00
  on Fridays and holiday eves. A bank may set an earlier cut-off for a particular
  branch or a particular type of deposit, provided it posts notice. The credit day
  is not otherwise keyed on the deposit channel, so a channel-specific cut-off
  comes from the bank's own terms.
- **The payment system runs Sunday to Friday.** The Bank of Israel's ZAHAV RTGS
  system operates Sunday through Friday, with Friday and holiday eves as short
  days. In 2026 it is closed on Knesset election day, 27 October.
- **Only the stock exchange moved.** Since 5 January 2026 the Tel Aviv Stock
  Exchange trades Monday to Friday. The banks and the payment system did not move:
  Sunday is still a banking day. Securities settlement follows the TASE calendar.
- **Consequence for matching.** A Friday or Sunday posting is an ordinary posting,
  not a weekend anomaly. Only Saturday and holidays are genuinely non-business
  days. Remember that Sunday has no representative rate even though it is a
  banking day (see `vat-and-fx-rules.md`).

## Reversals that re-open a prior match

- **Returned cheque.** A deposited cheque is credited on the clearing day, but the
  credit is provisional and becomes final only at the end of three further banking
  business days, unless the bank reverses it in that window because the drawee
  bank refused the cheque. On a reversal: un-match the original receipt, re-open
  the customer's balance, and post the returned-cheque fee as its own line. If the
  original receipt sat in a closed period, the reversal is a current-period item
  that references it; do not silently edit the closed reconciliation.
- **Direct debit (חיוב על פי הרשאה), Proper Conduct of Banking Business Directive
  439.** The customer may cancel a specific debit by notice to the bank no later
  than 3 business days after the debit date; if the notice comes after the debit
  date, the credit is given at the value date of the notice. The customer may also
  cancel the authorisation itself at any time, effective one business day after
  the notice, and a debit taken after that is refunded at the debit's value date.
  An authorisation unused for 24 months from its last debit lapses. For matching:
  a refund line is the reversal of a specific earlier debit, so pair it with that
  debit rather than booking it as income.
- **What "הוראת קבע" on a statement may be.** A line marked הוראת קבע / הו"ק
  may be a debit under a direct-debit authorisation or a standing transfer.
  Confirm the type with the bank or the account's authorisations list; only a
  debit under an authorisation carries the Directive 439 rights above (the
  Directive itself speaks of debits under an authorisation, not of the statement
  label). A direct debit's amount can vary, so identify it by payee rather than
  by a stable amount. A recurring
  TRANSFER the customer schedules from their own account is a different
  instrument; Directive 439 does not cover it, and no comparable reversal right
  was verified for it.

## Scraper history window

`israeli-bank-scrapers` cannot reach arbitrarily far back. Its README gives up to
one year for Hapoalim, Leumi, Mizrahi, Otsar Hahayal, Visa Cal, Max, Isracard and
Amex, one year minus one day for Discount and Mercantile, and six months for Yahav;
it is silent for the other providers. A catch-up on an older period, or a full
calendar year reconciled late in the following year, therefore needs the bank's
own statement export for the months the scraper can no longer return. Check the
window before promising a full-year scrape.

## Sign-off, ageing and materiality

A reconciliation a practitioner can sign carries:

- **Sign-off block**: preparer, reviewer, date prepared, and the statement it ties
  to (bank, account number, statement period, statement closing balance).
- **Ageing of open items**: each outstanding cheque, deposit in transit, post-dated
  cheque and unmatched entry with its origin date and the number of periods it has
  rolled forward. An item carried across more than one period is a follow-up item,
  not background noise.
- **Materiality**: the tool never accepts a residual. Whether a small unexplained
  difference may be written off is the reviewer's documented policy, recorded in
  the sign-off block with the amount and the reason, not a tolerance the tool
  applies on its own.
