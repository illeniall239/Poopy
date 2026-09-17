import { test } from "node:test";
import assert from "node:assert/strict";
import { safeDivide, sumOfQuotients } from "./solution.ts";

test("divides normally", () => {
  assert.deepEqual(safeDivide(10, 4), { ok: true, value: 2.5 });
  assert.deepEqual(safeDivide(0, 5), { ok: true, value: 0 });
  assert.deepEqual(safeDivide(-9, 3), { ok: true, value: -3 });
});

test("dividing by zero is a failure, not Infinity", () => {
  assert.deepEqual(safeDivide(1, 0), { ok: false, error: "Cannot divide by zero" });
  assert.deepEqual(safeDivide(0, 0), { ok: false, error: "Cannot divide by zero" });
});

test("non-finite inputs are a failure", () => {
  assert.deepEqual(safeDivide(NaN, 2), { ok: false, error: "Inputs must be finite numbers" });
  assert.deepEqual(safeDivide(1, Infinity), { ok: false, error: "Inputs must be finite numbers" });
  assert.deepEqual(safeDivide(-Infinity, 1), { ok: false, error: "Inputs must be finite numbers" });
});

test("the finite check comes before the zero check", () => {
  assert.deepEqual(safeDivide(NaN, 0), { ok: false, error: "Inputs must be finite numbers" });
});

test("sums the quotients of all pairs", () => {
  assert.deepEqual(sumOfQuotients([{ a: 10, b: 2 }, { a: 9, b: 3 }]), { ok: true, value: 8 });
});

test("no pairs sums to 0", () => {
  assert.deepEqual(sumOfQuotients([]), { ok: true, value: 0 });
});

test("reports the first failing pair with its position", () => {
  assert.deepEqual(
    sumOfQuotients([{ a: 1, b: 1 }, { a: 5, b: 0 }, { a: NaN, b: 1 }]),
    { ok: false, error: "Pair 2: Cannot divide by zero" },
  );
  assert.deepEqual(
    sumOfQuotients([{ a: Infinity, b: 1 }]),
    { ok: false, error: "Pair 1: Inputs must be finite numbers" },
  );
});
