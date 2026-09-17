import { test } from "node:test";
import assert from "node:assert/strict";
import { isLeapYear } from "./solution.ts";

test("divisible by 4 is a leap year", () => {
  assert.equal(isLeapYear(2024), true);
});

test("not divisible by 4 is not a leap year", () => {
  assert.equal(isLeapYear(2023), false);
});

test("divisible by 100 but not 400 is not a leap year", () => {
  assert.equal(isLeapYear(1900), false);
  assert.equal(isLeapYear(2100), false);
});

test("divisible by 400 is a leap year", () => {
  assert.equal(isLeapYear(2000), true);
  assert.equal(isLeapYear(2400), true);
});

test("even but not divisible by 4", () => {
  assert.equal(isLeapYear(2022), false);
});

test("small years follow the same rules", () => {
  assert.equal(isLeapYear(4), true);
  assert.equal(isLeapYear(1), false);
});

test("returns a real boolean", () => {
  assert.equal(typeof isLeapYear(2023), "boolean");
});
