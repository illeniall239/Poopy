import { test } from "node:test";
import assert from "node:assert/strict";
import { findSeat } from "./solution.ts";

test("first seat is row 1, column 1", () => {
  assert.deepEqual(findSeat(1, 10), { row: 1, column: 1 });
});

test("seat in the middle of a later row", () => {
  assert.deepEqual(findSeat(25, 10), { row: 3, column: 5 });
});

test("last seat in a row stays in that row", () => {
  assert.deepEqual(findSeat(10, 10), { row: 1, column: 10 });
});

test("seat after the last seat starts the next row", () => {
  assert.deepEqual(findSeat(11, 10), { row: 2, column: 1 });
});

test("last seat of a later row", () => {
  assert.deepEqual(findSeat(12, 4), { row: 3, column: 4 });
});

test("one seat per row", () => {
  assert.deepEqual(findSeat(7, 1), { row: 7, column: 1 });
});

test("large seat number", () => {
  assert.deepEqual(findSeat(1000000, 999), { row: 1002, column: 1 });
});
