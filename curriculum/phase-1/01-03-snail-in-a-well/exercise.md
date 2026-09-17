# Snail in a well

Topic: 1. A method for solving problems
Difficulty: 3 of 3

## Problem

A snail sits at the bottom of a well that is `depth` metres deep. Every day it climbs up `climb` metres. Every night it slides back down `slide` metres.

The snail is out as soon as it reaches the top (height `depth` or more) during a day. Once it is out, it does not slide back.

Write `daysToEscape(depth, climb, slide)` that returns the day number on which the snail gets out. If the snail can never get out, return `-1`.

Before you write any code: restate the problem in your own words, work out the answers for `(10, 3, 2)` and `(10, 2, 2)` by hand, and write your plan as numbered steps.

## Examples

```
daysToEscape(10, 3, 2)  → 8
daysToEscape(5, 3, 1)   → 2
daysToEscape(3, 5, 1)   → 1
daysToEscape(10, 2, 2)  → -1
```

## Constraints

- `depth` is a whole number from 1 to 1000000.
- `climb` is a whole number from 1 to 1000000.
- `slide` is a whole number from 0 to 1000000.

## Hints

1. For `(10, 3, 2)`, make a table with one line per day: height in the morning, height after climbing, height after sliding. When do you stop filling it in?
2. Your table shows the snail is out on day 8, but after 7 full days it has only gained 7 metres. Why doesn't "10 metres at 1 metre per day = 10 days" give the right answer?
3. The last day is different from all the days before it. How high must the snail be at the start of its last day, so that one climb gets it out?
4. When is it impossible to escape? Think about what happens on day 1, and about what one full day and night does to the snail's height.

## Explain-back

- Which line of your hand-worked table shows why the answer for `(10, 3, 2)` is 8 and not 10?
- What does your code return for `(10, 5, 5)` and for `(5, 5, 5)`? Why are they different?
- You passed the four examples. What other input did you check before trusting your code, and why that one?
