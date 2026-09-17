# Hash map with chaining

Topic: 3. Classes for building data structures
Difficulty: 3 of 3

## Problem

Build the idea behind `Map` yourself. Write a generic class `StringHashMap<V>` that maps string keys to values of type `V`.

Store entries in an array of buckets. A key's bucket index comes from a hash function you write that uses **every character** of the key, reduced to the range `0` to `bucketCount() - 1`. Keys that land in the same bucket share it as a list of `[key, value]` entries (chaining). Don't use `Map`, `Set` or a plain object as a dictionary anywhere in the class.

- `constructor()` starts empty with 8 buckets.
- `set(key, value)` stores `value` under `key`, replacing any value already there. If this added a new key and now `size() / bucketCount() > 0.75`, double the number of buckets and move every entry to its bucket in the new array.
- `get(key)` returns the value stored under `key`, or `undefined` if there is none.
- `has(key)` returns whether `key` is stored, even when its value is `undefined`, `0` or `""`.
- `delete(key)` removes `key` and returns `true`, or returns `false` if it wasn't stored. The bucket count never shrinks.
- `size()` returns the number of stored keys.
- `bucketCount()` returns the current number of buckets.

`set`, `get`, `has` and `delete` must be O(1) on average.

## Examples

```
const m = new StringHashMap<number>();
m.set("ab", 1); m.set("ba", 2); m.set("ab", 3);
m.get("ab"), m.get("ba"), m.get("zz")   → 3, 2, undefined
m.size(), m.bucketCount()               → 2, 8
m.delete("ab"), m.delete("ab")          → true, false
// after 7 different keys are stored:
m.bucketCount()                         → 16
```

## Constraints

- Up to 1000000 operations; keys are 0 to 20 characters long.
- Storing 200000 keys like `"key0"`, `"key1"`, ... and reading them back must take well under a second. A hash that looks at only some characters, or a map that never grows, can't manage that.

## Hints

1. With 8 buckets and a number from your hash function, how do you choose a bucket? What happens to two keys whose hashes give the same bucket?
2. `"ab"` and `"ba"` contain the same characters. Would a hash that adds up character codes tell them apart? Does it need to for your map to be correct, or only to be fast?
3. When you double the bucket count, does an entry stay at the same index? What must happen to every entry already stored?
4. `set` on a key that's already stored: should that count towards the load factor? Where in `set` do you check whether to grow?

## Explain-back

- Why are `get` and `set` O(1) on average but O(n) in the worst case? Describe inputs that cause the worst case.
- Why does doubling the bucket count keep `set` amortized O(1), and what is the cost of one resize?
- What would go wrong if resizing created the new bucket array but left entries at their old indices?
- What invariants does your class keep true, and how does keeping the buckets private protect them?
