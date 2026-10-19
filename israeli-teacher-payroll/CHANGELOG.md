# Changelog

## 1.5.1 - 2026-10-19

- The script's input cleaner listed invisible direction-control characters
  (U+202A to U+202C, RLM, LRM, NBSP) as literal characters in the source, which
  the Tank scanner rightly flags as a bidirectional-override risk. They are now
  written as escape sequences; behaviour is unchanged.
- One evidence snippet carried zero-width spaces copied from the Bituach Leumi
  page; re-quoted from a contiguous part of the page without them.

## 1.5.0 - 2026-10-19

School year תשפ"ז pay changes, the teacher pension and study-fund rates, and a
script that mishandled shekel floors and the Oz shekel supplement.

- **Oz tosefet shiklit is 1,790.50 NIS from 1.9.2026** (was 1,518 NIS from
  1.9.2025). The signed table schedules 2,066.75 NIS from 1.9.2027. It is
  prorated by position fraction including above 100% (section 7(ג)); the skill
  and script treated it as an unprorated flat line.
- **Script fixes.** A shekel floor was tested against the SUM of every gmul, so
  `--gmul 10 --gmul 6 --gmul-floor 1000` let the 6% satisfy the homeroom floor,
  and a floor with no gmul paid the floor outright. Floors now attach to one gmul
  (`--gmul 10:1000`). Added `--fixed-prorated` (Oz tosefet shiklit) and
  `--gmul-scaled` (special-education and inclusion only). Inputs are validated:
  empty values, template placeholders, NaN, negatives, percent-typed positions
  and shekel amounts typed as a percentage are rejected; decimal commas,
  thousands separators, a percent sign and fractions like 1/3 are accepted.
- **New Oz gmul tafkid beit-sifri** (tashpaz): 2 to 5 units of 200 NIS, full
  value from a third of a position, inside the two-role cap.
- **Keren hishtalmut and pension rates** now stated from the Ministry: dedicated
  teacher fund 4.2% / 8.4%, non-dedicated 2.5% / 7.5%; funded pension employer
  7.5% + 6.224%, employee 6% or 7%; budgetary pension for state teachers with
  kviut hired before 1.9.2002.
- **Oz merit points**: 10 points = 1.67% of the combined salary, at most 4
  grades (6.69%), 3 years apart.
- **Ichud maskorot** conditions now sourced to the Ministry page, with the
  larger-position rule, the baalut-first block and the excluded principals.
- **Retention grant** conditions (kviut at 70%+, prorated by weighted position
  over 36 months) and the timing conflict between the union page and the
  agreement.
- **Irgun HaMorim agreement of 31.8.2026**: physics bagrut gmul 4%, a one-off
  gmul shiluv for tashpav, unpaid substitution hours, the 8.6.2026 strike day.
- Rakaz shichva floor under Ofek flagged as a source conflict (1,000 vs 1,100).
- **The salary cell has an education-grade dimension** (musmach, musmach bachir,
  BA, MA, doctorate) in both reforms, and **Oz LaTmura has no 9-rank ladder**: its
  cell is grade x seniority plus up to four 1.67% promotion grades. The skill had
  sent Oz teachers to a "rank 6" cell that does not exist.
- **Tosefet Ofek 2022** named: the largest line after the base on a new Ofek
  teacher's slip.
- **Retention grant** applies to every new teacher from 1.9.2023 onward, not one
  cohort.
- **Gmul hishtalmut is prorated by position** (terms of service), so it is not a
  role gmul; the script now separates role gmulim (`--gmul`), study gmulim and
  promotion grades (`--gmul-scaled`), and the special-education share
  (`--gmul-share PCT@SHARE`, the share of her frontal hours, not the position).
- Script input hardening: ambiguous separators (12.000, 10,1000), repeated
  `--base`, sub-hour positions, 0:FLOOR and uppercase placeholders are refused.
- July and August are proportional to months worked; pension layers on expense
  reimbursements and above-100% work; retroactive July maternity deductions.
- Removed the unsourced "gmul pituach miktzoi 6%" row and the unsourced "BL
  raised from 0.40%" history; the Oz full-position rule for role gmulim is now
  hedged (the source is Ofek-only).

## 1.4.0 - 2026-08-27

Corrected the computation model and brought the skill up to school year תשפ"ז.

- **Script model fixed (was materially wrong at part-time).** `teacher_gross.py`
  prorated role gmulim by the position fraction. Role gmulim are computed on a
  FULL position and are not prorated, per the Histadrut HaMorim gmulei-tafkid
  page; only the combined salary scales. The two exceptions (special-education
  and inclusion gmulim) now need an explicit `--scale-gmulim`. Example 3, a
  half-position kindergarten manager, was understating gross.
- **Script can now express shekel components at all.** Added `--gmul-floor` (the
  higher-of test behind the 1,000 NIS gmul chinuch floor and the 1,100 NIS Oz
  rakaz shichva floor) and `--fixed` (tosefet shiklit, gmul yozma chinuchit).
  Previously every shekel line was silently dropped, so the gmul chinuch floor
  was breached for any combined cell under 10,000 NIS.
- **The seniority rule now matches the prose.** The script still encoded 2% for
  years 1 to 7; the agreement, and v1.3.2's own correction, is 2% up to and
  including year 6 then 1% to year 36. The domain checklist carried the same
  stale rule.
- **New gmul in force 1.9.2026:** gmul yozma chinuchit beit-sifrit under Ofek
  Chadash, 2 to 5 units per initiative at 200 NIS each, 400 to 1,000 NIS a
  month, re-decided annually. Reconciled against the union terms page, which
  still dates it September 2025.
- **10,000 NIS retention grant** paid in the September 2026 salary to teachers
  whose employment began 1.9.2023.
- **Havraa:** teachers are public sector at 511.60 NIS a day from 1.6.2026 (up
  from 471.40), NOT the private-sector 451.50 NIS. Added the days-by-seniority
  table. The skill previously stated no rate at all.
- **Bigud** updated to 2,527 NIS for 2026, and the 91 NIS cut is now correctly
  described as a one-time 2025 measure.
- **Bituach Leumi and health tax are categorical.** The stated 1.04% / 7.00% and
  3.23% / 5.17% are only the form-102 column-1 row. Added the rows a teacher
  actually hits: a working old-age pensioner pays nothing on the employee side,
  a 67-to-70 non-pensioner pays 3.93% / 10.03%, a disability-pension holder pays
  3.23% / 5.17%. Added the 51,910 NIS maximum insured income.
- **Age-based hour reductions** added for BOTH reforms (Oz 23/36 at 50-55 and
  21/34 over 55; Ofek minus 2 frontal from 50 and minus 4 from 55).
- **Oz rakaz gmulim are now stated, not routed away.** The previous version told
  the agent the rate table was an unreadable image. It is page text. Added the
  full Ofek and Oz role-gmul tables, which differ from each other, plus gmul
  yeutz (12% / 18%), gmul chinuch meyuchad (Ofek 8.5/15/17 against Oz 10/15/17),
  and the corrected two-gmul cap exceptions for principals and deputies.
- Oz gmul hishtalmut quota corrected to 19 units (was 16).
- Named what the gross model cannot express: travel reimbursement, menak yovel,
  havraa, bigud. Stated that pension is computed on the pensionable salary, not
  on gross.
- Moved the temporary wage reduction and the seniority-advancement bands into
  `references/wage-reduction.md`, and recorded that what applies from 1.1.2027 is
  unresolved rather than assuming continuity.
- Replaced dead or paraphrased citations across the evidence file, including the
  ITU gmulei-tafkid page (404 at its old URL) and the Ofek per-level work-week
  splits.

## 1.3.2 - 2026-08-11

Corrected the seniority (vetek) rule, which was off by one year in both limbs. The Ofek Chadash agreement pays 2% for each year up to and including year 6, then 1% from the seventh year to year 36; the skill said 2% through year 7 and 1% from year 8. Verified verbatim against the agreement PDF and evidenced.

## 1.3.1 - 2026-08-11

Removed the unsourced "up to 29.7% for dual-degree" gmul figure, a stale derivation from the 1.2% per-unit rate that rose to 1.3% on 1.9.2025. Recorded the worked example's 10.4% as explicitly derived. Evidence re-grounded against the MoE circulars.

All notable changes to this skill are documented here.

## [1.3.0] - 2026-08-09

### Added

- נוסף פרק "הבהרה משפטית" בראש SKILL.md ו-SKILL_HE.md, המפרט מה הכלי עושה, מה הוא אינו, ולאיזה בעל מקצוע מוסמך יש לפנות.

### Changed

- התיאור נפתח כעת בהבהרה קצרה, כך שהיא נראית גם בכרטיס ובתוצאות החיפוש.
