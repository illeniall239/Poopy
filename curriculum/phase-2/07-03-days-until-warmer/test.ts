import { test } from "node:test";
import assert from "node:assert/strict";
import { daysUntilWarmer } from "./solution.ts";

test("mixed week", () => {
  assert.deepEqual(daysUntilWarmer([73, 74, 75, 71, 69, 72, 76, 73]), [1, 1, 4, 2, 1, 1, 0, 0]);
});

test("rising temperatures", () => {
  assert.deepEqual(daysUntilWarmer([30, 40, 50, 60]), [1, 1, 1, 0]);
});

test("falling temperatures never get warmer", () => {
  assert.deepEqual(daysUntilWarmer([60, 50, 40]), [0, 0, 0]);
});

test("equal temperature is not warmer", () => {
  assert.deepEqual(daysUntilWarmer([5, 5, 6]), [2, 1, 0]);
  assert.deepEqual(daysUntilWarmer([7, 7, 7]), [0, 0, 0]);
});

test("empty and single day", () => {
  assert.deepEqual(daysUntilWarmer([]), []);
  assert.deepEqual(daysUntilWarmer([-3]), [0]);
});

test("negative temperatures", () => {
  assert.deepEqual(daysUntilWarmer([-10, -20, -5, -30, 0]), [2, 1, 2, 1, 0]);
});

test("does not change the input", () => {
  const temps = [3, 1, 2];
  daysUntilWarmer(temps);
  assert.deepEqual(temps, [3, 1, 2]);
});

test("1000000 days in O(n)", () => {
  const n = 1000000;
  const temps = new Array<number>(n);
  for (let i = 0; i < n - 1; i++) temps[i] = n - i;
  temps[n - 1] = n + 1;
  const result = daysUntilWarmer(temps);
  let wrong = 0;
  for (let i = 0; i < n - 1; i++) if (result[i] !== n - 1 - i) wrong++;
  assert.equal(wrong, 0);
  assert.equal(result[n - 1], 0);
});
