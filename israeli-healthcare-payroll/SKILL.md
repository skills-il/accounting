---
name: israeli-healthcare-payroll
description: "Explains and sanity-checks the salary of Israeli public-healthcare-sector workers (nurses / achim ve'achayot, allied-health / miktzo'ot habriut such as physiotherapists, occupational therapists, dietitians, and speech clinicians, hospital pharmacists, and doctors / rofim), which is set by public-sector collective agreements, not private-sector negotiation. Use when a user asks how a healthcare payslip is built: which wage grade (dirug) applies, the base combined-salary cell (grade daraga by seniority vetek), healthcare tosafot like the nurses' tosefet achayot or the allied-health training supplement, shift and on-call pay (mishmarot, kononut, toranut), and how gross becomes net. Do NOT use for standard private-sector gross-to-net payroll (use israeli-payroll-calculator), teachers' pay (use israeli-teacher-payroll), or private home caregivers (use foreign-caregiver-payroll)."
license: MIT
---

# Israeli Healthcare Payroll

## Legal notice

This is a free information tool operated by an AI model. It explains the tax rules and helps you organise your own figures. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by a tax adviser or accountant. The output is not a tax opinion, not a return prepared by a licensed representative, and not professional advice, but a general calculation and explanation only: it does not examine the full extent of your income or your complete documents. An AI model may err, omit data, or present a wrong conclusion.

The binding entitlement is determined by the collective agreement and the employer; in a dispute over pay, consult the union or a lawyer.

Any form or text this tool produces is an automatic draft for your personal preparation only, and is not a filed return. Responsibility for reporting and for paying the tax is yours, the binding computation is the Tax Authority's, and representation before the Tax Authority is reserved to those permitted by law. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person. Consult a tax adviser or accountant before filing or paying. All use of its output is the user's sole responsibility.


## Problem

Israeli public-healthcare workers are paid under public-sector collective
agreements: the base is a combined-salary cell from a wage-grade (dirug) table of
rank by seniority, with healthcare allowances (tosafot) and shift and on-call
lines on top. A generic gross-to-net calculator does not know the dirug, treats
the base as a negotiated number instead of a table cell that already includes
seniority, and has no idea that a doctor's on-call is paid in workday
equivalents outside base salary. This skill encodes that structure so an agent
can read a healthcare payslip, estimate a gross from the right track, and route
the deduction step correctly.

## Instructions

Work in four steps. Steps 1 to 3 build the GROSS; step 4 turns gross into net.

Before any of them, know the layer above the Histadrut-represented dirugim (the
nurses' and allied-health dirugim among them): the public-sector framework agreement (heskem
misgeret) signed 17.7.2023 covering 2020 to 2027. It adds two salary lines on top
of the combined cell, so a slip read without them looks short. Its scope clause
covers Histadrut-represented dirugim; doctors are represented by the IMA and paid
under their own agreement stack (Step 3), so do not add the framework lines to a
doctor's slip unless they appear on it.

It pays a flat shekel supplement (tosefet shiklit) of 400 NIS from 1.7.2023,
raised to 500 NIS from 1.10.2024. **The raise to 500 does NOT reach everyone, and
nurses are on the excluded list**: nurses (including public-health nurses), social
workers, medical imaging technicians, medical technologists, and
administrative-and-maintenance staff all stay at 400 NIS. Do not put the 500 NIS
framework supplement on a nurse's slip (the 500 NIS tosefet achayot in Step 3 is a
separate line).

**The percentage raise is its own slip line, not part of the table.** It is
tosefet achuzit 2024: 2.0% from the December 2024 salary, 3.5% from April 2025,
5.0% from 1.4.2026, 6.0% from April 2027 (the last step), computed on the
hourly-rate base: the CURRENT combined salary (and seniority supplement, where
the dirug pays one; a nurse's cell already includes vetek, so do not add it
again) plus those supplements in force on 31.12.2022 that count for erech shaa.
Later supplements (tosefet achayot, tosefet hachsharot, the shekel supplement)
are not in that base. It is salary for all purposes. So never multiply the combined cell by 2%, 3.5% or 5%: compute the
line on its own base, as for tosefet nihul, and treat it as a pro-rated shekel
line. Read it off the slip when you can.

The framework also shortened the working week from 42 hours to 40 in two steps,
182 monthly hours to 177.667 and then 173.333. That matters beyond leave: the
hourly rate (erech shaa) is monthly salary divided by the monthly hours norm, so
a shorter week RAISES erech shaa and every line derived from it. **The tranche
dates differ by employer and government hospitals are on their own schedule**:
first tranche 1.12.2023 (at the latest 1.1.2024), second 1.7.2024 (or 1.6.2024 if
the first was deferred). Every other employer under the agreement, local
government included, ran 1.10.2023 (deferrable to 1.11.2023) and 1.9.2024. Use the
hours norm actually in force for the month being read.

Full tables, the complete exclusion list, and the per-employer tranche schedule
are in `references/framework-agreement.md`.

### Step 1: Identify the wage grade (dirug) and the employer

The dirug decides which table and which tosafot apply, so pin it first. Public
healthcare pay is set by collective agreements between the Histadrut and the
profession unions and the Wage Commissioner (haMemune al haSachar) at the
Finance Ministry, organized into occupational wage grades.

| Worker | Dirug (wage grade) |
|--------|--------------------|
| Nurses (certified and practical) | Nurses' dirug (dirug achim ve'achayot) |
| Occupational therapists | Occupational-therapy dirug (dirug ripui be'isuk) |
| Physiotherapists | Physiotherapists' dirug |
| Dietitians and speech clinicians | Para-medical dirug (dirug para-refui) |
| Hospital pharmacists, medical physicists, some lab scientists | Academic dirug (dirug haMachar), not a health dirug. **This skill identifies the dirug for them but does NOT carry the academic-dirug supplement set**, so build their gross from the employer's own table and tosafot list rather than from Step 3, which covers nurses, allied health and doctors only |
| Doctors | Doctors' dirug under the IMA (haRi) agreement |

Allied health is not one grade: occupational therapy, physiotherapy and the
para-medical grade are three separate dirugim, so never carry a number from one
to another. Pharmacists and some hospital scientists
sit in the academic dirug, which is why two "healthcare" workers on the same ward
can be on different tables.

The employer of record is a separate question from the dirug. The same nurse
grade is paid by the Ministry of Health, Clalit, Hadassah, or a municipal
hospital. The employer issues the payslip and can run a different pension
arrangement and different employer-specific supplements even though the dirug
table is the same. Ask who employs the worker before reading a slip.

### Step 2: Read the base combined salary (education, rank, seniority)

The base line (sachar meshulav) is read from a table that is THREE-dimensional,
not two. Skipping the first dimension is the most common way to read the wrong
number:

1. **Pick the table by education level.** The nurses' dirug is not one table but
   five: practical (maasi), registered (musmach), BA, MA, and doctorate.
2. **Find the rank (daraga).** Nurse ranks run 10 to 21.
3. **Find the seniority row (vetek).** Rows run 0 to 40.

The cell at that (education, rank, seniority) point IS the combined salary and
ALREADY includes seniority. Do NOT add a seniority percentage on top, or you
double-count. The per-year increment is itself banded and flattens with age:
3.10% a year for years 1 to 9, 2.10% for 10 to 19, 1.90% for 20 to 32, 1.10% for
33 to 35, and 0.85% from 36 on. A veteran whose base has stopped moving is on the
flat end of that curve, not looking at a payroll error.

Education does not open a separate scale; it shifts the worker along the same
ladder by about one rank per level. At seniority 0 the same cell is reached by a
doctorate at 15, an MA at 16, a BA at 17, a registered nurse at 18, a practical
nurse at 19.

**The combined-salary cell is an index, not a take-home base.** This is the most
misread thing on an Israeli healthcare slip. The cell for a registered nurse at
rank 13 with no seniority is 3,037.67 NIS in the last openly published grid
(effective 01/12/2008), while that nurse's actual pay is several times that. The
cell is what every percentage supplement, the hourly rate and the pension base are
computed FROM, so answering "what does a rank-13 nurse earn" with the cell alone
is wrong: give it as the base index, then add Step 3 and the framework lines.

`references/nurses-salary-tables.md` carries all five nurse grids in full (ranks
10 to 21, seniority 0 to 40), effective 01/12/2008. **Use them for STRUCTURE
only and never bridge them forward**: the 2008 grid predates every nurses'
agreement and public-sector raise from 2009 to 2023, so multiplying a 2008 cell
by 2%, 3.5% or 5% gives a confidently wrong number, not an estimate.

**Where the current cell comes from.** No current grid is published openly. In
order of reliability: the worker's payslip (the sachar meshulav line), the
employer's HR or payroll department, then the union or the Wage Commissioner on
request. If none is available, say the cell cannot be established rather than
estimating it from the 2008 grid.

### Step 3: Add the healthcare tosafot (and, for doctors, on-call)

On top of the combined-salary cell sit healthcare-specific additions. Some are a
percentage of the base; some are named fixed-shekel lines; shift and on-call pay
follow their own rules and are supplied as explicit amounts.

**Nurses.** A nurse's base is driven by more than the combined-salary cell:

- Gmul hishtalmut is one of the largest levers on a veteran nurse's pay: a
  salary supplement whose value is a function of the recognized study hours
  approved by the nursing studies committee. Read the current rate and cap from
  the committee or the slip rather than freezing a number. Omitting it
  understates a course-holding nurse badly.
- Tosefet achayot 2024: 250 NIS per full-time position from 1.10.2024, raised to
  500 NIS from 1.4.2025. It counts as salary for all purposes (hourly rate,
  overtime, on-call, severance, pension, keren hishtalmut), is pro-rated for
  part-time, and is excluded from special and reinforcement shift calculations.
- Tosefet nihul (management), from 1.12.2023: 7.2%, but ONLY for nurses at ranks
  14 to 21, so do not apply it across the board. Its base is the same hourly-rate
  base as tosefet achuzit (current cell plus the supplements in force on
  31.12.2022 that count for erech shaa), not the combined salary alone. Pensionable.
- Tosefet achrayut mishmarot, from 1.12.2023: 80 NIS per shift. NOT salary for
  any other purpose, so keep it out of the pensionable lines.
- A rotating-shift supplement, an academic-degree supplement (tosefet toar), and
  legacy fold-in shekel supplements also appear. Read each current rate. The full
  per-dirug table is in `references/healthcare-tosafot.md`.


**Allied health.** The agreement of 22.4.2025 was signed by the government and
the municipal hospitals, and its implementation circular applies to allied-health
staff employed in Ministry of Health hospitals. Clalit and Hadassah are not
named, and no parallel agreement is carried here, so for their staff read the
supplement's name and rate from the slip and do NOT assert the bands below. From
1.4.2025 it pays tosefet hachsharot (a training supplement) as a percentage of
the combined salary, banded by professional seniority. It is computed on the combined salary ONLY, with no
other contractual supplements in the base. Render all three bands, not just one:

| Professional seniority (years) | Tosefet hachsharot |
|--------------------------------|--------------------|
| 0 to 7 (7 excluded) | 3.50% |
| 7 to 17 (17 excluded) | 9.00% |
| 17 and over | 9.50% |

The band boundaries are exclusive at the top: a worker with exactly 7 years is in
the 9.00% band, not the 3.50% one. Seniority here is PROFESSIONAL seniority only,
meaning all work in the profession after the licence was issued, including at
other employers; army or national service does not count toward it.

Tosefet hachsharot REPLACES gmul hishtalmut for these grades rather than adding to
it, and a worker never receives both. The rule is the higher of the two: a worker
whose existing gmul hishtalmut is larger keeps the gmul and gets no tosefet
hachsharot; once rising seniority makes tosefet hachsharot the larger of the two,
the worker moves to it and stops receiving the gmul. The keren hishtalmut (study
fund) itself is a separate payroll line and still applies, so do not read any of
this as "no study fund". Tosefet hachsharot is salary for all purposes, including
the hourly rate, on-call, severance, pension, and keren hishtalmut.

Allied-health staff in government hospitals are also entitled to a position-scope
grant (mena'ak heikef misra) under the same 22.4.2025 agreement, per implementation
instructions issued 18.9.2025 and paid in the April 2026 salary. It is conditional,
on an undertaking to work at a qualifying position fraction and on completing a
number of months at it, so it will not appear on every slip and is easy to miss.

Allied-health workers also have a capped monthly incentive (tamritz), whose
ceiling rose from 4,125 NIS to 5,400 NIS per full-time position per month for
output from 1.4.2025, and, in eight named psychiatric hospitals and
child-development units at seven named medical centres only, a 10,000 NIS
retention grant per full-time position after 12 continuous months, paid in the
January salary. The grant is explicitly NOT salary (no severance, hourly rate,
pension or keren hishtalmut deposits). Neither is part of the fixed base.


**Doctors.** First pin the career stage, because the base track differs by it: a
resident (mitmach) sits on a different track from a specialist (mumche), who
differs again from a senior physician, and residents split by the board exams
into darga alef (45-hour week) and darga bet (42). Do not model "a doctor" as one
base cell.

Doctors have their own agreement (30.9.2024, replacing the 2011 one) raising the
combined-salary table cumulatively: 4.88% from 1.1.2025, 6.5% from 1.7.2025, 7.5%
from 1.1.2026. It has been amended repeatedly, so name the amendment you rely on.
A separate tosefet mesima leumit runs 1.1.2025 to 31.12.2029 on a base of 3,000
NIS staged to 4,500 then 6,000, with pension computed as if 6,000 throughout; it
is salary for severance and carries keren hishtalmut but is NOT in the mashkoret
koveat. The base is multiplied by a per-specialty coefficient, so the headline
figure is not what an individual doctor receives. Detail in
`references/healthcare-tosafot.md`.

A doctor's slip is structurally different: much of the pay is duty and on-call,
paid in workday equivalents that are NOT part of base salary. The two words are
distinct and pay differently. Toranut is an on-site duty shift; kononut is
on-call standby from home. A toranut pays roughly double a kononut for the same
weekday, so never read a kononut value for an on-site duty. Both are valued off
the doctor's day-value (erech yom), so the same shift pays a specialist more than
a resident.

The day-equivalent values for each band are tabulated in
`references/healthcare-tosafot.md`.

The IMA agreement says planned duty and on-call are not part of the salary, so
treat them as outside a doctor's pension and severance base unless the slip
shows deposits on them (Step 4). As a department-level
sanity check, a rota runs about 20 to 30 on-call slots a month and about 60 in
psychiatric hospitals; an individual doctor works a fraction of those. A doctor's
slip also carries a presence supplement (tosefet shehiya); read the amount.

Two more doctor lines sit outside the base: a shortage-specialty premium
(miktzo'ot bemtzuka) of about 12.5% of salary for specialties such as
neonatology, anesthesia and intensive care; periphery pay, a one-time recruitment
grant of 300,000 NIS (500,000 for residents and shortage-specialty specialists)
plus an ongoing premium that reached 25% of salary from 1.8.2013 for a resident or
field specialist. Read the current ongoing periphery rate from the slip; the ramp
history is in `references/healthcare-tosafot.md`.

Use `scripts/healthcare_gross.py` to apply percentage tosafot to the
combined-salary cell and add explicit shift or on-call shekel amounts you have
computed. The script never re-adds seniority and never ships a NIS grade table.
On a host with no shell, do the same arithmetic by hand: gross = cell x (1 +
sum of percentage tosafot / 100) x position, plus full-position pro-rated shekel
lines x position, plus the worked shift and on-call amounts. Tosefet nihul and
tosefet achuzit are not percentages of the cell: compute each on the hourly-rate base and treat it
as a pro-rated shekel line.

### Step 4: Gross to net

Healthcare net follows the standard statutory deductions. For the full mechanics
(income-tax brackets, credit points, ceilings) defer to the
`israeli-payroll-calculator` skill; do not restate income-tax brackets here. The
pieces:

- Income tax (mas hachnasa): progressive brackets, less credit points.
- National insurance (bituach leumi) and health tax (mas briut), employee share:
  charged on a reduced step and a full step. Health tax is 3.23% up to the
  reduced-collection step of 7,703 NIS (2026) and 5.17% above it. For the exact
  National Insurance percentages and the full net mechanics, defer to
  israeli-payroll-calculator.
- Pension: check the pension TYPE. Veteran workers hired long ago may be on a
  budgetary pension (pensia taktzivit), where the employee deduction differs;
  newer workers are on a funded pension (pensia tzoveret) into a pension fund.
  Ask which one applies before estimating net.
- Keren hishtalmut (study fund) and union dues: essentially every public-sector
  healthcare slip carries a union deduction (demei chaver or demei tipul) to the
  Histadrut or the profession union. Do not omit it; read the current amount.
- Temporary wage reduction (hafchatat sachar zmanit): a war-cost participation
  deduction, agreed by collective agreement on 25.11.2024 and separately
  legislated in 2025. THREE tracks apply, chosen by the dirug, not the employer.
  Histadrut-represented healthcare dirugim are on the agreement track: 2.290%
  from December 2024 to December 2025, then 1.200% for 2026. Workers outside an
  approved collective agreement are on the law track: 0.000% to March 2025,
  3.307% from April to December 2025, then 1.200%. The doctors' dirug has its own
  track under the agreement of 23.1.2025 (a freeze of the seniority supplement
  and of index linkage), NOT the 31.3.2025 wage agreement: 1.081% from 1.1.2025,
  raised to 1.781% for 1.7.2025 to 31.12.2025 by the monitoring committee of
  30.6.2025, then back to 1.081% for 2026.

  All three end 31.12.2026 and no successor instrument has been published, so do
  not assume the 1.2% continues into 2027. A worker who changes dirug between
  1.4.2025 and 31.12.2025 KEEPS the track they started on. The line shows as
  "tikun pensioni", is computed on salary excluding havraa, the clothing
  allowance, expense reimbursements and non-monthly payments (mena'ak yovel IS in
  the base), and reduces the keren hishtalmut base. Never subtract it before
  computing a one-off end-of-employment payment to the worker or their survivors,
  bridging payments or an employer-funded annuity top-up, the amount paid into a
  pension fund, the mashkoret koveat, or budgetary pension payments: the
  agreement and section 8 of the law list them and require them computed as if
  the reduction had never been made. On income tax, the law reduces the salary
  itself (section 2), and section 8(3) neutralises the reduction only for the tax
  treatment of pension contributions, so on the statute's structure the reduced
  salary is what is taxed. No Tax Authority instruction says so expressly (the
  employer reports the amount in Tofes 126), so reconcile against the slip's
  income-tax line. A 2025 or 2026 slip read without this line
  overstates net pay. Full tables in `references/wage-reduction.md`.

**Pension and severance base: split by pension type and employer.** Never
estimate a pension or severance figure from the gross, and never apply one
"pensionable" list to everyone:

- Budgetary pension (veterans): the mashkoret koveat is a narrow defined subset
  that does not include havraa. Read it from the employer.
- State employees on a funded pension (government-hospital staff covered by the
  transfer agreement of 3.3.1999): under Accountant General instruction 13.7.2
  (in force from 22.12.2011), tier 1 is that determining salary plus havraa
  (and yovel, which the 2026 circular instead puts in tier 2: read the slip) plus
  every other monthly component except expense reimbursements, tax gross-up and
  clothing, and tier 2 is pay for additional work. Both carry employee, employer
  and severance deposits (6% in the pension-fund tables). Whether a given line
  carries deposits still depends on the applicable collective agreement (para
  4.1): the 80 NIS shift-responsibility supplement is excluded, and the IMA
  agreement puts doctors' planned duty and on-call outside the salary.
- Severance the state pays directly includes one twelfth of the havraa (Takshir
  28.246).
- Clalit, Hadassah and municipal hospitals: read the employer's arrangement.

The 80 NIS shift-responsibility supplement and the setting grants are expressly
not salary whatever the pension type. Detail in
`references/pension-and-annual-lines.md`.

**Annual and irregular lines** (rules in `references/pension-and-annual-lines.md`,
days tables in `references/havraa-days.md`):

- Havraa: the PUBLIC rate, 511.60 NIS a day from 1.6.2026 (471.40 before; circular
  of 8.6.2026), never the private 451.50, usually paid once in the summer (June to
  September). State-employee days under Takshir 28.241: government-hospital staff
  9 to 15 by recognized seniority, doctors 6 to 13 (table in force from 1.1.2026),
  allied health outside government hospitals 6 to 11, pro-rated for part time and
  a partial year. **Do NOT apply the rate raw to a doctor**: under the agreement of
  14.5.2025 state-employed doctors' havraa was cut by 66.2% in 2025 and by 5% in
  2026. Clalit, Hadassah and municipal hospitals are not shown to follow the
  Takshir days, so read theirs from the employer.
- Clothing allowance 2026: 1,812.00 NIS at level 3 and 2,527.00 NIS at level 4
  (levels per Takshir 28.425), paid in the July 2026 salary, pro-rated.
- Mena'ak yovel: paid every year from 25 years of seniority (30 for doctors), 60%
  of the hourly-rate base, pro-rated; nurses in the November salary, most dirugim
  in September. It IS in the wage-reduction base, with its own 2026 line.
- Nurses in named psychiatric and geriatric hospitals: 5,000 NIS setting grants
  per full-time position (the geriatric one every January after 12 continuous
  months).
- Retroactive pay (hefreshei sachar): almost every agreement here was signed after
  its effective date, so expect back-payment lumps. Check for a retro line before
  calling a figure wrong; the wage reduction does not apply to arrears for periods
  before its window.

When a user asks why a month came out lower, run the month-on-month checklist in
`references/pension-and-annual-lines.md` before blaming the wage reduction.

## Examples

### Example 1: Hospital nurse, night shifts

A certified nurse in the nurses' dirug at a government hospital, grade and
seniority known, works rotating shifts including nights. Build gross: read the
combined-salary cell from the payslip or the employer (Step 2); it already
includes seniority, so do NOT re-add it. Add the tosefet achayot
2024 (500 NIS per full-time from 1.4.2025), the current shift-responsibility
supplement per entitled shift, and the actual shift premium for the nights
worked. Statutory night and overtime hours follow standard labor law, so keep
them separate from the collective-agreement shift supplement. Run:
`python3 scripts/healthcare_gross.py --base <cell> --add-prorated 500
--add-prorated 400 --add-prorated <achuzit> --add <shift_pay> --position
<fraction>`, then apply Step 4.
Tosefet achayot (500) and the framework supplement (400 for nurses) are
pro-rated for part-time (`--add-prorated`, full-position amounts); shift pay
reflects shifts worked (`--add`).

### Example 2: Physiotherapist, mid-career

A physiotherapist in the physiotherapists' dirug at a government hospital, 10
years of professional seniority, full position (at Clalit or Hadassah, read the
supplement from the slip instead, per Step 3). Physiotherapy is allied-health, so tosefet hachsharot
is 9.00% (the 7 to 17 band), applied to the combined salary only. Check first
whether the worker already holds a gmul hishtalmut larger than 9.00%: if so they
keep the gmul and get no tosefet hachsharot, since a worker never receives both.
Gross: read the current cell from the payslip or employer (it already includes
seniority), apply 9.00%, and add the framework lines (500 NIS shekel supplement,
tosefet achuzit 2024 on its own base) with `--add-prorated`.
If the worker earns the capped monthly incentive, add it up to the current 5,400
NIS ceiling. Run: `python3 scripts/healthcare_gross.py --base <cell> --tosefet
9.0 --add-prorated 500 --add-prorated <achuzit> --add <incentive> --position 1.0`. Note the incentive is a variable line, not
part of the fixed base.

### Example 3: Hospital doctor, duty and on-call

A specialist doctor under the IMA agreement, base read from the doctors' dirug
cell, who did several weekday on-site duties (toranut) and one weekday on-call
standby (kononut) in the month. A weekday toranut is four day-equivalents (one
plus three, section 42) and a weekday kononut two (section 49); multiply each by
the doctor's day-value (erech yom), sum, and pass the total as an explicit
addition.
These lines are NOT base salary. Run: `python3 scripts/healthcare_gross.py --base <cell> --add <duty_total>
--position 1.0`.

## Gotchas

- **Treating healthcare pay as private-sector negotiation.** The base is a
  collective-agreement combined-salary cell (grade by seniority), not a freely
  negotiated gross. Read the table; do not invent a base from hours times a rate.
- **Using the wrong dirug.** Occupational therapy, physiotherapy, and the
  para-medical grade are three separate tracks, and pharmacists sit in the
  academic dirug, not a health dirug. The base row and the tosafot differ by
  track. Pin the dirug before reading any number.
- **Re-adding seniority that is already in the cell.** The (grade, seniority)
  cell IS the combined salary; it already includes vetek. Adding a seniority
  percentage on top double-counts it.
- **Confusing kononut with toranut.** Toranut is an on-site duty shift; kononut
  is on-call standby. They are different pay lines with different rules.
- **Putting on-call into the base.** For doctors, planned on-call and duty are
  paid in workday equivalents and are NOT part of base salary. Do not fold them
  into the combined salary.
- **Writing a banded rate flat.** Tosefet hachsharot is 3.50%, 9.00%, or 9.50%
  by professional seniority (from licence date, excluding army and national
  service, boundaries exclusive at the top). One band for everyone misstates the
  slip badly.
- **Paying gmul hishtalmut and tosefet hachsharot together.** For allied-health
  grades the two are mutually exclusive; the worker gets the higher one only.
  Adding both overstates the slip.
- **Applying the nurses' management supplement to everyone.** Tosefet nihul
  (7.2%) is paid only at ranks 14 to 21. A nurse at rank 13 or below does not get
  it.
- **Quoting a combined-salary cell as "the salary".** The cell is a base index
  that supplements are computed from, not take-home pay; the 2008 rank-13 cell is
  nowhere near what that nurse earns today.
- **Omitting the temporary wage reduction.** From December 2024 public-sector
  slips carry a negative line. A net estimate without it is too high.
- **Freezing a shekel table.** Cells, the shift-responsibility amount, the
  clothing allowance and the incentive ceiling all change with agreements and
  CPI. Read the current figure; never hard-code a NIS cell.
- **Omitting the nurses' gmul hishtalmut.** For a course-holding nurse, the
  professional-development supplement is one of the largest lines on the slip.
  Leaving it out badly understates a veteran nurse's pay.
- **Modeling a doctor as one base cell.** A resident, a specialist, and a senior
  physician sit on different base tracks, and on-call sits on top.
  Pin the career stage before reading a doctor's slip.
- **One pensionable list for everyone.** On a budgetary pension havraa sits
  outside the determining salary; on a state funded pension havraa and most
  monthly lines carry deposits, but the collective agreement decides each line
  (doctors' on-call does not). Pin the pension type
  and the employer first.
- **Forgetting who signs the slip.** The same dirug is paid by the Ministry of
  Health, Clalit, Hadassah, or a municipal hospital, which changes the pension
  arrangement, the employer-specific supplements, and who issues the payslip.

## Reference Links

| Resource | What it gives |
|----------|---------------|
| [Nurses' agreement summary (Malam)](https://www.malam-payroll.com/הסכם-שכר-בדרוג-אחיות-מיום-1-11-2023-תשלום-תוספ/) | Nurses' dirug supplements (tosefet achayot 2024, shift-responsibility) |
| [Allied-health agreement summary (Malam)](https://www.malam-payroll.com/הסכם-שכר-קיבוצי-לעובדי-מקצועות-הבריאו/) | Three allied-health dirugim, training bands, incentive ceiling, grants |
| [IMA collective agreements (on-call payment, section 49)](https://www.ima.org.il/CollectiveAgreements/Default.aspx?CategoryId=5118) | Doctors' on-call (kononut) day-equivalent values |
| [IMA collective agreements (duty payment, section 42)](https://www.ima.org.il/CollectiveAgreements/Default.aspx?CategoryId=5111) | Doctors' on-site duty (toranut) day-equivalent values |
| [Doctors' rights summary (WorkRights)](https://www.workrights.co.il/זכויות_רופאים) | Resident grades, shortage-specialty and periphery premiums, on-call frequency |
| [Employee rates, National Insurance and health tax (Bituach Leumi)](https://www.btl.gov.il/Insurance/Rates/Pages/לעובדים%20שכירים.aspx) | Reduced-collection step, health-tax rates, employee National Insurance rates |
| [Public-sector framework agreement 2020-2027 (Malam)](https://www.malam-payroll.com/הסכם-קיבוצי-מסגרת-לשנים-2020-2027/) | The shekel supplement and tosefet achuzit 2024 (2%/3.5%/5%/6%), two lines on top of the combined cell |
| [Nurses' agreement of 11.12.2023 (Malam)](https://www.malam-payroll.com/הסכם-שכר-בדרוג-אחיות-מיום-11-12-2023/) | Tosefet nihul 7.2% at ranks 14-21, shift-responsibility 80 NIS per shift |
| [Temporary wage reduction 2025-2026 (gov.il)](https://www.gov.il/he/pages/salary-reduction-2025-2026) | The reduction law itself, who it applies to, and employer reporting via Tofes 126 |
| [Wage-reduction rates by track (Malam)](https://www.malam-payroll.com/השתתפות-העובדים-במגזר-הציבורי-בהוצאו/) | The agreement-track and law-track reduction rates per period, and the tikun pensioni slip lines |
| [Doctors' agreement implementation circular (Malam)](https://www.malam-payroll.com/הוראות-ביצוע-להסכם-קיבוצי-רופאים-מיום-30-9-2024/) | Doctors' confirmed salary tranche, the national-mission supplement coefficient, and its pension treatment |
| [Nurses' combined-salary tables (service-conditions compendium)](https://ogdan.ladpc.net.il/?page_id=4385) | The five nurse grids by education level, effective 01/12/2008; source of `references/nurses-salary-tables.md`. Structure only, not current pay |

## Bundled Resources

- `references/dirug-map.md` - the healthcare wage grades and who falls under each.
- `references/nurses-salary-tables.md` - all five nurse combined-salary grids
  (education level by rank 10-21 by seniority 0-40), the education-offset ladder,
  and the seniority-increment schedule. Cells are effective 01/12/2008 and are
  reproduced for structure, NOT as current pay.
- `references/healthcare-tosafot.md` - the named healthcare additions and how each is paid.
- `references/framework-agreement.md` - the 2020-2027 framework layer: shekel
  supplement, exclusion list, percentage tranches, and the per-employer
  working-week tranche schedule.
- `references/wage-reduction.md` - the three temporary-wage-reduction tracks.
- `references/havraa-days.md` - the state-employee havraa days tables by dirug.
- `references/pension-and-annual-lines.md` - pension and severance base by
  pension type, havraa, clothing, yovel, setting grants, retro, and the
  "why is this month lower?" checklist.
- `references/domain-checklist.md` - the coverage contract for this skill.
- `scripts/healthcare_gross.py` - applies percentage tosafot and explicit shift
  or on-call amounts to a combined-salary cell you supply (`--example` for a
  worked run). It never ships a NIS grade table and never re-adds seniority.
- `evidence.json` - every figure with its source and verbatim snippet.

## Troubleshooting

See `references/troubleshooting.md`.
