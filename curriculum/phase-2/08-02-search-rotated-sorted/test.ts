import { test } from "node:test";
import assert from "node:assert/strict";
import { searchRotated } from "./solution.ts";

const rotated = [40, 50, 60, 10, 20, 30];

test("target in the part after the rotation point", () => {
  assert.equal(searchRotated(rotated, 20), 4);
  assert.equal(searchRotated(rotated, 10), 3);
});

test("target in the part before the rotation point", () => {
  assert.equal(searchRotated(rotated, 50), 1);
  assert.equal(searchRotated(rotated, 40), 0);
  assert.equal(searchRotated(rotated, 60), 2);
});

test("missing target", () => {
  assert.equal(searchRotated(rotated, 35), -1);
  assert.equal(searchRotated(rotated, 5), -1);
  assert.equal(searchRotated(rotated, 70), -1);
});

test("not rotated at all", () => {
  assert.equal(searchRotated([10, 20, 30, 40], 30), 2);
  assert.equal(searchRotated([10, 20, 30, 40], 25), -1);
});

test("rotated by one in each direction", () => {
  assert.equal(searchRotated([2, 3, 4, 5, 1], 1), 4);
  assert.equal(searchRotated([5, 1, 2, 3, 4], 5), 0);
  assert.equal(searchRotated([5, 1, 2, 3, 4], 4), 4);
});

test("one and two elements", () => {
  assert.equal(searchRotated([7], 7), 0);
  assert.equal(searchRotated([7], 8), -1);
  assert.equal(searchRotated([3, 1], 1), 1);
  assert.equal(searchRotated([3, 1], 3), 0);
  assert.equal(searchRotated([3, 1], 2), -1);
});

test("empty array", () => {
  assert.equal(searchRotated([], 7), -1);
});

test("every element of every rotation of a small array", () => {
  const base = [-9, -4, 0, 3, 8, 15, 21];
  let wrong = 0;
  for (let k = 0; k < base.length; k++) {
    const nums = [...base.slice(base.length - k), ...base.slice(0, base.length - k)];
    nums.forEach((v, i) => {
      if (searchRotated(nums, v) !== i) wrong++;
      if (searchRotated(nums, v + 1) !== -1) wrong++;
    });
  }
  assert.equal(wrong, 0);
});

test("100000 searches in 1000000 rotated values in O(log n)", () => {
  const n = 1000000;
  const k = 300000;
  const nums = new Array<number>(n);
  for (let j = 0; j < n; j++) nums[j] = 2 * ((j + k) % n);
  let wrong = 0;
  for (let q = 0; q < 100000; q++) {
    const i = (q * 7919) % n;
    if (searchRotated(nums, 2 * i) !== (i - k + n) % n) wrong++;
    if (searchRotated(nums, 2 * i + 1) !== -1) wrong++;
  }
  assert.equal(wrong, 0);
});
