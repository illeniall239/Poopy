# Fewest coins

Topic: 16. Dynamic programming
Difficulty: 2 of 3

## Problem

Write `fewestCoins(coins, amount)` that returns the smallest number of coins that add up to exactly `amount`, or `-1` if no combination of coins makes that amount.

- `coins` holds distinct positive coin values, in no particular order.
- You have an unlimited supply of every coin value.
- An `amount` of 0 needs 0 coins.

Unlike the vending machine in Phase 1, these coin values are arbitrary, so always taking the largest coin that fits does not always give the fewest coins.

## Examples

```
fewestCoins([1, 2, 5], 11)  → 3    (5 + 5 + 1)
fewestCoins([1, 3, 4], 6)   → 2    (3 + 3; largest-first would use 4 + 1 + 1)
fewestCoins([2], 3)         → -1
fewestCoins([1], 0)         → 0
```

## Constraints

- 1 ≤ `coins.length` ≤ 12; each coin from 1 to 10 000.
- 0 ≤ `amount` ≤ 10 000.
- O(amount × coins.length) time. The tests include amounts of about 700, where trying every combination by plain recursion never finishes.

## Hints

1. Try largest-coin-first on `[1, 3, 4]` with amount 6. Why can't a single local choice be trusted here?
2. Suppose the last coin you use has value `c`. What smaller problem is left, and how does its answer relate to the answer for `amount`?
3. The answer for `amount` depends on answers for several smaller amounts. Which smaller amounts do you reach again and again from different paths, and how can you avoid recomputing them?
4. If you fill in answers for 0, 1, 2, … up to `amount`, what should an amount that cannot be made hold so that it never wins a "minimum" comparison and is easy to turn into `-1` at the end?

## Explain-back

- What does dp[x] mean in your solution, what is its base case, and what is the recurrence?
- Why does largest-coin-first fail for `[1, 3, 4]` and amount 6, while your approach is correct for any coin values?
- What are the time and space complexity in terms of `amount` and the number of coins? Why was the plain recursive version exponential?
- How does your code handle amounts that cannot be made, both in the middle of the table and as the final answer?
