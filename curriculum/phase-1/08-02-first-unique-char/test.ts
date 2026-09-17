import { test } from "node:test";
import assert from "node:assert/strict";
import { firstUniqueIndex } from "./solution.ts";

test("first character is unique", () => {
  assert.equal(firstUniqueIndex("leetcode"), 0);
});

test("unique character in the middle", () => {
  assert.equal(firstUniqueIndex("loveleetcode"), 2);
});

test("no unique character", () => {
  assert.equal(firstUniqueIndex("aabb"), -1);
});

test("empty string", () => {
  assert.equal(firstUniqueIndex(""), -1);
});

test("case-sensitive", () => {
  assert.equal(firstUniqueIndex("aA"), 0);
  assert.equal(firstUniqueIndex("aAa"), 1);
});

test("a character that repeats later is not unique", () => {
  assert.equal(firstUniqueIndex("abcabd"), 2);
});

test("unique character at the end", () => {
  assert.equal(firstUniqueIndex("xyxyz"), 4);
});

test("spaces count as characters", () => {
  assert.equal(firstUniqueIndex("aa bb"), 2);
});

test("long string is handled quickly", () => {
  let text = "";
  for (let i = 0; i < 50000; i++) text += "ab";
  assert.equal(firstUniqueIndex(text + "c"), 100000);
});
