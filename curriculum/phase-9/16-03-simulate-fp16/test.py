import math
import unittest

from solution import to_fp16, loss_scale_ok


class TestSimulateFp16(unittest.TestCase):
    def test_exact_and_rounded_values(self):
        self.assertEqual(to_fp16(1.0), (1.0, "ok"))
        self.assertEqual(to_fp16(0.1), (0.0999755859375, "ok"))
        self.assertEqual(to_fp16(65504.0), (65504.0, "ok"))
        self.assertEqual(to_fp16(65519.0), (65504.0, "ok"))

    def test_overflow_keeps_the_sign(self):
        self.assertEqual(to_fp16(70000.0), (math.inf, "overflow"))
        self.assertEqual(to_fp16(65520.0), (math.inf, "overflow"))
        self.assertEqual(to_fp16(-1e6), (-math.inf, "overflow"))
        self.assertEqual(to_fp16(1e300), (math.inf, "overflow"))

    def test_underflow_to_zero(self):
        value, status = to_fp16(1e-8)
        self.assertEqual((value, status), (0.0, "underflow"))
        self.assertEqual(to_fp16(-1e-9)[1], "underflow")

    def test_subnormals_and_zero_are_ok(self):
        value, status = to_fp16(1e-7)
        self.assertEqual(status, "ok")
        self.assertAlmostEqual(value, 1.1920928955078125e-07, places=20)
        self.assertEqual(to_fp16(0.0), (0.0, "ok"))

    def test_special_inputs_are_ok(self):
        self.assertEqual(to_fp16(math.inf), (math.inf, "ok"))
        value, status = to_fp16(math.nan)
        self.assertTrue(math.isnan(value))
        self.assertEqual(status, "ok")

    def test_loss_scale_rescues_tiny_gradients(self):
        grads = [1e-8, 1e-3]
        self.assertFalse(loss_scale_ok(grads, 1.0))
        self.assertTrue(loss_scale_ok(grads, 1024.0))

    def test_too_large_a_scale_overflows(self):
        self.assertFalse(loss_scale_ok([1e-8, 1e-3], 1e8))
        self.assertTrue(loss_scale_ok([0.0, 0.5, -2.0], 1.0))

    def test_loss_scale_edge_cases(self):
        self.assertTrue(loss_scale_ok([], 1.0))
        with self.assertRaises(ValueError):
            loss_scale_ok([1.0], 0.0)
        with self.assertRaises(ValueError):
            loss_scale_ok([1.0], -8.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
