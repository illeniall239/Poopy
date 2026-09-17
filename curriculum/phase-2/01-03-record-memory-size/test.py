import unittest

from solution import array_size, record_size


class TestRecordMemorySize(unittest.TestCase):
    def test_padding_before_a_larger_field(self):
        self.assertEqual(record_size(["i8", "i32"]), 8)

    def test_padding_at_the_end_rounds_to_the_largest_field(self):
        self.assertEqual(record_size(["i32", "i8"]), 8)
        self.assertEqual(record_size(["bool", "i16"]), 4)

    def test_field_order_changes_the_size(self):
        self.assertEqual(record_size(["i8", "i64", "i8"]), 24)
        self.assertEqual(record_size(["i64", "i8", "i8"]), 16)

    def test_one_byte_fields_need_no_padding(self):
        self.assertEqual(record_size(["i8", "bool", "i8"]), 3)

    def test_empty_record_has_size_0(self):
        self.assertEqual(record_size([]), 0)

    def test_mixed_field_types(self):
        self.assertEqual(record_size(["ptr", "f32", "f64", "i16"]), 32)
        self.assertEqual(record_size(["i16", "i8", "i32", "i8"]), 12)

    def test_array_of_records_includes_each_records_padding(self):
        self.assertEqual(array_size(["i32", "i8"], 1000), 8000)
        self.assertEqual(array_size(["i8", "i16", "i8"], 3), 18)

    def test_empty_arrays_and_empty_records_use_no_bytes(self):
        self.assertEqual(array_size(["i64"], 0), 0)
        self.assertEqual(array_size([], 5), 0)
        self.assertEqual(array_size(["f64", "i8"], 10000000), 160000000)


if __name__ == "__main__":
    unittest.main(verbosity=2)
