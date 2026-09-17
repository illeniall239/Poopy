# Slowest finishing speed

Topic: 8. Binary search
Difficulty: 2 of 3

## Problem

A print shop has several stacks of pages to shred before it closes in `h` hours. The shredder is set to a speed of `k` pages per hour, a whole number of at least 1. Each hour, the operator picks one stack and feeds up to `k` pages from it. If that stack has fewer than `k` pages left, it is finished and the shredder sits idle for the rest of that hour; it never moves on to a second stack in the same hour.

So a stack of `p` pages takes `Math.ceil(p / k)` hours.

Write `minShredSpeed(stacks: number[], h: number): number` that returns the smallest speed `k` that shreds every stack within `h` hours in total.

Don't change `stacks`.

## Examples

```
minShredSpeed([3, 6, 7, 11], 8)       → 4
minShredSpeed([30, 11, 23, 4, 20], 5) → 30
minShredSpeed([30, 11, 23, 4, 20], 6) → 23
minShredSpeed([10], 3)                → 4
minShredSpeed([5, 5], 1000000000)     → 1
```

For the first example, speed 4 takes 1 + 2 + 2 + 3 = 8 hours, and speed 3 would take 1 + 2 + 3 + 4 = 10.

## Constraints

- `stacks` has 1 to 100000 elements; each is a whole number from 1 to 1000000000.
- `h` is a whole number from `stacks.length` to 1000000000, so an answer always exists.
- Required: O(n log m) time, where m is the largest stack, and O(1) extra space.
- In the large test the answer is far from both the smallest and the largest speed worth trying, so trying speeds one by one is too slow.
- In Java, total hours can exceed the `int` range; use `long` for the running total.

## Hints

1. Which speed definitely works, however small `h` is? Is there any point trying a speed larger than that? What's the smallest speed worth trying?
2. Write a helper that answers "can speed `k` finish within `h` hours?". If speed 10 works, what do you know about speed 11? If speed 10 fails, what about speed 9?
3. The answers to that helper for speeds 1, 2, 3, ... look like `false, false, ..., false, true, true, ...`. What are you really searching for in that sequence?
4. When the middle speed works, should you throw it away or keep it as a possible answer? How does that choice decide between `hi = mid` and `hi = mid - 1`?

## Explain-back

- Why is "can finish with speed k" monotonic, and why does binary search need that?
- State what `lo` and `hi` mean in your loop, and why the loop ends on the smallest working speed rather than one next to it.
- What are the time and space complexity? How many speeds do you test for stacks up to 1000000000 pages?
- How do you compute `Math.ceil(p / k)` without floating point, and where could an integer overflow happen in Java?
