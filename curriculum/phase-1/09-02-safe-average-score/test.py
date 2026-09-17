import unittest

from solution import Student, average_score


class TestAverageScore(unittest.TestCase):
    def test_all_scores_present(self):
        self.assertEqual(average_score([Student("Ana", 80), Student("Ben", 90)]), 85)

    def test_absent_score_is_skipped_not_counted_as_zero(self):
        self.assertEqual(average_score([Student("Ana", 80), Student("Ben")]), 80)

    def test_a_score_of_0_counts(self):
        self.assertEqual(average_score([Student("Ana", 0), Student("Ben", 10)]), 5)

    def test_none_scores_are_skipped(self):
        self.assertEqual(
            average_score([
                Student("Ana", None),
                Student("Ben", 40),
                Student("Cy"),
                Student("Di", 60),
            ]),
            50,
        )

    def test_no_present_scores_gives_none(self):
        self.assertIsNone(average_score([Student("Ana", None), Student("Ben")]))

    def test_empty_list_gives_none(self):
        self.assertIsNone(average_score([]))

    def test_result_is_not_rounded(self):
        self.assertEqual(average_score([Student("Ana", 1), Student("Ben", 2)]), 1.5)

    def test_all_zeros_averages_to_0_not_none(self):
        self.assertEqual(average_score([Student("Ana", 0)]), 0)

    def test_does_not_modify_the_input(self):
        students = [Student("Ana", 70), Student("Ben")]
        average_score(students)
        self.assertEqual(students, [Student("Ana", 70), Student("Ben")])


if __name__ == "__main__":
    unittest.main(verbosity=2)
