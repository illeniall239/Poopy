import { test } from "node:test";
import assert from "node:assert/strict";
import { climbWays } from "./solution.ts";

test("zero steps: one way (do nothing)", () => {
  assert.equal(climbWays(0), 1);
});

test("one step", () => {
  assert.equal(climbWays(1), 1);
});

test("two steps", () => {
  assert.equal(climbWays(2), 2);
});

test("three steps", () => {
  assert.equal(climbWays(3), 3);
});

test("five steps", () => {
  assert.equal(climbWays(5), 8);
});

test("ten steps", () => {
  assert.equal(climbWays(10), 89);
});

test("45 steps needs stored sub-answers", () => {
  assert.equal(climbWays(45), 1836311903);
});

test("70 steps", () => {
  assert.equal(climbWays(70), 308061521170129);
});
