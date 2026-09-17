# Word frequency

Topic: 8. Objects, Map and Set
Difficulty: 1 of 3

## Problem

Write `wordFrequency(text)` that counts how often each word appears in `text` and returns a `Map` from word to count.

- A word is a run of one or more English letters (`a`–`z`, `A`–`Z`) back to back. Every other character (spaces, punctuation, digits, apostrophes) separates words.
- Counting is case-insensitive. Keys in the map are lowercase.
- The map's entries are in the order each word first appears in `text`.
- Text with no words returns an empty `Map`.

## Examples

```
wordFrequency("the cat and the hat")
  → Map { "the" → 2, "cat" → 1, "and" → 1, "hat" → 1 }

wordFrequency("Hi, hi! HI?")
  → Map { "hi" → 3 }

wordFrequency("...")
  → Map {}
```

## Constraints

- `text` has 0 to 100000 characters.
- `text` contains no letters outside `a`–`z` / `A`–`Z`.

## Hints

1. Count the words in `"Hi, hi! HI?"` by hand. What did you do with the commas and question mark, and with the capitals?
2. As you walk through the characters, how do you know a word has just ended? What should happen to the word you were building at that moment?
3. When you finish a word, how do you add one to its count if it might or might not be in the map yet?
4. Does a word that runs right up to the end of the text get counted by your plan? Check it on `"the cat"`.

## Explain-back

- Why is a `Map` a better fit here than a plain object? Think about a word like `"constructor"` or `"toString"`.
- What order do your entries come out in, and what guarantees that order?
- Where does the case-insensitivity happen in your code, and what would the result be for `"The the"` if it didn't?
