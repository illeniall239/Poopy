import unittest

from solution import split_bill


class TestSplitBill(unittest.TestCase):
    def test_leftover_cent_goes_to_one_person(self):
        self.assertEqual(split_bill(10, 3), {"shareCents": 333, "peopleWithExtraCent": 1})

    def test_even_split_has_no_extra_cents(self):
        self.assertEqual(split_bill(12, 4), {"shareCents": 300, "peopleWithExtraCent": 0})

    def test_several_leftover_cents(self):
        self.assertEqual(split_bill(100, 7), {"shareCents": 1428, "peopleWithExtraCent": 4})

    def test_19_99_dollars_is_1999_cents_despite_floating_point_error(self):
        self.assertEqual(split_bill(19.99, 2), {"shareCents": 999, "peopleWithExtraCent": 1})

    def test_0_29_dollars_is_29_cents_despite_floating_point_error(self):
        self.assertEqual(split_bill(0.29, 1), {"shareCents": 29, "peopleWithExtraCent": 0})

    def test_fewer_cents_than_people(self):
        self.assertEqual(split_bill(0.02, 3), {"shareCents": 0, "peopleWithExtraCent": 2})

    def test_zero_bill(self):
        self.assertEqual(split_bill(0, 5), {"shareCents": 0, "peopleWithExtraCent": 0})

    def test_one_person_pays_everything(self):
        self.assertEqual(split_bill(1.15, 1), {"shareCents": 115, "peopleWithExtraCent": 0})


if __name__ == "__main__":
    unittest.main(verbosity=2)
