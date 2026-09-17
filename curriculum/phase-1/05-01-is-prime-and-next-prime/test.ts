import { test } from "node:test";
import assert from "node:assert/strict";
import { isPrime, nextPrime } from "./solution.ts";

test("small primes", () => {
  assert.equal(isPrime(2), true);
  assert.equal(isPrime(3), true);
  assert.equal(isPrime(7), true);
});

test("numbers below 2 are not prime", () => {
  assert.equal(isPrime(1), false);
  assert.equal(isPrime(0), false);
  assert.equal(isPrime(-7), false);
});

test("even numbers above 2 are not prime", () => {
  assert.equal(isPrime(4), false);
  assert.equal(isPrime(100), false);
});

test("squares of primes are not prime", () => {
  assert.equal(isPrime(9), false);
  assert.equal(isPrime(25), false);
  assert.equal(isPrime(49), false);
});

test("larger primes", () => {
  assert.equal(isPrime(97), true);
  assert.equal(isPrime(7919), true);
  assert.equal(isPrime(1000003), true);
});

test("next prime is strictly greater", () => {
  assert.equal(nextPrime(13), 17);
  assert.equal(nextPrime(2), 3);
  assert.equal(nextPrime(14), 17);
});

test("next prime from zero, one and negatives is 2", () => {
  assert.equal(nextPrime(0), 2);
  assert.equal(nextPrime(1), 2);
  assert.equal(nextPrime(-10), 2);
});

test("next prime for a large number", () => {
  assert.equal(nextPrime(1000000), 1000003);
});
