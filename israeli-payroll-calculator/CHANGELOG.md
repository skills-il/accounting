# Changelog

## 1.4.0 (2026-08-19)

- `scripts/calculate_payroll.py` now takes `--ni-category`, so the skill's own Bituach Leumi rate table is reachable from code. Previously the script hardcoded the standard 4.27% / 12.17% employee row with no age, pension or status dimension, which over-charged a minor or a pensioner by the entire deduction, the exact failure the reference file warned about. `--list-ni-categories` prints the whole table.
- Completed the employee rate table against the official form-102 table on btl.gov.il. The skill covered 6 categories; the official table has 11, plus a controlling-shareholder sub-row under each. Added: controlling shareholder in a close company (4.25% / 11.96%), which is where every owner-director of an Israeli micro-company sits and who was previously being quoted the standard rate; new resident after age 62 below retirement age (3.60% / 7.45%); woman between her retirement age and the men's who became a resident after 62 (3.28% / 5.52%); man or woman between 67 and 70 who became a resident after 62 (3.26% / 5.31%); over 70 who became a resident after 62 (3.23% / 5.17%); and soldier in regular service, organ donor or treaty-country foreign resident (1.04% / 7.00%, National Insurance only with no health tax).
- Re-sourced the disability-pension row. The rate (3.23% / 5.17%) is correct and does appear on the official page, but the label carried an unsourced "75%+/100%" qualifier. The official label is recipients of a work-injury or general-disability pension holding an annual confirmation from Bituach Leumi, and it now reads that way.
- Corrected the 67-to-70 row's label from "men 67-70" to "women and men aged 67 to 70", matching the official table, and corrected its reduced-tier National Insurance component from 0.61% to 0.70% (0.61% did not add up with the 3.23% health rate to the published 3.93% total).
- Dropped the "reduced tier up to 60% of the average wage" description from both language files. The reference file already warned against deriving the threshold that way; 7,703 is published separately by Bituach Leumi.

## 1.3.6 (2026-08-11)

- Added the reciprocal boundary to `israeli-attendance-wage-checker`. This skill starts from an agreed gross; working out what gross is owed from a timesheet, including overtime tiers, weekly-rest premium, paid breaks and the burden shift when no hours record exists, is that skill's job and it runs first.
- Stated the scope check at the top of the instructions, so an agent that lands here with an hours question routes out before computing anything.
