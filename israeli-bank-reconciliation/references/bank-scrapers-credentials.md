# israeli-bank-scrapers credential fields

Authoritative source: the `SCRAPERS` map in the library's
`src/definitions.ts` (https://raw.githubusercontent.com/eshaham/israeli-bank-scrapers/master/src/definitions.ts).
Read that file, not the README prose: the two disagree for `amex`, where the
README says `username` and the code declares `id`.

## Full provider table (19 CompanyTypes members)

| Provider | Credential fields |
|---|---|
| `hapoalim` | `userCode`, `password` |
| `leumi`, `mizrahi`, `otsarHahayal`, `beinleumi`, `massad`, `max`, `visaCal`, `union`, `pagi` | `username`, `password` |
| `discount`, `mercantile` | `id`, `password`, `num` |
| `isracard`, `amex` | `id`, `card6Digits`, `password` |
| `yahav` | `username`, `nationalID`, `password` |
| `behatsdaa`, `beyahadBishvilha` | `id`, `password` |
| `oneZero` | `email`, `password`, `otpCodeRetriever`, `phoneNumber`, `otpLongTermToken` |

`oneZero` cannot be built from environment variables: `otpCodeRetriever` is a
`() => Promise<string>` function, not a string.

## Builder

Note the fail-closed default. Falling through to `['username','password']` for an
unrecognised `companyId` posts a well-formed but wrong-shaped credential to the
bank; the login fails and counts toward account lockout, which is the exact harm
the skill warns about. Throw instead.

```javascript
const { CompanyTypes } = require('israeli-bank-scrapers');

// Field list per provider. Copy from the library README for your provider before
// running; these can change between major versions.
const CREDENTIAL_FIELDS = {
  [CompanyTypes.hapoalim]:   ['userCode', 'password'],
  [CompanyTypes.discount]:   ['id', 'password', 'num'],
  [CompanyTypes.mercantile]: ['id', 'password', 'num'],
  [CompanyTypes.isracard]:   ['id', 'card6Digits', 'password'],
  [CompanyTypes.amex]:       ['id', 'card6Digits', 'password'],
  [CompanyTypes.yahav]:      ['username', 'nationalID', 'password'],
  [CompanyTypes.behatsdaa]:  ['id', 'password'],
  [CompanyTypes.beyahadBishvilha]: ['id', 'password'],
};
// Every provider NOT listed above uses ['username','password'] per the library's
// SCRAPERS map. Do NOT fall through silently for an unknown companyId: guessing
// the shape posts a well-formed but wrong credential to the bank, and repeated
// failed logins lock the account. Fail closed instead.
const DEFAULT_FIELDS = ['username', 'password'];
const KNOWN_DEFAULT = new Set(['leumi','mizrahi','otsarHahayal','beinleumi',
  'massad','max','visaCal','union','pagi']);

// Build credentials in code, from the environment, matching the provider's shape.
function credentialsFor(account) {
  let fields = CREDENTIAL_FIELDS[account.companyId];
  if (!fields) {
    if (!KNOWN_DEFAULT.has(account.companyId)) {
      throw new Error(
        `Unknown companyId "${account.companyId}": refusing to guess its credential ` +
        `fields. Check SCRAPERS in the library's src/definitions.ts and add it above.`);
    }
    fields = DEFAULT_FIELDS;
  }
  const creds = {};
  for (const field of fields) {
    const envName = `${account.credentialsEnvPrefix}_${field.toUpperCase()}`;
    const value = process.env[envName];
    if (!value) {
      throw new Error(`Missing ${envName}. Set it before running; do NOT put secrets in the config file.`);
    }
    creds[field] = value;
  }
  return creds;
}
```

## Other ScraperOptions worth knowing for a reconciliation

- `futureMonthsToScrape` pulls forward-dated card charges into the result set,
  so rows can appear with dates after the period you asked for.
- `outputData.enableTransactionsFilterByDate` switches off the library's own
  date filtering, so the caller must filter.
- `identifier` is typed `string | number | undefined` in `src/transactions.ts`,
  so coerce with `String(txn.identifier)` before comparing.
