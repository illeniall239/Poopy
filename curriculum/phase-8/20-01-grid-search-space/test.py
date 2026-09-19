import unittest

from sklearn.model_selection import ParameterGrid

from solution import grid


class TestGrid(unittest.TestCase):
    def test_hand_computed_order(self):
        self.assertEqual(grid({"lr": [0.1, 0.01], "depth": [2, 4, 8]}), [
            {"depth": 2, "lr": 0.1}, {"depth": 2, "lr": 0.01},
            {"depth": 4, "lr": 0.1}, {"depth": 4, "lr": 0.01},
            {"depth": 8, "lr": 0.1}, {"depth": 8, "lr": 0.01},
        ])

    def test_order_ignores_dict_insertion_order(self):
        a = grid({"b": [1, 2], "a": ["x", "y"], "c": [True]})
        b = grid({"c": [True], "a": ["x", "y"], "b": [1, 2]})
        self.assertEqual(a, b)
        self.assertEqual([list(d) for d in a][0], ["a", "b", "c"])

    def test_matches_sklearn_parameter_grid(self):
        space = {"reg": [0.0, 0.01, 0.1, 1.0], "kernel": ("rbf", "linear"), "degree": [2, 3], "shrink": [True, False]}
        expected = list(ParameterGrid(space))
        got = grid(space)
        self.assertEqual(len(got), 32)
        self.assertEqual(got, expected)

    def test_values_keep_their_given_order(self):
        self.assertEqual(grid({"k": [5, 1, 3]}), [{"k": 5}, {"k": 1}, {"k": 3}])

    def test_empty_space_is_one_empty_configuration(self):
        self.assertEqual(grid({}), [{}])

    def test_rejects_empty_or_non_list_values(self):
        with self.assertRaises(ValueError):
            grid({"lr": []})
        with self.assertRaises(ValueError):
            grid({"lr": 0.1})
        with self.assertRaises(ValueError):
            grid({"lr": [0.1], "name": "abc"})

    def test_dicts_are_independent(self):
        configs = grid({"a": [1], "b": [2, 3]})
        configs[0]["a"] = 99
        self.assertEqual(configs[1]["a"], 1)
        self.assertIsNot(configs[0], configs[1])


if __name__ == "__main__":
    unittest.main(verbosity=2)
