import { test } from "node:test";
import assert from "node:assert/strict";
import { LRUCache } from "./solution.ts";

test("evicts the least recently used entry when full", () => {
  const cache = new LRUCache(2);
  cache.put(1, 100);
  cache.put(2, 200);
  const got1 = cache.get(1);
  cache.put(3, 300);
  assert.deepEqual([got1, cache.get(2), cache.get(1), cache.get(3)], [100, -1, 100, 300]);
});

test("missing key returns -1", () => {
  const cache = new LRUCache(3);
  assert.equal(cache.get(42), -1);
  cache.put(1, 5);
  assert.equal(cache.get(2), -1);
});

test("put on an existing key updates the value without evicting", () => {
  const cache = new LRUCache(2);
  cache.put(1, 100);
  cache.put(2, 200);
  cache.put(1, 111);
  assert.deepEqual([cache.get(1), cache.get(2)], [111, 200]);
});

test("put on an existing key counts as a use", () => {
  const cache = new LRUCache(2);
  cache.put(1, 100);
  cache.put(2, 200);
  cache.put(1, 111);
  cache.put(3, 300);
  assert.deepEqual([cache.get(2), cache.get(1), cache.get(3)], [-1, 111, 300]);
});

test("get counts as a use, but a missing get does not", () => {
  const cache = new LRUCache(2);
  cache.put(1, 100);
  cache.put(2, 200);
  cache.get(1);
  cache.get(9);
  cache.put(3, 300);
  assert.deepEqual([cache.get(2), cache.get(1), cache.get(3)], [-1, 100, 300]);
});

test("capacity 1 keeps only the latest entry", () => {
  const cache = new LRUCache(1);
  cache.put(1, 100);
  cache.put(2, 200);
  assert.deepEqual([cache.get(1), cache.get(2)], [-1, 200]);
});

test("0 is a stored value, not a missing one", () => {
  const cache = new LRUCache(2);
  cache.put(0, 0);
  cache.put(7, 0);
  assert.deepEqual([cache.get(0), cache.get(7)], [0, 0]);
});

test("longer sequence of mixed calls", () => {
  const cache = new LRUCache(3);
  cache.put(1, 1);
  cache.put(2, 2);
  cache.put(3, 3);
  cache.get(1);
  cache.put(4, 4);
  cache.get(3);
  cache.put(5, 5);
  cache.put(1, 10);
  cache.put(6, 6);
  assert.deepEqual([1, 2, 3, 4, 5, 6].map((k) => cache.get(k)), [10, -1, -1, -1, 5, 6]);
});

test("100000 entries and 600000 calls in O(1) each", () => {
  const cap = 100000;
  const cache = new LRUCache(cap);
  for (let k = 0; k < cap; k++) cache.put(k, 2 * k);
  let wrong = 0;
  for (let i = 0; i < 500000; i++) {
    const k = (i * 7919) % cap;
    if (cache.get(k) !== 2 * k) wrong++;
  }
  // The last get touched key (499999 * 7919) % cap, so it is the most recently used.
  const newest = (499999 * 7919) % cap;
  for (let k = cap; k < 2 * cap - 1; k++) cache.put(k, 2 * k);
  if (cache.get(newest) !== 2 * newest) wrong++;
  for (let k = 0; k < cap; k += 997) if (k !== newest && cache.get(k) !== -1) wrong++;
  for (let k = cap; k < 2 * cap - 1; k += 991) if (cache.get(k) !== 2 * k) wrong++;
  assert.equal(wrong, 0);
});
