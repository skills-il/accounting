---
name: israeli-attendance-wage-checker
description: >-
  Not legal advice. Turns an Israeli timesheet into a wage reconciliation: converts clock-in and
  clock-out spans into working hours, splits them into ordinary, overtime and weekly-rest hours,
  applies the statutory premiums, and itemises owed against paid. Works for a small employer
  checking compliance and for an employee who suspects a short payslip. Use when a user asks
  whether they were paid correctly for overtime or Shabbat, how to compute shaot nosafot, what a
  timesheet is actually worth, or what to do when the employer kept no hours record. It matters
  because the premium tiers reset daily rather than monthly, the statutory week and the practical
  week are different numbers, and an employer who kept no ledger carries the burden of proof up to
  a capped number of hours. Do NOT use for gross-to-net (use israeli-payroll-calculator), for
  severance or notice pay, to draft a claim, or for teacher or foreign-caregiver payroll.
license: MIT
allowed-tools: 'Bash(python3:*)'
compatibility: >-
  Knowledge plus a Python reconciliation helper (pure local arithmetic, no network). The helper is
  optional: Step 6 states the same arithmetic for agents that cannot run scripts.
---

# Israeli Attendance Wage Checker

## Legal notice

This is a free information tool operated by an AI model. It explains the law and computes an indicative figure from the hours you supply. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by an advocate. The output is not legal advice and not a legal opinion. It is a general explanation and an arithmetic estimate only: it does not read your employment contract, does not know which collective agreement or extension order applies to your workplace, does not check current case law, and does not examine your specific circumstances. An AI model may err, omit data, or present a wrong conclusion.

The binding computation is the one your employer is obliged to make under the law and any applicable collective agreement, and a labour court decides any dispute about it. Any figure this tool produces is a draft for your personal preparation only, it is not a document prepared by an advocate, and it must not be relied on as evidence. This tool is not a substitute for advice that takes account of the particular circumstances and needs of each person, and before filing anything you should consult a licensed advocate. All use of the output is the user's sole responsibility.

## Problem

An Israeli payslip shows a number of hours and a number of shekels, and almost nobody can tell whether the second follows from the first. The arithmetic is not intuitive: the premium tiers reset every day rather than accumulating over the month, so a worker can be owed overtime in a week where he worked exactly the standard hours. The statutory week and the week actually used in the economy are different figures, and quoting the wrong one moves every downstream number. Meal breaks come out of the count but some breaks stay in. And the most valuable rule of all is procedural rather than arithmetic: an employer who did not keep the hours ledger the law requires carries the burden of proving the employee did not work the disputed hours, up to a capped number of them. This skill starts from raw clock-in and clock-out entries and produces the reconciliation neither side usually has.

## Problem boundary

This skill starts from HOURS and stops at GROSS owed. It does not compute income tax, National Insurance, health tax, pension, or net pay, which is `israeli-payroll-calculator`. It does not handle severance, notice pay, or end-of-employment settlements, and it does not compute annual leave, recuperation pay, or travel as standalone entitlements, though it flags them where they trigger a statutory presumption. It does not draft a claim or assess its merits. Teacher payroll and foreign-caregiver payroll have their own dedicated skills; do not reimplement them here.

## Instructions

Read `references/rates-and-tiers.md` before computing any figure and `references/records-and-remedies.md` before answering anything about missing records, payslips, or late payment.

### Step 0, the applicability gate, run this first and every time

The Hours of Work and Rest Law does not apply to everyone. It expressly excludes police and prison service, state employees required to be available outside regular hours, seafarers and fishermen, air crew, **employees in management roles or in roles requiring a special degree of personal trust**, and employees whose work conditions prevent the employer from exercising any supervision over their hours.

If the worker falls in one of these classes, **no overtime and no weekly-rest premium is owed at all**, and every figure this skill would produce is legally meaningless. Ask before computing.

Two things about that gate matter more than the list itself, and most write-ups omit both:

- **The exclusion is the employer's to prove, and it is construed narrowly.** It is a defence, not the default. A worker is inside the law unless the employer establishes otherwise, so an agent that treats "you were a manager" as settled has silently decided the case against the user.
- **It turns on what the person actually did, not on a job title.** A "manager" with no subordinates, no discretion over budget or hiring, and a clocked-in schedule is very unlikely to fall inside it. Where it is arguable, say it is arguable, compute the figure as a conditional, and name what evidence would settle it (an org chart, signing authority, whether the person clocked in).

### Step 1, establish the basis before touching the numbers

1. **Pay basis**: monthly salaried, or hourly/daily. This changes the rest-day answer completely, see Step 4.
2. **Which week applies.** The statute says a work week shall not exceed **45 hours**. The practical basis in the economy has been **42 hours** since the 2018 extension order, implemented by shortening one defined day rather than by trimming every day. Public bodies that joined the later framework agreement moved to 40. Ask which applies, and for which period, because a user reconciling an older payslip needs the basis that applied then.
3. **The daily maximum did not change.** It is still **8 hours**, and **7 hours** on night work, on the day before the weekly rest, and on the day before a holiday the employee does not work. The 2018 order moved only the weekly basis.
4. **Five or six day week**, and which day is the shortened one.
5. **The period being reconciled**, and whether a payslip exists for it.
6. **The hourly rate itself, where the wage is global.** A monthly wage does not state an hourly rate, and every premium in this skill is a multiple of one. Derive it from the wage and the agreed monthly hours basis, state the divisor you used, and say plainly that a different divisor changes every figure downstream. Do not silently assume a divisor.
7. **Check the wage against the minimum-wage floor before anything else.** If the derived hourly rate is below the statutory minimum in force for that period, that shortfall is its own claim and it sits underneath the whole reconciliation. This skill does not carry the minimum-wage figure, because it is updated by order; look it up for the specific period rather than using a remembered number.
8. **Tips.** In service sectors, whether tips form part of the wage, and on what basis they were recorded, changes the base every premium multiplies. Establish it rather than assuming the payslip's base line is the whole wage.

### Step 2, convert the raw spans into working hours

Working hours are the time the employee stands at the employer's disposal, including short agreed rest breaks and toilet breaks, and **excluding** the statutory meal break.

- A day of six hours or more carries a break of at least three quarters of an hour, including one continuous half hour. Deduct it unless Step 3 says otherwise.
- On the day before the weekly rest or a holiday the break is at least half an hour.
- Night work is any work with at least two hours falling between 22:00 and 06:00.

### Step 3, decide which breaks are paid

A break of half an hour or more counts as **part of working hours** where the employee's presence at the workplace was necessary to the work process or to the operation of equipment and the employer required him to stay. A shop assistant told to eat behind the counter is on paid time; a worker free to leave is not. Ask which it was rather than assuming, because it is often the largest single line in the reconciliation.

### Step 4, split the hours and apply the premiums

**Order matters. Compute daily first, then weekly, and never from a monthly total.** Overtime is defined against the daily bound and against the weekly bound independently, so a worker can be owed overtime in a week that totals exactly the standard hours.

| Hours | Rate |
|---|---|
| Ordinary, within the daily and weekly bounds | 100 percent |
| First two overtime hours **of that day** | 125 percent |
| Third overtime hour of that day onward | 150 percent |
| Weekly rest (and holiday, where it applies) | 150 percent |

Three things that change the answer:

- **The two-hour tier resets every day.** It is not a monthly allowance. An agent that applies it once per month understates the claim badly.
- **The base is not bare salary.** For these two sections, "regular wage" includes **all the supplements the employer pays**. Computing 125 percent off base pay while ignoring supplements is the most common way a shortfall is created.
- **Rest day depends on pay basis.** A monthly-salaried employee is already paid for the day, so the marginal entitlement is the premium element on top, plus paid compensating rest. An hourly or daily paid employee is entitled to the full 150 percent, and the compensating rest is treated as unpaid unless an agreement says otherwise. Note the paid/unpaid split is labour-court practice, not statutory text, so present it as practice. `references/rates-and-tiers.md` works both through.

The weekly rest is at least **36 continuous hours**, which is what decides whether a Saturday-night shift is still inside it.

### Step 5, flag the compliance breaches separately from the money

Hours beyond the permitted caps are still owed their premium, but the illegality is a separate finding and should be reported separately rather than folded into the money. Flag at least: a gap of less than **8 hours** between one working day and the next; a day exceeding the overtime caps; and night-shift patterns beyond what is permitted. Report these as "this may be unlawful, here is the provision", not as an entitlement.

### Step 6, produce the reconciliation

Show owed against paid, per period, with the gap itemised by cause. If you can run scripts, `scripts/reconcile_hours.py` does the daily-then-weekly split and the tiering. If you cannot, do it inline: for each day, hours worked minus break, compare to the daily bound, tier the excess 2 then rest; then sum the ordinary hours across the week and tier anything above the weekly bound; then value each bucket against the regular wage **including supplements**.

Never present the output as a figure the employer owes as a matter of decided law. It is what the statutory rates produce on the hours supplied.

### Step 7, when there is no hours record

This is the highest-value part of the skill and it is procedural.

The employer must keep a ledger of work hours, weekly rest hours, overtime and the premiums. Where the hours are in dispute in an employee's claim, **the burden of proof is on the employer** to show the employee was not at his disposal during the disputed hours, if the employer did not produce attendance records from that ledger.

Two limits that most write-ups omit, and that the skill must state:

- The burden applies only up to **15 weekly overtime hours or 60 monthly overtime hours**. It is not unlimited.
- The employee still has to put forward a minimal factual version of what he worked. The shift is not a substitute for saying anything.

**Do not let the cap shape what the user claims.** The 15/60 figure limits how far the evidentiary presumption carries, not how many hours a person may claim. A user who genuinely worked more should plead the hours they worked and prove the excess by ordinary means. An agent that quietly trims the claim down to the cap has given away the difference before anyone has argued about it.

### Step 7b, global overtime, and what the remedy actually is

A wage set so as to include overtime or weekly-rest premium is treated by `סעיף 5` of the Wage Protection Law as **regular wage only**. Get the consequence right, because the common version of it is wrong:

The remedy is **re-characterisation, not a top-up of the excess**. It is not "the global covers 40 hours, you worked 46, so 6 hours are owed". If the arrangement fails, the whole global sum is treated as regular wage, the hourly rate is re-derived from it, and **every** overtime hour in the period is then owed its premium on that re-derived rate. That is a materially larger figure, and an agent that computes only the excess understates the claim.

The labour courts do recognise a valid global arrangement, on cumulative conditions: informed consent, a genuine supplement rather than a relabelling of existing pay, respect for the statutory caps, a payslip that separates the component, and periodic reconciliation so the global is not systematically below the real hours. State the conditions, apply them to the facts the user gives, and do not validate the arrangement as compliant on the user's say-so.

### Step 7c, evidence, and how long the claim lives

**Evidence first.** Where the employer has no ledger, the user's own material is what carries the claim. Tell them to collect, and preserve, what they already have: payslips for the whole period, the employment contract and any global-pay annex, their own diary or calendar, entry-badge or shift-app records, WhatsApp and email traffic showing when they were asked to stay, and the names of colleagues who worked the same shifts. A written request to the employer for the section 24 ledger is worth making in its own right, because a refusal is itself informative.

**The limitation clock on the wage.** A wage claim is an ordinary civil claim and it prescribes in **seven years** (`סעיף 5(1)` of the Limitation Law, "בשאינו מקרקעין, שבע שנים"), running from when the cause of action arose, which for wages means each payment separately. Say this whenever a user asks about an old period, and keep it distinct from the far shorter delayed-wage clock in Step 8. Confusing the two is how a live seven-year wage claim gets abandoned because someone read the 60-day figure.

### Step 7d, what this skill does not price

Flag these and stop, rather than folding a guess into the figure:

- **Sector extension orders** (guarding, cleaning, hotels and restaurants, manpower contractors, care work) set their own rates and supplements above the statutory floor. If one applies, it governs and the figures here are the fallback.
- **דמי חגים** (holiday pay) is a separate entitlement with its own qualifying conditions and its own interaction with the rest-day rules. It is adjacent to this reconciliation, not part of it.

### Step 8, timing, and the two different clocks

A monthly wage is payable at the end of the month it is paid for. Delayed wage attracts compensation computed as the **higher of** two formulas, one week-based and one index-plus-percentage based, both set out in `references/records-and-remedies.md`.

Warn about the clock, because it is short and it is not the same as the wage claim: the right to delayed-wage compensation lapses if no claim is filed within **one year** from when the wage is treated as delayed, or **60 days** from receiving the related wage, **whichever is earlier**, extendable by the court to 90 days. The underlying wage itself remains claimable far longer. A user told only the halana figure, with no clock, has been actively misled.

## Examples

### A five-day week, one long Tuesday

Tuesday runs 08:00 to 19:30 with a 45-minute break. Working hours 10.75, daily bound 8, so 2.75 overtime hours: two at 125 percent and 0.75 at 150 percent. Even if the week totals under the weekly bound, that Tuesday premium is owed, because the daily limb is independent.

### Saturday work, two employees, same hours

Both work six hours in the weekly rest. The monthly-salaried employee is already paid for the day, so the marginal entitlement is the premium element plus paid compensating rest. The hourly employee is entitled to 150 percent of his hourly rate for all six hours, with unpaid compensating rest. Same hours, different owed figure.

### No attendance records at all

The employee says he worked roughly ten overtime hours a week for a year and the employer produced nothing. Explain the burden shift, then immediately explain the cap and the requirement to give a minimal factual version, and produce the figure as a bounded range rather than as the full year at ten hours a week.

### A payslip with no hours line

Point out that the payslip must state the hours actually worked and the value of a regular hour, then move to the presumption that a missing or incomplete payslip triggers, which is set out in the references.

## Reference Links

| Source | URL | What to check |
|---|---|---|
| חוק שעות עבודה ומנוחה | https://he.wikisource.org/wiki/חוק_שעות_עבודה_ומנוחה | Sections 1, 2, 3, 7, 16, 17, 18, 20, 21, 25, 30 |
| חוק הגנת השכר | https://he.wikisource.org/wiki/חוק_הגנת_השכר | Sections 5, 9, 17, 17a, 24, 26b and the Schedule |
| צו הרחבה, קיצור שבוע העבודה | https://www.gov.il/BlobFolder/dynamiccollectorresultitem/extention-order-short-week-2018/he/extention-order-short-week-2018.pdf | The 42-hour basis and the shortened-day mechanism |

## Bundled Resources

| File | Use it for |
|---|---|
| `references/rates-and-tiers.md` | The full tier table, the monthly-versus-hourly rest-day split, worked examples |
| `references/records-and-remedies.md` | Ledger duty, the burden shift and its cap, payslip fields, delayed-wage computation and its clock |
| `references/domain-checklist.md` | Coverage contract, and figures circulating in the wild that are wrong |
| `scripts/reconcile_hours.py` | Daily-then-weekly split and tiering. Optional, see Step 6 |

## Gotchas

- **The two-hour tier is daily, not monthly.** Applying it once per month is the single most common computational error and it always understates what is owed.
- **Never compute from a monthly hour total.** The daily limb and the weekly limb are independent, so a month that looks fine in aggregate can still contain owed overtime on individual days.
- **The statutory week and the operative week are different numbers.** The statute says 45; the economy has run on 42 since 2018; some public bodies are at 40. Say which one you are using and why.
- **The premium base includes supplements.** Computing off bare base salary is how a compliant-looking payslip hides a shortfall.
- **"No records means the employee wins everything" is wrong.** The burden shift is capped, and the employee must still give a minimal factual version.
- **The delayed-wage clock is much shorter than the wage claim.** Reporting a halana figure without the one-year and 60-day limits misleads the user about what is still recoverable.
- **Check the applicability gate before doing any arithmetic.** For a genuine management or personal-trust role the entire computation is void, and producing a confident number for such a worker is worse than producing none.

## Troubleshooting

| Symptom | Cause | What to do |
|---|---|---|
| The monthly totals look right but the user insists he is owed | The daily limb was ignored | Recompute day by day; overtime can arise in a week that totals exactly the standard hours |
| The premium comes out lower than the user expects | The base excluded supplements | Recompute the regular wage including all supplements the employer pays |
| Two employees worked the same Saturday and the figures differ | Monthly-salaried versus hourly | This is correct. Explain the two regimes rather than reconciling them |
| The employer says the salary already includes overtime | Inclusive wage | Such a wage is treated as regular wage only, so the entitlement survives; check whether an approved collective agreement applies |
| The user wants net pay | Out of scope | Compute gross owed here and hand off to `israeli-payroll-calculator` |
| The worker is a manager | The applicability gate | Do not produce a premium figure as though it were owed. Explain the exclusion and that it turns on the actual role |
