# LRU cache

Topic: 9. Linked lists
Difficulty: 3 of 3

## Problem

An image viewer keeps recently opened thumbnails in memory, but only up to a fixed number of them. When it's full and a new thumbnail arrives, it throws away the one that was used least recently.

Write a class `LRUCache` with:

- `constructor(capacity: number)`: an empty cache that holds at most `capacity` entries.
- `get(key: number): number`: if `key` is in the cache, returns its value and marks the entry as the most recently used. Otherwise returns `-1` and changes nothing.
- `put(key: number, value: number): void`:
  - If `key` is already in the cache, replaces its value and marks it as the most recently used. Nothing is evicted.
  - Otherwise, if the cache already holds `capacity` entries, first removes the least recently used entry, then adds the new entry as the most recently used.

"Used" means a successful `get` or any `put` of that key. A `get` for a missing key doesn't count as using anything.

Build it from a `Map` from key to node plus your own doubly linked list of nodes ordered by recency. Don't rely on `Map` keeping insertion order, and don't search or reorder an array of keys.

## Examples

```
const cache = new LRUCache(2);
cache.put(1, 100);
cache.put(2, 200);
cache.get(1)       → 100   (1 is now the most recently used)
cache.put(3, 300);         (full: evicts 2, the least recently used)
cache.get(2)       → -1
cache.put(1, 111);         (updates 1, evicts nothing)
cache.put(4, 400);         (full: evicts 3)
cache.get(3)       → -1
cache.get(1)       → 111
cache.get(4)       → 400
```

## Constraints

- `capacity` is from 1 to 100000.
- Keys are whole numbers from 0 to 1000000000; values are whole numbers from 0 to 1000000000, so `-1` always means "missing".
- Up to 1000000 calls to `get` and `put`.
- Required: `get` and `put` are both O(1) on average; the cache uses O(capacity) space.
- The large test fills a cache of 100000 entries and then makes 500000 calls, so any operation that scans all entries is too slow.

## Hints

1. Which operations must be O(1)? For each one, which structure can find the entry instantly, and which structure can keep entries in order of use?
2. If each linked-list node knows both its previous and next node, what do you need to do to cut a node out of the middle of the list? How many pointers change?
3. Where do the most recently used and least recently used entries live in your list? What does "mark as most recently used" become in list operations?
4. A dummy head node and a dummy tail node that are never removed mean every real node always has a neighbour on both sides. Which `if` checks does that remove? When you evict, what else besides the list must you update?

## Explain-back

- Why does the linked list need `prev` pointers? What would removing a node cost in a singly linked list?
- Why does each node store its key as well as its value? Point to the line that needs it.
- What are the time complexity of `get` and `put`, and the space complexity of the cache? Why would an array of keys in use order make them O(capacity)?
- Walk through `put` on a key that's already present. Which pointers change, and why is nothing evicted?
