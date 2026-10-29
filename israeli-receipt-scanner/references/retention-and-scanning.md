# Retention and Destroying the Paper After Scanning

Users of a receipt scanner ask "can I throw the paper away now?". The default answer is **no**:
the output of this skill (photos, JSON, CSV) is a working copy, not a scanned document in the
sense of the Bookkeeping Directives. This file states the rules so the agent can say why, and
what would have to be true before the paper may go.

Sources: section 75 of the VAT Law; sections 25 and 36 of the Bookkeeping Directives (הוראות מס
הכנסה (ניהול פנקסי חשבונות), התשל"ג-1973), annexes F and G of section 36 (in force since
1.1.2013).

## How long to keep

| Law | Rule |
|---|---|
| VAT Law, section 75 | books, the documents they are based on and the dealer's purchase invoices are kept seven years, from the last entry in the book or from the date the purchase invoice was issued, whichever is later |
| Bookkeeping Directives, section 25(ג) | the accounting system is kept seven years from the end of the tax year it relates to, or six years from the date the income-tax return for that year was filed, whichever is later |

Keep each document until the LATER of the two periods ends. A document received as a signed
computer file (an e-invoice) is kept in electronic storage as part of the accounting system
(section 25(ג2)); printing it does not replace the file.

## When a scan may stand in for the paper (annex F of section 36)

Section 25(ה)(2) accepts external documentation "כתוצר של סריקה ממוחשבת" only if the scan was
made under annex F and the file is kept in a digital archive under annex G. Annex F applies to
receipts, delivery notes, invoices, tax invoices, credit notes and orders the taxpayer received
on paper. A "מסמך סרוק" must meet ALL of these:

1. the document is recorded in the taxpayer's accounting system;
2. it went through computerised scanning, defined as "הליך טכנולוגי המעתיק מסמך מקור לקובץ באופן
   שניתן לאחזר ממנו תוצר קריא הזהה למקור";
3. the words "מסמך סרוק" were added prominently to the file;
4. the file was signed with an approved electronic signature (חתימה אלקטרונית מאושרת, as defined
   in the Electronic Signature Law, 2001) of the taxpayer or someone on their behalf, confirming
   the original was scanned in full;
5. a second person checked that the original is identical to the scan and signed with their own
   approved electronic signature;
6. reasonable protection was regularly applied against intrusion into, or disruption of, the
   file.

The definition is technology-neutral, so a phone camera is not banned as such. But a photo in a
gallery, or a JSON record produced by this skill, meets none of conditions 1, 3, 4 and 5.

## The digital archive (annex G)

The archive must hold capture metadata (a unique identifier, the user, document type, the
issuer's VAT number, document date and number, capture date), allow search, prevent deletion or
editing after capture, keep an event log that cannot be deleted or changed, preserve the digital
signature, allow export, and have backup and restore.

## When the paper may be destroyed (annex F, section 2)

A taxpayer may destroy a scanned document for a given tax year only if:

1. the file is kept in an annex G digital archive as part of the accounting system;
2. the return under section 131 of the Income Tax Ordinance was filed for that tax year;
3. for a withholding agent under section 166 of the Ordinance, the withholding report (form
   0856) was filed on time;
4. the taxpayer (and for a corporation, its rights holders and managers) was not convicted of a
   tax offence, or of certain Penal Law offences, in the four years before that tax year began;
5. the books for that year were not found inadmissible and are not the subject of a pending
   proceeding.

Each condition is tested per tax year. A current-year document can never qualify, because that
year's return cannot have been filed yet.

## What the agent should say

- "Do not throw these away yet. Keep the originals for at least seven years; the exact end date
  is the later of the VAT and income-tax periods above."
- "Scanning with this tool does not make the scan a legal substitute. That needs an approved
  electronic signature by you and by a second checker, a 'מסמך סרוק' mark, and a compliant
  digital archive. Ask your bookkeeper whether your accounting software provides one."
- "A receipt that is not deductible for VAT may still matter for income tax. Keep it."
- Thermal slips fade. That is a reason to scan early as a working copy, not a reason to destroy
  the original.

Whether the Tax Authority keeps a separate approval list for scanning or archive products is
not stated in the Directives and was not verified; do not assert one.
