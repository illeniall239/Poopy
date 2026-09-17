import { test } from "node:test";
import assert from "node:assert/strict";
import { digitSumUntilSingle } from "./solution.ts";

test("one pass is enough", () => {
  assert.equal(digitSumUntilSingle(16), 7);
});

test("needs several passes", () => {
  assert.equal(digitSumUntilSingle(493193), 2);
});

test("10 is two digits and becomes 1", () => {
  assert.equal(digitSumUntilSingle(10), 1);
});

test("a single digit is returned unchanged", () => {
  assert.equal(digitSumUntilSingle(0), 0);
  assert.equal(digitSumUntilSingle(9), 9);
});

test("sum that lands exactly on 10", () => {
  assert.equal(digitSumUntilSingle(19), 1);
});

test("zeros inside the number", () => {
  assert.equal(digitSumUntilSingle(1000000), 1);
});

test("largest safe integer", () => {
  assert.equal(digitSumUntilSingle(9007199254740991), 4);
});
