import { test } from "node:test";
import assert from "node:assert/strict";
import { subsets } from "./solution.ts";

// Sorts each subset and then the list of subsets, so any output order is accepted.
function normalize(sets: number[][]): number[][] {
  return sets
    .map((s) => [...s].sort((a, b) => a - b))
    .sort((x, y) => {
      for (let i = 0; i < Math.min(x.length, y.length); i++) if (x[i] !== y[i]) return x[i] - y[i];
      return x.length - y.length;
    });
}

function distinctCount(sets: number[][]): number {
  return new Set(normalize(sets).map((s) => s.join(","))).size;
}

test("all subsets of three numbers", () => {
  assert.deepEqual(normalize(subsets([1, 2, 3])), normalize([[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]));
});

test("empty array has only the empty subset", () => {
  assert.deepEqual(subsets([]), [[]]);
});

test("one number", () => {
  assert.deepEqual(normalize(subsets([5])), [[], [5]]);
});

test("negative and unsorted numbers", () => {
  assert.deepEqual(normalize(subsets([3, -1])), [[], [-1], [-1, 3], [3]]);
});

test("each stored subset is its own copy", () => {
  const nums = [4, 8, 15, 16, 23, 42, -1, -2, -3, 0];
  const result = subsets(nums);
  assert.equal(result.length, 1024);
  assert.equal(distinctCount(result), 1024);
  assert.deepEqual(nums, [4, 8, 15, 16, 23, 42, -1, -2, -3, 0]);
});

test("all 65 536 subsets of 16 numbers", () => {
  const nums = Array.from({ length: 16 }, (_, i) => i * 3 - 20);
  const result = subsets(nums);
  assert.equal(result.length, 65536);
  assert.equal(distinctCount(result), 65536);
});
