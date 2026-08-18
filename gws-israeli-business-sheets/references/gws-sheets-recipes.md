# GWS CLI Sheets Recipes

Common recipes for Google Sheets operations using the Google Workspace CLI (`gws`, package `@googleworkspace/cli`).

The `gws` command surface is generated dynamically from Google's Discovery API. There is no `gws sheets create` or `gws sheets read` command. Every Sheets operation is either a raw API method (`gws sheets spreadsheets <method> --params '<JSON>' [--json '<body>']`) or one of the two helper shortcuts (`gws sheets +read`, `gws sheets +append`). When in doubt, run `gws sheets --help`, `gws sheets spreadsheets --help`, or `gws schema sheets.spreadsheets.values.get`.

## Installation and Setup

```bash
# Install globally
npm install -g @googleworkspace/cli

# Or use via npx (no install needed)
npx @googleworkspace/cli sheets --help

# Authenticate
gws auth login

# Check auth status
gws auth status
```

## Core Commands

### Create a New Spreadsheet

```bash
# Create with a title (the response JSON includes "spreadsheetId")
gws sheets spreadsheets create --json '{"properties":{"title":"My Spreadsheet"}}'
```

### Read Data

```bash
# Helper: read a range (returns the raw values array)
gws sheets +read --spreadsheet SHEET_ID --range "Sheet1!A1:D10"

# Helper: read an entire sheet tab
gws sheets +read --spreadsheet SHEET_ID --range "Sheet1"

# Raw API: read a range (response is a ValueRange with a "values" array)
gws sheets spreadsheets values get --params '{"spreadsheetId":"SHEET_ID","range":"Sheet1!A:J"}'

# Read as CSV (use the --format flag, not a fabricated --output flag)
gws sheets spreadsheets values get --params '{"spreadsheetId":"SHEET_ID","range":"Sheet1!A:J"}' --format csv
```

### Append Data

```bash
# Helper: append a single simple row
gws sheets +append --spreadsheet SHEET_ID --values 'value1,value2,value3,value4'

# Helper: append multiple rows
gws sheets +append --spreadsheet SHEET_ID --json-values '[["r1c1","r1c2"],["r2c1","r2c2"]]'

# Raw API: append rows (valueInputOption is required)
gws sheets spreadsheets values append \
  --params '{"spreadsheetId":"SHEET_ID","range":"Sheet1!A:D","valueInputOption":"USER_ENTERED"}' \
  --json '{"values":[["value1","value2","value3","value4"]]}'

# Dry run (preview without writing)
gws sheets spreadsheets values append \
  --params '{"spreadsheetId":"SHEET_ID","range":"Sheet1!A:D","valueInputOption":"USER_ENTERED"}' \
  --json '{"values":[["test","data"]]}' --dry-run
```

### Write to a Specific Range

```bash
# Overwrite a range (e.g. write a header row)
gws sheets spreadsheets values update \
  --params '{"spreadsheetId":"SHEET_ID","range":"Sheet1!A1:D1","valueInputOption":"RAW"}' \
  --json '{"values":[["Date","Description","Amount","Notes"]]}'
```

### Add a New Sheet Tab

```bash
gws sheets spreadsheets batchUpdate \
  --params '{"spreadsheetId":"SHEET_ID"}' \
  --json '{"requests":[{"addSheet":{"properties":{"title":"Summary"}}}]}'
```

## Recipes

### Recipe: Backup All Tabs as CSV

```bash
# Export each named tab to its own CSV file
for tab in "Sheet1" "Sheet2" "Summary"; do
  gws sheets spreadsheets values get \
    --params "{\"spreadsheetId\":\"SHEET_ID\",\"range\":\"$tab\"}" --format csv > "${tab}.csv"
done
```

### Recipe: Copy a Header Row to a New Month Tab

```bash
# Read headers from the current month (the response has a "values" array)
HEADERS=$(gws sheets spreadsheets values get \
  --params '{"spreadsheetId":"SHEET_ID","range":"Jan-2026!A1:J1"}' | jq -c '.values')

# Write those headers into the new month tab
gws sheets spreadsheets values update \
  --params '{"spreadsheetId":"SHEET_ID","range":"Feb-2026!A1:J1","valueInputOption":"RAW"}' \
  --json "{\"values\":$HEADERS}"
```

### Recipe: Compare Two Sheet Tabs

```bash
# Export both tabs as CSV and diff
gws sheets spreadsheets values get --params '{"spreadsheetId":"SHEET_ID","range":"Sheet1!A:J"}' --format csv > tab1.csv
gws sheets spreadsheets values get --params '{"spreadsheetId":"SHEET_ID","range":"Sheet2!A:J"}' --format csv > tab2.csv
diff tab1.csv tab2.csv
```

### Recipe: Filter Rows by Category

The `values get` response is a ValueRange: `{"range":"...","majorDimension":"ROWS","values":[[...],[...]]}`. The `values` field is an array of rows, each row an array of cell strings. Use `jq` against `.values` to filter. With the column order from the SKILL.md sheet structure, column C (index 2) is Category:

```bash
# Read all data, then keep only rows where the Category column equals "Professional Services"
gws sheets spreadsheets values get --params '{"spreadsheetId":"SHEET_ID","range":"Sheet1!A:J"}' \
  | jq -c '.values[] | select(.[2] == "Professional Services")'
```

### Recipe: Count Rows by Type

Column G (index 6) is the Type column (Income/Expense):

```bash
# Read the Type column and count income vs expense rows
gws sheets spreadsheets values get --params '{"spreadsheetId":"SHEET_ID","range":"Sheet1!G:G"}' \
  | jq '.values[1:] | group_by(.[0]) | map({type: .[0][0], count: length})'
```

## Common Range Notations

| Range | Meaning |
|-------|---------|
| `Sheet1!A1:J1` | First row, columns A through J |
| `Sheet1!A:J` | All rows, columns A through J |
| `Sheet1!A2:J` | All rows starting from row 2 (skip headers) |
| `Sheet1` | Entire sheet |
| `'VAT Period 1'!A:D` | Sheet with spaces in name (use quotes) |

## Tips

- Always use `--dry-run` before appending to production sheets.
- The default output format is `json`. Use `--format csv` when exporting for accountants or external tools, or `--format table` for a quick human-readable view.
- Spreadsheet ID is the long string in the Google Sheets URL between `/d/` and `/edit`.
- A `values get` / `+read` response is the raw Sheets API `ValueRange` object. The cell data lives under the `values` key as an array of arrays. Parse with `jq '.values'`, not by assuming named columns.
- `valueInputOption` is required on `values append` and `values update`. Use `USER_ENTERED` to let Sheets interpret dates and numbers, or `RAW` to store strings verbatim.
