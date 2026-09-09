#!/usr/bin/env python3
"""Work out which Israeli amuta duties a turnover triggers, plus the fee tier and report year.

Pure computation. No network access, so it runs on every host including sandboxed ones.

Every threshold carries a year. The audit threshold is index-linked and re-gazetted each February
under s.19(c)(2), so pass --audit-threshold when filing for a year other than 2026 rather than
trusting the built-in default.

Usage:
  python3 band_check.py --turnover <amount> --certificate-year 2026
  python3 band_check.py --turnover <amount> --certificate-year 2027 --section-46
  python3 band_check.py --example
"""

import argparse

# s.19(c)(1) base, adjusted to 1996. Index-linked by s.19(c)(2).
AUDIT_THRESHOLD_BY_YEAR = {
    2026: 1_380_630,  # Yalkut HaPirsumim 14348, notice dated 24.2.2026
}
BOOKKEEPING_THRESHOLD = 750_000      # Second Schedule. NOT index-linked.
INTERNAL_AUDIT_THRESHOLD = 10_000_000  # s.30a
FOREIGN_DONATION_THRESHOLD = 300_000   # s.36a
FEE_TURNOVER_THRESHOLD = 300_000

FEES_YEAR = 2026
FEES_2026 = {"reduced": 176, "early": 1338, "standard": 1777}


def report_year(certificate_year):
    """A certificate for year X is granted against the annual reports for year X-2."""
    return certificate_year - 2


def filing_deadline(certificate_year):
    """s.36(d): filed no later than 30 June of the year following the report period."""
    return "30 June %d" % (report_year(certificate_year) + 1)


def audit_threshold(year, override=None):
    """Threshold for the year whose TURNOVER is being measured, i.e. the report year.

    s.19(c) binds an amuta by reference to the amount published for the year its turnover is
    measured in, so a certificate for 2026 is decided on the 2024 turnover against the 2024
    amount. Using the certificate year's amount under-triggers, because the later figure is
    higher, and under-triggering is the direction that costs a certificate.
    """
    if override is not None:
        return override, "supplied on the command line"
    if year in AUDIT_THRESHOLD_BY_YEAR:
        return AUDIT_THRESHOLD_BY_YEAR[year], "gazetted amount for %d" % year
    return None, ("no gazetted amount recorded for %d. s.19(c)(2) requires the Minister to publish "
                  "it in Reshumot at the start of February each year. Look up the notice for %d and "
                  "pass it with --audit-threshold. Do NOT substitute another year's amount" 
                  % (year, year))


def evaluate(turnover, certificate_year, section_46=False, audit_override=None,
             first_two_years=False, filed_online_small=False):
    out = []
    ry = report_year(certificate_year)
    out.append("Certificate year:      %d" % certificate_year)
    out.append("Annual reports needed: %d  (the X minus 2 rule)" % ry)
    out.append("Statutory deadline:    %s, signed by two board members (s.36(d))"
               % filing_deadline(certificate_year))
    out.append("")
    out.append("Turnover used: %s NIS" % format(int(turnover), ","))
    out.append("")
    out.append("Duties triggered")
    out.append("  Organs: general assembly, board, audit committee (s.19(a)). Applies at any "
               "turnover, including none.")
    out.append("  Balance sheet and income/expenditure statement (s.36(a)). Applies to every amuta; "
               "only the AUDIT is banded.")

    if turnover > BOOKKEEPING_THRESHOLD:
        out.append("  Double-entry bookkeeping required (Second Schedule, above %s NIS)."
                   % format(BOOKKEEPING_THRESHOLD, ","))
    else:
        out.append("  Receipts-and-payments book is enough (Second Schedule, at or below %s NIS)."
                   % format(BOOKKEEPING_THRESHOLD, ","))

    threshold, note = audit_threshold(ry, audit_override)
    if threshold is None:
        out.append("  Audit: CANNOT DETERMINE for report year %d. %s" % (ry, note))
        known = ", ".join("%d = %s NIS" % (y, format(v, ","))
                          for y, v in sorted(AUDIT_THRESHOLD_BY_YEAR.items()))
        out.append("    Recorded amounts: %s. These are NOT comparators for another year." % known)
    elif turnover > threshold:
        out.append("  Accountant must be appointed and the report audited to the general assembly "
                   "(s.19(c)(1), s.37(a)). Threshold %s NIS, %s." % (format(threshold, ","), note))
    else:
        out.append("  No mandatory accountant on turnover (threshold %s NIS, %s). Note s.37(b): the "
                   "Registrar may still order an audit." % (format(threshold, ","), note))

    if turnover > INTERNAL_AUDIT_THRESHOLD:
        out.append("  Internal auditor required, with the audit committee's agreement (s.30a, above "
                   "%s NIS)." % format(INTERNAL_AUDIT_THRESHOLD, ","))

    if turnover > FOREIGN_DONATION_THRESHOLD:
        out.append("  If it received foreign political-entity donations, they must be stated (s.36a, "
                   "above %s NIS)." % format(FOREIGN_DONATION_THRESHOLD, ","))

    out.append("")
    if certificate_year == FEES_YEAR:
        out.append("Annual fee (%d amounts, Associations (Fees) Regulations)" % FEES_YEAR)
    else:
        out.append("Annual fee: CANNOT DETERMINE for %d. The amounts below are the %d ones, shown "
                   "only for shape. The fee is index-linked and updated once a year, so look up the "
                   "amounts for %d before quoting any of them."
                   % (certificate_year, FEES_YEAR, certificate_year))
    out.append("  The certificate application requires the fee for the PRECEDING year to be paid, "
               "including arrears from earlier years.")
    if filed_online_small and turnover > FEE_TURNOVER_THRESHOLD:
        out.append("  INPUT CONFLICT: --filed-online-small asserts turnover at or below %s NIS, but "
                   "--turnover is %s NIS. Resolve this before quoting a tier; the reduced tier is "
                   "not available on this turnover unless the amuta is in its first two years."
                   % (format(FEE_TURNOVER_THRESHOLD, ","), format(int(turnover), ",")))
    elif first_two_years or filed_online_small:
        reason = ("first two years after the year of incorporation" if first_two_years
                  else "reported online that turnover did not exceed %s NIS"
                       % format(FEE_TURNOVER_THRESHOLD, ","))
        out.append("  Reduced tier: %d NIS  (%s)" % (FEES_2026["reduced"], reason))
    elif turnover > FEE_TURNOVER_THRESHOLD:
        out.append("  %d NIS if paid up to 31.03, then %d NIS from 01.04."
                   % (FEES_2026["early"], FEES_2026["standard"]))
        out.append("  Paying the full fee BEFORE filing the online reports forfeits any refund of "
                   "the excess.")
    else:
        out.append("  Possibly the reduced tier of %d NIS, but the trigger is having FILED the "
                   "online annual reports, not turnover alone. Confirm with the Registrar."
                   % FEES_2026["reduced"])
    out.append("  The gov.il fee page is internally inconsistent about which year's turnover "
               "governs. Do not rely on a 2023 turnover test.")

    if section_46:
        out.append("")
        out.append("Section 46 digital donation reporting")
        out.append("  Mandatory since 1 January 2026 via the Trumot Israel system, for donations AND "
                   "cancellations, from the first shekel, with no minimum.")
        out.append("  The Section 46 approval is CONDITIONAL on complying (execution instruction "
                   "11/2025, s.10).")
        out.append("  Prerequisites: registration for Tax Authority digital services, and a "
                   "morshe-al appointed.")
        out.append("  The duty applies even if the amuta is exempt from issuing receipts.")
        out.append("  There is no April 2026 deadline. The date is 1 January 2026.")
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--turnover", type=float, help="annual turnover in NIS for the reported year")
    p.add_argument("--certificate-year", type=int, help="the year the certificate is sought for")
    p.add_argument("--audit-threshold", type=float, default=None,
                   help="gazetted s.19(c) amount for the filing year, if not 2026")
    p.add_argument("--section-46", action="store_true", help="the amuta holds a Section 46 approval")
    p.add_argument("--first-two-years", action="store_true",
                   help="within the first two years after the year of incorporation")
    p.add_argument("--filed-online-small", action="store_true",
                   help="filed online reports showing turnover at or below 300,000 NIS")
    p.add_argument("--example", action="store_true", help="run a worked example")
    a = p.parse_args()

    if a.example:
        demo = BOOKKEEPING_THRESHOLD + 150_000
        print("Example: turnover between the bookkeeping and audit thresholds, "
              "certificate for 2026, holds Section 46\n")
        for line in evaluate(demo, 2026, section_46=True):
            print(line)
        return
    if a.turnover is None or a.certificate_year is None:
        p.error("--turnover and --certificate-year are required (or use --example)")
    for line in evaluate(a.turnover, a.certificate_year, a.section_46, a.audit_threshold,
                         a.first_two_years, a.filed_online_small):
        print(line)


if __name__ == "__main__":
    main()
