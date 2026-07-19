---
name: israeli-teacher-payroll
description: "Computes and explains the salary of Israeli teachers (ovdei horaa / sachar ovdei horaa) under the two collective-agreement reforms: Ofek Chadash (ofek chadash, New Horizon, covering kindergartens, elementary, and junior-high) and Oz LaTmura (oz latmura, upper-secondary only). Use when a user asks how a teacher's pay is built: reform, rank (daraga), seniority (vetek), the weekly work-week split between front-of-class hours and private (pratani) hours, gmul (gmul) increments like gmul hishtalmut or gmul chinuch, and how gross becomes net. Also handles the split appointment, where one teacher teaches in both a junior-high and a high school and earns under both reforms at once, each part by its position fraction. Do NOT use for standard private-sector gross-to-net payroll (use israeli-payroll-calculator), bookkeeping journal entries (use israeli-bookkeeping-automation), or Bagrut and school-system navigation (use israeli-education-system)."
license: MIT
---

# Israeli Teacher Payroll

## Problem

Israeli teachers are not paid like private-sector employees. Their pay is set by
two collective-agreement reforms, Ofek Chadash and Oz LaTmura, each with its own
work-week structure, its own 9-rank salary table, and its own rules for
increments (gmulim). A generic gross-to-net calculator gets this wrong: it does
not know that a "full position" is a fixed weekly split of front-of-class hours,
private (small-group) hours, and stay/support hours; it does not know that rank
and seniority feed a collective-agreement table rather than an hourly rate; and
it forgets the gmulim that can add 10% to 30% on top. This skill encodes the
Israel-specific structure so an agent can explain a teacher's payslip, estimate a
gross salary from the right table, and route the deduction step correctly.

## Instructions

Work in four steps. Steps 1 to 3 build the GROSS; step 4 turns gross into net.

### Step 1: Identify the reform and school level

The reform decides everything downstream, so pin it first.

| Reform | Who | Ranks |
|--------|-----|-------|
| Ofek Chadash | Kindergarten (gan), elementary (yesodi), and junior-high (chativat beynayim) teachers | 9 (1-9) |
| Oz LaTmura | Upper-secondary (chativa elyona / high school) teachers | 9 |

Kindergarten teachers (gananot) are under Ofek Chadash, not Oz LaTmura: the Ofek
reform runs in kindergartens, elementary schools, and middle schools. Oz LaTmura
covers upper-secondary only. If the user is unsure, ask which grades they teach.
Never carry a number from one reform's table to the other. But a teacher who
teaches in two divisions at once (for example a junior-high and a high school) is
under both reforms at the same time; do not force a single reform on her, go to
Step 1b.

Who signs the payslip is a separate question from the reform. Upper-secondary
teachers are often employed by a baalut (an operator such as ORT, Amal, AMIT, or
Branco Weiss) or by a municipality rather than directly by the Ministry of
Education. The baalut issues the payslip and can run a different pension
arrangement, even though the Oz LaTmura salary structure still applies. Ask who
the employer of record is before reading a slip.

### Step 1b: The split appointment (a teacher under both reforms at once)

Step 1 pins ONE reform, but a teacher can teach across both divisions at the same
time and earn under BOTH reforms. The common case is a six-year school (chativa
shesh-shnatit): she teaches junior-high grades (7-9, Ofek Chadash, usually paid by
the Ministry of Education) and upper-secondary grades (10-12, Oz LaTmura, usually
paid by a baalut). A man can be in this position too; most teachers are women, so
the wording here is in the feminine. Do NOT pick one reform. Run the gross build
(Steps 2 to 3) TWICE, once per division, and add the two parts:

- Each division is its own position fraction (chelkiyut misra), for example a
  third position (1/3) in the junior-high plus two-thirds (2/3) in the high school.
  Each fraction is relative to THAT reform's own full position (Ofek 36 hours, Oz
  38 or 40), so combine them as fractions of a position, not as raw weekly hours.
- Each part uses its OWN reform: its own hour structure (Step 2), its own combined
  (rank x seniority) cell from that reform's table, and its own gmulim (Step 3),
  then scaled by that division's fraction. Read the recognized rank for each reform
  from the official table; the two ranks follow each reform's own advancement rules
  and the ministry's cross-reform recognition, so do not assume they are identical
  and do not invent a conversion. Seniority (vetek) is her own recognized teaching
  seniority, read into each reform's table.
- The two-gmul cap is per TEACHER, not per division: count role gmulim (gmulei
  tafkid) across the whole appointment, so a homeroom gmul in the junior-high plus a
  coordinator gmul in the high school is already the two-gmul maximum, not two per
  side.
- Total gross = Ofek part + Oz part. There is no blended table: the two parts stay
  separate and are summed. She keeps being paid under both reforms according to her
  position fraction in each division.

Two reforms is NOT the same as two employers. Who pays the slip depends on the
school's operator, not on the reform: a six-year school run by a single baalut or
municipality can pay BOTH the Ofek junior-high part and the Oz high-school part on
ONE payslip, and then there is one employer, one withholding, and no tax
coordination to do, even though she is under both reforms. The two-employer case
arises only when the two divisions are paid by two different payers (often the
Ministry for the junior-high and a baalut for the high school, but confirm the
actual payers, do not assume from the reform).

Only when there are two payers: by default she gets two separate payslips, so she
must file a tax coordination (teum mas) every year or the second employer withholds
income tax at the top rate, and each payer also deposits her pension separately
(possibly into different funds, each with its own ceiling). She can then request
salary unification (ichud maskorot) to get both parts on ONE organized payslip (an
Ofek section, an Oz section, a non-reform-benefits section, then a total), which
removes the teum mas and consolidates the deposits under one payer. Unification
needs permanence (kviut) at the employer she wants to be paid through, plus at
least a third position (1/3) in the junior-high to unify through the Ministry, or
at least a half position (1/2) in the high school to unify through the baalut. One
caveat: when the two parts together exceed a full position (100%), unification can
make her lose benefits that are capped at 100% of a position, such as havraa
(recreation pay), bigud (clothing allowance), and meonot (childcare subsidy); weigh
that against the convenience of one payslip.

### Step 2: Read the reform's work-week structure

A full 100% position is a fixed weekly split. Front-of-class ("frontal") hours
are only part of it; private and stay/support hours are also paid work.

Ofek Chadash, full position = 36 weekly hours:

| Level | Frontal | Private | Stay | Total |
|-------|---------|---------|------|-------|
| Elementary | 26 | 5 | 5 | 36 |
| Junior-high | 23 | 4 | 9 | 36 |

Kindergarten (gan) teachers are also under Ofek Chadash, but the gan work-week is
defined differently from the school rows above. Read the current gan structure
from the union or the ministry rather than reusing an elementary row.

Oz LaTmura, base position = 40 weekly hours: 24 frontal + 6 private + 10
teaching-support. From school year tashpe (2024/25) this becomes 38 hours (25
frontal + 3 private, support unchanged) - check the year on the payslip, since
older tables still show 40. See `references/reform-hour-structure.md`.

Private hours mean teaching one student or a small group (Ofek: up to 5; Oz: up
to 3, or up to 5 by pedagogical decision). If a teacher works less than a full
position, scale by the position fraction.

### Step 3: Build the gross

1. Read the combined salary directly from the official table. The union salary
   tables and the ministry salary-simulation calculator are two-dimensional
   grids of rank (daraga) by seniority (vetek). The cell you read for a given
   (rank, seniority) pair IS the "combined salary" (sachar meshulav): it ALREADY
   includes seniority. Do NOT add a seniority percentage on top of it, or you
   double-count. The 2% per year up to year 7 and 1% per year from year 8 to
   year 36 is the rule the table already applied to produce that cell; it is not
   something you re-add.
2. Rank context (for reading the right row): rank 1 is a new teacher. Under Ofek
   Chadash, promotion up to rank 6 needs paznun plus 60 professional-development
   hours a year, and rank 7 and up adds 75 hours a year, promotion quotas, and a
   personal evaluation. This dev-hour promotion rule is Ofek-specific. Oz
   LaTmura rank advancement runs on merit points, not on a dev-hour quota, so do
   not apply the Ofek promotion rule to an Oz teacher.
3. Apply gmulim as a percentage of the combined salary you read in step 1. Cap:
   at most two role gmulim (gmulei tafkid) per teacher.

| Gmul | Rate |
|------|------|
| Gmul hishtalmut (professional development) | 1.2% per 112-hour unit, up to 16 units; up to 29.7% for dual-degree. Per-unit rate rose to 1.3% from 1.9.2025 |
| Gmul chinuch (homeroom) | 10%, or 11.5% for grade-1 homeroom |
| Gmul rikuz miktzoa (subject coordinator, not English/math) | 8% |
| Gmul pituach miktzoi (professional-development role) | 6% |
| Gmul nihul gan (kindergarten management, an Ofek Chadash role) | ~17% up to 5 yrs, 20% for 6-10 yrs |

**Oz LaTmura shekel supplement (tosefet shiklit).** The Irgun HaMorim agreement
of 23.9.2024, whose execution directive took effect 1.9.2025, raised the Oz
shekel supplement from 1,200 NIS to 1,518 NIS. Two further steps of 250 NIS each
are signed and future-dated to 1.9.2026 and 1.9.2027, so a slip read in the
autumn of 2026 should already carry the first of them. This is an Oz LaTmura
line: do not apply it to an Ofek Chadash teacher.

The same agreement also changed several coordinator (rakaz) gmulim from 1.9.2025.
The authoritative rate table for those is published as an image rather than page
text, so read the current per-role rate from the execution circular instead of
assuming the rates above still hold for an Oz coordinator.

Two Ofek Chadash items were deferred rather than paid: gmul beit-sifri moved from
1.9.2025 to 1.9.2026, and the shiluv/pitzul gmul cost-frame was frozen. Do not
show either as already paid on a 2025 slip.

More gmulim exist beyond this list. School principals and their deputies earn a
gmul nihul / sgan menahel (distinct from the kindergarten gan-management gmul),
and special-education teachers earn a gmul chinuch meyuchad. English, mathematics,
and physics teachers sit under their own separate incentive and coordination
arrangements, which is why the subject-coordinator gmul above is scoped to
subjects other than English and math. Read the exact current rate for any of
these from the union table, do not invent one.

Reform difference: Ofek Chadash teachers do NOT bank hishtalmut or merit gmulim
(dev hours push the rank instead) BUT role gmulim (for example gmul chinuch for a
homeroom, or gmul nihul gan) still apply to them. Oz teachers bank at most one
gmul a year, and merit points convert to promotion gmulim (10 points = 2%, up to
8%). See `references/gmul-components.md`.

Use `scripts/teacher_gross.py` to apply gmulim to the combined-salary cell once
you have read it. The script takes the combined cell as its base input and adds
only gmulim; it does not re-add seniority.

This gross model (combined cell times the gmul factor) is an approximation, not a
full payslip. Real teacher slips also carry fixed-shekel additions (tosafot
shkaliyot) and reform or percentage tosafot that do NOT scale with rank, plus
havraa (recreation pay). A model built only from base times gmulim cannot express
those lines, so treat the script's output as an estimate of the core salary and
reconcile it against the actual slip.

### Step 4: Gross to net

Teacher net follows the standard statutory deductions. For the full mechanics
(brackets, credit points, ceilings) defer to the `israeli-payroll-calculator`
skill; do not restate income-tax brackets here. The pieces:

- Income tax (mas hachnasa): progressive brackets, less credit points.
- National insurance (bituach leumi), employee share: reduced rate 1.04% (raised
  from 0.40%), full rate 7.00% above the reduced step.
- Health tax (mas briut): 3.23% up to the reduced step of 7,703 NIS, 5.17% above.
- Pension: check the pension TYPE, because it changes the employee deduction and
  the net. Veteran teachers (typically hired before 2000-2004) may be on pensia
  taktzivit (budgetary pension), where the state pays the future pension and the
  employee deduction differs. Newer teachers are on pensia tzoveret (funded /
  accumulating pension) into a pension fund. Ask which one applies before
  estimating net.
- Keren Hishtalmut: teachers contribute to a study fund via the employer; the
  teacher study funds and their exact split are teacher-specific, so read the
  slip rather than assume a private-sector rate.
- Union dues: essentially every teacher slip carries a union deduction, demei
  chaver (member dues) or demei tipul (handling dues), to Histadrut HaMorim
  (Ofek / kindergartens and elementary and middle school) or to Irgun HaMorim
  (upper-secondary). Do not omit it. Read the current amount from the union;
  do not invent a rate.

**The temporary wage reduction (2025 and 2026).** Teachers ARE covered by the
war-cost participation deduction, and a teacher slip read without it will
overstate net pay. Union representation does not exempt anyone: the 27.3.2025
temporary-order law binds the whole broad public sector, and the teacher unions
negotiated a mitigation on top of it rather than an exemption. The rate differs
by reform, so do NOT carry one rate across both:

| Period | Ofek Chadash | Oz LaTmura |
|--------|--------------|------------|
| December 2024 to March 2025 | 2.290% | 2.290% |
| April 2025 | 3.307% (superseded below) | 3.307% |
| 1.5.2025 to 31.12.2025 | 0.95% | see note |
| 1.1.2026 to 31.12.2026 | 1.2% | 1.2% |

The 0.95% mitigation comes from the collective agreement of 29.6.2025 and is
scoped explicitly to teachers employed under Ofek Chadash. No equivalent
mitigating agreement for Oz LaTmura was locatable, so for an Oz teacher in the
May to December 2025 window do not assume 0.95%: check the current circular, and
state that the law rate of 3.307% applies unless a separate agreement is found.
That agreement also excludes teacher-college staff and state-service supervisory
and HQ teaching staff.

**On a teacher's slip the line is NOT called "tikun pensioni".** The rest of the
public sector shows tikun pensioni split across three components; teachers get a
single line under the symbol `חוק הת. כלכלית אופק`. A teacher searching their
slip for "tikun pensioni" will not find it and will conclude the deduction is
missing. The reduction is scaled by an absence coefficient and does not affect
the minimum-wage calculation.

**Your pension is not reduced.** The deduction does not harm pension or provident
contributions, does not reduce the mashkoret koveat for those retiring on a
budgetary pension, and does not reduce gmulim or grants. Note the easy inversion:
pensionable salary is the BASE used to COMPUTE the seniority-advancement
reduction below, but it is not itself reduced.

**The seniority-advancement reduction (September to December 2025 only).** This
one is teacher-specific and has no analogue elsewhere in the public sector. A
teacher entitled to a seniority (vetek) step in the salary table had an extra
amount deducted for those four months, equal to the raise the step would have
paid. The rate is banded by seniority, and the base is first-tier pensionable
salary minus the shekel supplements that seniority does not affect:

| Seniority (years) | Reduction |
|-------------------|-----------|
| 0 to under 6 | 1.9603% |
| 6 to under 36 | 0.9900% |
| 36 and over | 0.0000% |

This applies ONLY to employers that signed the agreement and does NOT apply to
teaching staff employed by local authorities. Separately the seniority payment
itself was frozen for those same four months and resumed in January 2026, with
no loss of seniority-dependent rights.

**One December 2025 anomaly worth recognising.** The December 2025 deduction was
0.95% PLUS the school-hours amount otherwise payable that month, and that extra
was refunded through the reduction component in the January 2026 salary. An
unexplained one-month spike followed by a reversal is this, not a payroll error.

**The 2023 public-sector framework agreement does NOT apply to teachers.** Its
shekel supplement and its 2% / 3.5% / 5% / 6% tranches are scoped to dirugim
represented by the general Histadrut, and teacher dirugim are represented by
Histadrut HaMorim and Irgun HaMorim instead. Teachers reading press coverage of
the April 2026 5% tranche will expect it and should be told plainly that their
raises come from their own agreements. The framework's own "teaching employees"
clause exists only to stop double-counting for non-teachers whose pay is pegged
to the teacher scale.

Additions on the gross side (not deductions): teachers receive havraa
(recreation pay) like other employees, and teacher pay is spread across all
twelve months, so July and August are paid even though school is on summer break.
The annual clothing allowance was de-indexed and cut by 91 NIS: 2,405 NIS in
2024, 2,314 NIS in 2025.

Context: minimum wage is 6,247.67 NIS/month (from 1.4.2025), 6,443.85 NIS (from
1.4.2026); the average wage is 13,769 NIS (Jan 2026). Teacher base pay comes from
the agreement table, not from these figures.

## Examples

### Example 1: Ofek Chadash elementary homeroom teacher

Teacher in an elementary school, rank 4, 5 years seniority, homeroom of a grade-3
class, full position. Reform is Ofek Chadash, so the position is 36 hours (26
frontal + 5 private + 5 stay). Build gross: read the combined-salary cell for
rank 4 at 5 years seniority straight from the official grid, that cell already
includes the seniority, so do NOT re-add it. Then apply only the 10% gmul chinuch
on top. This teacher is under Ofek, and Ofek teachers do not bank hishtalmut
gmulim, but the homeroom role gmul still applies to them. Run:
`python3 scripts/teacher_gross.py --base <rank4_year5_cell> --gmul 10
--position 1.0`. Then apply Step 4 for net.

### Example 2: Oz LaTmura upper-secondary teacher with development gmul

Teacher in a high school, rank 6, 12 years seniority, subject coordinator (not
English or math), holds 8 units of gmul hishtalmut, full position. Reform is Oz
LaTmura, position 38 hours from tashpe (25 frontal + 3 private + 10 support).
Gross: read the rank-6 at 12-years-seniority cell (it already includes the
seniority), then apply gmulim = 8% coordinator + (8 units x 1.3% =) 10.4%
development. Coordinator plus development is within the two-role cap. This teacher
advances rank on merit points, not on Ofek dev-hour quotas. Run:
`python3 scripts/teacher_gross.py --base <rank6_year12_cell> --gmul 8 --gmul 10.4
--position 1.0`.

### Example 3: Kindergarten manager under Ofek Chadash, half position

Kindergarten manager (gananet menahelet) under Ofek Chadash (kindergartens are an
Ofek reform, not Oz), rank 3, 3 years of management seniority, gmul nihul gan
(~17% for up to 5 years of management seniority), half position. Gross: read the
rank-3 combined-salary cell (already includes seniority), apply the ~17% gmul
nihul gan, then scale by 0.5. The management gmul is one role gmul, leaving room
for at most one more. Caveat for part-time slips: not every component scales the
same way under chelkiyut misra. Some role gmulim are not scaled like the combined
salary, so a blanket multiply by the position fraction can misstate a part-time
slip; confirm against the actual slip.

### Example 4: Teacher split across both reforms in a six-year school

A teacher in a six-year school teaches a third position (1/3) in the junior-high
grades (Ofek Chadash, paid by the Ministry) and two-thirds (2/3) in the
upper-secondary grades (Oz LaTmura, paid by an ORT baalut). She is under both
reforms at once, so build gross TWICE and sum. Ofek part: read her Ofek combined
cell for her rank and seniority, apply her Ofek role gmulim (say 10% gmul chinuch
for a junior-high homeroom), scale by 1/3. Oz part: read her Oz combined cell for
her Oz rank and the same recognized seniority, apply her Oz gmulim, scale by 2/3.
Total gross = Ofek part + Oz part. Run the script once per division and add:
`python3 scripts/teacher_gross.py --base <ofek_cell> --gmul 10 --position 0.333`
then `python3 scripts/teacher_gross.py --base <oz_cell> --gmul 8 --position 0.667`.
Her two role gmulim (homeroom in the junior-high, coordinator in the high school)
are already the two-gmul maximum, counted across the whole appointment. If a single
baalut runs the six-year school and pays both divisions, this is one payslip with
no tax coordination; if the Ministry pays the junior-high and a baalut pays the
high school, she files a yearly teum mas or requests ichud maskorot. Had her two
fractions summed to more than a full position, the 100% benefit cap above would
apply.

## Gotchas

- **Re-adding seniority that is already in the cell.** The official (rank x
  seniority) cell IS the combined salary; it already includes vetek. Adding a
  seniority percentage on top double-counts it. Read the cell, then apply only
  gmulim.
- **Putting kindergartens under the wrong reform.** Kindergarten teachers
  (gananot) are under Ofek Chadash, together with elementary and junior-high.
  Oz LaTmura is upper-secondary only. A "kindergarten teacher under Oz" does not
  exist.
- **Ignoring who signs the slip.** Upper-secondary teachers are often employed by
  a baalut (ORT, Amal, AMIT, Branco Weiss) or a municipality, not by the ministry
  directly, which changes who issues the payslip and can change the pension
  arrangement.
- **Applying private-sector hourly logic.** A teacher's pay is a table cell (rank
  x seniority), not hours x hourly rate. Do not multiply frontal hours by a
  minimum-wage-style rate.
- **Confusing frontal hours with the full position.** "I teach 24 hours" may be a
  full Oz position (24 frontal) or a partial Ofek load. Frontal hours are only
  part of the paid week; private and stay/support hours count too. Always ask
  which reform and whether the number is frontal-only or the whole position.
- **Using a stale table.** Base-rate cells and the Oz hour split change with wage
  agreements (Oz moved from 40 to 38 hours in tashpe). Read the current union
  table or the ministry calculator; never freeze a NIS cell.
- **Forgetting gmulim.** Gmul hishtalmut, gmul chinuch, and role gmulim can add
  10% to 30%. Leaving them out understates gross badly. But respect the two-role
  gmul cap.
- **Assuming both reforms share a structure.** Ofek rewards through rank
  (dev hours, no classic gmulim); Oz banks one gmul a year with merit-point
  promotions. Different tables, different hour splits, different increment logic.
- **Forcing one reform on a teacher who teaches in both divisions.** A teacher in
  both a junior-high and a high school is under both reforms at once. Build the
  gross twice (one part per division, each by its own position fraction and its own
  reform's table and gmulim) and sum; do not blend them into one table. Reform is
  not employer: two separate payers (not the two reforms) are what create a yearly
  teum mas, which ichud maskorot removes. See Step 1b.

## Reference Links

| Resource | What it gives |
|----------|---------------|
| [Portal Ovdei Horaa: Ofek work-week](https://poh.education.gov.il/administrative/salary-agreements/new-ofek/work-week-ofek/) | Official Ofek Chadash hour structure |
| [Portal Ovdei Horaa: Oz reform](https://poh.education.gov.il/administrative/salary-agreements/oz-letmura/oz-litmura-reform/) | Official Oz LaTmura structure |
| [Salary-simulation calculator (Ministry of Education)](https://poh.education.gov.il/administrative/salary/salary-sheet/salary-simulation-calculator/) | Official gross estimate by rank/seniority/gmul |
| [Gmulei hishtalmut (Ministry of Education)](https://poh.education.gov.il/MerhavMinhali/HskalaVetek/Pages/GmuleiHishtalmut.aspx) | Professional-development gmul rules |
| [Histadrut HaMorim](https://www.itu.org.il/) | Union salary tables and gmulei tafkid |
| [Irgun HaMorim](https://www.igm.org.il/) | Upper-secondary teachers' union tables |
| [Position scope (Portal Ovdei Horaa)](https://poh.education.gov.il/administrative/transaction-details/position-scope/) | How position fraction is set and combined across divisions |

## Bundled Resources

- `references/reform-hour-structure.md` - Ofek vs Oz work-week comparison, all rows.
- `references/gmul-components.md` - every gmul type with its rate and basis.
- `references/domain-checklist.md` - the coverage contract for this skill.
- `scripts/teacher_gross.py` - applies gmulim to a combined-salary cell you
  supply (`--example` for a worked run). It never ships a NIS rank table and
  never re-adds seniority.
- `evidence.json` - every figure with its source and verbatim snippet.

## Troubleshooting

- **"I do not know the base rate."** The skill does not carry NIS rank cells on
  purpose (they change per agreement). Use the ministry salary-simulation
  calculator or the union table, then feed the rate into `teacher_gross.py`.
- **"The numbers do not match my payslip."** Check the year (Oz hour base changed
  in tashpe), the exact rank and recognized seniority (read the combined cell, do
  not re-add seniority), and whether every gmul is included and within the
  two-role cap. Remember the slip also carries fixed-shekel tosafot and havraa the
  script does not model, and deductions like union dues and the pension type
  (budgetary vs funded) shift the net. If gross still differs, the base cell may
  be from a newer agreement than the table you used.
- **"Is this net or gross?"** This skill computes GROSS. Net needs Step 4 and the
  `israeli-payroll-calculator` skill for the deduction mechanics.
- **The user actually needs bookkeeping or Bagrut help.** Route to
  `israeli-bookkeeping-automation` or `israeli-education-system`; this skill is
  only the teacher pay structure.
