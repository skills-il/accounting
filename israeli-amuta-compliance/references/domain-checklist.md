# Domain Coverage Checklist, israeli-amuta-compliance

This is the coverage contract. A future `update-skill` run reads it and flags any Must-cover item
missing from SKILL.md. The full research checklist, with every source URL and the verbatim gazette
and statute quotations, is a build-time QA artifact held outside the published skill folder; the
citations for everything below live in `evidence.json`.

Checklist version: 2. Generated 2026-09-09, revised the same day after expert review.

## Must cover (core)

### Reporting cycle
- [ ] The four annual documents: financial report, verbal report, audit committee protocol, general
      assembly report. Why core: this is the filing package itself.
- [ ] The standing deadline of 30 June in the year following the report period, and the requirement
      that the financial report be signed by two board members. Why core: every other date is
      measured from it.
- [ ] The Registrar's express power to extend that deadline. Why core: it is the mechanism behind
      every emergency extension, so a user should be told to check for a live one rather than be
      told none exists.
- [ ] The X minus 2 rule: a certificate for a given year is granted against the annual reports for
      the year two years earlier. Why core: users assume the years match and prepare the wrong
      year's package.
- [ ] Filing is online, and a blocked submission is usually stale authorised role-holders rather
      than a document problem. Why core: it is the most common operational failure.

### Hard limits and enforcement
- [ ] The one-year bar: a certificate request is not processed where the accompanying documents were
      filed more than a year late. Why core: it decides whether the cycle is open at all, and it is
      the most likely reason a request is refused outright.
- [ ] The ninety-day deemed-cessation rule and the Registrar's power to strike the amuta off.
      Why core: late filing is not only a certificate problem, and no summary states the real stakes.
- [ ] That extensions are granted to ACCOUNTANTS as filing quotas, not to individual amutot, that an
      accountant outside the arrangement confers none on its clients, and that missing a quota counts
      as the amuta's own non-compliance. Why core: the amuta bears its accountant's default and
      cannot see the arrangement from its own side.
- [ ] That filing the annual reports is mandatory whether or not a certificate is wanted. Why core:
      a refused amuta may otherwise conclude filing is now pointless.

### The refusal path
- [ ] Distinguishing the four letters: a documents demand, a notice of intent to refuse, a refusal,
      and a demand to sign a defect-correction plan. Why core: they lead to different actions and are
      routinely confused.
- [ ] Reading and diarising the response window stated in the letter. Why core: most time-critical
      step in the workflow.
- [ ] The defect-correction plan as a named status, including that signing REVOKES a certificate the
      amuta currently holds. Why core: signing is not a neutral remedial step and nobody tells them.
- [ ] The lesser status confirming documents were filed, obtained through its own service and
      accepted by many funders as an interim. Why core: a refused amuta is usually not told it exists.
- [ ] That a refusal is an administrative decision, answerable, with a right to be heard and a
      judicial-review route, and that this is where a lawyer takes over. Why core: without it the
      skill dead-ends the user on a decision that can be answered.

### Governance and audit bands
- [ ] Every amuta, at any turnover including none, needs a general assembly, a board and an audit
      committee. Why core: the most common gap in a certificate application.
- [ ] Every amuta prepares a balance sheet and an income and expenditure statement. Only the AUDIT
      is banded. Why core: a small amuta that concludes it need not prepare accounts has misread it.
- [ ] The bookkeeping band at 750,000 NIS, which is NOT index-linked: above it, double-entry books;
      at or below it, a receipts-and-payments book. Why core: it is a different duty from the audit.
- [ ] The audit band, 1,380,630 NIS for 2026, which IS index-linked and re-gazetted each February.
      Above it an accountant must be appointed and the report reaches the general assembly audited.
      Why core: this decides whether the amuta must pay for an auditor at all.
- [ ] That the bookkeeping and audit thresholds share a 1996 base but are different numbers today,
      and must never be substituted for one another. Why core: quoting the base figure as the audit
      threshold tells a mid-sized amuta it needs an auditor when it does not.
- [ ] The internal-audit band at 10,000,000 NIS, requiring an internal auditor appointed with the
      audit committee's agreement. Why core: third band, routinely omitted by summaries that only
      contrast small with large.
- [ ] That an auditing body is an election by the general assembly to replace the audit committee,
      available at any size, and not a turnover band. Why core: it is consistently mis-described as
      a threshold consequence.
- [ ] That the Registrar may order an audit even below the threshold. Why core: below-threshold is
      not a guarantee.
- [ ] The attachment listing every payment made or undertaken to each of the five highest-paid
      people, including retirement terms. Why core: separate from the financial report and the most
      commonly missed component of the package.
- [ ] That the organs must be validly COMPOSED, not merely exist: no family majority on the board or
      among signatories, and no salary recipients who are relatives of an audit committee member.
      Why core: this is the substantive refusal ground and a small amuta is most likely to fail it.
- [ ] The certificate application set beyond the four annual documents: the internal-auditor
      appointment protocol above the internal-audit band, the named five-highest-earners online form
      as a distinct form, the fee paid INCLUDING arrears from earlier years, and the foreign-donation
      statement. Why core: arrears alone are a standalone refusal ground.
- [ ] The signature requirements: signatories' names stated beside the original signature, and the
      audit committee form expressly stating whether it recommends approval. Why core: these defeat
      applications on their own.

### Annual fee
- [ ] The full band table: the reduced tier of 176 NIS, and for turnover above 300,000 NIS the
      1,338 NIS early amount and the 1,777 NIS standard amount, with the date the amount changes.
      Why core: the correct fee tier is a stated deliverable.
- [ ] That the reduced tier reaches an amuta in its first two years after the year of incorporation,
      and an amuta that has FILED online reports, so the operative lever is filing rather than
      turnover alone. Why core: the tier is widely mis-described as a simple size test.
- [ ] That the official fee page is internally inconsistent about which year's turnover governs, so
      no turnover-year test should be encoded. Why core: prevents a future update from hardcoding
      the wrong year.
- [ ] That paying the full fee before filing the online reports forfeits any refund of the excess.
      Why core: irreversible and costly.
- [ ] That the fee exemption was abolished from 2020, and that the official page still displays the
      superseded exemption procedure above the sentence abolishing it. Why core: the single most
      likely way an agent gives dangerous advice in this domain.
- [ ] That unpaid fees can be transferred to the fines collection centre, after which the tier can
      no longer be corrected. Why core: escalation path the user should know before it happens.

### Foreign political-entity donations
- [ ] The annual disclosure duty, which IS turnover-gated, including the cumulative donation
      threshold, the per-donation detail required, and publication on the amuta's own website.
- [ ] The quarterly reporting duty, which is NOT turnover-gated and is due within one week of the
      end of the quarter in which the donation was received. Why core: a small amuta below the
      turnover line still owes it, and the skill must never answer "under the threshold, nothing
      to do".

### Section 46 donation reporting
- [ ] The duty, in force from 1 January 2026, to report donations and cancellations through the
      Tax Authority donations system. Why core: the live change that makes the skill timely.
- [ ] That the Section 46 approval is itself conditional on meeting the reporting duty. Why core:
      this is the enforcement consequence and the strongest reason to act.
- [ ] That reporting runs from the first shekel with no minimum. Why core: users assume a threshold.
- [ ] The two prerequisites: registration for Tax Authority digital services, and appointment of a
      super-authorised user. Why core: without them the amuta cannot report at all.
- [ ] The two reporting routes, interfaced receipting software or the manual online application.
      Why core: determines what the amuta actually has to do next.
- [ ] That each reported receipt and cancellation returns a unique reporting number which must
      appear on the receipt, and that reporting must be retried until a valid number is returned.
      Why core: a silent failure must not be treated as success.
- [ ] That the duty applies even where the amuta is exempt from issuing receipts. Why core: a
      receipt exemption is the most natural reason to assume the duty does not apply.
- [ ] That an anonymous donation does not entitle anyone to a tax benefit. Why core: affects what
      the amuta should tell its donors.
- [ ] That there is no April compliance deadline, only the January one. Why core: a circulating
      error that conflates this with the fee calendar.

## Should cover (advanced / edge cases)
- [ ] The sentinel donor entity numbers used for a foreign resident and for an anonymous donation.
- [ ] Payment-means rules: a separate receipt per payment type and per card, foreign currency
      handling, and post-dated cheques split by tax year according to the due date.
- [ ] In-kind donations, which are reportable but do not receive the credit automatically.
- [ ] Cancellations and corrections, citing the original reporting number, including the paper-book
      case that needs no system report.
- [ ] Donations through interfaced digital platforms, reported by the platform.
- [ ] The employer route for granting the credit through the payslip.
- [ ] The foreign political-entity donation statement required above 300,000 NIS turnover.
- [ ] Registrar inspectors' power to enter premises without prior coordination.
- [ ] The public benefit company fork: it registers and pays as a company, its certificate issues
      under the Companies Law, and it files an additional annual return.

## Out of scope (explicit, with rationale)
- Producing the audited financial statement, the balance sheet as an audited product, or an
  auditor's opinion. Reserved to a licensed accountant. Note that the Accountants Law expressly
  excludes bookkeeping from the reservation, so preparation work is clear.
- Drafting or amending the articles, and any legal opinion. Reserved to a lawyer, and the
  reservation is disjunctive so being free is not a defence.
- Incorporating a new amuta. Adjacent workflow, heavier lawyer involvement.
- Obtaining Section 46 status for the first time. This skill covers reporting BY a holder.
- The donor's own tax-credit computation. Handled by the employee tax refund and tax return skills.

## Open items, do not invent these
- The complete certificate application document set, and how it differs between a first-time
  applicant, a renewal, and a newly registered amuta.
- The current company fee table for a public benefit company. The official company-fee pages
  errored when checked on 2026-09-09; route the user to the companies unit.
- The widely repeated twenty-four month rule for a newly registered amuta. No primary source found.
