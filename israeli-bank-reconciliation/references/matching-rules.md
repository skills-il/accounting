# Matching rules for an Israeli bank reconciliation

Detail moved out of SKILL.md Step 5 to stay under the 5,000-word cap.

Configure rules for automatic transaction matching. The matching engine supports multiple strategies applied in priority order.

**Exact match**: Match by reference number and exact amount.

**Fuzzy match**: Match by date range (+/- 3 days), amount tolerance (within 1 ILS), and vendor name similarity.

**Pattern match**: Define regex patterns for recurring transactions (rent, utilities, subscriptions).

**Standing-order match (hora'ot keva)**: Standing orders are the most common recurring Israeli bank debit (rent, loan repayments, gym, insurance, donations). Detect them by a stable amount that repeats on roughly the same day each month from the same payee, often carrying a "הוראת קבע" / "הו"ק" marker in the description. Treat a confirmed standing order as a recurring expense the books should already expect, and roll an unbooked one forward as a posting candidate (see Step 6) rather than chasing it as a missing invoice.

```javascript
const matchingRules = [
  {
    name: 'exact-reference',
    priority: 1,
    match: (bankTxn, accRecord) =>
      // Normalise both sides: the bank reference arrives as a number from the
      // library and the ledger reference is a string. Compare as trimmed strings,
      // and require both to be non-empty so blank === blank is not a "match".
      String(bankTxn.reference ?? '').trim() !== '' &&
      String(bankTxn.reference ?? '').trim() === String(accRecord.reference ?? '').trim() &&
      Math.abs(bankTxn.amount - accRecord.amount) < 0.01
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
// same CompanyTypes enum) and match the SUM for the settlement cycle.
// cycleStart/cycleEnd come from the issuer's actual billing cycle, which you can
// read off the card statement. Do NOT guess a fixed lookback: a rolling window
// sweeps in the tail of the previous cycle and produces a false difference.
// Amounts are compared as magnitudes throughout, since expenses are negative.
function matchCardSettlement(bankDebit, cardTxns, cycleStart, cycleEnd, toleranceIls = 1.0) {
  const inCycle = cardTxns.filter(t => {
    const d = dayjs(t.processedDate || t.date);
    return !d.isBefore(dayjs(cycleStart)) && !d.isAfter(dayjs(cycleEnd));
  });
  const total = inCycle.reduce((sum, t) => sum + Math.abs(t.amount), 0);
  const difference = total - Math.abs(bankDebit.amount);
  return Math.abs(difference) <= toleranceIls
    ? { matched: true, coveredBy: inCycle }
    : { matched: false, difference };
}

// B) Split / partial settlement: N ledger items to ONE bank line, or the reverse.
// Try small subsets before declaring an exception.
function* combinations(arr, size, start = 0, picked = []) {
  if (picked.length === size) { yield picked; return; }
  for (let i = start; i < arr.length; i++) {
    yield* combinations(arr, size, i + 1, [...picked, arr[i]]);
  }
}

function matchGroup(bankTxn, candidates, toleranceIls = 1.0, maxGroup = 3) {
  const near = candidates.filter(c =>
    Math.abs(dayjs(bankTxn.date).diff(dayjs(c.date), 'day')) <= 7);
  for (let size = 2; size <= maxGroup; size++) {
    for (const combo of combinations(near, size)) {
      // Compare magnitudes, matching matchCardSettlement above.
      const total = combo.reduce((sum, c) => sum + Math.abs(c.amount), 0);
      if (Math.abs(total - Math.abs(bankTxn.amount)) <= toleranceIls) return combo;
    }
  }
  return null;
}
```

Reconcile the card side separately against the purchase ledger as well: matching only the settlement total proves the bank line, not the individual purchases behind it.

**Tolerances are a policy choice, not a default.** A plus-or-minus 1 ILS amount window combined with plus-or-minus 3 days will cross-match distinct transactions of similar size in a busy account, and the fuzzy rule above compares no payee at all. Add a description or vendor similarity condition before relying on it, mark every fuzzy match as "requires review" in the report so it is visibly weaker than an exact-reference match, and never let a fuzzy match silently overwrite an exact one.

