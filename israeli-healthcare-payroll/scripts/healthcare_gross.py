#!/usr/bin/env python3
"""Israeli public-healthcare-sector gross-salary breakdown helper.

Builds a gross monthly salary for a healthcare-sector employee (nurse, allied /
paramedical clinician, hospital pharmacist, doctor) from the COMBINED-salary
cell you read off the official wage-grade table, applies percentage tosafot
(allowances), adds explicit shekel shift / on-call amounts you supply, and then
scales by the position fraction.

IMPORTANT about seniority: the public-sector wage-grade tables (published by the
Wage Commissioner / hemune al hasachar and the profession unions) are
grids indexed by rank (daraga) and seniority (vetek), and for nurses there is a
separate grid per education level, so the cell is picked by (education, rank,
seniority). The cell you read for that point IS the combined salary (sachar
meshulav) and
ALREADY includes seniority. So this script does NOT add a seniority percentage
on top of the base you pass in. Re-adding seniority would double-count it. Pass
the combined cell as --base.

This script ships NO NIS grade table. Healthcare base pay comes from the
collective-agreement wage-grade tables for the relevant dirug (nurses' dirug,
paramedical dirug, pharmacists, or the doctors' agreement), and those change
with every wage agreement. Read the combined cell for the exact grade,
seniority, education level, dirug, employer, and year from the union or the Wage
Commissioner, with the framework-agreement tranche in force applied,
then feed it here.

Shift and on-call pay are NOT percentages of the base in the general case. Night
and evening shift premiums and on-call (kononut) / on-site duty (toranut) are
usually paid as their own computed amounts (a premium per shift, or an hourly
rate times hours). This script does not know those rates. Pass the already
computed shift / on-call shekel amounts via --add, or leave them out and add
them from the slip. Do not guess a shift percentage.

This is an approximation of the core salary, not a full payslip. Real healthcare
slips also carry fixed-shekel tosafot that do not scale with grade, a clothing
allowance (ktzuvat bigud) paid periodically, havraa (recreation pay), and
profession-specific lines. A model built from base times tosafot plus a few
explicit add-ons cannot express every line, so reconcile against the actual slip.

No third-party dependencies. Standard library only.

Usage:
  python3 healthcare_gross.py --example
  python3 healthcare_gross.py --base 11000 --tosefet 8 --tosefet 6 --add 1400 --position 1.0
"""

import argparse


def compute(combined_base: float, tosefet_pcts, add_amounts, position: float,
            prorated_amounts=None):
    """Compute a gross salary breakdown from the combined-salary cell.

    combined_base   NIS combined salary (grade x seniority cell) from the
                    official table. This ALREADY includes seniority; do not
                    re-add it.
    tosefet_pcts    list of percentage tosafot, for example [8, 6] for a
                    professional-development gmul plus a role tosefet. Each is a
                    percent of the combined base.
    add_amounts     list of explicit shekel additions that are NOT scaled by the
                    position fraction, because they reflect work actually done
                    rather than the position: shift premiums, on-call and duty
                    pay, the per-shift responsibility supplement.
    prorated_amounts
                    list of explicit shekel additions that ARE scaled by the
                    position fraction, because the agreement pro-rates them for
                    part-time. Tosefet achayot 2024 (500 NIS full-time) is the
                    main one: at position 0.5 it is worth 250 NIS, so passing it
                    through add_amounts would overstate a part-timer's gross.

    WARNING about mixed bases: every percentage in tosefet_pcts is applied to
    combined_base. That is correct for tosefet hachsharot and for gmul
    hishtalmut, which are defined on the combined salary. It is NOT correct for
    the nurses' tosefet nihul (7.2%), which is defined on the wider hourly-rate
    base (combined salary plus seniority plus the supplements that existed on
    31.12.2022). Passing --tosefet 7.2 here understates it. Compute that one
    separately against its own base and pass the result as an explicit amount.
    position        position fraction, for example 1.0 full or 0.5 half. Applied
                    to the base-plus-tosafot part only.
    """
    tosefet_total_pct = sum(tosefet_pcts)
    tosefet_pay = combined_base * (tosefet_total_pct / 100.0)
    core_full = combined_base + tosefet_pay
    core = core_full * position
    prorated_amounts = prorated_amounts or []
    prorated_total = sum(prorated_amounts) * position
    adds_total = sum(add_amounts)
    gross = core + adds_total + prorated_total
    return {
        "combined_base": combined_base,
        "tosefet_total_pct": tosefet_total_pct,
        "tosefet_pay": round(tosefet_pay, 2),
        "core_full_position": round(core_full, 2),
        "position": position,
        "core_for_position": round(core, 2),
        "adds_total": round(adds_total, 2),
        "prorated_total": round(prorated_total, 2),
        "gross": round(gross, 2),
    }


def render(result: dict) -> str:
    lines = [
        "Healthcare-sector gross salary breakdown",
        "========================================",
        f"Combined salary cell (education x rank x seniority, includes vetek): "
        f"{result['combined_base']:,.2f} NIS",
        f"Percentage tosafot: +{result['tosefet_total_pct']}% "
        f"= {result['tosefet_pay']:,.2f} NIS",
        f"Core (base + tosafot), full position: "
        f"{result['core_full_position']:,.2f} NIS",
        f"Position fraction: {result['position']}",
        f"Core for this position: {result['core_for_position']:,.2f} NIS",
        f"Explicit shekel additions, not pro-rated (shift / on-call): "
        f"{result['adds_total']:,.2f} NIS",
        f"Pro-rated shekel additions, scaled by position: "
        f"{result['prorated_total']:,.2f} NIS",
        f"Gross: {result['gross']:,.2f} NIS",
        "",
        "Note: this is GROSS and an APPROXIMATION of the core salary. Shift and",
        "on-call pay are supplied as explicit shekel amounts, not derived here.",
        "It does not model every fixed-shekel tosefet, the periodic clothing",
        "allowance, or havraa. Net follows after income tax, national insurance,",
        "health tax, pension, keren hishtalmut, and union dues. See the",
        "israeli-payroll-calculator skill for the deduction step. Confirm the",
        "combined cell on the official table; it already includes seniority, so",
        "do not add a seniority percentage to it.",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build an Israeli healthcare-sector gross salary from the "
                    "combined wage-grade cell."
    )
    parser.add_argument("--base", type=float,
                        help="NIS combined salary cell (grade x seniority) from "
                             "the official table; it already includes seniority")
    parser.add_argument("--tosefet", type=float, action="append", default=None,
                        help="a percentage tosefet; repeat for several tosafot")
    parser.add_argument("--add", type=float, action="append", default=None,
                        help="an explicit shekel addition (shift, on-call, "
                             "clothing); repeat for several")
    parser.add_argument("--add-prorated", type=float, action="append",
                        default=None, dest="add_prorated",
                        help="shekel addition that IS pro-rated by position "
                             "(for example tosefet achayot 2024, 500 NIS "
                             "full-time)")
    parser.add_argument("--position", type=float, default=1.0,
                        help="position fraction, e.g. 1.0 full or 0.5 half")
    parser.add_argument("--example", action="store_true",
                        help="run a worked illustrative example")
    args = parser.parse_args()

    if args.example:
        # Illustrative only. The base here is a placeholder combined cell, NOT an
        # official figure. It stands in for a real (grade x seniority) cell you
        # would read from the union table or the Wage Commissioner.
        print("Illustrative example (placeholder combined cell, not an official cell):")
        print()
        demo = compute(combined_base=11000.0, tosefet_pcts=[8, 6],
                       add_amounts=[1400.0], position=1.0)
        print(render(demo))
        return

    if args.base is None:
        parser.error("provide --base (the combined salary cell) or use --example")

    tosafot = args.tosefet if args.tosefet else []
    adds = args.add if args.add else []
    prorated = args.add_prorated if args.add_prorated else []
    result = compute(combined_base=args.base, tosefet_pcts=tosafot,
                     add_amounts=adds, position=args.position,
                     prorated_amounts=prorated)
    print(render(result))


if __name__ == "__main__":
    main()
