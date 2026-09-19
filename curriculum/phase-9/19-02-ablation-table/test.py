import copy
import unittest

from solution import ablation_table


def runs():
    return [
        {"name": "base", "seed": 0, "metrics": {"val_loss": 2.00, "val_acc": 0.60}},
        {"name": "no-dropout", "seed": 0, "metrics": {"val_loss": 2.25, "val_acc": 0.55}},
        {"name": "adamw", "seed": 1, "metrics": {"val_loss": 1.90, "val_acc": 0.63, "train_loss": 1.2}},
    ]


class TestAblationTable(unittest.TestCase):
    def assertDeltas(self, got, want):
        self.assertEqual(set(got), set(want))
        for k in want:
            self.assertAlmostEqual(got[k], want[k], delta=1e-9, msg=k)

    def test_rows_and_order(self):
        table = ablation_table(runs(), "base")
        self.assertEqual([row["name"] for row in table], ["no-dropout", "adamw"])
        self.assertDeltas(table[0]["deltas"], {"val_loss": 0.25, "val_acc": -0.05})
        self.assertDeltas(table[1]["deltas"], {"val_loss": -0.10, "val_acc": 0.03})

    def test_flags_seed_mismatch(self):
        table = ablation_table(runs(), "base")
        self.assertIs(table[0]["seed_differs"], False)
        self.assertIs(table[1]["seed_differs"], True)

    def test_baseline_need_not_be_first(self):
        rs = runs()
        table = ablation_table(rs, "no-dropout")
        self.assertEqual([row["name"] for row in table], ["base", "adamw"])
        self.assertDeltas(table[0]["deltas"], {"val_loss": -0.25, "val_acc": 0.05})
        self.assertDeltas(table[1]["deltas"], {"val_loss": -0.35, "val_acc": 0.08})
        self.assertEqual([row["seed_differs"] for row in table], [False, True])

    def test_only_baseline_metrics_are_compared(self):
        table = ablation_table(runs(), "base")
        self.assertNotIn("train_loss", table[1]["deltas"])

    def test_baseline_alone_gives_empty_table(self):
        self.assertEqual(ablation_table(runs()[:1], "base"), [])

    def test_does_not_modify_input(self):
        rs = runs()
        before = copy.deepcopy(rs)
        ablation_table(rs, "base")
        self.assertEqual(rs, before)

    def test_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            ablation_table(runs(), "baseline")
        dup = runs() + [{"name": "adamw", "seed": 0, "metrics": {"val_loss": 1.0, "val_acc": 0.7}}]
        with self.assertRaises(ValueError):
            ablation_table(dup, "base")
        missing = runs() + [{"name": "bn", "seed": 0, "metrics": {"val_loss": 1.8}}]
        with self.assertRaises(ValueError):
            ablation_table(missing, "base")


if __name__ == "__main__":
    unittest.main(verbosity=2)
