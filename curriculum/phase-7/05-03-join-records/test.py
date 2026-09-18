import unittest

import pandas as pd
import pandas.testing as pdt

from solution import enrich_orders, orders_per_customer


def make_tables():
    orders = pd.DataFrame({"order_id": [1, 2, 3, 4], "customer_id": [7, 7, 9, 42], "amount": [10.0, 20.0, 5.0, 99.0]})
    customers = pd.DataFrame({"customer_id": [7, 8, 9], "name": ["Ann", "Bob", "Cy"], "country": ["NO", "DE", "FR"]})
    return orders, customers


class TestJoinRecords(unittest.TestCase):
    def test_inner_drops_unknown_customer(self):
        out = enrich_orders(*make_tables())
        self.assertEqual(list(out.columns), ["order_id", "customer_id", "amount", "name", "country"])
        self.assertEqual(out["order_id"].tolist(), [1, 2, 3])
        self.assertEqual(out["name"].tolist(), ["Ann", "Ann", "Cy"])
        self.assertEqual(out["country"].tolist(), ["NO", "NO", "FR"])
        self.assertEqual(list(out.index), [0, 1, 2])

    def test_left_keeps_unknown_customer_with_nan(self):
        out = enrich_orders(*make_tables(), how="left")
        self.assertEqual(out["order_id"].tolist(), [1, 2, 3, 4])
        self.assertTrue(pd.isna(out.loc[3, "name"]))
        self.assertTrue(pd.isna(out.loc[3, "country"]))
        self.assertAlmostEqual(out.loc[3, "amount"], 99.0)

    def test_invalid_how_raises(self):
        with self.assertRaises(ValueError):
            enrich_orders(*make_tables(), how="outer")

    def test_duplicate_customer_multiplies_rows(self):
        orders, customers = make_tables()
        customers = pd.concat([customers, pd.DataFrame({"customer_id": [7], "name": ["Ann2"], "country": ["SE"]})], ignore_index=True)
        out = enrich_orders(orders, customers)
        self.assertEqual(len(out), 5)
        self.assertEqual((out["customer_id"] == 7).sum(), 4)

    def test_inputs_not_modified(self):
        orders, customers = make_tables()
        o, c = orders.copy(), customers.copy()
        enrich_orders(orders, customers, "left")
        orders_per_customer(orders, customers)
        pdt.assert_frame_equal(orders, o)
        pdt.assert_frame_equal(customers, c)

    def test_orders_per_customer(self):
        out = orders_per_customer(*make_tables())
        self.assertIsInstance(out, pd.Series)
        self.assertEqual(list(out.index), [7, 8, 9])
        self.assertEqual(out.tolist(), [2, 0, 1])
        self.assertTrue(pd.api.types.is_integer_dtype(out))

    def test_orders_per_customer_ignores_unknown_and_keeps_order(self):
        orders, customers = make_tables()
        customers = customers.iloc[::-1].reset_index(drop=True)
        out = orders_per_customer(orders, customers)
        self.assertEqual(list(out.index), [9, 8, 7])
        self.assertEqual(out.tolist(), [1, 0, 2])
        self.assertEqual(out.sum(), 3)

    def test_empty_orders(self):
        orders, customers = make_tables()
        out = orders_per_customer(orders.iloc[0:0], customers)
        self.assertEqual(out.tolist(), [0, 0, 0])
        self.assertEqual(len(enrich_orders(orders.iloc[0:0], customers)), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
