import unittest

from solution import shipping_cost


class TestShippingCost(unittest.TestCase):
    def test_light_parcel_including_exactly_1_kg(self):
        self.assertEqual(shipping_cost(2000, 0.5, False), 499)
        self.assertEqual(shipping_cost(2000, 1, False), 499)

    def test_middle_tier_including_exactly_5_kg(self):
        self.assertEqual(shipping_cost(2000, 1.5, False), 899)
        self.assertEqual(shipping_cost(2000, 5, False), 899)

    def test_heavy_tier_just_over_5_kg(self):
        self.assertEqual(shipping_cost(2000, 5.1, False), 1499)

    def test_free_shipping_starts_at_exactly_5000_cents(self):
        self.assertEqual(shipping_cost(4999, 3, False), 899)
        self.assertEqual(shipping_cost(5000, 3, False), 0)

    def test_express_adds_1000_and_is_never_free(self):
        self.assertEqual(shipping_cost(2000, 1, True), 1499)
        self.assertEqual(shipping_cost(6000, 3, True), 1899)

    def test_free_shipping_applies_up_to_and_including_20_kg(self):
        self.assertEqual(shipping_cost(6000, 20, False), 0)
        self.assertEqual(shipping_cost(6000, 25, False), 1499)

    def test_over_30_kg_cant_ship_even_with_free_shipping_or_express(self):
        self.assertEqual(shipping_cost(9000, 31, False), -1)
        self.assertEqual(shipping_cost(100, 30.5, True), -1)

    def test_exactly_30_kg_can_still_ship(self):
        self.assertEqual(shipping_cost(100, 30, True), 2499)

    def test_zero_subtotal_is_not_free(self):
        self.assertEqual(shipping_cost(0, 2, False), 899)


if __name__ == "__main__":
    unittest.main(verbosity=2)
