import math
import unittest

import pandas as pd

from solution import load_typed_csv

TEXT = (
    "id,name,amount,signup,score\n"
    '1,Ann,"$1,200.50",2024-01-05,3\n'
    "2,Bob,n/a,2024-02-30,NA\n"
    "3,,$-40,,7\n"
)


class TestLoadTypedCsv(unittest.TestCase):
    def setUp(self):
        self.df = load_typed_csv(TEXT, ["signup"])

    def test_returns_dataframe_with_csv_columns(self):
        self.assertIsInstance(self.df, pd.DataFrame)
        self.assertEqual(list(self.df.columns), ["id", "name", "amount", "signup", "score"])
        self.assertEqual(len(self.df), 3)

    def test_money_column_becomes_float(self):
        self.assertTrue(pd.api.types.is_float_dtype(self.df["amount"]))
        vals = self.df["amount"].tolist()
        self.assertAlmostEqual(vals[0], 1200.5)
        self.assertTrue(math.isnan(vals[1]))
        self.assertAlmostEqual(vals[2], -40.0)

    def test_missing_markers_become_nan(self):
        self.assertEqual(self.df["name"].isna().tolist(), [False, False, True])
        self.assertEqual(self.df["score"].isna().tolist(), [False, True, False])
        self.assertAlmostEqual(self.df["score"].iloc[2], 7.0)

    def test_dates_parsed_with_nat_on_failure(self):
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(self.df["signup"]))
        self.assertEqual(self.df["signup"].isna().tolist(), [False, True, True])
        self.assertEqual(self.df["signup"].iloc[0], pd.Timestamp("2024-01-05"))

    def test_text_column_stays_text(self):
        self.assertEqual(self.df["name"].iloc[0], "Ann")
        self.assertTrue(pd.api.types.is_string_dtype(self.df["name"]))

    def test_already_numeric_untouched(self):
        self.assertTrue(pd.api.types.is_integer_dtype(self.df["id"]))
        self.assertEqual(self.df["id"].tolist(), [1, 2, 3])

    def test_thousands_without_dollar_and_case_insensitive_na(self):
        df = load_typed_csv("qty,city\n\"3,000\",Oslo\nN/A,na\n\"1,5\",Rome\n", [])
        self.assertTrue(pd.api.types.is_float_dtype(df["qty"]))
        self.assertAlmostEqual(df["qty"].iloc[0], 3000.0)
        self.assertTrue(math.isnan(df["qty"].iloc[1]))
        self.assertAlmostEqual(df["qty"].iloc[2], 15.0)
        self.assertEqual(df["city"].isna().tolist(), [False, True, False])

    def test_mixed_text_and_numbers_not_coerced(self):
        df = load_typed_csv("code\n$12\nABC\n", [])
        self.assertEqual(df["code"].tolist(), ["$12", "ABC"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
