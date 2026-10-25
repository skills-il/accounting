# Matching rules for an Israeli bank reconciliation

Detail moved out of SKILL.md Step 5 to stay under the 5,000-word cap.

Configure rules for automatic transaction matching. The matching engine supports multiple strategies applied in priority order.

**Exact match**: Match by reference number and exact amount.

**Fuzzy match**: Match by date range (+/- 3 days), amount tolerance (within 1 ILS), and vendor name similarity.

**Pattern match**: Define regex patterns for recurring transactions (rent, utilities, subscriptions).

**Recurring-debit match (הוראת קבע / הו"ק)**: On an Israeli statement, a line marked "הוראת קבע" may be a debit pulled by the payee under a direct-debit authorisation (הרשאה לחיוב חשבון) or a standing transfer; confirm the type with the bank or the account's authorisations list before relying on the Directive 439 rights. Match these by PAYEE, not by a stable amount, since many vary month to month (usage-based bills, index-linked amounts). A fixed amount on the same day each month is a useful extra signal, not the test. Treat a confirmed recurring debit as an expense the books should already expect. If it is unbooked, it still needs the payee's tax invoice (a utility or phone bill is one), so it is a missing-invoice item, not a bank-originated posting; only the bank's own charges are posted without a document. Watch for two failure modes: the same debit taken twice in one cycle (flag it, the customer can cancel a specific debit within 3 business days), and a debit that continues after the user believes it was cancelled (a debit after the authorisation was cancelled is refunded at the debit's value date). Pair any refund line with the debit it reverses (`period-close.md`).

```javascript
const matchingRules = [
  {
    name: 'exact-reference',
    priority: 1,
    match: (bankTxn, accRecord) => {
      // The bank reference can arrive as a number and the ledger reference is a
      // string, and "001234" must equal "1234". Normalise both to digits with
      // leading zeros stripped, and require non-empty so blank is not a match.
      // Compare against the ledger's cheque/asmachta field: an invoice number is
      // a different number space from the bank's asmachta.
      const norm = v => String(v ?? '').replace(/\D/g, '').replace(/^0+/, '');
      const b = norm(bankTxn.reference), a = norm(accRecord.reference);
      return b !== '' && b === a && Math.abs(bankTxn.amount - accRecord.amount) < 0.01;
    }
  },
  {
    name: 'amount-date-fuzzy',
    priority: 2,
    match: (bankTxn, accRecord) => {
      const dateDiff = Math.abs(
        dayjs(bankTxn.date).diff(dayjs(accRecord.date), 'day')
      );
      const amountDiff = Math.abs(bankTxn.amount - accRecord.amount);
      return dateDiff <= 3 && amountDiff <= 1.0;
    }
  },
  {
    name: 'recurring-pattern',
    priority: 3,
    patterns: [
      { regex: /חשמל|electric/i, category: 'utilities' },
      { regex: /ארנונה|municipal/i, category: 'municipal-tax' },
      { regex: /ביטוח|insurance/i, category: 'insurance' }
    ]
  }
];
```

`dayjs` must be required in this block if you run it separately: `const dayjs = require('dayjs');`

**One-to-one rules cannot express the two most common Israeli cases.** Add grouped matching, or the card settlement and any split payment land in the exceptions list and the report overstates problems:

```javascript
// A) Card settlement: ONE bank debit covers MANY card transactions.
// Pull the issuer's own transactions (isracard / max / visaCal / amex are in the
// same CompanyTypes enum) and match the SUM of the lines CHARGED on this debit.
// Key on the charge date: a card line's processedDate is the date it is charged
// to the bank, so the lines belonging to this debit are the ones whose
// processedDate falls on the debit's settlement date. Do NOT use the purchase
// window printed on the card statement (it ends before the charge date) or a
// rolling lookback (it sweeps in the previous cycle). This also handles
// installments, one line per month with combineInstallments: false.
// Sum SIGNED amounts: purchases are negative and a refund on the card is
// positive, so it must reduce the total. Summing magnitudes would turn a 200
// refund into a false 400 difference.
// cardAccount: the card's accountNumber from the scrape. Each card usually has
// its own bank debit line, so sum ONE card at a time. If the issuer posts one
// combined debit for several cards, call it once per card set instead.
// The charge date may fall on a Saturday or holiday while the bank posts on the
// next business day, so accept card lines charged on the debit day or up to 3
// days before it.
function matchCardSettlement(bankDebit, cardTxns, cardAccount, toleranceIls = 1.0) {
  const ilDay = s => new Date(s).toLocaleDateString('sv-SE', { timeZone: 'Asia/Jerusalem' });
  const settleDay = ilDay(bankDebit.processedDate || bankDebit.date);
  const earliest = ilDay(new Date(new Date(settleDay).getTime() - 3 * 86400000).toISOString());
  const inCycle = cardTxns.filter(t => {
    const d = ilDay(t.processedDate || t.date);
    return t.accountNumber === cardAccount && d >= earliest && d <= settleDay;
  });
  const total = inCycle.reduce((sum, t) => sum + t.amount, 0);
  const difference = total - bankDebit.amount;
  return Math.abs(difference) <= toleranceIls
    ? { matched: true, coveredBy: inCycle }
    : { matched: false, difference };
}

// B) Split / partial settlement: N ledger items to ONE bank line.
// Try small subsets of the SAME counterparty's open items before declaring an
// exception. Do not restrict candidates to a few days around the bank date:
// a payment on net+30/60/90 terms settles invoices issued months earlier.
// Run the same search the other way too (one ledger item settled by several
// bank lines: part payments, a customer paying in three transfers).
function* combinations(arr, size, start = 0, picked = []) {
  if (picked.length === size) { yield picked; return; }
  for (let i = start; i < arr.length; i++) {
    yield* combinations(arr, size, i + 1, [...picked, arr[i]]);
  }
}

// openItems: this counterparty's unsettled ledger items, sorted OLDEST FIRST so
// a payment settles the earliest equal items (FIFO) and ageing stays right, signed (a credit note
// carries the opposite sign to its invoice, so netting works and a receivable
// can never combine with an expense to fake a match).
function matchGroup(bankTxn, openItems, toleranceIls = 1.0, maxGroup = 3) {
  for (let size = 2; size <= maxGroup; size++) {
    for (const combo of combinations(openItems, size)) {
      const total = combo.reduce((sum, c) => sum + c.amount, 0);
      if (Math.abs(total - bankTxn.amount) <= toleranceIls) return combo;
    }
  }
  return null;
}
```

Reconcile the card side separately against the purchase ledger as well: matching only the settlement total proves the bank line, not the individual purchases behind it.

**Card RECEIPTS are a different shape.** If the business accepts cards, a credit from the card company can be net of a clearing fee, and a sale paid in installments can arrive in several credits. In that case match the card company's own settlement report to the sales rather than each credit to an invoice, and book the fee as an expense instead of reading the shortfall as a short payment.

**Payments net of withholding tax.** A customer may pay an invoice net of income tax withheld at source (ניכוי במקור) and send a withholding certificate. Treat bank credit plus certificate amount as the settlement of the invoice, and record the withheld amount; do not chase it as a short payment or issue a second invoice.

**Tolerances are a policy choice, not a default.** A plus-or-minus 1 ILS amount window combined with plus-or-minus 3 days will cross-match distinct transactions of similar size in a busy account, and the fuzzy rule above compares no payee at all. Add a description or vendor similarity condition before relying on it, mark every fuzzy match as "requires review" in the report so it is visibly weaker than an exact-reference match, and never let a fuzzy match silently overwrite an exact one.

