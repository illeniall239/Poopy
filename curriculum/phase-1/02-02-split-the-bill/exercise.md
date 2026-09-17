# Split the bill

Topic: 2. Values, types, variables and expressions
Difficulty: 2 of 3

## Problem

A group splits a restaurant bill evenly. Money can only be paid in whole cents, so when the bill doesn't divide evenly, the leftover cents go one each to the first people in the group.

Write `splitBill(totalDollars, people)` that returns `{ shareCents, peopleWithExtraCent }`:

- `shareCents` is the number of whole cents every person pays at least.
- `peopleWithExtraCent` is how many people (the first ones in the group) pay one extra cent on top of `shareCents`.

`totalDollars` is given in dollars, for example `19.99` means 1999 cents. Everyone together must pay exactly the total, no more and no less.

## Examples

```
splitBill(10, 3)     → { shareCents: 333, peopleWithExtraCent: 1 }
splitBill(19.99, 2)  → { shareCents: 999, peopleWithExtraCent: 1 }
splitBill(0.29, 1)   → { shareCents: 29, peopleWithExtraCent: 0 }
splitBill(0.02, 3)   → { shareCents: 0, peopleWithExtraCent: 2 }
```

## Constraints

- `totalDollars` is from 0 to 100000 with at most two decimal places.
- `people` is a whole number from 1 to 1000.

## Hints

1. Work out `splitBill(10, 3)` by hand in cents. How much does each person pay, and how many cents are left over?
2. Why is it easier to do the whole calculation in cents rather than dollars?
3. What is `10 / 3` in TypeScript? Is that the "whole cents each" you worked out by hand? Which operator gives you the leftover cents?
4. Before you divide, print `0.29 * 100` and `19.99 * 100`. Are they the whole numbers you expected? Which `Math` function turns them into the right whole number of cents?

## Explain-back

- What is `1999 / 2` in TypeScript, and why can't you use it directly as `shareCents`?
- What does `Math.floor(19.99 * 100)` give, and why is that the wrong number of cents?
- How do you know the answer for `splitBill(0.02, 3)` adds up to exactly the total?
