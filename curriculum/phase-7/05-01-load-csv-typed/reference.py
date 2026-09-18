# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import io

import pandas as pd


def load_typed_csv(text: str, date_columns: list[str]) -> pd.DataFrame:
    df = pd.read_csv(io.StringIO(text), na_values=["", "NA", "na", "n/a", "N/A"], skipinitialspace=True)
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    for col in df.columns:
        if col in date_columns or not pd.api.types.is_string_dtype(df[col]):
            continue
        cleaned = df[col].str.strip().str.replace(r"^\$", "", regex=True).str.replace(",", "", regex=False)
        nums = pd.to_numeric(cleaned, errors="coerce")
        if nums.isna().sum() == df[col].isna().sum():
            df[col] = nums.astype(float)
    return df
