---
name: israeli-healthcare-payroll
description: "Explains and sanity-checks the salary of Israeli public-healthcare-sector workers (nurses / achim ve'achayot, allied-health / miktzo'ot habriut such as physiotherapists, occupational therapists, dietitians, and speech clinicians, hospital pharmacists, and doctors / rofim), which is set by public-sector collective agreements, not private-sector negotiation. Use when a user asks how a healthcare payslip is built: which wage grade (dirug) applies, the base combined-salary cell (grade daraga by seniority vetek), healthcare tosafot like the nurses' tosefet achayot or the allied-health training supplement, shift and on-call pay (mishmarot, kononut, toranut), and how gross becomes net. Do NOT use for standard private-sector gross-to-net payroll (use israeli-payroll-calculator), teachers' pay (use israeli-teacher-payroll), or private home caregivers (use foreign-caregiver-payroll)."
license: MIT
---

# Israeli Healthcare Payroll

## Legal notice

This is a free information tool operated by an AI model. It explains the tax rules and helps you organise your own figures. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by a tax adviser or accountant. The output is not a tax opinion, not a return prepared by a licensed representative, and not professional advice, but a general calculation and explanation only: it does not examine the full extent of your income or your complete documents. An AI model may err, omit data, or present a wrong conclusion.

Any form or text this tool produces is an automatic draft for your personal preparation only, and is not a filed return. Responsibility for reporting and for paying the tax is yours, the binding computation is the Tax Authority's, and representation before the Tax Authority is reserved to those permitted by law. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person. Consult a tax adviser or accountant before filing or paying. All use of its output is the user's sole responsibility.


## Problem

Israeli public-healthcare workers are not paid like private-sector employees.
A nurse, a physiotherapist, or a hospital doctor is paid under a public-sector
collective agreement: the base is a combined-salary cell from a wage-grade
(dirug) table of rank by seniority, and on top sit healthcare-specific
allowances (tosafot) and, for shift and on-call staff, pay lines that follow
their own rules. A generic gross-to-net calculator gets this wrong: it does not
know which of several dirugim the worker belongs to, it treats the base as a
freely negotiated number instead of a table cell that already includes
seniority, and it has no idea that a doctor's on-call is paid in workday
equivalents that are not even part of base salary. This skill encodes the
Israel-specific structure so an agent can read a healthcare payslip, estimate a
gross from the right track, and route the deduction step correctly.

## Instructions

Work in four steps. Steps 1 to 3 build the GROSS; step 4 turns gross into net.

Before any of them, know the layer sitting above every dirug: the public-sector
framework agreement (heskem misgeret) signed 17.7.2023 covering 2020 to 2027. It
moves EVERY wage-grade table, so a base read without it is stale by construction.

It pays a flat shekel supplement (tosefet shiklit) of 400 NIS from 1.7.2023,
raised to 500 NIS from 1.10.2024. **The raise to 500 does NOT reach everyone, and
nurses are on the excluded list**: nurses (including public-health nurses), social
workers, medical imaging technicians, medical technologists, and
administrative-and-maintenance staff all stay at 400 NIS. Do not put 500 NIS on a
nurse's slip. It also pays cumulative percentage raises: 2% from December 2024,
3.5% from April 2025, 5% from April 2026, 6% from April 2027.

**Order of operations (read this once and apply it consistently).** The tranches
are folded INTO the published wage table: a table issued as "in force from
1.4.2026" already contains the 5%. Read a DATED cell, check the date, and do NOT
apply a tranche on top of a cell that already postdates it. Apply a tranche
yourself only when deliberately rolling a cell forward from an earlier in-force
date to a later one, and say so when you do. Never apply a tranche to a cell of
unknown date.

The framework also shortened the working week from 42 hours to 40 in two steps,
182 monthly hours to 177.667 and then 173.333. That matters beyond leave: the
hourly rate (erech shaa) is monthly salary divided by the monthly hours norm, so
a shorter week RAISES erech shaa and every line derived from it. **The tranche
dates differ by employer and government hospitals are on their own schedule**:
first tranche 1.12.2023 (at the latest 1.1.2024), second 1.7.2024 (or 1.6.2024 if
the first was deferred). Every other employer under the agreement, local
government included, ran 1.10.2023 (deferrable to 1.11.2023) and 1.9.2024. Use the
hours norm actually in force for the month being read.

Do not assume a tosefet yoker (cost-of-living allowance) line is live: it is
activated only by a separate extension order and is not paid routinely.

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
para-medical grade are three separate dirugim. They are published as TWO table
sets, occupational therapy sharing one with the para-medical grade and
physiotherapy having its own, so never carry a physiotherapy number to either of
the other two. Pharmacists and some hospital scientists
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
is wrong: give it as the base index, then add Step 3. Do NOT add a framework
tranche here; a currently dated table already contains it.

`references/nurses-salary-tables.md` carries all five nurse grids in full (ranks
10 to 21, seniority 0 to 40) so the ladder can be read directly. Those cells are
effective 01/12/2008 and are reproduced for STRUCTURE ONLY.

**Do NOT bridge the 2008 cells forward to a current base.** The 2008 grid
predates every nurses' agreement and every public-sector raise between 2009 and
2023, and the framework tranches cover only the tail of that period. Multiplying
a 2008 cell by 2%, 3.5% or 5% produces a confidently wrong number, not an
estimate. Use the file for STRUCTURE only, never as the arithmetic base.

**Where the current cell actually comes from.** No current-dated grid is
published openly, so there is no URL to send the user to. In order of
reliability: the worker's own payslip, where it appears as a named line (sachar
meshulav) and which is usually the right answer to "what is my base"; the
employer's HR or payroll department, which holds the current table; then the
profession union or the Wage Commissioner on request. Feed that cell into
`scripts/healthcare_gross.py`. If none is available, say the current cell cannot
be established rather than estimating it from the 2008 grid.

### Step 3: Add the healthcare tosafot (and, for doctors, on-call)

On top of the combined-salary cell sit healthcare-specific additions. Some are a
percentage of the base; some are named fixed-shekel lines; shift and on-call pay
follow their own rules and are supplied as explicit amounts.

**Nurses.** A nurse's base is driven by more than the combined-salary cell:

- Gmul hishtalmut is one of the largest levers on a veteran nurse's pay: a
  permanent, pensionable percentage of the combined salary, credited in units of
  recognized study hours approved by the nursing studies committee. Read the
  current per-unit rate and unit cap from the committee rather than freezing a
  number. Omitting it understates a course-holding nurse badly.
- Tosefet achayot 2024: 250 NIS per full-time position from 1.10.2024, raised to
  500 NIS from 1.4.2025. It counts as salary for all purposes (hourly rate,
  overtime, on-call, severance, pension, keren hishtalmut), is pro-rated for
  part-time, and is excluded from special and reinforcement shift calculations.
- Tosefet nihul (management), from 1.12.2023: 7.2%, but ONLY for nurses at ranks
  14 to 21, so do not apply it across the board. Its base is the hourly-rate base
  as it stood on 31.12.2022, not the combined salary alone. Pensionable.
- Tosefet achrayut mishmarot, from 1.12.2023: 80 NIS per shift. NOT salary for
  any other purpose, so keep it out of the pensionable lines.
- A rotating-shift supplement, an academic-degree supplement (tosefet toar), and
  legacy fold-in shekel supplements also appear. Read each current rate. The full
  per-dirug table is in `references/healthcare-tosafot.md`.


**Allied health.** From 1.4.2025 the allied-health agreement pays tosefet
hachsharot (a training supplement) as a percentage of the combined salary, banded
by professional seniority. It is computed on the combined salary ONLY, with no
other contractual supplements in the base. Render all three bands, not just one:

| Professional seniority (years) | Tosefet hachsharot |
|--------------------------------|--------------------|
| 0 to 7 (7 excluded) | 3.50% |
| 7 to 17 (17 excluded) | 9.00% |
| 17 and over | 9.50% |

The band boundaries are exclusive at the top: a worker with exactly 7 years is in
the 9.00% band, not the 3.50% one. Seniority here is PROFESSIONAL seniority only,
counted from the date the licence was issued; army or national service does not
count toward it.

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

Allied-health workers also have a capped monthly incentive (tamritz); the ceiling
rose from 4,125 NIS to 5,400 NIS per full-time position per month for output from
1.4.2025. A retention and recruitment grant of 10,000 NIS per full-time position
goes to eligible workers who completed 12 continuous months, but only in eight
named psychiatric hospitals and child-development units at seven named medical
centres, paid in the January salary. The grant is explicitly NOT salary: no
severance, no hourly rate, no pension or keren hishtalmut deposits. The incentive
and the grant are variable or conditional lines, not part of the fixed base.


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

The day-equivalent values for each toranut and kononut band are tabulated in
`references/healthcare-tosafot.md`. In outline, a weekday toranut pays four
day-equivalents against a weekday kononut's two, which is why reading a kononut
value for an on-site duty roughly halves the line.

Planned duty and on-call are not part of base salary, so they do not enter the
pension and severance base the way the combined salary does. As a department-level
sanity check, a rota runs about 20 to 30 on-call slots a month and about 60 in
psychiatric hospitals; an individual doctor works a fraction of those. A doctor's
slip also carries a presence supplement (tosefet shehiya); read the amount.

Three more doctor-specific lines sit outside the base:

- Shortage-specialty premium (miktzo'ot bemtzuka): about 12.5% of the doctor's
  salary, for specialties such as neonatology, anesthesia, cardiology, and the
  general, pediatric, and cardiac intensive-care units.
- Periphery: a one-time recruitment grant (ma'anak periferia) of 300,000 NIS, and
  500,000 NIS for residents and shortage-specialty specialists, plus an ongoing
  periphery premium that ramped from 10% (from 1.8.2011) to 17.5% (2012) to 25%
  (from 1.8.2013) of salary for a resident or field specialist; read the current
  ongoing rate.
- Global additional hours (sha'ot nosafot globaliyot): a substantial senior-doctor
  line that is neither base nor on-call; read the current amount.

Use `scripts/healthcare_gross.py` to apply percentage tosafot to the
combined-salary cell and add explicit shift or on-call shekel amounts you have
computed. The script never re-adds seniority and never ships a NIS grade table.

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
  legislated in 2025. THREE tracks apply across the health dirugim, and which one
  applies depends on the dirug, not on the employer. Histadrut-represented
  healthcare dirugim are on the agreement track: 2.290% from December 2024 to
  December 2025, then 1.200% for 2026. Workers outside an approved collective
  agreement are on the law track: 0.000% to March 2025, 3.307% from April to
  December 2025, then 1.200%. The doctors' dirug is on a third track of its own
  under the agreement of 23.1.2025 (a freeze of the seniority supplement and of
  index linkage), NOT the 31.3.2025 wage agreement: 1.081% from 1.1.2025, raised
  to 1.781% for 1.7.2025 to 31.12.2025 by the monitoring committee of 30.6.2025,
  then back to 1.081% for 2026. Under the separate agreement of 14.5.2025,
  state-employed doctors' havraa was also cut, by 66.2% in 2025 and by 5% in 2026.

  All three end 31.12.2026 and no successor instrument has been published, so do
  not assume the 1.2% continues into 2027. A worker who changes dirug between
  1.4.2025 and 31.12.2025 KEEPS the track they started on. The line shows as
  "tikun pensioni", is computed on salary excluding havraa, the clothing
  allowance, expense reimbursements and non-monthly payments (mena'ak yovel IS in
  the base), and reduces the keren hishtalmut base. It does NOT reduce a one-off
  end-of-employment payment to the worker or their survivors, bridging payments,
  the amount paid into a pension fund, or the mashkoret koveat: the agreement
  lists those expressly and requires them to be computed as if the reduction had
  never been made, so never subtract it before computing those four items.
  A 2025 or 2026 slip read without this line overstates net pay. Full tables in
  `references/wage-reduction.md`.

Pensionable base: not every line feeds the pension and severance base. As a rule
the combined salary, gmul hishtalmut, and certain permanent tosafot are
pensionable, while shift premiums, on-call, havraa, and the clothing allowance
are not. The incentive (tamritz) is widely treated as non-pensionable but we
could not source that either way, so check the agreement rather than asserting
it. For budgetary-pension veterans the pensionable
subset (the mashkoret koveat gimlaot) is defined even more narrowly. When
estimating a pension or severance figure, separate the pensionable lines from the
rest rather than using the gross.

Additions on the gross side (not deductions): havraa (recreation pay) and an
annual clothing allowance (ktzuvat bigud). Both appear on their own schedule, not
evenly each month, and neither is pensionable.

**Public-healthcare workers are PUBLIC sector, so the public havraa day rate
applies**: 511.60 NIS a day from 1.6.2026, up from 471.40, per the Commissioner
on Wages circular of 8.6.2026. **Do NOT apply that rate raw to a doctors'-dirug
slip.** Under the collective agreement of 14.5.2025, state-employed doctors'
havraa was cut by 66.2% in 2025 and is cut by 5% in 2026, so a doctor's havraa is
the public rate less that year's reduction. The private-sector 451.50 NIS agreed on 22.6.2026
is a different figure for a different population, and using it understates every
havraa day. The days are higher than the private table and the per-dirug day
table sits in the Takshir rather than on a readable page, so read the days from
the employer and never reuse a private days table.

The clothing allowance was updated 1.9455% over 2025 by the circular of
17.6.2026, paid in the July 2026 salary and pro-rated. The 2026 amounts are
1,812.00 NIS at level 3 (to administrative grade 16 or unified 7) and 2,527.00
NIS at level 4 (grade 17 or 8 and above), per Takshir 28.425.

Two more lines a practitioner will look for:

- Mena'ak yovel (long-service award): a recurring public-sector tenure
  entitlement that appears on veteran slips. Unlike havraa and the clothing
  allowance, it IS inside the base on which the temporary wage reduction is
  computed. Read the current entitlement rule and amount for the dirug.
- Retroactive pay (hefreshei sachar, "retro"): expect it. Almost every agreement
  cited here was signed after its own effective date, so the money arrived as a
  back-payment lump rather than in the month it was earned. This is one of the
  most common reasons a slip refuses to reconcile against a computed gross: the
  month contains arrears for earlier months. Check for a retro line before
  concluding a figure is wrong. The temporary wage reduction does NOT apply to
  arrears paid for periods preceding its window.

## Examples

### Example 1: Hospital nurse, night shifts

A certified nurse in the nurses' dirug at a government hospital, grade and
seniority known, works rotating shifts including nights. Build gross: read the
combined-salary cell for that (grade, seniority) straight from the union table,
the cell already includes seniority so do NOT re-add it. Add the tosefet achayot
2024 (500 NIS per full-time from 1.4.2025), the current shift-responsibility
supplement per entitled shift, and the actual shift premium for the nights
worked. Statutory night and overtime hours follow standard labor law, so keep
them separate from the collective-agreement shift supplement. Run:
`python3 scripts/healthcare_gross.py --base <cell> --add-prorated 500 --add
<shift_pay> --position <fraction>`, then apply Step 4 for net. Tosefet achayot
2024 goes through `--add-prorated` because it is pro-rated for part-time, while
the shift pay goes through `--add` because it reflects shifts actually worked.

### Example 2: Physiotherapist, mid-career

A physiotherapist in the physiotherapists' dirug, 10 years of professional
seniority, full position. Physiotherapy is allied-health, so tosefet hachsharot
is 9.00% (the 7 to 17 band), applied to the combined salary only. Check first
whether the worker already holds a gmul hishtalmut larger than 9.00%: if so they
keep the gmul and get no tosefet hachsharot, since a worker never receives both.
Gross: read the current (education, rank, seniority) cell from the payslip or
employer (it already includes seniority, and if it is a currently dated table it
already includes the framework tranche), then apply 9.00% as a tosefet.
If the worker earns the capped monthly incentive, add it up to the current 5,400
NIS ceiling. Run: `python3 scripts/healthcare_gross.py --base <cell> --tosefet
9.0 --add <incentive> --position 1.0`. Note the incentive is a variable line, not
part of the fixed base.

### Example 3: Hospital doctor, duty and on-call

A specialist doctor under the IMA agreement, base read from the doctors' dirug
cell, who did several weekday on-site duties (toranut) and one weekday on-call
standby (kononut) in the month. Duty and on-call are paid in workday equivalents
times the day-value (erech yom): a weekday toranut is four day-equivalents (one
plus three, section 42), and a weekday kononut is two day-equivalents (section
49), so a toranut pays about double for the same day. Do not read the kononut
value for an on-site duty. Compute each shift as its day-equivalent count times
the doctor's day-value, sum them, and pass the total as an explicit addition.
These lines are NOT base salary, so they do not raise the pension and severance
base. Run: `python3 scripts/healthcare_gross.py --base <cell> --add <duty_total>
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
  paid in workday equivalents and are NOT part of base salary, so they do not
  raise the pension and severance base. Do not fold them into the combined salary.
- **Writing a banded rate flat.** Tosefet hachsharot is 3.50%, 9.00%, or 9.50%
  depending on professional seniority, and the jump from the first band to the
  second is large. Picking one band for everyone misstates the slip badly. Read
  the worker's professional seniority (from licence date, excluding army and
  national service) and apply the right band, remembering the boundaries are
  exclusive at the top.
- **Paying gmul hishtalmut and tosefet hachsharot together.** For allied-health
  grades the two are mutually exclusive; the worker gets the higher one only.
  Adding both overstates the slip.
- **Applying the nurses' management supplement to everyone.** Tosefet nihul
  (7.2%) is paid only at ranks 14 to 21. A nurse at rank 13 or below does not get
  it.
- **Quoting a combined-salary cell as "the salary".** The cell is a base index
  that supplements are computed from, not take-home pay. A rank-13 registered
  nurse's cell is about 3,038 NIS in the last openly published grid (effective
  01/12/2008), which is nowhere near what that nurse actually earns today.
- **Omitting the temporary wage reduction.** From December 2024 public-sector
  slips carry a negative line. A net estimate without it is too high.
- **Freezing a shekel table.** The combined-salary cells, the shift-responsibility
  amount, the clothing allowance, and the incentive ceiling all change with
  agreements and CPI. Read the current figure from the union or the Wage
  Commissioner; never hard-code a NIS cell.
- **Omitting the nurses' gmul hishtalmut.** For a course-holding nurse, the
  professional-development supplement is one of the largest lines on the slip and
  is pensionable. Leaving it out badly understates a veteran nurse's pay.
- **Modeling a doctor as one base cell.** A resident, a specialist, and a senior
  physician sit on different base tracks, and on-call and global hours sit on top.
  Pin the career stage before reading a doctor's slip.
- **Treating every line as pensionable.** Shift premiums, on-call,
  havraa, and the clothing allowance do not feed the pension and severance base.
  Do not estimate a pension or severance figure from the gross.
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
| [Public-sector framework agreement 2020-2027 (Malam)](https://www.malam-payroll.com/הסכם-קיבוצי-מסגרת-לשנים-2020-2027/) | The shekel supplement and the 2%/3.5%/5%/6% tranches that move every dirug table |
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
- `references/domain-checklist.md` - the coverage contract for this skill.
- `scripts/healthcare_gross.py` - applies percentage tosafot and explicit shift
  or on-call amounts to a combined-salary cell you supply (`--example` for a
  worked run). It never ships a NIS grade table and never re-adds seniority.
- `evidence.json` - every figure with its source and verbatim snippet.

## Troubleshooting

See `references/troubleshooting.md`.
