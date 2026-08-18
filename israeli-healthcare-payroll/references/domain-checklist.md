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
- [x] Public-sector framework agreement 17.7.2023 for 2020-2027: shekel supplement reaching 500 NIS plus cumulative 2% (12/2024), 3.5% (4/2025), 5% (4/2026), 6% (4/2027). Moves every dirug table. (framework-agreement-2020-2027)
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
- [x] 30.9.2024 agreement: confirmed first leg +4.88% (1.1.2025); later legs exist but are not confirmable from a reachable source, so route to the circular rather than asserting a figure. (doctors-2024-agreement-tranches)
- [x] Tosefet mesima leumit is a base amount times a specialty/role coefficient (about 0.3 to 1.5), mutually exclusive with tosefet mar'ag, excluded from the mashkoret koveat. Do NOT quote a flat shekel figure. (doctors-mission-supplement)

### Gross to net (name, defer mechanics)
- [x] Statutory deductions apply: income tax, National Insurance and health tax (health 3.23% up to the 7,703 NIS reduced step, 5.17% above), pension, keren hishtalmut, union dues. Defer the math to israeli-payroll-calculator. (statutory-step-and-health)
- [x] Pension TYPE (budgetary vs funded) changes the employee deduction; ask which applies. (structural)
- [x] Pensionable vs non-pensionable split: combined salary + gmulim + certain permanent tosafot are pensionable; incentive, shift premiums, on-call, havraa, and clothing allowance are not. (structural)
- [x] Union dues (demei chaver / demei tipul) appear on essentially every public-sector healthcare slip. (structural)
- [x] Temporary wage reduction, BOTH tracks: by agreement 2.290% (12/2024-12/2025) then 1.200% (2026); by law 0.000% (12/2024-3/2025), 3.307% (4-12/2025), 1.200% (2026). Ends 31.12.2026. Track is sticky on a dirug change. Does not reduce the pensionable insured salary. (temporary-wage-reduction)

## Should cover (advanced / edge cases)
- [x] Employer-specific management supplement (tosefet minhal / nihul) and legacy fold-in shekel supplements on veteran slips. (structural)
- [x] Shortage-specialty (miktzo'ot bemtzuka) premium for doctors such as neonatology, anesthesia, intensive care; read the current rate. (structural)
- [x] Annual clothing allowance (ktzuvat bigud), usually paid once a year around July, set by grade level. (structural)
- [x] Havraa (recreation pay) on the gross side. (structural)
- [x] Mena'ak yovel: recurring tenure entitlement, inside the temporary-wage-reduction base (unlike havraa and bigud). (structural)
- [x] Retroactive pay (hefreshei sachar): expect back-payment lumps; a common reason a slip fails to reconcile. (structural)
- [x] Framework working-week reduction 42 to 40 hours changes the monthly hours norm and therefore erech shaa. (framework-working-week)
- [x] Order of operations: tranches are folded into the published table; never apply a tranche to a cell of unknown date; never bridge the 2008 grid forward. (structural)
- [ ] Setting-specific retention bonuses (for example psychiatric-hospital nurses); read the current agreement.
- [ ] Ionizing-radiation extra leave for operating-room staff; a non-cash entitlement.

## Out of scope (explicit, with rationale)
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
