import { test } from "node:test";
import assert from "node:assert/strict";
import { longestCommonSubsequence } from "./solution.ts";

function makeString(n: number, m: number, mul: number): string {
  let s = "";
  for (let i = 0; i < n; i++) s += "acgt"[((i * i * mul + 3 * i + mul) % m) % 4];
  return s;
}

test("subsequence of the other string", () => {
  assert.equal(longestCommonSubsequence("abcde", "ace"), 3);
});

test("identical strings", () => {
  assert.equal(longestCommonSubsequence("abc", "abc"), 3);
});

test("no shared characters", () => {
  assert.equal(longestCommonSubsequence("abc", "def"), 0);
});

test("empty string", () => {
  assert.equal(longestCommonSubsequence("", "abc"), 0);
});

test("interleaved matches", () => {
  assert.equal(longestCommonSubsequence("AGGTAB", "GXTXAYB"), 4);
});

test("repeated characters and case matters", () => {
  assert.equal(longestCommonSubsequence("aaaa", "aa"), 2);
  assert.equal(longestCommonSubsequence("Abc", "abc"), 2);
});

test("two 1000-character strings in O(n x m)", () => {
  assert.equal(longestCommonSubsequence(makeString(1000, 7, 1), makeString(1000, 11, 3)), 648);
});
