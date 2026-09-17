import { test } from "node:test";
import assert from "node:assert/strict";
import { area } from "./solution.ts";

test("unit circle", () => {
  assert.equal(area({ kind: "circle", radius: 1 }), Math.PI);
});

test("circle area grows with the square of the radius", () => {
  assert.equal(area({ kind: "circle", radius: 2 }), 4 * Math.PI);
  assert.equal(area({ kind: "circle", radius: 0.5 }), Math.PI / 4);
});

test("rectangle", () => {
  assert.equal(area({ kind: "rectangle", width: 3, height: 4 }), 12);
});

test("triangle is half of base times height", () => {
  assert.equal(area({ kind: "triangle", base: 5, height: 3 }), 7.5);
});

test("rectangle and triangle with the same numbers differ", () => {
  assert.equal(area({ kind: "rectangle", width: 4, height: 5 }), 20);
  assert.equal(area({ kind: "triangle", base: 4, height: 5 }), 10);
});

test("zero-sized shapes have zero area", () => {
  assert.equal(area({ kind: "circle", radius: 0 }), 0);
  assert.equal(area({ kind: "rectangle", width: 0, height: 9 }), 0);
  assert.equal(area({ kind: "triangle", base: 7, height: 0 }), 0);
});
