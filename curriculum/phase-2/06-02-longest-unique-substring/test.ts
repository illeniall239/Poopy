import { test } from "node:test";
import assert from "node:assert/strict";
import { longestUniqueSubstring } from "./solution.ts";

test("repeating pattern", () => {
  assert.equal(longestUniqueSubstring("abcabcbb"), 3);
});

test("one repeated character", () => {
  assert.equal(longestUniqueSubstring("bbbbb"), 1);
});

test("substring must be contiguous", () => {
  assert.equal(longestUniqueSubstring("pwwkew"), 3);
  assert.equal(longestUniqueSubstring("dvdf"), 3);
});

test("left edge never moves backwards", () => {
  assert.equal(longestUniqueSubstring("abba"), 2);
  assert.equal(longestUniqueSubstring("tmmzuxt"), 5);
});

test("all characters distinct", () => {
  assert.equal(longestUniqueSubstring("abcdef"), 6);
  assert.equal(longestUniqueSubstring("x"), 1);
});

test("empty string gives 0", () => {
  assert.equal(longestUniqueSubstring(""), 0);
});

test("spaces, digits and non-ASCII characters count as characters", () => {
  assert.equal(longestUniqueSubstring("a b a"), 3);
  assert.equal(longestUniqueSubstring("1231"), 3);
  assert.equal(longestUniqueSubstring("ñañb"), 3);
});

test("100000 characters over a large alphabet in O(n)", () => {
  const m = 50000;
  let distinct = "";
  for (let i = 0; i < m; i++) distinct += String.fromCharCode(0x100 + i);
  assert.equal(longestUniqueSubstring(distinct + distinct), m);
});
