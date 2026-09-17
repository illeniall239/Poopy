import unittest

from solution import range_sums


class TestRangeSums(unittest.TestCase):
    def test_several_ranges_including_one_starting_at_index_0(self):
        self.assertEqual(range_sums([3, -2, 5, 1, 4], [(0, 2), (1, 3), (2, 4)]), [6, 4, 10])

    def test_a_single_element_range_and_the_whole_list(self):
        self.assertEqual(range_sums([3, -2, 5, 1, 4], [(3, 3), (0, 4)]), [1, 11])

    def test_no_queries_gives_an_empty_result(self):
        self.assertEqual(range_sums([7], []), [])

    def test_all_negative_values(self):
        self.assertEqual(range_sums([-4, -6, -1], [(0, 1), (1, 2), (0, 0)]), [-10, -7, -4])

    def test_answers_stay_in_query_order_repeats_included(self):
        self.assertEqual(range_sums([2, 9, 4], [(2, 2), (0, 0), (2, 2), (0, 2)]), [4, 2, 4, 15])

    def test_does_not_change_the_inputs(self):
        values = [1, 2, 3]
        queries = [(0, 2)]
        range_sums(values, queries)
        self.assertEqual(values, [1, 2, 3])
        self.assertEqual(queries, [(0, 2)])

    def test_100000_long_queries_over_100000_values_in_o_n_plus_q(self):
        n = 100000
        values = list(range(n))
        queries = []
        expected = []
        for q in range(n):
            i = q % (n // 2)
            j = n - 1 - i
            queries.append((i, j))
            expected.append((i + j) * (j - i + 1) // 2)
        self.assertEqual(range_sums(values, queries), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
