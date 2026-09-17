import { test } from "node:test";
import assert from "node:assert/strict";
import { last, chunk } from "./solution.ts";

test("last returns the final element", () => {
  assert.equal(last([3, 1, 4]), 4);
  assert.equal(last(["a"]), "a");
});

test("last of an empty array is undefined", () => {
  assert.equal(last([]), undefined);
});

test("last returns a falsy final element, not undefined", () => {
  assert.equal(last([1, 0]), 0);
});

test("chunk leaves a shorter final group", () => {
  assert.deepEqual(chunk([1, 2, 3, 4, 5], 2), [[1, 2], [3, 4], [5]]);
});

test("chunk with size equal to length gives one group", () => {
  assert.deepEqual(chunk(["a", "b", "c"], 3), [["a", "b", "c"]]);
});

test("chunk with size larger than length gives one group", () => {
  assert.deepEqual(chunk([1, 2], 10), [[1, 2]]);
});

test("chunk of an empty array is empty", () => {
  assert.deepEqual(chunk([], 4), []);
});

test("chunk rejects sizes below 1 or not whole", () => {
  assert.throws(() => chunk([1, 2], 0), Error);
  assert.throws(() => chunk([1, 2], -1), Error);
  assert.throws(() => chunk([1, 2], 1.5), Error);
});

test("neither function changes the input", () => {
  const items = [1, 2, 3];
  last(items);
  chunk(items, 2);
  assert.deepEqual(items, [1, 2, 3]);
});
