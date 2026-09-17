# Min-heap

Topic: 13. Heaps and priority queues
Difficulty: 1 of 3

## Problem

Build a class `MinHeap` that stores numbers and always gives back the smallest one first. Store the values in a plain array laid out as a complete binary tree: the children of index `i` are at `2i + 1` and `2i + 2`, and its parent is at `Math.floor((i - 1) / 2)`.

Write the heap yourself. Do not sort the array and do not use a library heap (in Python that means no `heapq`, in Java no `PriorityQueue`).

- `new MinHeap(values?)` creates a heap. If an array of starting values is given, the heap holds all of them. The array passed in must not be changed.
- `push(value)` adds a value. O(log n).
- `pop()` removes and returns the smallest value, or `undefined` if the heap is empty. O(log n).
- `peek()` returns the smallest value without removing it, or `undefined` if the heap is empty. O(1).
- `size()` returns how many values the heap holds. O(1).

Duplicate values are allowed and each copy counts separately.

## Examples

```
const heap = new MinHeap();
heap.push(5); heap.push(3); heap.push(8);
heap.peek()  → 3
heap.size()  → 3
heap.pop()   → 3
heap.pop()   → 5
heap.pop()   → 8
heap.pop()   → undefined

new MinHeap([9, 4, 7, 1]).pop()  → 1
```

## Constraints

- Up to 200 000 values, each a whole number from -10⁹ to 10⁹.
- `push` and `pop` must be O(log n); `peek` and `size` O(1). The tests push 200 000 values and pop them all, which a heap that sorts on every push or scans on every pop cannot finish in time.

## Hints

1. Draw the array `[1, 3, 2, 7, 4]` as a tree using the index rules. What is true about every parent compared with its children?
2. After you put a new value at the end of the array, which single parent–child relationship might now be broken? Which direction should the value travel to fix it, and when does it stop?
3. To remove the root without leaving a hole in the middle of the array, which element could take its place? After that move, which relationships might be broken?
4. When a value moving down is bigger than both of its children, which child must it swap with so the rule still holds for the other child? What goes wrong if you pick the other one?

## Explain-back

- Is the array inside your heap sorted? Give a small heap whose array is not sorted and explain why that is fine.
- Why are `push` and `pop` O(log n)? What is the height of a complete binary tree with n nodes, and how much extra space does the heap use?
- In `pop`, why do you move the last element to the root instead of shifting everything left by one?
- How would you turn your class into a max-heap without rewriting the sift logic?
