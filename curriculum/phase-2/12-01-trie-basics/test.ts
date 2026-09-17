import { test } from "node:test";
import assert from "node:assert/strict";
import { Trie } from "./solution.ts";

// Five lowercase letters encoding x (0 <= x < 26^5), most significant first.
function encode(x: number): string {
  let s = "";
  for (let k = 0; k < 5; k++) {
    s = String.fromCharCode(97 + (x % 26)) + s;
    x = Math.floor(x / 26);
  }
  return s;
}

test("whole word versus its beginning", () => {
  const trie = new Trie();
  trie.insert("apple");
  assert.equal(trie.search("apple"), true);
  assert.equal(trie.search("app"), false);
  assert.equal(trie.startsWith("app"), true);
});

test("a prefix becomes a word once inserted", () => {
  const trie = new Trie();
  trie.insert("apple");
  trie.insert("app");
  assert.equal(trie.search("app"), true);
  assert.equal(trie.search("apple"), true);
});

test("empty trie answers false", () => {
  const trie = new Trie();
  assert.equal(trie.search("a"), false);
  assert.equal(trie.startsWith("a"), false);
});

test("words sharing a beginning", () => {
  const trie = new Trie();
  for (const w of ["car", "cart", "cat"]) trie.insert(w);
  assert.equal(trie.search("car"), true);
  assert.equal(trie.search("cart"), true);
  assert.equal(trie.search("cat"), true);
  assert.equal(trie.search("ca"), false);
  assert.equal(trie.startsWith("ca"), true);
  assert.equal(trie.startsWith("cab"), false);
  assert.equal(trie.startsWith("cart"), true);
});

test("inserting the same word twice changes nothing", () => {
  const trie = new Trie();
  trie.insert("dog");
  trie.insert("dog");
  assert.equal(trie.search("dog"), true);
  assert.equal(trie.search("do"), false);
  assert.equal(trie.startsWith("dog"), true);
});

test("query longer than any stored word", () => {
  const trie = new Trie();
  trie.insert("cat");
  assert.equal(trie.search("cats"), false);
  assert.equal(trie.startsWith("cats"), false);
});

test("different first letters", () => {
  const trie = new Trie();
  for (const w of ["dog", "dot", "cat"]) trie.insert(w);
  assert.equal(trie.startsWith("d"), true);
  assert.equal(trie.startsWith("c"), true);
  assert.equal(trie.startsWith("e"), false);
  assert.equal(trie.search("d"), false);
});

test("50000 words and 100000 queries in O(L) each", () => {
  const W = 50000;
  const trie = new Trie();
  const words = new Set<string>();
  const prefixes = new Set<string>();
  const list: string[] = [];
  for (let i = 0; i < W; i++) {
    const w = encode((i * 7919) % 1000003);
    list.push(w);
    words.add(w);
    prefixes.add(w.slice(0, 4));
    trie.insert(w);
  }
  const expected: boolean[] = [];
  const got: boolean[] = [];
  for (let q = 0; q < W; q++) {
    const s = q % 2 === 0 ? list[q] : encode((q * 104729) % 1000003);
    expected.push(words.has(s), prefixes.has(s.slice(0, 4)));
    got.push(trie.search(s), trie.startsWith(s.slice(0, 4)));
  }
  assert.deepEqual(got, expected);
});
