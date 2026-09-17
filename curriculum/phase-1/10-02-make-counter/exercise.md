# Make a counter

Topic: 10. Higher-order functions and closures
Difficulty: 2 of 3

## Problem

Write `makeCounter(start, step)` that returns a new `Counter`: an object with four functions that share one private count.

- `increment()` adds `step` to the count and returns the new count.
- `decrement()` subtracts `step` from the count and returns the new count.
- `reset()` sets the count back to `start` and returns it.
- `value()` returns the current count without changing it.

`start` defaults to `0` and `step` defaults to `1`. The count starts at `start`.

The count must be private: the returned object has exactly the four keys `increment`, `decrement`, `reset` and `value`, and nothing else. Each call to `makeCounter` makes an independent counter. The functions must keep working when taken off the object, for example `const inc = counter.increment; inc();`.

## Examples

```
const c = makeCounter();
c.increment()   → 1
c.increment()   → 2
c.decrement()   → 1
c.value()       → 1

const byTen = makeCounter(100, 10);
byTen.increment()  → 110
byTen.reset()      → 100

Object.keys(makeCounter())  → ["increment", "decrement", "reset", "value"]  (any order)
```

## Constraints

- `start` and `step` are whole numbers from -1000000 to 1000000.
- Don't use classes or `this`.

## Hints

1. Where can a number live so that four different functions can all read and change it, but code outside can't reach it?
2. When `makeCounter` returns, you might expect its local variables to disappear. What keeps a variable alive after the function that declared it has finished?
3. If you call `makeCounter` twice, how many separate copies of that local variable exist? What does that tell you about independence?
4. Why might a function that reads `this.count` break when you write `const inc = counter.increment; inc();`, while one that reads a local variable doesn't?

## Explain-back

- Point to the exact variable each of your four functions closes over. Where does it live after `makeCounter` returns?
- Two counters made by two calls to `makeCounter` don't affect each other. Explain why, using the idea of a closure.
- In `for (var i = 0; i < 3; i++) fns.push(() => i)`, every function returns `3`. With `let` instead of `var` they return `0`, `1`, `2`. What is each closure capturing in the two cases?
