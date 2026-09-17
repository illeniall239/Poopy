# Rotate in place

Topic: 2. Big-O: time and space complexity
Difficulty: 2 of 3

## Problem

Write `rotateRight(values: number[], k: number): void`. It rotates `values` to the right by `k` steps, changing the array it was given and returning nothing. One step moves the last element to the front and shifts every other element one place right.

`k` can be much larger than the array's length. Rotating an empty array does nothing.

## Examples

```
values = [1, 2, 3, 4, 5, 6, 7]; rotateRight(values, 3)   → values is [5, 6, 7, 1, 2, 3, 4]
values = [1, 2, 3];             rotateRight(values, 10)  → values is [3, 1, 2]
values = [];                    rotateRight(values, 5)   → values is []
```

## Constraints

- `values` has 0 to 1000000 integers.
- `0 <= k <= 10^9`.
- Time: O(n), no matter how large `k` is. Doing the steps one at a time is far too slow.
- Extra space: O(1). Don't build a second array of size n.

## Hints

1. Rotating `[1, 2, 3]` by 3 gives back `[1, 2, 3]`. What does that tell you about rotating by 10?
2. What goes wrong if you use `k % values.length` on an empty array?
3. Look at `[1, 2, 3, 4, 5, 6, 7]` rotated by 3. The last 3 elements end up in front, still in their original order. What happens if you reverse the whole array first, and what's still wrong afterwards?
4. After reversing the whole array, which two separate parts of it would you reverse again, and where exactly does the first part end?

## Explain-back

- Why does reversing the whole array and then the two parts produce the rotation? Show it on `[1, 2, 3, 4, 5]` with k = 2.
- What are the time and the extra space complexity of your solution? Why doesn't a large `k` make it slower?
- What would doing one step at a time `k` times cost, and why is `values.unshift(values.pop())` in a loop not O(1) per step?
- `values.splice(0, 0, ...values.splice(-k))` gives the right answer. What does it cost in time and in extra space?
