import unittest

from solution import max_call_depth


class TestMaxCallDepth(unittest.TestCase):
    def test_entry_that_calls_nothing_is_one_frame(self):
        self.assertEqual(max_call_depth({"main": []}, "main"), 1)

    def test_a_chain_of_nested_calls(self):
        self.assertEqual(max_call_depth({"main": ["parse"], "parse": ["readFile"]}, "main"), 3)

    def test_calls_made_one_after_another_do_not_stack_up(self):
        self.assertEqual(max_call_depth({"main": ["log", "log", "save"], "save": []}, "main"), 2)

    def test_picks_the_deepest_branch(self):
        self.assertEqual(max_call_depth({"main": ["a", "b"], "a": [], "b": ["c"], "c": ["d"]}, "main"), 4)

    def test_a_shared_helper_reached_twice_is_not_recursion(self):
        calls = {"main": ["a", "b"], "a": ["util"], "b": ["util"], "util": []}
        self.assertEqual(max_call_depth(calls, "main"), 3)

    def test_a_function_calling_itself_recurses_forever(self):
        self.assertEqual(max_call_depth({"main": ["loop"], "loop": ["loop"]}, "main"), -1)

    def test_mutual_recursion_off_the_deepest_path_recurses_forever(self):
        calls = {
            "main": ["deep", "isEven"], "deep": ["x"], "x": ["y"], "y": ["z"],
            "isEven": ["isOdd"], "isOdd": ["isEven"],
        }
        self.assertEqual(max_call_depth(calls, "main"), -1)

    def test_a_cycle_that_entry_never_reaches_does_not_matter(self):
        self.assertEqual(max_call_depth({"main": ["a"], "a": [], "b": ["c"], "c": ["b"]}, "main"), 2)

    def test_300_layers_of_shared_helpers_finish_quickly(self):
        layers = 300
        calls = {}
        for i in range(layers):
            calls[f"f{i}"] = [f"a{i}", f"b{i}"]
            calls[f"a{i}"] = [f"f{i + 1}"]
            calls[f"b{i}"] = [f"f{i + 1}"]
        self.assertEqual(max_call_depth(calls, "f0"), 2 * layers + 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
