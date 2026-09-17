# Debug: binary to decimal

Topic: 15. Reading and debugging code
Difficulty: 2 of 3

## Problem

`binaryToDecimal(bits)` is supposed to convert a string of binary digits into the number it represents. The rightmost character is worth 1, the next one to the left 2, then 4, 8 and so on; the result is the sum of the values of the positions holding a `"1"`. Leading zeros are allowed.

It rejects bad input:
- an empty string throws an `Error` with the message `Binary string is empty`;
- a string containing any character other than `"0"` or `"1"` throws an `Error` with the message `Not a binary string: "<bits>"`.

This function has a bug (or bugs). Find and fix it without rewriting it from scratch.

## Examples

```
binaryToDecimal("0")      → 0
binaryToDecimal("1")      → 1
binaryToDecimal("10")     → 2
binaryToDecimal("0110")   → 6
binaryToDecimal("1011")   → 11
binaryToDecimal("")       → throws Error: Binary string is empty
binaryToDecimal("102")    → throws Error: Not a binary string: "102"
```

## Constraints

- `bits` has 0 to 50 characters.
- Keep the function's structure. The fix should be small.

## Hints

1. Run the tests and list which inputs give the wrong answer and which give the right one. `"0110"` passes but `"1011"` doesn't. What's different about those two strings?
2. For each failing input, what did the function return, and what's the difference between that and the right answer? Is the difference always the value of one particular position?
3. Make a tracing table for `binaryToDecimal("10")` with columns `i`, `bits[i]`, `placeValue` and `result`. Which characters of the string does the loop actually look at?
4. Look at the loop's start value, its condition and its update together. For a string of length 2, which indexes should the loop visit, and which does it visit?

## Explain-back

- What was your hypothesis before you changed any code, and which test result or trace row confirmed it?
- Why did inputs starting with `"0"` hide the bug? What input would you add to a test suite to catch this kind of mistake early?
- Suppose you'd "fixed" it by adding `if (bits[0] === "1") result += 1` at the end. Some tests would pass. Why is that fixing a symptom rather than the cause?
