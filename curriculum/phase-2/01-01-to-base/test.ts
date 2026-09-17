import { test } from "node:test";
import assert from "node:assert/strict";
import { toBase, fromBase } from "./solution.ts";

test("ten in binary", () => {
  assert.equal(toBase(10, 2), "1010");
});

test("digits come out most significant first", () => {
  assert.equal(toBase(6, 2), "110");
});

test("letters for digits above 9", () => {
  assert.equal(toBase(255, 16), "ff");
});

test("zero is written as a single digit", () => {
  assert.equal(toBase(0, 7), "0");
});

test("largest 32-bit integer in base 16 and base 2", () => {
  assert.equal(toBase(2147483647, 16), "7fffffff");
  assert.equal(toBase(2147483647, 2), "1".repeat(31));
});

test("fromBase reads binary", () => {
  assert.equal(fromBase("1010", 2), 10);
});

test("fromBase reads zero and letters", () => {
  assert.equal(fromBase("0", 2), 0);
  assert.equal(fromBase("7fffffff", 16), 2147483647);
});

test("round trip in every base", () => {
  for (let base = 2; base <= 16; base++) {
    for (const n of [1, 15, 16, 999, 123456789, 2147483646]) {
      assert.equal(fromBase(toBase(n, base), base), n);
    }
  }
  assert.equal(toBase(123456789, 10), "123456789");
});
