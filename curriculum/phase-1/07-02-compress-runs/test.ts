import { test } from "node:test";
import assert from "node:assert/strict";
import { compressRuns } from "./solution.ts";

test("mixed runs", () => {
  assert.equal(compressRuns("aaabcc"), "a3bc2");
});

test("no repeats stays the same", () => {
  assert.equal(compressRuns("abc"), "abc");
});

test("same character in separate runs", () => {
  assert.equal(compressRuns("aabbaa"), "a2b2a2");
});

test("case-sensitive", () => {
  assert.equal(compressRuns("aAA"), "aA2");
});

test("empty string", () => {
  assert.equal(compressRuns(""), "");
});

test("single character", () => {
  assert.equal(compressRuns("z"), "z");
});

test("last run is included", () => {
  assert.equal(compressRuns("abcccc"), "abc4");
});

test("run length of two or more digits", () => {
  assert.equal(compressRuns("xxxxxxxxxxxxy"), "x12y");
});

test("spaces and punctuation are characters too", () => {
  assert.equal(compressRuns("hi!!  ok"), "hi!2 2ok");
});
