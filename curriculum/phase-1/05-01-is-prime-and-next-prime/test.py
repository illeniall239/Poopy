import unittest

from solution import is_prime, next_prime


class TestIsPrimeAndNextPrime(unittest.TestCase):
    def test_small_primes(self):
        self.assertEqual(is_prime(2), True)
        self.assertEqual(is_prime(3), True)
        self.assertEqual(is_prime(7), True)

    def test_numbers_below_2_are_not_prime(self):
        self.assertEqual(is_prime(1), False)
        self.assertEqual(is_prime(0), False)
        self.assertEqual(is_prime(-7), False)

    def test_even_numbers_above_2_are_not_prime(self):
        self.assertEqual(is_prime(4), False)
        self.assertEqual(is_prime(100), False)

    def test_squares_of_primes_are_not_prime(self):
        self.assertEqual(is_prime(9), False)
        self.assertEqual(is_prime(25), False)
        self.assertEqual(is_prime(49), False)

    def test_larger_primes(self):
        self.assertEqual(is_prime(97), True)
        self.assertEqual(is_prime(7919), True)
        self.assertEqual(is_prime(1000003), True)

    def test_next_prime_is_strictly_greater(self):
        self.assertEqual(next_prime(13), 17)
        self.assertEqual(next_prime(2), 3)
        self.assertEqual(next_prime(14), 17)

    def test_next_prime_from_zero_one_and_negatives_is_2(self):
        self.assertEqual(next_prime(0), 2)
        self.assertEqual(next_prime(1), 2)
        self.assertEqual(next_prime(-10), 2)

    def test_next_prime_for_a_large_number(self):
        self.assertEqual(next_prime(1000000), 1000003)


if __name__ == "__main__":
    unittest.main(verbosity=2)
