# Balanced brackets

Topic: 7. Stacks and queues
Difficulty: 1 of 3

## Problem

A code editor highlights a line red when its brackets don't match up.

Write `isBalanced(s: string): boolean`. It returns `true` when every bracket in `s` is correctly matched and nested, and `false` otherwise.

- The bracket pairs are `()`, `[]` and `{}`.
- Every opening bracket must be closed by the same kind of bracket, and an inner pair must close before the pair around it closes: `([])` is balanced, `([)]` is not.
- A closing bracket with nothing open before it makes the string unbalanced, and so does an opening bracket that is never closed.
- Every other character (letters, digits, spaces, punctuation) is ignored.
- A string with no brackets at all, including `""`, is balanced.

## Examples

```
isBalanced("()[]{}")           → true
isBalanced("{[()]}")           → true
isBalanced("(]")               → false
isBalanced("([)]")             → false
isBalanced("((")               → false
isBalanced("())")              → false
isBalanced("f(a[0]) { x; }")   → true
```

## Constraints

- `s` has 0 to 400000 characters.
- Required: O(n) time. O(n) extra space is fine.
- The large test nests brackets 200000 levels deep, so repeatedly deleting `"()"` pairs from the string is too slow, and recursion overflows the call stack.

## Hints

1. Read `{[()]}` left to right. When you reach the first `)`, which opening bracket must it match: the first one you saw, or the most recent one that is still open?
2. Which structure hands back the most recently added item first? What should happen to an opening bracket when you meet it?
3. When you meet a closing bracket, there are two different ways it can be wrong. What are they?
4. When you reach the end of the string without finding a mistake, is that enough to return `true`? What else must you check?

## Explain-back

- Why is a stack the right structure here and not a queue? Use `([)]` to show what goes wrong with first-in-first-out.
- What does your code do for `")"` and for `"(("`? Point to the line that handles each one.
- What are the time and space complexity of your solution? Which input makes the stack as large as possible?
- Why is "delete every `()`, `[]` and `{}` until nothing changes" O(n²) in the worst case?
