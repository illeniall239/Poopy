import { test } from "node:test";
import assert from "node:assert/strict";
import { sumOfMultiples } from "./solution.ts";

test("multiples below 10", () => {
  assert.equal(sumOfMultiples(10), 23);
});

test("15 is counted once, not twice", () => {
  assert.equal(sumOfMultiples(16), 60);
});

test("n itself is not included", () => {
  assert.equal(sumOfMultiples(3), 0);
  assert.equal(sumOfMultiples(15), 45);
});

test("the first multiple just below n is included", () => {
  assert.equal(sumOfMultiples(4), 3);
});

test("zero and one give zero", () => {
  assert.equal(sumOfMultiples(0), 0);
  assert.equal(sumOfMultiples(1), 0);
});

test("larger n", () => {
  assert.equal(sumOfMultiples(1000), 233168);
});
