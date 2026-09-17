import unittest

from solution import Order, grand_total, totals_by_customer

orders = [
    Order("ana", 1200),
    Order("ben", 500),
    Order("ana", 300),
]


class TestOrderTotals(unittest.TestCase):
    def test_grand_total_adds_every_order(self):
        self.assertEqual(grand_total(orders), 2000)

    def test_grand_total_of_no_orders_is_0(self):
        self.assertEqual(grand_total([]), 0)

    def test_totals_are_grouped_per_customer(self):
        self.assertEqual(totals_by_customer(orders), {"ana": 1500, "ben": 500})

    def test_customers_appear_in_order_of_first_appearance(self):
        result = totals_by_customer([
            Order("zoe", 1),
            Order("adam", 2),
            Order("zoe", 3),
        ])
        self.assertEqual(list(result.keys()), ["zoe", "adam"])

    def test_no_orders_gives_an_empty_dict(self):
        result = totals_by_customer([])
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 0)

    def test_customer_names_are_case_sensitive_and_zero_amounts_still_count(self):
        result = totals_by_customer([
            Order("Ana", 0),
            Order("ana", 100),
        ])
        self.assertEqual(result, {"Ana": 0, "ana": 100})

    def test_does_not_change_the_input(self):
        input = [
            Order("ana", 1200),
            Order("ana", 300),
        ]
        grand_total(input)
        totals_by_customer(input)
        self.assertEqual(input, [
            Order("ana", 1200),
            Order("ana", 300),
        ])


if __name__ == "__main__":
    unittest.main(verbosity=2)
