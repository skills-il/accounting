---
name: israeli-healthcare-payroll
description: "Explains and sanity-checks the salary of Israeli public-healthcare-sector workers (nurses / achim ve'achayot, allied-health / miktzo'ot habriut such as physiotherapists, occupational therapists, dietitians, and speech clinicians, hospital pharmacists, and doctors / rofim), which is set by public-sector collective agreements, not private-sector negotiation. Use when a user asks how a healthcare payslip is built: which wage grade (dirug) applies, the base combined-salary cell (grade daraga by seniority vetek), healthcare tosafot like the nurses' tosefet achayot or the allied-health training supplement, shift and on-call pay (mishmarot, kononut, toranut), and how gross becomes net. Do NOT use for standard private-sector gross-to-net payroll (use israeli-payroll-calculator), teachers' pay (use israeli-teacher-payroll), or private home caregivers (use foreign-caregiver-payroll)."
license: MIT
---

# Israeli Healthcare Payroll

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
It pays a flat shekel supplement (tosefet shiklit) that reached 500 NIS, plus
cumulative percentage raises:

| Effective from salary of | Cumulative percentage raise |
|--------------------------|-----------------------------|
| December 2024 | 2% |
| April 2025 | 3.5% |
| April 2026 | 5% |
| April 2027 | 6% |

**Order of operations (read this once and apply it consistently).** The tranches
are folded INTO the published wage table: a table issued as "in force from
1.4.2026" already contains the 5%. So the rule is: read a DATED cell, check the
date, and do NOT apply a tranche on top of a cell that already postdates it.
Apply a tranche yourself only when you are deliberately rolling a cell forward
from an earlier in-force date to a later one, and say so explicitly when you do.
Never apply a tranche to a cell of unknown date.

Separately, do not assume a tosefet yoker (general cost-of-living allowance) line
is live. It is activated only by a separate extension order and is not paid
routinely, so check whether one is in force for the month being read before
putting it on a slip. The framework also shortened the public-sector working week
(42 hours down to 40 in two steps). That matters beyond leave: the hourly rate
(erech shaa) is the monthly salary divided by the monthly hours norm, so a
shorter week RAISES erech shaa and every line derived from it. Use the hours norm
in force for the month being read.

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
| Hospital pharmacists, medical physicists, some lab scientists | Academic dirug (dirug haMachar), not a health dirug |
| Doctors | Doctors' dirug under the IMA (haRi) agreement |

Allied health is not one grade: occupational therapy, physiotherapy, and the
para-medical grade (dietitians and speech clinicians) are three separate tracks
with their own tables and their own tosafot. Do not carry a number from one to
another. Pharmacists and some hospital scientists sit in the academic dirug, not
a health dirug, which is why two "healthcare" workers on the same ward can be on
different tables.

The employer of record is a separate question from the dirug. The same nurse
grade is paid by the Ministry of Health (government hospitals), by Clalit (which
owns hospitals and community clinics), or by Hadassah or a municipal hospital.
The employer issues the payslip and can run a different pension arrangement and
different employer-specific supplements, even though the dirug table is the
same. Ask who employs the worker before reading a slip.

### Step 2: Read the base combined salary (education, rank, seniority)

The base line (sachar meshulav, combined salary) is read from a table that is
THREE-dimensional, not two. Skipping the first dimension is the most common way
to read the wrong number:

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

Education does not open a separate pay scale; it shifts the worker along the same
ladder by about one rank per level. At seniority 0 the same cell is reached by a
doctorate at rank 15, an MA at 16, a BA at 17, a registered nurse at 18, and a
practical nurse at 19.

**The combined-salary cell is an index, not a take-home base.** This is the single
most misread thing on an Israeli healthcare slip. The cell for a registered nurse
at rank 13 with no seniority is 3,037.67 NIS in the last openly published grid
(effective 01/12/2008), while that nurse's actual monthly pay is several times
that. The cell is what every percentage supplement, the hourly rate, and the
pension base are computed FROM. If someone asks what a nurse at rank 13 earns,
answering with the cell alone is wrong: give the cell as the base index, then add
the supplements in Step 3. Do NOT also add a framework tranche here: a currently
dated table already contains it (see the order-of-operations rule above).

`references/nurses-salary-tables.md` carries all five nurse grids in full (ranks
10 to 21, seniority 0 to 40) so the ladder can be read directly. Those cells are
effective 01/12/2008 and are reproduced for STRUCTURE ONLY.

**Do NOT try to bridge the 2008 cells forward to a current base.** The gap is not
bridgeable with anything in this skill: the 2008 grid predates every nurses'
agreement and every public-sector raise between 2009 and 2023, and the 2020-2027
framework tranches cover only the tail of that period. Multiplying a 2008 cell by
2%, 3.5% or 5% produces a confidently wrong number, not an estimate. Use the file
to read the STRUCTURE (which rank range applies, how education shifts the ladder,
how the seniority curve flattens), never as the arithmetic base for current pay.

**Where the current cell actually comes from.** No current-dated grid for this
dirug is published openly, so there is no public URL to send the user to. Three
routes, in order of reliability:

1. **The worker's own payslip**, where the combined salary appears as a named
   line (sachar meshulav). Fastest and most reliable, and usually the right
   answer to "what is my base": ask them to read that line.
2. **The employer's HR or payroll department**, which holds the current table.
3. **The profession union or the Wage Commissioner**, on request.

Feed that cell into `scripts/healthcare_gross.py`. If none is available, say the
current cell cannot be established rather than estimating it from the 2008 grid.

### Step 3: Add the healthcare tosafot (and, for doctors, on-call)

On top of the combined-salary cell sit healthcare-specific additions. Some are a
percentage of the base; some are named fixed-shekel lines; shift and on-call pay
follow their own rules and are supplied as explicit amounts.

**Nurses.** A nurse's base is driven by more than the combined-salary cell:

- Gmul hishtalmut (professional-development supplement) is one of the largest
  levers on a veteran nurse's pay. Its value is a function of the recognized
  study hours, credited in units (a unit is a block of recognized study hours),
  approved by the nursing studies committee, and it is a permanent, pensionable
  percentage of the combined salary. Read the current per-unit rate and the unit
  cap from the nursing committee rather than freezing a number. A slip that omits
  gmul hishtalmut understates a course-holding nurse badly.
- Tosefet achayot 2024: a named supplement for nurses, 250 NIS per full-time
  position from 1.10.2024, updated to 500 NIS per full-time position from
  1.4.2025. It counts as salary for all purposes: hourly rate, overtime, on-call,
  severance, pension, and keren hishtalmut. It is pro-rated for part-time and is
  excluded from special and reinforcement shift calculations.
- Tosefet nihul (management supplement), from 1.12.2023: 7.2%, but paid ONLY to
  nurses at ranks 14 to 21. A nurse at rank 13 or below does not receive it, so
  do not apply it across the board. Its base is the hourly-rate base (combined
  salary, seniority, and the salary supplements that existed on 31.12.2022), not
  the combined salary alone. It is pensionable.
- Tosefet achrayut mishmarot (shift-responsibility supplement), from 1.12.2023:
  80 NIS per shift for entitled nurses. This one is NOT salary for other
  purposes: it does not enter the hourly rate, overtime, on-call, severance, or
  pension and keren hishtalmut deposits. Keep it separate from the pensionable
  lines.
- A rotating-shift supplement is paid to two-shift and three-shift workers, and
  is distinct from both of the above and from statutory night and overtime pay.
- An academic-degree supplement (tosefet toar) and legacy fold-in shekel
  supplements also appear on many slips. Read the current rate for each.


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

Allied-health workers also have a capped monthly incentive (tamritz); the ceiling
rose from 4,125 NIS to 5,400 NIS per full-time position per month for output from
1.4.2025. A retention and recruitment grant of 10,000 NIS per full-time position
goes to eligible workers who completed 12 continuous months, but only in eight
named psychiatric hospitals and child-development units at seven named medical
centres, paid in the January salary. The grant is explicitly NOT salary: no
severance, no hourly rate, no pension or keren hishtalmut deposits. The incentive
and the grant are variable or conditional lines, not part of the fixed base.


**Doctors.** First pin the career stage, because the base track differs by it: a
resident (mitmach) sits on a different base track from a specialist (mumche), who
differs again from a senior or attending physician. Residents are themselves split
by the board exams: darga alef, before passing the written board exam (bechinat
shlav alef), works a 45-hour week; darga bet, after it, works 42 hours. Each stage
carries its own lines and a different on-call profile. Do not model "a doctor" as
one base cell.

Doctors have their own agreement (signed 30.9.2024, covering the state, Clalit,
Hadassah and municipal hospitals) on top of the general framework. It raises the
combined salary in tranches, of which the confirmed first leg is 4.88% from
1.1.2025. Later legs exist but their exact percentages and dates could not be
confirmed against a reachable published source, so read them from the current
Wage Commissioner implementation circular rather than assuming a figure. A
separate tosefet mesima leumit (national-mission supplement) was raised during
2025, in two steps rather than one, by the amending agreement of 31.3.2025. Do
NOT quote a shekel amount for it from memory: the published amounts could not be
confirmed against a reachable source, and more importantly the headline figure is
not what any individual doctor receives.

**The amount is a base figure multiplied by a coefficient (mekadem)** set by
specialty and role, roughly 0.3 to 1.5: residents and field physicians at the
bottom, forensic medicine at the top. Applying the headline base to a resident
overstates the line about threefold. Read both the current base and the worker's
coefficient from the Wage Commissioner circular. It is mutually exclusive with
tosefet mar'ag (higher of the two, never both), is NOT counted in the mashkoret
koveat for gimlaot, and is time-limited rather than permanent.

A doctor's slip is structurally different: a large part of pay is duty and
on-call, both paid in workday equivalents that are NOT part of base salary. Two
words are distinct, must not be conflated, and pay differently. Toranut is an
on-site duty shift (the doctor is physically in the hospital). Kononut is on-call
standby from home (the senior doctor the on-site doctor consults). A toranut pays
roughly double a kononut for the same weekday, so never read a kononut value for
an on-site duty. Both are valued off the doctor's day-value (erech yom), the
monthly salary expressed as a single day's worth, so it rises with rank and the
same shift pays a specialist more than a resident.

Toranut (on-site duty, IMA agreement section 42):

| Toranut timing | Payment |
|----------------|---------|
| Weekday | One workday plus three more (four day-equivalents) |
| Friday eve or holiday eve | One workday plus four more (five day-equivalents) |
| Sabbath or holiday daytime | Two workdays plus half (two and a half day-equivalents) |

Kononut (on-call standby, IMA agreement section 49):

| Kononut timing | Payment |
|----------------|---------|
| Weekday, 16:00 to 08:00 next morning | Two workdays |
| Weekday, summoned in after 19:30 for 4.5 hours or more | Three workdays |
| Emergency-department, by a specialist | Three and a quarter workdays |
| Sabbath or holiday daytime, 08:00 to 16:00 | One workday |
| Sabbath eve or holiday eve, 13:00 to 16:00 | Half a workday |

Planned duty shifts and on-call are not part of the base salary, so they do not
enter the pension and severance base the way the combined salary does. As a
department-level sanity check (not an individual's line), a department's rota runs
about 20 to 30 on-call slots a month, and about 60 in psychiatric hospitals; an
individual doctor works a fraction of those. A doctor's payslip also carries a presence/stay supplement
(tosefet shehiya) among its standing lines; read the current amount.

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
  legislated on 27.3.2025. There are TWO tracks with different rates, and which
  one applies depends on whether the worker is covered by the collective
  agreement. Histadrut-represented healthcare dirugim are on the agreement track;
  doctors are covered by their own agreement of 31.3.2025; workers outside an
  approved collective agreement fall under the law track.

| Period | By agreement | By law |
|--------|--------------|--------|
| December 2024 to March 2025 | 2.290% | 0.000% |
| April 2025 to December 2025 | 2.290% | 3.307% |
| January 2026 to December 2026 | 1.200% | 1.200% |

  The two tracks converge at 1.200% for 2026 and the reduction ends 31.12.2026.
  A worker who changes dirug between 1.4.2025 and 31.12.2025 KEEPS the track they
  started on, even when the other track's rate is higher.

  It is computed on the salary excluding havraa, the clothing allowance, expense
  reimbursements, and payments not made monthly, weekly or daily; mena'ak yovel
  IS in the base. It shows on the slip as "tikun pensioni" and also reduces the
  keren hishtalmut base. It does NOT reduce the pensionable insured salary or
  final-settlement payments, so never subtract it before computing a pension.
  A 2025 or 2026 slip read without this line overstates net pay.

Pensionable base: not every line feeds the pension and severance base. As a rule
the combined salary, gmul hishtalmut, and certain permanent tosafot are
pensionable, while the incentive (tamritz), shift premiums, on-call, havraa, and
the clothing allowance are not. For budgetary-pension veterans the pensionable
subset (the mashkoret koveat gimlaot) is defined even more narrowly. When
estimating a pension or severance figure, separate the pensionable lines from the
rest rather than using the gross.

Additions on the gross side (not deductions): healthcare workers receive havraa
(recreation pay), and public-sector employees receive an annual clothing
allowance (ktzuvat bigud), paid annually rather than monthly. Read the current
payment month and the amount for the grade from the employer or the agreement
rather than assuming them. These appear on the slip on their own schedule, not
evenly each month, and neither is pensionable.

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
- **Treating every line as pensionable.** The incentive, shift premiums, on-call,
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
- `references/domain-checklist.md` - the coverage contract for this skill.
- `scripts/healthcare_gross.py` - applies percentage tosafot and explicit shift
  or on-call amounts to a combined-salary cell you supply (`--example` for a
  worked run). It never ships a NIS grade table and never re-adds seniority.
- `evidence.json` - every figure with its source and verbatim snippet.

## Troubleshooting

- **"I do not know the base rate."** The skill does not carry NIS grade cells on
  purpose (they change per agreement). Read the combined cell for the exact
  grade, seniority, and dirug from the union table or the Wage Commissioner, then
  feed it into `healthcare_gross.py`.
- **"The numbers do not match my payslip."** Check the dirug (allied health is
  three separate tracks), the recognized seniority (read the combined cell, do
  not re-add seniority), whether every tosefet is included, and, for a doctor,
  whether on-call was computed in workday equivalents rather than folded into
  base. The slip also carries lines the script does not model (clothing
  allowance, havraa, legacy fold-in supplements), and the pension type
  (budgetary vs funded) and union dues shift the net.
- **"Is this net or gross?"** This skill computes GROSS. Net needs Step 4 and the
  `israeli-payroll-calculator` skill for the deduction mechanics.
- **The user is a teacher, a private-sector employee, or a home caregiver.** Route
  to `israeli-teacher-payroll`, `israeli-payroll-calculator`, or
  `foreign-caregiver-payroll`; this skill is only public-healthcare-sector pay.
