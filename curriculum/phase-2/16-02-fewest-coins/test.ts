import { test } from "node:test";
import assert from "node:assert/strict";
import { fewestCoins } from "./solution.ts";

test("three coins make 11", () => {
  assert.equal(fewestCoins([1, 2, 5], 11), 3);
});

test("largest-first would not be fewest", () => {
  assert.equal(fewestCoins([1, 3, 4], 6), 2);
});

test("impossible amount gives -1", () => {
  assert.equal(fewestCoins([2], 3), -1);
});

test("amount 0 needs no coins", () => {
  assert.equal(fewestCoins([1], 0), 0);
});

test("unsorted coins", () => {
  assert.equal(fewestCoins([7, 3], 23), 5);
});

test("amount 700 from 3, 7 and 11", () => {
  assert.equal(fewestCoins([3, 7, 11], 700), 64);
});

test("odd amount 699 from even coins is impossible", () => {
  assert.equal(fewestCoins([4, 6], 699), -1);
});
