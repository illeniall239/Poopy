import unittest

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402
from numpy.testing import assert_allclose  # noqa: E402

from solution import plot_learning_curves  # noqa: E402

TRAIN = [1.0, 0.6, 0.4, 0.3]
VAL = [1.1, 0.7, 0.65, 0.7]


class TestPlotLearningCurves(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_returns_figure_with_one_axes(self):
        fig = plot_learning_curves(TRAIN, VAL)
        self.assertIsInstance(fig, Figure)
        self.assertEqual(len(fig.axes), 1)

    def test_line_data(self):
        ax = plot_learning_curves(TRAIN, VAL).axes[0]
        lines = ax.get_lines()
        self.assertGreaterEqual(len(lines), 2)
        assert_allclose(lines[0].get_xdata(), [1, 2, 3, 4])
        assert_allclose(lines[0].get_ydata(), TRAIN)
        assert_allclose(lines[1].get_xdata(), [1, 2, 3, 4])
        assert_allclose(lines[1].get_ydata(), VAL)

    def test_labels_title_and_legend(self):
        ax = plot_learning_curves(TRAIN, VAL, title="Run 7").axes[0]
        self.assertEqual(ax.get_xlabel(), "epoch")
        self.assertEqual(ax.get_ylabel(), "loss")
        self.assertEqual(ax.get_title(), "Run 7")
        legend = ax.get_legend()
        self.assertIsNotNone(legend)
        self.assertEqual([t.get_text() for t in legend.get_texts()], ["train", "validation"])

    def test_default_title(self):
        self.assertEqual(plot_learning_curves(TRAIN, VAL).axes[0].get_title(), "Learning curves")

    def test_best_epoch_vertical_line(self):
        ax = plot_learning_curves(TRAIN, VAL).axes[0]
        vlines = [l for l in ax.get_lines()[2:] if len(set(np.asarray(l.get_xdata()).tolist())) == 1]
        self.assertEqual(len(vlines), 1)
        self.assertAlmostEqual(float(np.asarray(vlines[0].get_xdata())[0]), 3.0)
        self.assertEqual(vlines[0].get_linestyle(), "--")

    def test_best_epoch_moves_with_data(self):
        ax = plot_learning_curves([1, 1, 1, 1, 1], [5, 4, 3, 2, 1]).axes[0]
        vlines = [l for l in ax.get_lines()[2:] if len(set(np.asarray(l.get_xdata()).tolist())) == 1]
        self.assertAlmostEqual(float(np.asarray(vlines[0].get_xdata())[0]), 5.0)

    def test_errors(self):
        with self.assertRaises(ValueError):
            plot_learning_curves([1.0, 0.5], [1.0])
        with self.assertRaises(ValueError):
            plot_learning_curves([], [])

    def test_long_run(self):
        n = 2000
        rng = np.random.default_rng(0)
        train = np.exp(-np.linspace(0, 5, n)).tolist()
        val = (np.exp(-np.linspace(0, 5, n)) + 0.01 * rng.random(n)).tolist()
        lines = plot_learning_curves(train, val).axes[0].get_lines()
        self.assertEqual(len(lines[0].get_xdata()), n)
        assert_allclose(lines[1].get_ydata(), val)


if __name__ == "__main__":
    unittest.main(verbosity=2)
