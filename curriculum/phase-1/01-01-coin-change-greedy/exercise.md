# Coin change

Topic: 1. A method for solving problems
Difficulty: 1 of 3

## Problem

A vending machine gives change using quarters (25¢), dimes (10¢), nickels (5¢) and pennies (1¢). It always uses the fewest coins possible.

Write `makeChange(cents)` that returns how many of each coin to give, as `{ quarters, dimes, nickels, pennies }`.

Before you write any code: restate the problem in your own words, work out the answer for `41` and for `0` by hand, and write your plan as numbered steps.

## Examples

```
makeChange(41)  → { quarters: 1, dimes: 1, nickels: 1, pennies: 1 }
makeChange(30)  → { quarters: 1, dimes: 0, nickels: 1, pennies: 0 }
makeChange(0)   → { quarters: 0, dimes: 0, nickels: 0, pennies: 0 }
```

## Constraints

- `cents` is a whole number from 0 to 100000.

## Hints

1. How did you work out 41 by hand? Write down exactly what you did first, second, third.
2. When you picked quarters first, how did you decide how many quarters? What was left over afterwards?
3. After giving some quarters, is the remaining problem the same problem, just with a smaller amount and fewer coin types?
4. `41 / 25` gives `1.64`, not the whole number `1`. Which `Math` function drops the fraction, and which operator gives you what's left over?

## Explain-back

- Why does taking the largest coin first give the fewest coins here?
- What does your code do for `0`, and why is that correct without a special case?
- If the machine also had a 12¢ coin, would your approach still give the fewest coins for 15¢? Work it out by hand.
