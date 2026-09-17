# Days until warmer

Topic: 7. Stacks and queues
Difficulty: 2 of 3

## Problem

A weather app shows, under each day's forecast, how long you have to wait for a warmer day.

Write `daysUntilWarmer(temps: number[]): number[]`. `temps[i]` is the temperature on day `i`. Return a new array of the same length where position `i` holds the number of days from day `i` to the next later day that is strictly warmer than day `i`. If no later day is warmer, that position holds `0`.

An equal temperature does not count as warmer. Don't change `temps`.

## Examples

```
daysUntilWarmer([73, 74, 75, 71, 69, 72, 76, 73])  → [1, 1, 4, 2, 1, 1, 0, 0]
daysUntilWarmer([30, 40, 50, 60])                  → [1, 1, 1, 0]
daysUntilWarmer([60, 50, 40])                      → [0, 0, 0]
daysUntilWarmer([5, 5, 6])                         → [2, 1, 0]
daysUntilWarmer([])                                → []
```

## Constraints

- `temps` has 0 to 1000000 elements; each is a whole number from -1000000000 to 1000000000.
- Required: O(n) time and O(n) extra space.
- The large test has a long run of falling temperatures, so checking every later day for every day is too slow.

## Hints

1. In `[73, 74, 75, 71, 69, 72]`, days 3 and 4 (71 and 69) are both waiting when you reach 72. Which of the waiting days are still waiting after that, and in what order did they arrive?
2. If you keep a collection of days that haven't found their warmer day yet, what do you notice about their temperatures from oldest to newest?
3. When a new day arrives, which waiting days can it settle, and where in your collection are they? When can you stop checking?
4. What should you store for a waiting day so that you can work out its answer later: its temperature, its index, or both?

## Explain-back

- Why does the collection of waiting days behave like a stack, and why are its temperatures never increasing from bottom to top?
- Your loop has a `while` inside a `for`. Why is the total time still O(n)? How many times can one index be pushed and popped?
- What does your code do with two days of equal temperature, like `[5, 5, 6]`, and which comparison decides that?
- What is the extra space in the worst case, and which input causes it?
