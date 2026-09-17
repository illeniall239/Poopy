import { test } from "node:test";
import assert from "node:assert/strict";
import { minShredSpeed } from "./solution.ts";

test("speed between the smallest and largest stack", () => {
  assert.equal(minShredSpeed([3, 6, 7, 11], 8), 4);
});

test("one hour per stack needs the largest stack as speed", () => {
  assert.equal(minShredSpeed([30, 11, 23, 4, 20], 5), 30);
});

test("one extra hour lowers the speed", () => {
  assert.equal(minShredSpeed([30, 11, 23, 4, 20], 6), 23);
});

test("a partial last hour still counts as an hour", () => {
  assert.equal(minShredSpeed([10], 3), 4);
  assert.equal(minShredSpeed([10], 5), 2);
  assert.equal(minShredSpeed([10], 10), 1);
});

test("plenty of time gives speed 1", () => {
  assert.equal(minShredSpeed([5, 5], 1000000000), 1);
});

test("single one-page stack", () => {
  assert.equal(minShredSpeed([1], 1), 1);
});

test("does not change the input", () => {
  const stacks = [11, 3, 7];
  minShredSpeed(stacks, 5);
  assert.deepEqual(stacks, [11, 3, 7]);
});

test("huge stacks with the answer far from both ends, in O(n log m)", () => {
  const n = 100000;
  const stacks = new Array<number>(n).fill(1);
  stacks[n >> 1] = 1000000000;
  assert.equal(minShredSpeed(stacks, n + 1), 500000000);
  stacks[0] = 999999999;
  assert.equal(minShredSpeed(stacks, n + 4), 333333334);
});
