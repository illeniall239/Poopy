import { test } from "node:test";
import assert from "node:assert/strict";
import { groupAnagrams } from "./solution.ts";

test("groups anagrams in order of first appearance", () => {
  assert.deepEqual(groupAnagrams(["eat", "tea", "tan", "ate", "nat", "bat"]), [
    ["eat", "tea", "ate"],
    ["tan", "nat"],
    ["bat"],
  ]);
});

test("different lengths are never anagrams", () => {
  assert.deepEqual(groupAnagrams(["ab", "abc", "ba"]), [["ab", "ba"], ["abc"]]);
});

test("empty input", () => {
  assert.deepEqual(groupAnagrams([]), []);
});

test("no anagrams gives one group per word", () => {
  assert.deepEqual(groupAnagrams(["cat", "dog", "bird"]), [["cat"], ["dog"], ["bird"]]);
});

test("same letters but different counts are not anagrams", () => {
  assert.deepEqual(groupAnagrams(["aab", "abb", "bab"]), [["aab"], ["abb", "bab"]]);
});

test("duplicate words stay in the same group", () => {
  assert.deepEqual(groupAnagrams(["stop", "pots", "stop"]), [["stop", "pots", "stop"]]);
});

test("does not modify the input", () => {
  const words = ["tops", "spot", "a"];
  groupAnagrams(words);
  assert.deepEqual(words, ["tops", "spot", "a"]);
});
