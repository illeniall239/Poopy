# Wildcard word search

Topic: 12. Tries
Difficulty: 2 of 3

## Problem

A crossword helper stores a dictionary and answers pattern queries such as `"c.t"`, where a dot stands for any single letter. Build the class `WordDictionary` on top of a trie.

The starter defines `TrieNode`: a node holds `children`, a `Map` from one character to the child node for it, and an `isEndOfWord` flag. You decide how `WordDictionary` uses it.

- `new WordDictionary()` creates an empty dictionary.
- `addWord(word)` stores `word`, a non-empty string of lowercase letters `a`–`z`. Adding the same word again changes nothing.
- `search(query)` returns `true` if some stored word matches `query`, `false` otherwise.

A stored word matches `query` when they have the same length and, at every position, the query has either the same letter or a `.`. A `.` matches exactly one letter: not zero, not several. A query with no dots matches only the identical word; a query of only dots matches any stored word of that length. On an empty dictionary every search returns `false`.

Queries are non-empty and contain only lowercase letters and dots. A query never has more than two dots.

## Examples

```
const dict = new WordDictionary();
dict.addWord("bad");
dict.addWord("dad");
dict.addWord("mad");
dict.search("pad")   → false
dict.search("bad")   → true
dict.search(".ad")   → true
dict.search("b..")   → true
dict.search("ba")    → false
dict.search("b.d.")  → false
```

## Constraints

- Up to 50 000 words, each 1 to 20 letters.
- Required: `addWord` in O(L). `search` must not depend on the number of stored words: with no dots it is O(L), and each dot may multiply the work by at most 26.
- The large test adds 50 000 words and runs 150 000 searches (20 000 and 60 000 in Python), so comparing the query against every stored word is too slow.

## Hints

1. With no dots, how is `search` different from a plain whole-word trie search? Get that case working first.
2. When the current query character is `.`, which children of the current node could continue the match? What must the rest of the query match under each of them?
3. If the first child you try under a `.` leads nowhere, what should happen next? When, and only when, may the function give up and return `false`?
4. Your search needs to know both where it is in the trie and where it is in the query. What are its base cases: the query is used up at a node with the flag set, the query is used up at a node without it, and the next letter has no child?

## Explain-back

- Why can't a plain `Set` of words answer `".a."` without looking at many words, while a trie can? What does the trie let you skip?
- What is the worst-case cost of a query with d dots and length L? Why do the constraints limit the number of dots?
- What goes wrong if the wildcard search returns after the first child that fails instead of trying the others? Give an input that shows it.
- What is the space complexity, and how do repeated `addWord` calls for the same word affect it?
