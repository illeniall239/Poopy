import { test } from "node:test";
import assert from "node:assert/strict";
import { binaryToDecimal } from "./solution.ts";

test("zero", () => {
  assert.equal(binaryToDecimal("0"), 0);
  assert.equal(binaryToDecimal("0000"), 0);
});

test("leading zeros are allowed", () => {
  assert.equal(binaryToDecimal("0110"), 6);
});

test("one", () => {
  assert.equal(binaryToDecimal("1"), 1);
});

test("leftmost 1 is counted", () => {
  assert.equal(binaryToDecimal("10"), 2);
  assert.equal(binaryToDecimal("1011"), 11);
});

test("all ones", () => {
  assert.equal(binaryToDecimal("11111111"), 255);
  assert.equal(binaryToDecimal("1".repeat(32)), 4294967295);
});

test("empty string is rejected", () => {
  assert.throws(() => binaryToDecimal(""), { message: "Binary string is empty" });
});

test("non-binary characters are rejected", () => {
  assert.throws(() => binaryToDecimal("102"), { message: 'Not a binary string: "102"' });
  assert.throws(() => binaryToDecimal(" 1"), { message: 'Not a binary string: " 1"' });
});
