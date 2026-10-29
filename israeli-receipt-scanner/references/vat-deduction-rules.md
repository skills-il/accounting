# Input-VAT Deduction Rules: the Detail Behind Step 7

This file carries the statutory detail behind the decision path in SKILL.md Step 7. The
decision path itself (the AND-list and the hard bars) stays in SKILL.md; read this file when
a record lands in `decision: "review"` and the bookkeeper asks why.

Abbreviations: VAT Law = חוק מס ערך מוסף, התשל"ו-1975. VAT Regulations = תקנות מס ערך מוסף,
התשל"ו-1976. Bookkeeping Directives = הוראות מס הכנסה (ניהול פנקסי חשבונות), התשל"ג-1973.

## 1. Allocation number (מספר הקצאה)

### Bands, selected by the invoice's own date

| Invoice date | Allocation number required when the net amount (before VAT) exceeds |
|---|---|
| Up to 4 May 2024 | not required, the regime did not apply yet |
| 5 May 2024 - Dec 2024 | NIS 25,000 |
| Jan 2025 - Dec 2025 | NIS 20,000 |
| Jan 2026 - May 2026 | NIS 10,000 |
| Jun 2026 onwards (current) | NIS 5,000 |

Section 38(א1) of the VAT Law says `עולה על` (exceeds), so an invoice sitting exactly on a
band figure is outside it. NIS 5,000 is the standing figure in the statute; no later step has
been legislated. Secondary sources still quoting a 2024 committee schedule (15,000 in 2026,
10,000 in 2027) are out of date. The 25,000 figure is absent from the consolidated text of
section 38(א1), which shows only the current schedule; that absence is not evidence the band
never existed.

### Format

The Tax Authority's FAQ: the allocation number is **9 digits**, printed on the invoice
(preferably under the document number), and **random, with no check digit**. So:

- Extract it as a string. Never run a Luhn or any other checksum on it.
- If a longer string is printed where the number should be, keep it verbatim in
  `allocation_number_raw`, leave `allocation_number` null and route the record to `review`.
  No Tax Authority text read for this skill says which digits of a longer string are the
  number, so do not guess.
- A 9-digit number that is not printed under an "מספר הקצאה" label may be anything (an order
  number, a phone number). Do not promote it to an allocation number.
- The only authoritative check is the buyer's own: the number also appears in the buyer's
  personal area on the Tax Authority site. Point the bookkeeper there; this tool does not call
  the service.

### Scope

- Only a tax invoice (חשבונית מס, including חשבונית מס / קבלה) needs one. A קבלה, a חשבונית
  עסקה and a credit note do not.
- Section 47(א2)(1): zero-rated transactions are outside the mechanism. Do not warn on a large
  zero-rated or Eilat invoice.
- Section 40ב: where the Tax Authority's own systems failed, the Director may allow the
  deduction without a number.

### What a missing number costs, and how to fix it

- Section 38(א1) sits in the input-tax chapter and disallows the BUYER's deduction. It does not
  invalidate the invoice: the seller still owes output tax, and section 47(א2)(3)(ג)(2)
  contemplates an invoice issued with no allocated number. Invalidity is section 50 and missing
  allocation numbers are not in it. Say "the buyer cannot deduct", never "the invoice is
  invalid".
- Section 47(א2)(1) obliges the seller to request a number "לפי דרישת הקונה". The practical
  advice is to go back to the supplier and demand allocation, not to reject the document.
- The Tax Authority's FAQ: a number may be requested **up to one year after the invoice
  date**; if the invoice is already older than six months, it can then be claimed only after an
  extension request. Section 47(א2)(4): a number allocated later does not move the six-month
  date of section 38(א).
- Section 47(א2)(3): the Director may refuse to allocate where there is reasonable ground to
  suspect the invoice would be issued unlawfully. An empty field may mean the supplier never
  asked, or that allocation was refused; only the supplier can say which.

## 2. The six-month window and its extension

- Section 38(א) of the VAT Law: the deduction must be made "בתוך ששה חדשים מיום הוצאת
  החשבונית".
- Section 116(א): the Director may extend any time limit in the Law, "ובלבד שלא יאריך את
  המועד לניכוי מס תשומות לפי סעיף 38(א) לתקופה העולה על חמש שנים".

So past six months the invoice cannot be deducted in the ordinary course; it needs an
extension request to the Director, which is discretionary and can never reach beyond five years.
Past five years it is closed. Set `deduction_deadline` to the invoice date plus six months, and
let the bookkeeper decide which periodic return that falls in.

## 3. The buyer's registration number

Section 47(ב)(1) of the VAT Law: a tax invoice must show the tax separately "וכן מספר הרישום של
הקונה", but the Director may permit, generally or for classes of dealers or transactions, the
words "כולל מס" instead and the omission of the buyer's number. So the default is that every
tax invoice carries the buyer's number, and any small-sum exemption is a Director's permit
whose general amount is not openly published. Do not invent one.

The one published small-sum figure: under regulation 9א(ג)(1) of the VAT Bookkeeping
Regulations, a cash-register sales slip issued by a dealer to whom section 4 of the eleventh
schedule to the Directives applies is treated as a tax invoice for a **service** whose price
does not exceed NIS 309 including VAT. That covers services from those dealers only. It is not
a general buyer-number threshold.

Regulation 12ג: the Director may allow a deduction on an invoice not in the dealer's name where
it is proved the inputs served the business and the tax is for telephone, water, gas,
electricity "או הוצאות כיוצא באלה". The bookkeeper will need proof of business use, typically
the lease. This is why a utility bill in a landlord's name is `decision: "review"`, not `denied`.

## 4. Mixed use: regulation 18 and section 41

- **Section 41**: "אין לנכות מס על תשומות אלא אם הן לשימוש בעסקה החייבת במס." Inputs that serve
  only exempt transactions (for example residential rent the claimant also earns) are not
  deductible at all.
- **18(א) comes first.** Input tax on an asset or service used both for the business and
  otherwise "יהא ניתן לניכוי בשיעור יחסי שהוא כיחס השימוש לצרכי העסק לכלל השימוש". When the
  business share is known (90% of a phone, 40% of a home-office electricity bill), that ratio
  is the fraction. The same regulation apportions inputs shared between taxable and exempt
  transactions.
- **18(ב) applies only when the non-business use is indeterminate** ("שימוש בלתי מסויים"). Then:
  if the Director has fixed the non-business proportion, that determination governs and is
  treated as an assessment; otherwise **two-thirds** where use is mainly for the business and
  **one-quarter** where it is mainly private.
- 18(ג) is repealed. Do not reinstate it.

`deductible_fraction` (and `candidate_fraction` on a review record) therefore takes any value from 0 to 1, and `business_use.basis` records
which limb produced it: `reg18a_actual_ratio`, `reg18b_director`, `reg18b_mainly_business`,
`reg18b_mainly_private`, or `wholly_business`.

## 5. Vehicles: purchase versus running costs

- **Buying or importing a private car (רכב פרטי) is a complete bar.** Regulation 14(א): the tax
  on the sale of a private car to a dealer, or its import by a dealer, is not deductible at all.
- Regulation 14(ב) carves out a dealer whose main business is selling vehicles (holding the car
  for resale) and a car used exclusively for driving instruction, rental by a rental business,
  passenger transport by a transport business, or organised tours.
- **Running costs, including fuel, are a regulation 18 mixed-use question**, not a vehicle rule.
- **A commercial or work vehicle outside the private-car definition** (truck, taxi) is not
  caught by regulation 14 at all; its input VAT follows the ordinary rules.

Record `vehicle.class` (`private`, `commercial`, `reg14b_exempt_use`, `unknown`) and
`vehicle.document_kind` (`purchase`, `import`, `lease`, `fuel`, `repair`, `other`). Purchase or
import with class `private` gives fraction 0 under regulation 14(א). Everything else goes to the
regulation 18 test. `unknown` forces `decision: "review"`.

## 6. Hosting, employee benefits, the owner's own consumption and home

- **Regulation 16**: "לא יהא ניתן לניכוי מס תשומות בשל הוצאות אירוח, פרט לניכוי מס תשומות על
  הוצאה לאירוח אדם מחוץ לארץ."
- **Regulation 15א** (employee benefits: meals, housing, gifts, entertainment): not deductible
  unless the input was sold or supplied to the employee and that sale is reported as a taxable
  transaction. Its definition of "עובד" includes "אדם שיש לו חלק בבעלות בעסק או אחד ממנהליו",
  so a sole trader's own meal or gift to themselves falls under the same bar.
- **Regulation 15**: "עוסק לא יהא רשאי לנכות מס תשומות על רכישת דירת מגוריו או על בנייתה, כולה
  או מקצתה, ולא את מס התשומות על השירותים שקיבל לצורך רכישתה או בנייתה אם הדירה משמשת או
  תשמש גם כמקום עסקו." Ordinary home-office running costs stay under regulation 18.

## 6a. Credit notes

A credit note (הודעת זיכוי) reduces input tax. Regulation 24(ב): "עוסק המקבל הודעת זיכוי במס
חייב לתקן לפיה את סכום מס התשומות בדו"ח התקופתי של התקופה שבה נתקבלה ההודעה." Section 43
says the same for a cancelled or changed transaction after the buyer deducted it. So a credit
note is never a positive input: link it to the original invoice and net it in the period it
was received.

## 7. Cash Law consequence

Under the Law for Reducing the Use of Cash (Tax Authority guide):

| Parties | No cash limit up to | Above that, cash allowed up to |
|---|---|---|
| A business is a party | NIS 6,000 | the lower of 10% of the transaction and NIS 6,000 |
| Two private individuals | NIS 15,000 | the lower of 10% of the transaction and NIS 15,000 |
| Private purchase of a vehicle | NIS 50,000 | the lower of 10% of the transaction and NIS 50,000 |

Section 38(א2) of the VAT Law disallows input VAT on that invoice where it was decided the
payment breached the Cash Law AND a monetary penalty was imposed under section 9 of that law,
unless the dealer satisfies the Director that tax was duly paid on the transaction. A cash
payment above the cap does not by itself void the deduction; warn, do not deny.

## 8. Foreign vendors

App Store, Google Play, AWS, Azure, GCP, Stripe, OpenAI, Anthropic and similar foreign-issued
receipts are not Israeli tax invoices. Their tax line never populates `vat_amount`.

- A transaction made in Israel by a foreign-resident supplier (typically an imported service):
  regulation 6ד, "תחול חובת תשלום המס על הקונה, זולת אם ברשותו של הקונה חשבונית בשל העסקה".
  Set `reverse_charge_required: true` and leave the self-reporting to the bookkeeper. Whether
  the claimant may then deduct the same tax depends on its own status (Step 0).
- Imported **goods**: the Israeli VAT is paid at customs and deducted through the import entry
  (רשימון יבוא), not through a self-invoice.

## 9. Retention and digitisation

See `references/retention-and-scanning.md`.
