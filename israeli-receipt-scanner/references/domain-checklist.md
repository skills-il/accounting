# Domain Checklist: Israeli Receipt / Tax-Invoice Scanning for Input-VAT (מס תשומות)

Scope of this skill: digitize Israeli receipts and tax invoices so a bookkeeper can (a) record the expense and (b) decide whether the input VAT is deductible and correctly claimable. The bar for "correct" is the input-VAT claim, not just data capture.

## Must cover (a wrong/missing item here can produce an over-claimed or rejected input-VAT deduction)

1. **Document-type classification drives deductibility**, only a חשבונית מס (or חשבונית מס/קבלה) supports input VAT; a קבלה, a חשבונית עסקה (proforma), and any osek-patur document do not. Source: Kol Zchut, הוצאת חשבונית מס, חשבונית עסקה וקבלה, https://www.kolzchut.org.il/he/הוצאת_חשבונית_מס,_חשבונית_עסקה_וקבלה
2. **Supplier osek number captured and 9-digit-validated**, input VAT is deductible only against a tax invoice issued by a registered osek murshe; the supplier's 9-digit מספר עוסק must be on the invoice. Source: Kol Zchut, מס תשומות, https://www.kolzchut.org.il/he/מס_תשומות
3. **osek-patur supplier flagged as carrying NO VAT**, an osek-patur issues no tax invoice and charges no VAT, so there is nothing to deduct; any VAT "extracted" from such a document is an error. Source: Kol Zchut, עוסק פטור, https://www.kolzchut.org.il/he/עוסק_פטור
4. **Allocation number (מספר הקצאה) captured and threshold-checked**, from 1 Jan 2026 input VAT is disallowed without an allocation number on tax invoices above the threshold (NIS 10,000 net Jan 2026; NIS 5,000 net from 1 Jun 2026; NIS 20,000 in 2025). Source: ACI, חובת מספר הקצאה בניכוי מס תשומות מ-2026, https://aci.org.il/knowledge/allocation-number-input-tax-2026/ ; Lishkat HaMischar T"A, https://www.chamber.org.il/serviceslobby/finance/1429/162557/
5. **Invoice must be issued in the BUYER's name (and, above threshold, carry the buyer's osek number)**, the law allows deduction only for "חשבוניות מקוריות שהוצאו על שמו כדין"; an invoice issued to someone else / generic / no-buyer is not deductible. For invoices above the small-sum threshold the buyer's name + VAT number are mandatory invoice fields. Source: Kol Zchut, מס תשומות, https://www.kolzchut.org.il/he/מס_תשומות ; Takanot Ma"M (pratim bechashbonit), https://www.nevo.co.il/law_html/law01/271_005.htm
6. **VAT rate / arithmetic correctness**, standard VAT is 18% since 1 Jan 2025; total must equal net + VAT within rounding tolerance, else flag. Source: Sovos, https://sovos.com/regulatory-updates/vat/israel-vat-rate-increase-to-18-from-january-1-2025/

## Should cover (improves correctness; absence will not by itself produce a wrong claim)

1. **Business-meal / hosting (אירוח) input VAT generally non-deductible**, flag restaurant/hosting invoices as usually non-deductible. Source: RAF CPA, https://www.raf-cpa.com/24376
2. **Partial-deduction (two-thirds / mixed business-private) cases**, for mixed-use inputs only two-thirds (or a use-proportion) of input VAT is deductible; flag for bookkeeper rather than claiming 100%. Source: Kol Zchut, קיזוז תשלומי מע"מ של עוסק מורשה, https://www.kolzchut.org.il/he/קיזוז_תשלומי_מע%22מ_של_עוסק_מורשה_(מס_תשומות)
3. **Private-vehicle (רכב פרטי) input VAT blocked/restricted**, input VAT on passenger vehicles and related running costs is generally non-deductible; fuel at a gas station may fall under this. Source: Kol Zchut, מס תשומות (links to מדריך ניכוי מס תשומות לרכב), https://www.kolzchut.org.il/he/מס_תשומות
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
- Sovos, Israel VAT 18% from 2025, https://sovos.com/regulatory-updates/vat/israel-vat-rate-increase-to-18-from-january-1-2025/
