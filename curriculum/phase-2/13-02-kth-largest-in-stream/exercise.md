# K-th largest in a stream

Topic: 13. Heaps and priority queues
Difficulty: 2 of 3

## Problem

Numbers arrive one at a time and you need to keep answering "what is the k-th largest number so far?".

Build a class `KthLargest`:

- `new KthLargest(k)` starts with no numbers seen. `k` is at least 1.
- `add(value)` records `value` and returns the k-th largest of all numbers added so far, or `undefined` if fewer than `k` numbers have been added.

Duplicates count separately: after adding `5, 5, 3`, the 2nd largest is `5`. Each instance keeps its own numbers.

Each `add` must take O(log k) time, and the class must use O(k) memory no matter how many numbers arrive. In TypeScript there is no built-in heap, so write a small binary heap yourself (you may reuse your `MinHeap` from the previous Exercise). In Python you may use `heapq`, and in Java `PriorityQueue`.

## Examples

```
const tracker = new KthLargest(3);
tracker.add(4)  → undefined
tracker.add(5)  → undefined
tracker.add(8)  → 4
tracker.add(2)  → 4
tracker.add(9)  → 5
tracker.add(4)  → 5
```

## Constraints

- `k` is from 1 to 100 000; up to 200 000 calls to `add`.
- Values are whole numbers from -10⁹ to 10⁹.
- O(log k) per `add` and O(k) memory. The tests add 200 000 numbers with k = 50 000, which sorting or inserting into a sorted array on every call cannot finish in time.

## Hints

1. Out of all the numbers seen so far, which ones could ever be the answer again, now or after more numbers arrive? Which ones can you forget for good?
2. If you keep only the k largest numbers, where among those k is the answer? Is it the biggest of them or the smallest?
3. Which kind of heap gives you fast access to that particular number, a min-heap or a max-heap?
4. When a new number arrives and you already hold k numbers, what comparison with the top of your heap decides whether the new number replaces it or is thrown away?

## Explain-back

- Why does a min-heap, not a max-heap, answer "k-th largest"? What would go wrong with a max-heap holding every number?
- What is the time for each `add` and the total for n additions? What is the memory, and why doesn't it grow with n?
- Is the array inside your heap sorted? Why don't you need it to be?
- How does your class behave before k numbers have arrived, and why does it return `undefined` rather than the smallest number seen?
