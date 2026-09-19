import unittest

from solution import training_loop

CYCLE = ["zero_grad", "forward", "loss", "backward", "step"]


def fake(log):
    return {
        "zero_grad": lambda: log.append("zero_grad"),
        "forward": lambda x: (log.append("forward"), x * 2)[1],
        "loss": lambda out, y: (log.append("loss"), out - y)[1],
        "backward": lambda loss: log.append("backward"),
        "step": lambda: log.append("step"),
    }


class TestTrainingLoopOrder(unittest.TestCase):
    def test_one_batch_exact_order(self):
        log = []
        training_loop(fake(log), [(1, 0)], 1)
        self.assertEqual(log, CYCLE)

    def test_every_batch_every_epoch(self):
        log = []
        training_loop(fake(log), [(1, 0), (3, 1), (5, 2)], 2)
        self.assertEqual(log, CYCLE * 6)

    def test_returns_mean_loss_per_epoch(self):
        result = training_loop(fake([]), [(1, 0), (3, 1)], 3)
        self.assertEqual(result, [3.5, 3.5, 3.5])
        self.assertIsInstance(result[0], float)

    def test_values_flow_through_the_chain(self):
        seen = {"forward": [], "loss": [], "backward": []}
        sentinel = object()
        fns = {
            "zero_grad": lambda: None,
            "forward": lambda x: (seen["forward"].append(x), ("out", x))[1],
            "loss": lambda out, y: (seen["loss"].append((out, y)), 7.0)[1],
            "backward": lambda loss: seen["backward"].append(loss),
            "step": lambda: None,
        }
        training_loop(fns, [(sentinel, "y0")], 1)
        self.assertIs(seen["forward"][0], sentinel)
        self.assertEqual(seen["loss"][0], (("out", sentinel), "y0"))
        self.assertEqual(seen["backward"], [7.0])

    def test_backward_gets_the_loss_object_itself(self):
        class Loss(float):
            pass

        the_loss = Loss(1.5)
        got = []
        fns = fake([])
        fns["loss"] = lambda out, y: the_loss
        fns["backward"] = lambda loss: got.append(loss)
        training_loop(fns, [(1, 0)], 1)
        self.assertIs(got[0], the_loss)

    def test_zero_epochs_makes_no_calls(self):
        log = []
        self.assertEqual(training_loop(fake(log), [(1, 0)], 0), [])
        self.assertEqual(log, [])

    def test_rejects_bad_arguments_before_calling_anything(self):
        log = []
        with self.assertRaises(ValueError):
            training_loop(fake(log), [], 1)
        with self.assertRaises(ValueError):
            training_loop(fake(log), [(1, 0)], -1)
        fns = fake(log)
        del fns["step"]
        with self.assertRaises(ValueError):
            training_loop(fns, [(1, 0)], 1)
        self.assertEqual(log, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
