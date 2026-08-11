# Rates, tiers, and the two rest-day regimes

Read this before computing any figure. Every rate here is the statutory floor. A collective
agreement or an extension order can be more generous, never less, so where the user's workplace has
one, it governs and this file is the fallback.

## 1. The bounds

| Bound | Value | Source |
|---|---|---|
| Working day | **8 hours** | `סעיף 2(א)` |
| Working day, night work / eve of weekly rest / eve of a holiday not worked | **7 hours** | `סעיף 2(ב)` |
| Working week, **statutory** | **45 hours** | `סעיף 3` |
| Working week, **operative in the economy since 2018** | **42 hours** | 2018 extension order |
| Working week, public bodies in the later framework agreement | 40 hours | framework agreement, ask whether it applies |
| Weekly rest | at least **36 continuous hours** | `סעיף 7` |
| Minimum gap between working days | **8 hours** | `סעיף 21` |

The 2018 order shortened the week by removing **one hour on a single defined and fixed day**, the
`יום מקוצר`, rather than trimming every day. **It did not change the daily maximum**, which is why
`סעיף 2` still reads 8 hours. An agent that "spreads" the reduction across the week will compute the
daily overtime threshold wrongly on four days out of five.

Say which weekly basis you are applying and for which period. A user reconciling a payslip from
before April 2018 needs the basis that applied then, not today's.

## 2. The premium tiers

| Bucket | Rate | Source |
|---|---|---|
| Ordinary hours | 100 percent | |
| First **two** overtime hours **of that day** | **125 percent** | `סעיף 16(א)` |
| Each overtime hour after them, same day | **150 percent** | `סעיף 16(א)` |
| Hours in the weekly rest | **150 percent** | `סעיף 17(א)(1)` |

The statute renders these as the mixed fractions `1 1/4` and `1 1/2`. A transcription that drops the
leading `1` produces 25 percent and 50 percent, understating by a factor of five. If you ever see a
quoted snippet reading `לא פחות מ־1/4 מהשכר הרגיל`, it has been mis-transcribed.

### Three rules that decide the answer

1. **The two-hour tier resets daily.** `שבאותו יום` is in the text. It is not a monthly allowance.
2. **Daily first, then weekly.** Overtime is defined against the daily bound and the weekly bound as
   two independent limbs (`סעיף 1`). Count each day's excess first; then take the remaining ordinary
   hours and count what exceeds the weekly bound. Never start from a monthly total. A worker can be
   owed overtime in a week that totals exactly the standard hours.
3. **The base includes supplements.** `סעיף 18`: for sections 16 and 17, `שכר רגיל` includes **all
   the supplements the employer pays the employee**. Computing the premium off bare base salary is
   the most common way a shortfall is manufactured on a payslip that otherwise looks compliant.

## 3. The rest day, which splits by pay basis

Same hours, two different owed figures. Get the pay basis before answering.

| | Monthly salaried | Hourly or daily paid |
|---|---|---|
| The day itself | Already covered by the monthly salary | Not otherwise paid |
| Marginal entitlement for hours in the weekly rest | The **premium element on top** of the salary already covering the day | The **full 150 percent** of the regular hourly wage |
| Compensating rest | Given. Treated as **paid** in practice (not deducted from salary or leave) | Given. Treated as **unpaid** unless an agreement provides otherwise |

**Sourcing caution on that last row.** `סעיף 17(א)(2)` requires compensating rest but is **silent on
whether it is paid**. The paid-for-monthly / unpaid-for-hourly split is settled labour-court practice
rather than statutory text, and it is NOT in this skill's evidence file. State it as practice, not as
a provision, and do not quote a section number for it.

`סעיף 17(ב)` separately lets an employer of a monthly-or-longer-salaried employee give **an hour and
a half of rest** for each rest-day hour worked, in place of the money. Compensating rest cannot be
commuted to cash and is not redeemable on termination.

## 4. Overtime inside the weekly rest

Where overtime hours fall **within** the weekly rest, the entitlements are **cumulative**, not
multiplicative: the rest-day element and the overtime element are added. Do not multiply 150 percent
by 125 percent. A multiplicative reading circulates and is wrong; the national labour court has
reaffirmed the cumulative method.

Because the exact combined figures depend on the pay basis and on whether an extension order applies,
state the components rather than asserting a single combined percentage, and show the arithmetic so
the user can check it against their own payslip.

## 5. What to flag as unlawful, separately from the money

Hours worked beyond the permitted caps are **still owed their premium**. The illegality is a separate
finding. Report it in its own section so the user does not read a compliance breach as an extra
entitlement, or an entitlement as permission.

Flag at least:

- A gap of less than 8 hours between one working day and the next (`סעיף 21`).
- A working day that, including overtime, exceeds the permitted ceiling.
- A working week exceeding the permitted overtime count.
- Night-shift patterns beyond what the permits allow.

The caps sit in a general permit rather than in the statute, and they have been varied by temporary
provisions during wartime periods. If the reconciliation covers such a period, say that the caps may
have been relaxed rather than flagging a breach you cannot substantiate.

## 6. Worked example, five-day week, 42-hour basis

Tuesday 08:00 to 19:30, 45-minute break.

```
span              11.50 h
less break         0.75 h
working hours     10.75 h
daily bound        8.00 h
overtime           2.75 h  ->  2.00 h @ 125%
                             0.75 h @ 150%
```

The Tuesday premium is owed whether or not the week reaches the weekly bound, because the daily limb
stands on its own. Then, separately, sum the week's **ordinary** hours (the 8 from Tuesday plus each
other day's ordinary hours) and tier anything above the weekly bound.

## 7. Categories this file does not cover, and where they go

- **Youth under 18**, part-timers on fixed days, piece-rate workers, and shift supplements folded
  into the base: each has its own rule. Name the rule and say it needs checking rather than applying
  the general tiers to them.
- **Holidays** interact with the rest-day rules and with holiday pay, and the combined figure differs
  again for hourly workers compelled to work. Treat as adjacent and flag.
- **Global overtime** (`גמול גלובלי`) is recognised by the labour courts on cumulative conditions,
  including informed consent, a genuine supplement, respect for the statutory caps, and a payslip
  that separates the component. Where actual overtime exceeds what the global covers, the excess is
  owed. Flag it; do not validate a global arrangement as compliant.
- **Sector regimes** (guarding, hotels and restaurants, manpower contractors, foreign care workers)
  have their own extension orders. Say so and stop.
