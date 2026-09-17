import { test } from "node:test";
import assert from "node:assert/strict";
import { sortBySeveralKeys } from "./solution.ts";

function player(id: number, name: string, score: number) {
  return { id, name, score };
}

function idsOf(players: { id: number }[]): number[] {
  return players.map((p) => p.id);
}

test("score descending, then name ascending", () => {
  const players = [player(1, "cara", 50), player(2, "alex", 80), player(3, "bea", 50)];
  assert.deepEqual(idsOf(sortBySeveralKeys(players)), [2, 3, 1]);
});

test("names only matter within equal scores", () => {
  const players = [player(1, "zed", 90), player(2, "amy", 70), player(3, "bob", 90), player(4, "cat", 70)];
  assert.deepEqual(idsOf(sortBySeveralKeys(players)), [3, 1, 2, 4]);
});

test("fully equal keys keep their input order", () => {
  const players = [player(1, "sam", 10), player(2, "sam", 10), player(3, "sam", 10)];
  assert.deepEqual(idsOf(sortBySeveralKeys(players)), [1, 2, 3]);
  const mixed = [player(5, "kim", 10), player(6, "kim", 20), player(7, "kim", 10)];
  assert.deepEqual(idsOf(sortBySeveralKeys(mixed)), [6, 5, 7]);
});

test("names compare by character code, upper case first", () => {
  const players = [player(1, "alice", 5), player(2, "Bob", 5), player(3, "aaron", 5)];
  assert.deepEqual(idsOf(sortBySeveralKeys(players)), [2, 3, 1]);
});

test("negative and large scores", () => {
  const players = [player(1, "a", -1000000000), player(2, "b", 1000000000), player(3, "c", 0)];
  assert.deepEqual(idsOf(sortBySeveralKeys(players)), [2, 3, 1]);
});

test("empty and single-element arrays", () => {
  assert.deepEqual(sortBySeveralKeys([]), []);
  assert.deepEqual(idsOf(sortBySeveralKeys([player(9, "solo", 1)])), [9]);
});

test("returns the same objects in a new array and leaves the input untouched", () => {
  const players = [player(1, "b", 1), player(2, "a", 2)];
  const result = sortBySeveralKeys(players);
  assert.notEqual(result, players);
  assert.equal(result[0], players[1]);
  assert.equal(result[1], players[0]);
  assert.deepEqual(idsOf(players), [1, 2]);
});

test("200000 records in O(n log n)", () => {
  const n = 200000;
  const players = Array.from({ length: n }, (_, i) => player(i, "p" + ((i * 7919) % 1000), (i * 104729) % 500));
  const result = sortBySeveralKeys(players);
  assert.equal(result.length, n);
  assert.equal(new Set(idsOf(result)).size, n);
  for (let i = 1; i < n; i++) {
    const a = result[i - 1];
    const b = result[i];
    const ordered = a.score > b.score || (a.score === b.score && (a.name < b.name || (a.name === b.name && a.id < b.id)));
    assert.ok(ordered, `records ${i - 1} and ${i} are out of order`);
  }
});
