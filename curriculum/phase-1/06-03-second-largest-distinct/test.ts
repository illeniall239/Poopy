import { test } from "node:test";
import assert from "node:assert/strict";
import { secondLargest } from "./solution.ts";

test("unsorted distinct values", () => {
  assert.equal(secondLargest([3, 1, 2]), 2);
});

test("duplicates of the largest are skipped", () => {
  assert.equal(secondLargest([5, 5, 4]), 4);
});

test("all negative numbers", () => {
  assert.equal(secondLargest([-1, -3, -2]), -2);
});

test("all values equal gives undefined", () => {
  assert.equal(secondLargest([7, 7, 7]), undefined);
});

test("empty and single-element arrays give undefined", () => {
  assert.equal(secondLargest([]), undefined);
  assert.equal(secondLargest([9]), undefined);
});

test("new largest pushes old largest into second place", () => {
  assert.equal(secondLargest([1, 2, 3, 10]), 3);
});

test("second largest appears after the largest", () => {
  assert.equal(secondLargest([10, 1, 8, 10, 8]), 8);
});

test("zero can be the answer", () => {
  assert.equal(secondLargest([0, -4, 6]), 0);
});

test("does not modify the input", () => {
  const nums = [4, 9, 2, 9];
  secondLargest(nums);
  assert.deepEqual(nums, [4, 9, 2, 9]);
});
