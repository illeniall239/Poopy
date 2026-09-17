import unittest

from solution import parse_command


class TestParseCommand(unittest.TestCase):
    def assert_error(self, input):
        result = parse_command(input)
        self.assertEqual(result["type"], "error", f'expected an error for "{input}"')
        self.assertGreater(len(result["message"]), 0, f'empty error message for "{input}"')

    def test_move_command(self):
        self.assertEqual(parse_command("move up 3"), {"type": "move", "direction": "up", "steps": 3})

    def test_extra_spaces_and_mixed_case(self):
        self.assertEqual(parse_command("  MOVE   Left 10 "), {"type": "move", "direction": "left", "steps": 10})
        self.assertEqual(parse_command("Move DOWN 007"), {"type": "move", "direction": "down", "steps": 7})

    def test_say_joins_words_with_single_spaces_and_keeps_their_case(self):
        self.assertEqual(parse_command("say Hello   there"), {"type": "say", "message": "Hello there"})
        self.assertEqual(parse_command(" SAY move up 3 "), {"type": "say", "message": "move up 3"})

    def test_quit(self):
        self.assertEqual(parse_command("quit"), {"type": "quit"})
        self.assertEqual(parse_command("  QUIT "), {"type": "quit"})

    def test_bad_direction_is_an_error(self):
        for input in ["move north 2", "move Upward 2"]:
            self.assert_error(input)

    def test_steps_must_be_whole_digits_and_at_least_1(self):
        for input in ["move up 0", "move up -1", "move up 2.5", "move up two", "move up 3x"]:
            self.assert_error(input)

    def test_wrong_number_of_words_is_an_error(self):
        for input in ["move up", "move up 2 3", "say", "say   ", "quit now"]:
            self.assert_error(input)

    def test_empty_and_unknown_input_is_an_error(self):
        for input in ["", "    ", "jump 3"]:
            self.assert_error(input)


if __name__ == "__main__":
    unittest.main(verbosity=2)
