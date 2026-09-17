import unittest

from solution import binary_to_decimal


class TestBinaryToDecimal(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(binary_to_decimal("0"), 0)
        self.assertEqual(binary_to_decimal("0000"), 0)

    def test_leading_zeros_are_allowed(self):
        self.assertEqual(binary_to_decimal("0110"), 6)

    def test_one(self):
        self.assertEqual(binary_to_decimal("1"), 1)

    def test_leftmost_1_is_counted(self):
        self.assertEqual(binary_to_decimal("10"), 2)
        self.assertEqual(binary_to_decimal("1011"), 11)

    def test_all_ones(self):
        self.assertEqual(binary_to_decimal("11111111"), 255)
        self.assertEqual(binary_to_decimal("1" * 32), 4294967295)

    def test_empty_string_is_rejected(self):
        with self.assertRaises(ValueError) as cm:
            binary_to_decimal("")
        self.assertEqual(str(cm.exception), "Binary string is empty")

    def test_non_binary_characters_are_rejected(self):
        with self.assertRaises(ValueError) as cm:
            binary_to_decimal("102")
        self.assertEqual(str(cm.exception), 'Not a binary string: "102"')
        with self.assertRaises(ValueError) as cm:
            binary_to_decimal(" 1")
        self.assertEqual(str(cm.exception), 'Not a binary string: " 1"')


if __name__ == "__main__":
    unittest.main(verbosity=2)
