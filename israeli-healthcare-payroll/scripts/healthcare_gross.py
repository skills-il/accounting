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
seniority, education level, dirug, employer, and month from the payslip or the
employer, then feed it here. The framework agreement's tosefet achuzit 2024 is
NOT in the cell: it is its own line on the wider hourly-rate base (the current
cell plus the supplements in force on 31.12.2022 that count for erech shaa), so
compute it separately and pass it with --add-prorated (or read it off the slip).

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

Number formats: each flag takes ONE number, written as on an Israeli payslip.
Shekel flags (--base, --add, --add-prorated) accept plain digits, comma
thousands separators (on --base also the non-breaking space a formatter emits), a decimal point or a decimal comma, and a shekel marker
(\u20aa, NIS, ILS, \u05e9"\u05d7) at the start or the end. --tosefet takes
percentage points (9 for 9%, not 0.09) and accepts a trailing %. --position
takes a fraction (0.5) or a percent (50%). A comma followed by exactly three
digits is a thousands separator; a comma followed by one or two digits is a
decimal comma. Anything else is rejected with an error rather than guessed: an
empty value, a placeholder like <cell>, two numbers in one flag ("8 6"), a unit
that contradicts the flag (a shekel marker on --tosefet, a % on a shekel flag),
a dot used as a thousands separator (3.037), NaN, infinity, or a negative value.

Usage:
  python3 healthcare_gross.py --example
  python3 healthcare_gross.py --base 11000 --tosefet 8 --tosefet 6 --add 1400 --position 1.0
"""

import argparse
import math
import re
import sys

_BIDI = re.compile("[\u200e\u200f\u202a-\u202e\u2066-\u2069\u061c]")
# Only the non-breaking and thin spaces that number formatters emit count as a
# thousands separator, only on --base (a combined cell is always a single
# number of thousands), and only when the leading group has 1 or 2 digits
# ("11 000", "11 000,50"). On every other flag they are refused. A plain space is always rejected, and so is a
# formatter space after a 3-digit group ("500 300"): those cannot be told apart
# from two numbers, and reading two numbers as one is the worse failure.
_SPACES = "\u00a0\u2009\u202f"
_SPACE_THOUSANDS = re.compile(r"^\d{1,2}([%s]\d{3})+([.,]\d{1,2}|\.\d+)?$" % _SPACES)
_THOUSANDS = re.compile(r"^\d{1,3}(,\d{3})+(\.\d+)?$")
_DOT_THOUSANDS = re.compile(r"^\d{1,3}(\.\d{3})+$")
_DECIMAL_COMMA = re.compile(r"^\d+,\d{1,2}$")
_PLAIN = re.compile(r"^\d+\.?\d*$|^\.\d+$")
# Longest first, so that "ILS" is not left half-stripped.
_CURRENCY = ("\u05e9\"\u05d7", "\u05e9\u05f4\u05d7", "\u05e9'\u05d7", "\u05e9\u05f3\u05d7",
             "\u05e9\u05d7", "\u20aa",
             "NIS", "ILS")

KINDS = ("amount", "percent", "fraction")


def _strip_token(s: str, tokens) -> (str, bool):
    """Strip one token from the start or the end of s. Case-insensitive."""
    for tok in tokens:
        if s.upper().startswith(tok.upper()):
            return s[len(tok):].strip(), True
        if s.upper().endswith(tok.upper()):
            return s[:-len(tok)].strip(), True
    return s, False


def parse_number(raw: str, what: str = "value", kind: str = "amount") -> float:
    """Parse one non-negative number written in Israeli payslip style.

    kind is "amount" (shekels), "percent" (percentage points) or "fraction"
    (a position fraction, where a trailing % means divide by 100).
    Raises ValueError with a readable message instead of guessing.
    """
    if kind not in KINDS:
        raise ValueError(f"unknown kind {kind!r}")
    if raw is None:
        raise ValueError(f"{what} is missing")
    s = _BIDI.sub("", str(raw)).strip()
    if not s:
        raise ValueError(f"{what} is empty")

    s, had_currency = _strip_token(s, _CURRENCY)
    if had_currency and kind != "amount":
        raise ValueError(f"{what} takes a {'percentage' if kind == 'percent' else 'fraction'}, "
                         f"not a shekel amount: {raw!r} (use --add for shekels)")
    had_percent = s.endswith("%")
    if had_percent:
        s = s[:-1].strip()
        if kind == "amount":
            raise ValueError(f"{what} takes shekels, not a percentage: {raw!r} "
                             "(use --tosefet for a percentage)")
    if any(tok.upper() in s.upper() for tok in _CURRENCY) or "%" in s:
        raise ValueError(f"{what}: a unit may appear only at the start or the end: {raw!r}")

    if s.startswith("+"):
        s = s[1:].strip()
    if s.startswith("-"):
        raise ValueError(f"{what} cannot be negative: {raw!r}")
    if not s:
        raise ValueError(f"{what} is empty")

    if _SPACE_THOUSANDS.match(s) and what == "--base":
        s = re.sub("[%s]" % _SPACES, "", s).replace(",", ".")
    elif re.search("[\\s%s]" % _SPACES, s):
        raise ValueError(f"{what}: one number per flag (repeat the flag for several "
                         f"values; write a thousands separator as a comma): {raw!r}")

    if _THOUSANDS.match(s):
        s = s.replace(",", "")
    elif _DECIMAL_COMMA.match(s):
        s = s.replace(",", ".")
    elif kind == "amount" and _DOT_THOUSANDS.match(s):
        raise ValueError(f"{what}: {raw!r} is ambiguous (a dot used as a thousands "
                         "separator?). Write it with a comma or with no separator")
    elif not _PLAIN.match(s):
        raise ValueError(f"{what} is not a number: {raw!r}")
    value = float(s)
    if not math.isfinite(value):
        raise ValueError(f"{what} is not a finite number: {raw!r}")
    if kind == "fraction" and had_percent:
        value = value / 100.0
    return value


def _arg(what: str, kind: str):
    """argparse type wrapper so the parse error message reaches the user."""
    def convert(raw: str) -> float:
        try:
            return parse_number(raw, what, kind)
        except ValueError as exc:
            raise argparse.ArgumentTypeError(str(exc))
    return convert


class _StoreOnce(argparse.Action):
    """Reject a flag given twice instead of silently keeping the last value."""
    def __call__(self, parser, namespace, values, option_string=None):
        if getattr(namespace, "_seen_" + self.dest, False):
            parser.error(f"{option_string} given more than once")
        setattr(namespace, "_seen_" + self.dest, True)
        setattr(namespace, self.dest, values)


def compute(combined_base: float, tosefet_pcts, add_amounts, position: float,
            prorated_amounts=None):
    """Compute a gross salary breakdown from the combined-salary cell.

    combined_base   NIS combined salary (grade x seniority cell) from the
                    official table. This ALREADY includes seniority; do not
                    re-add it.
    tosefet_pcts    list of percentage tosafot defined on the combined salary,
                    for example [9] for the allied-health tosefet hachsharot
                    band. Each is a percent of the combined base.
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
    combined_base. That is correct for tosefet hachsharot, which is defined on
    the combined salary only. Check the base of any other percentage supplement
    before passing it here. It is NOT correct for the nurses' tosefet nihul
    (7.2%) or tosefet achuzit 2024, which are defined on the wider hourly-rate
    base (the current cell plus the supplements in force on 31.12.2022 that
    count for erech shaa). Passing --tosefet 7.2 here understates it. Compute that one
    separately against its own base and pass the full-position result in
    prorated_amounts (--add-prorated), since it is pro-rated for part-time.
    position        position fraction, for example 1.0 full or 0.5 half. Applied
                    to the base-plus-tosafot part only.
    """
    values = [combined_base, position] + list(tosefet_pcts) + list(add_amounts) \
        + list(prorated_amounts or [])
    if any(not math.isfinite(v) for v in values):
        raise ValueError("every value must be a finite number")
    if combined_base < 0:
        raise ValueError("--base cannot be negative")
    if any(v < 0 for v in list(tosefet_pcts) + list(add_amounts)
           + list(prorated_amounts or [])):
        raise ValueError("tosafot and shekel additions cannot be negative; "
                         "deductions belong to the net step, not here")
    if any(v > 100 for v in tosefet_pcts):
        raise ValueError("a single --tosefet above 100 percent is not a percentage "
                         "supplement; pass a shekel amount with --add instead")
    if position <= 0 or position > 1:
        raise ValueError("--position must be a fraction above 0 and at most 1 "
                         "(1.0 is a full position; overtime is not a position)")
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
    parser.add_argument("--base", type=_arg("--base", "amount"),
                        action=_StoreOnce,
                        help="NIS combined salary cell from the payslip or the "
                             "employer; it already includes seniority")
    parser.add_argument("--tosefet", type=_arg("--tosefet", "percent"),
                        action="append", default=None,
                        help="a percentage tosefet on the combined cell, in "
                             "percentage points (9 for 9%%); repeat for several. "
                             "NOT tosefet nihul, whose base is wider: compute "
                             "7.2%% x the hourly-rate base and pass it with "
                             "--add-prorated")
    parser.add_argument("--add", type=_arg("--add", "amount"),
                        action="append", default=None,
                        help="an explicit shekel addition NOT scaled by "
                             "position, because it reflects work actually done "
                             "(shift premiums, on-call, duty); repeat for several")
    parser.add_argument("--add-prorated",
                        type=_arg("--add-prorated", "amount"),
                        action="append",
                        default=None, dest="add_prorated",
                        help="shekel addition that IS pro-rated by position, "
                             "given at its FULL-POSITION amount (500, not 250 "
                             "at half time; the script scales it): tosefet "
                             "achayot 2024, the framework shekel supplement "
                             "(400 or 500 NIS), tosefet nihul; repeat for several")
    parser.add_argument("--position",
                        type=_arg("--position", "fraction"), default=1.0,
                        action=_StoreOnce,
                        help="position fraction, 0.5 or 50%%. For a partial "
                             "month or unpaid absence, multiply in the "
                             "fraction of the month worked")
    parser.add_argument("--example", action="store_true",
                        help="run a worked illustrative example")
    args = parser.parse_args()

    if args.example and (args.base is not None or args.tosefet or args.add
                         or args.add_prorated or args.position != 1.0):
        parser.error("--example takes no other flags")

    if args.example:
        # Illustrative only. The base here is a placeholder combined cell, NOT an
        # official figure. It stands in for a real (grade x seniority) cell you
        # would read from the payslip or the employer.
        print("Illustrative example (placeholder combined cell, not an official cell):")
        print()
        demo = compute(combined_base=11000.0, tosefet_pcts=[8, 6],
                       add_amounts=[1400.0], position=1.0)
        print(render(demo))
        return

    if args.base is None:
        parser.error("provide --base (the combined salary cell) or use --example")
    if args.tosefet and all(v < 1 for v in args.tosefet):
        print("warning: every --tosefet is below 1. --tosefet takes percentage "
              "points (9 for 9%), not fractions (0.09).", file=sys.stderr)
    if args.position < 0.05:
        print(f"warning: --position {args.position:g} is below 0.05 (5%); "
              "check you did not mean a percentage like 50%.", file=sys.stderr)
    if args.base < 1000:
        parser.error(f"--base {args.base:g} is below any combined cell in the "
                     "published nurse grids, even the 2008 one. Did you write a "
                     "thousands dot, or drop digits?")

    tosafot = args.tosefet if args.tosefet else []
    adds = args.add if args.add else []
    prorated = args.add_prorated if args.add_prorated else []
    try:
        result = compute(combined_base=args.base, tosefet_pcts=tosafot,
                         add_amounts=adds, position=args.position,
                         prorated_amounts=prorated)
    except ValueError as exc:
        parser.error(str(exc))
    print(render(result))


if __name__ == "__main__":
    main()
