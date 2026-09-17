import { test } from "node:test";
import assert from "node:assert/strict";
import { canReachLastIndex } from "./solution.ts";

test("reachable with a choice of routes", () => {
  assert.equal(canReachLastIndex([2, 3, 1, 1, 4]), true);
});

test("every route lands on a zero", () => {
  assert.equal(canReachLastIndex([3, 2, 1, 0, 4]), false);
});

test("single square", () => {
  assert.equal(canReachLastIndex([0]), true);
});

test("two squares", () => {
  assert.equal(canReachLastIndex([0, 1]), false);
  assert.equal(canReachLastIndex([1, 0]), true);
});

test("landing exactly on the last square", () => {
  assert.equal(canReachLastIndex([2, 0, 0]), true);
});

test("jumping past the end counts as reaching it", () => {
  assert.equal(canReachLastIndex([10, 0, 0]), true);
});

test("stuck before the end despite a later non-zero", () => {
  assert.equal(canReachLastIndex([4, 1, 1, 0, 0, 1]), false);
});

test("200000 squares reachable in O(n)", () => {
  const n = 200000;
  const jumps = Array.from({ length: n }, (_, i) => n - 1 - i);
  assert.equal(canReachLastIndex(jumps), true);
});

test("200000 squares unreachable in O(n)", () => {
  const n = 200000;
  const jumps = Array.from({ length: n }, (_, i) => Math.max(0, n - 2 - i));
  assert.equal(canReachLastIndex(jumps), false);
});
