import { test } from "node:test";
import assert from "node:assert/strict";
import { celsiusToFahrenheit, fahrenheitToCelsius } from "./solution.ts";

test("boiling point to Fahrenheit", () => {
  assert.equal(celsiusToFahrenheit(100), 212);
});

test("freezing point to Fahrenheit", () => {
  assert.equal(celsiusToFahrenheit(0), 32);
});

test("body temperature to Fahrenheit", () => {
  assert.equal(celsiusToFahrenheit(37), 98.6);
});

test("floating-point noise is rounded to one decimal place", () => {
  assert.equal(celsiusToFahrenheit(36.6), 97.9);
});

test("-40 is the same on both scales", () => {
  assert.equal(celsiusToFahrenheit(-40), -40);
  assert.equal(fahrenheitToCelsius(-40), -40);
});

test("subtracts 32 before multiplying", () => {
  assert.equal(fahrenheitToCelsius(212), 100);
});

test("body temperature to Celsius", () => {
  assert.equal(fahrenheitToCelsius(98.6), 37);
});

test("negative result rounds to one decimal place", () => {
  assert.equal(fahrenheitToCelsius(0), -17.8);
});

test("returns a number, not a string", () => {
  assert.equal(typeof fahrenheitToCelsius(50), "number");
  assert.equal(fahrenheitToCelsius(50), 10);
});
