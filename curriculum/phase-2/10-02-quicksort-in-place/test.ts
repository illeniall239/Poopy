import { test } from "node:test";
import assert from "node:assert/strict";
import { quickSort } from "./solution.ts";

function sorted(nums: number[]): number[] {
  quickSort(nums);
  return nums;
}

function isAscending(nums: number[]): boolean {
  for (let i = 1; i < nums.length; i++) if (nums[i - 1] > nums[i]) return false;
  return true;
}

const N = 200000;

test("sorts a small array with a duplicate", () => {
  assert.deepEqual(sorted([5, 2, 9, 1, 5, 6]), [1, 2, 5, 5, 6, 9]);
});

test("compares as numbers, with negatives", () => {
  assert.deepEqual(sorted([10, -3, 9, 100, 0, -1000000000, 1]), [-1000000000, -3, 0, 1, 9, 10, 100]);
});

test("empty, single and two-element arrays", () => {
  assert.deepEqual(sorted([]), []);
  assert.deepEqual(sorted([42]), [42]);
  assert.deepEqual(sorted([2, 1]), [1, 2]);
});

test("sorts the same array in place and returns nothing", () => {
  const nums = [3, 1, 2];
  const returned = quickSort(nums);
  assert.equal(returned, undefined);
  assert.deepEqual(nums, [1, 2, 3]);
});

test("many repeated values", () => {
  assert.deepEqual(sorted([2, 1, 2, 3, 1, 2, 3, 1, 2]), [1, 1, 1, 2, 2, 2, 2, 3, 3]);
});

test("200000 shuffled numbers", () => {
  const nums = Array.from({ length: N }, (_, i) => ((i * 7919 + 13) % 1000003) - 500000);
  const expected = nums.slice().sort((a, b) => a - b);
  quickSort(nums);
  assert.ok(nums.length === N && nums.every((v, i) => v === expected[i]), "not sorted correctly");
});

test("200000 numbers already sorted and reversed", () => {
  const up = Array.from({ length: N }, (_, i) => i);
  const down = Array.from({ length: N }, (_, i) => N - i);
  quickSort(up);
  quickSort(down);
  assert.ok(isAscending(up) && up[0] === 0 && up[N - 1] === N - 1, "sorted input came out wrong");
  assert.ok(isAscending(down) && down[0] === 1 && down[N - 1] === N, "reversed input came out wrong");
});

test("200000 equal values", () => {
  const same = new Array<number>(N).fill(7);
  quickSort(same);
  assert.ok(same.length === N && same.every((v) => v === 7));
});

test("200000 values drawn from only three numbers", () => {
  const few = Array.from({ length: N }, (_, i) => (i * 7) % 3);
  quickSort(few);
  const counts = [0, 0, 0];
  for (const v of few) counts[v]++;
  assert.ok(isAscending(few), "not in ascending order");
  assert.deepEqual(counts, [66667, 66667, 66666]);
});
