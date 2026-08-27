# Domain checklist: Israeli Healthcare Payroll (israeli-healthcare-payroll)

Coverage contract for explaining and sanity-checking the salary of Israeli
public-healthcare-sector workers (nurses, allied health, hospital pharmacists,
doctors), whose pay is set by public-sector collective agreements. Every "Must
cover" row maps to a claim in evidence.json or to a structural instruction.

## Must cover (core)

### Public-sector pay model
- [x] Pay is a collective-agreement wage grade (dirug), not private negotiation; base = combined-salary cell (grade x seniority) signed with the Wage Commissioner. (structural, nurses-dirug-applies)
- [x] The combined-salary cell already includes seniority; do not re-add a seniority percentage. (structural)
- [x] Employer of record (Ministry of Health vs Clalit vs Hadassah vs municipal) is separate from the dirug and changes pension arrangement, employer supplements, and who issues the slip. (structural)

### Wage grades (render every track)
- [x] Nurses' dirug (achim ve'achayot), certified and practical. (nurses-dirug-applies)
- [x] Allied health is THREE separate grades: occupational therapy, physiotherapy, and the para-medical grade (dietitians and speech clinicians). (allied-three-dirugim)
- [x] Pharmacists and some hospital scientists sit in the academic dirug (haMachar), not a health dirug. (structural)
- [x] Doctors' dirug under the IMA (haRi) agreement. (doctors-oncall-section)

### Framework layer (above every dirug)
- [x] Public-sector framework agreement 17.7.2023 for 2020-2027: shekel supplement of 400 NIS from 1.7.2023 rising to 500 NIS from 1.10.2024, plus cumulative 2% (12/2024), 3.5% (4/2025), 5% (4/2026), 6% (4/2027). Moves every dirug table. (framework-agreement-2020-2027, shiklit-400-from-2023)
- [x] The 500 NIS step's EXCLUSION LIST, in full: nurses (including public-health nurses), social workers, medical imaging technicians, medical technologists, and administrative-and-maintenance staff stay at 400 NIS. Nurses are the skill's largest audience, so a bare "500 NIS" is a coverage failure, not a rounding one. (shiklit-nurses-excluded-400)
- [x] Working-week shortening 42 to 40 hours, that is 182 to 177.667 to 173.333 monthly hours, with the PER-EMPLOYER tranche schedule: government ministries and government hospitals 1.12.2023 (latest 1.1.2024) then 1.7.2024 (or 1.6.2024); local government 1.10.2023 then 1.9.2024. erech shaa depends on which norm was in force. (working-week-gov-hospitals, working-week-local-gov, working-week-norms)
- [x] Tosefet yoker is not paid routinely; check whether an extension order is in force before showing it as a live line. (structural)

### Base salary
- [x] Base = combined salary (sachar meshulav); the nurses' grid is THREE-dimensional: education level (five tables) by rank 10-21 by seniority 0-40. (nurses-table-structure)
- [x] Seniority increment schedule: 3.10% yrs 1-9, 2.10% 10-19, 1.90% 20-32, 1.10% 33-35, 0.85% from 36. (nurses-seniority-curve)
- [x] Education shifts the worker about one rank along the SAME ladder rather than opening a separate scale. (nurses-table-structure)
- [x] The combined-salary cell is a base index, not take-home pay; a rank-13 musmach cell is 3,037.67 NIS in the published grid. (nurses-rank13-cell)

### Nurses tosafot
- [x] Gmul hishtalmut (professional-development supplement): a pensionable percentage of the combined salary credited in recognized-study-hour units, committee-approved; one of the largest levers on a veteran nurse's pay. Read the current per-unit rate and unit cap. (nurses-gmul-hishtalmut)
- [x] Tosefet achayot 2024: 250 NIS/full-time from 1.10.2024, 500 NIS/full-time from 1.4.2025. (nurses-tosefet-2024-250, nurses-tosefet-2024-500)
- [x] Tosefet nihul 7.2%, ranks 14-21 ONLY, on the hourly-rate base, pensionable. (nurses-tosefet-nihul)
- [x] Tosefet achrayut mishmarot 80 NIS per shift, explicitly NOT salary for hourly rate, overtime, severance or pension. (nurses-shift-responsibility-80)
- [x] Two distinct shift lines: shift-responsibility supplement (tosefet achrayut mishmarot, paid to the ward nurse taking shift responsibility, not only managers) AND a rotating-shift supplement for two/three-shift workers. (nurses-shift-responsibility-exists)
- [x] Charge-nurse-of-the-shift (achot achrait mishmeret) role line and academic-degree supplement (tosefet toar). (structural)

### Allied-health tosafot (render the full band set)
- [x] Tosefet hachsharot (from 1.4.2025), percentage of the combined salary ONLY, banded by PROFESSIONAL seniority with exclusive upper bounds: 3.50% (0 to 7), 9.00% (7 to 17), 9.50% (17+). (allied-training-bands)
- [x] Tosefet hachsharot REPLACES gmul hishtalmut; the worker receives the higher of the two, never both. (allied-training-bands)
- [x] Monthly incentive (tamritz) ceiling: 4,125 NIS raised to 5,400 NIS/full-time/month from 1.4.2025. (allied-incentive-ceiling)
- [x] Retention and recruitment grant up to 10,000 NIS/full-time for eligible settings. (allied-retention-grant)

### Doctors on-call and duty (render the full band set)
- [x] Career stage sets the base track: resident (mitmach) vs specialist (mumche) vs senior; residents split into darga alef (pre-board-exam, 45h) and darga bet (post-exam, 42h). (doctors-resident-grades)
- [x] Shortage-specialty premium (miktzo'ot bemtzuka) about 12.5% of salary for neonatology/anesthesia/cardiology/intensive-care. (doctors-shortage-specialty-premium)
- [x] Periphery recruitment grant 300,000 NIS (500,000 for residents) plus ongoing periphery premium; global additional hours (sha'ot nosafot globaliyot) for seniors. (doctors-periphery-grant)
- [x] On-call frequency norm: about 20-30/month, ~60 in psychiatric hospitals (magnitude sanity check). (doctors-oncall-frequency)
- [x] On-call (kononut) band: summoned in after 19:30 for 4.5h+ = 3 workdays. (doctors-oncall-called-after-1930)
- [x] Toranut (on-site duty, section 42) tabled SEPARATELY from kononut (section 49): weekday = 1+3 (four day-equivalents), Fri/holiday eve = 1+4 (five), Sabbath/holiday day = 2+0.5. Toranut pays ~double kononut; do not conflate. (doctors-toranut-weekday, doctors-toranut-eve, doctors-toranut-weekend-day, doctors-oncall-not-base)
- [x] Duty/on-call amount = day-value (erech yom, higher for specialists) times the day-equivalent count, not a plain daily rate. (structural)
- [x] Residents carry a presence/stay supplement (tosefet shehiya). (doctors-shahiya-supplement)
- [x] On-call day-equivalents by timing band: weekday 16:00 to 08:00 = 2 workdays; ER specialist = 3.25 workdays; Sabbath/holiday daytime 08:00 to 16:00 = 1 workday; holiday eve 13:00 to 16:00 = half workday. (doctors-oncall-weekday-2days, doctors-oncall-er, doctors-oncall-sabbath-1day, doctors-oncall-holiday-eve-half)
- [x] On-call and planned duty are NOT part of base salary (no pension/severance base). (doctors-oncall-not-base)

### Doctors' salary tranches
- [x] Doctors' combined-salary legs are now all sourced: 4.88% (1.1.2025), 1.62% more (1.7.2025, 6.5% cumulative), 1% more (1.1.2026, 7.5% cumulative). The prior 'not confirmable, route to the circular' instruction is superseded. (doctors-first-leg-488, doctors-table-tranches)
- [x] Tosefet mesima leumit is a base amount times a specialty/role coefficient from the agreement table, excluded from the mashkoret koveat. Do NOT quote a flat shekel figure, and do NOT state a coefficient range: the previously carried 0.3-to-1.5 range and the claimed mutual exclusivity with tosefet mar'ag were both unsourced and were withdrawn 2026-08-27. (doctors-mission-supplement, mesima-leumit-salary-status)

### Gross to net (name, defer mechanics)
- [x] Statutory deductions apply: income tax, National Insurance and health tax (health 3.23% up to the 7,703 NIS reduced step, 5.17% above), pension, keren hishtalmut, union dues. Defer the math to israeli-payroll-calculator. (statutory-step-and-health)
- [x] Pension TYPE (budgetary vs funded) changes the employee deduction; ask which applies. (structural)
- [x] Pensionable vs non-pensionable split: combined salary + gmulim + certain permanent tosafot are pensionable; shift premiums, on-call, havraa and the clothing allowance are not. The incentive (tamritz) is NOT classified either way, because no readable source settles it, and the skill must say so rather than assert. (structural)
- [x] Union dues (demei chaver / demei tipul) appear on essentially every public-sector healthcare slip. (structural)
- [x] Temporary wage reduction, ALL THREE tracks (agreement, law, and the doctors' own under 23.1.2025): by agreement 2.290% (12/2024-12/2025) then 1.200% (2026); by law 0.000% (12/2024-3/2025), 3.307% (4-12/2025), 1.200% (2026). Ends 31.12.2026. Track is sticky on a dirug change. Does not reduce the pensionable insured salary. (temporary-wage-reduction)

## Should cover (advanced / edge cases)
- [x] Employer-specific management supplement (tosefet minhal / nihul) and legacy fold-in shekel supplements on veteran slips. (structural)
- [x] Shortage-specialty (miktzo'ot bemtzuka) premium for doctors such as neonatology, anesthesia, intensive care; read the current rate. (structural)
- [x] Annual clothing allowance (ktzuvat bigud), usually paid once a year around July, set by grade level. (structural)
- [x] Havraa: public-healthcare workers are PUBLIC sector, so 511.60 NIS a day from 1.6.2026 (was 471.40), NOT the private-sector 451.50 NIS. (hc-havraa-public-2026, hc-havraa-private-451)
- [x] Doctors' havraa is the public rate LESS their own reduction: 66.2% in 2025 and 5% in 2026 under the agreement of 14.5.2025. Applying the public rate raw to a doctors'-dirug slip overstates it. (doctors-havraa-reduction)
- [x] Allied health in government hospitals: position-scope grant (mena'ak heikef misra) under the 22.4.2025 agreement, implementation instructions 18.9.2025, paid in the April 2026 salary, conditional on a qualifying position fraction and a number of months at it. (allied-manak-heikef-misra)
- [x] Clothing allowance 2026: 1,812.00 NIS at level 3 and 2,527.00 NIS at level 4, updated 1.9455% over 2025, paid in the July 2026 salary, levels per Takshir 28.425. (bigud-2026-levels, bigud-2026-uplift)
- [ ] Havraa DAYS by seniority for the health dirugim: NOT carried. The public-sector days table lives in the Takshir and is not on an openly readable page; Kol Zchut publishes only the private-sector table and states expressly that the public-sector numbers are higher. Shipping the private table for a public-sector worker would be worse than silence. UNRESOLVED, not out of scope: revisit next cycle. (hc-havraa-public-2026)
- [x] Mena'ak yovel: recurring tenure entitlement, inside the temporary-wage-reduction base (unlike havraa and bigud). (structural)
- [x] Retroactive pay (hefreshei sachar): expect back-payment lumps; a common reason a slip fails to reconcile. (structural)
- [x] Framework working-week reduction 42 to 40 hours changes the monthly hours norm and therefore erech shaa. (framework-working-week)
- [x] Order of operations: tranches are folded into the published table; never apply a tranche to a cell of unknown date; never bridge the 2008 grid forward. (structural)
- [ ] Setting-specific retention bonuses (for example psychiatric-hospital nurses); read the current agreement.
- [ ] Ionizing-radiation extra leave for operating-room staff; a non-cash entitlement.

- [x] Doctors: the temporary-wage-reduction track is their OWN (agreement 23.1.2025), at 1.081% / 1.781% / 1.081%, not the general agreement or law track, and not the 31.3.2025 wage agreement. (doctors-reduction-rates)
- [x] Doctors: all three combined-salary legs, 4.88% (1.1.2025), 1.62% more (1.7.2025, 6.5% cumulative), 1% more (1.1.2026, 7.5% cumulative). A single-leg rendering is a coverage gap. (doctors-first-leg-488, doctors-table-tranches)
- [x] Doctors: tosefet mesima leumit is a five-year window (1.1.2025 to 31.12.2029) on a base of 3,000 NIS staged to 4,500 and then 6,000, with pension computed as if 6,000 throughout; salary for severance, carries keren hishtalmut, NOT in the mashkoret koveat. (mesima-leumit-window, mesima-leumit-base-3000, mesima-leumit-4500-staging, mesima-leumit-salary-status)

## Out of scope (explicit, with rationale)

- [ ] Toranut per-band CLOCK WINDOWS. The kononut table anchors each band to a clock window; the toranut table gives day-type only. Carried unresolved for three cycles and closed here: the asymmetry is a property of the source agreements (the 2011 base agreement and the 2.10.2023 agreement, both behind gov.il), not a research failure. No authoritative source publishes toranut clock windows. Reviewed 2026-08-27. If a future cycle finds one, reopen.
- [ ] Global additional hours (sha'ot nosafot globaliyot) for NURSING MANAGEMENT and ALLIED HEALTH. Positive searches for such an arrangement returned nothing; do not assert one exists. The doctors' case is covered, and the 15.7.2025 reserve-duty agreement separately provides that toranut pay replaces overtime pay. Reviewed 2026-08-27.
- [ ] Doctors' own pensionable continuing-education gemulim. Three cycles unresolved; a positive search for the IMA mechanism returned nothing readable. Reviewed 2026-08-27.
- [ ] Whether tamritz is pensionable. Three cycles unresolved and no readable source states it either way. The skill therefore says to check the agreement rather than asserting non-pensionability. Reviewed 2026-08-27.
- [ ] Whether the temporary wage reduction enters the severance base. No readable source settles it; the skill says so rather than asserting. Reviewed 2026-08-27.
- [ ] Entry rank per education track on the nurse ladder. The 10-21 range and the seniority-0 equivalence point are carried; the entry point per track is not published. Reviewed 2026-08-27.
- Generic gross-to-net mechanics (income-tax brackets, credit points, the arithmetic of net pay) - handled by `israeli-payroll-calculator`. This skill names which deductions apply and defers the math.
- Teachers' pay (Ofek Chadash / Oz LaTmura) - handled by `israeli-teacher-payroll`.
- Private home caregivers' pay - handled by `foreign-caregiver-payroll` (private-household employment, not public-sector collective agreements).
- Privately negotiated clinic or private-hospital salaries - out of scope; this skill is specifically PUBLIC-healthcare collective-agreement pay.
- A CURRENT-dated shekel grid for every dirug - not reproduced, because none is published openly. Reversed in v1.2.0 for the nurses' dirug: the last openly published grid (effective 01/12/2008) IS now shipped in full in `references/nurses-salary-tables.md`, clearly dated and labelled as a structural base index rather than current pay. Allied-health and doctors' grids remain unreproduced.

## Authoritative sources
- https://www.malam-payroll.com/הסכם-שכר-בדרוג-אחיות-מיום-1-11-2023-תשלום-תוספ/ - nurses' dirug page: tosefet achayot 2024 (250 / 500 NIS), shift-responsibility supplement.
- https://www.malam-payroll.com/הסכם-שכר-קיבוצי-לעובדי-מקצועות-הבריאו/ - allied-health page: three dirugim, tosefet hachsharot bands (3.50 / 9.00 / 9.50%, rate table published as an image), incentive ceiling (5,400 NIS), retention grant (10,000 NIS).
- https://www.ima.org.il/CollectiveAgreements/Default.aspx?CategoryId=5118 - doctors' on-call day-equivalents; on-call is not base salary.
- https://www.btl.gov.il/Insurance/Rates/Pages/לעובדים%20שכירים.aspx - reduced-collection step (7,703 NIS), health-tax rates, employee National Insurance rates.
- https://www1.health.gov.il/nursing/work/recognized-programs/information-for-nurses/ - nurses' gmul hishtalmut (value is a function of recognized study hours).
