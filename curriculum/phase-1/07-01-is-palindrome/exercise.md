# Is it a palindrome?

Topic: 7. Strings
Difficulty: 1 of 3

## Problem

A palindrome reads the same forwards and backwards. When checking sentences, people ignore capital letters, spaces and punctuation: "A man, a plan, a canal: Panama!" counts as a palindrome.

Write `isPalindrome(text)` that returns `true` if `text` is a palindrome and `false` otherwise, using these rules:

- Only the English letters `a`–`z` and `A`–`Z` count. Every other character (spaces, punctuation, digits) is ignored.
- Upper and lower case count as the same letter.
- A string with no letters at all (including `""`) is a palindrome.

## Examples

```
isPalindrome("racecar")                          → true
isPalindrome("A man, a plan, a canal: Panama!")  → true
isPalindrome("hello")                            → false
isPalindrome("Ab1a")                             → true
isPalindrome("")                                 → true
```

## Constraints

- `text` has 0 to 100000 characters.
- Letters outside `a`–`z` / `A`–`Z` (such as `é`) do not appear.

## Hints

1. By hand, what did you do to "A man, a plan..." before comparing its two ends?
2. Is it easier to compare the original text directly, or to first build a new string that contains only what matters? What goes into that new string?
3. How can you tell, for a single character, whether it is one of the letters you care about? Would comparing it against `"a"` and `"z"` help, and should you change its case before or after that comparison?
4. With the cleaned string, which two positions do you compare first, and where do the two positions meet?

## Explain-back

- Why can't you remove the punctuation by assigning to `text[i]`? What did you do instead?
- What does `"A" === "a"` give, and what would `isPalindrome("Aa")` return if your code forgot about case?
- When comparing the two ends, where does your loop stop, and what happens for a cleaned string of odd length?
