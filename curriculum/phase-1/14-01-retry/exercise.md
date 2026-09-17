# Retry

Topic: 14. Promises, async/await and the event loop
Difficulty: 1 of 3

## Problem

Network calls sometimes fail for no lasting reason, so it's common to try again. Write `retry(task, maxAttempts, delayMs)`:

- `task` is a function that returns a `Promise<string>`. Each call to `task` is one attempt.
- Call `task`. If its promise resolves, `retry` resolves with that value and makes no more attempts.
- If it rejects and fewer than `maxAttempts` attempts have been made, wait `delayMs` milliseconds, then try again.
- If all `maxAttempts` attempts reject, `retry` rejects with the error from the last attempt (the same error object, not a copy or a new error).
- Attempts never overlap: the next attempt starts only after the previous one has rejected and the delay has passed.
- `delayMs` defaults to `0`.
- If `maxAttempts` is less than 1, `retry` rejects with a `RangeError` whose message is `maxAttempts must be at least 1`, without calling `task`.

## Examples

```
// flaky() rejects the first two times it's called, then resolves "ok"
await retry(flaky, 3)        → "ok"     (flaky was called 3 times)
await retry(flaky, 2)        → rejects with the error from the 2nd call
await retry(alwaysFails, 0)  → rejects with RangeError: maxAttempts must be at least 1
await retry(alwaysFails, 3, 20)
  → rejects after about 40ms (two waits of 20ms between three attempts)
```

## Constraints

- `maxAttempts` is a whole number from -10 to 100.
- `delayMs` is a whole number from 0 to 1000.
- You'll need a way to wait `delayMs` milliseconds. Build a small promise around `setTimeout`.

## Hints

1. Describe in words what happens for `retry(flaky, 3)`: for each attempt, what did the task do, and what did `retry` do next?
2. To know whether an attempt failed, you have to catch its rejection. What happens with `try { return task(); } catch { ... }` if you leave out `await`? Where does the rejection go?
3. After the loop ends because every attempt failed, which error do you still have access to? Where do you need to store it so it survives the loop?
4. `setTimeout` takes a callback, not a promise. How can you wrap it in a `new Promise` so you can `await` a pause?

## Explain-back

- Walk through what happens, line by line, when the second attempt rejects in `retry(flaky, 3, 20)`. When does the third attempt start?
- What changes if you remove `await` in front of `task()`? Which test would fail, and why?
- Why do attempts in your solution never overlap? What would you have to write to make them overlap by accident?
