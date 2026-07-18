---
name: israeli-annual-reports
description: Navigate and analyze Israeli corporate annual reports (dochot titkuftiim), financial filings, and regulatory disclosures. Use when user asks about Israeli annual reports, MAYA filings, IFRS financial statements, doch titkufti, dochot kaspiyim, or Companies Law reporting requirements. Covers TASE filing types, Israeli GAAP to IFRS transition, Hebrew financial terminology, and key financial statement analysis.
license: MIT
compatibility: Works with Claude Code, Cursor, GitHub Copilot, Windsurf, OpenCode, Codex.
---


# Israeli Annual Reports

## Reporting Framework
Israeli public companies adopted IFRS in 2008. Prior reports use Israeli GAAP. Banks report under the Bank of Israel Supervisor of Banks "Public Reporting Directives" (Hora'ot ha-Divuach la-Tzibur), an Israel-specific template that draws on US bank-reporting rules and incorporates IFRS for some topics, not plain IFRS. For insurers, Israel postponed first-time IFRS 17 implementation to 1 January 2025 (the original global effective date was 2023).

**Check the reporting currency first, do not assume shekels.** Under IFRS a company reports in its functional / presentation currency (matbea hatzaga), and a large share of TASE issuers, especially tech and shipping names (e.g. ZIM, Tower, Nova, Camtek, Sapiens), present their statements in USD. Read the figures in the statement's own currency and convert only if the user explicitly needs another, forcing everything into NIS produces wrong numbers and wrong peer comparisons.

## Report Types and Deadlines
| Report | Deadline | Content |
|--------|----------|--------|
| Annual / Periodic (Doch Titkufti) | Within 3 months after year-end (outer bound); also at least 14 days before the AGM that approves the statements, or within 3 days of the auditor's opinion date, whichever is earlier | Audited financials, board report |
| Quarterly (Doch Rivoni) | 60 days (about 2 months) after quarter | Reviewed interim financials |
| Half-Yearly (Doch Chatzi-Shnati) | About 60 days after H1 | Reviewed interim financials, filed by small corporations (taagid katan) without public debt in place of Q1/Q3 reports |
| Immediate (Doch Miyadi) | Hours after event | Material events |
| Shelf Prospectus | Valid up to 3 years | Securities offering framework |

**Reviewed vs. audited (critical distinction):** only the ANNUAL statements are audited. The quarterly and half-yearly interim statements are REVIEWED (sekira) under the auditor's interim-review standard, which is LIMITED assurance ("nothing came to our attention"), not a full audit. Do not treat interim numbers as if they were audited.

## Annual Report Structure
- Part A: Description of Business (operations, markets, risks)
- Part B: Board Report (MD&A, financial review)
- Part C: Financial Statements (balance sheet, P&L, cash flow, statement of changes in equity (Doch al ha-Shinuyim ba-Hon), and the Notes / Biurim)
  - In the Notes (Biurim), read: segment data, IFRS 16 lease liabilities, contingencies and provisions, related-party disclosures (IAS 24), and subsequent events. The analytic detail lives in the Notes, not on the face of the statements.
- Part D: Additional Information (officer compensation, shareholder-approved remuneration policy, audit committee). Part D also carries the CEO and CFO management certifications (hatzharot menahalim) on the financial statements and on disclosure controls, the Israeli analogue of the US SOX management certification. In an ISOX-exempt small corporation the CEO/CFO still file a reduced certification on the financial statements themselves; only the disclosure-controls / internal-control-effectiveness portions are removed, and that reduction is itself a signal about the issuer's size/status.
- Consolidated vs. separate/solo: an Israeli periodic report carries BOTH the consolidated (me'uchad) group statements AND a mandated separate/solo (nifrad) data section for the parent alone. Default headline analysis to the CONSOLIDATED figures. Grabbing the parent-only solo revenue/net profit materially misstates a holding company (and TASE is heavy with pyramidal holding structures).
- ESG / sustainability: modern Israeli annual reports increasingly carry ESG and climate-risk disclosures. The ISA maintains a voluntary ESG/climate disclosure framework, and mandatory sustainability reporting is under active debate. Look for (and do not assume the absence of) an ESG or climate-risk section.

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
- Sec. 267-269: Audit-committee requirements
- Sec. 270-275: Related-party transaction approvals (cross-reference IAS 24 disclosure)

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
5. Check the auditor opinion grade (ICPAS standards 700/705): unqualified (Bilti Mesuyeget / Naki), qualified (Mesuyeget), adverse (Shlilit), or disclaimer (Himanut me-Chavat Daat). Separately, look for a going-concern emphasis (Hearat Esek Chai): this is an emphasis-of-matter paragraph (ICPAS 706/570) that does NOT change the opinion grade, but it is a red flag an analyst must read. For larger issuers also read the Key Audit Matters section (ISA 701) where the auditor flags the riskiest estimates
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
- The 3-month annual deadline is only the outer bound. Under Reg. 7(a) the periodic report is also due at least 14 days before the AGM that approves the statements, or within 3 days of the auditor's opinion date, whichever is earlier. Quarterly is 60 days (about 2 months). Agents may apply US SEC deadlines which do not match Israeli requirements.
- A small corporation (taagid katan, defined in Reg. 5d: not in the TA-100 or TA-Beyond-50 index, with average share market value under NIS 300M) gets a bundle of reliefs, not just half-yearly reporting. If its debt is not publicly held it is exempt from Q1 and Q3 quarterly reports and files a half-yearly report (doch chatzi-shnati) instead. It is also exempt from the internal-control (ISOX) report, gets a raised valuation-attachment materiality threshold (20% instead of 10%), and gets market-risk-disclosure relief. Expect those disclosures to be absent by right, do not flag them as gaps. Agents may also wrongly expect four interim reports from every issuer, then flag a "missing" Q1 or Q3.
- The analytic detail lives in the Notes (Biurim), not on the face of the statements. Agents that read only the balance sheet and P&L miss segment breakdowns, lease liabilities (IFRS 16), contingencies, and related-party transactions (IAS 24).
- Always check the auditor opinion grade before trusting the numbers. Israeli auditing standards (ICPAS 700/705) define four grades: unqualified (bilti mesuyeget / naki), qualified (mesuyeget), adverse (shlilit), and disclaimer (himanut me-chavat daat). Agents that list only three, or treat a qualified/adverse/disclaimer report as clean, mislead the reader.
- A going-concern emphasis (hearat esek chai) is NOT an opinion grade. It is an emphasis-of-matter paragraph (ICPAS 706, sourced from the going-concern standard ICPAS 570) that draws attention without modifying the opinion. Agents may wrongly downgrade the opinion because of it, or wrongly ignore it: it is a red flag worth surfacing even when the opinion itself is unqualified.
- For larger TASE issuers the auditor's report includes a Key Audit Matters section (ISA 701, "inyanei mafteach be-bikoret"), flagging the riskiest estimates. This is often the most useful part of the report for an analyst, and agents that skip it miss the auditor's own risk signal.


## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Israel Securities Authority (ISA) | https://www.isa.gov.il | Disclosure rules, periodic reporting obligations |
| MAYA disclosure system | https://maya.tase.co.il | Live filings index, search by company |
| Tel Aviv Stock Exchange | https://www.tase.co.il | Listed companies, indices, filing types |
| IFRS Foundation | https://www.ifrs.org | IFRS standards (Israel applies full IFRS) |
| Companies Registrar | https://www.gov.il/he/departments/corporations_authority | Company filings, annual report obligations |

## Troubleshooting

### Error: "Cannot find report on MAYA system"
Cause: Company may file under a different Hebrew name or subsidiary
Solution: Search MAYA by securities number (mispar niyar) rather than company name. Hebrew company names may differ from the English trading name.

### Error: "Financial terms not matching standard translations"
Cause: Israeli companies sometimes use non-standard Hebrew financial terminology
Solution: Consult `references/hebrew-financial-terms.md` for standard terms. Some companies use colloquial Hebrew instead of formal accounting terms (e.g., "רווחים" instead of "רווח נקי").
