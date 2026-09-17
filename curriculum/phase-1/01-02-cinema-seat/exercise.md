# Cinema seat

Topic: 1. A method for solving problems
Difficulty: 2 of 3

## Problem

A cinema numbers its seats starting at 1. Numbering goes left to right along row 1, then continues left to right along row 2, and so on. Every row has the same number of seats.

Write `findSeat(seatNumber, seatsPerRow)` that returns where the seat is, as `{ row, column }`. Rows and columns both start at 1.

Before you write any code: restate the problem in your own words, work out the answer for seat `25` and for seat `10` in a cinema with 10 seats per row by hand, and write your plan as numbered steps.

## Examples

```
findSeat(1, 10)   → { row: 1, column: 1 }
findSeat(25, 10)  → { row: 3, column: 5 }
findSeat(10, 10)  → { row: 1, column: 10 }
findSeat(11, 10)  → { row: 2, column: 1 }
```

## Constraints

- `seatNumber` is a whole number from 1 to 1000000.
- `seatsPerRow` is a whole number from 1 to 1000.

## Hints

1. Draw the first three rows of a cinema with 4 seats per row and write the seat number in each box. What do you notice about the seat numbers at the end of each row?
2. Which seat numbers end up in column 1? What do those numbers have in common?
3. Your first idea probably works for seat 25 but not for seat 10. What is special about the last seat in a row?
4. What would change if the seats were numbered starting at 0 instead of 1? Could you shift the number, do the work, then shift back?

## Explain-back

- Walk through seat `10` with 10 seats per row. Which step of your plan handles the last seat in a row?
- Which examples did you check by hand before you ran the tests, and why did you pick them?
- If a cinema has 1 seat per row, what does your code return for seat `7`? Work it out without running it.
