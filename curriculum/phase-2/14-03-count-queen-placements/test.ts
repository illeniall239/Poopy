import { test } from "node:test";
import assert from "node:assert/strict";
import { countQueens } from "./solution.ts";

test("one queen on a 1x1 board", () => {
  assert.equal(countQueens(1), 1);
});

test("no placement on a 2x2 board", () => {
  assert.equal(countQueens(2), 0);
});

test("no placement on a 3x3 board", () => {
  assert.equal(countQueens(3), 0);
});

test("two placements on a 4x4 board", () => {
  assert.equal(countQueens(4), 2);
});

test("four placements on a 6x6 board", () => {
  assert.equal(countQueens(6), 4);
});

test("92 placements on an 8x8 board", () => {
  assert.equal(countQueens(8), 92);
});

test("12x12 board needs pruning", () => {
  assert.equal(countQueens(12), 14200);
});
