# Sort by several keys

Topic: 10. Sorting
Difficulty: 1 of 3

## Problem

A leaderboard lists players as records:

```ts
type Player = { id: number; name: string; score: number };
```

Write `sortBySeveralKeys(players: Player[]): Player[]`. Return a new array holding the same player objects ordered by:

1. `score`, highest first;
2. among equal scores, `name` in ascending order, comparing character codes (`"Bob" < "alice"` because `"B"` comes before `"a"`; don't use locale-aware comparison);
3. among equal scores and names, the original order of `players`.

Use the built-in sort with a comparator; don't write your own sorting algorithm. Don't change the order of `players`. An empty array gives an empty array.

## Examples

```
sortBySeveralKeys([
  { id: 1, name: "cara", score: 50 },
  { id: 2, name: "alex", score: 80 },
  { id: 3, name: "bea",  score: 50 },
])
→ ids in order: [2, 3, 1]                       80 first; then "bea" before "cara"

sortBySeveralKeys([
  { id: 1, name: "sam", score: 10 },
  { id: 2, name: "sam", score: 10 },
])
→ ids in order: [1, 2]                          fully equal keys keep their input order

sortBySeveralKeys([])  → []
```

## Constraints

- `players` has 0 to 400000 records; `score` is an integer between -10^9 and 10^9; `name` is a non-empty string.
- Time: O(n log n). The large test has 200000 records, so an O(n²) sort is far too slow.
- Extra space: O(n) for the copy.

## Hints

1. A comparator returns a negative number, zero or a positive number. For "highest score first", what should `compare(a, b)` return when `a.score > b.score`?
2. When the scores are equal, what should the comparator look at next? What must it return when the names are equal too?
3. Compare `"Bob"` with `"alice"` using `<` and using `localeCompare`. Which one does the problem ask for, and what about `a.score - b.score` when scores could be huge negatives in another language?
4. How do you get a new sorted array without reordering the one you were given? What happens to the tied records after the built-in sort, and why?

## Explain-back

- Why is `(a, b) => b.score - a.score` correct for descending scores, and what would `(a, b) => a.score > b.score` (returning a boolean) do instead?
- Why do fully tied players keep their input order without you writing any code for it? Which property of the built-in sort guarantees this?
- What are the time and space complexity of your solution?
- If you first sorted by name ascending and then re-sorted the result by score descending with two separate calls, would that give the same order? Why does that trick depend on stability?
