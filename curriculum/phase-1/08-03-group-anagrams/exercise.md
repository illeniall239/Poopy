# Group anagrams

Topic: 8. Objects, Map and Set
Difficulty: 3 of 3

## Problem

Two words are anagrams if they use exactly the same letters the same number of times, in any order: `"listen"` and `"silent"` are anagrams; `"aab"` and `"abb"` are not.

Write `groupAnagrams(words)` that returns an array of groups, where each group is an array of words that are anagrams of each other.

- Groups appear in the order their first word appears in `words`.
- Inside a group, words keep their order from `words`.
- Duplicate words are kept (each copy goes into the same group).
- An empty input returns `[]`.
- Do not change the input array.

## Examples

```
groupAnagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
  → [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]

groupAnagrams(["ab", "abc", "ba"])
  → [["ab", "ba"], ["abc"]]

groupAnagrams([])
  → []
```

## Constraints

- `words` has 0 to 10000 elements.
- Each word has 1 to 20 characters, all lowercase letters `a`–`z`.

## Hints

1. Group the first example by hand. How did you decide that `"tea"` belongs with `"eat"` without comparing it to every other word?
2. Could you turn each word into a "signature" so that all anagrams produce the same signature and non-anagrams don't? What could that signature be?
3. Once you have a signature, which structure lets you jump straight from the signature to the group it belongs to?
4. Why wouldn't two separate arrays like `["e","a","t"]` work as that lookup key, while a string would? And what does the structure you chose promise about the order of its entries?

## Explain-back

- What signature did you use, and why do `"aab"` and `"abb"` get different ones?
- Why can't an array be used as a `Map` key to find an existing group? What does `["a"] === ["a"]` give?
- How does your code produce the groups in the required order without any sorting of the groups?
