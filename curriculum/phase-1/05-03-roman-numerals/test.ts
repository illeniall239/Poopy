import { test } from "node:test";
import assert from "node:assert/strict";
import { toRoman } from "./solution.ts";

test("ones place from 1 to 9", () => {
  assert.equal(toRoman(1), "I");
  assert.equal(toRoman(3), "III");
  assert.equal(toRoman(4), "IV");
  assert.equal(toRoman(5), "V");
  assert.equal(toRoman(8), "VIII");
  assert.equal(toRoman(9), "IX");
});

test("tens and ones together", () => {
  assert.equal(toRoman(14), "XIV");
  assert.equal(toRoman(40), "XL");
  assert.equal(toRoman(90), "XC");
});

test("zero digits in the middle write nothing", () => {
  assert.equal(toRoman(101), "CI");
  assert.equal(toRoman(2006), "MMVI");
});

test("hundreds use C, D and M", () => {
  assert.equal(toRoman(400), "CD");
  assert.equal(toRoman(900), "CM");
  assert.equal(toRoman(500), "D");
});

test("every place at once", () => {
  assert.equal(toRoman(1994), "MCMXCIV");
  assert.equal(toRoman(3888), "MMMDCCCLXXXVIII");
});

test("largest allowed number", () => {
  assert.equal(toRoman(3999), "MMMCMXCIX");
});

test("out of range gives an empty string", () => {
  assert.equal(toRoman(0), "");
  assert.equal(toRoman(-5), "");
  assert.equal(toRoman(4000), "");
});

test("non-whole numbers give an empty string", () => {
  assert.equal(toRoman(2.5), "");
});
