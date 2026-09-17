import { test } from "node:test";
import assert from "node:assert/strict";
import { makeChange } from "./solution.ts";

test("one of each coin for 41", () => {
  assert.deepEqual(makeChange(41), { quarters: 1, dimes: 1, nickels: 1, pennies: 1 });
});

test("skips coins that aren't needed", () => {
  assert.deepEqual(makeChange(30), { quarters: 1, dimes: 0, nickels: 1, pennies: 0 });
});

test("zero cents gives no coins", () => {
  assert.deepEqual(makeChange(0), { quarters: 0, dimes: 0, nickels: 0, pennies: 0 });
});

test("pennies only below 5", () => {
  assert.deepEqual(makeChange(4), { quarters: 0, dimes: 0, nickels: 0, pennies: 4 });
});

test("exact multiple of 25", () => {
  assert.deepEqual(makeChange(100), { quarters: 4, dimes: 0, nickels: 0, pennies: 0 });
});

test("two dimes, no nickel for 20 after quarters", () => {
  assert.deepEqual(makeChange(99), { quarters: 3, dimes: 2, nickels: 0, pennies: 4 });
});

test("large amount", () => {
  assert.deepEqual(makeChange(100000), { quarters: 4000, dimes: 0, nickels: 0, pennies: 0 });
});
