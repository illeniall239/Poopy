# Ways to climb

Topic: 16. Dynamic programming
Difficulty: 1 of 3

## Problem

A staircase has `n` steps. Each move, you climb either 1 step or 2 steps. Write `climbWays(n)` that returns how many different sequences of moves take you from the bottom to exactly the top.

Two sequences are different if they differ in any move: for `n = 3`, `1+2` and `2+1` count as two ways. For `n = 0` you are already at the top, and doing nothing counts as exactly 1 way.

## Examples

```
climbWays(1)  → 1    (1)
climbWays(2)  → 2    (1+1, 2)
climbWays(3)  → 3    (1+1+1, 1+2, 2+1)
climbWays(0)  → 1
```

## Constraints

- 0 ≤ n ≤ 70. The answer for 70 is below 2⁵³, so a `number` holds it exactly (use `long` in Java).
- O(n) time. The tests include n = 45 and n = 70; plain recursion that recomputes the same sub-answers makes billions of calls and cannot finish.

## Hints

1. Think about the very last move onto the top step. What are the only two possibilities, and where were you standing just before each?
2. Write "the number of ways to reach step n" in terms of the number of ways to reach smaller steps. Which base cases does that need?
3. Draw the calls your formula makes for n = 5. Which values get computed more than once, and how many times?
4. If you work upwards from the bottom step instead of downwards from the top, how many earlier answers do you actually need to keep at any moment?

## Explain-back

- State your state and recurrence in words: what does "ways(i)" mean, and why does ways(i) = ways(i − 1) + ways(i − 2)?
- Why does the plain recursive version take exponential time, and why does storing each answer make it O(n)?
- What is the space complexity of your solution? Could you make it O(1), and what would you keep?
- Why is ways(0) = 1 the right base case and not 0? What would your answers be if it were 0?
