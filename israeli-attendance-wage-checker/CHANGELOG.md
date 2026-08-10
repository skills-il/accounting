# Changelog

## 1.0.0 (2026-08-11)

Initial release.

- Applicability gate first: all six exclusion classes of חוק שעות עבודה ומנוחה סעיף 30, because for a management or personal-trust role no premium is owed at all and every computed figure would be meaningless.
- Daily-then-weekly overtime ordering, with the two-hour 125 percent tier resetting every day rather than accumulating monthly, which is the most common computational error in the domain.
- The statutory 45-hour week and the operative 42-hour week kept distinct, with the note that the 2018 extension order shortened one defined day and did NOT change the 8-hour daily maximum.
- Rest-day premium split by pay basis: the premium element plus paid compensating rest for a monthly-salaried employee, the full 150 percent with unpaid compensating rest for an hourly or daily one.
- The premium base defined per סעיף 18 as including every supplement the employer pays, which is how a compliant-looking payslip hides a shortfall.
- Paid-versus-unpaid break rule from סעיף 20, turning on whether the employee was required to stay.
- The procedural core: the employer's ledger duty, the burden shift in סעיף 26ב of חוק הגנת השכר, and both of its limits, the 15 weekly / 60 monthly cap and the employee's own minimal factual version.
- Inclusive wage treated as regular wage only under סעיף 5, so a global-salary arrangement does not extinguish the entitlement.
- Delayed-wage compensation as the higher of the two statutory formulas, with its short and separate limitation clock stated every time a figure is produced.
- Compliance breaches reported separately from money owed, so a breach is never read as an entitlement.
- Optional `scripts/reconcile_hours.py`, pure local arithmetic that never guesses an hourly rate and never decides the applicability gate.
