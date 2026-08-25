# Changelog

## 1.2.0 (2026-08-25)

- The payslip is now a first-class entry point, not just a document the reconciliation happens to read. New Step 1b audits the payslip on its own terms: the components `סעיף 24` and its Schedule require, three internal-consistency checks that need no attendance record, and the `סעיף 26ב(ג)` presumption that makes a payslip-only case workable.
- New routing table at the top of Instructions dispatches on the document the user actually holds, treating "a payslip and nothing else" as the normal case rather than the degraded one.
- `סעיף 26ב(ג)` gains three evidence entries (the trigger list, the presumption, and its consequence), all sliced from the rendered source. It was previously asserted in `references/records-and-remedies.md` with no evidence entry behind it.
- The Problem boundary now says explicitly that the skill audits the EARNINGS side of a payslip and not the deductions side, with a named hand-off to `israeli-payroll-calculator` for tax, National Insurance and pension.
- Renamed to "בדיקת תלוש שכר ודוח נוכחות" / "Israeli Payslip and Wage Checker", and the description now leads with the payslip. The skill answered payslip questions before this release but did not say so where search or a routing agent would see it.
- Step 1b's first consistency check is gated on pay basis. For an hourly or daily paid employee, hours times the stated value of a regular hour should equal the wage line. For a monthly-salaried employee it should not, because the base does not move with the hours actually worked, and applying the hourly test to a monthly payslip reports a shortfall that does not exist.
- Fixed a pre-existing wrong section reference. Step 7c told the user to ask the employer in writing for "the `סעיף 24` ledger" in both languages. `סעיף 24` of חוק הגנת השכר is the PAYSLIP duty; the hours-ledger duty is `סעיף 25` of חוק שעות עבודה ומנוחה, as `references/records-and-remedies.md` section 1 already stated correctly. A user following the old text would have cited the wrong provision to their employer.
- The evidence-gathering list moved from Step 7c into `references/records-and-remedies.md` section 7, leaving the rule and a pointer in the body.
- Step 1b's hours-line check no longer treats a monthly hours total above the nominal basis as overtime. The 182 or 186 divisor is an average and not a monthly cap, a month with more working days lawfully produces more ordinary hours, and overtime is defined daily and weekly. A high hours line with no overtime units is now framed as a question that requires the daily breakdown, not as a finding.
- Step 1b's premium check now handles a single combined overtime line, which is common on Israeli payslips: the quotient blends the 125 and 150 percent tiers and lands between them, so only a quotient at or near 100 percent is a reliable finding.
- New Gotcha warning against applying the Step 1b presumption and the Step 7b global-overtime remedy to the same sum twice, since both re-derive the base from the paid wage.
- Step 1b now establishes the payslip's booking convention before any consistency check runs: whether the wage line covers ordinary hours only and the premium line carries the full 125 or 150 percent, or the wage line already carries the 100 percent element of every hour worked and the premium line carries only the 25 or 50 percent supplement. Nearly every false finding in the earlier draft came from assuming one convention on a payslip drawn on the other.
- The hourly branch of the first consistency check no longer expects hours times the value of a regular hour to equal the wage line. Hours actually worked include the overtime hours, which the wage line does not value at 100 percent on the full-rate convention, so the product must exceed the wage line and an exact match is itself the defect. The worked example was corrected to match.
- The monthly branch now divides the FULL-TIME base by the nominal basis rather than the base actually paid. משרה חלקית, a mid-month start or termination, and unpaid absence all prorate the paid base while the hourly value stays contractual, so the earlier form reported a shortfall on every lawful part-time payslip.
- The premium check no longer reads a quotient at or below 100 percent as proof the premium was never applied. On the supplement-only convention the lawful quotients are 25 and 50 percent, and a monthly-salaried weekly-rest line at 50 percent is exactly what Step 4 requires.
- The hours-line check now also states that a total BELOW the nominal basis is not a finding either.
- The hourly branch of the first check is conditioned on the booking convention, not only on what the hours figure contains. On the supplement-only convention the wage line values every hour at 100 percent, so all hours times the value of a regular hour equals the wage line lawfully and that equality is expected rather than a defect; the earlier draft called it the defect. The full-rate branch now states the excess correctly as the overtime hours times the hourly value. הבראה, נסיעות, a 13th salary and equivalent-unit booking joined the list of lawful residuals.
- The worked example was rebuilt so its arithmetic closes. The previous form paid 195 hours of wage plus a 20-hour premium line for 175 ordinary and 20 overtime hours, which overpays by 15 hours of value while concluding the premium was never applied. The example now shows 20 overtime units against no premium amount: 195 hours of value paid where 200 is owed, a shortfall of 5, detectable under either convention and invisible to check 1 alone on a supplement-only payslip.
- The example's shortfall is stated as a floor ("at least five hours of value"), since five assumes all 20 overtime hours sit in the 125 percent tier and the daily split may put some at 150.
- The components table gains the nominal hours basis and היקף משרה, which the first check needs as its divisor and its scale, and the leave, הבראה and נסיעות lines, which `סעיף 26ב(ג)` names as presumption triggers. The full Schedule list is in `references/records-and-remedies.md` section 4.

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
