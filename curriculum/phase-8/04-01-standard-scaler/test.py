import unittest

import numpy as np
from sklearn.preprocessing import StandardScaler as SkScaler

from solution import StandardScaler


def split_data(seed):
    rng = np.random.default_rng(seed)
    train = rng.normal([10.0, -3.0, 1000.0], [2.0, 0.5, 300.0], size=(200, 3))
    test = rng.normal([14.0, -2.0, 500.0], [1.0, 1.0, 100.0], size=(50, 3))
    return train, test


class TestStandardScaler(unittest.TestCase):
    def test_fit_returns_self_and_stores_stats(self):
        s = StandardScaler()
        self.assertIs(s.fit(np.array([[1.0, 5.0], [3.0, 5.0]])), s)
        np.testing.assert_allclose(s.mean_, [2.0, 5.0])
        np.testing.assert_allclose(s.scale_, [1.0, 1.0])

    def test_train_becomes_mean_zero_std_one(self):
        train, _ = split_data(0)
        z = StandardScaler().fit(train).transform(train)
        np.testing.assert_allclose(z.mean(axis=0), 0.0, atol=1e-12)
        np.testing.assert_allclose(z.std(axis=0), 1.0, atol=1e-12)

    def test_test_rows_use_train_statistics(self):
        train, test = split_data(1)
        z = StandardScaler().fit(train).transform(test)
        expected = (test - train.mean(axis=0)) / train.std(axis=0)
        np.testing.assert_allclose(z, expected, rtol=1e-12)
        # Refitting on the test rows would make these means 0; with train statistics they are far from it.
        self.assertTrue(np.all(np.abs(z.mean(axis=0)) > 0.5))

    def test_single_row_is_not_rescaled_by_itself(self):
        s = StandardScaler().fit(np.array([[1.0, 5.0], [3.0, 5.0]]))
        np.testing.assert_allclose(s.transform(np.array([[7.0, 9.0]])), [[5.0, 4.0]])
        np.testing.assert_allclose(s.transform(np.array([[1.0, 5.0]])), [[-1.0, 0.0]])

    def test_zero_variance_column(self):
        train = np.array([[1.0, 4.0], [2.0, 4.0], [3.0, 4.0]])
        s = StandardScaler().fit(train)
        z = s.transform(train)
        self.assertTrue(np.all(np.isfinite(z)))
        np.testing.assert_allclose(z[:, 1], 0.0)
        np.testing.assert_allclose(s.transform(np.array([[2.0, 6.0]])), [[0.0, 2.0]])

    def test_matches_sklearn_and_does_not_mutate(self):
        train, test = split_data(2)
        ours = StandardScaler().fit(train)
        theirs = SkScaler().fit(train)
        test_copy = test.copy()
        np.testing.assert_allclose(ours.transform(test), theirs.transform(test), rtol=1e-12, atol=1e-12)
        np.testing.assert_array_equal(test, test_copy)
        np.testing.assert_allclose(ours.scale_, theirs.scale_, rtol=1e-12)

    def test_integer_input_gives_float_output(self):
        s = StandardScaler().fit(np.array([[1, 2], [3, 6]]))
        z = s.transform(np.array([[2, 4]]))
        self.assertEqual(z.dtype.kind, "f")
        np.testing.assert_allclose(z, [[0.0, 0.0]])

    def test_errors(self):
        with self.assertRaises(RuntimeError):
            StandardScaler().transform(np.ones((1, 2)))
        with self.assertRaises(ValueError):
            StandardScaler().fit(np.ones(3))
        with self.assertRaises(ValueError):
            StandardScaler().fit(np.ones((0, 3)))
        s = StandardScaler().fit(np.ones((2, 3)))
        with self.assertRaises(ValueError):
            s.transform(np.ones((2, 2)))
        with self.assertRaises(ValueError):
            s.transform(np.ones(3))


if __name__ == "__main__":
    unittest.main(verbosity=2)
