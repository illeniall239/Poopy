# Safe divide with a result object

Topic: 13. Errors and input validation
Difficulty: 2 of 3

## Problem

Instead of throwing, some functions return a result object that says whether they worked. Use this type:

```ts
type Result = { ok: true; value: number } | { ok: false; error: string };
```

Write two functions that never throw:

- `safeDivide(a, b)` returns `{ ok: true, value: a / b }` when the division makes sense. Check these in order and return the first failure:
  1. If `a` or `b` is not a finite number (`NaN`, `Infinity` or `-Infinity`), return `{ ok: false, error: "Inputs must be finite numbers" }`.
  2. If `b` is `0`, return `{ ok: false, error: "Cannot divide by zero" }`.
- `sumOfQuotients(pairs)` takes an array of `{ a, b }` objects, divides each pair with `safeDivide`, and returns `{ ok: true, value: <sum of all quotients> }`. If any pair fails, it stops at the first failing pair and returns `{ ok: false, error: "Pair <position>: <error>" }`, where `<position>` counts from 1 and `<error>` is that pair's error. An empty array sums to `0`.

Result objects have exactly the keys shown: a success has no `error` key and a failure has no `value` key.

## Examples

```
safeDivide(10, 4)          → { ok: true, value: 2.5 }
safeDivide(0, 5)           → { ok: true, value: 0 }
safeDivide(1, 0)           → { ok: false, error: "Cannot divide by zero" }
safeDivide(NaN, 0)         → { ok: false, error: "Inputs must be finite numbers" }

sumOfQuotients([{ a: 10, b: 2 }, { a: 9, b: 3 }])               → { ok: true, value: 8 }
sumOfQuotients([{ a: 1, b: 1 }, { a: 5, b: 0 }, { a: 1, b: 0 }]) → { ok: false, error: "Pair 2: Cannot divide by zero" }
sumOfQuotients([])                                               → { ok: true, value: 0 }
```

## Constraints

- `pairs` has 0 to 1000 items.
- Neither function may throw, and neither may use `try`/`catch`.

## Hints

1. What does `1 / 0` give in JavaScript? Does it throw? Why is that a problem for the code that uses the answer?
2. Which built-in check tells you a number is not `NaN` and not infinite in one go?
3. After calling `safeDivide` inside `sumOfQuotients`, TypeScript won't let you read `.value` straight away. What do you have to check first, and why does that check make `.value` available?
4. When one pair fails, what information does the caller of `sumOfQuotients` need that `safeDivide`'s error alone doesn't give?

## Explain-back

- When is returning a result object better than throwing, and when is throwing better? Use this exercise and `parseAge` as examples.
- Your `sumOfQuotients` adds `Pair 2:` to the message. Why add context at this level instead of inside `safeDivide`?
- If `sumOfQuotients` ignored failing pairs and summed the rest, what would go wrong for someone relying on the total?
