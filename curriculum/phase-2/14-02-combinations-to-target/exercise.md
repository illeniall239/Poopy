# Combinations to a target

Topic: 14. Backtracking
Difficulty: 2 of 3

## Problem

Write `combinationsToTarget(candidates, target)` that returns every combination of numbers from `candidates` whose sum is exactly `target`.

- `candidates` holds distinct positive whole numbers, in no particular order.
- Each candidate may be used any number of times in one combination.
- Two combinations are the same if they use the same numbers the same number of times, whatever the order: `[2, 2, 3]` and `[3, 2, 2]` are one combination, so only one of them may appear.
- If no combination works, return `[]`.

The order of the combinations in the result does not matter, and neither does the order of numbers inside a combination: the tests sort both before comparing.

Do not change `candidates`.

## Examples

```
combinationsToTarget([2, 3, 6, 7], 7)  → [[2, 2, 3], [7]]
combinationsToTarget([2, 3, 5], 8)     → [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
combinationsToTarget([2], 1)           → []
```

## Constraints

- 1 ≤ `candidates.length` ≤ 30; each candidate from 1 to 200; all distinct.
- 1 ≤ `target` ≤ 500.
- The tests include `[2, 3, 5, 7, 11]` with target 60, which has 531 combinations. A search that keeps going after the running sum passes the target never ends.

## Hints

1. Draw the choice tree for `[2, 3]` and target 5. At each step, what are you choosing, and what is left of the target afterwards?
2. When the remaining target reaches 0, what do you record? When it goes below 0, is anything further down that branch worth exploring?
3. Your tree probably produces both `[2, 3]` and `[3, 2]`. What rule about which candidates a branch may still pick would stop the second one from ever being built?
4. With that rule, a branch that has just picked the candidate at position `i` may pick which positions next? Why does that still allow using the same candidate again?

## Explain-back

- How does your search avoid producing the same combination twice? What would happen if every step restarted from the first candidate?
- Where do you prune, and why can no valid combination be lost by pruning there? What would sorting the candidates first let you prune additionally?
- Why must you record a copy of the current combination, and what must happen to it after each recursive call returns?
- Roughly how does the running time grow with the target and the smallest candidate? What is the deepest the recursion can go?
