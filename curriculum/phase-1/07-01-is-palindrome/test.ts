import { test } from "node:test";
import assert from "node:assert/strict";
import { isPalindrome } from "./solution.ts";

test("simple lowercase palindrome", () => {
  assert.equal(isPalindrome("racecar"), true);
});

test("sentence with spaces and punctuation", () => {
  assert.equal(isPalindrome("A man, a plan, a canal: Panama!"), true);
});

test("not a palindrome", () => {
  assert.equal(isPalindrome("hello"), false);
});

test("case is ignored", () => {
  assert.equal(isPalindrome("Aa"), true);
  assert.equal(isPalindrome("No 'x' in Nixon"), true);
});

test("digits are ignored", () => {
  assert.equal(isPalindrome("Ab1a"), true);
  assert.equal(isPalindrome("a12b"), false);
});

test("empty string and no letters are palindromes", () => {
  assert.equal(isPalindrome(""), true);
  assert.equal(isPalindrome("?! 42"), true);
});

test("almost a palindrome fails in the middle", () => {
  assert.equal(isPalindrome("abcxba"), false);
});

test("even and odd lengths", () => {
  assert.equal(isPalindrome("abba"), true);
  assert.equal(isPalindrome("abcba"), true);
  assert.equal(isPalindrome("ab"), false);
});
