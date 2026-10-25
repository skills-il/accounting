# What credential scraping costs, and the licensed alternative

Detail for SKILL.md Step 2a.

Tell the user plainly what the scraping path involves, because it is not a read-only token:

- **You are handing full online-banking credentials to a script** that logs in as you through a headless browser. That is not the same as an API key, and it cannot be scoped or revoked independently of your own access.
- **Bank terms of service.** Israeli online-banking agreements generally restrict disclosing credentials to third parties and automated access. Doing it anyway can shift liability for fraudulent activity onto the customer. This is a contractual and risk question, not a criminal one, but it is real and the user should make the decision knowingly.
- **Lockout.** Repeated failed logins lock the account. Validate credentials before the run and stop on the first authentication failure.
- **Two-factor authentication.** Where the bank enforces 2FA on every login, unattended scraping largely does not work. The library's interface declares two-factor hooks, but only OneZero implements them (an OTP callback or a long-term token); every other scraper throws if they are called. Do not promise the user a config flag that does not exist.
- **The scraped data is sensitive at rest.** A full period of business transactions with counterparty names lands in local CSV/JSON. Keep it out of version control, restrict file permissions, and delete working copies when the reconciliation is signed off. For a business handling counterparty data this also engages Privacy Protection Law obligations.

**There is a licensed alternative, and for a business account it is the better production path.** Israel's Financial Information Service Law, 2021 (in force since 14 June 2022) established a regulated open-banking regime in which providers are licensed by the Israel Securities Authority and access account data through open interfaces **without the customer exposing their banking credentials**. The banks' duty to give access covered individuals first, small corporations (turnover up to NIS 5 million a year) from the end of January 2023, and all other corporations from 14 April 2024. Payment initiation is regulated separately, under a 2023 law. If the user is setting this up for an ongoing business process rather than a one-off, point them at a licensed aggregator before pointing them at a scraper.

**Business accounts.** Business online banking is often a separate portal with its own users and its own second factor, and the library's README does not say whether any scraper reaches a business portal. For a business account, start from the bank's own statement export and treat scraping as an experiment, not the plan.
