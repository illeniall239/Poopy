import { test } from "node:test";
import assert from "node:assert/strict";
import { grandTotal, totalsByCustomer } from "./solution.ts";

const orders = [
  { customer: "ana", amountCents: 1200 },
  { customer: "ben", amountCents: 500 },
  { customer: "ana", amountCents: 300 },
];

test("grand total adds every order", () => {
  assert.equal(grandTotal(orders), 2000);
});

test("grand total of no orders is 0", () => {
  assert.equal(grandTotal([]), 0);
});

test("totals are grouped per customer", () => {
  assert.deepEqual(totalsByCustomer(orders), new Map([["ana", 1500], ["ben", 500]]));
});

test("customers appear in order of first appearance", () => {
  const result = totalsByCustomer([
    { customer: "zoe", amountCents: 1 },
    { customer: "adam", amountCents: 2 },
    { customer: "zoe", amountCents: 3 },
  ]);
  assert.deepEqual([...result.keys()], ["zoe", "adam"]);
});

test("no orders gives an empty Map", () => {
  const result = totalsByCustomer([]);
  assert.ok(result instanceof Map);
  assert.equal(result.size, 0);
});

test("customer names are case-sensitive and zero amounts still count", () => {
  const result = totalsByCustomer([
    { customer: "Ana", amountCents: 0 },
    { customer: "ana", amountCents: 100 },
  ]);
  assert.deepEqual(result, new Map([["Ana", 0], ["ana", 100]]));
});

test("does not change the input", () => {
  const input = [
    { customer: "ana", amountCents: 1200 },
    { customer: "ana", amountCents: 300 },
  ];
  grandTotal(input);
  totalsByCustomer(input);
  assert.deepEqual(input, [
    { customer: "ana", amountCents: 1200 },
    { customer: "ana", amountCents: 300 },
  ]);
});
