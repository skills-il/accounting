# Changelog

## 1.4.0 - 2026-08-27

- **The 500 NIS framework shekel supplement does not reach nurses.** Nurses,
  including public-health nurses, are on the named exclusion list and stay at
  400 NIS, along with social workers, medical imaging technicians, medical
  technologists and administrative staff. The skill stated 500 NIS as a universal
  framework fact, in a skill whose largest audience is nurses.
- **The working-week tranche dates are per-employer and government hospitals have
  their own.** First tranche 1.12.2023 (at the latest 1.1.2024), second 1.7.2024
  (or 1.6.2024 if the first was deferred), against 1.10.2023 and 1.9.2024 in local
  government. The skill said "two steps" with no dates, which leaves erech shaa,
  and every line derived from it, indeterminate for a 2024 slip.
- **Havraa now carries a rate, and it is the PUBLIC one.** 511.60 NIS a day from
  1.6.2026, up from 471.40, not the private-sector 451.50. The skill previously
  named havraa without any figure, which invited the private number.
- **Clothing allowance 2026** added: 1,812.00 NIS at level 3 and 2,527.00 NIS at
  level 4, a 1.9455% uplift, paid in the July 2026 salary, levels per Takshir
  28.425. The amounts are published only as an image and were read from it.
- **Doctors are on a THIRD wage-reduction track**, under the agreement of
  23.1.2025, at 1.081% / 1.781% / 1.081%. The skill assigned them to the
  31.3.2025 wage agreement, which is a different instrument.
- **Doctors' later wage legs are no longer "unconfirmable":** 1.62% from 1.7.2025
  (6.5% cumulative) and 1% from 1.1.2026 (7.5% cumulative).
- **Tosefet mesima leumit is no longer "do not quote":** a five-year window
  (1.1.2025 to 31.12.2029), base 3,000 NIS staged to 4,500 NIS then 6,000 NIS,
  with pension computed as if 6,000 throughout; salary for severance, carries
  keren hishtalmut, not in the mashkoret koveat.
- **Doctors' havraa is cut and the skill now says so.** Under the agreement of
  14.5.2025 state-employed doctors' havraa was reduced 66.2% in 2025 and 5% in
  2026. Without this, the newly added 511.60 NIS public rate would have been
  applied raw to a doctors' slip.
- **Allied-health position-scope grant added** (mena'ak heikef misra, 22.4.2025
  agreement, implementation instructions 18.9.2025, paid in the April 2026
  salary). The skill had mined that agreement for three other lines and missed it.
- **Hospital pharmacists are no longer silently unserved.** The skill sells the
  academic dirug in its description but carries no supplement set for it; Step 1
  now says so explicitly and routes them to the employer's own table instead of
  letting the gross build return base plus nothing.
- Corrected the allied-health table claim: three dirugim but TWO published table
  sets, occupational therapy sharing one with the para-medical grade.
- The script's `--add` help wrongly listed the clothing allowance as a
  non-prorated addition, against the skill's own statement that bigud is
  pro-rated. Moved to `--add-prorated` alongside the framework shekel supplement
  and havraa.
- Withdrew the unsourced tosefet mesima leumit coefficient range and its claimed
  mutual exclusivity with tosefet mar'ag, in both languages.

- Two three-cycle debts closed by declaring them out of scope with a rationale
  rather than leaving them open: toranut clock windows (the asymmetry is in the
  source agreements) and global overtime for nursing management and allied health
  (positive searches found no such arrangement, so the skill must not assert one).
- Two unevidenced assertions withdrawn rather than restated: that tamritz is
  non-pensionable, and that the wage reduction does not reduce the severance base.
  Both now say to check rather than asserting.
- The script now rejects a negative base and a non-positive position instead of
  silently computing on them.
- Split the framework layer and the wage-reduction detail into
  `references/framework-agreement.md` and `references/wage-reduction.md`, and moved
  the toranut and kononut day-equivalent tables into `references/healthcare-tosafot.md`.

## 1.3.1 - 2026-08-13

Moved the Troubleshooting section to references/ to bring SKILL.md under the 5,000-word validator cap, which it had been exceeding. No content was removed.

All notable changes to this skill are documented here.

## [1.3.0] - 2026-08-09

### Added

- נוסף פרק "הבהרה משפטית" בראש SKILL.md ו-SKILL_HE.md, המפרט מה הכלי עושה, מה הוא אינו, ולאיזה בעל מקצוע מוסמך יש לפנות.

### Changed

- התיאור נפתח כעת בהבהרה קצרה, כך שהיא נראית גם בכרטיס ובתוצאות החיפוש.
