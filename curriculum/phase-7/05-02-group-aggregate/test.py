import unittest

import numpy as np
import pandas as pd
import pandas.testing as pdt

from solution import revenue_by_region, share_by_status


def make_orders():
    return pd.DataFrame(
        {
            "order_id": [1, 2, 3, 4, 5],
            "region": ["north", "north", "south", "south", None],
            "status": ["paid", "paid", "paid", "refund", "paid"],
            "amount": [10.0, 30.0, 5.0, 50.0, 100.0],
        }
    )


class TestGroupAggregate(unittest.TestCase):
    def test_revenue_by_region_values(self):
        out = revenue_by_region(make_orders())
        self.assertEqual(list(out.columns), ["orders", "revenue", "mean_order"])
        self.assertEqual(out.index.name, "region")
        self.assertEqual(list(out.index), ["north", "south"])
        np.testing.assert_allclose(out["orders"].to_numpy(), [2, 1])
        np.testing.assert_allclose(out["revenue"].to_numpy(), [40.0, 5.0])
        np.testing.assert_allclose(out["mean_order"].to_numpy(), [20.0, 5.0])

    def test_nan_region_dropped_by_groupby(self):
        out = revenue_by_region(make_orders())
        self.assertEqual(len(out), 2)
        self.assertAlmostEqual(out["revenue"].sum(), 45.0)

    def test_unpaid_rows_excluded(self):
        orders = make_orders()
        orders.loc[3, "amount"] = 1e6
        out = revenue_by_region(orders)
        self.assertAlmostEqual(out.loc["south", "revenue"], 5.0)

    def test_sorted_by_revenue_descending(self):
        orders = pd.DataFrame(
            {
                "order_id": range(6),
                "region": ["a", "b", "c", "a", "b", "c"],
                "status": ["paid"] * 6,
                "amount": [1.0, 10.0, 5.0, 1.0, 10.0, 5.0],
            }
        )
        self.assertEqual(list(revenue_by_region(orders).index), ["b", "c", "a"])

    def test_input_not_modified(self):
        orders = make_orders()
        before = orders.copy()
        revenue_by_region(orders)
        share_by_status(orders)
        pdt.assert_frame_equal(orders, before)

    def test_share_by_status(self):
        out = share_by_status(make_orders())
        self.assertIsInstance(out, pd.Series)
        self.assertEqual(list(out.index), ["paid", "refund"])
        np.testing.assert_allclose(out.to_numpy(), [0.8, 0.2])
        self.assertAlmostEqual(out.sum(), 1.0)

    def test_share_uses_every_row_and_sorts(self):
        orders = pd.DataFrame(
            {
                "order_id": range(10),
                "region": ["x"] * 10,
                "status": ["refund"] * 5 + ["paid"] * 3 + ["pending"] * 2,
                "amount": [1.0] * 10,
            }
        )
        out = share_by_status(orders)
        self.assertEqual(list(out.index), ["refund", "paid", "pending"])
        np.testing.assert_allclose(out.to_numpy(), [0.5, 0.3, 0.2])

    def test_larger_random_matches_manual(self):
        rng = np.random.default_rng(0)
        n = 5000
        orders = pd.DataFrame(
            {
                "order_id": range(n),
                "region": rng.choice(["e", "w", "n", "s"], size=n),
                "status": rng.choice(["paid", "paid", "refund"], size=n),
                "amount": rng.uniform(1, 100, size=n).round(2),
            }
        )
        out = revenue_by_region(orders)
        paid = orders[orders["status"] == "paid"]
        for region in out.index:
            sub = paid[paid["region"] == region]
            self.assertEqual(out.loc[region, "orders"], len(sub))
            self.assertAlmostEqual(out.loc[region, "revenue"], sub["amount"].sum(), places=6)
            self.assertAlmostEqual(out.loc[region, "mean_order"], sub["amount"].mean(), places=6)
        self.assertTrue(out["revenue"].is_monotonic_decreasing)


if __name__ == "__main__":
    unittest.main(verbosity=2)
