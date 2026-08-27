# Changelog

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
