#!/usr/bin/env python3
"""Israeli teacher gross-salary breakdown helper.

Builds a gross monthly salary from the COMBINED-salary cell you read off the
official table, applying any gmul (increment) percentages, shekel floors and
flat shekel lines, and scaling by the position fraction where the rules say so.

IMPORTANT about the cell: the official tables and the Ministry of Education
salary-simulation calculator give the combined salary (sachar meshulav) for a
teacher's education grade (BA, MA, and so on), her rank (Ofek Chadash) and her
seniority (vetek). That cell ALREADY includes seniority, so this script does NOT
add a seniority percentage on top of the base you pass in. Pass the combined
cell as --base, for a FULL position, as a monthly NIS amount.

This script does NOT ship a NIS table: teacher base pay comes from the
collective-agreement tables (Ofek Chadash / Oz LaTmura), which change with every
wage agreement. Read the cell from the Ministry calculator or the union table,
then feed it here.

This is an approximation of the core salary, not a full payslip. Real teacher
slips also carry lines a base-times-gmulim model cannot express (travel, menak
yovel, havraa, bigud, other non-scaling tosafot).

No third-party dependencies. Standard library only.

Usage:
  python3 teacher_gross.py --example
  python3 teacher_gross.py --base 12000 --gmul 10:1000 --position 1
  python3 teacher_gross.py --base 8000 --gmul 10:1000 --position 0.5
  python3 teacher_gross.py --base 14000 --gmul 8 --gmul-scaled 10.4 --fixed-prorated 1790.50 --position 0.75
  python3 teacher_gross.py --base 12000 --gmul 10:1000 --gmul-share 15@13/26 --position 1
  python3 teacher_gross.py --base 10000 --illustrative-seniority 10

Numbers may be written as 12000, 12,000, 12000.50, 12000,50 or 12.000,50, with
or without a shekel sign or word. In amounts and gmul rates a decimal comma takes
one or two digits (a position or share such as 0,333 may take more), and an amount
written with a dot before exactly three digits (12.000) is refused as ambiguous. A
position may be written as 0.5, 0,5, 1/3, or as a percent with a percent sign.

HOW EACH LINE IS APPLIED.
  --base               scaled by --position.
  --gmul PCT[:FLOOR]   a role gmul (gmul tafkid). Computed on a FULL position and
                       NOT prorated by chelkiyut misra. Source: the Histadrut
                       HaMorim gmulei-tafkid page, "כל גמולי התפקיד מחושבים לפי
                       משרה מלאה למעט גמול מורה לחינוך מיוחד ומורה שילוב". That
                       page is about Ofek Chadash; no Oz LaTmura text we reached
                       states the rule either way, so check an Oz slip. :FLOOR is
                       that gmul's own shekel floor (higher-of test), e.g.
                       10:1000 gmul chinuch, 6:1100 Oz rakaz shichva, 17:1500 gmul
                       nihul gan. A floor belongs to ONE gmul, never to a sum.
  --gmul-share PCT[:FLOOR]@SHARE
                       the special-education and inclusion gmulim, computed on
                       the share of her frontal hours taught in that setting out
                       of all her frontal hours. SHARE is that fraction, e.g.
                       13/26 or 0.5. Whether the position fraction ALSO applies
                       on top of SHARE is not stated; the script uses the full
                       cell x PCT x SHARE and prints the alternative.
  --gmul-scaled PCT[:FLOOR]
                       a percentage of the combined salary that IS prorated by
                       --position: gmul hishtalmut (the terms of service pay it
                       in proportion to the position at each employer, above
                       100% too) and the Oz promotion grades (1.67% each; their
                       proration is assumed, not published: check the slip).
  --fixed AMOUNT       a flat shekel line paid at its FULL value regardless of
                       position: the Oz gmul tafkid beit-sifri (full value from a
                       third of a position; the full-position amount above 100%;
                       the rule below a third is not published). Also used for
                       the Ofek gmul yozma chinuchit, whose part-time rule is not
                       published.
  --fixed-prorated AMOUNT
                       a flat shekel line quoted for a FULL position and scaled by
                       --position, INCLUDING above 100%: the Oz tosefet shiklit
                       (agreement of 23.9.2024, section 7(ג)).
  --scale-gmulim       legacy switch: treat every --gmul as --gmul-scaled.

UNRESOLVED: no source we could reach states whether a shekel FLOOR itself
prorates when its gmul is prorated. The higher-of test runs on the full-position
amount and the winner is then scaled. Reconcile against the actual slip.
"""

import argparse
import math
import re


# Seniority rule, kept ONLY for the optional illustrative approximation below:
# 2 percent for each year up to and including year 6, then 1 percent for each
# year from the seventh year up to year 36 (Ofek Chadash collective agreement).
# This is NOT applied to the gross, because the official cell already includes
# seniority.
SENIORITY_HIGH_RATE = 0.02   # years 1 to 6 inclusive
SENIORITY_LOW_RATE = 0.01    # year 7 up to year 36
SENIORITY_LOW_START = 6
SENIORITY_CAP_YEARS = 36

# Sanity bounds. These do not encode pay rules; they catch inputs that are
# almost certainly a unit mistake (an hourly rate, a percent typed as a
# fraction, a shekel amount typed as a percentage).
MIN_WAGE_MONTHLY_2026 = 6443.85   # from 1.4.2026; revised by law, check yearly
POSITION_MIN = 0.025              # about one weekly hour; below is a typo
POSITION_MAX_ERROR = 1.5          # above this the input is not a fraction
POSITION_MAX_APPROVED = 1.315     # Oz: 100% + 12 frontal hours = 131.5%
GMUL_PCT_MAX = 50.0               # no single gmul is anywhere near this
FLOOR_WARN_ABOVE = 3000.0         # no published floor exceeds 1,500 NIS

_SHEKEL_WORDS = re.compile(r"(₪|ש\"ח|ש״ח|ש''ח|שקלים|שקל|שח|shekels|shekel|nis|ils)",
                           re.IGNORECASE)
_PLACEHOLDERS = ("x", "xx", "xxx", "n/a", "na", "tbd", "?", "-", "none", "null")


class InputError(ValueError):
    pass


WARNINGS = []


def _warn(msg):
    WARNINGS.append(msg)


def parse_number(raw, what, money=True, fraction=False):
    """Parse a user-supplied number, tolerating common locale formats.

    Accepts 12000, 12,000, 12000.5, 12,000.50, 12.000,50, 12000,50, 0,5 and a
    shekel sign or word. Rejects empty strings, template placeholders such as
    <rank4_cell> or RANK4_CELL, ambiguous dot-thousands (12.000), NaN and
    infinity with an explanation.
    """
    if raw is None:
        raise InputError(f"{what}: no value given")
    s = str(raw).strip()
    if not s:
        raise InputError(f"{what}: empty value. Read the figure from the official "
                         f"table or the payslip and pass it as a number")
    if (s.startswith("<") or s.endswith(">") or "{" in s
            or s.lower() in _PLACEHOLDERS
            or re.search(r"[A-Za-z_\u0590-\u05ff]{2,}", _SHEKEL_WORDS.sub("", s))):
        raise InputError(f"{what}: '{s}' is a placeholder, not a number. Read the "
                         f"real figure from the Ministry calculator or the union "
                         f"table first")
    s = _SHEKEL_WORDS.sub("", s)
    for ch in ("\u200f", "\u200e", "\u202a", "\u202b", "\u202c", " ", "\u00a0", "'"):
        s = s.replace(ch, "")
    if not s:
        raise InputError(f"{what}: '{raw}' has no digits")
    if not re.fullmatch(r"[+-]?[0-9.,]+", s):
        raise InputError(f"{what}: cannot read '{raw}' as a number")
    body = s.lstrip("+-")
    if "," in s and "." in s:
        if s.rfind(",") > s.rfind("."):
            if not re.fullmatch(r"[1-9]\d{0,2}(\.\d{3})+,\d{1,2}", body):
                raise InputError(f"{what}: cannot read '{raw}' as a number")
            s = s.replace(".", "").replace(",", ".")     # 12.000,50
        else:
            if not re.fullmatch(r"[1-9]\d{0,2}(,\d{3})+\.\d+", body):
                raise InputError(f"{what}: cannot read '{raw}' as a number")
            s = s.replace(",", "")                       # 12,000.50
    elif "," in s:
        if fraction and re.fullmatch(r"[01],\d+", body):
            s = s.replace(",", ".")                      # 0,333 as a fraction
        elif re.fullmatch(r"[1-9]\d{0,2}(,\d{3})+", body):
            s = s.replace(",", "")                       # 12,000 / 1,518
        elif re.fullmatch(r"\d+,\d{1,2}", body):
            s = s.replace(",", ".")                      # 0,5 / 10,4 / 1790,50
        else:
            raise InputError(
                f"{what}: '{raw}' is ambiguous. Use a dot for decimals, a comma "
                f"only between thousands, and PCT:FLOOR to give a gmul its floor")
    elif "." in s and money:
        if re.fullmatch(r"[1-9]\d{0,2}(\.\d{3})+", body):
            raise InputError(
                f"{what}: '{raw}' is ambiguous (dot as a thousands separator?). "
                f"Write 12000 or 12,000 for twelve thousand, or 12.0 for twelve")
    try:
        value = float(s)
    except ValueError:
        raise InputError(f"{what}: cannot read '{raw}' as a number") from None
    if math.isnan(value) or math.isinf(value):
        raise InputError(f"{what}: '{raw}' is not a finite number")
    return value


def parse_fraction(raw, what):
    """Parse a decimal, a fraction such as 1/3, or a percent-sign form."""
    s = str(raw).strip() if raw is not None else ""
    if not s:
        raise InputError(f"{what}: empty value")
    if s.endswith("%"):
        pct = parse_number(s[:-1], what, money=False)
        if 0 < pct < 1:
            raise InputError(f"{what} {raw}: {pct:g}% is almost certainly a typo. "
                             f"Did you mean {pct:g} (a fraction) or {pct * 100:g}%?")
        return pct / 100.0
    if "/" in s:
        num, _, den = s.partition("/")
        n = parse_number(num, f"{what} numerator", money=False)
        d = parse_number(den, f"{what} denominator", money=False)
        if d == 0:
            raise InputError(f"{what}: division by zero")
        return n / d
    return parse_number(s, what, money=False, fraction=True)


def parse_position(raw):
    value = parse_fraction(raw, "--position")
    if value <= 0:
        raise InputError("--position must be greater than 0")
    if value < POSITION_MIN:
        raise InputError(
            f"--position {raw} is below one weekly hour. Pass 0.5 for half a "
            f"position, 1 for full, or a percent with a percent sign")
    if value > POSITION_MAX_ERROR:
        raise InputError(
            f"--position {raw} is not a fraction of a position. Pass 0.5 for half, "
            f"1 for full, or a percent with a percent sign")
    return value


def parse_gmul(raw, what, with_share=False):
    """Parse PCT, PCT:FLOOR, and (for --gmul-share) PCT[:FLOOR]@SHARE.

    Returns (pct, floor, share). share is None unless with_share.
    """
    s = str(raw).strip() if raw is not None else ""
    share = None
    if with_share:
        if "@" not in s:
            raise InputError(f"{what} {raw}: give the special-education share as "
                             f"PCT@SHARE, e.g. 15@13/26 (13 of 26 frontal hours)")
        s, _, share_s = s.partition("@")
        share = parse_fraction(share_s, f"{what} share")
        if not 0 < share <= 1:
            raise InputError(f"{what} {raw}: the share must be above 0 and at most 1")
    elif "@" in s:
        raise InputError(f"{what} {raw}: '@SHARE' belongs to --gmul-share only")
    floor = 0.0
    if s.count(":") > 1:
        raise InputError(f"{what} {raw}: write PCT or PCT:FLOOR")
    if ":" in s:
        pct_s, _, floor_s = s.partition(":")
        floor = parse_number(floor_s, f"{what} floor")
    else:
        pct_s = s
    pct_s = pct_s.strip()
    if pct_s.endswith("%"):
        pct_s = pct_s[:-1]
    pct = parse_number(pct_s, what, money=False)
    if pct < 0:
        raise InputError(f"{what}: a gmul percentage cannot be negative")
    if pct > GMUL_PCT_MAX:
        raise InputError(
            f"{what} {raw}: {pct:g}% is not a gmul rate. If it is a shekel amount, "
            f"pass it as a floor (PCT:FLOOR) or with --fixed / --fixed-prorated")
    if floor < 0:
        raise InputError(f"{what}: a floor cannot be negative")
    if pct == 0 and floor > 0:
        raise InputError(f"{what} {raw}: a floor belongs to a real percentage gmul; "
                         f"a flat shekel line goes in --fixed")
    if 0 < pct < 1:
        _warn(f"{what} {raw}: {pct:g}% is unusually small. Gmul rates are entered "
              f"as percent (10 for 10%), not as a fraction (0.10)")
    if floor and floor < 100:
        _warn(f"{what} {raw}: a floor of {floor:g} NIS is unusually small; floors "
              f"are shekel amounts such as 1000, 1100 or 1500")
    if floor > FLOOR_WARN_ABOVE:
        _warn(f"{what} {raw}: a floor of {floor:,.2f} NIS is far above any published "
              f"floor (the highest is 1,500 NIS)")
    return pct, floor, share


def parse_amount(raw, what):
    value = parse_number(raw, what)
    if value < 0:
        raise InputError(f"{what}: a shekel amount cannot be negative")
    if 0 < value < 50:
        _warn(f"{what} {raw}: {value:g} NIS is unusually small for a shekel line. "
              f"If you meant a percentage, use --gmul instead")
    return value


def seniority_fraction(years: int) -> float:
    """Illustrative seniority uplift as a fraction, for the approximation only.

    Example: 5 years gives 0.10 (10 percent); 10 years gives 0.12+0.04=0.16.
    This curve is the Ofek Chadash one. Oz LaTmura seniority follows its own
    agreement curve, so do not read this as an Oz figure.
    """
    years = max(0, min(years, SENIORITY_CAP_YEARS))
    high_years = min(years, SENIORITY_LOW_START)
    low_years = max(0, years - SENIORITY_LOW_START)
    return high_years * SENIORITY_HIGH_RATE + low_years * SENIORITY_LOW_RATE


# A gmul line: (pct, floor, mode, share). mode is "full" (role gmul, not
# prorated), "scaled" (prorated by position) or "share" (special education).
def _gmul_line(base, pct, floor, mode, share, position):
    pct_pay = base * pct / 100.0
    full = max(pct_pay, floor)
    if mode == "scaled":
        paid = full * position
    elif mode == "share":
        paid = full * share
    else:
        paid = full
    return {"pct": pct, "floor": floor, "pct_pay": round(pct_pay, 2),
            "floor_binds": floor > pct_pay, "full": round(full, 2), "mode": mode,
            "share": share, "paid": round(paid, 2), "paid_exact": paid,
            "alt_paid": round(full * share * position, 2) if mode == "share" else None}


def compute(combined_base: float, gmuls, position: float, fixed: float = 0.0,
            fixed_prorated: float = 0.0):
    """Compute a gross salary breakdown from the combined-salary cell.

    combined_base   NIS combined salary cell for a FULL position. Already
                    includes seniority; do not re-add it.
    gmuls           list of (pct, floor, mode, share) tuples; floor 0 = none;
                    mode "full" | "scaled" | "share"; share only for "share".
    position        position fraction, 1.0 full, 0.5 half.
    fixed           flat shekel lines paid in full whatever the position.
    fixed_prorated  flat shekel lines quoted per full position, scaled by
                    position including above 100% (Oz tosefet shiklit).
    """
    if not combined_base or combined_base <= 0:
        raise InputError("--base must be a positive monthly NIS amount")
    if position <= 0:
        raise InputError("--position must be greater than 0")
    norm = []
    for g in gmuls:
        if len(g) == 3:            # (pct, floor, scaled_bool), older callers
            pct, floor, scaled = g
            norm.append((pct, floor, "scaled" if scaled else "full", None))
        else:
            norm.append(g)
    lines = [_gmul_line(combined_base, p, f, m, sh, position) for p, f, m, sh in norm]
    base_part = combined_base * position
    gmul_part = sum(l["paid_exact"] for l in lines)
    fixed_prorated_part = fixed_prorated * position
    gross = base_part + gmul_part + fixed + fixed_prorated_part
    alt_delta = sum(l["alt_paid"] - l["paid_exact"] for l in lines
                    if l["mode"] == "share")
    return {
        "combined_base": combined_base,
        "position": position,
        "base_part": round(base_part, 2),
        "gmul_lines": lines,
        "gmul_part": round(gmul_part, 2),
        "fixed": fixed,
        "fixed_prorated": fixed_prorated,
        "fixed_prorated_part": round(fixed_prorated_part, 2),
        "gross": round(gross, 2),
        "gross_alt_share": round(gross + alt_delta, 2) if alt_delta else None,
    }


def render(result: dict) -> str:
    out = [
        "Teacher gross salary breakdown",
        "==============================",
        f"Combined salary cell (full position, already includes vetek): "
        f"{result['combined_base']:,.2f} NIS",
        f"Position fraction: {result['position']:g}",
        f"  combined salary x position = {result['base_part']:,.2f} NIS",
    ]
    for i, l in enumerate(result["gmul_lines"], 1):
        out.append(f"Gmul {i}: {l['pct']:g}% of the full-position cell = "
                   f"{l['pct_pay']:,.2f} NIS")
        if l["floor"]:
            if l["floor_binds"]:
                out.append(f"  FLOOR BINDS: {l['floor']:,.2f} NIS is higher, so the "
                           f"floor is paid")
            else:
                out.append(f"  floor of {l['floor']:,.2f} NIS does not bind")
        if l["mode"] == "scaled":
            out.append(f"  prorated by position = {l['paid']:,.2f} NIS")
        elif l["mode"] == "share":
            out.append(f"  x special-education share {l['share']:g} = "
                       f"{l['paid']:,.2f} NIS (if the position fraction also "
                       f"applies: {l['alt_paid']:,.2f} NIS)")
        else:
            out.append(f"  NOT prorated (role-gmul full-position rule) = "
                       f"{l['paid']:,.2f} NIS")
    if result["fixed"]:
        out.append(f"Flat shekel lines paid in full: {result['fixed']:,.2f} NIS")
    if result["fixed_prorated"]:
        out.append(f"Flat shekel lines prorated by position: "
                   f"{result['fixed_prorated']:,.2f} x {result['position']:g} "
                   f"= {result['fixed_prorated_part']:,.2f} NIS")
    out.append(f"Gross for this position: {result['gross']:,.2f} NIS")
    if result.get("gross_alt_share") is not None:
        out.append(f"  (alternative reading for the special-education gmul: "
                   f"{result['gross_alt_share']:,.2f} NIS)")
    out += [
        "",
        "Note: this is GROSS and an APPROXIMATION of the core salary. It does not",
        "model travel reimbursement, menak yovel, havraa, bigud, or any other",
        "non-scaling line. Whether a shekel floor itself prorates at part-time is",
        "not stated by any source we could reach; this script tests the floor on",
        "the full-position amount. Reconcile against the slip. Net follows after",
        "income tax, national insurance, health tax, pension, keren hishtalmut,",
        "union dues and, in 2026, the temporary wage reduction.",
    ]
    if WARNINGS:
        out.append("")
        out.append("WARNINGS:")
        out += [f"  - {w}" for w in WARNINGS]
    return "\n".join(out)


def render_seniority_approx(years: int) -> str:
    frac = seniority_fraction(years)
    out = [
        "",
        "ILLUSTRATIVE SENIORITY APPROXIMATION (NOT part of the gross above)",
        "-----------------------------------------------------------------",
        "WARNING: the official cell ALREADY includes vetek.",
        "Do NOT add this on top of --base or you will double-count seniority.",
        "This is the Ofek Chadash curve; do not read it as an Oz figure.",
        f"For {min(years, SENIORITY_CAP_YEARS)} year(s), seniority would be about "
        f"+{round(frac * 100, 2)}%.",
    ]
    if years > SENIORITY_CAP_YEARS:
        out.append(f"NOTE: seniority is capped at {SENIORITY_CAP_YEARS} years, so "
                   f"{years} was clamped to {SENIORITY_CAP_YEARS}.")
    return "\n".join(out)


def _single(values, flag):
    if not values:
        return None
    if len(values) > 1:
        raise InputError(f"{flag} was given {len(values)} times. Run the script once "
                         f"per division (for example once for the Ofek part and once "
                         f"for the Oz part) and add the results")
    return values[0]


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(
        description="Build an Israeli teacher gross salary from the combined cell."
    )
    parser.add_argument("--base", action="append", default=[],
                        help="NIS combined salary cell for a FULL position; it "
                             "already includes seniority")
    parser.add_argument("--gmul", action="append", default=[], metavar="PCT[:FLOOR]",
                        help="a role gmul percentage, computed on a full position and "
                             "not prorated. Optional :FLOOR is its own shekel floor, "
                             "e.g. 10:1000. Repeat for several gmulim")
    parser.add_argument("--gmul-share", action="append", default=[],
                        metavar="PCT[:FLOOR]@SHARE",
                        help="special-education or inclusion gmul, by the share of "
                             "frontal hours in that setting, e.g. 15@13/26")
    parser.add_argument("--gmul-scaled", action="append", default=[],
                        metavar="PCT[:FLOOR]",
                        help="a percentage prorated by --position (gmul hishtalmut, "
                             "Oz promotion grades)")
    parser.add_argument("--position", action="append", default=[],
                        help="position fraction: 1, 0.5, 1/3, or a percent with a "
                             "%% sign. Default 1")
    parser.add_argument("--gmul-floor", action="append", default=[],
                        help="legacy: a shekel floor for the ONLY --gmul given. "
                             "Prefer PCT:FLOOR")
    parser.add_argument("--fixed", action="append", default=[], metavar="NIS",
                        help="flat shekel line paid in full whatever the position "
                             "(Oz gmul tafkid beit-sifri, Ofek gmul yozma chinuchit)")
    parser.add_argument("--fixed-prorated", action="append", default=[], metavar="NIS",
                        help="flat shekel line quoted per full position and scaled by "
                             "--position, including above 100%% (Oz tosefet shiklit)")
    parser.add_argument("--scale-gmulim", action="store_true",
                        help="legacy: treat every --gmul as --gmul-scaled")
    parser.add_argument("--illustrative-seniority", type=int, default=None,
                        metavar="YEARS",
                        help="OPTIONAL: print an illustrative seniority uplift; NOT "
                             "added to the gross")
    parser.add_argument("--example", action="store_true",
                        help="run a worked illustrative example (takes no other input)")
    args = parser.parse_args(argv)

    if args.example:
        if (args.base or args.gmul or args.gmul_scaled or args.gmul_share or args.fixed
                or args.fixed_prorated or args.position or args.gmul_floor
                or args.scale_gmulim or args.illustrative_seniority is not None):
            parser.error("--example runs a fixed demo and takes no other input")
        print("Illustrative example (placeholder combined cell, not an official cell):")
        print()
        demo = compute(combined_base=12000.0,
                       gmuls=[(10, 1000, "full", None), (6, 0, "full", None)],
                       position=1.0)
        print(render(demo))
        return

    try:
        base_raw = _single(args.base, "--base")
        if base_raw is None:
            parser.error("provide --base (the combined salary cell) or use --example")
        base = parse_number(base_raw, "--base")
        if base <= 0:
            raise InputError("--base must be a positive monthly NIS amount")
        pos_raw = _single(args.position, "--position")
        position = parse_position(pos_raw) if pos_raw is not None else 1.0
        gmuls = []
        for g in args.gmul:
            pct, floor, _ = parse_gmul(g, "--gmul")
            gmuls.append((pct, floor, "scaled" if args.scale_gmulim else "full", None))
        for g in args.gmul_scaled:
            pct, floor, _ = parse_gmul(g, "--gmul-scaled")
            gmuls.append((pct, floor, "scaled", None))
        for g in args.gmul_share:
            pct, floor, share = parse_gmul(g, "--gmul-share", with_share=True)
            gmuls.append((pct, floor, "share", share))
        floor_raw = _single(args.gmul_floor, "--gmul-floor")
        if floor_raw is not None:
            legacy_floor = parse_amount(floor_raw, "--gmul-floor")
            if len(args.gmul) != 1 or args.gmul_scaled or args.gmul_share:
                raise InputError(
                    "--gmul-floor is ambiguous unless exactly one --gmul is given: a "
                    "floor belongs to one gmul. Write it as --gmul 10:1000 instead")
            pct, floor, mode, share = gmuls[0]
            if pct == 0:
                raise InputError("--gmul-floor needs a real percentage gmul")
            gmuls[0] = (pct, max(floor, legacy_floor), mode, share)
        fixed = sum(parse_amount(v, "--fixed") for v in args.fixed)
        fixed_prorated = sum(parse_amount(v, "--fixed-prorated")
                             for v in args.fixed_prorated)
        if args.illustrative_seniority is not None and args.illustrative_seniority < 0:
            raise InputError("--illustrative-seniority cannot be negative")
    except InputError as exc:
        parser.error(str(exc))

    if base < MIN_WAGE_MONTHLY_2026:
        _warn(f"--base {base:,.2f} is below the full-time monthly minimum wage "
              f"({MIN_WAGE_MONTHLY_2026:,.2f} NIS from 1.4.2026). --base must be the "
              f"FULL-position monthly cell, not an hourly rate or an already "
              f"part-time amount")
    if base > 60000:
        _warn(f"--base {base:,.2f} is far above any teacher table cell. Check it is "
              f"a monthly NIS figure")
    if position > POSITION_MAX_APPROVED:
        _warn(f"position {position:g} is above the 131.5% Oz ceiling (100% plus 12 "
              f"approved frontal hours). Check the input")
    elif position > 1:
        _warn(f"position {position:g} is above a full position. Excess needs "
              f"ministry approval; --fixed lines stay at the full-position amount")
    if fixed and position < 1 / 3 - 1e-9:
        _warn("a --fixed line below a third of a position: the Oz gmul tafkid "
              "beit-sifri is guaranteed at full value only from a third, and other "
              "flat lines have no published part-time rule. Check the slip")
    if len(args.gmul) > 2 or (len(args.gmul) == 2 and args.fixed):
        _warn(f"{len(args.gmul)} role gmulim given{' plus a flat line' if args.fixed else ''}. "
              f"A teacher may hold at most two role gmulim (the Oz gmul tafkid "
              f"beit-sifri counts as one); gmul hishtalmut is not one of them and "
              f"belongs in --gmul-scaled")

    result = compute(combined_base=base, gmuls=gmuls, position=position,
                     fixed=fixed, fixed_prorated=fixed_prorated)
    print(render(result))
    if args.illustrative_seniority is not None:
        print(render_seniority_approx(args.illustrative_seniority))


if __name__ == "__main__":
    main()
