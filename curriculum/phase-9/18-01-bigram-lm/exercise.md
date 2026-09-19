# Bigram character language model

Topic: 18. Sequence modeling: n-gram LM → MLP LM → RNN, LSTM, GRU
Difficulty: 2 of 3

## Problem

The simplest language model predicts the next character from the current one, using nothing but counts. Build one with NumPy.

The vocabulary is fixed at 27 tokens: index 0 is `"."`, which marks both the start and the end of a word, and indices 1 to 26 are `"a"` to `"z"`. A word `"ab"` is read as the bigrams `(".", "a")`, `("a", "b")`, `("b", ".")`.

- `bigram_counts(words)` returns a `(27, 27)` integer array where entry `[i, j]` counts how often token `j` follows token `i` over all words. Raise `ValueError` if a word contains anything other than `a`–`z`. (The empty word contributes one `(".", ".")`.)
- `bigram_probs(counts, smoothing=0.0)` returns a `(27, 27)` float array: add `smoothing` to every count, then divide each row by its sum so it becomes a probability distribution over the next token. A row whose sum is 0 (only possible with `smoothing = 0`) stays all zeros. Raise `ValueError` if `smoothing < 0`. Do not modify `counts`.
- `sample(probs, rng, n)` generates `n` words. For each word start at token 0 and repeatedly draw the next token with exactly one call `rng.choice(27, p=probs[current])`, where `rng` is the `numpy.random.Generator` you were given; stop when the drawn token is 0 (it is not part of the word). Return the words as a `list[str]`. Never touch the global `np.random` state: the same seed must always give the same words.
- `avg_nll(words, probs)` returns the **mean** negative log-likelihood per bigram over all the words (start and end bigrams included) as a Python `float`. If any bigram has probability 0, return `math.inf` without NumPy warnings. Raise `ValueError` for an empty list of words.

## Examples

```
c = bigram_counts(["ab", "a"])
c[0, 1], c[1, 2], c[2, 0], c[1, 0]   → 2, 1, 1, 1         5 bigrams in total
p = bigram_probs(c)
p[1, 2], p[1, 0]                      → 0.5, 0.5
avg_nll(["ab", "a"], p)               → 0.2772588...       (0 + ln 2 + 0 + 0 + ln 2) / 5
avg_nll(["ba"], p)                    → inf                  ".b" was never seen
avg_nll(["ba"], bigram_probs(c, 1.0)) → finite
sample(p, np.random.default_rng(0), 3) → three words made only of "a" and "ab"
```

Perplexity is `exp(avg_nll)`: here `exp(0.277) ≈ 1.32`, as if choosing between 1.32 equally likely characters.

## Constraints

- Up to 10 000 words of up to 30 characters.
- NumPy allowed; the tests pass `np.random.default_rng(seed)`.

## Hints

1. How do you map `"."` and `"a"`–`"z"` to 0–26, and how do you turn a word into its list of consecutive pairs, including the start and end markers?
2. With a `(27, 27)` array, how do you divide every row by its own sum in one broadcast? What happens to a row that sums to 0?
3. What does "same seed, same words" rule out about which random generator you call? And how many draws does one character cost?
4. Why divide the total NLL by the number of bigrams rather than report the sum? How can you detect a zero probability before taking its log?

## Explain-back

- Why does a bigram model that never saw `"qz"` assign such a word infinite NLL, and how does smoothing fix it? What does too much smoothing do?
- What is the difference between sampling and greedy decoding (always picking the most likely next character)? What would greedy decoding produce from your model?
- Why is the mean NLL (not the sum) the number to compare across datasets of different sizes? And why can you *not* compare perplexities from models with different tokenizers?
- A bigram model only sees one character of context. What does that predict about its samples, and what does the next model in this Topic change?
