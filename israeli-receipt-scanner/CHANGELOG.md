# Changelog

## 1.5.0 - 2026-08-27

Grounded the VAT rules in the primary statute and closed three gaps that let the
scanner emit a deductible flag it had no right to.

- **Buying a private car is a COMPLETE bar on input VAT, not a two-thirds
  restriction.** Regulation 14(א) of the VAT Regulations disallows the tax on the
  sale of a private car to a dealer, or its import, outright. The skill applied
  the mixed-use fractions to vehicle documents generally, understating a total
  bar in the buyer's favour. Purchase and running costs are now separated, with
  regulation 14(ב)'s carve-outs stated.
- **The two-thirds and one-quarter fractions were misattributed.** They are
  regulation 18(ב)'s GENERAL default for any mixed-use input, and they apply only
  where the Director has not fixed a proportion; a determination is treated as an
  assessment and overrides them.
- **The six-month deduction window (section 38(א)) was absent.** For a tool whose
  purpose is digitizing accumulated paper, this was the most consequential
  omission: it would emit vat_deductible true on an eleven-month-old invoice. A
  retroactively obtained allocation number does not restart it (section 47(א2)(4)).
- **The cash-law consequence is now the statutory one.** Section 38(א2) disallows
  the input VAT where a section 9 penalty was imposed, with an escape if the
  dealer proves tax was duly paid, and a refund with interest if the penalty
  appeal succeeds. Added the 10%-of-transaction limb, which often binds below
  6,000, and the private-party caps.
- **Zero-rated transactions are exempt from the allocation requirement**
  (section 47(א2)(1)), so the skill no longer raises a false missing-allocation
  warning on a large zero-rated invoice.
- **Stated plainly what a missing allocation number does.** It disallows the
  BUYER's deduction; it does not make the invoice invalid. The statute expressly
  contemplates issuing an invoice with no allocated number, the seller still owes
  output tax, and invalidity is a different provision (section 50). Also added
  that the seller need only request a number at the buyer's demand, and that an
  empty field may mean allocation was refused.
- Added the osek patur turnover ceiling (NIS 122,833, section 1).

- **Hosting and entertainment is an absolute bar and was missing from the decision
  path.** Regulation 16 disallows input VAT on hosting expenses, with the single
  exception of hosting a person from abroad. It appeared only as prose in an
  example, so a restaurant tax invoice in the company's name, under the allocation
  band and inside the six-month window, satisfied every condition in the
  deductibility AND-list and would have been flagged deductible. Added as a
  hard-false trigger in both lists, alongside regulation 15א on employee benefits.
- **Regulation 12ג added**: an invoice NOT in the dealer's name may still be
  allowed by the Director for telephone, water, gas and electricity and like
  expenses, so a utility bill in a landlord's name is needs_review, not a denial.
- **The record can now carry a fraction.** Regulation 18(ב) produces two-thirds
  and one-quarter outcomes that a boolean cannot express, so `deductible_fraction`
  and `deductibility_basis` were added, and `needs_review` and `warnings` were
  added to the CSV columns, which previously dropped every caveat on export.
- Resolved a contradiction where Step 6 and Step 7 gave different answers on
  commercial-vehicle fuel; Step 6 now defers to the vehicle gate.
- Removed a stale inline `metadata:` block from the Hebrew frontmatter that still
  said version 1.3.0, against the convention that metadata lives in metadata.json.
- Refreshed references/domain-checklist.md, which still carried the pre-correction
  framing of the vehicle and mixed-use rules, and corrected its misattribution of
  the invoice-particulars requirement to the VAT Regulations, which contain no
  such provision.

Checked and NOT changed: the allocation threshold timeline (20,000 in 2025,
10,000 for January to May 2026, 5,000 from 1 June 2026) is correct, and 5,000 is
the figure in the primary statute rather than a transitional step, so there is no
2027 band to add. A finding proposing the regulation 18(ג) full-deduction
election was rejected: that subsection is marked repealed.

All notable changes to this skill are documented here.

## [1.4.0] - 2026-08-09

### Added

- נוסף פרק "הבהרה משפטית" בראש SKILL.md ו-SKILL_HE.md, המפרט מה הכלי עושה, מה הוא אינו, ולאיזה בעל מקצוע מוסמך יש לפנות.

### Changed

- התיאור נפתח כעת בהבהרה קצרה, כך שהיא נראית גם בכרטיס ובתוצאות החיפוש.
