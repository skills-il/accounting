---
name: israeli-teacher-payroll
description: "Computes and explains the salary of Israeli teachers (ovdei horaa / sachar ovdei horaa) under the two collective-agreement reforms: Ofek Chadash (ofek chadash, New Horizon, covering kindergartens, elementary, and junior-high) and Oz LaTmura (oz latmura, upper-secondary only). Use when a user asks how a teacher's pay is built: reform, rank (daraga), seniority (vetek), the weekly work-week split between front-of-class hours and private (pratani) hours, gmul (gmul) increments like gmul hishtalmut or gmul chinuch, and how gross becomes net. Also handles the split appointment, where one teacher teaches in both a junior-high and a high school and earns under both reforms at once, each part by its position fraction. Do NOT use for standard private-sector gross-to-net payroll (use israeli-payroll-calculator), bookkeeping journal entries (use israeli-bookkeeping-automation), or Bagrut and school-system navigation (use israeli-education-system)."
license: MIT
---

# Israeli Teacher Payroll

## Legal notice

This is a free information tool operated by an AI model. It explains the tax rules and helps you organise your own figures. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by a tax adviser or accountant. The output is not a tax opinion, not a return prepared by a licensed representative, and not professional advice, but a general calculation and explanation only: it does not examine the full extent of your income or your complete documents. An AI model may err, omit data, or present a wrong conclusion.

Any form or text this tool produces is an automatic draft for your personal preparation only, and is not a filed return. Responsibility for reporting and for paying the tax is yours, the binding computation is the Tax Authority's, and representation before the Tax Authority is reserved to those permitted by law. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person. Consult a tax adviser or accountant before filing or paying. All use of its output is the user's sole responsibility.


## Problem

Israeli teachers are not paid like private-sector employees. Their pay is set by
two collective-agreement reforms, Ofek Chadash and Oz LaTmura, each with its own
work-week structure, its own 9-rank salary table, and its own rules for
increments (gmulim). A generic gross-to-net calculator gets this wrong: it does
not know that a "full position" is a fixed weekly split of front-of-class hours,
private (small-group) hours, and stay/support hours; it does not know that rank
and seniority feed a collective-agreement table rather than an hourly rate; and
it forgets the gmulim, which stack into a double-digit uplift on the base. This skill encodes the
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

Kindergarten teachers (gananot) are under Ofek Chadash, not Oz: the Ofek reform
runs in kindergartens, elementary and middle schools, and Oz covers
upper-secondary only. If the user is unsure, ask which grades they teach. Never
carry a number from one reform's table to the other. A teacher who teaches in two
divisions at once is under both reforms at the same time: go to Step 1b.

Who signs the payslip is a separate question from the reform. Upper-secondary
teachers are often employed by a baalut (ORT, Amal, AMIT, Branco Weiss) or a
municipality rather than by the Ministry directly. The baalut issues the payslip
and can run a different pension arrangement even though the Oz salary structure
still applies. Ask who the employer of record is before reading a slip.

### Step 1b: The split appointment (a teacher under both reforms at once)

Step 1 pins ONE reform, but a teacher can teach across both divisions at the same
time and earn under BOTH reforms. The common case is a six-year school (chativa
shesh-shnatit): she teaches junior-high grades (7-9, Ofek Chadash, usually paid by
the Ministry of Education) and upper-secondary grades (10-12, Oz LaTmura, usually
paid by a baalut). A man can be in this position too; most teachers are women, so
the wording here is in the feminine. Do NOT pick one reform. Run the gross build
(Steps 2 to 3) TWICE, once per division, and add the two parts:

- Each division is its own position fraction (chelkiyut misra), for example 1/3
  in the junior-high plus 2/3 in the high school. Each fraction is relative to
  THAT reform's own full position (Ofek 36 hours, Oz 38 or 40), so combine them
  as fractions of a position, not as raw weekly hours.
- Each part uses its OWN reform: its own hour structure, its own combined
  (rank x seniority) cell, and its own gmulim, then scaled by that division's
  fraction. Read the recognized rank per reform from the official table; the two
  ranks follow each reform's own advancement rules and the ministry's
  cross-reform recognition, so do not assume they are identical and do not invent
  a conversion. Seniority is her own recognized teaching seniority, read into each
  reform's table.
- The two-gmul cap is per TEACHER, not per division: count role gmulim (gmulei
  tafkid) across the whole appointment, so a homeroom gmul in the junior-high plus a
  coordinator gmul in the high school is already the two-gmul maximum, not two per
  side.
- Total gross = Ofek part + Oz part. There is no blended table: the two parts stay
  separate and are summed. She keeps being paid under both reforms according to her
  position fraction in each division.

Two reforms is NOT the same as two employers. Who pays depends on the school's
operator, not on the reform: a six-year school run by one baalut or municipality
can pay BOTH parts on ONE payslip, and then there is one employer, one
withholding, and no tax coordination, even though she is under both reforms. The
two-employer case arises only when the two divisions are paid by different
payers. Confirm the actual payers; do not infer them from the reform.

Only when there are two payers: by default she gets two payslips, so she must file
a tax coordination (teum mas) every year or the second employer withholds at the
top rate, and each payer deposits her pension separately. Salary unification
(ichud maskorot) puts both parts on ONE payslip, removing the teum mas and
consolidating the deposits. The reported conditions are permanence (kviut) at the
paying employer plus at least a third position in the junior-high to unify through
the Ministry, or at least a half position in the high school to unify through the
baalut; these come from a teacher-finance publication rather than an official
page, so confirm with the payroll unit before electing, since the election is not
casually reversible. One caveat: when the two parts together exceed 100% of a
position, unification can lose benefits capped at 100%, such as havraa, bigud and
meonot.

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

Both reforms reduce the required hours by age, and missing this scores an older
teacher as under-working a full position. Oz: ages 50 to 55 a full position is 23
frontal and 36 in total, over 55 it is 21 frontal and 34 in total. Ofek: a serving
teacher from age 50 drops 2 frontal hours, and from 55 drops 4 hours (3 frontal
plus 1 private); a newly hired teacher from 50 drops 2. Both are for high position
fractions and scale down proportionally below that.

Private hours mean teaching one student or a small group (Ofek: up to 5; Oz: up
to 3, or up to 5 by pedagogical decision). If a teacher works less than a full
position, scale by the position fraction.

### Step 3: Build the gross

1. Read the combined salary directly from the official table. The union salary
   tables and the ministry salary-simulation calculator are two-dimensional
   grids of rank (daraga) by seniority (vetek). The cell you read for a given
   (rank, seniority) pair IS the "combined salary" (sachar meshulav): it ALREADY
   includes seniority. Do NOT add a seniority percentage on top of it, or you
   double-count. The 2% per year up to year 6 (inclusive) and 1% per year from year 7 to
   year 36 is the rule the table already applied to produce that cell; it is not
   something you re-add.
2. Rank and seniority advancement take effect with the school year, on 1
   September, and are read into the table from that date. Rank 1 is a new
   teacher. Ofek Chadash promotion turns on three criteria together: paznun (the
   required months in rank), shapam (professional-development hours), and an
   evaluation. Ranks 2 and 3 need 30 months and 120 hours; ranks 4, 5 and 6 need
   36 months and 180 hours; ranks 7, 8 and 9 need 48 months and 210 hours.
   **Promotion quotas for ranks 7 to 9 were abolished in the 2016 agreement**, so
   do not tell a teacher a quota is blocking them. This is Ofek-specific: Oz
   LaTmura advances on merit points, so do not apply the Ofek rule to an Oz
   teacher.
3. Apply gmulim as a percentage of the combined salary you read in step 1.
   **The two reforms publish separate role-gmul tables with genuinely different
   rates**, and the table below mixes both, so check the reform label on the row
   before applying it. Full per-reform tables are in
   `references/gmul-components.md`. Cap:
   at most two role gmulim (gmulei tafkid) per teacher. A principal cannot draw a
   role gmul at all; a first deputy may only be a homeroom teacher; and for a
   second deputy or above the deputy gmul itself consumes one of the two slots.

| Gmul | Rate |
|------|------|
| Gmul hishtalmut (Oz; Ofek banks dev hours instead) | 1.2% per 112-hour unit; per-unit rate rose to 1.3% from 1.9.2025. The Oz quota is 19 units (raised from 18 in tashaf), at most one banked per year |
| Gmul chinuch (homeroom) | Both reforms: 10% OR 1,000 NIS, whichever is higher; 11.5% (same floor) for a grade-1 homeroom or a chativa-tzeira kindergarten teacher |
| Gmul rikuz miktzoa (subject coordinator) | Oz: 8%, or 9% for mathematics and English, from 1.9.2025. Ofek: 6% elementary, 8% junior-high |
| Gmul pituach miktzoi (professional-development role) | 6% |
| Gmul nihul gan (Ofek, kindergarten management) | 17% up to 5 years of management seniority, 20% for 6 to 10, 21% above 10, and in every band a floor of 1,500 NIS, whichever is higher |
| Gmul yeutz (educational counsellor) | Both reforms: 12% on a temporary licence, 18% on a permanent one. Keyed to the licence, not to counselling seniority |
| Gmul chinuch meyuchad (special education) | Oz 10 / 15 / 17 percent; Ofek 8.5 / 15 / 17. The top band is autism or severe-psychiatric settings |

**Oz LaTmura shekel supplement (tosefet shiklit).** The Irgun HaMorim agreement
of 23.9.2024, whose execution directive took effect 1.9.2025, raised the Oz
shekel supplement from 1,200 NIS to 1,518 NIS. Later steps may have been agreed
for subsequent school years, so read the current amount from the execution
circular rather than assuming 1,518 NIS still holds. This is an Oz LaTmura
line: do not apply it to an Ofek Chadash teacher.

The same agreement also changed the Oz coordinator (rakaz) gmulim: tikshuv and
pedagogi rose to 8%, chinuch chevrati to 10%, rakaz shichva became 6% or 1,100
NIS whichever is higher, and the remaining rakaz roles sit at 6%. **The reforms
publish DIFFERENT role-gmul tables and the rates genuinely differ** (special
education is 8.5 / 15 / 17 percent under Ofek against 10 / 15 / 17 under Oz;
rakaz miktzoa is 6% in an Ofek elementary school against 8% in a junior-high and
8 or 9 percent under Oz). Both full tables, and both are page text on live union
and ministry pages, are in `references/gmul-components.md`. Read the right
reform's table.

**A 10,000 NIS retention grant (manak shimur) is paid in the September 2026
salary** to an Ofek teacher whose employment began on 1.9.2023. It is a one-off,
not a salary component, so do not fold it into a monthly gross. Whether it is
pensionable, whether it prorates by position, and whether it can be spread for
tax (perisa) are not stated in the union announcement, so do not assert any of
the three: a large one-month spike taxed at the marginal rate is the expected
appearance, and the payroll unit is the place to confirm the rest.

**A new Ofek Chadash gmul starts with school year tashpaz.** Gmul yozma chinuchit
beit-sifrit takes effect 1.9.2026 for Ofek teachers and for deputy principals the
principal appoints. Each approved initiative carries 2 to 5 units at the
principal's discretion, each unit 200 NIS a month, so the gmul runs 400 to 1,000
NIS a month. It is a fixed-shekel line, NOT a percentage of the combined salary,
so never feed it to the script as a gmul percentage. It is re-decided each year.
This is the gmul the 2022 agreement scheduled for 1.9.2025 and then deferred, so
the union's standing terms page still dates it September 2025 while its actual
entry into force, announced 16.8.2026, is 1.9.2026. It is correctly absent from a
2025 slip. Treat 1.9.2026 as the operative date and the 2-unit minimum as
binding: a single 200 NIS unit is not payable. The shiluv/pitzul cost-frame
stays frozen and un-freezes 1.1.2027.

More gmulim exist beyond this list, including a deputy-principal gmul and roles
scoped to a single school level. English, mathematics and physics have their own
subject incentive arrangements, but that does NOT remove the coordinator gmul
from their coordinators: under Oz a maths or English rakaz miktzoa draws 9%. Read
the current rate from `references/gmul-components.md`, do not invent one.

Reform difference: Ofek Chadash teachers do NOT bank hishtalmut or merit gmulim
(dev hours push the rank instead) BUT role gmulim (for example gmul chinuch for a
homeroom, or gmul nihul gan) still apply to them. Oz teachers bank at most one
gmul a year (sabbatical and unpaid leave excepted), and rank advances on merit
points (nekudot zechut) accrued from roles, at rates we could not confirm on a
live official page: read the ministry's nekudot zechut page, do not assume a
fixed points-to-percent conversion. See `references/gmul-components.md`.

Use `scripts/teacher_gross.py` to apply gmulim to the combined-salary cell once
you have read it. It takes the combined cell as its base and does not re-add
seniority. Three rules it now enforces, each of which is easy to get wrong:

- **Role gmulim are computed on a FULL position and are not prorated by the
  position fraction.** Only the combined salary is scaled. The two exceptions are
  the special-education and inclusion gmulim, computed on the share of frontal
  hours taught in that setting: pass `--scale-gmulim` for those and only those.
- **A shekel floor is a higher-of test, not an add-on.** Pass it with
  `--gmul-floor 1000` for gmul chinuch or `--gmul-floor 1100` for Oz rakaz
  shichva. Whether the floor itself prorates at part-time, and whether the
  higher-of test runs before or after the fraction, is not stated by any source
  we could reach; the script tests on the full position and says so. Reconcile
  against the slip.
- **Flat shekel lines go in `--fixed`, never in `--gmul`.** That covers the Oz
  tosefet shiklit and the gmul yozma chinuchit.

This gross model is an approximation, not a full payslip. It cannot express lines
that do not derive from the combined cell: travel reimbursement, menak yovel,
havraa, bigud, and tosafot that do not scale with rank. Reconcile against the
slip.

### Step 4: Gross to net

Teacher net follows the standard statutory deductions. For the full mechanics
(brackets, credit points, ceilings) defer to the `israeli-payroll-calculator`
skill; do not restate income-tax brackets here. The pieces:

- Income tax (mas hachnasa): progressive brackets, less credit points.
- National insurance (bituach leumi), employee share: reduced rate 1.04% (raised
  from 0.40%), full rate 7.00% above the reduced step of 7,703 NIS.
- Health tax (mas briut): 3.23% up to that same 7,703 NIS step, 5.17% above, so
  the employee pays 4.27% and then 12.17% in total. Deductions stop at the
  maximum insured income of 51,910 NIS.
- **Those figures are only the form-102 column-1 row, an able-bodied resident
  aged 18 to retirement age, and a teacher is often not on it.** The employee
  side is categorical: a teacher drawing an old-age pension who keeps teaching
  pays NOTHING (the 0.61% / 2.12% on that row is the employer's share alone), a
  teacher aged 67 to 70 NOT drawing one pays 3.93% / 10.03%, and a
  disability-pension holder with an annual BL certificate pays 3.23% / 5.17%.
  Read the category before you read a rate. Full table in
  `israeli-payroll-calculator`.
- Pension: the deduction is computed on the defined pensionable salary (the
  mashkoret koveat / first-tier pensionable pay), NOT on gross, and the teacher
  arrangements are their own, so read the rate and the base off the slip rather
  than applying the private-sector 6% extension order. Check the pension TYPE
  too, because it changes the employee deduction and the net. Veteran teachers (typically hired before 2000-2004) may be on pensia
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
war-cost participation deduction, and a slip read without it overstates net pay.
Union representation is not an exemption. The rate differs by reform and by
period: 2.290% December 2024 to March 2025, 3.307% in April 2025, then 0.95% from
1.5.2025 to 31.12.2025 for Ofek Chadash ONLY (Oz stays on the law rate of 3.307%,
no mitigating agreement exists), and 1.2% for all of 2026 under both reforms.
What applies from 1.1.2027, mid-tashpaz, is unsettled: read the circular. On a
teacher slip the line is NOT called "tikun pensioni" but sits under the symbol
`חוק הת. כלכלית אופק`, it is scaled by an absence coefficient, and it does not
reduce pension, the mashkoret koveat, gmulim or grants. A separate
seniority-advancement reduction ran September to December 2025 only, banded by
seniority, and does not apply to teaching staff employed by local authorities.
Full tables, bands, and the December 2025 anomaly are in
`references/wage-reduction.md`.

**The 2023 public-sector framework agreement does NOT apply to teachers.** Its
shekel supplement and its 2% / 3.5% / 5% / 6% tranches are scoped to dirugim
represented by the general Histadrut, and teacher dirugim are represented by
Histadrut HaMorim and Irgun HaMorim instead. Teachers reading press coverage of
the April 2026 5% tranche will expect it and should be told plainly that their
raises come from their own agreements. The framework's own "teaching employees"
clause exists only to stop double-counting for non-teachers whose pay is pegged
to the teacher scale.

Additions on the gross side (not deductions): teacher pay is spread across all
twelve months, so July and August are paid even though school is on summer break.

**Havraa (recreation pay): teachers are on the PUBLIC-sector rate, not the
private one.** Per the Commissioner on Wages circular of 8.6.2026, the public day
rate is 511.60 NIS from 1.6.2026, up from 471.40 NIS. The 451.50 NIS agreed for
the private sector on 22.6.2026 does not bind teachers, and using it understates
every havraa day. Days are set by teaching seniority for a full position (7
days in the first 3 years rising in steps to 13 from 25 years; the full table is
in `references/reform-hour-structure.md`), proportional for part-time.

The annual clothing allowance (bigud) is 2,527 NIS for a full position at
seniority level 4 in 2026. The 91 NIS cut and the de-indexation that produced
2,314 NIS in 2025 (from 2,405 NIS in 2024) were a one-time measure for that year
only, so do not carry them forward.

Context: minimum wage is 6,443.85 NIS/month since 1.4.2026 (it was 6,247.67 NIS
from 1.4.2025); the hourly rate on the 182-hour basis is 35.40 NIS. The average
wage is 13,769 NIS (Jan 2026). Teacher base pay comes from
the agreement table, not from these figures.

## Examples

### Example 1: Ofek Chadash elementary homeroom teacher

Teacher in an elementary school, rank 4, 5 years seniority, homeroom of a grade-3
class, full position. Reform is Ofek Chadash, so the position is 36 hours (26
frontal + 5 private + 5 stay). Build gross: read the combined-salary cell for
rank 4 at 5 years seniority straight from the official grid, that cell already
includes the seniority, so do NOT re-add it. Then apply only the 10% gmul chinuch
on top, subject to its 1,000 NIS floor. This teacher is under Ofek, and Ofek
teachers do not bank hishtalmut gmulim, but the homeroom role gmul still applies.
Run: `python3 scripts/teacher_gross.py --base <rank4_year5_cell> --gmul 10
--gmul-floor 1000 --position 1.0`. Then apply Step 4 for net.

### Example 2: Oz LaTmura upper-secondary teacher with development gmul

Teacher in a high school, rank 6, 12 years seniority, subject coordinator (not
English or math), holds 8 units of gmul hishtalmut, full position. Reform is Oz
LaTmura, position 38 hours from tashpe (25 frontal + 3 private + 10 support).
Gross: read the rank-6 at 12-years-seniority cell (it already includes the
seniority), then apply gmulim = 8% coordinator + (8 units x 1.3% =) 10.4%
development. Coordinator plus development is within the two-role cap. This teacher
advances rank on merit points, not on Ofek dev-hour quotas. The Oz tosefet shiklit
is a shekel line, so it goes in `--fixed`, never in `--gmul`. Run:
`python3 scripts/teacher_gross.py --base <rank6_year12_cell> --gmul 8 --gmul 10.4
--fixed 1518 --position 1.0`.

### Example 3: Kindergarten manager under Ofek Chadash, half position

Kindergarten manager (gananet menahelet) under Ofek Chadash (kindergartens are an
Ofek reform, not Oz), rank 3, 3 years of management seniority, gmul nihul gan
(17% for up to 5 years of management seniority, or its 1,500 NIS floor if that is
higher), half position. Gross: read the rank-3 combined-salary cell (already
includes seniority), scale THAT by 0.5, and add the 17% gmul computed on the
FULL-position cell WITHOUT scaling it, because
role gmulim are not prorated by chelkiyut misra. Run:
`python3 scripts/teacher_gross.py --base <rank3_cell> --gmul 17 --gmul-floor 1500
--position 0.5`.
So it is half the cell PLUS the whole gmul, not half of both, which is a
materially larger figure on any part-time slip. The management
gmul is one role gmul, leaving room for at most one more. The two exceptions,
special-education and inclusion gmulim, DO scale and need `--scale-gmulim`.
Reconcile against the actual slip.

### Example 4: Teacher split across both reforms in a six-year school

A teacher in a six-year school teaches a third position (1/3) in the junior-high
grades (Ofek Chadash, paid by the Ministry) and two-thirds (2/3) in the
upper-secondary grades (Oz LaTmura, paid by an ORT baalut). She is under both
reforms at once, so build gross TWICE and sum. Ofek part: read her Ofek combined
cell for her rank and seniority, apply her Ofek role gmulim (say 10% gmul chinuch
for a junior-high homeroom), scale by 1/3. Oz part: read her Oz combined cell for
her Oz rank and the same recognized seniority, apply her Oz gmulim, scale by 2/3.
Total gross = Ofek part + Oz part. Run the script once per division and add:
`python3 scripts/teacher_gross.py --base <ofek_cell> --gmul 10 --gmul-floor 1000
--position 0.333` then `python3 scripts/teacher_gross.py --base <oz_cell> --gmul 8
--position 0.667`. Each division's role gmul is computed on that reform's
full-position cell and is not prorated.
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
- **Confusing frontal hours with the full position.** "I teach 25 hours" may be a
  full Oz position (25 frontal since tashpe) or a partial Ofek load. Frontal hours are only
  part of the paid week; private and stay/support hours count too. Always ask
  which reform and whether the number is frontal-only or the whole position.
- **Using a stale table.** Base-rate cells and the Oz hour split change with wage
  agreements (Oz moved from 40 to 38 hours in tashpe). Read the current union
  table or the ministry calculator; never freeze a NIS cell.
- **Forgetting gmulim.** Gmul hishtalmut, gmul chinuch, and role gmulim stack
  into a double-digit uplift. Leaving them out understates gross badly. But respect the two-role
  gmul cap.
- **Paying a teacher the private-sector havraa rate.** Teachers are public
  sector. Reaching for the private day rate, or for a private-sector payroll
  skill's figure, understates every havraa payment.
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

- `references/reform-hour-structure.md` - Ofek vs Oz work-week comparison, all
  rows, the age and mother-teacher reductions, the position ceiling, and the
  havraa-days table.
- `references/gmul-components.md` - the Ofek and Oz role-gmul tables in full.
- `references/wage-reduction.md` - the temporary wage reduction and the
  seniority-advancement reduction, with every band.
- `references/domain-checklist.md` - the coverage contract for this skill.
- `scripts/teacher_gross.py` - applies gmulim to a combined-salary cell you
  supply. Flags: `--base`, `--gmul` (repeatable), `--gmul-floor` (shekel
  higher-of test), `--fixed` (flat shekel lines, repeatable), `--position`,
  `--scale-gmulim` (special-education and inclusion gmulim only),
  `--illustrative-seniority`, `--example`. It never ships a NIS rank table and
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
