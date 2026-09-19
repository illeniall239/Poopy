import unittest

import torch
from torch import nn

from solution import conv_output_size, conv_params


class TestConvShapesAndParams(unittest.TestCase):
    def test_output_size_basic(self):
        self.assertEqual(conv_output_size(32, 3, 1, 1), 32)
        self.assertEqual(conv_output_size(32, 5, 0, 1), 28)

    def test_output_size_with_stride(self):
        self.assertEqual(conv_output_size(7, 3, 0, 2), 3)
        self.assertEqual(conv_output_size(8, 3, 1, 2), 4)
        self.assertEqual(conv_output_size(8, 2, 0, 2), 4)

    def test_output_size_counts_padding_on_both_sides(self):
        self.assertEqual(conv_output_size(5, 3, 2, 1), 7)
        self.assertEqual(conv_output_size(1, 3, 1, 1), 1)

    def test_output_size_matches_torch(self):
        x = torch.zeros(1, 1, 11, 11)
        for k, p, s in [(3, 0, 1), (3, 1, 2), (5, 2, 3), (4, 1, 2), (11, 0, 1), (2, 3, 4)]:
            want = nn.Conv2d(1, 1, k, stride=s, padding=p)(x).shape[-1]
            self.assertEqual(conv_output_size(11, k, p, s), want, msg=f"k={k} p={p} s={s}")

    def test_output_size_errors(self):
        for args in [(2, 5, 0, 1), (0, 1, 0, 1), (5, 0, 0, 1), (5, 3, -1, 1), (5, 3, 0, 0)]:
            with self.assertRaises(ValueError, msg=str(args)):
                conv_output_size(*args)

    def test_params_with_and_without_bias(self):
        self.assertEqual(conv_params(3, 16, 3), 448)
        self.assertEqual(conv_params(3, 16, 3, bias=False), 432)
        self.assertEqual(conv_params(64, 128, 1), 8320)

    def test_params_match_torch(self):
        for in_c, out_c, k, bias in [(1, 4, 3, True), (4, 8, 5, False), (2, 3, 1, True), (7, 2, 2, True)]:
            layer = nn.Conv2d(in_c, out_c, k, bias=bias)
            want = sum(p.numel() for p in layer.parameters())
            self.assertEqual(conv_params(in_c, out_c, k, bias), want)

    def test_params_errors(self):
        for args in [(0, 4, 3), (3, 0, 3), (3, 4, 0)]:
            with self.assertRaises(ValueError, msg=str(args)):
                conv_params(*args)


if __name__ == "__main__":
    unittest.main(verbosity=2)
