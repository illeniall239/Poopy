import { test } from "node:test";
import assert from "node:assert/strict";
import { triangleKind } from "./solution.ts";

test("all sides equal is equilateral, not isosceles", () => {
  assert.equal(triangleKind(3, 3, 3), "equilateral");
});

test("two equal sides in any position is isosceles", () => {
  assert.equal(triangleKind(3, 3, 5), "isosceles");
  assert.equal(triangleKind(5, 3, 3), "isosceles");
  assert.equal(triangleKind(3, 5, 3), "isosceles");
});

test("no equal sides is scalene", () => {
  assert.equal(triangleKind(3, 4, 5), "scalene");
  assert.equal(triangleKind(5, 3, 4), "scalene");
});

test("flat triangle is invalid", () => {
  assert.equal(triangleKind(1, 2, 3), "invalid");
  assert.equal(triangleKind(3, 1, 2), "invalid");
});

test("two equal sides that are too short is invalid, not isosceles", () => {
  assert.equal(triangleKind(1, 1, 5), "invalid");
  assert.equal(triangleKind(5, 1, 1), "invalid");
});

test("all sides zero is invalid, not equilateral", () => {
  assert.equal(triangleKind(0, 0, 0), "invalid");
});

test("negative sides are invalid", () => {
  assert.equal(triangleKind(-3, 4, 5), "invalid");
  assert.equal(triangleKind(-2, -2, -2), "invalid");
});

test("just valid when two sides add up to one more than the third", () => {
  assert.equal(triangleKind(2, 3, 4), "scalene");
  assert.equal(triangleKind(1, 1, 1), "equilateral");
});
