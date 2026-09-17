import { test } from "node:test";
import assert from "node:assert/strict";
import { flatten, depth, type Nested } from "./solution.ts";

test("flattens mixed nesting in left-to-right order", () => {
  assert.deepEqual(flatten([1, [2, 3], [[4]], 5]), [1, 2, 3, 4, 5]);
});

test("empty arrays contribute nothing", () => {
  assert.deepEqual(flatten([[], [[]], 6]), [6]);
  assert.deepEqual(flatten([]), []);
});

test("already flat input comes back as a new equal array", () => {
  const input = [3, 1, 2];
  const result = flatten(input);
  assert.deepEqual(result, [3, 1, 2]);
  assert.notEqual(result, input);
});

test("handles deep nesting", () => {
  let deep: Nested = 42;
  for (let i = 0; i < 100; i++) deep = [deep];
  assert.deepEqual(flatten([0, deep, 1]), [0, 42, 1]);
});

test("does not change the input", () => {
  const input = [1, [2, [3]], []];
  flatten(input);
  depth(input);
  assert.deepEqual(input, [1, [2, [3]], []]);
});

test("depth of flat arrays is 1", () => {
  assert.equal(depth([1, 2, 3]), 1);
  assert.equal(depth([]), 1);
});

test("depth takes the deepest branch", () => {
  assert.equal(depth([1, [2, [3]], [4]]), 3);
  assert.equal(depth([[4], [2, [3]]]), 3);
  assert.equal(depth([[], 1]), 2);
});
