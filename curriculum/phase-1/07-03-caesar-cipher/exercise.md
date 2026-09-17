# Caesar cipher

Topic: 7. Strings
Difficulty: 3 of 3

## Problem

A Caesar cipher hides a message by moving every letter a fixed number of places along the alphabet. With a shift of 3, `a` becomes `d`, `b` becomes `e`, and `z` wraps around to `c`.

Write `caesarShift(text, shift)` that returns the shifted text:

- Letters `a`–`z` shift within the lowercase alphabet; letters `A`–`Z` shift within the uppercase alphabet. Case is kept.
- Shifting past `z` wraps to `a` (and past `Z` to `A`).
- A negative `shift` moves letters backwards, wrapping from `a` to `z`.
- `shift` can be larger than 26 in either direction; a shift of 27 behaves like a shift of 1.
- Every other character (spaces, digits, punctuation) stays exactly as it is.

## Examples

```
caesarShift("abc", 1)              → "bcd"
caesarShift("xyz", 3)              → "abc"
caesarShift("Hello, World!", 5)    → "Mjqqt, Btwqi!"
caesarShift("bcd", -1)             → "abc"
caesarShift("abc", 27)             → "bcd"
```

## Constraints

- `text` has 0 to 100000 characters, and contains no letters outside `a`–`z` / `A`–`Z`.
- `shift` is a whole number from -1000000 to 1000000.

## Hints

1. Shift `"xyz"` by 3 by hand using the alphabet written out. How did you find the new letter for `y`?
2. If each letter has a position number (a = 0, ..., z = 25), what is the new position before wrapping? How do you bring a number like 27 back into 0–25?
3. What does `%` give for a negative number, such as `-1 % 26`? How can you turn that into a position between 0 and 25?
4. How can the same lowercase logic work for `"H"`, while making sure the result comes out uppercase again? And how will you tell whether a character is a letter at all?

## Explain-back

- Why can't you just replace the letter inside `text`, and what does your code build instead?
- Walk through `caesarShift("a", -27)`. What value does each step of your position calculation produce?
- How does your code keep `"H"` uppercase and leave `","` untouched?
