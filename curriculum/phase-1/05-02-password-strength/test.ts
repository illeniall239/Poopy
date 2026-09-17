import { test } from "node:test";
import assert from "node:assert/strict";
import { hasLowercase, hasUppercase, hasDigit, hasSymbol, passwordStrength } from "./solution.ts";

test("hasLowercase and hasUppercase check the right case", () => {
  assert.equal(hasLowercase("ABc"), true);
  assert.equal(hasLowercase("ABC1!"), false);
  assert.equal(hasUppercase("abC"), true);
  assert.equal(hasUppercase("abc1!"), false);
});

test("hasDigit finds a digit anywhere, including 0 and 9", () => {
  assert.equal(hasDigit("abc1"), true);
  assert.equal(hasDigit("0abc"), true);
  assert.equal(hasDigit("ab9c"), true);
  assert.equal(hasDigit("abc"), false);
});

test("hasSymbol counts anything that is not a letter or digit", () => {
  assert.equal(hasSymbol("abc!"), true);
  assert.equal(hasSymbol("a b"), true);
  assert.equal(hasSymbol("aB3"), false);
});

test("helpers return false for an empty string", () => {
  assert.equal(hasLowercase(""), false);
  assert.equal(hasUppercase(""), false);
  assert.equal(hasDigit(""), false);
  assert.equal(hasSymbol(""), false);
});

test("empty password scores 0 and is weak", () => {
  assert.deepEqual(passwordStrength(""), { score: 0, label: "weak" });
});

test("length 8 earns a point, score 2 is still weak", () => {
  assert.deepEqual(passwordStrength("abcdefg"), { score: 1, label: "weak" });
  assert.deepEqual(passwordStrength("abcdefgh"), { score: 2, label: "weak" });
});

test("score 3 and 4 are medium", () => {
  assert.deepEqual(passwordStrength("abcdefgH"), { score: 3, label: "medium" });
  assert.deepEqual(passwordStrength("ABCDEFGHIJK1"), { score: 4, label: "medium" });
});

test("score 5 is strong", () => {
  assert.deepEqual(passwordStrength("Abcdefg1!"), { score: 5, label: "strong" });
});

test("length 12 earns an extra point for a score of 6", () => {
  assert.deepEqual(passwordStrength("Abcdefghij1"), { score: 4, label: "medium" });
  assert.deepEqual(passwordStrength("Abcdefghij1!"), { score: 6, label: "strong" });
});
