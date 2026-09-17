# Compose a pipeline

Topic: 10. Higher-order functions and closures
Difficulty: 3 of 3

## Problem

A `Step` is a function `(n: number) => number`. Write two functions that build new Steps out of other functions:

- `pipeline(steps)` returns a single `Step` that runs the steps left to right: the first step gets the input, each later step gets the previous step's output, and the last output is returned. With no steps, the returned Step gives back its input unchanged. Each step runs exactly once per call. The returned Step can be called any number of times. Changing the `steps` array after calling `pipeline` (for example, pushing another step onto it) must not change what the returned Step does.
- `when(predicate, step)` returns a `Step` that runs `step` on its input if `predicate(input)` is `true`, and otherwise returns the input unchanged.

## Examples

```
const addOne = (n: number) => n + 1;
const double = (n: number) => n * 2;

pipeline([addOne, double])(3)   → 8     (3 + 1 = 4, then 4 * 2)
pipeline([double, addOne])(3)   → 7
pipeline([])(42)                → 42

const halveEvens = when((n) => n % 2 === 0, (n) => n / 2);
halveEvens(10)  → 5
halveEvens(7)   → 7

pipeline([addOne, halveEvens, double])(5)  → 6
```

## Constraints

- `steps` has 0 to 1000 functions.
- Don't use `for` or `while` loops.

## Hints

1. What does `pipeline` return: a number or a function? What does that returned function need to remember from the call that created it?
2. Running steps one after another means "take the value so far, apply the next step, carry the result forward". Which array method carries a value forward like that?
3. With that method, what should the starting value be so that zero steps gives back the input?
4. The returned function reads the steps later, when it's called. If someone pushes onto the same array in between, what will it see? How could you make sure it only ever sees the steps that existed when `pipeline` was called?

## Explain-back

- Which variables does the function returned by `pipeline` close over, and when is each one read?
- Why does the "push a step afterwards" case break some solutions but not others? Is the closure capturing the array's contents or a reference to the array?
- What would go wrong if you left out `reduce`'s starting value here, for an empty `steps` array and for a non-empty one?
