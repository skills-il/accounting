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
This skill does NOT ship frozen shekel wage-grade tables, because they change
with every agreement and CPI update. Read the current combined-salary cell from
the union or the Wage Commissioner, then reason from the structure below.

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

### Step 2: Read the base combined salary (grade by seniority)

The base line (sachar meshulav, combined salary) comes from a two-dimensional
table of grade (daraga) by seniority (vetek). The cell you read for a given
(grade, seniority) pair IS the combined salary and ALREADY includes seniority.
Do NOT add a seniority percentage on top of it, or you double-count. Seniority
years advance the row; the recognized vetek can include prior relevant
experience, so check the recognized count against the slip. Recognized seniority
also stops accruing after a capped number of years, so a base that stopped rising
with seniority is usually the cap, not an error.

The skill does not carry the NIS cells on purpose. Read the exact cell for the
grade, seniority, dirug, employer, and year from the profession union table or
the Wage Commissioner, then feed it as the base into `scripts/healthcare_gross.py`.

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
- Tosefet achayot 2024: a named supplement for state-employed nurses, 250 NIS
  per full-time position from 1.10.2024, updated to 500 NIS per full-time
  position from 1.4.2025.
- Shift pay comes in two distinct lines: a shift-responsibility supplement
  (tosefet achrayut mishmarot) paid to the nurse who takes responsibility for a
  shift (a rank-and-file ward nurse, not only a manager), and a rotating-shift
  supplement paid to two-shift and three-shift workers. Both change with the
  agreement; read the current amounts and keep them separate from statutory
  night and overtime pay.
- A charge-nurse-of-the-shift (achot achrait mishmeret) role line is paid to the
  ward nurse holding shift responsibility, distinct from the employer-specific
  management supplement (tosefet minhal / nihul) paid to nurses in management
  roles. An academic-degree supplement (tosefet toar) and legacy fold-in shekel
  supplements also appear on many slips. Read the current rate for each.

**Allied health.** The allied-health agreement pays a training supplement as a
percentage of the combined salary, banded by professional seniority. It replaces
the gmul-increment mechanism for these grades, but the keren hishtalmut (study
fund) itself still applies as a separate payroll line, so do not read this as
"no study fund". Render all three bands, not just one:

| Professional seniority | Training supplement |
|------------------------|---------------------|
| 0 to 7 years | 4.5% |
| 7 to 17 years | 5.5% |
| Over 17 years | 6.5% |

Allied-health workers also have a capped monthly incentive (tamritz); the
ceiling rose from 4,125 NIS to 5,400 NIS per full-time position per month from
1.4.2025. Some settings carry a retention and recruitment grant of 10,000 NIS
per full-time position for eligible workers (for example in psychiatric
hospitals and child-development units). The incentive and grants are variable or
conditional lines, not part of the fixed base.

**Doctors.** First pin the career stage, because the base track differs by it: a
resident (mitmach) sits on a different base track from a specialist (mumche), who
differs again from a senior or attending physician. Residents are themselves split
by the board exams: darga alef, before passing the written board exam (bechinat
shlav alef), works a 45-hour week; darga bet, after it, works 42 hours. Each stage
carries its own lines and a different on-call profile. Do not model "a doctor" as
one base cell.

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
| Holiday eve, 13:00 to 16:00 | Half a workday |

Planned duty shifts and on-call are not part of the base salary, so they do not
enter the pension and severance base the way the combined salary does. As a
department-level sanity check (not an individual's line), a department's rota runs
about 20 to 30 on-call slots a month, and about 60 in psychiatric hospitals; an
individual doctor works a fraction of those. Residents also carry a presence/stay
supplement (tosefet shehiya) among their standing slip lines; read the current
amount.

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

Pensionable base: not every line feeds the pension and severance base. As a rule
the combined salary, gmul hishtalmut, and certain permanent tosafot are
pensionable, while the incentive (tamritz), shift premiums, on-call, havraa, and
the clothing allowance are not. For budgetary-pension veterans the pensionable
subset (the mashkoret koveat gimlaot) is defined even more narrowly. When
estimating a pension or severance figure, separate the pensionable lines from the
rest rather than using the gross.

Additions on the gross side (not deductions): healthcare workers receive havraa
(recreation pay), and public-sector employees receive an annual clothing
allowance (ktzuvat bigud), usually paid once a year around July and set by grade
level. These appear on the slip on their own schedule, not evenly each month.

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
`python3 scripts/healthcare_gross.py --base <cell> --add 500 --add <shift_pay>
--position 1.0`, then apply Step 4 for net.

### Example 2: Physiotherapist, mid-career

A physiotherapist in the physiotherapists' dirug, 10 years of professional
seniority, full position. Reform is allied-health, so the training supplement is
5.5% (the 7 to 17 years band), applied to the combined salary. Gross: read the
(grade, seniority) cell (it already includes seniority), then apply 5.5% as a
tosefet. If the worker earns the capped monthly incentive, add it up to the
current 5,400 NIS ceiling. Run: `python3 scripts/healthcare_gross.py --base
<cell> --tosefet 5.5 --add <incentive> --position 1.0`. Note the incentive is a
variable line, not part of the fixed base.

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
- **Writing a banded rate flat.** The allied-health training supplement is 4.5%,
  5.5%, or 6.5% depending on professional seniority. Picking one band for
  everyone misstates the slip. Read the worker's seniority and apply the right
  band.
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

## Bundled Resources

- `references/dirug-map.md` - the healthcare wage grades and who falls under each.
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
