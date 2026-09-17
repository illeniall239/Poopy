import { test } from "node:test";
import assert from "node:assert/strict";
import { toClock } from "./solution.ts";

test("zero seconds pads every part", () => {
  assert.equal(toClock(0), "00:00:00");
});

test("seconds only", () => {
  assert.equal(toClock(59), "00:00:59");
});

test("exactly one minute", () => {
  assert.equal(toClock(60), "00:01:00");
});

test("one second before an hour", () => {
  assert.equal(toClock(3599), "00:59:59");
});

test("exactly one hour", () => {
  assert.equal(toClock(3600), "01:00:00");
});

test("every part has two different digits", () => {
  assert.equal(toClock(45296), "12:34:56");
});

test("single-digit parts get a leading zero", () => {
  assert.equal(toClock(3725), "01:02:05");
});

test("hours do not wrap at 24", () => {
  assert.equal(toClock(90000), "25:00:00");
});

test("largest allowed value", () => {
  assert.equal(toClock(359999), "99:59:59");
});
