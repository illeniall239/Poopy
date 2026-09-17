import unittest

from solution import SparseMatrix


class TestSparseMatrix(unittest.TestCase):
    def test_a_new_matrix_is_all_zeros(self):
        m = SparseMatrix(3, 4)
        self.assertEqual(m.get(0, 0), 0)
        self.assertEqual(m.get(2, 3), 0)
        self.assertEqual(m.non_zero_count(), 0)

    def test_set_and_get_keep_rows_and_columns_apart(self):
        m = SparseMatrix(2, 2)
        m.set(0, 1, 5)
        m.set(1, 0, -7)
        self.assertEqual([m.get(0, 0), m.get(0, 1), m.get(1, 0), m.get(1, 1)], [0, 5, -7, 0])
        self.assertEqual(m.non_zero_count(), 2)

    def test_overwriting_a_cell_does_not_add_to_the_count(self):
        m = SparseMatrix(1, 1)
        m.set(0, 0, 3)
        m.set(0, 0, 4)
        self.assertEqual(m.get(0, 0), 4)
        self.assertEqual(m.non_zero_count(), 1)

    def test_setting_0_removes_a_stored_cell_and_ignores_an_empty_one(self):
        m = SparseMatrix(2, 2)
        m.set(1, 1, 9)
        m.set(1, 1, 0)
        m.set(0, 0, 0)
        self.assertEqual(m.get(1, 1), 0)
        self.assertEqual(m.non_zero_count(), 0)

    def test_multiplies_by_a_vector(self):
        m = SparseMatrix(2, 3)
        m.set(0, 0, 1)
        m.set(0, 2, 2)
        m.set(1, 1, 3)
        self.assertEqual(m.multiply_vector([4, 5, 6]), [16, 15])

    def test_empty_rows_give_0_and_removed_cells_do_not_contribute(self):
        m = SparseMatrix(3, 2)
        m.set(1, 0, -1)
        m.set(1, 1, 2)
        m.set(2, 0, 8)
        m.set(2, 0, 0)
        self.assertEqual(m.multiply_vector([3, 4]), [0, 5, 0])

    def test_a_matrix_with_no_cells_gives_a_zero_vector_of_length_rows(self):
        self.assertEqual(SparseMatrix(4, 1).multiply_vector([7]), [0, 0, 0, 0])

    def test_40000_x_40000_matrix_with_80000_cells_in_o_rows_plus_non_zeros(self):
        n = 40000
        m = SparseMatrix(n, n)
        for i in range(n):
            m.set(i, i, 2)
            m.set(i, (i + 1) % n, 1)
        self.assertEqual(m.non_zero_count(), 2 * n)
        vector = [i % 1000 for i in range(n)]
        result = m.multiply_vector(vector)
        self.assertEqual(len(result), n)
        wrong = sum(1 for i in range(n) if result[i] != 2 * (i % 1000) + ((i + 1) % n) % 1000)
        self.assertEqual(wrong, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
