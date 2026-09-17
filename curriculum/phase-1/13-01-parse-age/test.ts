import { test } from "node:test";
import assert from "node:assert/strict";
import { parseAge } from "./solution.ts";

test("parses a plain age", () => {
  assert.equal(parseAge("42"), 42);
});

test("ignores surrounding spaces and leading zeros", () => {
  assert.equal(parseAge("  7 "), 7);
  assert.equal(parseAge("007"), 7);
});

test("accepts the boundaries 0 and 150", () => {
  assert.equal(parseAge("0"), 0);
  assert.equal(parseAge("150"), 150);
});

test("empty or blank input is reported as empty, not as 0", () => {
  assert.throws(() => parseAge(""), { name: "Error", message: "Age is empty" });
  assert.throws(() => parseAge("   "), { name: "Error", message: "Age is empty" });
});

test("non-digits are rejected with the original input in the message", () => {
  assert.throws(() => parseAge("12.5"), { name: "Error", message: 'Age must be a whole number, got "12.5"' });
  assert.throws(() => parseAge("abc"), { name: "Error", message: 'Age must be a whole number, got "abc"' });
  assert.throws(() => parseAge(" -5"), { name: "Error", message: 'Age must be a whole number, got " -5"' });
});

test("inputs that Number or parseInt would accept are still rejected", () => {
  assert.throws(() => parseAge("1e2"), { message: 'Age must be a whole number, got "1e2"' });
  assert.throws(() => parseAge("12abc"), { message: 'Age must be a whole number, got "12abc"' });
  assert.throws(() => parseAge("4 2"), { message: 'Age must be a whole number, got "4 2"' });
});

test("too old is a RangeError", () => {
  assert.throws(() => parseAge("151"), { name: "RangeError", message: "Age must be between 0 and 150, got 151" });
  assert.throws(() => parseAge(" 0200"), { name: "RangeError", message: "Age must be between 0 and 150, got 200" });
});
