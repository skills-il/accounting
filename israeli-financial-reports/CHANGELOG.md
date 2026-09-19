# Changelog

All notable changes to this skill are documented here.

## [1.4.2] - 2026-09-19

### Fixed
- Example 2 no longer calls company statements "ready for submission to the Registrar of Companies". A private company's statements are audited by its CPA, and its Registrar annual report generally does not attach them; the output is a draft for the auditor.
- Osek zeir: the 30% deduction replaces actual expenses (it is not "the higher of"), and in most cases also exempts the annual return.
- Allocation-number gate now lists the 2025 threshold (NIS 20,000) and applies the threshold in force on the invoice date, matching the skill's own Nov-Dec 2025 example.
- VAT cadence: added the 1,805,000 NIS reckoning amount from 1 January 2027.
- Cash flow worked example now ties to the balance sheet's change in cash (60,380.50), with a mandatory tie-out check.
- VAT summary: input VAT is the actual VAT on valid documents, with the regulatory deduction restrictions; allocation-number gate adds the 25,000 NIS first stage.
- Removed an unsourced "1.67 million NIS section 67a" parenthetical; statements are labelled unaudited and PDF export is for accountant review.
- Replaced an unverified "assets right, liabilities left" gotcha with RTL rendering guidance.

## [1.4.1] - 2026-08-11

### Fixed
- Repaired a dead Kol Zchut link in references/domain-checklist.md (the URL omitted the gershayim in דו"חות and returned 404).
- Rebuilt evidence.json snippets as contiguous verbatim quotes from the cited pages, split multi-passage entries into one entry per quote, and re-sourced the income-tax advances entry to the gov.il mikdamot service page. No figure or rule in the skill body changed.

## [1.4.0] - 2026-08-09

### Added

- נוסף פרק "הבהרה משפטית" בראש SKILL.md ו-SKILL_HE.md, המפרט מה הכלי עושה, מה הוא אינו, ולאיזה בעל מקצוע מוסמך יש לפנות.

### Changed

- התיאור נפתח כעת בהבהרה קצרה, כך שהיא נראית גם בכרטיס ובתוצאות החיפוש.
