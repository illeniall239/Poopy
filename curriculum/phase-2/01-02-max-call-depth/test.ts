import { test } from "node:test";
import assert from "node:assert/strict";
import { maxCallDepth } from "./solution.ts";

test("entry that calls nothing is one frame", () => {
  assert.equal(maxCallDepth({ main: [] }, "main"), 1);
});

test("a chain of nested calls", () => {
  assert.equal(maxCallDepth({ main: ["parse"], parse: ["readFile"] }, "main"), 3);
});

test("calls made one after another don't stack up", () => {
  assert.equal(maxCallDepth({ main: ["log", "log", "save"], save: [] }, "main"), 2);
});

test("picks the deepest branch", () => {
  assert.equal(maxCallDepth({ main: ["a", "b"], a: [], b: ["c"], c: ["d"] }, "main"), 4);
});

test("a shared helper reached twice is not recursion", () => {
  assert.equal(maxCallDepth({ main: ["a", "b"], a: ["util"], b: ["util"], util: [] }, "main"), 3);
});

test("a function calling itself recurses forever", () => {
  assert.equal(maxCallDepth({ main: ["loop"], loop: ["loop"] }, "main"), -1);
});

test("mutual recursion off the deepest path recurses forever", () => {
  const calls = { main: ["deep", "isEven"], deep: ["x"], x: ["y"], y: ["z"], isEven: ["isOdd"], isOdd: ["isEven"] };
  assert.equal(maxCallDepth(calls, "main"), -1);
});

test("a cycle that entry never reaches doesn't matter", () => {
  assert.equal(maxCallDepth({ main: ["a"], a: [], b: ["c"], c: ["b"] }, "main"), 2);
});

test("300 layers of shared helpers finish quickly", () => {
  const layers = 300;
  const calls: Record<string, string[]> = {};
  for (let i = 0; i < layers; i++) {
    calls[`f${i}`] = [`a${i}`, `b${i}`];
    calls[`a${i}`] = [`f${i + 1}`];
    calls[`b${i}`] = [`f${i + 1}`];
  }
  assert.equal(maxCallDepth(calls, "f0"), 2 * layers + 1);
});
