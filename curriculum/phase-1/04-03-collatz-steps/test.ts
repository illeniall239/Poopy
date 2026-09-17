import { test } from "node:test";
import assert from "node:assert/strict";
import { collatzSteps } from "./solution.ts";

test("sequence from 6", () => {
  assert.deepEqual(collatzSteps(6), { steps: 8, peak: 16 });
});

test("1 needs no steps and its peak is itself", () => {
  assert.deepEqual(collatzSteps(1), { steps: 0, peak: 1 });
});

test("2 needs exactly one step", () => {
  assert.deepEqual(collatzSteps(2), { steps: 1, peak: 2 });
});

test("the starting number can be the peak", () => {
  assert.deepEqual(collatzSteps(16), { steps: 4, peak: 16 });
});

test("odd start climbs before falling", () => {
  assert.deepEqual(collatzSteps(7), { steps: 16, peak: 52 });
});

test("27 takes a long path", () => {
  assert.deepEqual(collatzSteps(27), { steps: 111, peak: 9232 });
});

test("large start", () => {
  assert.deepEqual(collatzSteps(837799), { steps: 524, peak: 2974984576 });
});
