# Flatten nested arrays

Topic: 12. Recursion
Difficulty: 2 of 3

## Problem

A `Nested` value is either a number or an array of `Nested` values, so arrays can hold numbers and other arrays to any depth:

```ts
type Nested = number | Nested[];
```

Write two recursive functions:

- `flatten(items)` returns a new array of all the numbers inside `items`, at any depth, in the order they appear from left to right. Empty arrays contribute nothing.
- `depth(items)` returns how many levels of arrays `items` has. `items` itself counts as level 1, so a flat array (including `[]`) has depth 1, and each array inside adds a level. The depth is the deepest level anywhere inside.

Neither function may change `items` or any array inside it.

## Examples

```
flatten([1, [2, 3], [[4]], 5])   → [1, 2, 3, 4, 5]
flatten([[], [[]], 6])           → [6]
flatten([])                      → []

depth([1, 2, 3])                 → 1
depth([])                        → 1
depth([1, [2, [3]], [4]])        → 3
depth([[], 1])                   → 2
```

## Constraints

- There are at most 10000 numbers in total, nested at most 100 levels deep.
- Don't use the built-in `flat` or `flatMap`.

## Hints

1. Look at one element of `items`. What are the only two kinds of thing it can be, and how can you tell them apart at runtime?
2. If an element is a number, what do you do with it? If it's an array, what smaller version of the whole problem do you need to solve first?
3. When a recursive call gives you back a flat array, how do you get its numbers into your result without nesting them again?
4. For `depth`: if you knew the depth of every inner array, how would you combine those answers into the depth of `items`? What's the answer when there are no inner arrays at all?

## Explain-back

- What's the base case in `flatten`? There's no `if (items.length === 0)` in many solutions. Where does the recursion actually stop?
- Trace the call stack for `flatten([1, [2, [3]]])`. What does each call return to the one that called it?
- A classmate's `flatten` does `console.log(n)` for each number instead of building a result, and it prints the right numbers. Why doesn't it pass, and what does each call need to hand back instead?
