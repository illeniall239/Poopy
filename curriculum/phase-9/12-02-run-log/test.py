import unittest

from solution import RunLog


def sample_log():
    log = RunLog()
    log.start("base", {"lr": 0.1, "bs": 32}, seed=0, code_version="a1b2c3")
    log.start("lr01", {"lr": 0.01, "bs": 32}, seed=0, code_version="a1b2c3")
    log.log("base", 1, {"val_loss": 0.9, "acc": 0.6})
    log.log("base", 2, {"val_loss": 0.7, "acc": 0.7})
    log.log("lr01", 1, {"val_loss": 0.8})
    log.log("lr01", 2, {"val_loss": 0.5})
    return log


class TestRunLog(unittest.TestCase):
    def test_best_min_and_max(self):
        log = sample_log()
        self.assertEqual(log.best("val_loss"), ("lr01", 2, 0.5))
        self.assertEqual(log.best("acc", mode="max"), ("base", 2, 0.7))
        self.assertEqual(log.best("acc", mode="min"), ("base", 1, 0.6))

    def test_best_ties_go_to_first_run_then_earliest_step(self):
        log = RunLog()
        log.start("a", {}, 0, "v1")
        log.start("b", {}, 0, "v1")
        log.log("b", 1, {"loss": 0.3})
        log.log("a", 5, {"loss": 0.4})
        log.log("a", 6, {"loss": 0.3})
        log.log("a", 7, {"loss": 0.3})
        self.assertEqual(log.best("loss"), ("a", 6, 0.3))

    def test_compare_reports_changed_config_and_deltas(self):
        out = sample_log().compare("base", "lr01")
        self.assertEqual(out["changed"], {"lr": (0.1, 0.01)})
        self.assertEqual(set(out["deltas"]), {"val_loss"})
        self.assertAlmostEqual(out["deltas"]["val_loss"], -0.2)

    def test_compare_includes_seed_code_version_and_missing_keys(self):
        log = RunLog()
        log.start("a", {"lr": 0.1, "wd": 0.0}, seed=0, code_version="aaa")
        log.start("b", {"lr": 0.1, "warmup": 100}, seed=1, code_version="bbb")
        self.assertEqual(
            log.compare("a", "b")["changed"],
            {"wd": (0.0, None), "warmup": (None, 100), "seed": (0, 1), "code_version": ("aaa", "bbb")},
        )

    def test_deltas_use_the_last_logged_value_of_each_metric(self):
        log = RunLog()
        log.start("a", {}, 0, "v")
        log.start("b", {}, 0, "v")
        log.log("a", 1, {"loss": 2.0, "acc": 0.5})
        log.log("a", 2, {"loss": 1.0})
        log.log("b", 1, {"loss": 1.5, "acc": 0.8})
        deltas = log.compare("a", "b")["deltas"]
        self.assertAlmostEqual(deltas["loss"], 0.5)
        self.assertAlmostEqual(deltas["acc"], 0.3)

    def test_config_is_copied(self):
        log = RunLog()
        cfg = {"lr": 0.1}
        log.start("a", cfg, 0, "v")
        cfg["lr"] = 0.5
        log.start("b", cfg, 0, "v")
        self.assertEqual(log.compare("a", "b")["changed"], {"lr": (0.1, 0.5)})

    def test_log_errors(self):
        log = sample_log()
        with self.assertRaises(ValueError):
            log.log("base", 2, {"acc": 0.8})
        with self.assertRaises(ValueError):
            log.log("base", 1, {"acc": 0.8})
        with self.assertRaises(KeyError):
            log.log("nope", 1, {"acc": 0.8})

    def test_start_errors(self):
        log = sample_log()
        with self.assertRaises(ValueError):
            log.start("base", {}, 0, "v")
        with self.assertRaises(ValueError):
            log.start("new", {"seed": 3}, 0, "v")

    def test_best_and_compare_errors(self):
        log = sample_log()
        with self.assertRaises(KeyError):
            log.best("f1")
        with self.assertRaises(ValueError):
            log.best("acc", mode="median")
        with self.assertRaises(KeyError):
            log.compare("base", "ghost")


if __name__ == "__main__":
    unittest.main(verbosity=2)
