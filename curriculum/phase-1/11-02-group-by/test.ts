import { test } from "node:test";
import assert from "node:assert/strict";
import { groupBy } from "./solution.ts";

test("groups numbers by parity", () => {
  assert.deepEqual(
    groupBy([1, 2, 3, 4, 5], (n) => (n % 2 === 0 ? "even" : "odd")),
    { odd: [1, 3, 5], even: [2, 4] },
  );
});

test("groups objects and keeps input order within each group", () => {
  const people = [
    { name: "Ana", team: "red" },
    { name: "Bo", team: "blue" },
    { name: "Cy", team: "red" },
  ];
  assert.deepEqual(groupBy(people, (p) => p.team), {
    red: [{ name: "Ana", team: "red" }, { name: "Cy", team: "red" }],
    blue: [{ name: "Bo", team: "blue" }],
  });
});

test("groups hold the original objects, not copies", () => {
  const ana = { name: "Ana", team: "red" };
  const result = groupBy([ana], (p) => p.team);
  assert.equal(result.red[0], ana);
});

test("empty input gives an empty object", () => {
  assert.deepEqual(groupBy([], (s: string) => s), {});
});

test("every item in one group", () => {
  assert.deepEqual(groupBy(["x", "y"], () => "all"), { all: ["x", "y"] });
});

test("keyOf is called once per item", () => {
  let calls = 0;
  groupBy([1, 2, 3], (n) => {
    calls++;
    return String(n);
  });
  assert.equal(calls, 3);
});

test("does not change the input", () => {
  const items = [3, 1, 2];
  groupBy(items, (n) => String(n % 2));
  assert.deepEqual(items, [3, 1, 2]);
});
