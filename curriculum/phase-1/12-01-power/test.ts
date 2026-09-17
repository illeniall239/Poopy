import { test } from "node:test";
import assert from "node:assert/strict";
import { power } from "./solution.ts";

test("even exponent", () => {
  assert.equal(power(2, 10), 1024);
});

test("odd exponent", () => {
  assert.equal(power(3, 5), 243);
  assert.equal(power(3, 13), 1594323);
});

test("exponent 0 gives 1, even for base 0", () => {
  assert.equal(power(5, 0), 1);
  assert.equal(power(0, 0), 1);
});

test("exponent 1 gives the base", () => {
  assert.equal(power(7, 1), 7);
});

test("negative base keeps the right sign", () => {
  assert.equal(power(-2, 3), -8);
  assert.equal(power(-2, 4), 16);
});

test("decimal base", () => {
  assert.equal(power(0.5, 3), 0.125);
});

test("huge exponent finishes without overflowing the stack", () => {
  assert.equal(power(1, 1000000000), 1);
  assert.equal(power(-1, 999999999), -1);
  assert.equal(power(2, 1023), 2 ** 1023);
});
