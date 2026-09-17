import { test } from "node:test";
import assert from "node:assert/strict";
import { runningAverages } from "./solution.ts";

test("increasing numbers", () => {
  assert.deepEqual(runningAverages([1, 2, 3, 4]), [1, 1.5, 2, 2.5]);
});

test("negative numbers pull the average down", () => {
  assert.deepEqual(runningAverages([10, -10, 6]), [10, 0, 2]);
});

test("single element", () => {
  assert.deepEqual(runningAverages([5]), [5]);
});

test("empty array gives empty array", () => {
  assert.deepEqual(runningAverages([]), []);
});

test("constant values keep a constant average", () => {
  assert.deepEqual(runningAverages([4, 4, 4, 4]), [4, 4, 4, 4]);
});

test("first element is its own average (divide by count so far)", () => {
  assert.deepEqual(runningAverages([8, 0, 0, 0]), [8, 4, 8 / 3, 2]);
});

test("does not modify the input", () => {
  const nums = [3, 5, 7];
  const result = runningAverages(nums);
  assert.deepEqual(nums, [3, 5, 7]);
  assert.notEqual(result, nums);
});

test("large input", () => {
  const nums: number[] = [];
  for (let i = 0; i < 100000; i++) nums.push(2);
  const result = runningAverages(nums);
  assert.equal(result.length, 100000);
  assert.equal(result[99999], 2);
});
