import unittest

from solution import param_memory_mb, adam_training_memory_mb

MIB = 1_048_576


class TestTrainingMemory(unittest.TestCase):
    def test_float32_one_mebi_params(self):
        self.assertAlmostEqual(param_memory_mb(MIB, "float32"), 4.0)

    def test_every_dtype_size(self):
        self.assertAlmostEqual(param_memory_mb(MIB, "float64"), 8.0)
        self.assertAlmostEqual(param_memory_mb(MIB, "float16"), 2.0)
        self.assertAlmostEqual(param_memory_mb(MIB, "bfloat16"), 2.0)

    def test_uses_binary_megabytes_and_returns_float(self):
        result = param_memory_mb(1_000_000, "float32")
        self.assertIsInstance(result, float)
        self.assertAlmostEqual(result, 3.814697265625)

    def test_zero_params(self):
        self.assertEqual(param_memory_mb(0, "float16"), 0.0)
        self.assertEqual(adam_training_memory_mb(0), 0.0)

    def test_rejects_unknown_dtype_and_negative_count(self):
        for bad in ("int8", "fp32", "float"):
            with self.assertRaises(ValueError):
                param_memory_mb(10, bad)
        with self.assertRaises(ValueError):
            param_memory_mb(-1, "float32")
        with self.assertRaises(ValueError):
            adam_training_memory_mb(-5)

    def test_adam_counts_weights_grads_and_two_moments(self):
        self.assertAlmostEqual(adam_training_memory_mb(MIB), 16.0)
        self.assertAlmostEqual(adam_training_memory_mb(1000), 1000 * 16 / MIB)

    def test_adam_seven_billion(self):
        self.assertAlmostEqual(adam_training_memory_mb(7_000_000_000), 106811.5234375, places=6)


if __name__ == "__main__":
    unittest.main(verbosity=2)
