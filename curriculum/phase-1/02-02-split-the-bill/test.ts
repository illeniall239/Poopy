import { test } from "node:test";
import assert from "node:assert/strict";
import { splitBill } from "./solution.ts";

test("leftover cent goes to one person", () => {
  assert.deepEqual(splitBill(10, 3), { shareCents: 333, peopleWithExtraCent: 1 });
});

test("even split has no extra cents", () => {
  assert.deepEqual(splitBill(12, 4), { shareCents: 300, peopleWithExtraCent: 0 });
});

test("several leftover cents", () => {
  assert.deepEqual(splitBill(100, 7), { shareCents: 1428, peopleWithExtraCent: 4 });
});

test("19.99 dollars is 1999 cents despite floating-point error", () => {
  assert.deepEqual(splitBill(19.99, 2), { shareCents: 999, peopleWithExtraCent: 1 });
});

test("0.29 dollars is 29 cents despite floating-point error", () => {
  assert.deepEqual(splitBill(0.29, 1), { shareCents: 29, peopleWithExtraCent: 0 });
});

test("fewer cents than people", () => {
  assert.deepEqual(splitBill(0.02, 3), { shareCents: 0, peopleWithExtraCent: 2 });
});

test("zero bill", () => {
  assert.deepEqual(splitBill(0, 5), { shareCents: 0, peopleWithExtraCent: 0 });
});

test("one person pays everything", () => {
  assert.deepEqual(splitBill(1.15, 1), { shareCents: 115, peopleWithExtraCent: 0 });
});
