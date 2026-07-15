# Domain checklist: Israeli Teacher Payroll (israeli-teacher-payroll)

Coverage contract for computing and explaining the salary of Israeli teachers
(ovdei horaa) under the two collective-agreement reforms: Ofek Chadash and Oz
LaTmura. Every "Must cover" row maps to a claim in evidence.json.

## Must cover (core)

### Which reform applies
- [x] Ofek Chadash covers kindergarten (gan), elementary (yesodi), and junior-high (chativat beynayim). (ofek-applies-to, ofek-kindergartens, ofek-kindergartens-portal)
- [x] Oz LaTmura covers upper-secondary (high school / chativa elyona) teachers ONLY. Kindergartens are NOT under Oz. (oz-applies-and-gmul-merit, ofek-kindergartens)
- [x] The reform decides the whole hour structure and pay table, so it must be identified first.
- [x] Employer / baalut distinction: upper-secondary teachers are often employed by a baalut (ORT, Amal, AMIT, Branco Weiss) or a municipality, not the ministry directly, which changes who issues the payslip and sometimes the pension arrangement. (structural)

### Ofek Chadash work-week table (render EVERY row)
- [x] Full 100% position total = 36 weekly hours (frontal + private + stay). (ofek-total-hours)
- [x] Elementary row: 26 frontal + 5 private + 5 stay = 36. (ofek-elementary-split)
- [x] Junior-high row: 23 frontal + 4 private + 9 stay = 36. (ofek-juniorhigh-split)
- [x] Private (pratani) hour definition: 1 student or small group up to 5. (ofek-private-def)
- [x] Stay (shehiya) hour definition: meetings, prep, parents, checking work. (ofek-stay-def)

### Oz LaTmura work-week table (render EVERY row)
- [x] Base position = 40 weekly hours: 24 frontal + 6 private + 10 support. (oz-base-structure-40)
- [x] The 10 support-hour breakdown: meetings 2, team training 2, parents 1, prep+checking 5. (oz-support-breakdown)
- [x] Private hour definition: group up to 3 (up to 5 by pedagogical decision). (oz-private-def)
- [x] tashpe (2024/25) change: 38 weekly hours, 25 frontal + 3 private. (oz-tshpe-change)

### Rank (daraga) and seniority (vetek)
- [x] 9 ranks (1-9); new teacher starts at rank 1. (ofek-9-ranks)
- [x] Ofek-specific promotion: paznun + 60 dev hours/year up to rank 6; rank 7+ adds 75 hours/year + quotas + evaluation. Oz advances on merit points, NOT a dev-hour quota. (ofek-promotion-rule, oz-applies-and-gmul-merit)
- [x] Seniority: 2% per year to year 7, then 1% per year to year 36. (seniority-rate)
- [x] Seniority is ALREADY in the cell: the official (rank x seniority) grid cell IS the combined salary; do NOT re-add a seniority percentage on top (would double-count). (seniority-rate)

### Gmul (gmul) table (render EVERY gmul type as its own row)
- [x] Ofek teachers accumulate dev hours, NOT gmulim; Oz teachers accumulate max 1 gmul/year. (ofek-no-gmul)
- [x] Oz merit-point promotion gmul: 10 points = 2%, up to 4 gmulim = 8%. (oz-applies-and-gmul-merit)
- [x] Gmul hishtalmut: 112 hours = 1 unit; 1.2% per unit up to 16, up to 29.7% dual-degree; per-unit rate 1.2% to 1.3% from 1.9.2025. (gmul-hishtalmut-unit)
- [x] Gmul chinuch (homeroom): 10%, grade-1 homeroom 11.5%. (gmul-chinuch-rate)
- [x] Subject-coordinator gmul (non-English/math): 8%; professional-development role gmul: 6%. (gmul-coordinator-and-dev)
- [x] Kindergarten management gmul (gmul nihul gan), an Ofek Chadash role: ~17% (up to 5 yrs), 20% (6-10 yrs). (gmul-nihul-gan)
- [x] Ofek role gmulim (e.g. gmul chinuch) still apply even though Ofek teachers do not bank hishtalmut/merit gmulim. (ofek-no-gmul, gmul-chinuch-rate)
- [x] Additional gmulim beyond the core list: gmul nihul / sgan menahel (principals and deputies, distinct from gan management) and gmul chinuch meyuchad (special education); English/math/physics have their own separate incentive arrangements. (structural, no invented rate)
- [x] At most two role gmulim (gmulei tafkid) per teacher. (two-role-gmul-max)

### Gross-to-net deduction step (mechanics live in israeli-payroll-calculator)
- [x] National insurance employee rate: reduced 1.04% (from 0.40%), full 7.00%. (bituach-leumi-employee-rates)
- [x] Health tax: 3.23% below the 7,703 NIS reduced step, 5.17% above. (health-tax-rates)
- [x] Income tax: progressive brackets (route to israeli-payroll-calculator, do not restate).
- [x] Pension TYPE flag: pensia taktzivit (budgetary, older/veteran) vs pensia tzoveret (funded, newer) materially changes the employee deduction and net. (structural)
- [x] Keren Hishtalmut: teacher study-fund contribution via the employer; teacher-specific, read the slip. (structural)
- [x] Union dues: demei chaver / demei tipul to Histadrut HaMorim or Irgun HaMorim appears on essentially every teacher slip; do not omit. (structural, no invented rate)
- [x] Non-percentage layer: fixed-shekel tosafot (tosafot shkaliyot) and non-scaling reform/percentage tosafot exist; the base x (1 + Sum gmul) model cannot express them, so the script is an approximation, not a full slip. (structural)
- [x] Havraa (recreation pay) and 12-month spread (July-August paid). Part-time caveat: not every role gmul scales like the combined salary under chelkiyut misra. (structural)

### Context baselines
- [x] Minimum wage 6,247.67 NIS (1.4.2025), 6,443.85 NIS (1.4.2026), hourly 34.32 NIS. (min-wage-2025, min-wage-2026)
- [x] Average wage 13,769 NIS (Jan 2026); minimum wage = 47.5% of average. (avg-wage-2026, min-wage-def-pct)
- [x] Teacher base pay comes from the collective-agreement tables, NOT the generic bracket math. (starting-salary-approx)

## Should cover (advanced)
- [x] Split appointment / dual reform: a teacher teaching in both a junior-high (Ofek) and a high school (Oz) at once earns under BOTH reforms, each part by its own position fraction, table, hour structure, and gmulim; total = Ofek part + Oz part. Salary unification (ichud maskorot) puts both on one payslip (needs >=1/3 in junior-high for the Ministry route or >=1/2 in high school for the baalut route, plus kviut); without it two employers mean a yearly teum mas; above 100% combined, unification loses benefits capped at 100% (havraa, bigud, meonot). (split-appointment-dual-reform, ichud-maskorot-eligibility, ichud-maskorot-tax-coord, ichud-over-100-benefit-cap)
- [x] Why the same teacher gets a different table under each reform.
- [x] The tashpe transition for Oz (older payslips use the 40-hour base).
- [x] "Shaot gil" and reductions in required frontal hours by age (mentioned, route to union guide).
- [x] Afternoon / extra-activity pay beyond the fixed position (Ofek).
- [x] A worked Python breakdown that takes a base rate as input (no invented table).

## Out of scope (explicit)
- [ ] Standard private-sector gross-to-net payroll (use israeli-payroll-calculator).
- [ ] Bookkeeping journal entries for salary (use israeli-bookkeeping-automation).
- [ ] Bagrut and school-system navigation (use israeli-education-system).
- [ ] Higher-education / university lecturer pay (different agreements).
- [ ] Exact per-rank NIS base-salary cells (they change per wage agreement; route to the union table + official calculator, never invent a cell).

## Authoritative sources
- Ofek Chadash work-week (Ministry of Education, Portal Ovdei Horaa): https://poh.education.gov.il/administrative/salary-agreements/new-ofek/work-week-ofek/
- Ofek Chadash rank page: https://poh.education.gov.il/administrative/salary-agreements/new-ofek/new-ofek-degree/
- Ofek Chadash covers kindergartens (Ministry of Education): https://mosdot.education.gov.il/teachers/ofek-reform/
- Ofek Chadash in kindergartens (Ministry of Education kindergarten portal): https://pob.education.gov.il/institutions/main-kindergartens/kindergarten-ofek/
- Oz LaTmura reform (Portal Ovdei Horaa): https://poh.education.gov.il/administrative/salary-agreements/oz-letmura/oz-litmura-reform/
- Gmulei hishtalmut (Ministry of Education): https://poh.education.gov.il/MerhavMinhali/HskalaVetek/Pages/GmuleiHishtalmut.aspx
- Salary grade and seniority (terms-service.education.gov.il): https://terms-service.education.gov.il/terms/general-1b/salary-grade-and-seniority/
- Official salary-simulation calculator: https://poh.education.gov.il/administrative/salary/salary-sheet/salary-simulation-calculator/
- Histadrut HaMorim (work-week + gmulei tafkid): https://www.itu.org.il/
- Bituach Leumi rates: https://www.btl.gov.il/Insurance/Rates/Pages/for-employees.aspx
- Minimum / average wage: https://www.btl.gov.il/Mediniyut/GeneralData/Pages/minimum-wage.aspx
- Position scope / combining across divisions (Portal Ovdei Horaa): see evidence claim ref-url-position-scope
- Salary unification (ichud maskorot) eligibility + advantages/disadvantages: see evidence claims split-appointment-dual-reform, ichud-maskorot-eligibility, ichud-maskorot-tax-coord, ichud-over-100-benefit-cap

## Extraction notes
- Kolzchut, gov.il, and Wikipedia could not be fetched directly (domain-verification block); numbers were captured from search snippets that quote those pages verbatim. Hour tables are text, not image-based, so no Playwright render was needed.
- Per-rank NIS salary cells were deliberately NOT captured: they change with each wage agreement and belong in the live union table + the official calculator, not a frozen skill.
