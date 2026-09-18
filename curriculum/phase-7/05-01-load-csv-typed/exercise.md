# Load a typed CSV

Topic: 5. pandas DataFrames and loading data
Difficulty: 1 of 3

## Problem

Write `load_typed_csv(text: str, date_columns: list[str]) -> pd.DataFrame` that reads CSV text (a string, not a file) with `pd.read_csv` and repairs the dtype inference that real exports break:

- Cells that are empty, `NA` or `n/a` (any capitalization, surrounding spaces allowed) become `NaN`.
- Every column named in `date_columns` is parsed to a datetime dtype; an unparseable cell becomes `NaT`.
- Any remaining string column whose non-missing cells all look like numbers once you strip a leading `$` and thousands separators (`,`) — for example `$1,200.50` or `-3,000` — becomes a float column. Columns with genuine text (or a mix of text and numbers) stay as text.
- Columns that pandas already inferred as numeric are left as they are.

Return a new DataFrame; column order is the CSV's. pandas is required; `io.StringIO` from the standard library wraps the text.

## Examples

```
text = "id,name,amount,signup,score\n"
       "1,Ann,\"$1,200.50\",2024-01-05,3\n"
       "2,Bob,n/a,2024-02-30,NA\n"
       "3,,$-40,,7\n"

df = load_typed_csv(text, ["signup"])
df.dtypes  → id int64, name object, amount float64, signup datetime64[ns], score float64
df["amount"].tolist()   → [1200.5, nan, -40.0]
df["signup"].isna().tolist()  → [False, True, True]     Feb 30 is NaT
df["name"].isna().tolist()    → [False, False, True]
```

## Constraints

- Up to 10 000 rows; vectorized string methods (`.str.replace`, `pd.to_numeric`, `pd.to_datetime`) rather than row loops.
- `"NA"` inside a text column is missing, not the string `"NA"`.
- Do not raise on unparseable dates; use `errors="coerce"`.

## Hints

1. `pd.read_csv` accepts a file-like object. Which standard-library class makes a string behave like one? Which `read_csv` argument lists the strings that mean missing?
2. `pd.to_numeric(..., errors="coerce")` turns anything unparseable into `NaN`. How could you tell "every non-missing cell parsed" from "some text cell became `NaN`"?
3. Which string cleaning must happen before `pd.to_numeric` for `"$1,200.50"` to parse? Does `.str.replace` treat the pattern as a regex by default?
4. `pd.to_datetime` with `errors="coerce"` returns `NaT` for `2024-02-30`. What dtype does `df.dtypes` show for that column afterwards?

## Explain-back

- Why did pandas read `amount` as a string column rather than failing loudly? Which is the better failure mode for a data pipeline, and why?
- `NaN == NaN` is `False`. How do you count missing values in a column, and why does `df[df.col == np.nan]` never match?
- A 10 GB table with typed columns and dates arrives every day. Would you store it as CSV, JSON or Parquet? Name one thing CSV loses.
- `df[df.amount > 0]` was run and `df` still has negative rows. What did that expression return, and what would mutate `df`?
