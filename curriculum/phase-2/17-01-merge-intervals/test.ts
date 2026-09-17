import { test } from "node:test";
import assert from "node:assert/strict";
import { mergeIntervals } from "./solution.ts";

test("merges overlapping neighbours", () => {
  assert.deepEqual(mergeIntervals([[1, 3], [2, 6], [8, 10], [15, 18]]), [[1, 6], [8, 10], [15, 18]]);
});

test("touching endpoints merge", () => {
  assert.deepEqual(mergeIntervals([[1, 4], [4, 5]]), [[1, 5]]);
  assert.deepEqual(mergeIntervals([[1, 3], [4, 5]]), [[1, 3], [4, 5]]);
});

test("unsorted input", () => {
  assert.deepEqual(mergeIntervals([[8, 10], [1, 3], [2, 6]]), [[1, 6], [8, 10]]);
  assert.deepEqual(mergeIntervals([[5, 6], [1, 2]]), [[1, 2], [5, 6]]);
});

test("nested intervals disappear into the outer one", () => {
  assert.deepEqual(mergeIntervals([[1, 10], [2, 3], [4, 5]]), [[1, 10]]);
  assert.deepEqual(mergeIntervals([[2, 3], [1, 10]]), [[1, 10]]);
});

test("a chain of overlaps merges into one", () => {
  assert.deepEqual(mergeIntervals([[1, 2], [2, 3], [3, 4], [4, 5]]), [[1, 5]]);
});

test("negative bounds and single-point intervals", () => {
  assert.deepEqual(mergeIntervals([[-5, -1], [-2, 0], [3, 4]]), [[-5, 0], [3, 4]]);
  assert.deepEqual(mergeIntervals([[5, 5], [5, 5], [7, 7]]), [[5, 5], [7, 7]]);
});

test("empty input and a single interval", () => {
  assert.deepEqual(mergeIntervals([]), []);
  assert.deepEqual(mergeIntervals([[1, 2]]), [[1, 2]]);
});

test("does not change the input or return its pairs", () => {
  const first: [number, number] = [4, 6];
  const intervals: [number, number][] = [first, [1, 5], [9, 9]];
  const result = mergeIntervals(intervals);
  assert.deepEqual(result, [[1, 6], [9, 9]]);
  assert.deepEqual(intervals, [[4, 6], [1, 5], [9, 9]]);
  assert.deepEqual(first, [4, 6]);
  assert.ok(result.every((pair) => !intervals.includes(pair)), "result must hold new pairs");
});

test("200000 shuffled disjoint intervals in O(n log n)", () => {
  const n = 200000;
  const intervals: [number, number][] = Array.from({ length: n }, (_, i) => {
    const k = (i * 7919) % n;
    return [3 * k, 3 * k + 1];
  });
  const result = mergeIntervals(intervals);
  assert.equal(result.length, n);
  assert.ok(result.every((pair, i) => pair[0] === 3 * i && pair[1] === 3 * i + 1), "result is not sorted and disjoint");
});
