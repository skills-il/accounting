# Changelog

## 1.1.0 (2026-08-11)

- Step 0 now states that the section 30 exclusion is the employer's to prove and is construed narrowly, and that it turns on what the person actually did rather than on a job title.
- Step 1 adds three things every figure downstream depends on: deriving an hourly rate from a global wage and stating the divisor, checking the derived rate against the minimum-wage floor for that period, and establishing whether tips form part of the wage.
- New Step 7b corrects the global-overtime remedy. It is re-characterisation of the whole global sum under `סעיף 5` of the Wage Protection Law, not a top-up of the excess hours, and the cumulative conditions for a valid arrangement now sit in the body rather than only in the reference file.
- New Step 7c on evidence-gathering when the employer keeps no ledger, and on the seven-year wage limitation under `סעיף 5(1)` of the Limitation Law, kept explicitly distinct from the one-year / 60-day delayed-wage clock.
- New Step 7d flags sector extension orders and דמי חגים as out of scope rather than folding a guess into the figure.
- Step 7 now warns against trimming a claim down to the 15/60 cap. The cap limits the evidentiary presumption, not how many hours may be claimed.
- `scripts/reconcile_hours.py` implements the rest-day pay-basis split (`--pay-basis monthly` values rest-day hours at the marginal premium element only, since the salary already covers the day), and refuses input spanning more than seven days, because the weekly limb is applied once.

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
