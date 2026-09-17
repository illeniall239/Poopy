# All subsets

Topic: 14. Backtracking
Difficulty: 1 of 3

## Problem

Write `subsets(nums)` that returns every subset of `nums`, an array of distinct whole numbers. A subset is any selection of the numbers, including the empty selection and the whole array.

Each subset must appear exactly once. The order of the subsets in the result does not matter, and neither does the order of the numbers inside a subset: the tests sort both before comparing. `[1, 2]` and `[2, 1]` are the same subset, so only one of them may appear.

Do not change `nums`.

## Examples

```
subsets([1, 2, 3])  → [[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]   (any order)
subsets([])         → [[]]
subsets([5])        → [[], [5]]
```

## Constraints

- 0 ≤ `nums.length` ≤ 16; all numbers distinct, from -100 to 100.
- The result has 2ⁿ subsets, so O(n · 2ⁿ) time is expected. The tests ask for all 65 536 subsets of 16 numbers.

## Hints

1. For the first number in `nums`, what are the only two choices a subset can make about it? Draw the tree of choices for `[1, 2]`.
2. How many leaves does that tree have for n numbers? What does the path from the root to one leaf describe?
3. If you build the current subset in one shared array, adding a number before exploring and removing it afterwards, what must you store when you reach a leaf so later changes don't affect it?
4. After exploring "with this number", what state must the shared array be in before you explore "without this number"?

## Explain-back

- Why is the time O(n · 2ⁿ) and not just O(2ⁿ)? How much memory do the recursion stack and the result use?
- What would every subset in your result look like if you stored the shared array itself instead of a copy? Why?
- What breaks if you forget to remove the number after exploring the branch that includes it?
- How does your approach make sure `[1, 2]` and `[2, 1]` are never both produced?
