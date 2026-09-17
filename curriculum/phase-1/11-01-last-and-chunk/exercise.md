# Last and chunk

Topic: 11. Generics and utility types
Difficulty: 1 of 3

## Problem

Write two generic functions that work on arrays of any element type and keep that type for the caller.

- `last<T>(items: T[]): T | undefined` returns the final element, or `undefined` for an empty array.
- `chunk<T>(items: T[], size: number): T[][]` splits `items` into consecutive groups of `size` elements. The final group holds whatever is left and may be shorter. An empty array returns `[]`. If `size` is not a whole number of at least 1, throw an `Error`.

Neither function changes the input array. Don't use `any`.

## Examples

```
last([3, 1, 4])                 → 4
last(["a"])                     → "a"
last([])                        → undefined

chunk([1, 2, 3, 4, 5], 2)       → [[1, 2], [3, 4], [5]]
chunk(["a", "b", "c"], 3)       → [["a", "b", "c"]]
chunk([], 4)                    → []
chunk([1, 2], 0)                → throws Error
```

## Constraints

- `items` has 0 to 10000 elements.
- The type of `last(["a", "b"])` must be `string | undefined`, and the type of `chunk([1, 2], 1)` must be `number[][]`. Your editor shows this when you hover over the call.

## Hints

1. Write `last` for `number[]` only first. What exactly would have to change to make it work for `string[]` too, without writing it twice?
2. If you typed the parameter as `any[]`, what type would the caller get back from `last(["a"])`? Hover over it and see.
3. For `chunk`, work `[1, 2, 3, 4, 5]` with size 2 by hand. At which indexes does each group start, and how do you get a group out of the array without a nested loop?
4. What does `slice` do when its end index is past the end of the array? Does that already handle the short final group for you?

## Explain-back

- What does `T` stand for while your code runs? Does it exist at runtime at all?
- Why is `T | undefined` more honest than `T` as the return type of `last`?
- Why does `chunk` return `T[][]` and not `T[]`? Describe the shape in words.
