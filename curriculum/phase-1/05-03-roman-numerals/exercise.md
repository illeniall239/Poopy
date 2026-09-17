# Roman numerals

Topic: 5. Functions and breaking problems down
Difficulty: 3 of 3

## Problem

Roman numerals use these symbols: `I` = 1, `V` = 5, `X` = 10, `L` = 50, `C` = 100, `D` = 500, `M` = 1000.

A number is written from its largest place to its smallest (thousands, hundreds, tens, ones). Each place follows the same pattern, using that place's "one", "five" and "ten" symbols. For the ones place (`I`, `V`, `X`):

```
1 I    2 II    3 III    4 IV    5 V    6 VI    7 VII    8 VIII    9 IX
```

A digit of 0 writes nothing. The tens place uses `X`, `L`, `C` the same way (40 is `XL`, 90 is `XC`), the hundreds place uses `C`, `D`, `M`, and thousands use only `M` (3000 is `MMM`).

Write `toRoman(n)` that returns `n` as a Roman numeral string. If `n` is not a whole number from 1 to 3999, return the empty string `""`.

## Examples

```
toRoman(3)     → "III"
toRoman(14)    → "XIV"
toRoman(1994)  → "MCMXCIV"
toRoman(3999)  → "MMMCMXCIX"
toRoman(0)     → ""
toRoman(4000)  → ""
```

## Constraints

- `n` is any number from -100000 to 100000 and may have decimals.
- The result uses capital letters only.

## Hints

1. Convert 1994 by hand, one place at a time. What did you write for the 1, the 9, the 9 and the 4? What did you do differently for each place?
2. Writing a 9 in the hundreds place and a 9 in the tens place follows the same steps, just with different letters. What would a helper that writes one digit need to be given?
3. Look at the table for 1 to 9. Which groups of digits share a shape (for example 1–3, 4, 5–8, 9)? How would your helper handle each group?
4. Which checks belong at the very start of `toRoman`, before any conversion? How do you get each place's digit out of `n` with the operators from Topic 2?

## Explain-back

- What does your one-digit helper promise? Test it in your head with digit `4` and the tens symbols.
- Where do you reject invalid input, and why is an early return there clearer than an `if` around all the rest?
- If your helper printed the letters with `console.log` instead of returning them, what would `toRoman` get back?
