# Can you reach the last index

Topic: 17. Intervals and greedy algorithms
Difficulty: 1 of 3

## Problem

A board game is a row of squares. Each square shows a number: the most squares you may move forward from it. Standing on square `i`, you may jump to any of the squares `i + 1`, `i + 2`, …, `i + jumps[i]`. A square showing `0` cannot be left. You start on square `0`.

Write `canReachLastIndex(jumps: number[]): boolean`. It returns `true` if you can reach the last square, `false` otherwise.

- A jump may be any length from `1` to `jumps[i]`, so being able to jump past the last square means you can also land exactly on it.
- The array always has at least one element; with a single element you are already on the last square, so the answer is `true`.
- The value on the last square is irrelevant, because you never need to leave it.
- Don't change the array.

## Examples

```
canReachLastIndex([2, 3, 1, 1, 4])  → true     (0 → 1 → 4)
canReachLastIndex([3, 2, 1, 0, 4])  → false    (every route lands on the 0 at index 3)
canReachLastIndex([0])              → true
canReachLastIndex([0, 1])           → false
canReachLastIndex([2, 0, 0])        → true
```

## Constraints

- 1 ≤ `jumps.length` ≤ 200 000; 0 ≤ `jumps[i]` ≤ 200 000.
- Required: O(n) time and O(1) extra space.
- The large tests have 200 000 squares (100 000 in Python) with very large jump values, so trying every landing square from every square is too slow.

## Hints

1. From square `0` alone, which squares can you land on? If you can reach square 3, what does that tell you about squares 1 and 2?
2. Walk from left to right keeping one number: the farthest square you know you can reach so far. What does it mean if you arrive at a square beyond that number?
3. When you stand on a reachable square `i`, how does it change the farthest reachable square? When can you stop the walk early?
4. Try `[3, 2, 1, 0, 4]` by hand with your one number. Where does it get stuck, and why does the `4` never matter?

## Explain-back

- Why is it enough to track a single "farthest reachable" number instead of the set of every reachable square?
- What are the time and space complexity? Compare with a solution that tries every jump length from every square and remembers the answer per square.
- What is the greedy choice here, and why is it never wrong? What would a counterexample have to look like, and why can't one exist?
- Where would this approach break if jumps could also go backwards, or if some squares were forbidden to land on?
