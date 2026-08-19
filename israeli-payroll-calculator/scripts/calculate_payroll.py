#!/usr/bin/env python3
"""Calculate Israeli payroll: gross to net salary with all deductions.

Computes income tax (progressive brackets), Bituach Leumi (National Insurance),
health tax, and pension contributions based on 2026 Israeli rates. Supports
shovi rechev (company-car use value) as taxable imputed income.

Usage:
    python scripts/calculate_payroll.py --gross 20000
    python scripts/calculate_payroll.py --gross 20000 --credits 2.75 --pension
    python scripts/calculate_payroll.py --gross 22000 --shovi-rechev 3500
    python scripts/calculate_payroll.py --gross 15000 --employer-cost
    python scripts/calculate_payroll.py --example
"""

import sys
import argparse
from dataclasses import dataclass


# 2026 Israeli Income Tax Brackets (monthly).
# Updated per Amendment 288 (published 31.3.2026, retroactive to 1.1.2026).
# Brackets 3-5 widened: 20% now up to 19,000; 31% now 19,001-25,100; 35% from 25,101.
TAX_BRACKETS = [
    (7010, 0.10),
    (10060, 0.14),
    (19000, 0.20),
    (25100, 0.31),
    (46690, 0.35),
    (60130, 0.47),
    (float("inf"), 0.50),
]

# Tax credit point value (monthly, 2026)
CREDIT_POINT_VALUE = 242  # NIS per month

# Pension tax credit (Zikui Gemel, Section 45a), 2026
PENSION_CREDIT_RATE = 0.35              # 35% credit on eligible pension contribution
PENSION_CREDIT_SALARY_CEILING = 9700    # NIS/month insured-salary ceiling
PENSION_CREDIT_CONTRIBUTION_RATE = 0.07  # up to 7% of insured salary qualifies

# Bituach Leumi (National Insurance) rates for employees (2026)
# Per Amendment 252 (effective 1.1.2026): reduced-tier rates raised,
# reduced-tier threshold now 7,703 (a separately-set BTL figure for 2026, not a plain 60% of the average wage).
NI_REDUCED_CEILING = 7703       # NIS/month (reduced tier threshold, 2026)
NI_FULL_CEILING = 51910         # NIS/month (max insurable salary, 2026)

# Health-tax rates. These are the same for every category that pays health tax
# at all (the official rate table publishes them once, in its headline table).
HEALTH_REDUCED_RATE = 0.0323    # 3.23% employee health (was 3.10% in 2025)
HEALTH_FULL_RATE = 0.0517       # 5.17% employee health (was 5.00% in 2025)

# ---------------------------------------------------------------------------
# Employee / employer rates BY INSURANCE CATEGORY (Bituach Leumi form-102 table)
# ---------------------------------------------------------------------------
# The employee deduction is NOT one number. It depends on age, old-age-pension
# status, controlling-shareholder status, residency history and a few special
# statuses. Applying the standard 4.27% / 12.17% to a minor, a pensioner, or an
# owner-director over-charges them, in the minor/pensioner case by the entire
# deduction. See references/bituach-leumi-rates.md for the same table in prose.
#
# `employee_reduced` / `employee_full` are the TOTAL employee rates published by
# Bituach Leumi (NI + health combined) - those totals are the sourced figures.
# The NI-only component is DERIVED here by subtracting the health rate, which
# the table itself confirms at two independent points (standard 4.27 - 3.23 =
# 1.04 and 12.17 - 5.17 = 7.00, both equal to the published NI rates; and the
# controlling-shareholder derivation 4.25 - 3.23 = 1.02 / 11.96 - 5.17 = 6.79
# reproduces the NI rates published for the treaty-resident shareholder row).
#
# Source: btl.gov.il employee rate table (2026 values, effective 01.01.2026).

@dataclass(frozen=True)
class NiCategory:
    """One row of the official Bituach Leumi employee rate table."""
    label: str
    employee_reduced: float   # total employee rate, reduced tier (NI + health)
    employee_full: float      # total employee rate, full tier (NI + health)
    employer_reduced: float
    employer_full: float
    pays_health: bool = True  # False = National Insurance only, no health tax

    @property
    def health_reduced(self) -> float:
        return HEALTH_REDUCED_RATE if self.pays_health and self.employee_reduced else 0.0

    @property
    def health_full(self) -> float:
        return HEALTH_FULL_RATE if self.pays_health and self.employee_full else 0.0

    @property
    def ni_reduced(self) -> float:
        return round(self.employee_reduced - self.health_reduced, 6)

    @property
    def ni_full(self) -> float:
        return round(self.employee_full - self.health_full, 6)


NI_CATEGORIES: dict[str, NiCategory] = {
    "standard": NiCategory(
        "Israeli resident aged 18 to retirement age (form-102 column 1)",
        0.0427, 0.1217, 0.0451, 0.0760),
    "controlling-shareholder": NiCategory(
        "Controlling shareholder in a close company, 18 to retirement age (column 2)",
        0.0425, 0.1196, 0.0446, 0.0738),
    "under-18": NiCategory(
        "Under 18 (employer pays its share only)",
        0.0, 0.0, 0.0061, 0.0212),
    "under-18-shareholder": NiCategory(
        "Under 18, controlling shareholder in a close company",
        0.0, 0.0, 0.0060, 0.0206),
    "old-age-pension": NiCategory(
        "Receiving an old-age pension (kitzbat ezrach vatik), any age",
        0.0, 0.0, 0.0061, 0.0212),
    "old-age-pension-shareholder": NiCategory(
        "Receiving an old-age pension, controlling shareholder in a close company",
        0.0, 0.0, 0.0060, 0.0206),
    "age-67-70-no-pension": NiCategory(
        "Women and men aged 67 to 70 who are NOT receiving an old-age pension",
        0.0393, 0.1003, 0.0413, 0.0696),
    "age-67-70-no-pension-shareholder": NiCategory(
        "Women and men aged 67 to 70 not receiving an old-age pension, controlling shareholder",
        0.0393, 0.1003, 0.0412, 0.0690),
    "woman-retirement-to-67-no-pension": NiCategory(
        "Woman between her own retirement age and the men's retirement age (67), "
        "not receiving an old-age pension",
        0.0395, 0.1024, 0.0417, 0.0712),
    "new-resident-over-62-under-retirement": NiCategory(
        "Became an Israeli resident for the first time after age 62, below retirement age",
        0.0360, 0.0745, 0.0104, 0.0295),
    "new-resident-over-62-woman-to-67": NiCategory(
        "Woman between her retirement age and the men's retirement age, "
        "first became an Israeli resident after age 62",
        0.0328, 0.0552, 0.0070, 0.0247),
    "new-resident-over-62-67-to-70": NiCategory(
        "Man or woman between the men's retirement age and 70, "
        "first became an Israeli resident after age 62",
        0.0326, 0.0531, 0.0066, 0.0231),
    "new-resident-over-62-over-70": NiCategory(
        "Over 70 (old-age-pension eligibility age), first became an Israeli resident after age 62",
        0.0323, 0.0517, 0.0061, 0.0212),
    "new-resident-over-62-over-70-shareholder": NiCategory(
        "Over 70, first became an Israeli resident after age 62, controlling shareholder",
        0.0323, 0.0517, 0.0060, 0.0206),
    "disability-pension": NiCategory(
        "Receiving a work-injury or general-disability pension, with an annual "
        "confirmation from Bituach Leumi",
        0.0323, 0.0517, 0.0061, 0.0212),
    "disability-pension-shareholder": NiCategory(
        "Receiving a work-injury or general-disability pension with an annual "
        "confirmation, controlling shareholder",
        0.0323, 0.0517, 0.0060, 0.0206),
    "soldier-organ-donor-treaty-resident": NiCategory(
        "Soldier in regular service, organ donor, or foreign resident from a "
        "social-security treaty country (National Insurance only, no health tax)",
        0.0104, 0.0700, 0.0451, 0.0760, pays_health=False),
    "soldier-organ-donor-treaty-resident-shareholder": NiCategory(
        "Soldier in regular service, organ donor, or treaty-country foreign resident, "
        "controlling shareholder (National Insurance only, no health tax)",
        0.0102, 0.0679, 0.0446, 0.0738, pays_health=False),
}

DEFAULT_NI_CATEGORY = "standard"


def get_ni_category(name: str) -> NiCategory:
    """Look up an insurance category, failing loudly on an unknown one."""
    try:
        return NI_CATEGORIES[name]
    except KeyError:
        raise SystemExit(
            f"Unknown --ni-category {name!r}.\n"
            "Run with --list-ni-categories to see the full official table."
        )


# Backwards-compatible aliases for the standard category (column 1 of the table).
NI_REDUCED_RATE = NI_CATEGORIES["standard"].ni_reduced      # 1.04%
NI_FULL_RATE = NI_CATEGORIES["standard"].ni_full            # 7.00%
EMPLOYER_NI_REDUCED = NI_CATEGORIES["standard"].employer_reduced  # 4.51%
EMPLOYER_NI_FULL = NI_CATEGORIES["standard"].employer_full        # 7.60%

# Pension rates (mandatory since 2017)
PENSION_EMPLOYEE = 0.06         # 6% employee
PENSION_EMPLOYER = 0.065        # 6.5% employer
PENSION_SEVERANCE = 0.06        # 6% employer severance (pitzuim)


@dataclass
class PayrollResult:
    """Complete payroll calculation result."""
    gross_salary: float
    shovi_rechev: float
    taxable_gross: float  # gross + shovi_rechev (base for income tax and NI)
    income_tax: float
    pension_credit: float  # Section 45a pension tax credit (already netted in income_tax)
    bituach_leumi: float
    health_tax: float
    pension_employee: float
    net_salary: float
    ni_category: str = DEFAULT_NI_CATEGORY
    # Employer costs
    employer_ni: float = 0.0
    employer_pension: float = 0.0
    employer_severance: float = 0.0
    total_employer_cost: float = 0.0


def calculate_pension_credit(
    insured_salary: float, employee_contribution: float
) -> float:
    """Calculate the Section 45a pension tax credit (zikui gemel).

    The employee gets a 35% tax credit on their pension contribution, up to
    a contribution ceiling of 7% of the insured salary, where the insured
    salary itself is capped at 9,700 NIS/month (2026).

    Args:
        insured_salary: The pension-insurable salary (cash gross, excludes shovi rechev).
        employee_contribution: The employee's actual monthly pension contribution.

    Returns:
        The tax credit amount in NIS/month. Max ~237.65 NIS/month in 2026.
    """
    capped_salary = min(insured_salary, PENSION_CREDIT_SALARY_CEILING)
    max_qualifying = capped_salary * PENSION_CREDIT_CONTRIBUTION_RATE
    eligible = min(employee_contribution, max_qualifying)
    return round(eligible * PENSION_CREDIT_RATE, 2)


def calculate_income_tax(
    taxable_monthly: float,
    credit_points: float = 2.25,
    pension_credit: float = 0.0,
) -> float:
    """Calculate monthly income tax using progressive brackets.

    Args:
        taxable_monthly: Monthly taxable income (gross salary + shovi_rechev + other imputed income).
        credit_points: Number of tax credit points (nekudot zikui).
        pension_credit: Section 45a pension tax credit in NIS/month (see calculate_pension_credit).

    Returns:
        Monthly income tax amount in NIS.
    """
    tax = 0.0
    prev_ceiling = 0

    for ceiling, rate in TAX_BRACKETS:
        if taxable_monthly <= prev_ceiling:
            break
        taxable = min(taxable_monthly, ceiling) - prev_ceiling
        tax += taxable * rate
        prev_ceiling = ceiling

    # Subtract credit points value and pension credit. Tax cannot go negative.
    credit_value = credit_points * CREDIT_POINT_VALUE
    tax = max(0, tax - credit_value - pension_credit)

    return round(tax, 2)


def calculate_bituach_leumi(
    taxable_monthly: float, category: NiCategory | None = None
) -> tuple[float, float]:
    """Calculate employee National Insurance and Health Tax.

    NI and health tax apply to gross + shovi_rechev, capped at the max
    insurable salary ceiling. The RATE depends on the employee's insurance
    category (age, old-age-pension status, controlling-shareholder status,
    residency history), not just on the salary: see NI_CATEGORIES.

    Args:
        taxable_monthly: Monthly taxable income subject to NI (gross + shovi_rechev).
        category: Insurance category row. Defaults to the standard employee.

    Returns:
        Tuple of (national_insurance, health_tax) in NIS.
    """
    cat = category or NI_CATEGORIES[DEFAULT_NI_CATEGORY]
    insurable = min(taxable_monthly, NI_FULL_CEILING)

    # Reduced bracket
    reduced_portion = min(insurable, NI_REDUCED_CEILING)
    ni = reduced_portion * cat.ni_reduced
    health = reduced_portion * cat.health_reduced

    # Full bracket
    if insurable > NI_REDUCED_CEILING:
        full_portion = insurable - NI_REDUCED_CEILING
        ni += full_portion * cat.ni_full
        health += full_portion * cat.health_full

    return round(ni, 2), round(health, 2)


def calculate_employer_ni(
    taxable_monthly: float, category: NiCategory | None = None
) -> float:
    """Calculate employer NI contribution. Applies to gross + shovi_rechev.

    Health tax is employee-only in Israel, so there is no employer health
    component. The employer rate also varies by the employee's insurance
    category: for a minor or a pensioner the employee pays nothing but the
    employer still pays its reduced 0.61% / 2.12%.

    Args:
        taxable_monthly: Monthly income subject to NI (gross + shovi_rechev).
        category: Insurance category row. Defaults to the standard employee.

    Returns:
        Employer NI amount in NIS.
    """
    cat = category or NI_CATEGORIES[DEFAULT_NI_CATEGORY]
    insurable = min(taxable_monthly, NI_FULL_CEILING)

    reduced_portion = min(insurable, NI_REDUCED_CEILING)
    ni = reduced_portion * cat.employer_reduced

    if insurable > NI_REDUCED_CEILING:
        full_portion = insurable - NI_REDUCED_CEILING
        ni += full_portion * cat.employer_full

    return round(ni, 2)


def calculate_payroll(
    gross_salary: float,
    credit_points: float = 2.25,
    has_pension: bool = True,
    calc_employer: bool = False,
    shovi_rechev: float = 0.0,
    ni_category: str = DEFAULT_NI_CATEGORY,
) -> PayrollResult:
    """Calculate complete payroll breakdown.

    Args:
        gross_salary: Monthly gross salary in NIS (cash).
        credit_points: Tax credit points (default 2.25 for male resident).
        has_pension: Whether pension deductions apply.
        calc_employer: Whether to calculate employer cost.
        shovi_rechev: Company-car use value (monthly, NIS). Added to taxable
            gross for income tax and NI; NOT subject to pension. Employee does
            NOT receive this in cash.
        ni_category: Bituach Leumi insurance category key (see NI_CATEGORIES).
            Defaults to the standard employee aged 18 to retirement. Getting
            this wrong is a material error for minors, pensioners and
            owner-directors.

    Returns:
        PayrollResult with all deduction details.
    """
    cat = get_ni_category(ni_category)
    taxable_gross = gross_salary + shovi_rechev

    # Pension contributions apply to the pension-insurable salary, which does
    # NOT include shovi_rechev. We use gross_salary as the base here.
    pension_employee = round(gross_salary * PENSION_EMPLOYEE, 2) if has_pension else 0.0

    # Section 45a pension tax credit (zikui gemel): 35% of eligible contribution.
    pension_credit = (
        calculate_pension_credit(gross_salary, pension_employee) if has_pension else 0.0
    )

    income_tax = calculate_income_tax(taxable_gross, credit_points, pension_credit)
    ni, health = calculate_bituach_leumi(taxable_gross, cat)

    # Net cash = gross cash salary minus all deductions. The employee never
    # receives shovi_rechev as cash, so it doesn't appear as an addend here.
    net_salary = round(
        gross_salary - income_tax - ni - health - pension_employee, 2
    )

    result = PayrollResult(
        gross_salary=gross_salary,
        shovi_rechev=shovi_rechev,
        taxable_gross=taxable_gross,
        income_tax=income_tax,
        pension_credit=pension_credit,
        bituach_leumi=ni,
        health_tax=health,
        pension_employee=pension_employee,
        net_salary=net_salary,
        ni_category=ni_category,
    )

    if calc_employer:
        emp_ni = calculate_employer_ni(taxable_gross, cat)
        emp_pension = round(gross_salary * PENSION_EMPLOYER, 2) if has_pension else 0.0
        emp_severance = round(gross_salary * PENSION_SEVERANCE, 2) if has_pension else 0.0

        result.employer_ni = emp_ni
        result.employer_pension = emp_pension
        result.employer_severance = emp_severance
        result.total_employer_cost = round(
            gross_salary + emp_ni + emp_pension + emp_severance, 2
        )

    return result


def format_payslip(result: PayrollResult, show_employer: bool = False) -> str:
    """Format payroll result as a readable payslip."""
    lines = [
        "=== Israeli Payroll Calculation (Tlush Maskoret) ===",
        "",
        f"  Gross Salary (Bruto):      {result.gross_salary:>10,.2f} NIS",
    ]

    cat = NI_CATEGORIES[result.ni_category]
    lines.append(f"  NI category: {result.ni_category} ({cat.label})")

    if result.shovi_rechev > 0:
        lines.extend([
            f"  Shovi Rechev (car value):  {result.shovi_rechev:>10,.2f} NIS  (taxable, not cash)",
            f"  Taxable Gross:             {result.taxable_gross:>10,.2f} NIS",
        ])

    lines.append(f"  Income Tax (Mas Hachnasa): -{result.income_tax:>10,.2f} NIS")
    if result.pension_credit > 0:
        lines.append(
            f"    (incl. -{result.pension_credit:.2f} pension credit, sec. 45a)"
        )
    lines.extend([
        f"  Bituach Leumi (NI):        -{result.bituach_leumi:>10,.2f} NIS"
        f"   ({cat.ni_reduced:.2%} / {cat.ni_full:.2%})",
        f"  Health Tax (Mas Briut):    -{result.health_tax:>10,.2f} NIS"
        f"   ({cat.health_reduced:.2%} / {cat.health_full:.2%})",
        f"  Pension (Employee 6%):     -{result.pension_employee:>10,.2f} NIS",
        f"  {'-' * 42}",
        f"  Net Salary (Neto):          {result.net_salary:>10,.2f} NIS",
    ])

    if show_employer and result.total_employer_cost > 0:
        lines.extend([
            "",
            "  === Employer Cost ===",
            f"  Gross Salary:               {result.gross_salary:>10,.2f} NIS",
            f"  Employer NI:               +{result.employer_ni:>10,.2f} NIS"
            f"   ({cat.employer_reduced:.2%} / {cat.employer_full:.2%})",
            f"  Employer Pension (6.5%):   +{result.employer_pension:>10,.2f} NIS",
            f"  Employer Severance (6%):   +{result.employer_severance:>10,.2f} NIS",
            f"  {'-' * 42}",
            f"  Total Employer Cost:        {result.total_employer_cost:>10,.2f} NIS",
        ])

    lines.extend([
        "",
        "NOTE: Estimate based on 2026 rates. Consult a certified",
        "      accountant (roeh cheshbon) for exact figures.",
    ])
    return "\n".join(lines)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Calculate Israeli payroll (gross to net)"
    )
    parser.add_argument("--gross", type=float, help="Monthly gross salary in NIS (cash)")
    parser.add_argument(
        "--credits", type=float, default=2.25,
        help="Tax credit points (default: 2.25 for male resident)"
    )
    parser.add_argument(
        "--no-pension", action="store_true", help="Exclude pension deductions"
    )
    parser.add_argument(
        "--shovi-rechev", type=float, default=0.0,
        help="Shovi rechev (company car use value, monthly NIS). "
             "Taxable imputed income: adds to income-tax and NI base, "
             "not to pension base, and not received as cash."
    )
    parser.add_argument(
        "--ni-category", default=DEFAULT_NI_CATEGORY,
        choices=sorted(NI_CATEGORIES),
        help="Bituach Leumi insurance category. Default: standard (Israeli "
             "resident aged 18 to retirement). Use --list-ni-categories to see "
             "the full official table with its rates."
    )
    parser.add_argument(
        "--list-ni-categories", action="store_true",
        help="Print the official Bituach Leumi employee rate table and exit"
    )
    parser.add_argument(
        "--employer-cost", action="store_true",
        help="Include employer cost calculation"
    )
    parser.add_argument(
        "--example", action="store_true", help="Show example calculation"
    )

    args = parser.parse_args()

    if args.list_ni_categories:
        print("Bituach Leumi employee rate table (2026, btl.gov.il)")
        print(f"Reduced tier: up to {NI_REDUCED_CEILING:,} NIS/month. "
              f"Full tier: up to {NI_FULL_CEILING:,} NIS/month.\n")
        print(f"{'--ni-category':<48} {'employee':>17} {'employer':>17}")
        print(f"{'':<48} {'reduced / full':>17} {'reduced / full':>17}")
        for key, cat in NI_CATEGORIES.items():
            emp = f"{cat.employee_reduced:.2%} / {cat.employee_full:.2%}"
            er = f"{cat.employer_reduced:.2%} / {cat.employer_full:.2%}"
            print(f"{key:<48} {emp:>17} {er:>17}")
            print(f"    {cat.label}")
        return

    if args.example:
        print("Example: 22,000 NIS gross + 3,500 NIS shovi rechev, male (2.25 credits), with pension")
        print()
        result = calculate_payroll(22000, 2.25, True, True, shovi_rechev=3500)
        print(format_payslip(result, show_employer=True))
        return

    if args.gross is None:
        parser.print_help()
        sys.exit(1)

    result = calculate_payroll(
        args.gross,
        args.credits,
        not args.no_pension,
        args.employer_cost,
        shovi_rechev=args.shovi_rechev,
        ni_category=args.ni_category,
    )
    print(format_payslip(result, show_employer=args.employer_cost))


if __name__ == "__main__":
    main()
