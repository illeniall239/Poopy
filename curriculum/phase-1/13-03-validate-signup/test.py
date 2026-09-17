import unittest

from solution import validate_signup

good = {"username": "ada_99", "email": "ada@example.com", "password": "s3cretpass", "confirm_password": "s3cretpass"}


class TestValidateSignup(unittest.TestCase):
    def test_a_correct_form_is_valid(self):
        self.assertEqual(validate_signup(good), {"valid": True})

    def test_surrounding_spaces_in_username_and_email_are_ignored(self):
        self.assertEqual(validate_signup({**good, "username": "  ada ", "email": " ada@example.com  "}), {"valid": True})

    def test_reports_every_broken_field_at_once_in_field_order(self):
        self.assertEqual(
            validate_signup({"username": "  ", "email": "ada@example", "password": "short1", "confirm_password": "short2"}),
            {
                "valid": False,
                "errors": [
                    {"field": "username", "message": "Username is required"},
                    {"field": "email", "message": "Email is not valid"},
                    {"field": "password", "message": "Password must be at least 8 characters"},
                    {"field": "confirm_password", "message": "Passwords do not match"},
                ],
            },
        )

    def test_only_the_first_broken_rule_per_field_is_reported(self):
        self.assertEqual(
            validate_signup({**good, "username": "a!", "password": "abc", "confirm_password": "abc"}),
            {
                "valid": False,
                "errors": [
                    {"field": "username", "message": "Username must be 3 to 20 characters"},
                    {"field": "password", "message": "Password must be at least 8 characters"},
                ],
            },
        )

    def test_username_rules(self):
        def message_for(username):
            result = validate_signup({**good, "username": username})
            return None if result["valid"] else result["errors"][0]["message"]

        self.assertEqual(message_for("ab"), "Username must be 3 to 20 characters")
        self.assertEqual(message_for("a" * 21), "Username must be 3 to 20 characters")
        self.assertIsNone(message_for("a" * 20))
        self.assertEqual(message_for("ada lovelace"), "Username may only contain letters, digits and underscores")
        self.assertEqual(message_for("adé"), "Username may only contain letters, digits and underscores")

    def test_email_rules(self):
        def message_for(email):
            result = validate_signup({**good, "email": email})
            return None if result["valid"] else result["errors"][0]["message"]

        self.assertEqual(message_for(""), "Email is required")
        self.assertIsNone(message_for("a@b.co"))
        for bad in ["@a.com", "a@b.", "a@.com", "a@@b.com", "a@b@c.com", "a b@c.com", "abc.com", "a@bcom"]:
            self.assertEqual(message_for(bad), "Email is not valid", bad)

    def test_password_rules_and_confirm_is_checked_against_the_password_as_typed(self):
        def errors_for(password, confirm_password):
            result = validate_signup({**good, "password": password, "confirm_password": confirm_password})
            return [] if result["valid"] else result["errors"]

        self.assertEqual(errors_for("abcdefgh", "abcdefgh"), [{"field": "password", "message": "Password must contain a digit"}])
        self.assertEqual(errors_for("12345678", "12345678"), [{"field": "password", "message": "Password must contain a letter"}])
        self.assertEqual(errors_for("pass word1", "pass word1"), [])
        self.assertEqual(errors_for("s3cretpass", "s3cretpass "), [{"field": "confirm_password", "message": "Passwords do not match"}])


if __name__ == "__main__":
    unittest.main(verbosity=2)
