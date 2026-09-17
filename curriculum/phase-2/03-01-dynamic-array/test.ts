import { test } from "node:test";
import assert from "node:assert/strict";
import { DynamicArray } from "./solution.ts";

test("starts empty with capacity 1", () => {
  const a = new DynamicArray<number>();
  assert.equal(a.size(), 0);
  assert.equal(a.capacity(), 1);
  assert.deepEqual(a.toArray(), []);
});

test("push then get keeps order", () => {
  const a = new DynamicArray<string>();
  a.push("x");
  a.push("y");
  a.push("z");
  assert.equal(a.size(), 3);
  assert.deepEqual([a.get(0), a.get(1), a.get(2)], ["x", "y", "z"]);
});

test("capacity doubles only when full", () => {
  const a = new DynamicArray<number>();
  const capacities: number[] = [];
  for (let i = 0; i < 5; i++) {
    a.push(i);
    capacities.push(a.capacity());
  }
  assert.deepEqual(capacities, [1, 2, 4, 4, 8]);
});

test("get and set throw RangeError outside 0..size-1, even below capacity", () => {
  const a = new DynamicArray<number>();
  a.push(1);
  a.push(2);
  a.push(3);
  assert.equal(a.capacity(), 4);
  assert.throws(() => a.get(3), RangeError);
  assert.throws(() => a.get(-1), RangeError);
  assert.throws(() => a.set(3, 9), RangeError);
});

test("set replaces a value without changing the size", () => {
  const a = new DynamicArray<number>();
  a.push(1);
  a.push(2);
  a.set(0, 7);
  assert.deepEqual(a.toArray(), [7, 2]);
  assert.equal(a.size(), 2);
});

test("pop returns the last element and never shrinks capacity", () => {
  const a = new DynamicArray<number>();
  for (const v of [1, 2, 3]) a.push(v);
  assert.equal(a.pop(), 3);
  assert.equal(a.pop(), 2);
  assert.equal(a.size(), 1);
  assert.equal(a.capacity(), 4);
  assert.throws(() => a.get(1), RangeError);
  assert.equal(a.pop(), 1);
  assert.throws(() => a.pop(), RangeError);
});

test("toArray returns a copy that can't break the structure", () => {
  const a = new DynamicArray<number>();
  a.push(1);
  a.push(2);
  a.push(3);
  const copy = a.toArray();
  assert.equal(copy.length, 3);
  copy[0] = 99;
  copy.push(100);
  assert.deepEqual(a.toArray(), [1, 2, 3]);
  assert.equal(a.size(), 3);
});

test("1000000 pushes with amortized O(1) push", () => {
  const a = new DynamicArray<number>();
  const n = 1000000;
  for (let i = 0; i < n; i++) a.push(i);
  assert.equal(a.size(), n);
  assert.equal(a.capacity(), 1048576);
  assert.equal(a.get(n - 1), n - 1);
  assert.equal(a.get(123456), 123456);
});
