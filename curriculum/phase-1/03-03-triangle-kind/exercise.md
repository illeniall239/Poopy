# Triangle kind

Topic: 3. Conditionals and boolean logic
Difficulty: 3 of 3

## Problem

Write `triangleKind(a, b, c)` that takes three side lengths and returns one of these strings (the type `TriangleKind`):

- `"invalid"` if the sides can't make a triangle. Sides make a triangle only when every side is greater than 0 **and** each pair of sides adds up to strictly more than the third side. So `1, 2, 3` is `"invalid"`: it would be a flat line.
- `"equilateral"` if it's a valid triangle with all three sides equal.
- `"isosceles"` if it's a valid triangle with exactly two sides equal.
- `"scalene"` if it's a valid triangle with no sides equal.

The sides can be given in any order.

## Examples

```
triangleKind(3, 3, 3)  → "equilateral"
triangleKind(5, 3, 3)  → "isosceles"
triangleKind(3, 4, 5)  → "scalene"
triangleKind(1, 2, 3)  → "invalid"
triangleKind(1, 1, 5)  → "invalid"
triangleKind(0, 0, 0)  → "invalid"
```

## Constraints

- `a`, `b` and `c` are whole numbers from -1000 to 1000.

## Hints

1. Classify `1, 1, 5` and `0, 0, 0` by hand. Which two answers does each one seem to fit? Which is correct?
2. So which question must your code ask before any of the others?
3. An equilateral triangle also has "two sides equal". If you check for isosceles before equilateral, what happens to `3, 3, 3`?
4. How many different pairs of sides could be the equal pair? Which operator says "at least one of these is true"? For the triangle rule, how many comparisons do you need, and must all of them or just one of them hold?

## Explain-back

- Why does your code check for `"invalid"` first? Show an input that breaks if that check moves to the end.
- `if (a && b && c)` looks like a way to reject zero sides. What does it do with `-3`, and why isn't it enough?
- Write "the sides are invalid" as the negation of your "the sides are valid" expression, without a `!` in front of the brackets. Did every `&&` become `||`?
