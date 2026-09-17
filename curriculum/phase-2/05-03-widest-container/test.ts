import { test } from "node:test";
import assert from "node:assert/strict";
import { widestContainer } from "./solution.ts";

test("classic example", () => {
  assert.equal(widestContainer([1, 8, 6, 2, 5, 4, 8, 3, 7]), 49);
});

test("outer walls win despite a dip in the middle", () => {
  assert.equal(widestContainer([4, 3, 2, 1, 4]), 16);
});

test("width beats height", () => {
  assert.equal(widestContainer([1, 2, 1]), 2);
});

test("two tall neighbours beat wide short walls", () => {
  assert.equal(widestContainer([2, 3, 4, 5, 18, 17, 6]), 17);
});

test("two walls", () => {
  assert.equal(widestContainer([1, 1]), 1);
  assert.equal(widestContainer([3, 9]), 3);
});

test("fewer than two walls give 0", () => {
  assert.equal(widestContainer([]), 0);
  assert.equal(widestContainer([5]), 0);
});

test("zero-height walls hold nothing", () => {
  assert.equal(widestContainer([0, 0, 0]), 0);
  assert.equal(widestContainer([0, 4, 0, 4, 0]), 8);
});

test("does not change the input", () => {
  const heights = [3, 1, 2];
  widestContainer(heights);
  assert.deepEqual(heights, [3, 1, 2]);
});

test("200000 alternating walls in O(n)", () => {
  const n = 200000;
  const heights = Array.from({ length: n }, (_, i) => (i % 2 === 0 ? 1000 : 1));
  assert.equal(widestContainer(heights), 1000 * (n - 2));
});
