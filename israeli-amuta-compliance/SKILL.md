---
name: israeli-amuta-compliance
description: "Not legal or accounting advice and not an audited financial statement. Prepares an Israeli amuta or public benefit company (chalatz) for its annual filing to the Registrar of Associations: builds the checklist for the four annual documents, works out which governance organs and which audit duty the turnover band triggers, fixes the correct annual fee tier and deadline, and produces a gap report naming what blocks the ishur nihul takin. Use when the user asks about amuta annual reports, ishur nihul takin, doch miluli, vaadat bikoret, the amuta annual fee, or Section 46 digital donation reporting to the Tax Authority. Do NOT use for incorporating a new amuta, drafting or amending a takanon, producing the audited financial statement itself, which is reserved to a licensed accountant, or for listed-company reporting to the TASE or MAYA, which israeli-annual-reports covers."
license: MIT
---

# Israeli Amuta Compliance

## Legal notice

This is a free information tool operated by an AI model, with no accountant or lawyer involved,
reviewing it or approving it. It produces checklists, gap lists and summaries of deadlines and
amounts for internal organisation only, for the amuta's own officers to review and adopt
themselves. It is not legal advice and not accounting advice.

It does not produce, and must not be presented as producing, an audited financial statement, an
auditor's opinion, or any other work product reserved to a licensed accountant under the Accountants
Law. Auditing a financial report is reserved to a רואה חשבון. Drafting or amending a תקנון, and any
legal opinion, belong to a lawyer: the Bar Association Law reserves those whether or not a fee is
charged, so the fact that this tool is free is not a defence. It drafts no legal instrument, and any
text it does produce is an automatic draft for personal organisation only, not a document prepared
by a lawyer or an accountant.

The tool may err, omit data, or present a wrong conclusion, and it is not a substitute for advice
that takes account of the particular circumstances and needs of each person. Responsibility for
filing and payment is yours, the binding determination belongs to the Registrar of Associations and
to the Tax Authority as the case may be, and representation before the Tax Authority is reserved to
those entitled to it by law.

Figures in this skill carry a year. Israeli thresholds are index-linked and are re-gazetted
annually. Confirm the operative figure for the year you are filing before relying on it.

## Problem

An amuta loses its אישור ניהול תקין for reasons that have nothing to do with how well it runs its
programmes: it filed the wrong year's reports, it never appointed the organ its turnover band
requires, or it paid the wrong fee tier and cannot get the difference back. The rules sit across
the Associations Law, a Registrar circular, a fee regulation and a Tax Authority execution
instruction, and the public guides that summarise them are wrong often enough to be dangerous.
Without the certificate the amuta cannot receive state support, cannot apply to most foundations,
and its donors cannot claim their tax credit.

## Instructions

Work through the steps in order. Steps 1 to 3 establish which rules apply to this amuta; steps 4 to
7 produce the deliverables. Do not skip step 2: getting the reporting year wrong is the single most
common way a user prepares an entire package that cannot be filed.

### Step 1: Identify the entity and read its registry position

Ask for the amuta's registration number (מספר עמותה, 9 digits starting 58) or its exact name. A
חל"צ has a company number starting 51 and follows a different track, see step 8.

If the `israel-amutot` MCP is available, read the entity's current position rather than asking the
user to recall it:

| Question | Tool |
|---|---|
| Does the amuta exist and what is its status | `search_amuta`, `get_amuta_details` |
| Does it hold a current certificate, and for which year | `check_management_certificate` |
| What turnover did it last report | `get_financial_info` |
| Has it received foreign political-entity donations | `search_foreign_donations` |

Treat registry figures as the amuta's last reported position, not as today's truth. The turnover
that decides this year's duties is the turnover of the year being reported.

If the MCP is unavailable, ask the user for the status, the last certificate year and the turnover,
and say plainly that you are relying on their figures.

### Step 2: Fix the reporting year (the X minus 2 rule)

A certificate for year X is granted against the annual reports for year **X minus 2**.

| Certificate sought | Annual reports required | Those reports fell due |
|---|---|---|
| 2026 | 2024 | 30 June 2025 |
| 2027 | 2025 | 30 June 2026 |
| 2028 | 2026 | 30 June 2027 |

State the mapping back to the user explicitly before going further. Users almost always assume the
certificate year and the report year are the same, and then prepare the wrong year's documents.

The statutory deadline is section 36(ד): the financial report is filed no later than **30 June of
the year following the end of the report period**, signed by **two board members**. The same section
expressly lets the Registrar extend that date, which is how the emergency extensions are granted.

**Two hard limits decide whether this cycle is open at all. Check them before building anything.**

- **The one-year bar.** The Registrar does not process a certificate request whose accompanying
  documents were filed more than a year late, meaning after 30 June of the year the certificate is
  sought for. Past that point the cycle is closed and no amount of remediation reopens it.
- **Ninety days is a separate cliff.** Under s.59 an amuta is deemed to have ceased operating if it
  does not pay a fee within ninety days of the last date set for it, or does not file the financial
  report within ninety days of the s.36 date. The Registrar may then strike it off, applying s.368
  of the Companies Ordinance. Late filing is not only a certificate problem.

**Extensions go to ACCOUNTANTS, not to amutot.** They are issued as filing quotas. Under the
arrangement published on 19 May 2026, for 2025 reports and the 2027 certificate, a participating
accountant may file 20 percent of client reports by 31.7.2026, 45 percent cumulatively by
31.8.2026, 70 percent cumulatively by 4.10.2026, and 100 percent cumulatively by 1.11.2026. Three
consequences the amuta must understand:

- An accountant who did not send the client list to the Registrar by 31.7.2026 is not in the
  arrangement at all, so their clients get no extension.
- Missing the quota counts as **the amuta's** failure to comply, not the accountant's.
- A request filed after 1.11.2026 is handled subject to workload, and a certificate runs from the
  date it is signed, so a full calendar year cannot be guaranteed.

Ask which accountant files for the amuta and whether that accountant joined the arrangement. Then
read the Registrar's news page for the arrangement governing the cycle in front of you: these dates
are re-issued annually and the ones above are specific to the 2027 cycle.

### Step 3: Band the amuta by turnover

Four independent bands key off turnover. They are cumulative, and they are not the same number, so
work through all four rather than assuming one threshold governs everything.

| Band | Threshold | Consequence | Source |
|---|---|---|---|
| Organs | any turnover, including none | general assembly, board, and audit committee | s.19(א) |
| Bookkeeping | above 750,000 NIS | double-entry books instead of a receipts-and-payments book | Second Schedule |
| Audit | above **1,380,630 NIS for 2026** | must appoint a רו"ח, and the financial report must reach the general assembly audited | s.19(ג)(1), s.37(א) |
| Internal audit | above 10,000,000 NIS | must additionally appoint a מבקר פנימי | s.30א |

Four things to get right here:

1. **The audit threshold is index-linked; the bookkeeping threshold is not.** Both descend from a
   750,000 NIS figure, but only s.19(ג) carries the indexation clause in s.19(ג)(2). Never reuse the
   audit figure as the bookkeeping figure.
2. **The audit figure is re-gazetted every year.** s.19(ג)(2) requires publication in רשומות at the
   start of February. If the user is filing for a year other than 2026, tell them to take that
   year's gazetted amount rather than reusing 1,380,630.
3. **Every amuta prepares a מאזן.** s.36(א) requires a balance sheet and a statement of income and
   expenditure from every amuta regardless of size. It is the **audit** that is banded, not the
   balance sheet. A small amuta that concludes it need not prepare accounts has misread this.
4. **A גוף מבקר is not a turnover band.** Under s.19(ב) the general assembly may resolve to appoint
   an accountant or a Registrar-approved body *instead of* the audit committee. That is an election,
   available at any size, not something a threshold forces.

Note also s.37(ב): the Registrar may order an audit even for an amuta below the threshold, on the
audit committee's request, on the request of a tenth of the members, or on the Registrar's own
initiative. Below-threshold is therefore not a guarantee.

**Existence is not enough, check composition.** The Registrar's proper-management questionnaire
screens the organs for family proximity, and a small amuta is the population most likely to fail,
because a small board is often a family board. Ask whether there is a majority of relatives among
the board members, a majority of relatives among the authorised signatories, or salary recipients
who are relatives of an audit committee member. An audit committee that is two siblings is a
defect, not a committee. Report it as a gap even though the organ formally exists. This is a
substantive refusal ground, as distinct from the paperwork grounds, and it is the one an agent will
miss if it only checks that the three organs are named.

### Step 4: Build the filing checklist

The annual package is four documents. Produce them as a checklist with a status per document, not
as prose.

| # | Document | Notes |
|---|---|---|
| 1 | דוח כספי (financial report) | balance sheet plus income and expenditure, per the Second Schedule list. Signed by two board members. Audited if step 3 put the amuta over the audit threshold |
| 2 | דוח מילולי (verbal report) | narrative account of activity for the year |
| 3 | פרוטוקול ועדת ביקורת | the audit committee's or auditing body's recommendations on approving the financial report |
| 4 | דיווח אסיפה כללית | record that the general assembly approved the financial report |

One attachment is missed more often than any of the four: under s.36(ב) the board must attach a
statement giving a full and precise account of **all payments made or undertaken to each of the five
highest-paid people in the amuta**, including retirement terms, and covering anything of monetary
value, loans, securities and other benefits, whether paid to the person or to someone else on their
behalf. Ask for it explicitly.

**The annual reports are not the whole application.** The certificate application set also
includes a board protocol appointing an internal auditor where turnover exceeds ten million NIS, a
named list of the five highest earners submitted on the Registrar's online form (a distinct form,
not merely the s.36(ב) attachment), confirmation that the annual fee is paid **including arrears
from earlier years**, and the s.36א foreign-donation statement. Unsettled arrears are a standalone
reason a certificate is refused.

Signature detail defeats applications on its own: the signatories' **names must be stated beside
the original signature**, and the audit committee's form must expressly say whether it recommends
approving the financial report. Confirm the current cycle's exact set against the Registrar's own
circular, because the numbering and the online forms change between cycles.

Filing is online. If the submission is blocked, the cause is usually that the amuta's authorised
role-holders are out of date rather than a problem with the documents themselves.

Filing the annual reports is mandatory in its own right. It does not depend on whether the amuta
wants a certificate this year.

### Step 5: Fix the fee tier and the deadline

The fee is annual, per calendar year, under the Associations (Fees) Regulations.

| Situation | 2026 amount | Timing |
|---|---|---|
| Reduced tier | 176 NIS | whole year |
| Turnover above 300,000 NIS, paid up to 31.03 | 1,338 NIS | until 31.03 |
| Turnover above 300,000 NIS, paid from 01.04 | 1,777 NIS | from 01.04 |

The reduced tier is not simply "a small amuta". It reaches an amuta in the **first two years after
the year of incorporation**, and an amuta that has **reported online** that its turnover did not
exceed 300,000 NIS. The gov.il page is internally inconsistent about which year's turnover governs,
naming 2023 in one sentence while twice naming the **2024 online reports** as the operative trigger
for the 2026 rate. Do not encode a 2023 turnover test. Tell the user the operative lever is filing
the online annual reports, and have them confirm the tier with the Registrar before paying.

Two consequences worth stating up front:

- **Paying early does not just save money, it is irreversible in one direction.** An amuta that pays
  the full fee before filing its online reports is not entitled to a refund of the excess.
- **Unpaid fees escalate.** Debts can be transferred to the מרכז לגביית קנסות, which can levy on
  assets, and once transferred the fee tier can no longer be corrected.

The fee is index-linked and updated once a year, and carries no VAT component.

### Step 6: Check Section 46 digital donation readiness

Only relevant if the amuta holds a Section 46 approval. If it does, this is the most urgent item in
the whole review, because the approval itself is now conditional on it.

Execution instruction 11/2025 states that from **1 January 2026** amutot holding a Section 46
approval must report donations and donation cancellations through the **תרומות ישראל** system, and
that "אישור לפי סעיף 46 מותנה בעמידה בחובת הדיווח על פי הוראת ביצוע זו". Failing to report puts the
approval at risk, not merely the donor's credit.

Check these in order, because the first two are prerequisites and an amuta that has not done them
cannot report at all:

1. Is the amuta registered for Tax Authority digital services, and is every person who will report
   registered and separately authorised?
2. Has the amuta appointed a **מורשה-על**, who can report and authorise others on its behalf?
3. Is the receipting software interfaced with the system? If not, the fallback is the online
   application, which requires keying every receipt by hand and is explicitly not recommended.
4. Does every donation receipt carry the מספר דיווח returned by the system?

Four rules that catch people out:

- Reporting runs **from the first shekel**. There is no minimum donation.
- The duty applies **even where the amuta is exempt from issuing a receipt**.
- A **תרומה בעילום שם does not entitle anyone to a tax benefit**, and a donation with a full name but
  no ID number is not attributed to the donor.
- Cancellations are reportable too, citing the original מספר דיווח.

There is no April 2026 compliance deadline. The date is 1 January 2026. If a user has been told
otherwise, they have probably been given the annual-fee calendar by mistake, where 01.04 is when the
fee rises from 1,338 to 1,777.

### Step 7: Foreign political-entity donations

Two separate duties, with different triggers. Conflating them is the usual error.

**Annual disclosure, turnover-gated.** s.36א(ב)(1) requires an amuta with turnover above 300,000
NIS to state in its financial report whether it received donations from foreign political entities
whose cumulative value exceeds 20,000 NIS, and if so to give the donor's identity, the amount, the
purpose, and any conditions or undertakings attached. s.36א(ג) requires the amuta to publish that
information **on its own website**, and where it has told the Registrar it has no website, the
Registrar publishes it on the Ministry of Justice site.

**Naming donors generally.** Separately from foreign political entities, the Second Schedule lets
an amuta omit a donor's name from the financial report only where the receipt carries
"תרומה בעילום שם" in the donor-name field AND either the donation does not exceed the maximum the
Minister set, or the Registrar granted a **special approval** not to name the donor. The
Registrar's questionnaire screens for donors above that cumulative annual figure, so an amuta with
a large single donor and no special approval should expect to name them. Do not confuse this
threshold with the foreign political-entity one; they are different rules that happen to share a
number.

**Receipt-book mechanics that bind the two workstreams together.** Donation receipts go in a
SEPARATE receipt book, the word "תרומה" must be printed conspicuously on every receipt in it, and
an amuta holding a Section 46 approval must additionally print on the receipt that it holds an
Income Tax approval for donations under Section 46. This is a concrete, checkable defect an
inspector will find, and it is where the Registrar workstream and the Section 46 workstream meet.

**Quarterly reporting, NOT turnover-gated.** Section 2 of the Disclosure Duty Law 2011 requires a
body that received a donation from a foreign political entity to file an online report with the
Registrar **within one week of the end of the quarter** in which the donation was received, giving
the donor, the amount, the purpose and any conditions. There is no turnover gate and no amount gate
on this duty.

The practical consequence: a small amuta below the 300,000 NIS turnover line that takes a single
foreign political donation still owes a quarterly report within a week of quarter end, even though
it owes no annual disclosure. Never answer "your turnover is under the threshold, nothing to do".

### Step 8: Produce the gap report

Close with a gap report that names what currently blocks the certificate, one line per gap, each
with the concrete next action and who has to take it. Order by what blocks filing first. Separate:

- gaps the amuta's own officers can close (appoint the missing organ, convene the assembly, update
  role-holders, appoint a מורשה-על),
- gaps that need a licensed professional (the audit itself, any תקנון amendment),
- gaps that are purely a payment or a deadline.

Say explicitly which items you could not verify and which the user must confirm with the Registrar.

### Step 9: When the certificate is refused or not granted

A refusal letter is not the end of the process, and this is the situation most users arrive in.
Work through it in this order.

**First, identify what the letter actually is.** They are routinely confused, and they lead to
different places:

| The letter is | What it means | What it asks for |
|---|---|---|
| דרישה להשלמת מסמכים | the application is alive, something is missing | supply the named items within the stated window |
| הודעה על כוונה לסרב | a decision has not been taken yet | respond within the stated window, before the decision |
| סירוב | a decision has been taken | see the response and challenge routes below |
| דרישה לחתום על תכנית לתיקון ליקויים | substantive defects were found | see the warning below before signing |

**Read the response window off the letter itself and diarise it.** It is the single most
time-critical thing in the whole workflow.

**Then ask whether the defect is curable in this cycle.** Apply the one-year bar from step 2. If
the documents are already more than a year late, the cycle is closed and the work belongs to the
next cycle, not this one. Saying so plainly is more useful than a remediation plan for a cycle that
cannot be reopened.

**A defect-correction plan is not a neutral remedial step.** An amuta offered a תכנית לתיקון
ליקויים should understand two things before signing: the certificate is granted only once the
Registrar is satisfied the material defects were fixed, informed by the accompanying body's report,
and an amuta that **currently holds** a valid certificate has it revoked as of signature. Flag this
and route the decision to the amuta's own professional advisers.

**There is a separate, lesser confirmation, but be precise about it.** The Registrar's service
page refers to an **אישור על קבלת מסמכים**, alongside the proper management certificate. Two
cautions before raising it with a refused amuta. Its documented population is a NEW amuta, or one
that has not carried on continuous activity for two years, rather than an established amuta whose
certificate was refused. And state support decisions condition support on the proper management
certificate itself, so do not present the lesser confirmation as a substitute for it. Ask the
Registrar whether it is available in the amuta's specific situation instead of assuming it is.

**On challenging the decision itself.** A Registrar refusal is an administrative decision. Israeli
administrative law attaches a right to be heard before an adverse decision, and such decisions are
challengeable in the בית המשפט לעניינים מנהליים. This skill does not advise on that and must not:
say clearly that the decision is answerable, that there are deadlines attached, and that this is
the point where the amuta should take a lawyer. Do not leave the user believing a refusal is final.

### Step 10: Public benefit companies (chalatz)

A חל"צ is a company, not an amuta, and diverges in ways that matter:

- It is registered with רשם החברות and supervised by רשם ההקדשות; its certificate is issued against
  the Companies Law rather than the Associations Law.
- It files an additional annual return, טופס 5, under s.141 of the Companies Law.
- It pays its annual fee at the **companies** unit, not the amutot unit, on a separate fee table.

Do not quote the amuta fee table to a חל"צ. Route the user to the companies unit for the current
company fee amounts.

## Recommended MCP Servers

| MCP | What it adds here | Install |
|---|---|---|
| `israel-amutot` | Registry lookup over roughly 74,880 amutot: status, financials, certificate history by year, foreign-donation records, and חל"צ records | `npx -y @skills-il/israel-amutot-mcp` |
| `budgetkey` | Whether the amuta receives state support, which raises the cost of losing the certificate | `url:https://next.obudget.org/mcp` |

## Gotchas

- **Assuming the certificate year equals the report year.** It does not; it is X minus 2. This is the
  most expensive mistake in the domain because the user prepares a complete package for the wrong
  year before anyone notices.
- **Quoting the fee exemption.** There is no longer one. It was abolished from 2020. The gov.il fee
  page still displays the 2019 exemption procedure immediately above the sentence abolishing it, so
  an agent that stops reading early will confidently offer a dead exemption. Several published
  guides make exactly this error.
- **Reusing 750,000 NIS as the audit threshold.** It is the 1996 base and the current bookkeeping
  threshold, but the audit threshold for 2026 is 1,380,630 NIS. Quoting the base figure tells an
  amuta whose turnover sits between the two thresholds that it needs a paid auditor when it does
  not.
- **Treating an expired extension as available.** The שאגת הארי extension moved 2025 reports to
  31 July 2026 and covered only the 2027 certificate; both that date and the 30 June 2026 window for
  the 2026 certificate are in the past. Check the Registrar's news page for a current extension
  rather than repeating an old one or asserting that none exists.
- **Telling a small amuta it need not prepare accounts.** s.36(א) binds every amuta. Only the audit
  is banded.
- **Answering "under the threshold, nothing to do" on a foreign political donation.** The quarterly
  report under the Disclosure Duty Law has no turnover gate and is due within a week of quarter end.
  Only the annual disclosure is turnover-gated.
- **Checking that the organs exist without checking who sits on them.** A board or audit committee
  that is a family majority is a substantive refusal ground. Existence is not compliance.
- **Treating a refusal as final.** It is an administrative decision with a response window, and a
  lesser status exists to ask for in the meantime. Never close on "the certificate was refused".

## Bundled Resources

- `references/domain-checklist.md`: the full coverage checklist with every band, the verbatim rate
  tables, and a known-bad-figures section.
- `references/filing-package.md`: the four documents, the s.36(ב) attachment, and the certificate
  application set.
- `scripts/band_check.py`: given turnover, certificate year and Section 46 status, prints the bands,
  the fee tier, the report year and the deadline. Pure computation, no network access required.

## Reference Links

| Source | URL | What to Check |
|---|---|---|
| Registrar, proper management certificate | https://www.gov.il/he/service/association_certification_of_proper_management | current application route and forms |
| Registrar, annual fee | https://www.gov.il/he/service/association-annual-fee | the operative fee tiers for the year |
| Registrar, reporting duties | https://www.gov.il/he/service/association_annual_reporting_obligations | duties for amuta and chalatz, forms |
| Registrar news | https://www.gov.il/he/pages/news-rejection | whether an extension is currently in force |
| Associations Law | https://he.wikisource.org/wiki/חוק_העמותות | ss.19, 30א, 36, 36א, 37 and the Second Schedule |
| Execution instruction 11/2025 | https://www.gov.il/BlobFolder/policy/inst-11-2025/he/IncomeTax_inst-11-2025.pdf | Section 46 donation reporting rules |

## Troubleshooting

| Symptom | Likely cause | What to do |
|---|---|---|
| Online filing rejects the submission | the amuta's registered role-holders are stale, so the filer is not authorised. This is the most common cause, though other causes exist and the portal error text is rarely specific | update role-holders with the Registrar, then retry |
| Certificate refused despite documents filed | reports filed for the wrong year, or an organ the turnover band requires was never appointed | re-run steps 2 and 3 |
| Donation report returns no מספר דיווח | the report was not accepted | retransmit until a valid number is returned; instruction 11/2025 requires this rather than treating a silent failure as success |
| Amuta paid 1,777 and believes it qualified for 176 | full fee paid before the online reports were filed | no refund is available; file the reports so the following year is correct |
| Turnover sits near a threshold | the deciding figure is the reported year's turnover, and the audit figure changes annually | take the gazetted amount for the filing year, not this skill's 2026 value |
