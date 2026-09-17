import { test } from "node:test";
import assert from "node:assert/strict";
import { shippingCost } from "./solution.ts";

test("light parcel, including exactly 1 kg", () => {
  assert.equal(shippingCost(2000, 0.5, false), 499);
  assert.equal(shippingCost(2000, 1, false), 499);
});

test("middle tier, including exactly 5 kg", () => {
  assert.equal(shippingCost(2000, 1.5, false), 899);
  assert.equal(shippingCost(2000, 5, false), 899);
});

test("heavy tier just over 5 kg", () => {
  assert.equal(shippingCost(2000, 5.1, false), 1499);
});

test("free shipping starts at exactly 5000 cents", () => {
  assert.equal(shippingCost(4999, 3, false), 899);
  assert.equal(shippingCost(5000, 3, false), 0);
});

test("express adds 1000 and is never free", () => {
  assert.equal(shippingCost(2000, 1, true), 1499);
  assert.equal(shippingCost(6000, 3, true), 1899);
});

test("free shipping applies up to and including 20 kg", () => {
  assert.equal(shippingCost(6000, 20, false), 0);
  assert.equal(shippingCost(6000, 25, false), 1499);
});

test("over 30 kg can't ship, even with free shipping or express", () => {
  assert.equal(shippingCost(9000, 31, false), -1);
  assert.equal(shippingCost(100, 30.5, true), -1);
});

test("exactly 30 kg can still ship", () => {
  assert.equal(shippingCost(100, 30, true), 2499);
});

test("zero subtotal is not free", () => {
  assert.equal(shippingCost(0, 2, false), 899);
});
