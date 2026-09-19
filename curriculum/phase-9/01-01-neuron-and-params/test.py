import math
import unittest

from solution import neuron, count_params


class TestNeuronAndParams(unittest.TestCase):
    def test_neuron_with_identity_activation(self):
        self.assertAlmostEqual(neuron([1.0, 2.0], [0.5, -1.0], 0.25, lambda z: z), -1.25)

    def test_neuron_applies_the_activation(self):
        self.assertAlmostEqual(neuron([1.0, 2.0], [0.5, -1.0], 0.25, lambda z: max(0.0, z)), 0.0)
        self.assertAlmostEqual(neuron([1.0, 1.0], [1.0, 1.0], 0.0, math.tanh), math.tanh(2.0))

    def test_neuron_with_no_inputs_is_the_activated_bias(self):
        self.assertAlmostEqual(neuron([], [], 3.0, lambda z: z), 3.0)

    def test_neuron_rejects_mismatched_lengths(self):
        with self.assertRaises(ValueError):
            neuron([1.0, 2.0], [1.0], 0.0, lambda z: z)

    def test_count_params_small(self):
        self.assertEqual(count_params([2, 2, 1]), 9)

    def test_count_params_mnist_shaped(self):
        self.assertEqual(count_params([784, 128, 10]), 101770)

    def test_count_params_input_only(self):
        self.assertEqual(count_params([5]), 0)

    def test_count_params_deep(self):
        self.assertEqual(count_params([3, 4, 4, 1]), 41)


if __name__ == "__main__":
    unittest.main(verbosity=2)
