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
work-week structure, its own salary table, and its own rules for
increments (gmulim). A generic gross-to-net calculator misses that a "full
position" is a fixed weekly split of front-of-class, private and stay hours, that
rank and seniority feed an agreement table rather than an hourly rate, and that
gmulim stack into a double-digit uplift. This skill encodes the
Israel-specific structure so an agent can explain a teacher's payslip, estimate a
gross salary from the right table, and route the deduction step correctly.

## Instructions

Work in four steps. Steps 1 to 3 build the GROSS; step 4 turns gross into net.

### Step 1: Identify the reform and school level

The reform decides everything downstream, so pin it first.

| Reform | Who | The salary cell is read by |
|--------|-----|-------|
| Ofek Chadash | Kindergarten (gan), elementary (yesodi), and junior-high (chativat beynayim) teachers | Education grade x rank (1-9) x seniority |
| Oz LaTmura | Upper-secondary (chativa elyona / high school) teachers | Education grade x seniority, plus up to 4 promotion grades of 1.67% each. The 9 ranks are an Ofek structure; do not apply them to Oz |

The education grade (darga hashkala: musmach, musmach bachir, BA, MA, doctorate)
is set by the teacher's approved degree under both reforms, so a BA cell for an MA
teacher is wrong, and an approved degree moves the cell. Ask for it.

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
  cell, and its own gmulim, then scaled by that division's
  fraction. The Ofek part is read by her degree, Ofek rank and seniority; the
  Oz part by her degree and seniority, plus any promotion grades. Do not invent a
  rank conversion between them.
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
consolidating the deposits. Per the Ministry's salary-consolidation page it needs
kviut at the unifying employer plus at least a third position in the junior-high
(Ministry route) or a half in the high school (baalut route); the full conditions
and exclusions are in `references/reform-hour-structure.md`. Above 100% in total,
unification can lose benefits capped at 100% (havraa, bigud, meonot).

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

1. Read the combined salary directly from the official table or the ministry
   salary-simulation calculator, for her education grade, (Ofek) rank, and
   seniority (vetek). That cell IS the "combined salary" (sachar meshulav): it
   ALREADY includes seniority. Do NOT add a seniority percentage on top of it, or you
   double-count. The 2% per year up to year 6 (inclusive) and 1% per year from year 7 to
   year 36 is the rule the table already applied to produce that cell; it is not
   something you re-add.
2. Rank and seniority advancement take effect on 1 September. Ofek promotion
   needs paznun (months in rank), shapam (development hours) and an evaluation
   together, at 30/120, 36/180 and 48/210 for ranks 2-3, 4-6 and 7-9, and **the
   rank 7-9 quotas were abolished in 2016**, so no quota blocks her. Oz advances
   by promotion grades instead (below).
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
| Gmul hishtalmut (Oz; Ofek banks dev hours instead) | 1.2% per 112-hour unit; per-unit rate rose to 1.3% from 1.9.2025. The Oz quota is 19 units (raised from 18 in tashaf), at most one banked per year. A study gmul, not a role gmul: prorated by position |
| Gmul chinuch (homeroom) | Both reforms: 10% OR 1,000 NIS, whichever is higher; 11.5% (same floor) for a grade-1 homeroom or a chativa-tzeira kindergarten teacher |
| Gmul rikuz miktzoa (subject coordinator) | Oz: 8%, or 9% for mathematics and English, from 1.9.2025. Ofek: 6% elementary, 8% junior-high |
| Gmul nihul gan (Ofek, kindergarten management) | 17%, 20% or 21%, each with a 1,500 NIS floor, higher of. An existing gananet is banded by management years (up to 5, 6 to 10, above 10); a new gananet by Ofek rank (1-2, 3-4, 5-9) |
| Gmul yeutz (educational counsellor) | Both reforms: 12% on a temporary licence, 18% on a permanent one. Keyed to the licence, not to counselling seniority |
| Gmul chinuch meyuchad (special education) | Oz 10 / 15 / 17 percent; Ofek 8.5 / 15 / 17. The top band is autism or severe-psychiatric settings |

**Oz LaTmura shekel supplement (tosefet shiklit Oz 2023).** Under the Irgun
HaMorim agreement of 23.9.2024 it is 1,790.50 NIS for a full position from
1.9.2026 (it was 1,518 NIS from 1.9.2025 and 1,200 NIS before that). The signed
table schedules 2,066.75 NIS from 1.9.2027; check the execution circular before
using that figure. It is **prorated by the position fraction, including above
100%**, so pass it with `--fixed-prorated`, never `--fixed`. It counts for pension
and keren hishtalmut deposits but is not a base for any other supplement. An Oz
slip may also carry a separate, older "tosefet shiklit 2016" line; do not confuse
the two. This is an Oz LaTmura line: do not apply it to an Ofek Chadash teacher.

**Ofek Chadash shekel supplement (tosefet Ofek 2022).** Nearly every Ofek slip
carries it (the published table runs to rank step 8.5). It depends on the education grade and the rank step and falls as rank rises:
as updated from 1.9.2023 it was 1,585.54 NIS at rank 1 for a BA and 1,664.87 NIS
for an MA, shrinking to under 20 NIS at the top. For a new teacher it is the
largest line after the base, so leaving it out makes a junior slip look about
1,500 NIS too high. Read the current amount from the slip; how it treats part
time is not published, so check whether it scales.

**New Oz LaTmura gmul from tashpaz: gmul tafkid beit-sifri.** For a school role
the principal assigns, 2 to 5 units of 200 NIS a month (400 to 1,000 NIS). It is
paid at its FULL shekel value from a third of a position upward, and stays at the
full-position amount above 100%, so it goes in `--fixed`. The circular does not
say what a teacher below a third of a position gets, so do not assert it. It counts inside the two-role-gmul cap, principals and deputies cannot
draw it, it is not part of the combined salary, and no keren hishtalmut deposit is
made on it (it does count for pension deposits and severance).

The same agreement also changed the Oz coordinator (rakaz) gmulim: tikshuv and
pedagogi rose to 8%, chinuch chevrati to 10%, rakaz shichva became 6% or 1,100
NIS whichever is higher, and the remaining rakaz roles sit at 6%. **The reforms
publish DIFFERENT role-gmul tables and the rates genuinely differ** (special
education is 8.5 / 15 / 17 percent under Ofek against 10 / 15 / 17 under Oz;
rakaz miktzoa is 6% in an Ofek elementary school against 8% in a junior-high and
8 or 9 percent under Oz). Both full tables, and both are page text on live union
and ministry pages, are in `references/gmul-components.md`. Read the right
reform's table.

**A 10,000 NIS retention grant (manak shimur)** goes to every new Ofek teacher
who started work on or after 1.9.2023, not only that one cohort. The same
agreement lengthened their probation to three years, which is why the first
grants fall due only now. The 2022 agreement conditions it on reaching kviut
with a position of 70% or more, and a teacher below a full position gets it in
proportion to her weighted position over the preceding 36 months. The union page
gives the September 2026 salary for the first cohort, the agreement says the May
after kviut, so confirm the month with the payroll unit. It is a one-off, not a monthly gross component.
Its pension and tax treatment (including perisa) are not published, so do not
assert them; a one-month spike taxed at the marginal rate is the expected look.

**A new Ofek Chadash gmul from tashpaz: gmul yozma chinuchit beit-sifrit**, in
force 1.9.2026 for Ofek teachers and appointed deputy principals. Each approved
initiative carries 2 to 5 units at the principal's discretion, 200 NIS a unit, so
400 to 1,000 NIS a month, re-decided each year. It is a fixed-shekel line, never
a gmul percentage, and is correctly absent from a 2025 slip. Its part-time rule is
not published, so `--fixed` (full value) is an assumption to check on the slip.

More gmulim exist beyond this list, including a deputy-principal gmul and roles
scoped to a single school level. English, mathematics and physics have their own
subject incentive arrangements, but that does NOT remove the coordinator gmul
from their coordinators: under Oz a maths or English rakaz miktzoa draws 9%. Read
the current rate from `references/gmul-components.md`, do not invent one.

Reform difference: Ofek Chadash teachers do NOT bank hishtalmut or merit gmulim
(dev hours push the rank instead) BUT role gmulim (for example gmul chinuch for a
homeroom, or gmul nihul gan) still apply to them. Oz teachers bank at most one
gmul a year (sabbatical and unpaid leave excepted), and advance by promotion
grades earned with merit points (nekudot zechut) from roles: per the ministry's Oz page, every 10
points is a promotion grade of 1.67% of the combined salary, at most 4 grades
(6.69% cumulative), at least 3 years apart, and points accrue for one role only.
Pass the grades she holds as one percentage (2 grades: 3.34). Whether they scale
at part time is not published; they ride on the combined salary, so
`--gmul-scaled` is the assumption to check on the slip.
See `references/gmul-components.md`.

Use `scripts/teacher_gross.py` to apply gmulim to the combined-salary cell once
you have read it. It takes the full-position combined cell as its base and does
not re-add seniority. The rules it enforces, each easy to get wrong:

- **Role gmulim are computed on a FULL position and are not prorated by the
  position fraction** (`--gmul`). The Histadrut HaMorim page states this for Ofek;
  no Oz text we reached states it either way, so check an Oz slip. The exceptions
  are the special-education and inclusion gmulim, computed on the share of her
  frontal hours taught in that setting: `--gmul-share 15@13/26`.
- **Study gmulim scale with the position.** The terms of service pay gmul
  hishtalmut in proportion to the position at each employer, above 100% too, so it
  goes in `--gmul-scaled`. It is not a role gmul and does not count toward the
  two-role cap.
- **A shekel floor is a higher-of test on ONE gmul**, never on a sum: `--gmul
  10:1000` gmul chinuch, `--gmul 6:1100` Oz rakaz shichva, `--gmul 17:1500` gmul
  nihul gan. Whether a floor itself prorates at part time is not stated anywhere
  we reached; the script tests it on the full position.
- **Flat shekel lines split two ways.** The Oz tosefet shiklit is prorated by
  position (`--fixed-prorated`); the Oz gmul tafkid beit-sifri is paid in full
  (`--fixed`).
- Under Oz, the 6% rakaz gmulim (miyumanuyot and the roles added under section
  17(א)) are computed on the combined salary PLUS the Oz reform supplement
  (tosefet Oz LaTmura). The script has one base, so compute that gmul by hand as
  6% of the sum and pass the result with `--fixed`.

The script rejects empty values, placeholders, ambiguous separators (12.000,
10,1000), NaN, and repeated `--base`; run it once per division.

This gross model is an approximation, not a full payslip. It cannot express lines
that do not derive from the combined cell: travel reimbursement, menak yovel,
havraa, bigud, and tosafot that do not scale with rank. Reconcile against the
slip.

### Step 4: Gross to net

Teacher net follows the standard statutory deductions. For the full mechanics
(brackets, credit points, ceilings) defer to the `israeli-payroll-calculator`
skill; do not restate income-tax brackets here. The pieces:

- Income tax (mas hachnasa): progressive brackets, less credit points.
- National insurance (bituach leumi), employee share: reduced rate 1.04%, full rate 7% above the reduced step of 7,703 NIS.
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
  too, because it changes the employee deduction and the net. State-employed
  teachers with kviut hired before 1.9.2002 are on pensia taktzivit (budgetary
  pension); its employee deduction is not published on the Ministry page, so read
  it off the slip. Others are on pensia tzoveret (funded), where the Ministry page
  (stated as of 1.6.2018) lists employer 7.5% plus 6.224% severance and employee 6% or 7% (her choice) on
  the pensionable salary. Separate layers also take deposits on expense
  reimbursements such as travel and on work above 100%, so a slip shows more than
  one pension line; see `references/reform-hour-structure.md`. A baalut may differ.
- Keren Hishtalmut: in a dedicated teacher study fund the teacher pays 4.2% and
  the employer 8.4%, and these funds carry the sabbatical right; in a
  non-dedicated fund it is 2.5% and 7.5%. Not the private-sector default.
- Union dues: essentially every teacher slip carries a union deduction, demei
  chaver (member dues) or demei tipul (handling dues), to Histadrut HaMorim
  (Ofek / kindergartens and elementary and middle school) or to Irgun HaMorim
  (upper-secondary). Do not omit it. Read the current amount from the union;
  do not invent a rate.

**The temporary wage reduction (2025 and 2026).** Teachers ARE covered by the
war-cost participation deduction; a slip read without it overstates net pay. In
2026 it is 1.2% under both reforms. In 2025 the rates differed by reform (Ofek
0.95% from 1.5.2025, Oz the law rate of 3.307%). What applies from 1.1.2027 is
not published: read the circular. On a teacher slip the line is NOT "tikun
pensioni" but `חוק הת. כלכלית אופק`; it does not reduce pension, the mashkoret
koveat, gmulim or grants. Every period, band and the September to December 2025
seniority reduction are in `references/wage-reduction.md`.

**The 2023 public-sector framework agreement does NOT apply to teachers.** Its
shekel supplement and its 2% / 3.5% / 5% / 6% tranches are scoped to dirugim
represented by the general Histadrut; teacher dirugim are represented by
Histadrut HaMorim and Irgun HaMorim. A teacher expecting the April 2026 5% tranche
should be told plainly that teacher raises come from teacher agreements. The
newest is the Irgun HaMorim agreement of 31.8.2026 (in force to 31.8.2029); its
pay items are in `references/gmul-components.md`.

July and August are paid as holiday pay in proportion to the months actually
worked that year, and no pay component changes in those two months, so a
mid-year hire sees a smaller summer slip.

**Havraa, bigud and the baselines.** Teachers get the PUBLIC-sector havraa day
rate, 511.60 NIS from 1.6.2026, not the private 451.50 NIS; days follow teaching
seniority, proportional for part-time. Bigud is 2,527 NIS for a full position in
2026. Minimum wage is 6,443.85 NIS a month from 1.4.2026; average wage 13,769 NIS
(Jan 2026). Teacher base pay comes from the agreement table, not these figures.
The day table and the one-time 2025 bigud cut are in
`references/reform-hour-structure.md`.

## Examples

### Example 1: Ofek Chadash elementary homeroom teacher

Teacher in an elementary school, rank 4, 5 years seniority, homeroom of a grade-3
class, full position. Reform is Ofek Chadash, so the position is 36 hours (26
frontal + 5 private + 5 stay). Build gross: read the combined-salary cell for
rank 4 at 5 years seniority straight from the official grid, that cell already
includes the seniority, so do NOT re-add it. Then apply only the 10% gmul chinuch
on top, subject to its 1,000 NIS floor. This teacher is under Ofek, and Ofek
teachers do not bank hishtalmut gmulim, but the homeroom role gmul still applies.
Run: `python3 scripts/teacher_gross.py --base RANK4_YEAR5_CELL --gmul 10:1000
--position 1.0`, replacing the placeholder with her real cell for her degree. Then apply Step 4 for net.

### Example 2: Oz LaTmura upper-secondary teacher, three-quarter position

High-school teacher with an MA, 12 years of seniority, one promotion grade,
subject coordinator (not English or maths), 8 units of gmul hishtalmut, 0.75 of a
position. Reform is Oz LaTmura (38 hours from tashpe: 25 frontal + 3 private + 10
support). Read the Oz cell for an MA at 12 years (it already includes seniority);
no Ofek rank applies. Role gmul: 8% coordinator, kept whole under the
full-position rule (check an Oz slip). Scaled: 10.4% hishtalmut (8 x 1.3%) plus
1.67% for the grade (assumed to scale). Shekel: the tosefet shiklit, prorated. Run:
`python3 scripts/teacher_gross.py --base OZ_MA_YEAR12_CELL --gmul 8 --gmul-scaled
12.07 --fixed-prorated 1790.50 --position 0.75`.

### Example 3: Kindergarten manager under Ofek Chadash, half position

Kindergarten manager (gananet menahelet) under Ofek Chadash, an existing gananet
(banded by management years), BA, rank 3, 3 years of management, half position.
Read her rank-3 BA cell, scale it by 0.5, and add the 17% gmul nihul gan (floor
1,500 NIS; a NEW gananet at rank 3 would draw 20%) computed on the FULL-position
cell without scaling, because role gmulim are not prorated. Run:
`python3 scripts/teacher_gross.py --base RANK3_BA_CELL --gmul 17:1500
--position 0.5`. Half the cell PLUS the whole gmul, not half of both. Add her
tosefet Ofek 2022 line from the slip. The management gmul leaves room for at most
one more role gmul.

### Example 4: Teacher split across both reforms in a six-year school

A teacher in a six-year school teaches 1/3 in the junior-high (Ofek Chadash, paid
by the Ministry) and 2/3 in the upper-secondary grades (Oz LaTmura, paid by an ORT
baalut). Build gross TWICE and sum. Ofek part: her Ofek cell (degree, rank,
seniority) with a 10% homeroom gmul. Oz part: her Oz cell (degree, seniority) with
an 8% coordinator gmul and the prorated tosefet shiklit. Run once per division:
`python3 scripts/teacher_gross.py --base OFEK_CELL --gmul 10:1000 --position 1/3`
then `python3 scripts/teacher_gross.py --base OZ_CELL --gmul 8 --fixed-prorated
1790.50 --position 2/3`, and add. Her two role gmulim are already the two-gmul
maximum across the whole appointment. One baalut paying both divisions means one
payslip and no teum mas; the Ministry plus a baalut means a yearly teum mas or
ichud maskorot. Above 100% in total, the 100% benefit cap applies.

## Gotchas

- **Re-adding seniority that is already in the cell.** The official cell IS
  the combined salary; it already includes vetek. Adding a
  seniority percentage on top double-counts it. Read the cell, then apply only
  gmulim.
- **Putting kindergartens under the wrong reform.** Kindergarten teachers
  (gananot) are under Ofek Chadash, together with elementary and junior-high.
  Oz LaTmura is upper-secondary only. A "kindergarten teacher under Oz" does not
  exist.
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
- **Forcing one reform on a teacher who teaches in both divisions.** A teacher in
  both a junior-high and a high school is under both reforms at once: build the
  gross once per division and sum. Two payers, not two reforms, create a yearly
  teum mas. See Step 1b.

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
  supply. Flags: `--base`, `--gmul PCT[:FLOOR]` (repeatable, role gmul, not
  prorated), `--gmul-share PCT@SHARE` (special-education and inclusion, by
  frontal-hour share), `--gmul-scaled` (hishtalmut and promotion grades),
  `--fixed` (flat shekel line in full), `--fixed-prorated` (flat shekel line by
  position), `--position`, legacy `--gmul-floor` and `--scale-gmulim`,
  `--illustrative-seniority`, `--example`. It never ships a NIS rank table and
  never re-adds seniority.
- `evidence.json` - every figure with its source and verbatim snippet.

## Troubleshooting

- **"I do not know the base rate."** The skill does not carry NIS rank cells on
  purpose. Use the ministry salary-simulation calculator; the union PDF tables
  were last dated September 2022. Feed the cell into `teacher_gross.py`.
- **"The numbers do not match my payslip."** Check the year (Oz hour base changed
  in tashpe), the exact rank and recognized seniority (read the combined cell, do
  not re-add seniority), and whether every gmul is included and within the
  two-role cap. Remember the slip also carries fixed-shekel tosafot and havraa the
  script does not model, and deductions like union dues and the pension type
  (budgetary vs funded) shift the net. One-month spikes are usually retroactive
  differences (hefreshim), for example a gmul recognised retroactively, or, for a teacher
  who gave birth that year, retroactive pension, provident and keren deductions
  taken in July. Bigud is paid in the July salary and the yom chinuch aroch grant
  in May and June.
- **"Is this net or gross?"** This skill computes GROSS. Net needs Step 4 and the
  `israeli-payroll-calculator` skill for the deduction mechanics.
- **The user actually needs bookkeeping or Bagrut help.** Route to
  `israeli-bookkeeping-automation` or `israeli-education-system`; this skill is
  only the teacher pay structure.
