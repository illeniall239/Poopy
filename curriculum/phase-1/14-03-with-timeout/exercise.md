# With timeout

Topic: 14. Promises, async/await and the event loop
Difficulty: 3 of 3

## Problem

Some work never finishes, and you don't want to wait forever. Write two functions:

- `sleep(ms)` returns a `Promise<void>` that resolves after `ms` milliseconds.
- `withTimeout(promise, ms)` returns a new `Promise<string>` that settles the same way as `promise` if `promise` settles within `ms` milliseconds:
  - if `promise` resolves first, resolve with its value;
  - if `promise` rejects first, reject with its error (the same error object);
  - if `ms` milliseconds pass first, reject with an `Error` whose message is `Timed out after <ms>ms`, without waiting any longer for `promise`.

  Whatever `promise` does after `withTimeout` has settled is ignored, and must not cause an unhandled rejection. Once `promise` settles first, clear the timer so it doesn't keep the program running.

  If `ms` is negative, `withTimeout` returns a promise that rejects with a `RangeError` whose message is `ms must not be negative`.

## Examples

```
await sleep(20)                                            → undefined, after about 20ms

await withTimeout(sleep(5).then(() => "done"), 50)         → "done"
await withTimeout(sleep(50).then(() => "late"), 10)        → rejects: Error "Timed out after 10ms"  (after about 10ms)
await withTimeout(Promise.reject(new Error("boom")), 50)   → rejects with that same "boom" error
await withTimeout(Promise.resolve("ready"), 0)             → "ready"
await withTimeout(Promise.resolve("x"), -1)                → rejects: RangeError "ms must not be negative"
```

## Constraints

- `ms` is a whole number from -1000 to 10000.
- You may use `new Promise`, `setTimeout`, `clearTimeout`, and `Promise.race`.

## Hints

1. A promise can only settle once. If two things race to settle the same promise, what happens to the second attempt?
2. What would you need to create so that "time ran out" is itself something that can settle, just like `promise`?
3. If you write `const value = await promise;` before starting the timer, how long does `withTimeout` wait for slow work? Where should the waiting happen instead?
4. When `promise` wins the race, the timer is still scheduled. What does `setTimeout` give back that lets you cancel it, and where in your code do you know the race is over whichever side won?

## Explain-back

- Predict what's logged, and in what order, for: `console.log(1); withTimeout(sleep(10).then(() => "a"), 50).then(console.log); console.log(2);`. Explain why.
- After a timeout, the original `promise` might still resolve or reject later. What happens to that result, and why doesn't a late rejection crash the program?
- Does `withTimeout` stop the slow work itself? What would it take to actually cancel it?
