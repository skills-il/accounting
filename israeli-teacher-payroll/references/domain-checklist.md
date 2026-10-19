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
- [x] Ofek promotion needs paznun + shapam + evaluation together: ranks 2-3 need 30 months and 120 hours, ranks 4-6 need 36 months and 180, ranks 7-9 need 48 months and 210. Quotas for ranks 7-9 were ABOLISHED in the 2016 agreement. Oz advances on merit points instead. (ofek-promotion-rule, ofek-promotion-quotas-abolished)
- [x] Seniority: 2% per year up to and including year 6, then 1% per year from the seventh year to year 36. The bundled script must encode this same rule. (seniority-rate, seniority-2pct-to-year-6)
- [x] Seniority is ALREADY in the cell: the official cell (education grade, Ofek rank where it applies, seniority) IS the combined salary; do NOT re-add a seniority percentage on top (would double-count). (seniority-rate)

### Gmul (gmul) table (render EVERY gmul type as its own row)
- [x] Ofek teachers accumulate dev hours, NOT gmulim; Oz teachers accumulate max 1 gmul/year. (ofek-no-gmul)
- [x] Oz merit points: 10 points = one promotion grade of 1.67% of the combined salary, at most 4 grades (6.69%), at least 3 years apart, points for one role only. The old "10 points = 2%, up to 8%" was wrong. Resolved 2026-10-19 from the ministry credit-points page. (oz-merit-points-1-67, oz-promotion-points)
- [x] Oz tosefet shiklit 2023: 1,790.50 NIS full position from 1.9.2026 (1,518 from 1.9.2025); 2,066.75 scheduled 1.9.2027 in the signed table. PRORATED by position including above 100%; pensionable and keren-bearing; not a base for other supplements. (oz-shekel-supplement-2026, oz-shekel-supplement-prorated, oz-shekel-supplement)
- [x] Oz gmul tafkid beit-sifri (tashpaz): 2-5 units x 200 NIS, full value from 1/3 position, full-position amount above 100%, inside the two-role cap, not for principals or deputies, no keren hishtalmut deposit. (oz-gmul-beit-sifri)
- [x] Irgun HaMorim agreement of 31.8.2026 (to 31.8.2029): physics bagrut gmul 2% to 4% from 1.9.2026; one-off gmul shiluv 600 / 2,000 NIS for tashpav; 8.6.2026 strike day not deducted. (oz-agreement-310826-physics, oz-gmul-shiluv-tashpav, oz-strike-day-260608)
- [x] Gmul hishtalmut: 112 hours = 1 unit; 1.2% per unit, rising to 1.3% from 1.9.2025; the Oz quota is 19 units (raised from 18 in tashaf), at most one banked per year. (gmul-hishtalmut-unit, oz-hishtalmut-quota-19)
- [x] Gmul chinuch (homeroom): 10% OR 1,000 NIS, whichever is higher, from 1.9.2024; grade-1 homeroom 11.5%. (gmul-chinuch-rate, gmul-chinuch-floor-1000)
- [x] Subject-coordinator gmul 8%, and 9% for maths and English coordinators, from 1.9.2025. A "gmul pituach miktzoi 6%" row was REMOVED on 2026-10-19: no source names that gmul or rate. (gmul-coordinator-and-dev, gmul-rakaz-miktzoa-9-math-eng)
- [x] The salary cell has an education-grade dimension in BOTH reforms (musmach, musmach bachir, BA, MA, doctorate). Ofek: grade x rank 1-9 x seniority; Oz: grade x seniority plus up to 4 promotion grades of 1.67% (their part-time treatment is unpublished, assumed to scale). The 9 ranks are an Ofek structure. (education-grade-both-reforms, oz-merit-points-1-67)
- [x] Ofek tosefet Ofek 2022: shekel supplement by education grade and rank step, 1,585.54 NIS rank 1 BA / 1,664.87 MA as updated 1.9.2023, falling to under 20 NIS at the top; current amount read from the slip. (tosefet-ofek-2022)
- [x] Gmul hishtalmut is prorated by position at each employer (and applies above 100%); it is a study gmul, not a role gmul. (hishtalmut-prorated-by-position)
- [x] July and August: holiday pay in proportion to months worked; no component changes in those months. (july-august-proportional)
- [x] Pension layers: vatika, tzoveret, expense reimbursements, above-100%; July maternity retro deductions. (teacher-pension-layers, july-maternity-deductions)
- [x] Every Oz rakaz gmul as its own row (tikshuv 8%, pedagogi 8%, shichva 6% or 1,100 NIS higher-of, chinuch chevrati 10%, miyumanuyot / tiyulim / hishtalvut / bagrut / mishmaat / maarechet / yeutz 6%). These are page TEXT on poh, not an image; do not route the user away from them. (gmul-rakaz-tikshuv-pedagogi-8, gmul-rakaz-shichva, gmul-rakaz-chinuch-chevrati-10, gmul-rakaz-6pct-roles)
- [x] Gmul yeutz by licence: 12% temporary, 18% permanent, from 1.9.2024. (gmul-yeutz-licence)
- [x] Gmul chinuch meyuchad: 10% / 15% / 17% (autism or severe psychiatric), from 1.9.2024. (gmul-chinuch-meyuchad-rates)
- [x] Gmul yozma chinuchit beit-sifrit (Ofek Chadash, NEW from 1.9.2026): 2-5 units per initiative at the principal's discretion, 200 NIS per unit per month, 400-1,000 NIS per month, re-decided annually, teachers and appointed deputy principals. Fixed-shekel, NOT a percentage of the combined salary. (gmul-yozma-chinuchit-2026)
- [x] Kindergarten management gmul (gmul nihul gan), an Ofek Chadash role: ALL THREE bands, 17% / 20% / 21%, each with a 1,500 NIS floor, with TWO columns: an existing gananet by management years (up to 5, 6-10, above 10), a new gananet by Ofek rank (1-2, 3-4, 5-9). A one- or two-band rendering is a coverage gap. (gmul-nihul-gan)
- [x] Ofek role gmulim (e.g. gmul chinuch) still apply even though Ofek teachers do not bank hishtalmut/merit gmulim. (ofek-no-gmul, gmul-chinuch-rate)
- [x] Additional gmulim beyond the core list: gmul nihul / sgan menahel (principals and deputies, distinct from gan management) and gmul chinuch meyuchad (special education); English/math/physics have their own separate incentive arrangements. (structural, no invented rate)
- [x] At most two role gmulim (gmulei tafkid) per teacher. (two-role-gmul-max)

### Gross-to-net deduction step (mechanics live in israeli-payroll-calculator)
- [x] National insurance employee rate: reduced 1.04%, full 7% above 7,703 NIS, capped at maximum insured income 51,910 NIS. That pair is ONLY the able-bodied 18-to-retirement row; the categorical rows a teacher actually hits must be named: a working old-age pensioner and an under-18 pay NOTHING on the employee side (the 0.61%/2.12% there is the employer alone), a 67-70 non-pensioner pays 3.93%/10.03%, a disability-pension holder pays 3.23%/5.17%. (bl-max-insured-income, bl-employee-categorical-rows, bl-employee-pensioner-zero, bl-employee-disability-3-23, bl-employee-total-4-27-12-17)
- [x] Health tax: 3.23% below the 7,703 NIS reduced step, 5.17% above, so the employee total is 4.27% then 12.17%. (btl-health-insurance-rates-2026, bl-employee-total-4-27-12-17)
- [x] Income tax: progressive brackets (route to israeli-payroll-calculator, do not restate).
- [x] Pension TYPE flag: pensia taktzivit (budgetary, older/veteran) vs pensia tzoveret (funded, newer) materially changes the employee deduction and net. (structural)
- [x] Keren Hishtalmut: dedicated teacher fund employee 4.2% / employer 8.4% (carries the sabbatical right); non-dedicated fund 2.5% / 7.5%. (keren-hishtalmut-teacher-rates)
- [x] Funded-pension deposit rates: employer 7.5% + 6.224% severance, employee 6% or 7%. Budgetary pension: state teachers with kviut hired before 1.9.2002; the employee deduction is not published, read the slip. (teacher-pension-rates, teacher-budgetary-pension-cutoff)
- [x] Union dues: demei chaver / demei tipul to Histadrut HaMorim or Irgun HaMorim appears on essentially every teacher slip; do not omit. (structural, no invented rate)
- [x] Non-percentage layer: fixed-shekel tosafot (tosafot shkaliyot) and non-scaling reform/percentage tosafot exist; the base x (1 + Sum gmul) model cannot express them, so the script is an approximation, not a full slip. (structural)
- [x] Havraa: teachers are PUBLIC sector, 511.60 NIS/day from 1.6.2026 (was 471.40), NOT the private-sector 451.50 NIS; days by teaching seniority 7/9/10/11/12/13, proportional for part-time. (havraa-public-2026, havraa-teacher-days, havraa-private-451)
- [x] Clothing allowance (bigud): 2,527 NIS full position at seniority level 4 in 2026; the 91 NIS cut and de-indexation were a ONE-TIME 2025 measure. (bigud-2026, teacher-clothing-2025-a, teacher-clothing-2025-b)
- [x] July-August: holiday pay in proportion to months worked; no pay component changes in those months. Part-time caveat: role gmulim stay whole, study gmulim scale, and promotion grades are assumed to scale (unpublished; check the slip). (july-august-proportional, hishtalmut-prorated-by-position)

### Context baselines
- [x] Minimum wage 6,443.85 NIS/month in force since 1.4.2026 (6,247.67 NIS from 1.4.2025); hourly 35.40 NIS. (min-wage-2025, min-wage-monthly-2026, min-wage-hourly-2025)
- [ ] The 186-hour-basis hourly rate is deliberately NOT carried: teacher hours come from the reform work-week, not an hourly basis, so it would only invite the private-sector hourly logic the skill warns against. Out of scope (explicit), reviewed 2026-08-27.
- [x] Average wage 13,769 NIS (Jan 2026). (avg-wage-2026)
- [ ] Minimum wage as a percentage of the average wage: NOT carried. The percentage formulation is superseded by legislated steps and adds nothing to a teacher computation. Out of scope (explicit), reviewed 2026-08-27.
- [x] Teacher base pay comes from the collective-agreement tables, NOT the generic bracket math. (starting-salary-approx)

- [x] Role gmulim are computed on a FULL position and are NOT prorated by chelkiyut misra; the two exceptions are the special-education and inclusion gmulim, computed on the share of frontal hours in that setting. The bundled script must implement this, not prorate everything. (ofek-gmul-full-position)
- [x] Shekel floors are a higher-of test, not an add-on (1,000 NIS gmul chinuch, 1,100 NIS Oz rakaz shichva). Whether a floor itself prorates at part-time is UNRESOLVED and must be stated as such rather than guessed. (gmul-chinuch-floor-1000, gmul-rakaz-shichva)
- [x] Fixed-shekel lines (Oz tosefet shiklit, gmul yozma chinuchit, Oz gmul tafkid beit-sifri, the retention grant) are never expressible as a percentage gmul, and they split: the tosefet shiklit is prorated by position (`--fixed-prorated`), the school-role gmulim are paid in full (`--fixed`). (oz-shekel-supplement-prorated, gmul-yozma-chinuchit-2026, oz-gmul-beit-sifri, teacher-retention-grant-10000)
- [x] Retention grant conditions: kviut at 70%+ position; prorated by weighted position over 36 months; timing conflict (union: September 2026 salary; agreement: May after kviut). Pension and tax treatment UNRESOLVED. (teacher-retention-grant-10000, retention-grant-conditions)
- [x] A shekel floor belongs to ONE gmul; the script must never test a floor against the sum of several gmulim. (gmul-chinuch-floor-1000)
- [ ] Ofek rakaz shichva floor: ITU says 1,000 NIS above 4 classes and none up to 4; the payroll provider's summary says 1,100 NIS on both bands. UNRESOLVED conflict, stated as such in gmul-components.md. (ofek-rakaz-shichva-conflict)
- [x] Rank and seniority advancement take effect on 1 September with the school year. (vetek-max-36-years)
- [x] The two-gmul cap's exceptions: a principal draws no role gmul, a first deputy may only be a homeroom teacher, and for a second deputy or above the deputy gmul consumes one slot. (two-role-gmul-max, ofek-principal-no-gmul)
- [x] The gross model cannot express travel reimbursement, menak yovel, havraa or bigud; these must be NAMED as excluded rather than silently missing. (structural)
- [x] The pension deduction is computed on the defined pensionable salary, not on gross, and teacher arrangements are their own rather than the private-sector extension order. (structural)
- [ ] Travel reimbursement and menak yovel RATES: out of scope (explicit), reviewed 2026-08-27. They are named as excluded from the model; their amounts are employer-specific and belong on the slip, not frozen here.
- [ ] What replaces the temporary wage reduction from 1.1.2027: UNRESOLVED, not out of scope. No source we could reach settles it, and the skill says so rather than guessing. Revisit next cycle.

## Should cover (advanced)
- [x] Split appointment / dual reform: a teacher teaching in both a junior-high (Ofek) and a high school (Oz) at once earns under BOTH reforms, each part by its own position fraction, table, hour structure, and gmulim; total = Ofek part + Oz part. Salary unification (ichud maskorot) puts both on one payslip (needs >=1/3 in junior-high for the Ministry route or >=1/2 in high school for the baalut route, plus kviut); without it two employers mean a yearly teum mas; above 100% combined, unification loses benefits capped at 100% (havraa, bigud, meonot). (split-appointment-dual-reform, ichud-maskorot-official, ichud-maskorot-eligibility, ichud-maskorot-tax-coord, ichud-over-100-benefit-cap). Conditions now sourced to the Ministry salary-consolidation page, including the larger-position and baalut-first rules and the excluded principals.
- [x] Why the same teacher gets a different table under each reform.
- [x] The tashpe transition for Oz (older payslips use the 40-hour base).
- [x] BOTH reforms reduce hours by age. Oz: 23 frontal / 36 total at 50-55, 21 / 34 over 55. Ofek: minus 2 frontal from age 50, minus 4 (3 frontal + 1 private) from 55, minus 2 for a newly hired teacher from 50. (oz-age-band-hours, ofek-age-reduction)
- [x] "Shaot gil" and reductions in required frontal hours by age (mentioned, route to union guide).
- [x] Afternoon / extra-activity pay beyond the fixed position (Ofek).
- [x] A worked Python breakdown that takes a base rate as input (no invented table).

## Out of scope (explicit)
- [ ] Standard private-sector gross-to-net payroll (use israeli-payroll-calculator).
- [ ] Bookkeeping journal entries for salary (use israeli-bookkeeping-automation).
- [ ] Bagrut and school-system navigation (use israeli-education-system).
- [ ] Higher-education / university lecturer pay (different agreements).
- [ ] Exact per-rank NIS base-salary cells. RE-LITIGATED 2026-10-19: users do ask for them, so the skill answers "read the cell from the Ministry calculator (educalc) or the union table" rather than staying silent. Not capturable this cycle: the Histadrut HaMorim tables are still dated September 2022 (no tashpaz table published), the Ministry calculator is interactive with no dated table, and the Irgun HaMorim site did not render. Freezing a 2022 cell would be wrong. Re-check next cycle.

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
- Bituach Leumi employee rates (the English-slug page 404s; this is the live one): https://www.btl.gov.il/Insurance/Rates/Pages/%D7%9C%D7%A2%D7%95%D7%91%D7%93%D7%99%D7%9D%20%D7%A9%D7%9B%D7%99%D7%A8%D7%99%D7%9D.aspx
- Minimum wage (Kol Zchut, carries the current monthly and hourly figures): https://www.kolzchut.org.il/he/%D7%A9%D7%9B%D7%A8_%D7%9E%D7%99%D7%A0%D7%99%D7%9E%D7%95%D7%9D
- Position scope / combining across divisions (Portal Ovdei Horaa): see evidence claim ref-url-position-scope
- Salary unification (ichud maskorot), official: https://poh.education.gov.il/administrative/salary/salary-consolidation/
- Oz credit points: https://poh.education.gov.il/administrative/salary-agreements/oz-letmura/credit-points-oz/
- Keren hishtalmut and pension rates (Ministry): https://poh.education.gov.il/administrative/salary/training-gemel/education-fund/ and https://poh.education.gov.il/administrative/salary/training-gemel/pension/
- Salary unification (ichud maskorot) advantages/disadvantages: see evidence claims split-appointment-dual-reform, ichud-maskorot-eligibility, ichud-maskorot-tax-coord, ichud-over-100-benefit-cap

## Extraction notes
- Kolzchut, gov.il, and Wikipedia could not be fetched directly (domain-verification block); numbers were captured from search snippets that quote those pages verbatim. Hour tables are text, not image-based, so no Playwright render was needed.
- Per-rank NIS salary cells were deliberately NOT captured: they change with each wage agreement and belong in the live union table + the official calculator, not a frozen skill.
