# Autocomplete

Topic: 12. Tries
Difficulty: 2 of 3

## Problem

A search box shows suggestions while the user types: the first few dictionary words, in alphabetical order, that begin with what has been typed so far. Build the class `Autocomplete` on top of a trie.

The starter defines `TrieNode`: a node holds `children`, a `Map` from one character to the child node for it, and an `isEndOfWord` flag. You decide how `Autocomplete` uses it.

- `new Autocomplete(words)` stores every word in `words`. A word that appears more than once is stored once. The array passed in must not be changed.
- `suggest(prefix, n)` returns the first `n` stored words, in alphabetical order, that begin with `prefix`.

Details of `suggest`:

- Alphabetical order is plain string comparison of lowercase letters, so a shorter word comes before every longer word that extends it: `"car"` before `"card"`.
- A stored word equal to `prefix` begins with it and comes first.
- If fewer than `n` words match, return all of them; if none match, or `n` is `0`, return `[]`.
- The empty prefix `""` matches every stored word, so `suggest("", n)` gives the first `n` words overall.
- The order words were given in does not matter.

Words are non-empty strings of lowercase letters `a`–`z`; a prefix is a possibly empty string of lowercase letters.

## Examples

```
const ac = new Autocomplete(["apple", "app", "application", "apt", "banana"]);
ac.suggest("app", 2)   → ["app", "apple"]
ac.suggest("app", 10)  → ["app", "apple", "application"]
ac.suggest("ap", 1)    → ["app"]
ac.suggest("b", 3)     → ["banana"]
ac.suggest("c", 3)     → []
ac.suggest("", 2)      → ["app", "apple"]
ac.suggest("app", 0)   → []
```

## Constraints

- Up to 100 000 words, each 1 to 20 letters; 0 ≤ `n` ≤ 100.
- Required: building the trie in O(total characters); each `suggest` in time proportional to the prefix length plus the size of the output, and not to the number of stored words.
- The large test stores 100 000 words and runs 100 000 queries (30 000 and 30 000 in Python). Filtering or sorting the whole word list on every query is too slow.

## Hints

1. Walk down the trie along the prefix, one character per step. Where are all the matching words once you arrive? What if the walk fails partway?
2. If you visit a node's children in alphabetical order, `a` before `b` before `c`, in what order do you reach the words below it? Where does a word that ends at the node itself come relative to the words below it?
3. How can you stop the traversal as soon as you have `n` words, instead of collecting every match and cutting the list afterwards?
4. Which is simpler here: children in a `Map` whose keys you sort before visiting, or an array of 26 slots indexed by letter? What does each cost per node?

## Explain-back

- Why does depth-first traversal of a trie produce words in alphabetical order? What must be true about the order you visit children in?
- What is the time complexity of `suggest` in terms of the prefix length and `n`? Why doesn't it depend on the number of stored words? Where does the cost of sorting the children of each node go?
- Sorting the whole list once and using binary search would also work. Compare the build cost and the query cost of that approach with the trie.
- How would you change the design to return the most popular matching words instead of the alphabetically first ones?
