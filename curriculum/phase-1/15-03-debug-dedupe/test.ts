import { test } from "node:test";
import assert from "node:assert/strict";
import { dedupe } from "./solution.ts";

test("removes scattered duplicates, keeping first appearances", () => {
  assert.deepEqual(dedupe([1, 2, 1, 3, 2]), [1, 2, 3]);
});

test("removes runs of the same number", () => {
  assert.deepEqual(dedupe([5, 5, 5, 5]), [5]);
  assert.deepEqual(dedupe([1, 1, 2, 2, 2, 3]), [1, 2, 3]);
});

test("empty array", () => {
  assert.deepEqual(dedupe([]), []);
});

test("does not change the input", () => {
  const input = [4, 4, 7];
  assert.deepEqual(dedupe(input), [4, 7]);
  assert.deepEqual(input, [4, 4, 7]);
});

test("returns a new array even without duplicates", () => {
  const input = [3, 1, 2];
  const result = dedupe(input);
  assert.deepEqual(result, [3, 1, 2]);
  assert.notEqual(result, input);
});

test("keeps the position of each first appearance", () => {
  assert.deepEqual(dedupe([2, 9, 2, 9, 0, 2]), [2, 9, 0]);
});
