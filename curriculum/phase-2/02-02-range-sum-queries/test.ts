import { test } from "node:test";
import assert from "node:assert/strict";
import { rangeSums } from "./solution.ts";

test("several ranges, including one starting at index 0", () => {
  assert.deepEqual(rangeSums([3, -2, 5, 1, 4], [[0, 2], [1, 3], [2, 4]]), [6, 4, 10]);
});

test("a single-element range and the whole array", () => {
  assert.deepEqual(rangeSums([3, -2, 5, 1, 4], [[3, 3], [0, 4]]), [1, 11]);
});

test("no queries gives an empty result", () => {
  assert.deepEqual(rangeSums([7], []), []);
});

test("all negative values", () => {
  assert.deepEqual(rangeSums([-4, -6, -1], [[0, 1], [1, 2], [0, 0]]), [-10, -7, -4]);
});

test("answers stay in query order, repeats included", () => {
  assert.deepEqual(rangeSums([2, 9, 4], [[2, 2], [0, 0], [2, 2], [0, 2]]), [4, 2, 4, 15]);
});

test("does not change the inputs", () => {
  const values = [1, 2, 3];
  const queries: [number, number][] = [[0, 2]];
  rangeSums(values, queries);
  assert.deepEqual(values, [1, 2, 3]);
  assert.deepEqual(queries, [[0, 2]]);
});

test("200000 long queries over 200000 values in O(n + q)", () => {
  const n = 200000;
  const values = Array.from({ length: n }, (_, i) => i);
  const queries: [number, number][] = [];
  const expected: number[] = [];
  for (let q = 0; q < n; q++) {
    const i = q % (n / 2);
    const j = n - 1 - i;
    queries.push([i, j]);
    expected.push(((i + j) * (j - i + 1)) / 2);
  }
  assert.deepEqual(rangeSums(values, queries), expected);
});
