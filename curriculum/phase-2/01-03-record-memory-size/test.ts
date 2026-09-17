import { test } from "node:test";
import assert from "node:assert/strict";
import { recordSize, arraySize } from "./solution.ts";

test("padding before a larger field", () => {
  assert.equal(recordSize(["i8", "i32"]), 8);
});

test("padding at the end rounds to the largest field", () => {
  assert.equal(recordSize(["i32", "i8"]), 8);
  assert.equal(recordSize(["bool", "i16"]), 4);
});

test("field order changes the size", () => {
  assert.equal(recordSize(["i8", "i64", "i8"]), 24);
  assert.equal(recordSize(["i64", "i8", "i8"]), 16);
});

test("one-byte fields need no padding", () => {
  assert.equal(recordSize(["i8", "bool", "i8"]), 3);
});

test("empty record has size 0", () => {
  assert.equal(recordSize([]), 0);
});

test("mixed field types", () => {
  assert.equal(recordSize(["ptr", "f32", "f64", "i16"]), 32);
  assert.equal(recordSize(["i16", "i8", "i32", "i8"]), 12);
});

test("array of records includes each record's padding", () => {
  assert.equal(arraySize(["i32", "i8"], 1000), 8000);
  assert.equal(arraySize(["i8", "i16", "i8"], 3), 18);
});

test("empty arrays and empty records use no bytes", () => {
  assert.equal(arraySize(["i64"], 0), 0);
  assert.equal(arraySize([], 5), 0);
  assert.equal(arraySize(["f64", "i8"], 10000000), 160000000);
});
