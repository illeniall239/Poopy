import { test } from "node:test";
import assert from "node:assert/strict";
import { courseOrder } from "./solution.ts";

// A valid order has every course exactly once and each required course before the course needing it.
function assertValidOrder(numCourses: number, prerequisites: [number, number][], order: number[]): void {
  assert.equal(order.length, numCourses, "order must contain every course");
  const position = new Array<number>(numCourses).fill(-1);
  order.forEach((course, i) => {
    assert.ok(Number.isInteger(course) && course >= 0 && course < numCourses, `not a course: ${course}`);
    assert.equal(position[course], -1, `course ${course} appears twice`);
    position[course] = i;
  });
  for (const [course, required] of prerequisites) {
    assert.ok(position[required] < position[course], `${required} must come before ${course}`);
  }
}

test("one prerequisite", () => {
  const pre: [number, number][] = [[1, 0]];
  assertValidOrder(2, pre, courseOrder(2, pre));
});

test("two paths to the same course", () => {
  const pre: [number, number][] = [[1, 0], [2, 0], [3, 1], [3, 2]];
  assertValidOrder(4, pre, courseOrder(4, pre));
});

test("no prerequisites", () => {
  assertValidOrder(3, [], courseOrder(3, []));
});

test("single course", () => {
  assert.deepEqual(courseOrder(1, []), [0]);
});

test("two courses requiring each other", () => {
  assert.deepEqual(courseOrder(2, [[0, 1], [1, 0]]), []);
});

test("cycle that does not include every course", () => {
  assert.deepEqual(courseOrder(4, [[1, 0], [2, 1], [3, 2], [1, 3]]), []);
});

test("repeated pair", () => {
  const pre: [number, number][] = [[1, 0], [1, 0], [2, 1]];
  assertValidOrder(3, pre, courseOrder(3, pre));
});

test("chain of 100 000 courses in O(V + E)", () => {
  const n = 100000;
  const pre: [number, number][] = [];
  for (let i = 0; i < n - 1; i++) pre.push([i, i + 1]);
  assertValidOrder(n, pre, courseOrder(n, pre));
});
