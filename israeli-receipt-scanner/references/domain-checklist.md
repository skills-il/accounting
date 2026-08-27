# Domain Checklist: Israeli Receipt / Tax-Invoice Scanning for Input-VAT (מס תשומות)

Scope of this skill: digitize Israeli receipts and tax invoices so a bookkeeper can (a) record the expense and (b) decide whether the input VAT is deductible and correctly claimable. The bar for "correct" is the input-VAT claim, not just data capture.

## Must cover (a wrong/missing item here can produce an over-claimed or rejected input-VAT deduction)

1. **Document-type classification drives deductibility**, only a חשבונית מס (or חשבונית מס/קבלה) supports input VAT; a קבלה, a חשבונית עסקה (proforma), and any osek-patur document do not. Source: Kol Zchut, הוצאת חשבונית מס, חשבונית עסקה וקבלה, https://www.kolzchut.org.il/he/הוצאת_חשבונית_מס,_חשבונית_עסקה_וקבלה
2. **Supplier osek number captured and 9-digit-validated**, input VAT is deductible only against a tax invoice issued by a registered osek murshe; the supplier's 9-digit מספר עוסק must be on the invoice. Source: Kol Zchut, מס תשומות, https://www.kolzchut.org.il/he/מס_תשומות
3. **osek-patur supplier flagged as carrying NO VAT**, an osek-patur issues no tax invoice and charges no VAT, so there is nothing to deduct; any VAT "extracted" from such a document is an error. Source: Kol Zchut, עוסק פטור, https://www.kolzchut.org.il/he/עוסק_פטור
4. **Allocation number (מספר הקצאה) captured and threshold-checked**, from 1 Jan 2026 input VAT is disallowed without an allocation number on tax invoices above the threshold (NIS 10,000 net Jan 2026; NIS 5,000 net from 1 Jun 2026; NIS 20,000 in 2025). Source: ACI, חובת מספר הקצאה בניכוי מס תשומות מ-2026, https://aci.org.il/knowledge/allocation-number-input-tax-2026/ ; Lishkat HaMischar T"A, https://www.chamber.org.il/serviceslobby/finance/1429/162557/
5. **Invoice must be issued in the BUYER's name**, but with two qualifications the skill must state. The buyer-registration-number requirement is section 47(ב)(1) of the VAT Law, which empowers the Director to permit its omission for classes of dealers or transactions; it is NOT an amount threshold in the VAT Regulations, which contain no invoice-particulars provision at all (those live in the Director's bookkeeping directives). And תקנה 12ג lets the Director allow a deduction on an invoice NOT in the dealer's name for telephone, water, gas, electricity or like expenses, so a utility bill in a landlord's name must be needs_review rather than a hard denial. (vat-reg-12g-not-in-dealer-name)
6. **VAT rate / arithmetic correctness**, standard VAT is 18% since 1 Jan 2025; total must equal net + VAT within rounding tolerance, else flag. Source: Hebrew Wikipedia VAT (Israel), rate table set by Finance Minister order, https://he.wikipedia.org/wiki/%D7%9E%D7%A1_%D7%A2%D7%A8%D7%9A_%D7%9E%D7%95%D7%A1%D7%A3_(%D7%99%D7%A9%D7%A8%D7%90%D7%9C)

## Should cover (improves correctness; absence will not by itself produce a wrong claim)

1. **Hosting and entertainment (אירוח) input VAT is an ABSOLUTE bar, not a soft rule.** תקנה 16: no deduction for hosting expenses, with the single exception of hosting a person from abroad. This must sit in the deductibility decision path as a hard-false trigger, not merely in an example. Also carry תקנה 15א (employee benefits: meals, housing, gifts, entertainment), deductible only where the input was sold or supplied to the employee and reported as a taxable transaction. (vat-reg-16-hosting-bar, vat-reg-15a-employee-benefits)
2. **Mixed-use partial deduction is תקנה 18(ב), a GENERAL default and not a vehicle rule.** Where the Director has fixed the non-business proportion that determination governs as an assessment; otherwise two-thirds where use is mainly for the business and a quarter where mainly not. A boolean deductible flag cannot carry those outcomes, so the record must also carry a fraction and the provision relied on. (vat-reg-18b-mixed-use-default)
3. **Separate the PURCHASE of a private car from its RUNNING COSTS.** תקנה 14(א) bars input VAT on the sale or import of a private car to a dealer outright, with תקנה 14(ב) carving out a vehicle dealer and vehicles used exclusively for driving instruction, rental, passenger transport or organised tours. Running costs including fuel are a תקנה 18(ב) mixed-use question, not a vehicle rule. A commercial vehicle outside the private-car definition is not caught by תקנה 14 at all. A one-outcome rendering is a coverage gap. (vat-reg-14a-private-car-no-deduction, vat-reg-14b-carveouts, vat-reg-18b-mixed-use-default)
4. **6-month deduction deadline**, input VAT must be claimed within 6 months of invoice issue; capture invoice date so stale invoices can be flagged. Source: Kol Zchut, מס תשומות, https://www.kolzchut.org.il/he/מס_תשומות
5. **Date-aware "current" threshold selection**, the allocation threshold depends on the invoice date, not today's date; the tool must pick the band by the invoice's own date. Source: ACI, https://aci.org.il/knowledge/allocation-number-input-tax-2026/
6. **Foreign-vendor receipts are not Israeli tax invoices**, AWS/Apple/Google etc. carry no Israeli VAT; deduction only via reverse-charge self-report, never as a normal input-VAT line. Source: Kol Zchut, מס תשומות, https://www.kolzchut.org.il/he/מס_תשומות
7. **Osek-number check digit**, 9-digit osek/H.P. numbers carry a check digit; validate to catch OCR errors. Source: lookuptax Israel TIN guide, https://lookuptax.com/docs/tax-identification-number/israel-tax-id-guide

## Out of scope

- Bank-statement reconciliation, matching receipts to bank/credit lines (explicitly excluded in description).
- Handwritten receipts without printed text.
- Filing/transmitting the periodic מע"מ return to the ITA (the tool prepares data, it does not file).
- Income-tax expense deductibility (a separate question from input-VAT deductibility).
- Validating allocation numbers against the ITA's live SHAAM service (the tool reads the printed number; it does not call the API).

## Authoritative sources

- Israel Tax Authority, https://www.gov.il/he/departments/israel_tax_authority
- Kol Zchut, מס תשומות, https://www.kolzchut.org.il/he/מס_תשומות
- Kol Zchut, הוצאת חשבונית מס, חשבונית עסקה וקבלה, https://www.kolzchut.org.il/he/הוצאת_חשבונית_מס,_חשבונית_עסקה_וקבלה
- Kol Zchut, עוסק פטור, https://www.kolzchut.org.il/he/עוסק_פטור
- ACI, מספר הקצאה בניכוי מס תשומות 2026, https://aci.org.il/knowledge/allocation-number-input-tax-2026/
- Takanot Ma"M 1976 (invoice fields), https://www.nevo.co.il/law_html/law01/271_005.htm
- Hebrew Wikipedia, מס ערך מוסף (ישראל), full rate-by-date table, https://he.wikipedia.org/wiki/%D7%9E%D7%A1_%D7%A2%D7%A8%D7%9A_%D7%9E%D7%95%D7%A1%D7%A3_(%D7%99%D7%A9%D7%A8%D7%90%D7%9C)


## Added 2026-08-27 (v1.5.0)

- [x] Six-month deduction window, section 38(א) of the VAT Law. A retroactively obtained allocation number does not restart it (section 47(א2)(4)). Load-bearing for a shoebox-digitising tool. (vat-38a-six-month-window)
- [x] The cash-law consequence is statutory: section 38(א2) disallows input VAT where a section 9 penalty was imposed, with an escape if the dealer proves tax was duly paid. Cash caps are 6,000 NIS or 10% of the transaction, whichever is lower, with a business; 15,000 between non-businesses; 50,000 for a private vehicle sale. (vat-38a2-cash-law-disallowance, cash-law-caps-2022)
- [x] Zero-rated transactions are exempt from the allocation requirement, section 47(א2)(1). (vat-47a2-zero-rate-carveout)
- [x] A missing allocation number disallows the BUYER's deduction and does NOT invalidate the invoice. Invalidity is section 50. The seller need only request a number at the buyer's demand, and an empty field may mean allocation was refused under section 47(א2)(3). (vat-38a1-allocation-disallows-deduction, vat-50-invalid-document-is-separate, vat-47a2-3-refusal)
- [x] Osek patur turnover ceiling, NIS 122,833, section 1 of the VAT Law. (vat-osek-patur-ceiling)
- [ ] Out of scope (explicit), reviewed 2026-08-27: document-type numeric codes. Two live numbering systems disagree (SHAAM has 340 for קבלה and 400 for תעודת חיוב; a major vendor API uses 400 for קבלה), so a bare code would be misread. The skill names documents instead.
- [ ] UNRESOLVED, reviewed 2026-08-27: the amount above which a tax invoice must carry the buyer's registration number. It is set in the Director's bookkeeping directives, not in the law or the regulations (the phrase סכום קטן appears zero times in both), and no openly readable figure could be sourced. The skill names the threshold without a figure. Do NOT let a future cycle fill it in with a guess.
- [ ] NOT APPLICABLE, reviewed 2026-08-27: תקנה 18(ג), the self-use full-deduction election. The consolidated regulations mark it (בוטלה), repealed with effect from 1.4.1982; its text survives only inside the amendment-history apparatus. Do not reinstate it.
- [ ] CONFIRMED ABSENT, reviewed 2026-08-27: there is no 2027 allocation threshold. NIS 5,000 is the standing figure in section 38(א1); 25,000 and 10,000 appear zero times in the consolidated statute and 20,000 only in an unrelated criminal fine. The phase-in is complete.
