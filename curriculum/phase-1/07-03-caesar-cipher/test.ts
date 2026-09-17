import { test } from "node:test";
import assert from "node:assert/strict";
import { caesarShift } from "./solution.ts";

test("shift by one", () => {
  assert.equal(caesarShift("abc", 1), "bcd");
});

test("wraps past z", () => {
  assert.equal(caesarShift("xyz", 3), "abc");
});

test("keeps case and non-letters", () => {
  assert.equal(caesarShift("Hello, World!", 5), "Mjqqt, Btwqi!");
});

test("uppercase wraps within uppercase", () => {
  assert.equal(caesarShift("XYZ", 2), "ZAB");
});

test("negative shift wraps backwards", () => {
  assert.equal(caesarShift("bcd", -1), "abc");
  assert.equal(caesarShift("aB", -1), "zA");
});

test("shifts larger than 26", () => {
  assert.equal(caesarShift("abc", 27), "bcd");
  assert.equal(caesarShift("abc", 26), "abc");
  assert.equal(caesarShift("a", -27), "z");
  assert.equal(caesarShift("Hi", 1000000), caesarShift("Hi", 1000000 % 26));
});

test("digits and spaces unchanged, empty string stays empty", () => {
  assert.equal(caesarShift("route 66", 1), "spvuf 66");
  assert.equal(caesarShift("", 5), "");
});

test("shifting back undoes the shift", () => {
  const secret = caesarShift("Meet at 9pm, Zoe!", 11);
  assert.equal(caesarShift(secret, -11), "Meet at 9pm, Zoe!");
});
