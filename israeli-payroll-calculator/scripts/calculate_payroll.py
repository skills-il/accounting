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


# 2026 Israeli Income Tax Brackets (monthly). Frozen 2025-2027 by legislation.
TAX_BRACKETS = [
    (7010, 0.10),
    (10060, 0.14),
    (16150, 0.20),
    (22440, 0.31),
    (46690, 0.35),
    (60130, 0.47),
    (float("inf"), 0.50),
]

# Tax credit point value (monthly, 2026)
CREDIT_POINT_VALUE = 242  # NIS per month

# Bituach Leumi (National Insurance) rates for employees (2026)
NI_REDUCED_CEILING = 7522       # NIS/month (reduced tier threshold)
NI_FULL_CEILING = 51910         # NIS/month (max insurable salary, 2026)
NI_REDUCED_RATE = 0.004         # 0.4% employee NI
NI_FULL_RATE = 0.07             # 7.0% employee NI
HEALTH_REDUCED_RATE = 0.031     # 3.1% employee health
HEALTH_FULL_RATE = 0.05         # 5.0% employee health

# Employer rates (2026)
EMPLOYER_NI_REDUCED = 0.0345    # 3.45% employer NI (reduced bracket)
EMPLOYER_NI_FULL = 0.076        # 7.6% employer NI (full bracket)

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
    bituach_leumi: float
    health_tax: float
    pension_employee: float
    net_salary: float
    # Employer costs
    employer_ni: float = 0.0
    employer_pension: float = 0.0
    employer_severance: float = 0.0
    total_employer_cost: float = 0.0


def calculate_income_tax(taxable_monthly: float, credit_points: float = 2.25) -> float:
    """Calculate monthly income tax using progressive brackets.

    Args:
        taxable_monthly: Monthly taxable income (gross salary + shovi_rechev + other imputed income).
        credit_points: Number of tax credit points (nekudot zikui).

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

    # Apply credit points (cannot produce negative tax)
    credit_value = credit_points * CREDIT_POINT_VALUE
    tax = max(0, tax - credit_value)

    return round(tax, 2)


def calculate_bituach_leumi(taxable_monthly: float) -> tuple[float, float]:
    """Calculate employee National Insurance and Health Tax.

    NI and health tax apply to gross + shovi_rechev, capped at the max
    insurable salary ceiling.

    Args:
        taxable_monthly: Monthly taxable income subject to NI (gross + shovi_rechev).

    Returns:
        Tuple of (national_insurance, health_tax) in NIS.
    """
    insurable = min(taxable_monthly, NI_FULL_CEILING)

    # Reduced bracket
    reduced_portion = min(insurable, NI_REDUCED_CEILING)
    ni = reduced_portion * NI_REDUCED_RATE
    health = reduced_portion * HEALTH_REDUCED_RATE

    # Full bracket
    if insurable > NI_REDUCED_CEILING:
        full_portion = insurable - NI_REDUCED_CEILING
        ni += full_portion * NI_FULL_RATE
        health += full_portion * HEALTH_FULL_RATE

    return round(ni, 2), round(health, 2)


def calculate_employer_ni(taxable_monthly: float) -> float:
    """Calculate employer NI contribution. Applies to gross + shovi_rechev.

    Health tax is employee-only in Israel, so there is no employer health
    component.

    Args:
        taxable_monthly: Monthly income subject to NI (gross + shovi_rechev).

    Returns:
        Employer NI amount in NIS.
    """
    insurable = min(taxable_monthly, NI_FULL_CEILING)

    reduced_portion = min(insurable, NI_REDUCED_CEILING)
    ni = reduced_portion * EMPLOYER_NI_REDUCED

    if insurable > NI_REDUCED_CEILING:
        full_portion = insurable - NI_REDUCED_CEILING
        ni += full_portion * EMPLOYER_NI_FULL

    return round(ni, 2)


def calculate_payroll(
    gross_salary: float,
    credit_points: float = 2.25,
    has_pension: bool = True,
    calc_employer: bool = False,
    shovi_rechev: float = 0.0,
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

    Returns:
        PayrollResult with all deduction details.
    """
    taxable_gross = gross_salary + shovi_rechev

    income_tax = calculate_income_tax(taxable_gross, credit_points)
    ni, health = calculate_bituach_leumi(taxable_gross)

    # Pension contributions apply to the pension-insurable salary, which does
    # NOT include shovi_rechev. We use gross_salary as the base here.
    pension_employee = round(gross_salary * PENSION_EMPLOYEE, 2) if has_pension else 0.0

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
        bituach_leumi=ni,
        health_tax=health,
        pension_employee=pension_employee,
        net_salary=net_salary,
    )

    if calc_employer:
        emp_ni = calculate_employer_ni(taxable_gross)
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

    if result.shovi_rechev > 0:
        lines.extend([
            f"  Shovi Rechev (car value):  {result.shovi_rechev:>10,.2f} NIS  (taxable, not cash)",
            f"  Taxable Gross:             {result.taxable_gross:>10,.2f} NIS",
        ])

    lines.extend([
        f"  Income Tax (Mas Hachnasa): -{result.income_tax:>10,.2f} NIS",
        f"  Bituach Leumi (NI):        -{result.bituach_leumi:>10,.2f} NIS",
        f"  Health Tax (Mas Briut):    -{result.health_tax:>10,.2f} NIS",
        f"  Pension (Employee 6%):     -{result.pension_employee:>10,.2f} NIS",
        f"  {'-' * 42}",
        f"  Net Salary (Neto):          {result.net_salary:>10,.2f} NIS",
    ])

    if show_employer and result.total_employer_cost > 0:
        lines.extend([
            "",
            "  === Employer Cost ===",
            f"  Gross Salary:               {result.gross_salary:>10,.2f} NIS",
            f"  Employer NI:               +{result.employer_ni:>10,.2f} NIS",
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
        "--employer-cost", action="store_true",
        help="Include employer cost calculation"
    )
    parser.add_argument(
        "--example", action="store_true", help="Show example calculation"
    )

    args = parser.parse_args()

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
    )
    print(format_payslip(result, show_employer=args.employer_cost))


if __name__ == "__main__":
    main()
