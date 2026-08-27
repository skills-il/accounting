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
  python3 teacher_gross.py --base 8000 --gmul 10 --gmul-floor 1000 --position 0.5
  python3 teacher_gross.py --base 14000 --gmul 8 --fixed 1518 --position 1.0
  python3 teacher_gross.py --base 12000 --gmul 15 --scale-gmulim --position 0.5
  python3 teacher_gross.py --base 10000 --illustrative-seniority 10

HOW POSITION FRACTION IS APPLIED. Role gmulim (gmulei tafkid) are computed on a
FULL position and are NOT prorated by chelkiyut misra, per the Histadrut HaMorim
gmulei-tafkid page: "כל גמולי התפקיד מחושבים לפי משרה מלאה למעט גמול מורה לחינוך
מיוחד ומורה שילוב". So by default this script scales only the combined salary by
--position and leaves the gmul pay whole. Pass --scale-gmulim for the two
exceptions (special-education and inclusion gmulim), which are computed on the
share of frontal hours taught in the special-education setting.

FIXED-SHEKEL LINES. Several teacher pay components are shekel amounts, not
percentages: the Oz tosefet shiklit, the gmul yozma chinuchit, and the floors
under gmul chinuch (1,000 NIS) and Oz rakaz shichva (1,100 NIS). Pass a flat
amount with --fixed, and a higher-of floor with --gmul-floor. Never enter a
shekel amount as a --gmul percentage.

UNRESOLVED: no source we could reach states whether a shekel FLOOR itself
prorates at part-time, or whether the higher-of test runs before or after the
position fraction. This script runs the higher-of test on the full-position gmul
pay and then leaves it unscaled, consistent with the full-position rule above,
and says so in its output. Reconcile against the actual slip.
"""

import argparse


# Seniority rule, kept ONLY for the optional illustrative approximation below:
# 2 percent for each year up to and including year 6, then 1 percent for each
# year from the seventh year up to year 36 (Ofek Chadash collective agreement).
# This is NOT applied to the gross, because the official cell already includes
# seniority. It is exposed only to show, roughly, how much of a bare rank base
# seniority would represent when someone has ONLY a no-seniority figure.
SENIORITY_HIGH_RATE = 0.02   # years 1 to 6 inclusive
SENIORITY_LOW_RATE = 0.01    # year 7 up to year 36
SENIORITY_LOW_START = 6
SENIORITY_CAP_YEARS = 36


def seniority_fraction(years: int) -> float:
    """Illustrative seniority uplift as a fraction, for the approximation only.

    Example: 5 years gives 0.10 (10 percent); 10 years gives 0.12+0.04=0.16.
    Not used in the gross computation (the official cell already includes vetek).
    This curve is the Ofek Chadash one. Oz LaTmura seniority follows its own
    agreement curve, so do not read this as an Oz figure.
    """
    years = max(0, min(years, SENIORITY_CAP_YEARS))
    high_years = min(years, SENIORITY_LOW_START)
    low_years = max(0, years - SENIORITY_LOW_START)
    return high_years * SENIORITY_HIGH_RATE + low_years * SENIORITY_LOW_RATE


def compute(combined_base: float, gmul_pcts, position: float,
            gmul_floor: float = 0.0, fixed: float = 0.0,
            scale_gmulim: bool = False):
    """Compute a gross salary breakdown from the combined-salary cell.

    combined_base   NIS combined salary (rank x seniority cell) from the official
                    table. This ALREADY includes seniority; do not re-add it.
    gmul_pcts       list of gmul percentages, for example [10, 6] for a
                    homeroom gmul plus a professional-development gmul.
    position        position fraction, for example 1.0 for full or 0.5 for half.
    gmul_floor      a shekel floor applied to the gmul pay as a higher-of test,
                    e.g. 1000 for gmul chinuch. Applied to the FULL-position gmul.
    fixed           flat shekel additions that are not a percentage of anything
                    (tosefet shiklit, gmul yozma chinuchit). Never prorated here.
    scale_gmulim    prorate the gmul pay by position too. Only correct for the
                    special-education and inclusion gmulim.
    """
    if combined_base < 0:
        raise ValueError("--base cannot be negative")
    if position <= 0:
        raise ValueError("--position must be greater than 0")
    gmul_total_pct = sum(gmul_pcts)
    gmul_pct_pay = combined_base * (gmul_total_pct / 100.0)
    gmul_pay = max(gmul_pct_pay, gmul_floor) if gmul_floor else gmul_pct_pay
    floor_binds = bool(gmul_floor) and gmul_floor > gmul_pct_pay
    base_part = combined_base * position
    gmul_part = gmul_pay * position if scale_gmulim else gmul_pay
    gross = base_part + gmul_part + fixed
    return {
        "combined_base": combined_base,
        "gmul_total_pct": gmul_total_pct,
        "gmul_pct_pay": round(gmul_pct_pay, 2),
        "gmul_floor": gmul_floor,
        "floor_binds": floor_binds,
        "gmul_pay": round(gmul_pay, 2),
        "fixed": fixed,
        "position": position,
        "scale_gmulim": scale_gmulim,
        "base_part": round(base_part, 2),
        "gmul_part": round(gmul_part, 2),
        "gross_full_position": round(combined_base + gmul_pay + fixed, 2),
        "gross": round(gross, 2),
    }


def render(result: dict) -> str:
    lines = [
        "Teacher gross salary breakdown",
        "==============================",
        f"Combined salary cell (rank x seniority, already includes vetek): "
        f"{result['combined_base']:,.2f} NIS",
        f"Position fraction: {result['position']}",
        f"  combined salary x position = {result['base_part']:,.2f} NIS",
        f"Gmulim: +{result['gmul_total_pct']}% of the full-position cell "
        f"= {result['gmul_pct_pay']:,.2f} NIS",
    ]
    if result["gmul_floor"]:
        if result["floor_binds"]:
            lines.append(
                f"  FLOOR BINDS: {result['gmul_floor']:,.2f} NIS is higher than the "
                f"percentage, so the floor is paid")
        else:
            lines.append(
                f"  floor of {result['gmul_floor']:,.2f} NIS does not bind "
                f"(percentage is higher)")
    if result["scale_gmulim"]:
        lines.append(
            f"  gmul prorated by position (special-education / inclusion rule) "
            f"= {result['gmul_part']:,.2f} NIS")
    else:
        lines.append(
            f"  gmul NOT prorated: role gmulim are computed on a full position "
            f"= {result['gmul_part']:,.2f} NIS")
    if result["fixed"]:
        lines.append(
            f"Fixed-shekel additions: {result['fixed']:,.2f} NIS (not prorated)")
    lines += [
        f"Gross for this position: {result['gross']:,.2f} NIS",
        "",
        "Note: this is GROSS and an APPROXIMATION of the core salary. It does not",
        "model travel reimbursement, menak yovel, havraa, bigud, or any other",
        "non-scaling line, and it applies no shekel floor you did not pass with",
        "--gmul-floor. Whether a shekel floor itself prorates at part-time is not",
        "stated by any source we could reach, so reconcile against the slip. Net",
        "follows after income tax, national insurance, health tax, pension, and",
        "union dues. See the israeli-payroll-calculator skill for the deduction",
        "step. Confirm the combined cell on the official calculator; it already",
        "includes seniority, so do not add a seniority percentage to it.",
    ]
    return "\n".join(lines)


def render_seniority_approx(years: int) -> str:
    frac = seniority_fraction(years)
    out = [
        "",
        "ILLUSTRATIVE SENIORITY APPROXIMATION (NOT part of the gross above)",
        "-----------------------------------------------------------------",
        "WARNING: the official (rank x seniority) cell ALREADY includes vetek.",
        "Do NOT add this on top of --base or you will double-count seniority.",
        "This block is only for the rare case where you have a bare rank base",
        "with zero seniority and want a rough sense of the vetek portion.",
        "This is the Ofek Chadash curve; do not read it as an Oz figure.",
        f"For {years} year(s), seniority would be about +{round(frac * 100, 2)}%.",
    ]
    if years > SENIORITY_CAP_YEARS:
        out.append(
            f"NOTE: seniority is capped at {SENIORITY_CAP_YEARS} years, so "
            f"{years} was clamped to {SENIORITY_CAP_YEARS}.")
    return "\n".join(out)


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
    parser.add_argument("--gmul-floor", type=float, default=0.0,
                        help="shekel floor for the gmul, applied as a higher-of "
                             "test against the percentage, e.g. 1000 for gmul "
                             "chinuch or 1100 for Oz rakaz shichva")
    parser.add_argument("--fixed", type=float, action="append", default=None,
                        help="a flat shekel addition that is not a percentage "
                             "(tosefet shiklit, gmul yozma chinuchit); repeat "
                             "for several. Never prorated by --position")
    parser.add_argument("--scale-gmulim", action="store_true",
                        help="prorate the gmul pay by --position too. Correct "
                             "ONLY for the special-education and inclusion "
                             "gmulim; role gmulim are computed on a full position")
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
    try:
        result = compute(combined_base=args.base, gmul_pcts=gmuls,
                         position=args.position, gmul_floor=args.gmul_floor,
                         fixed=sum(args.fixed) if args.fixed else 0.0,
                         scale_gmulim=args.scale_gmulim)
    except ValueError as exc:
        parser.error(str(exc))
    print(render(result))
    if args.illustrative_seniority is not None:
        print(render_seniority_approx(args.illustrative_seniority))


if __name__ == "__main__":
    main()
