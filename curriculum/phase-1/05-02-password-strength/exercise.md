# Password strength

Topic: 5. Functions and breaking problems down
Difficulty: 2 of 3

## Problem

Write four small rule-check helpers. Each takes a password string and returns a `boolean`:

- `hasLowercase(password)`: contains at least one letter `a` to `z`.
- `hasUppercase(password)`: contains at least one letter `A` to `Z`.
- `hasDigit(password)`: contains at least one digit `0` to `9`.
- `hasSymbol(password)`: contains at least one character that is not `a`–`z`, `A`–`Z` or `0`–`9`. Spaces count as symbols.

Then write `passwordStrength(password)` that uses the helpers and returns `{ score, label }`. The score starts at 0 and gets 1 point for each of these:

1. length is 8 or more
2. length is 12 or more (on top of the point above)
3. `hasLowercase`
4. `hasUppercase`
5. `hasDigit`
6. `hasSymbol`

`label` is `"weak"` for a score of 0 to 2, `"medium"` for 3 or 4, and `"strong"` for 5 or 6.

None of the functions print anything.

## Examples

```
hasDigit("abc1")                  → true
hasSymbol("aB3")                  → false
passwordStrength("")              → { score: 0, label: "weak" }
passwordStrength("abcdefgH")      → { score: 3, label: "medium" }
passwordStrength("Abcdefg1!")     → { score: 5, label: "strong" }
passwordStrength("Abcdefghij1!")  → { score: 6, label: "strong" }
```

## Constraints

- `password` has 0 to 200 characters, all from the basic keyboard (ASCII).
- You can loop over the characters of a string with `for...of`, and compare single characters with `<`, `<=`, `>`, `>=` (for example `"c" >= "a"` is `true`).

## Hints

1. Before writing `passwordStrength`, write one helper and test it on its own with a few strings. What exactly does it promise?
2. For `hasDigit`, as soon as you find one digit, do you need to look at the rest of the string? What should happen if the loop finishes without finding one?
3. `hasSymbol` is "not a lowercase letter, not an uppercase letter, and not a digit" for one character. Could you reuse the character checks you already wrote for the other helpers?
4. Once the helpers work, `passwordStrength` only adds up points and picks a label. Which score boundaries decide the label, and which comparisons put 2, 3, 4 and 5 in the right group?

## Explain-back

- What does each helper promise? Could you test `hasSymbol` without `passwordStrength` existing?
- Why does `passwordStrength` return an object instead of printing the score and label? What could a caller not do if it printed?
- If `hasDigit` also added to the score directly, what would go wrong when you reuse it somewhere else?
