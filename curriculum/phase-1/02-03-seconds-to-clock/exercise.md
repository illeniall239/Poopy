# Seconds to clock

Topic: 2. Values, types, variables and expressions
Difficulty: 3 of 3

## Problem

A stopwatch stores elapsed time as a whole number of seconds. The screen shows it as hours, minutes and seconds.

Write `toClock(totalSeconds)` that returns a `string` in the form `"HH:MM:SS"`:

- `HH` is the number of whole hours, `MM` the remaining whole minutes (0 to 59), `SS` the remaining seconds (0 to 59).
- Each part is always exactly two digits, with a leading zero when it is below 10.
- Hours do not wrap around at 24.

## Examples

```
toClock(0)       → "00:00:00"
toClock(59)      → "00:00:59"
toClock(3600)    → "01:00:00"
toClock(45296)   → "12:34:56"
toClock(359999)  → "99:59:59"
```

## Constraints

- `totalSeconds` is a whole number from 0 to 359999, so hours are at most 99.
- Use arithmetic and template literals only; no string padding methods.

## Hints

1. Work out `45296` by hand. How many whole hours fit into it? How many seconds are left over after taking those hours out?
2. How many seconds are in an hour? In a minute? Which operators give you "how many whole ones fit" and "what's left over"?
3. Suppose you have `h = 1`. What does a template literal like `` `${h}:...` `` show? What should it show instead?
4. For a number from 0 to 99, how can you get its tens digit and its ones digit separately, using the same two operators as before?

## Explain-back

- What is `45296 / 3600` in TypeScript, and why can't you use it directly as the hours?
- What would `"0" + 5` and `0 + 5` each give, and which one did you want where?
- Trace `toClock(3599)` by hand through your code. What is the value of every variable?
