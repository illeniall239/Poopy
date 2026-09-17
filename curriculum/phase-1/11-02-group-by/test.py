import unittest

from solution import group_by


class TestGroupBy(unittest.TestCase):
    def test_groups_numbers_by_parity(self):
        self.assertEqual(
            group_by([1, 2, 3, 4, 5], lambda n: "even" if n % 2 == 0 else "odd"),
            {"odd": [1, 3, 5], "even": [2, 4]},
        )

    def test_groups_dicts_and_keeps_input_order_within_each_group(self):
        people = [
            {"name": "Ana", "team": "red"},
            {"name": "Bo", "team": "blue"},
            {"name": "Cy", "team": "red"},
        ]
        self.assertEqual(group_by(people, lambda p: p["team"]), {
            "red": [{"name": "Ana", "team": "red"}, {"name": "Cy", "team": "red"}],
            "blue": [{"name": "Bo", "team": "blue"}],
        })

    def test_groups_hold_the_original_objects_not_copies(self):
        ana = {"name": "Ana", "team": "red"}
        result = group_by([ana], lambda p: p["team"])
        self.assertIs(result["red"][0], ana)

    def test_empty_input_gives_an_empty_dict(self):
        self.assertEqual(group_by([], lambda s: s), {})

    def test_every_item_in_one_group(self):
        self.assertEqual(group_by(["x", "y"], lambda _: "all"), {"all": ["x", "y"]})

    def test_key_of_is_called_once_per_item(self):
        calls = []

        def key_of(n):
            calls.append(n)
            return str(n)

        group_by([1, 2, 3], key_of)
        self.assertEqual(len(calls), 3)

    def test_does_not_change_the_input(self):
        items = [3, 1, 2]
        group_by(items, lambda n: str(n % 2))
        self.assertEqual(items, [3, 1, 2])


if __name__ == "__main__":
    unittest.main(verbosity=2)
