import { test } from "node:test";
import assert from "node:assert/strict";
import { maxAndMin } from "./solution.ts";

test("mixed positive numbers", () => {
  assert.deepEqual(maxAndMin([3, 9, 1, 4]), { max: 9, min: 1 });
});

test("all negative numbers (max is not 0)", () => {
  assert.deepEqual(maxAndMin([-5, -2, -8]), { max: -2, min: -8 });
});

test("all positive numbers (min is not 0)", () => {
  assert.deepEqual(maxAndMin([12, 40, 7, 30]), { max: 40, min: 7 });
});

test("single element is both max and min", () => {
  assert.deepEqual(maxAndMin([7]), { max: 7, min: 7 });
});

test("empty array returns undefined", () => {
  assert.equal(maxAndMin([]), undefined);
});

test("max first and min last", () => {
  assert.deepEqual(maxAndMin([100, 50, 0, -50]), { max: 100, min: -50 });
});

test("decimals and repeated values", () => {
  assert.deepEqual(maxAndMin([2.5, 2.5, -0.5, 2.5]), { max: 2.5, min: -0.5 });
});

test("does not modify the input", () => {
  const nums = [4, 1, 3];
  maxAndMin(nums);
  assert.deepEqual(nums, [4, 1, 3]);
});
