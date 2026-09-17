# Course order

Topic: 15. Graphs
Difficulty: 3 of 3

## Problem

There are `numCourses` courses numbered `0` to `numCourses - 1`. `prerequisites` is an array of pairs `[course, required]`, each meaning you must take course `required` before course `course`. The same pair may appear more than once.

Write `courseOrder(numCourses, prerequisites)` that returns an array containing every course exactly once, in an order where each course comes after all of its required courses.

If there is no such order (because some courses require each other in a cycle), return an empty array `[]`.

Often several orders are valid; any valid order is accepted. The tests check that your array holds each course exactly once and respects every pair.

## Examples

```
courseOrder(2, [[1, 0]])                          → [0, 1]
courseOrder(4, [[1, 0], [2, 0], [3, 1], [3, 2]])  → [0, 1, 2, 3]  or  [0, 2, 1, 3]
courseOrder(3, [])                                → any order of 0, 1, 2
courseOrder(2, [[0, 1], [1, 0]])                  → []
```

## Constraints

- 1 ≤ `numCourses` ≤ 100 000; 0 ≤ `prerequisites.length` ≤ 100 000.
- `0 ≤ course, required < numCourses` and `course !== required`.
- O(numCourses + prerequisites.length) time and space. The tests include a chain of 100 000 courses.

## Hints

1. Draw the courses as nodes and each pair as an arrow. Which way should the arrow point so that following arrows matches the order you take courses?
2. Which courses can you take right now, on day one? What number, stored for each course, tells you that?
3. When you take a course, how does that change what you know about the courses that depend on it? When does one of them become ready?
4. If the process stops with some courses never taken, what must be true about those courses? How can you tell this happened without searching for the cycle itself?

## Explain-back

- What does a course's in-degree mean here, and why is a course with in-degree 0 always safe to take next?
- Why does "fewer than `numCourses` courses were output" prove there is a cycle?
- What are the time and space complexity, and where does each part (building the lists, the queue loop) come from?
- A repeated pair like `[1, 0]` listed twice: does your code handle it correctly, and why?
