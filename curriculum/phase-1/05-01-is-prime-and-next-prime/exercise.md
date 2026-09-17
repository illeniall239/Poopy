# Is prime and next prime

Topic: 5. Functions and breaking problems down
Difficulty: 1 of 3

## Problem

A prime is a whole number greater than 1 whose only divisors are 1 and itself.

Write two functions:

- `isPrime(n)` returns `true` if `n` is prime and `false` otherwise.
- `nextPrime(n)` returns the smallest prime that is strictly greater than `n`. It must use `isPrime`.

Both functions return their answer. Neither prints anything.

## Examples

```
isPrime(7)      → true
isPrime(1)      → false
isPrime(25)     → false
nextPrime(13)   → 17
nextPrime(0)    → 2
nextPrime(-10)  → 2
```

## Constraints

- `n` is a whole number from -1000000 to 2000000.
- Each call must finish well under a second.

## Hints

1. Write `isPrime` first and test it on its own. What does it promise to its caller, in one sentence? Which inputs are answered before any loop?
2. To decide that 97 is prime, which divisors do you need to try? Do you really need to go all the way up to 96?
3. If `n` has a divisor bigger than its square root, what can you say about the divisor it pairs with? So where can your loop stop, and should that stop be `<` or `<=`? Check with 25.
4. With a working `isPrime`, what does `nextPrime` need to do? Where does it start looking, and when does it stop?

## Explain-back

- What does `isPrime` promise, and how does `nextPrime` rely on that promise without knowing how it works?
- Where did you use an early return, and what would the code look like without it?
- If `isPrime` used `console.log(true)` instead of `return true`, what would `nextPrime` see?
