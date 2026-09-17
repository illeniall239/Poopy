import { test } from "node:test";
import assert from "node:assert/strict";
import { StringHashMap } from "./solution.ts";

test("set and get, missing keys give undefined", () => {
  const m = new StringHashMap<number>();
  m.set("apple", 1);
  m.set("pear", 2);
  assert.equal(m.get("apple"), 1);
  assert.equal(m.get("pear"), 2);
  assert.equal(m.get("plum"), undefined);
  assert.equal(m.size(), 2);
  assert.equal(m.bucketCount(), 8);
});

test("setting an existing key replaces the value, not the size", () => {
  const m = new StringHashMap<string>();
  m.set("k", "old");
  m.set("k", "new");
  assert.equal(m.get("k"), "new");
  assert.equal(m.size(), 1);
});

test("keys with the same characters and the empty key are all distinct", () => {
  const m = new StringHashMap<number>();
  m.set("ab", 1);
  m.set("ba", 2);
  m.set("listen", 3);
  m.set("silent", 4);
  m.set("", 5);
  assert.deepEqual([m.get("ab"), m.get("ba"), m.get("listen"), m.get("silent"), m.get("")], [1, 2, 3, 4, 5]);
  assert.equal(m.size(), 5);
});

test("has is true for stored falsy values", () => {
  const m = new StringHashMap<number | undefined>();
  m.set("zero", 0);
  m.set("nothing", undefined);
  assert.equal(m.has("zero"), true);
  assert.equal(m.has("nothing"), true);
  assert.equal(m.has("other"), false);
  assert.equal(m.get("zero"), 0);
});

test("delete removes only that key and reports whether it was there", () => {
  const m = new StringHashMap<number>();
  m.set("ab", 1);
  m.set("ba", 2);
  assert.equal(m.delete("ab"), true);
  assert.equal(m.delete("ab"), false);
  assert.equal(m.delete("never"), false);
  assert.equal(m.get("ab"), undefined);
  assert.equal(m.has("ab"), false);
  assert.equal(m.get("ba"), 2);
  assert.equal(m.size(), 1);
  m.set("ab", 7);
  assert.equal(m.size(), 2);
});

test("doubles the buckets only when the load factor passes 0.75", () => {
  const m = new StringHashMap<number>();
  const counts: number[] = [];
  for (let i = 1; i <= 13; i++) {
    m.set(`k${i}`, i);
    m.set(`k${i}`, i + 100);
    counts.push(m.bucketCount());
  }
  assert.deepEqual(counts, [8, 8, 8, 8, 8, 8, 16, 16, 16, 16, 16, 16, 32]);
});

test("every entry survives resizing", () => {
  const m = new StringHashMap<number>();
  for (let i = 0; i < 100; i++) m.set(`item-${i}`, i * i);
  const wrong: string[] = [];
  for (let i = 0; i < 100; i++) if (m.get(`item-${i}`) !== i * i) wrong.push(`item-${i}`);
  assert.deepEqual(wrong, []);
  assert.equal(m.size(), 100);
  assert.equal(m.bucketCount(), 256);
});

test("200000 keys with O(1) average operations", () => {
  const m = new StringHashMap<number>();
  const n = 200000;
  for (let i = 0; i < n; i++) m.set(`key${i}`, i);
  let wrong = 0;
  for (let i = 0; i < n; i++) if (m.get(`key${i}`) !== i) wrong++;
  assert.equal(wrong, 0);
  assert.equal(m.size(), n);
  assert.equal(m.bucketCount(), 524288);
});
