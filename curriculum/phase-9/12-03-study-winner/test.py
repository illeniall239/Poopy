import unittest

from solution import study_winner


def run(opt, lr, loss, steps=1000):
    metrics = {} if loss is None else {"val_loss": loss}
    return {"config": {"opt": opt, "lr": lr}, "steps": steps, "metrics": metrics}


RUNS = [
    run("sgd", 0.1, 0.50),
    run("sgd", 0.01, 0.40),
    run("adam", 0.01, 0.90),
    run("adam", 0.001, 0.35),
]


class TestStudyWinner(unittest.TestCase):
    def test_best_over_nuisance_not_average(self):
        winner, table = study_winner(RUNS, "opt", "val_loss")
        self.assertEqual(winner, "adam")
        self.assertEqual(set(table), {"sgd", "adam"})
        self.assertAlmostEqual(table["sgd"], 0.40)
        self.assertAlmostEqual(table["adam"], 0.35)

    def test_tie_broken_by_fewest_steps(self):
        runs = [run("sgd", 0.1, 0.3, steps=800), run("adam", 0.01, 0.3, steps=500)]
        self.assertEqual(study_winner(runs, "opt", "val_loss")[0], "adam")

    def test_tie_within_a_value_prefers_fewer_steps(self):
        runs = [run("sgd", 0.1, 0.3, steps=800), run("sgd", 0.01, 0.3, steps=200), run("adam", 0.01, 0.3, steps=500)]
        self.assertEqual(study_winner(runs, "opt", "val_loss")[0], "sgd")

    def test_full_tie_goes_to_the_best_run_listed_first(self):
        runs = [run("sgd", 0.1, 0.9), run("adam", 0.01, 0.3, 500), run("sgd", 0.01, 0.3, 500)]
        self.assertEqual(study_winner(runs, "opt", "val_loss")[0], "adam")

    def test_skips_nan_and_missing_metrics(self):
        runs = RUNS + [run("adam", 1.0, float("nan")), run("rmsprop", 0.1, None), run("lion", 0.1, float("nan"))]
        winner, table = study_winner(runs, "opt", "val_loss")
        self.assertEqual(winner, "adam")
        self.assertEqual(set(table), {"sgd", "adam"})

    def test_numeric_scientific_values(self):
        runs = [run("sgd", lr, loss) for lr, loss in [(0.1, 0.6), (0.01, 0.2), (0.001, 0.4), (0.01, 0.5)]]
        winner, table = study_winner(runs, "lr", "val_loss")
        self.assertEqual(winner, 0.01)
        self.assertEqual(set(table), {0.1, 0.01, 0.001})
        self.assertAlmostEqual(table[0.01], 0.2)

    def test_no_usable_runs(self):
        with self.assertRaises(ValueError):
            study_winner([], "opt", "val_loss")
        with self.assertRaises(ValueError):
            study_winner([run("sgd", 0.1, float("nan"))], "opt", "val_loss")


if __name__ == "__main__":
    unittest.main(verbosity=2)
