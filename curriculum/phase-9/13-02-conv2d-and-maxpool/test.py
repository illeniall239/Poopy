import unittest

import torch
import torch.nn.functional as F

from solution import conv2d, maxpool2d

EDGE = [[0, 0, 1, 1]] * 4
SOBEL_X = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]


class TestConv2dAndMaxpool(unittest.TestCase):
    def assertGridClose(self, got, want):
        self.assertEqual(len(got), len(want))
        for g_row, w_row in zip(got, want):
            self.assertEqual(len(g_row), len(w_row))
            for g, w in zip(g_row, w_row):
                self.assertAlmostEqual(g, w, delta=1e-9)

    def test_edge_detect(self):
        self.assertGridClose(conv2d(EDGE, SOBEL_X), [[4.0, 4.0], [4.0, 4.0]])

    def test_kernel_is_not_flipped(self):
        self.assertGridClose(conv2d(EDGE, [[1, -1]]), [[0.0, -1.0, 0.0]] * 4)

    def test_padding_adds_zeros_on_every_side(self):
        want = [[0, 0, 0, 0], [0, 1, 2, 0], [0, 3, 4, 0], [0, 0, 0, 0]]
        self.assertGridClose(conv2d([[1, 2], [3, 4]], [[1]], padding=1), want)

    def test_stride_and_padding_by_hand(self):
        self.assertGridClose(conv2d(EDGE, SOBEL_X, stride=2, padding=1), [[0.0, 3.0], [0.0, 4.0]])

    def test_conv_matches_torch_on_random_inputs(self):
        torch.manual_seed(0)
        for h, w, kh, kw, s, p in [(5, 5, 3, 3, 1, 0), (6, 7, 3, 2, 2, 1), (7, 5, 2, 4, 3, 2), (4, 4, 4, 4, 1, 0)]:
            img = torch.randn(h, w, dtype=torch.float64)
            ker = torch.randn(kh, kw, dtype=torch.float64)
            want = F.conv2d(img[None, None], ker[None, None], stride=s, padding=p)[0, 0].tolist()
            self.assertGridClose(conv2d(img.tolist(), ker.tolist(), stride=s, padding=p), want)

    def test_maxpool_by_hand(self):
        img = [[1, 2, 5, 0], [3, 4, 1, 1], [0, 0, 9, 8], [7, 0, 6, 2]]
        self.assertGridClose(maxpool2d(img, 2), [[4.0, 5.0], [7.0, 9.0]])
        self.assertGridClose(maxpool2d([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 2, stride=1), [[5.0, 6.0], [8.0, 9.0]])

    def test_maxpool_matches_torch_on_random_inputs(self):
        torch.manual_seed(1)
        for h, w, k, s in [(4, 4, 2, None), (5, 7, 2, None), (6, 6, 3, 2), (5, 5, 3, 1)]:
            img = torch.randn(h, w, dtype=torch.float64)
            want = F.max_pool2d(img[None, None], k, stride=s)[0, 0].tolist()
            self.assertGridClose(maxpool2d(img.tolist(), k, s), want)

    def test_errors(self):
        with self.assertRaises(ValueError):
            conv2d([[1, 2], [3, 4]], SOBEL_X)
        with self.assertRaises(ValueError):
            conv2d(EDGE, SOBEL_X, stride=0)
        with self.assertRaises(ValueError):
            maxpool2d([[1, 2], [3, 4]], 3)
        with self.assertRaises(ValueError):
            maxpool2d([[1, 2], [3, 4]], 2, stride=0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
