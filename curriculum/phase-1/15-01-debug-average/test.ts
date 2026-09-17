import { test } from "node:test";
import assert from "node:assert/strict";
import { average } from "./solution.ts";

test("empty array gives undefined", () => {
  assert.equal(average([]), undefined);
});

test("all zeros average to 0", () => {
  assert.equal(average([0, 0, 0]), 0);
});

test("single value is its own average", () => {
  assert.equal(average([5]), 5);
});

test("whole-number average", () => {
  assert.equal(average([2, 4, 6]), 4);
});

test("average is not rounded", () => {
  assert.equal(average([1, 2]), 1.5);
  assert.equal(average([1, 1, 2]), 4 / 3);
});

test("negative numbers", () => {
  assert.equal(average([-1, -2]), -1.5);
});

test("first element counts", () => {
  assert.equal(average([100, 0, 0, 0]), 25);
});
