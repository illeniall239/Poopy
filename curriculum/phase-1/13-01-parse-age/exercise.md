# Parse an age

Topic: 13. Errors and input validation
Difficulty: 1 of 3

## Problem

A sign-up form sends the user's age as text. Write `parseAge(input)` that turns it into a number, or throws an error that says exactly what was wrong.

1. Ignore spaces at the start and end of `input`.
2. If nothing is left, throw an `Error` with the message `Age is empty`.
3. If what's left contains any character that isn't a digit `0`–`9` (so no signs, decimal points, letters or inner spaces), throw an `Error` with the message `Age must be a whole number, got "<input>"`, where `<input>` is the original `input` exactly as it was passed in.
4. If the number is greater than 150, throw a `RangeError` with the message `Age must be between 0 and 150, got <number>`.
5. Otherwise return the number. Leading zeros are allowed: `"007"` is `7`.

## Examples

```
parseAge("42")      → 42
parseAge("  7 ")    → 7
parseAge("0")       → 0
parseAge("007")     → 7
parseAge("")        → throws Error: Age is empty
parseAge("12.5")    → throws Error: Age must be a whole number, got "12.5"
parseAge("1e2")     → throws Error: Age must be a whole number, got "1e2"
parseAge("200")     → throws RangeError: Age must be between 0 and 150, got 200
```

## Constraints

- `input` is any string up to 100 characters.

## Hints

1. What do `Number("")`, `Number("   ")`, `Number("1e2")` and `parseInt("12abc")` return? Which of these would sneak past a check like "is the result a number"?
2. Given the traps in hint 1, is it safer to check the text before converting it, or the number after? What exactly would you check?
3. The rules are numbered in order. What goes wrong if you check the range before checking for non-digits?
4. Someone reading only the error message in a log should know what went wrong and with which value. What does your message need to include for that, and which error type tells callers "the format was fine but the value is out of range"?

## Explain-back

- Why check the characters yourself instead of trusting `Number(...)` or `parseInt(...)`? Give an input that would slip through each.
- The caller that shows this error to the user: should it catch the error, or should `parseAge` catch its own error and return something like `-1`? Why?
- Why is `Age must be a whole number, got "12.5"` a better message than `Invalid input`?
