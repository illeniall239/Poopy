# Group by

Topic: 11. Generics and utility types
Difficulty: 2 of 3

## Problem

Write `groupBy<T>(items: T[], keyOf: (item: T) => string): Record<string, T[]>`.

It calls `keyOf` on every item and returns an object whose keys are the returned strings. Each key maps to an array of the items that produced it, in the same order they appear in `items`. An empty array returns `{}`.

`groupBy` must work for any item type, and the caller must get their item type back in the arrays. Don't use `any`, and don't change the input array.

## Examples

```
groupBy([1, 2, 3, 4, 5], (n) => (n % 2 === 0 ? "even" : "odd"))
  → { odd: [1, 3, 5], even: [2, 4] }

groupBy(
  [{ name: "Ana", team: "red" }, { name: "Bo", team: "blue" }, { name: "Cy", team: "red" }],
  (p) => p.team,
)
  → { red: [{ name: "Ana", team: "red" }, { name: "Cy", team: "red" }],
      blue: [{ name: "Bo", team: "blue" }] }

groupBy([], (s: string) => s)   → {}
```

## Constraints

- `items` has 0 to 10000 elements.
- Inside the `keyOf` you pass for the people example, your editor must know `p` has `name` and `team` without you annotating `p`.

## Hints

1. You wrote a word counter in Topic 8. What was the same about it, and what's different now that the key comes from a function?
2. When the result doesn't have a key yet, what has to happen before you can push an item into its array?
3. How does TypeScript know what `p` is inside `(p) => p.team`? Which part of your function signature tells it?
4. What is `Record<string, T[]>` short for, written out as an object type?

## Explain-back

- Why does the arrow function's `p` get the right type without an annotation? Walk through how `T` is worked out from the call.
- Why do the grouped arrays hold the original item objects rather than copies, and when could that surprise someone?
- What would the caller lose if `groupBy` returned `Record<string, unknown[]>` instead?
