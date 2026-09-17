import { test } from "node:test";
import assert from "node:assert/strict";
import { Autocomplete } from "./solution.ts";

// "w" followed by the five digits of k (zero-padded) written as the letters a..j, so numeric and alphabetical order agree.
function wordFor(k: number): string {
  return "w" + String(k).padStart(5, "0").replace(/\d/g, (d) => String.fromCharCode(97 + Number(d)));
}

test("first n matches in alphabetical order", () => {
  const ac = new Autocomplete(["apple", "app", "application", "apt", "banana"]);
  assert.deepEqual(ac.suggest("app", 2), ["app", "apple"]);
  assert.deepEqual(ac.suggest("app", 10), ["app", "apple", "application"]);
  assert.deepEqual(ac.suggest("ap", 1), ["app"]);
});

test("a word equal to the prefix comes first", () => {
  const ac = new Autocomplete(["card", "cart", "car"]);
  assert.deepEqual(ac.suggest("car", 3), ["car", "card", "cart"]);
});

test("no matches", () => {
  const ac = new Autocomplete(["apple", "banana"]);
  assert.deepEqual(ac.suggest("c", 3), []);
  assert.deepEqual(ac.suggest("apples", 3), []);
  assert.deepEqual(ac.suggest("b", 3), ["banana"]);
});

test("n of zero", () => {
  const ac = new Autocomplete(["apple"]);
  assert.deepEqual(ac.suggest("app", 0), []);
  assert.deepEqual(ac.suggest("", 0), []);
});

test("empty prefix gives the first n words overall", () => {
  const ac = new Autocomplete(["dog", "cat", "bird"]);
  assert.deepEqual(ac.suggest("", 2), ["bird", "cat"]);
  assert.deepEqual(ac.suggest("", 5), ["bird", "cat", "dog"]);
});

test("duplicates are stored once", () => {
  const ac = new Autocomplete(["a", "ab", "a", "ab", "a"]);
  assert.deepEqual(ac.suggest("a", 5), ["a", "ab"]);
});

test("insertion order does not matter and the input is not changed", () => {
  const words = ["band", "bandana", "banana", "ban"];
  const ac = new Autocomplete(words);
  assert.deepEqual(ac.suggest("ban", 3), ["ban", "banana", "band"]);
  assert.deepEqual(words, ["band", "bandana", "banana", "ban"]);
});

test("100000 words and 100000 queries without scanning the list", () => {
  const W = 100000;
  const words: string[] = [];
  for (let i = 0; i < W; i++) words.push(wordFor((i * 7919) % W));
  const ac = new Autocomplete(words);
  const got: string[][] = [];
  const expected: string[][] = [];
  for (let q = 0; q < W; q++) {
    const k = (q * 104729) % W;
    const base = k - (k % 100);
    got.push(ac.suggest(wordFor(k).slice(0, 4), 3));
    expected.push([wordFor(base), wordFor(base + 1), wordFor(base + 2)]);
  }
  assert.deepEqual(got, expected);
});
