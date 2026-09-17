import unittest

from solution import apply_patch, pick


def make_profile():
    return {"id": 7, "name": "Ana", "email": "ana@example.com", "theme": "dark"}


class TestPickAndPatch(unittest.TestCase):
    def test_pick_keeps_only_the_listed_keys(self):
        self.assertEqual(pick(make_profile(), ["name", "theme"]), {"name": "Ana", "theme": "dark"})

    def test_pick_with_no_keys_gives_an_empty_dict(self):
        self.assertEqual(pick(make_profile(), []), {})

    def test_pick_with_a_repeated_key_includes_it_once(self):
        self.assertEqual(pick(make_profile(), ["id", "id"]), {"id": 7})

    def test_pick_keeps_falsy_values(self):
        self.assertEqual(
            pick({"count": 0, "on": False, "label": ""}, ["count", "on", "label"]),
            {"count": 0, "on": False, "label": ""},
        )

    def test_pick_does_not_change_the_dict(self):
        profile = make_profile()
        pick(profile, ["name"])
        self.assertEqual(profile, make_profile())

    def test_apply_patch_replaces_patched_keys(self):
        self.assertEqual(apply_patch(make_profile(), {"theme": "light", "name": "Ana B"}), {
            "id": 7, "name": "Ana B", "email": "ana@example.com", "theme": "light",
        })

    def test_apply_patch_ignores_none_values(self):
        self.assertEqual(apply_patch(make_profile(), {"name": None}), make_profile())

    def test_apply_patch_keeps_falsy_patch_values_that_are_not_none(self):
        self.assertEqual(apply_patch({"count": 5, "on": True}, {"count": 0, "on": False}), {"count": 0, "on": False})

    def test_apply_patch_returns_a_new_dict_and_changes_neither_input(self):
        profile = make_profile()
        patch = {"theme": "light"}
        result = apply_patch(profile, patch)
        self.assertIsNot(result, profile)
        self.assertEqual(profile, make_profile())
        self.assertEqual(patch, {"theme": "light"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
