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

### Base salary
- [x] Base = combined salary (sachar meshulav) from a grade (daraga) by seniority (vetek) table; read the current cell, do not freeze a NIS table. (structural)

### Nurses tosafot
- [x] Gmul hishtalmut (professional-development supplement): a pensionable percentage of the combined salary credited in recognized-study-hour units, committee-approved; one of the largest levers on a veteran nurse's pay. Read the current per-unit rate and unit cap. (nurses-gmul-hishtalmut)
- [x] Tosefet achayot 2024: 250 NIS/full-time from 1.10.2024, 500 NIS/full-time from 1.4.2025. (nurses-tosefet-2024-250, nurses-tosefet-2024-500)
- [x] Two distinct shift lines: shift-responsibility supplement (tosefet achrayut mishmarot, paid to the ward nurse taking shift responsibility, not only managers) AND a rotating-shift supplement for two/three-shift workers. (nurses-shift-responsibility-exists)
- [x] Charge-nurse-of-the-shift (achot achrait mishmeret) role line and academic-degree supplement (tosefet toar). (structural)

### Allied-health tosafot (render the full band set)
- [x] Training supplement, percentage of combined salary banded by seniority: 4.5% (0 to 7 yrs), 5.5% (7 to 17 yrs), 6.5% (over 17 yrs). (allied-training-bands)
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

### Gross to net (name, defer mechanics)
- [x] Statutory deductions apply: income tax, National Insurance and health tax (health 3.23% up to the 7,703 NIS reduced step, 5.17% above), pension, keren hishtalmut, union dues. Defer the math to israeli-payroll-calculator. (statutory-step-and-health)
- [x] Pension TYPE (budgetary vs funded) changes the employee deduction; ask which applies. (structural)
- [x] Pensionable vs non-pensionable split: combined salary + gmulim + certain permanent tosafot are pensionable; incentive, shift premiums, on-call, havraa, and clothing allowance are not. (structural)
- [x] Union dues (demei chaver / demei tipul) appear on essentially every public-sector healthcare slip. (structural)

## Should cover (advanced / edge cases)
- [x] Employer-specific management supplement (tosefet minhal / nihul) and legacy fold-in shekel supplements on veteran slips. (structural)
- [x] Shortage-specialty (miktzo'ot bemtzuka) premium for doctors such as neonatology, anesthesia, intensive care; read the current rate. (structural)
- [x] Annual clothing allowance (ktzuvat bigud), usually paid once a year around July, set by grade level. (structural)
- [x] Havraa (recreation pay) on the gross side. (structural)
- [ ] Setting-specific retention bonuses (for example psychiatric-hospital nurses); read the current agreement.
- [ ] Ionizing-radiation extra leave for operating-room staff; a non-cash entitlement.

## Out of scope (explicit, with rationale)
- Generic gross-to-net mechanics (income-tax brackets, credit points, the arithmetic of net pay) - handled by `israeli-payroll-calculator`. This skill names which deductions apply and defers the math.
- Teachers' pay (Ofek Chadash / Oz LaTmura) - handled by `israeli-teacher-payroll`.
- Private home caregivers' pay - handled by `foreign-caregiver-payroll` (private-household employment, not public-sector collective agreements).
- Privately negotiated clinic or private-hospital salaries - out of scope; this skill is specifically PUBLIC-healthcare collective-agreement pay.
- Exact current shekel value of every grade cell in every dirug table - not reproduced; these change with each agreement. The skill teaches how to read the table and where to find the live one.

## Authoritative sources
- https://www.malam-payroll.com/הסכם-שכר-בדרוג-אחיות-מיום-1-11-2023-תשלום-תוספ/ - nurses' dirug page: tosefet achayot 2024 (250 / 500 NIS), shift-responsibility supplement.
- https://www.malam-payroll.com/הסכם-שכר-קיבוצי-לעובדי-מקצועות-הבריאו/ - allied-health page: three dirugim, training bands (4.5 / 5.5 / 6.5%), incentive ceiling (5,400 NIS), retention grant (10,000 NIS).
- https://www.ima.org.il/CollectiveAgreements/Default.aspx?CategoryId=5118 - doctors' on-call day-equivalents; on-call is not base salary.
- https://www.btl.gov.il/Insurance/Rates/Pages/לעובדים%20שכירים.aspx - reduced-collection step (7,703 NIS), health-tax rates, employee National Insurance rates.
- https://www1.health.gov.il/nursing/work/recognized-programs/information-for-nurses/ - nurses' gmul hishtalmut (value is a function of recognized study hours).
