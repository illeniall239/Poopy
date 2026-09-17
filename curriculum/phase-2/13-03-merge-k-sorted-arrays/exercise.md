# Merge k sorted arrays

Topic: 13. Heaps and priority queues
Difficulty: 3 of 3

## Problem

Write `mergeKSorted(arrays)` that takes an array of k arrays, each already sorted in ascending order, and returns one new array holding every value from all of them in ascending order. Duplicates are kept. Some inner arrays may be empty, and `arrays` itself may be empty.

Do not change the input arrays.

The merge must run in O(N log k) time, where N is the total number of values, using a heap that holds at most one value per input array. In TypeScript there is no built-in heap, so write a small binary heap yourself. In Python you may use `heapq` (but not `heapq.merge`), and in Java `PriorityQueue`.

## Examples

```
mergeKSorted([[1, 4, 7], [2, 5, 8], [3, 6, 9]])  → [1, 2, 3, 4, 5, 6, 7, 8, 9]
mergeKSorted([[], [1, 1, 3], [], [1, 2]])        → [1, 1, 1, 2, 3]
mergeKSorted([])                                 → []
```

## Constraints

- 0 ≤ k ≤ 10 000; N up to 200 000.
- Values are whole numbers from -10⁹ to 10⁹.
- O(N log k) time, O(k) extra space besides the output. The tests merge 10 000 arrays (5 000 in Python), where checking every array's front value to find the smallest takes too long.

## Hints

1. At any moment, which values are the only candidates for the next value of the output? How many candidates are there?
2. Looking through all k candidates each time costs O(k) per output value. Which data structure hands you the smallest of a changing group faster?
3. When you take the smallest candidate out, how do you know which array it came from and which value from that array should replace it? What must each heap entry remember?
4. When an array has no values left, what do you push in its place? How does the loop know it is finished?

## Explain-back

- Why is your merge O(N log k) and not O(N log N)? When k equals N, what does it become?
- Why is the heap never larger than k, and what extra space does your solution use?
- Concatenating everything and sorting is also correct. When is it slower, and what fact about the input does it ignore?
- How does your heap compare two entries when their values are equal, and does it matter for the output?
