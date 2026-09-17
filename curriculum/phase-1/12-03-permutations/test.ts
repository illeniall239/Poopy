import { test } from "node:test";
import assert from "node:assert/strict";
import { permutations } from "./solution.ts";

test("two characters", () => {
  assert.deepEqual(permutations("ab"), ["ab", "ba"]);
});

test("three characters, sorted", () => {
  assert.deepEqual(permutations("abc"), ["abc", "acb", "bac", "bca", "cab", "cba"]);
});

test("input order does not change the sorted result", () => {
  assert.deepEqual(permutations("cba"), ["abc", "acb", "bac", "bca", "cab", "cba"]);
});

test("repeated characters give distinct results only", () => {
  assert.deepEqual(permutations("aab"), ["aab", "aba", "baa"]);
  assert.deepEqual(permutations("aaa"), ["aaa"]);
});

test("single character", () => {
  assert.deepEqual(permutations("a"), ["a"]);
});

test("empty string has one ordering", () => {
  assert.deepEqual(permutations(""), [""]);
});

test("eight distinct characters give 40320 distinct results", () => {
  const result = permutations("abcdefgh");
  assert.equal(result.length, 40320);
  assert.equal(new Set(result).size, 40320);
  assert.equal(result[0], "abcdefgh");
  assert.equal(result[40319], "hgfedcba");
});
