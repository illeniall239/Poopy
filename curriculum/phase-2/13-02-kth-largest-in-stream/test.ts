import { test } from "node:test";
import assert from "node:assert/strict";
import { KthLargest } from "./solution.ts";

function addAll(tracker: KthLargest, values: number[]): (number | undefined)[] {
  return values.map((v) => tracker.add(v));
}

test("3rd largest as numbers arrive", () => {
  assert.deepEqual(addAll(new KthLargest(3), [4, 5, 8, 2, 9, 4]), [undefined, undefined, 4, 4, 5, 5]);
});

test("k = 1 tracks the maximum", () => {
  assert.deepEqual(addAll(new KthLargest(1), [3, 1, 7, 7]), [3, 3, 7, 7]);
});

test("duplicates count separately", () => {
  assert.deepEqual(addAll(new KthLargest(2), [5, 5, 5, 6, 6]), [undefined, 5, 5, 5, 6]);
});

test("negative numbers", () => {
  assert.deepEqual(addAll(new KthLargest(2), [-1, -5, -3, 0]), [undefined, -5, -3, -1]);
});

test("instances keep separate numbers", () => {
  const a = new KthLargest(2);
  const b = new KthLargest(1);
  assert.equal(a.add(1), undefined);
  assert.equal(b.add(10), 10);
  assert.equal(a.add(2), 1);
  assert.equal(b.add(3), 10);
});

test("200 000 additions with k = 50 000, O(log k) each", () => {
  const tracker = new KthLargest(50000);
  let sum = 0;
  let last: number | undefined;
  for (let i = 0; i < 200000; i++) {
    last = tracker.add((i * 7919) % 200003);
    if (last !== undefined) sum += last;
  }
  assert.equal(last, 150000);
  assert.equal(sum, 16136295473);
});
