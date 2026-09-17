import { test } from "node:test";
import assert from "node:assert/strict";
import { wordFrequency } from "./solution.ts";

test("counts repeated words in order of first appearance", () => {
  const result = wordFrequency("the cat and the hat");
  assert.ok(result instanceof Map);
  assert.deepEqual([...result], [["the", 2], ["cat", 1], ["and", 1], ["hat", 1]]);
});

test("case-insensitive with lowercase keys", () => {
  assert.deepEqual([...wordFrequency("The THE the")], [["the", 3]]);
});

test("punctuation separates words", () => {
  assert.deepEqual([...wordFrequency("Hi, hi! HI?")], [["hi", 3]]);
});

test("digits and apostrophes separate words", () => {
  assert.deepEqual([...wordFrequency("abc123abc it's")], [["abc", 2], ["it", 1], ["s", 1]]);
});

test("empty text and text without words", () => {
  assert.equal(wordFrequency("").size, 0);
  assert.equal(wordFrequency("... 42 !").size, 0);
});

test("word at the very end is counted", () => {
  assert.deepEqual([...wordFrequency("  go go")], [["go", 2]]);
});

test("words that clash with object property names", () => {
  assert.deepEqual([...wordFrequency("constructor toString constructor")], [["constructor", 2], ["tostring", 1]]);
});
