# Dynamic array

Topic: 3. Classes for building data structures
Difficulty: 2 of 3

## Problem

A JavaScript array grows when you `push`, but underneath, memory is handed out in fixed-size blocks. Build that growth yourself.

Write a generic class `DynamicArray<T>` that stores its elements in a private fixed-capacity array. You may create storage with `new Array(capacity)` and read or write its slots by index, but never call `push`, `pop`, `splice` or change `length` on it.

- `constructor()` starts empty with capacity 1.
- `size()` returns how many elements are stored.
- `capacity()` returns how many elements fit in the current storage.
- `push(value)` adds `value` at the end. If the storage is full, first replace it with storage of **double** the capacity and copy the elements across. Amortized O(1).
- `get(index)` returns the element at `index`. O(1).
- `set(index, value)` replaces the element at `index`. O(1).
- `pop()` removes and returns the last element. Capacity never shrinks. O(1).
- `toArray()` returns a new plain array of the elements in order, with length `size()`. Changing that array must not change the `DynamicArray`.

`get`, `set` and `pop` throw a `RangeError` when there is no such element: `index < 0`, `index >= size()` (even if it is below the capacity), or `pop()` on an empty array.

## Examples

```
const a = new DynamicArray<string>();
a.size(), a.capacity()     → 0, 1
a.push("x"); a.push("y"); a.push("z");
a.size(), a.capacity()     → 3, 4
a.get(1)                   → "y"
a.get(3)                   → throws RangeError
a.pop()                    → "z"
a.toArray()                → ["x", "y"]
```

## Constraints

- Up to 1000000 calls in total.
- `push` must be amortized O(1): pushing 1000000 elements has to finish in well under a second.

## Hints

1. After how many pushes does the storage fill up for the first few times, starting at capacity 1? How many element copies does each of those growths make?
2. Your class has two numbers that sound alike: the size and the capacity. Which one decides whether `get(index)` is allowed, and which one decides when to grow?
3. If a caller could get hold of your private storage array, what could they break? How does `toArray` avoid handing it out?
4. Add up all the copies made while pushing 16 elements with doubling. How does that total compare to 16? What would it be if the capacity grew by 1 each time?

## Explain-back

- What invariants does your class keep true after every method (think about `size`, `capacity` and which slots hold elements)?
- Why is `push` amortized O(1) with doubling, but O(n) per push on average if capacity grows by a fixed amount? What is the worst single `push`?
- What are the time and space complexity of `get`, `pop` and `toArray`, and how much unused space can the storage hold at worst?
- If someone writes `const add = arr.push; add(5);`, what goes wrong and why? How could they call it safely?
