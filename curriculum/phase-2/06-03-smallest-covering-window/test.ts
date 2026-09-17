import { test } from "node:test";
import assert from "node:assert/strict";
import { smallestCoveringWindow } from "./solution.ts";

test("classic example", () => {
  assert.equal(smallestCoveringWindow("ADOBECODEBANC", "ABC"), "BANC");
});

test("characters may appear in any order", () => {
  assert.equal(smallestCoveringWindow("abzcxcba", "abc"), "cba");
  assert.equal(smallestCoveringWindow("bba", "ab"), "ba");
});

test("leftmost of equally short windows", () => {
  assert.equal(smallestCoveringWindow("acbxbca", "abc"), "acb");
});

test("repeats in t must be covered", () => {
  assert.equal(smallestCoveringWindow("aa", "aa"), "aa");
  assert.equal(smallestCoveringWindow("a", "aa"), "");
  assert.equal(smallestCoveringWindow("abcaba", "aab"), "aba");
});

test("whole string is the only window", () => {
  assert.equal(smallestCoveringWindow("a", "a"), "a");
  assert.equal(smallestCoveringWindow("xyz", "zyx"), "xyz");
});

test("empty t or empty s gives an empty string", () => {
  assert.equal(smallestCoveringWindow("abc", ""), "");
  assert.equal(smallestCoveringWindow("", "a"), "");
  assert.equal(smallestCoveringWindow("", ""), "");
});

test("no window at all", () => {
  assert.equal(smallestCoveringWindow("abc", "d"), "");
  assert.equal(smallestCoveringWindow("ABC", "abc"), "");
});

test("200000 characters with the window at the end in O(n)", () => {
  const n = 200000;
  const s = "a".repeat(n - 1) + "b";
  assert.equal(smallestCoveringWindow(s, "ab"), "ab");
});
