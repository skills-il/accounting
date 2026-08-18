#!/usr/bin/env python3
"""Israeli teacher gross-salary breakdown helper.

Builds a gross monthly salary from the COMBINED-salary cell you read off the
official table, applying any gmul (increment) percentages and then scaling by
the position fraction.

IMPORTANT about seniority: the official union salary tables and the Ministry of
Education salary-simulation calculator are two-dimensional grids of rank
(daraga) by seniority (vetek). The cell you read for a given (rank, seniority)
pair IS the combined salary (sachar meshulav) and ALREADY includes seniority.
So this script does NOT add a seniority percentage on top of the base you pass
in. Re-adding seniority would double-count it. Pass the combined cell as --base.

This script does NOT ship a NIS rank table: teacher base pay comes from the
collective-agreement salary tables (Ofek Chadash / Oz LaTmura), which change
with every wage agreement. Read the combined cell for the exact rank, seniority,
reform, and year from the Ministry of Education salary calculator or the
teachers' union table, then feed it here.

This is an approximation of the core salary, not a full payslip. Real teacher
slips also carry fixed-shekel additions (tosafot shkaliyot), reform / percentage
tosafot that do not scale with rank, and havraa (recreation pay). A model built
only from base times gmulim cannot express those lines.

No third-party dependencies. Standard library only.

Usage:
  python3 teacher_gross.py --example
  python3 teacher_gross.py --base 12000 --gmul 10 --gmul 6 --position 1.0
"""

import argparse


# Seniority rule, kept ONLY for the optional illustrative approximation below:
# 2 percent for each of the first 7 years, then 1 percent for each year from
# year 8 up to year 36 (education ministry terms-of-service seniority page).
# This is NOT applied to the gross, because the official cell already includes
# seniority. It is exposed only to show, roughly, how much of a bare rank base
# seniority would represent when someone has ONLY a no-seniority figure.
SENIORITY_HIGH_RATE = 0.02   # years 1 to 7
SENIORITY_LOW_RATE = 0.01    # years 8 to 36
SENIORITY_LOW_START = 7
SENIORITY_CAP_YEARS = 36


def seniority_fraction(years: int) -> float:
    """Illustrative seniority uplift as a fraction, for the approximation only.

    Example: 5 years gives 0.10 (10 percent); 10 years gives 0.14+0.03=0.17.
    Not used in the gross computation (the official cell already includes vetek).
    """
    years = max(0, min(years, SENIORITY_CAP_YEARS))
    high_years = min(years, SENIORITY_LOW_START)
    low_years = max(0, years - SENIORITY_LOW_START)
    return high_years * SENIORITY_HIGH_RATE + low_years * SENIORITY_LOW_RATE


def compute(combined_base: float, gmul_pcts, position: float):
    """Compute a gross salary breakdown from the combined-salary cell.

    combined_base   NIS combined salary (rank x seniority cell) from the official
                    table. This ALREADY includes seniority; do not re-add it.
    gmul_pcts       list of gmul percentages, for example [10, 6] for a
                    homeroom gmul plus a professional-development gmul.
    position        position fraction, for example 1.0 for full or 0.5 for half.
    """
    gmul_total_pct = sum(gmul_pcts)
    gmul_pay = combined_base * (gmul_total_pct / 100.0)
    gross_full = combined_base + gmul_pay
    gross = gross_full * position
    return {
        "combined_base": combined_base,
        "gmul_total_pct": gmul_total_pct,
        "gmul_pay": round(gmul_pay, 2),
        "gross_full_position": round(gross_full, 2),
        "position": position,
        "gross": round(gross, 2),
    }


def render(result: dict) -> str:
    lines = [
        "Teacher gross salary breakdown",
        "==============================",
        f"Combined salary cell (rank x seniority, already includes vetek): "
        f"{result['combined_base']:,.2f} NIS",
        f"Gmulim: +{result['gmul_total_pct']}% "
        f"= {result['gmul_pay']:,.2f} NIS",
        f"Gross, full position: {result['gross_full_position']:,.2f} NIS",
        f"Position fraction: {result['position']}",
        f"Gross for this position: {result['gross']:,.2f} NIS",
        "",
        "Note: this is GROSS and an APPROXIMATION of the core salary. It does not",
        "model fixed-shekel tosafot, non-scaling reform tosafot, or havraa. Net",
        "follows after income tax, national insurance, health tax, pension, and",
        "union dues. See the israeli-payroll-calculator skill for the deduction",
        "step. Confirm the combined cell on the official calculator; it already",
        "includes seniority, so do not add a seniority percentage to it.",
    ]
    return "\n".join(lines)


def render_seniority_approx(years: int) -> str:
    frac = seniority_fraction(years)
    return "\n".join([
        "",
        "ILLUSTRATIVE SENIORITY APPROXIMATION (NOT part of the gross above)",
        "-----------------------------------------------------------------",
        "WARNING: the official (rank x seniority) cell ALREADY includes vetek.",
        "Do NOT add this on top of --base or you will double-count seniority.",
        "This block is only for the rare case where you have a bare rank base",
        "with zero seniority and want a rough sense of the vetek portion.",
        f"For {years} year(s), seniority would be about +{round(frac * 100, 2)}%.",
    ])


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build an Israeli teacher gross salary from the combined cell."
    )
    parser.add_argument("--base", type=float,
                        help="NIS combined salary cell (rank x seniority) from "
                             "the official table; it already includes seniority")
    parser.add_argument("--gmul", type=float, action="append", default=None,
                        help="a gmul percentage; repeat for several gmulim")
    parser.add_argument("--position", type=float, default=1.0,
                        help="position fraction, e.g. 1.0 full or 0.5 half")
    parser.add_argument("--illustrative-seniority", type=int, default=None,
                        metavar="YEARS",
                        help="OPTIONAL: print a clearly-labeled illustrative "
                             "seniority uplift; NOT added to the gross (the "
                             "official cell already includes seniority)")
    parser.add_argument("--example", action="store_true",
                        help="run a worked illustrative example")
    args = parser.parse_args()

    if args.example:
        # Illustrative only. The base here is a placeholder combined cell, NOT an
        # official figure. It stands in for a real (rank x seniority) cell you
        # would read from the union table or the ministry calculator.
        print("Illustrative example (placeholder combined cell, not an official cell):")
        print()
        demo = compute(combined_base=12000.0, gmul_pcts=[10, 6], position=1.0)
        print(render(demo))
        return

    if args.base is None:
        parser.error("provide --base (the combined salary cell) or use --example")

    gmuls = args.gmul if args.gmul else []
    result = compute(combined_base=args.base, gmul_pcts=gmuls,
                     position=args.position)
    print(render(result))
    if args.illustrative_seniority is not None:
        print(render_seniority_approx(args.illustrative_seniority))


if __name__ == "__main__":
    main()
