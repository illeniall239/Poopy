import { test } from "node:test";
import assert from "node:assert/strict";
import { daysToEscape } from "./solution.ts";

test("does not slide back on the last day", () => {
  assert.equal(daysToEscape(10, 3, 2), 8);
});

test("reaching exactly the top counts as out", () => {
  assert.equal(daysToEscape(5, 3, 1), 2);
});

test("one more metre needs one more day", () => {
  assert.equal(daysToEscape(6, 3, 1), 3);
});

test("out on day 1 when one climb is enough", () => {
  assert.equal(daysToEscape(3, 5, 1), 1);
});

test("never escapes when the slide undoes the climb", () => {
  assert.equal(daysToEscape(10, 2, 2), -1);
});

test("escapes on day 1 even if the slide equals the climb", () => {
  assert.equal(daysToEscape(5, 5, 5), 1);
});

test("never escapes when the slide is bigger than the climb", () => {
  assert.equal(daysToEscape(10, 3, 7), -1);
});

test("no slide at all", () => {
  assert.equal(daysToEscape(10, 3, 0), 4);
});

test("deep well, slow progress", () => {
  assert.equal(daysToEscape(1000000, 2, 1), 999999);
});
