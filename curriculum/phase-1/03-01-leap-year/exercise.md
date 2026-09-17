# Leap year

Topic: 3. Conditionals and boolean logic
Difficulty: 1 of 3

## Problem

In the Gregorian calendar, a year is a leap year when:

- it is divisible by 4,
- except years divisible by 100, which are not leap years,
- except years divisible by 400, which are leap years after all.

Write `isLeapYear(year)` that returns `true` if `year` is a leap year and `false` otherwise.

## Examples

```
isLeapYear(2024)  → true
isLeapYear(2023)  → false
isLeapYear(1900)  → false
isLeapYear(2000)  → true
```

## Constraints

- `year` is a whole number from 1 to 9999.
- Return a `boolean`.

## Hints

1. Put 2024, 2023, 1900 and 2000 through the three rules by hand. For each year, which rule decided the answer?
2. The rules overlap: 2000 is divisible by 4, by 100 and by 400. Which rule should win, and so which should you check first?
3. How do you test "divisible by 4" with an operator you already know? What does that expression give for 2023?
4. Once your `if`/`else if` version passes, can you write the same logic as one expression using `&&`, `||` and `!`? Check it against all four examples.

## Explain-back

- If your first condition returned `true` whenever the year is divisible by 4, what would 1900 give? Why does the order of your conditions matter?
- `year % 4` is `0` for 2024. Why is `if (year % 4)` a trap?
- Rewrite `!(year % 100 === 0 && year % 400 !== 0)` without the outer `!`. Does it mean the same thing?
