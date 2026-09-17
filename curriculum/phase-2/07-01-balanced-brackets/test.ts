import { test } from "node:test";
import assert from "node:assert/strict";
import { isBalanced } from "./solution.ts";

test("pairs side by side", () => {
  assert.equal(isBalanced("()[]{}"), true);
});

test("pairs nested inside each other", () => {
  assert.equal(isBalanced("{[()]}"), true);
});

test("wrong kind of closing bracket", () => {
  assert.equal(isBalanced("(]"), false);
});

test("pairs that cross instead of nesting", () => {
  assert.equal(isBalanced("([)]"), false);
});

test("opening brackets never closed", () => {
  assert.equal(isBalanced("(("), false);
});

test("closing bracket with nothing open", () => {
  assert.equal(isBalanced("())"), false);
  assert.equal(isBalanced(")"), false);
});

test("other characters are ignored", () => {
  assert.equal(isBalanced("f(a[0]) { x; }"), true);
  assert.equal(isBalanced("abc"), true);
});

test("empty string is balanced", () => {
  assert.equal(isBalanced(""), true);
});

test("200000 levels deep in O(n)", () => {
  const n = 200000;
  const deep = "([{".repeat(n / 2).slice(0, n);
  const closers: Record<string, string> = { "(": ")", "[": "]", "{": "}" };
  const close = [...deep].reverse().map((c) => closers[c]).join("");
  assert.equal(isBalanced(deep + close), true);
  assert.equal(isBalanced(deep + close.slice(1)), false);
});
