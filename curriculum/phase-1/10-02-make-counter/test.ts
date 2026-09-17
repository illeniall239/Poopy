import { test } from "node:test";
import assert from "node:assert/strict";
import { makeCounter } from "./solution.ts";

test("starts at 0 and steps by 1 by default", () => {
  const c = makeCounter();
  assert.equal(c.value(), 0);
  assert.equal(c.increment(), 1);
  assert.equal(c.increment(), 2);
  assert.equal(c.decrement(), 1);
  assert.equal(c.value(), 1);
});

test("uses a custom start and step", () => {
  const c = makeCounter(100, 10);
  assert.equal(c.increment(), 110);
  assert.equal(c.decrement(), 100);
  assert.equal(c.decrement(), 90);
});

test("reset goes back to the start, not to 0", () => {
  const c = makeCounter(5);
  c.increment();
  c.increment();
  assert.equal(c.reset(), 5);
  assert.equal(c.value(), 5);
});

test("value does not change the count", () => {
  const c = makeCounter(3);
  c.value();
  c.value();
  assert.equal(c.increment(), 4);
});

test("counters are independent", () => {
  const a = makeCounter();
  const b = makeCounter();
  a.increment();
  a.increment();
  assert.equal(b.increment(), 1);
  assert.equal(a.value(), 2);
});

test("functions still work when taken off the object", () => {
  const c = makeCounter();
  const inc = c.increment;
  const read = c.value;
  inc();
  inc();
  assert.equal(read(), 2);
});

test("the count is private", () => {
  const c = makeCounter();
  assert.deepEqual(Object.keys(c).sort(), ["decrement", "increment", "reset", "value"]);
});
