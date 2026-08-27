---
name: israeli-annual-reports
description: Not investment advice and not a recommendation to buy or sell. Navigate and analyze Israeli corporate annual reports (dochot titkuftiim), financial filings, and regulatory disclosures. Use when user asks about Israeli annual reports, MAYA filings, IFRS financial statements, doch titkufti, dochot kaspiyim, or Companies Law reporting requirements. Covers TASE filing types, Israeli GAAP to IFRS transition, Hebrew financial terminology, and key financial statement analysis.
license: MIT
compatibility: Works with Claude Code, Cursor, GitHub Copilot, Windsurf, OpenCode, Codex, Antigravity, Gemini CLI.
---


# Israeli Annual Reports

## Legal notice

This is a free information tool operated by an AI model. It explains how Israeli corporate reporting works and helps you read filings that issuers have already published. All of its outputs are produced automatically by an AI model, with no involvement, review, or approval by a licensed investment adviser. An AI model may err, omit data, or present a wrong conclusion.

The operators of this tool have no personal interest in the securities or financial assets mentioned in it, and receive no consideration, commission, or benefit of any kind for presenting them.

The output is not an accountant's opinion and not an audit of financial statements. It is not investment advice, not investment marketing, and not a recommendation to buy, sell, or hold any security or financial asset. It is not a substitute for advice that takes account of the particular data and needs of each person, and it does not take into account your financial position, your investment objectives, or the risk you are able to bear. Consult a licensed investment adviser before acting on anything here. All use of its output is the user's sole responsibility.


## Scope: which "annual report" this is

In Israeli usage "doch shnati" means two different filings, and they have nothing to do with each other. Establish which one the user means before answering.

- **This skill covers SECURITIES periodic reporting**: the doch titkufti a REPORTING CORPORATION files with the ISA through Magna and the public reads on MAYA, under the Securities Law 1968 and the Securities Regulations (Periodic and Immediate Reports) 1970.
- **This skill does NOT cover the Registrar of Companies annual report** (the Companies Law Sec. 141 doch shnati every Israeli company files with Rasham HaChavarot, with the annual fee (agra shnatit) and the chevra mefera consequences of not filing). If the user runs an ordinary private company and asks "how do I file my annual report", that is the filing they mean, and this skill is the wrong tool. Route them to the Corporations Authority (see Reference Links) rather than answering with securities disclosure.

## Reporting Framework
Israeli public companies adopted IFRS in 2008. Prior reports use Israeli GAAP. Banks report under the Bank of Israel Supervisor of Banks "Public Reporting Directives" (Hora'ot ha-Divuach la-Tzibur), an Israel-specific template that draws on US bank-reporting rules and incorporates IFRS for some topics, not plain IFRS. For insurers, Israel postponed first-time IFRS 17 implementation to 1 January 2025 (the original global effective date was 2023).

**Check the reporting currency first, do not assume shekels.** Under IAS 21 these are two different things: the FUNCTIONAL currency (matbea peilut) is determined by the primary economic environment and drives measurement, while the PRESENTATION currency (matbea hatzaga) is elected and drives translation, with translation differences going to OCI. A company can present in a currency other than its functional one. A large share of TASE issuers, especially tech and shipping names (e.g. ZIM, Tower, Nova, Camtek, Sapiens), present their statements in USD. Read the figures in the statement's own currency and convert only if the user explicitly needs another, forcing everything into NIS produces wrong numbers and wrong peer comparisons.

## Report Types and Deadlines
| Report | Deadline | Content |
|--------|----------|--------|
| Annual / Periodic (Doch Titkufti) | Within 3 months after year-end, and at least 14 days before the AGM that approves the statements (Reg. 7(a)). Separately, the auditor's signature date may not precede filing by more than 3 days: that is a maximum-lag constraint, NOT a deadline | Audited financials, board report |
| Quarterly (Doch Rivoni) | Two months from the report date, AND within 3 days of the auditor's signature on the interim review report (Reg. 39(a)) | Reviewed interim financials |
| Half-Yearly (Doch Chatzi-Shnati) | Two months from the end of the second quarter (Regs. 39-49 apply, reading "report date" as the last day of Q2) | Reviewed interim financials, filed by small corporations (taagid katan) without public debt in place of Q1/Q3 reports |
| Immediate (Doch Miyadi) | Event learned between 09:30 and 17:00: by 09:30 the next trading day. Learned after 17:00 and before 09:30: by 13:00 the next trading day (Reg. 30(b)) | Material events |
| Shelf Prospectus | Valid up to 3 years | Securities offering framework |

**Reviewed vs. audited (critical distinction):** only the ANNUAL statements are audited. The quarterly and half-yearly interim statements are REVIEWED (sekira) under the auditor's interim-review standard, which is LIMITED assurance ("nothing came to our attention"), not a full audit. Do not treat interim numbers as if they were audited.

## What else ships with a periodic report

The four Parts are the document. A complete filing also carries components a filing map must not omit, each with its own regulation:

| Component | Reg. |
|---|---|
| Separate/solo data attributed to the corporation | 9ג |
| Liabilities by repayment date (matzevet hitchayvuyot) | 9ד |
| Pro-forma data on a material acquisition or disposal | 9א |
| Internal-control (ISOX) effectiveness report + Ninth-Schedule certifications | 9ב, 38ג |
| Very-material valuation attachments | 8ב, 49 |
| Associated-company financial statements | 44 |
| Board report content | 10 |
| Officer remuneration | 21 |
| Controlling-shareholder transactions | 22 |
| Immediate-report categories (material event; enumerated events and board resolutions) | 30-37 |

ISOX is an OBLIGATION for a non-small reporting corporation (management's effectiveness report plus the auditor's separate ICFR opinion), not merely something a small corporation escapes. An offering is effected by the shelf OFFERING report (doch hatzaat madaf) under the shelf-offer rules, not by the shelf prospectus itself. Mergers and controlling-shareholder transactions carry their own Companies Law reporting and approval steps.

## Annual Report Structure
- Part A: Description of Business (operations, markets, risks)
- Part B: Board Report (MD&A, financial review)
- Part C: Financial Statements (balance sheet, P&L, cash flow, statement of changes in equity (Doch al ha-Shinuyim ba-Hon), and the Notes / Biurim)
  - In the Notes (Biurim), read: segment data, IFRS 16 lease liabilities, contingencies and provisions, related-party disclosures (IAS 24), and subsequent events. The analytic detail lives in the Notes, not on the face of the statements.
- Part D: Additional Information (officer compensation, shareholder-approved remuneration policy, audit committee). Part D also carries the CEO and CFO management certifications (hatzharot menahalim) on the financial statements and on disclosure controls, the Israeli analogue of the US SOX management certification. In an ISOX-exempt small corporation the CEO/CFO still file a reduced certification on the financial statements themselves; only the disclosure-controls / internal-control-effectiveness portions are removed, and that reduction is itself a signal about the issuer's size/status.
- Consolidated vs. separate/solo: an Israeli periodic report carries BOTH the consolidated (me'uchad) group statements AND, under Reg. 9ג, separate/solo data for the parent. Note what that section actually is: financial DATA extracted from the consolidated statements and attributed to the corporation itself, per the Tenth Addendum, NOT IAS 27 separate financial statements. It carries its own special auditor's report or review, distinct from the opinion on the consolidated statements. Do not produce IAS 27 separate statements when Reg. 9ג data is what is required. Default headline analysis to the CONSOLIDATED figures. Grabbing the parent-only solo revenue/net profit materially misstates a holding company (and TASE is heavy with pyramidal holding structures).
- ESG / sustainability: modern Israeli annual reports increasingly carry ESG and climate-risk sections. Look for one, and do not assume its absence. Before telling a user whether such disclosure is mandatory for a given issuer, check the ISA's current published position rather than relying on this skill, since that status has been moving.

## Key Hebrew Financial Terms
- Maazan = Balance Sheet
- Doch Revach VeHefsed = Income Statement
- Hachnasot = Revenue
- Revach Naki = Net Profit
- Nechasim Shotfim = Current Assets
- Monitin = Goodwill
- Odfim = Retained Earnings
- Tzad Kashur = Related Party

## Companies Law Requirements
- Sec. 171(a) of the **Companies Law 1999**: a reporting corporation (תאגיד מדווח) keeps accounts and prepares financial statements per the Securities Law; the board of directors (דירקטוריון) approves them.
- Sec. 172 covers a company that is NOT a reporting corporation (it prepares annual statements with a December 31 balance sheet). Disclosure of a reporting corporation's approved statements to shareholders is governed by the **Securities Law 1968** + the **Securities Regulations (Periodic and Immediate Reports) 1970**, not by Sec. 172. The financial-statements review committee sits under Sec. 171 plus the Companies Regulations (Conditions for the Process of Approving Financial Statements) 2010.
- Sec. 114-118 (Chapter Three, Sign J, ועדת ביקורת): Audit-committee requirements. A public company's board, and the board of a private bond company, appoints an audit committee from among its directors (Sec. 114); Sec. 115 sets its composition, which is the operative part: all external directors are members, a majority must be independent, it is chaired by an external director, and Sec. 115(b) excludes the chairman of the board, a controlling shareholder or their relative, and directors employed by or providing services to the company.
- Sec. 267A (Chapter Four A, מדיניות תגמול לנושאי משרה): the board of a public company, or of a private bond company, must adopt a remuneration policy (mediniyut tagmul) for officers after considering the remuneration committee's recommendations. The recommendations reach the board under Sec. 118B(1), and the policy itself requires general-meeting approval by a disinterested special majority. Sec. 267A(c) lets the board adopt the policy even over the general meeting's objection, on detailed reasoned grounds and after the remuneration committee and board re-discuss it, so a policy adopted despite shareholder rejection is lawful and routine, not a filing error. A policy is set for a period of up to three years, and the committee revisits the continued validity of a policy once every three years. Part D of the periodic report carries the approved policy, so a missing or lapsed policy is a governance red flag worth surfacing.
- Sec. 270-275 (Chapter Five, עסקאות עם בעלי ענין): Related-party transaction approvals (cross-reference IAS 24 disclosure). Sec. 275 is the operative one for an extraordinary transaction with a controlling shareholder: audit committee, then board, then general meeting with a disinterested majority.
- Sec. 302 (חלוקה): the distribution tests. Any issuer declaring a dividend turns on the profit test and the solvency test in Sec. 302. A distribution that fails the profit test can still be made with court approval where the solvency test is met. The board report discusses them, so read them alongside the dividend note.

## Filing Systems and Spec Compliance
- **Magna** (`www.magna.isa.gov.il`) is the filer-side system used by issuers to submit periodic and immediate reports to the ISA. **MAYA** (`maya.tase.co.il`) is the public-facing viewer of those filings. Don't conflate the two: agents asking "where do I file?" need Magna; agents asking "where do I read?" need MAYA.
- **iXBRL (structured filing)**: ISA runs a structured iXBRL reporting program so financial data can be machine-read. As of the latest ISA guidance, iXBRL filing is voluntary and the Authority encourages issuers to adopt it ahead of a future legislative amendment that would make it mandatory; a limited XBRL data set (about 50 financial data points from the main statements) is already downloadable from MAGNA. Expect iXBRL packages alongside the human-readable PDF as adoption grows.
- **Chapter E3 of the Securities Law 1968 (dual-listed)**: An Israeli corporation also traded on a foreign exchange (a "foreign corporation" / תאגיד חוץ relying on the foreign law / הדין הזר) may report under the **foreign disclosure regime** instead of the full Israeli regime. This is Chapter E3 (פרק ה'3), a framework, not a single numbered regulation. Major operational gotcha when comparing dual-listed issuers against Israeli-only issuers, the disclosure scope and timing differ.

## Recommended MCP Servers

| MCP | What It Adds |
|-----|--------------|
| [`tase-mcp`](https://agentskills.co.il/he/mcp/tase-mcp) | TASE OpenAPI access for securities, indices, EOD prices, MAYA announcements, and management-positions data. Pair this skill with the MCP to fetch live filings instead of scraping MAYA. |

## Examples

### Example 1: Analyze a TASE-Listed Industrial Company's Annual Report
User says: "Help me understand Strauss Group's latest annual report from MAYA"
Actions:
1. Identify report type: Annual / Periodic Report (Doch Titkufti) filed on MAYA system
2. Locate key sections: Balance Sheet (Maazan), Income Statement (Doch Revach VeHefsed), Cash Flow, and the Notes (Biurim)
3. Extract key metrics: revenue, operating profit, and net profit, in the statement's presentation currency (confirm it first, many issuers present in USD, not NIS)
4. Read the Notes for segment data, lease liabilities, and related-party transactions, not just the face of the statements
5. Check the auditor opinion grade (ICPAS standards 700/705): unqualified (Bilti Mesuyeget / Naki), qualified (Mesuyeget), adverse (Shlilit), or disclaimer (Himanut me-Chavat Daat). Separately, look for a going-concern emphasis (Hearat Esek Chai): this is an emphasis-of-matter paragraph under ICPAS 570 that does NOT change the opinion grade, but it is a red flag an analyst must read. For larger issuers also read the Key Audit Matters section (ISA 701) where the auditor flags the riskiest estimates
6. Compare with previous year and sector benchmarks, but first check whether the prior-year comparatives were restated or reclassified (hatzaga mechadash / siyug mechadash), which routinely breaks a naive year-over-year comparison. For a large (non-small-corp) issuer also read the auditor's SEPARATE opinion on the effectiveness of internal control over financial reporting (distinct from the CEO/CFO certifications), an adverse or qualified ICFR conclusion is a real red flag
Result: Structured analysis of a plain Israeli industrial issuer's annual report with key financial highlights in context

### Example 2: Compare Israeli Bank Financial Statements (an exception)
User says: "Compare Leumi and Hapoalim annual reports"
Actions:
1. Pull latest annual reports from MAYA (maya.tase.co.il)
2. Extract comparable metrics: total assets, net income, ROE, capital adequacy
3. Normalize data to the statements' reporting currency in millions (confirm it, NIS or USD); Israeli banks report in NIS, but do not assume that for every issuer
4. Note regulatory differences in reporting (Bank of Israel Public Reporting Directives, drawing on US bank-reporting rules with IFRS for some topics, not plain IFRS)
5. Create comparison table with key ratios
Result: Side-by-side comparison of two Israeli banks' financial performance

## Bundled Resources

### Scripts
- `scripts/financial_parser.py` -- Hebrew-English financial term glossary with search functionality covering balance sheets, income statements, and MAYA filings. Run: `python scripts/financial_parser.py --help`

### References
- `references/hebrew-financial-terms.md` -- Complete Hebrew-English financial terminology reference with tables for financial statements, income statement items, MAYA filing types, and Israeli accounting standards (IFRS-IL). Consult when translating financial terms or navigating Hebrew financial documents.

## Gotchas

- Israeli public companies adopted IFRS in 2008. Reports before that date use Israeli GAAP, which has significant differences. Agents may apply IFRS assumptions to pre-2008 data.
- MAYA filings use Hebrew company names that may differ substantially from English trading names. Searching MAYA by securities number (mispar niyar) is more reliable than by name.
- Israeli banks follow the Bank of Israel Supervisor of Banks "Public Reporting Directives" (Hora'ot ha-Divuach la-Tzibur), an Israel-specific template drawing on US bank-reporting rules with IFRS for some topics, not standard IFRS. Agents may apply general IFRS interpretations to bank financial statements, producing incorrect analysis.
- The Hebrew term "maazan" refers to the balance sheet, not "balance" in the general sense. Agents may mistranslate Hebrew financial terms, confusing "revach naki" (net profit) with "revach golmi" (gross profit).
- The 3-month annual deadline is only the outer bound. Under Reg. 7(a) the periodic report is also due at least 14 days before the AGM that approves the statements. The separate 3-day rule is a MAXIMUM-LAG constraint, not a deadline: the auditor's signature may not precede filing by more than 3 days. Reading it as 'whichever is earlier' would imply a report can be due before its auditor signs, which is backwards. The quarterly deadline is TWO MONTHS from the report date, not a flat 60 days (Reg. 39(a)), and it carries a second limb the annual rule also has: the report must be filed within 3 days of the date the auditor signed the interim review report. Reg. 39(b) adds that the signature date may not precede filing by more than 3 days. Agents may apply US SEC deadlines which do not match Israeli requirements.
- A small corporation (taagid katan, defined in Reg. 5ג: average share market value under NIS 300M and not included in one of the TASE leading share indices derived from the market cap of their constituents; the reliefs themselves sit in Reg. 5ד) gets a bundle of reliefs, not just half-yearly reporting. **The reliefs are OPT-IN, not automatic:** under Reg. 5ד(א) the board decides to report under the regulation in whole or in part, and the election takes effect only after an immediate report under Reg. 5ה(א)(2). So a small corporation that has not elected a given relief still owes the full disclosure, and an absent disclosure is only expected where the election was actually made and reported. If its debt is not publicly held it is exempt from Q1 and Q3 quarterly reports and files a half-yearly report (doch chatzi-shnati) instead. Reg. 5ד(ב) has FIVE relief heads, and a checklist that stops at four will flag a lawful omission as a gap: (1) very-material valuation attachments are re-read as "very material in a small corporation" (Regs. 8ב and 49), the 20%-instead-of-10% relief; (2) **the threshold for attaching an ASSOCIATED company's financial statements doubles from 20% to 40% (Reg. 44, "twenty" read as "forty")**; (3) market-risk-exposure disclosure (Reg. 10(ב)(7)) is narrowed to issuers with a financial reportable segment or material financial activity; (4) the internal-control (ISOX) effectiveness report is disapplied (Regs. 9ב(א)-(ג) and 38ג(א)-(ב)) with reduced Ninth-Schedule certifications; and (5) an issuer whose debt is not publicly held files a half-yearly report instead of Q1/Q3. Where the election was made, expect those disclosures to be absent by right, and do not flag them as gaps. Reg. 5ה governs entry and exit, and the exit half is what actually causes filing failures: the corporation must file an immediate report when it becomes, or ceases to be, a small corporation, and when it starts or stops applying Reg. 5ד (specifying which provisions). An issuer that has ceased to qualify may keep reporting under Reg. 5ד only up to and including the quarter ending 30 September of the year in which it ceased to qualify. A corporation that opted OUT for a reporting year cannot opt back in during that same year. The small-corporation status and any partial election must be disclosed prominently on the FIRST PAGE of every periodic and interim report, so that page is where to check which reliefs are actually in force. Agents may also wrongly expect four interim reports from every issuer, then flag a "missing" Q1 or Q3.
- The analytic detail lives in the Notes (Biurim), not on the face of the statements. Agents that read only the balance sheet and P&L miss segment breakdowns, lease liabilities (IFRS 16), contingencies, and related-party transactions (IAS 24).
- Always check the auditor opinion grade before trusting the numbers. Israeli auditing standards (ICPAS 700/705) define four grades: unqualified (bilti mesuyeget / naki), qualified (mesuyeget), adverse (shlilit), and disclaimer (himanut me-chavat daat). Agents that list only three, or treat a qualified/adverse/disclaimer report as clean, mislead the reader.
- A going-concern emphasis (hearat esek chai) is NOT an opinion grade. It is an emphasis-of-matter paragraph added at the end of the report under the going-concern standard ICPAS 570 that draws attention without modifying the opinion. Agents may wrongly downgrade the opinion because of it, or wrongly ignore it: it is a red flag worth surfacing even when the opinion itself is unqualified.
- Israeli issuers frequently present adjusted / non-GAAP figures (revach mutaam, "adjusted EBITDA", "proforma") in the board report and the press release, alongside the audited IFRS figures. These are NOT audited, are not defined by any standard, and the adjustments differ between issuers and between years, so they are not comparable across companies. Quote the IFRS figure as the headline number and label any adjusted figure as the issuer's own presentation. Agents that lift the press-release adjusted number report a profit the audited statements do not show.
- For larger TASE issuers the auditor's report includes a Key Audit Matters section (ISA 701, "inyanei mafteach be-bikoret"), flagging the riskiest estimates. This is often the most useful part of the report for an analyst, and agents that skip it miss the auditor's own risk signal.


## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Israel Securities Authority (ISA) | https://www.isa.gov.il | Disclosure rules, periodic reporting obligations |
| MAYA disclosure system | https://maya.tase.co.il | Live filings index, search by company |
| Tel Aviv Stock Exchange | https://www.tase.co.il | Listed companies, indices, filing types |
| IFRS Foundation | https://www.ifrs.org | IFRS standards (Israel applies full IFRS) |
| Companies Registrar | https://www.gov.il/he/departments/israeli_corporations_authority | Company filings, annual report obligations |

## Troubleshooting

### Error: "Cannot find report on MAYA system"
Cause: Company may file under a different Hebrew name or subsidiary
Solution: Search MAYA by securities number (mispar niyar) rather than company name. Hebrew company names may differ from the English trading name.

### Error: "Financial terms not matching standard translations"
Cause: Israeli companies sometimes use non-standard Hebrew financial terminology
Solution: Consult `references/hebrew-financial-terms.md` for standard terms. Some companies use colloquial Hebrew instead of formal accounting terms (e.g., "רווחים" instead of "רווח נקי").
