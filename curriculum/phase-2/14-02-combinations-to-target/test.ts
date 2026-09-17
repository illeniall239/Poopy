import { test } from "node:test";
import assert from "node:assert/strict";
import { combinationsToTarget } from "./solution.ts";

// Sorts each combination and then the list, so any output order is accepted.
function normalize(combos: number[][]): number[][] {
  return combos
    .map((c) => [...c].sort((a, b) => a - b))
    .sort((x, y) => {
      for (let i = 0; i < Math.min(x.length, y.length); i++) if (x[i] !== y[i]) return x[i] - y[i];
      return x.length - y.length;
    });
}

test("one repeat and one single", () => {
  assert.deepEqual(normalize(combinationsToTarget([2, 3, 6, 7], 7)), [[2, 2, 3], [7]]);
});

test("three combinations", () => {
  assert.deepEqual(normalize(combinationsToTarget([2, 3, 5], 8)), [[2, 2, 2, 2], [2, 3, 3], [3, 5]]);
});

test("no combination possible", () => {
  assert.deepEqual(combinationsToTarget([2], 1), []);
});

test("same candidate many times", () => {
  assert.deepEqual(normalize(combinationsToTarget([1], 3)), [[1, 1, 1]]);
});

test("unsorted candidates, no duplicate combinations", () => {
  const candidates = [8, 4, 2];
  assert.deepEqual(normalize(combinationsToTarget(candidates, 8)), [[2, 2, 2, 2], [2, 2, 4], [4, 4], [8]]);
  assert.deepEqual(candidates, [8, 4, 2]);
});

test("order does not make a new combination", () => {
  assert.deepEqual(normalize(combinationsToTarget([1, 2], 4)), [[1, 1, 1, 1], [1, 1, 2], [2, 2]]);
});

test("531 combinations for target 60", () => {
  const result = normalize(combinationsToTarget([2, 3, 5, 7, 11], 60));
  assert.equal(result.length, 531);
  assert.equal(new Set(result.map((c) => c.join(","))).size, 531);
  for (const c of result) {
    assert.equal(c.reduce((a, b) => a + b, 0), 60);
    assert.ok(c.every((v) => [2, 3, 5, 7, 11].includes(v)));
  }
});
