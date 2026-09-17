import { test } from "node:test";
import assert from "node:assert/strict";
import { countIslands } from "./solution.ts";

test("three islands", () => {
  assert.equal(countIslands(["11000", "11000", "00100", "00011"]), 3);
});

test("empty grid", () => {
  assert.equal(countIslands([]), 0);
});

test("all water", () => {
  assert.equal(countIslands(["000", "000"]), 0);
});

test("diagonal cells are not connected", () => {
  assert.equal(countIslands(["101", "010", "101"]), 5);
});

test("an island that winds around water", () => {
  assert.equal(countIslands(["10111", "10101", "11101"]), 1);
});

test("single row", () => {
  assert.equal(countIslands(["1011011"]), 3);
});

test("25x25 all land is one island", () => {
  assert.equal(countIslands(Array.from({ length: 25 }, () => "1".repeat(25))), 1);
});

test("1000x1000 grid in O(rows x columns)", () => {
  const grid = Array.from({ length: 1000 }, (_, r) =>
    Array.from({ length: 1000 }, (_, c) => (r % 2 === 0 && c % 2 === 0 ? "1" : "0")).join(""),
  );
  assert.equal(countIslands(grid), 250000);
});
