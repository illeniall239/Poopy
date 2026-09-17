import unittest

from solution import from_base, to_base


class TestBases(unittest.TestCase):
    def test_ten_in_binary(self):
        self.assertEqual(to_base(10, 2), "1010")

    def test_digits_come_out_most_significant_first(self):
        self.assertEqual(to_base(6, 2), "110")

    def test_letters_for_digits_above_9(self):
        self.assertEqual(to_base(255, 16), "ff")

    def test_zero_is_written_as_a_single_digit(self):
        self.assertEqual(to_base(0, 7), "0")

    def test_largest_32_bit_integer_in_base_16_and_base_2(self):
        self.assertEqual(to_base(2147483647, 16), "7fffffff")
        self.assertEqual(to_base(2147483647, 2), "1" * 31)

    def test_from_base_reads_binary(self):
        self.assertEqual(from_base("1010", 2), 10)

    def test_from_base_reads_zero_and_letters(self):
        self.assertEqual(from_base("0", 2), 0)
        self.assertEqual(from_base("7fffffff", 16), 2147483647)

    def test_round_trip_in_every_base(self):
        for base in range(2, 17):
            for n in [1, 15, 16, 999, 123456789, 2147483646]:
                self.assertEqual(from_base(to_base(n, base), base), n)
        self.assertEqual(to_base(123456789, 10), "123456789")


if __name__ == "__main__":
    unittest.main(verbosity=2)
