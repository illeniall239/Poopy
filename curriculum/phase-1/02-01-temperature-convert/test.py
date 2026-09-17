import unittest

from solution import celsius_to_fahrenheit, fahrenheit_to_celsius


class TestTemperatureConvert(unittest.TestCase):
    def test_boiling_point_to_fahrenheit(self):
        self.assertEqual(celsius_to_fahrenheit(100), 212)

    def test_freezing_point_to_fahrenheit(self):
        self.assertEqual(celsius_to_fahrenheit(0), 32)

    def test_body_temperature_to_fahrenheit(self):
        self.assertEqual(celsius_to_fahrenheit(37), 98.6)

    def test_floating_point_noise_is_rounded_to_one_decimal_place(self):
        self.assertEqual(celsius_to_fahrenheit(36.6), 97.9)

    def test_minus_40_is_the_same_on_both_scales(self):
        self.assertEqual(celsius_to_fahrenheit(-40), -40)
        self.assertEqual(fahrenheit_to_celsius(-40), -40)

    def test_subtracts_32_before_multiplying(self):
        self.assertEqual(fahrenheit_to_celsius(212), 100)

    def test_body_temperature_to_celsius(self):
        self.assertEqual(fahrenheit_to_celsius(98.6), 37)

    def test_negative_result_rounds_to_one_decimal_place(self):
        self.assertEqual(fahrenheit_to_celsius(0), -17.8)

    def test_returns_a_number_not_a_string(self):
        self.assertIsInstance(fahrenheit_to_celsius(50), (int, float))
        self.assertEqual(fahrenheit_to_celsius(50), 10)


if __name__ == "__main__":
    unittest.main(verbosity=2)
