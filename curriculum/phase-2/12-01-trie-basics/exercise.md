# Trie basics

Topic: 12. Tries
Difficulty: 1 of 3

## Problem

A spell checker keeps a growing dictionary and must answer two questions fast: "is this exact word in it?" and "does any word start with these letters?" Build the dictionary as a trie: a tree with one node per character, where words that share a beginning share the nodes for it.

The starter defines `TrieNode`: a node holds `children`, a `Map` from one character to the child node for it, and an `isEndOfWord` flag. You decide how `Trie` uses it.

Write the class `Trie`:

- `new Trie()` creates an empty trie.
- `insert(word)` stores `word`. Inserting the same word again changes nothing.
- `search(word)` returns `true` if exactly `word` was inserted, `false` otherwise. The beginning of a stored word is not itself a word unless it was inserted too.
- `startsWith(prefix)` returns `true` if at least one inserted word begins with `prefix`. A stored word counts as beginning with itself.

Words and prefixes are non-empty strings of lowercase letters `a`–`z`. On an empty trie both `search` and `startsWith` return `false`.

## Examples

```
const trie = new Trie();
trie.insert("apple");
trie.search("apple")      → true
trie.search("app")        → false
trie.startsWith("app")    → true
trie.insert("app");
trie.search("app")        → true
trie.startsWith("apples") → false
```

## Constraints

- Up to 50 000 inserts, each word 1 to 20 letters.
- Required: `insert`, `search` and `startsWith` each O(L), where L is the length of the string passed in, no matter how many words are stored.
- The large test inserts 50 000 words and runs 100 000 queries (20 000 and 40 000 in Python), so scanning every stored word per query is too slow.

## Hints

1. Draw the words "car", "cart" and "cat" as one tree of letters. How many nodes hold a "c"? At which node do "cart" and "cat" go separate ways?
2. When you walk "car" and stop at its last node, how can you tell whether "car" was stored or is only the beginning of "cart"?
3. `search` and `startsWith` walk the same path. What is the single difference at the end of the walk? Could one helper serve both?
4. In `insert`, what do you do when the current node has no child for the next letter? And when it already has one?

## Explain-back

- Why does `startsWith("ca")` cost the same whether 3 or 3 million words are stored? What does the cost depend on?
- What goes wrong if you drop the end-of-word flag and treat "the path exists" as "the word exists"? Give an input that shows it.
- What is the space complexity in terms of the total number of characters inserted? When is it much less than that, and when would a plain `Set` of words be the better choice?
- What are the time complexities of the three operations?
