import { test } from "node:test";
import assert from "node:assert/strict";
import { WordDictionary } from "./solution.ts";

// Five lowercase letters encoding x (0 <= x < 26^5), most significant first.
function encode(x: number): string {
  let s = "";
  for (let k = 0; k < 5; k++) {
    s = String.fromCharCode(97 + (x % 26)) + s;
    x = Math.floor(x / 26);
  }
  return s;
}

test("dots match any single letter", () => {
  const dict = new WordDictionary();
  for (const w of ["bad", "dad", "mad"]) dict.addWord(w);
  assert.equal(dict.search("pad"), false);
  assert.equal(dict.search("bad"), true);
  assert.equal(dict.search(".ad"), true);
  assert.equal(dict.search("b.."), true);
});

test("lengths must match", () => {
  const dict = new WordDictionary();
  dict.addWord("cat");
  assert.equal(dict.search("ca"), false);
  assert.equal(dict.search("c."), false);
  assert.equal(dict.search("c.t."), false);
  assert.equal(dict.search("cats"), false);
});

test("empty dictionary", () => {
  const dict = new WordDictionary();
  assert.equal(dict.search("a"), false);
  assert.equal(dict.search("."), false);
});

test("a query of only dots matches any word of that length", () => {
  const dict = new WordDictionary();
  dict.addWord("hello");
  assert.equal(dict.search("....."), true);
  assert.equal(dict.search("...."), false);
  assert.equal(dict.search("......"), false);
});

test("every branch under a dot is tried", () => {
  const dict = new WordDictionary();
  for (const w of ["abc", "abd", "abx"]) dict.addWord(w);
  assert.equal(dict.search("ab."), true);
  assert.equal(dict.search("a.x"), true);
  assert.equal(dict.search("a.y"), false);
  assert.equal(dict.search("b.."), false);
});

test("dots at the start and two dots", () => {
  const dict = new WordDictionary();
  dict.addWord("cab");
  dict.addWord("dab");
  assert.equal(dict.search(".ab"), true);
  assert.equal(dict.search("..b"), true);
  assert.equal(dict.search("..c"), false);
  assert.equal(dict.search(".a."), true);
});

test("a prefix of a stored word is not a match", () => {
  const dict = new WordDictionary();
  dict.addWord("dog");
  dict.addWord("dog");
  dict.addWord("dogs");
  assert.equal(dict.search("do"), false);
  assert.equal(dict.search("d."), false);
  assert.equal(dict.search("dog"), true);
  assert.equal(dict.search("d.g"), true);
  assert.equal(dict.search("do.s"), true);
});

test("50000 words and 150000 searches without scanning the words", () => {
  const W = 50000;
  const dict = new WordDictionary();
  const words = new Set<string>();
  const tailMasked = new Set<string>();
  const headMasked = new Set<string>();
  const list: string[] = [];
  for (let i = 0; i < W; i++) {
    const w = encode((i * 7919) % 1000003);
    list.push(w);
    words.add(w);
    tailMasked.add(w.slice(0, 4));
    headMasked.add(w.slice(1));
    dict.addWord(w);
  }
  const expected: boolean[] = [];
  const got: boolean[] = [];
  for (let q = 0; q < W; q++) {
    const s = q % 2 === 0 ? list[q] : encode((q * 104729) % 1000003);
    expected.push(words.has(s), tailMasked.has(s.slice(0, 4)), headMasked.has(s.slice(1)));
    got.push(dict.search(s), dict.search(s.slice(0, 4) + "."), dict.search("." + s.slice(1)));
  }
  assert.deepEqual(got, expected);
});
