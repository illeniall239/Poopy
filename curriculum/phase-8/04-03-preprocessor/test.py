import math
import unittest

import numpy as np

from solution import Preprocessor

SPEC = {
    "age": {"kind": "numeric"},
    "income": {"kind": "log"},
    "hour": {"kind": "bucket", "boundaries": [6, 12, 18]},
    "city": {"kind": "category"},
}
TRAIN = [
    {"age": 20, "income": 0, "hour": 5, "city": "Paris"},
    {"age": 30, "income": 9, "hour": 12, "city": "Lahore"},
    {"age": 40, "income": 99, "hour": 23, "city": "Paris"},
]
Z = -math.sqrt(1.5)  # (20 - 30) / sqrt(200/3) and (0 - ln 10) / (ln 10 * sqrt(2/3))


def random_rows(n, seed, age_shift=0.0, cities=("a", "b", "c")):
    rng = np.random.default_rng(seed)
    return [
        {"age": float(rng.normal(40 + age_shift, 10)), "income": float(rng.lognormal(10, 1)),
         "hour": float(rng.uniform(0, 24)), "city": str(rng.choice(cities)), "id": i}
        for i in range(n)
    ]


class TestPreprocessor(unittest.TestCase):
    def test_worked_example(self):
        p = Preprocessor(SPEC)
        self.assertIs(p.fit(TRAIN), p)
        out = p.transform(TRAIN)
        self.assertEqual(out.shape, (3, 9))
        np.testing.assert_allclose(out[0], [Z, Z, 1, 0, 0, 0, 0, 1, 0], atol=1e-9)
        np.testing.assert_allclose(out[1], [0, 0, 0, 0, 1, 0, 1, 0, 0], atol=1e-9)
        np.testing.assert_allclose(out[2], [-Z, -Z, 0, 0, 0, 1, 0, 1, 0], atol=1e-9)

    def test_unseen_category_and_boundary_value(self):
        p = Preprocessor(SPEC).fit(TRAIN)
        out = p.transform([{"age": 30, "income": 9, "hour": 18, "city": "Oslo"}])
        np.testing.assert_allclose(out, [[0, 0, 0, 0, 0, 1, 0, 0, 1]], atol=1e-9)

    def test_vocabulary_is_sorted_not_first_seen(self):
        p1 = Preprocessor({"c": {"kind": "category"}}).fit([{"c": "z"}, {"c": "a"}, {"c": "m"}])
        p2 = Preprocessor({"c": {"kind": "category"}}).fit([{"c": "m"}, {"c": "z"}, {"c": "a"}])
        rows = [{"c": "a"}, {"c": "m"}, {"c": "z"}]
        np.testing.assert_array_equal(p1.transform(rows), [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]])
        np.testing.assert_array_equal(p1.transform(rows), p2.transform(rows))

    def test_transform_never_recomputes_statistics(self):
        train = random_rows(500, seed=0)
        test = random_rows(200, seed=1, age_shift=25.0, cities=("a", "b", "d"))
        p = Preprocessor(SPEC).fit(train)
        batch = p.transform(test)
        for i in (0, 57, 199):
            np.testing.assert_allclose(p.transform([test[i]])[0], batch[i], atol=1e-12)
        ages = np.array([r["age"] for r in train])
        expected_age = (np.array([r["age"] for r in test]) - ages.mean()) / ages.std()
        np.testing.assert_allclose(batch[:, 0], expected_age, atol=1e-9)
        self.assertGreater(batch[:, 0].mean(), 2.0)  # the test rows really are older than train
        incomes = np.log1p([r["income"] for r in train])
        expected_income = (np.log1p([r["income"] for r in test]) - incomes.mean()) / incomes.std()
        np.testing.assert_allclose(batch[:, 1], expected_income, atol=1e-9)

    def test_train_numeric_columns_are_standardized(self):
        train = random_rows(1000, seed=2)
        out = Preprocessor(SPEC).fit(train).transform(train)
        self.assertEqual(out.shape, (1000, 1 + 1 + 4 + 4))
        np.testing.assert_allclose(out[:, :2].mean(axis=0), 0.0, atol=1e-9)
        np.testing.assert_allclose(out[:, :2].std(axis=0), 1.0, atol=1e-9)
        np.testing.assert_allclose(out[:, 2:].sum(axis=1), 2.0)

    def test_constant_column_and_empty_transform(self):
        p = Preprocessor({"x": {"kind": "numeric"}, "c": {"kind": "category"}}).fit([{"x": 4, "c": "a"}, {"x": 4, "c": "a"}])
        np.testing.assert_allclose(p.transform([{"x": 6, "c": "a"}]), [[2.0, 1.0, 0.0]])
        self.assertEqual(p.transform([]).shape, (0, 3))

    def test_spec_errors(self):
        for bad in ({}, {"x": {"kind": "ordinal"}}, {"x": {"kind": "bucket"}},
                    {"x": {"kind": "bucket", "boundaries": []}}, {"x": {"kind": "bucket", "boundaries": [3, 1]}}):
            with self.assertRaises(ValueError):
                Preprocessor(bad)

    def test_data_errors(self):
        with self.assertRaises(RuntimeError):
            Preprocessor(SPEC).transform(TRAIN)
        with self.assertRaises(ValueError):
            Preprocessor(SPEC).fit([])
        with self.assertRaises(ValueError):
            Preprocessor(SPEC).fit([{"age": 1, "income": 1, "hour": 1}])
        with self.assertRaises(ValueError):
            Preprocessor(SPEC).fit([{"age": 1, "income": -5, "hour": 1, "city": "a"}])
        p = Preprocessor(SPEC).fit(TRAIN)
        with self.assertRaises(ValueError):
            p.transform([{"age": 1, "hour": 1, "city": "a"}])
        with self.assertRaises(ValueError):
            p.transform([{"age": 1, "income": -1, "hour": 1, "city": "a"}])


if __name__ == "__main__":
    unittest.main(verbosity=2)
