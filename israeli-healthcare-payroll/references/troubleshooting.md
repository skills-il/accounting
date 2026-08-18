# Troubleshooting

- **"I do not know the base rate."** The skill does not carry NIS grade cells on
  purpose (they change per agreement). Read the combined cell for the exact
  grade, seniority, and dirug from the union table or the Wage Commissioner, then
  feed it into `healthcare_gross.py`.
- **"The numbers do not match my payslip."** Check the dirug (allied health is
  three separate tracks), the recognized seniority (read the combined cell, do
  not re-add seniority), whether every tosefet is included, and, for a doctor,
  whether on-call was computed in workday equivalents rather than folded into
  base. The slip also carries lines the script does not model (clothing
  allowance, havraa, legacy fold-in supplements), and the pension type
  (budgetary vs funded) and union dues shift the net.
- **"Is this net or gross?"** This skill computes GROSS. Net needs Step 4 and the
  `israeli-payroll-calculator` skill for the deduction mechanics.
- **The user is a teacher, a private-sector employee, or a home caregiver.** Route
  to `israeli-teacher-payroll`, `israeli-payroll-calculator`, or
  `foreign-caregiver-payroll`; this skill is only public-healthcare-sector pay.
