# Most similar words

Topic: 17. Embeddings
Difficulty: 2 of 3

## Problem

Nearest-neighbour search is the everyday use of an embedding table. Write it with NumPy.

`most_similar(word, table, vocab, k)` takes a query word, a float array `table` of shape `(V, D)` whose row `i` embeds `vocab[i]`, the list `vocab` of `V` distinct words, and a count `k`. It returns a `list` of up to `k` tuples `(other_word, similarity)`, where `similarity` is the Python `float` **cosine similarity** between the query's row and the other word's row:

```
cos(a, b) = (a · b) / (‖a‖ ‖b‖)
```

- The query word itself is never in the result.
- The list is sorted by similarity, highest first. Ties keep vocabulary order (the word that appears earlier in `vocab` comes first).
- If `k` is larger than the number of other words, return all of them. `k = 0` returns `[]`.
- Raise `ValueError` if `word` is not in `vocab`, if `k < 0`, or if `len(vocab) != table.shape[0]`.
- Use cosine, not the raw dot product: a row with a large norm must not win just because it is long. You may assume no row is all zeros.

## Examples

```
vocab = ["cat", "dog", "car", "kitten"]
table = [[1.0, 0.1], [0.9, 0.3], [0.0, 1.0], [10.0, 1.2]]

most_similar("cat", table, vocab, 2)  → [("kitten", 0.99998...), ("dog", 0.9981...)]
most_similar("car", table, vocab, 1)  → [("dog", 0.3162...)]
most_similar("cat", table, vocab, 10) → all three other words, sorted
most_similar("cow", table, vocab, 1)  → ValueError
```

The raw dot product would rank `kitten` first for `car` too, only because its row is ten times longer.

## Constraints

- `V` up to 10 000, `D` up to 300. Vectorize: one matrix-vector product, not a Python loop over `V` rows computing norms.
- NumPy allowed.

## Hints

1. What does dividing every row by its own length do to the dot products between rows?
2. After normalizing, how do you get the similarity of the query to *every* row in one operation?
3. How do you make sure the query never shows up in its own result, even when another word has the exact same vector?
4. Which NumPy sort keeps equal elements in their original order, and how do you sort descending without breaking that?

## Explain-back

- Why does cosine similarity ignore the length of the vectors, and why is that usually what you want for embeddings?
- "king − man + woman ≈ queen" is the famous example. Is that analogy typical of what embedding arithmetic gives you, or a hand-picked success? How would you check?
- Your nearest neighbours come from a table learned by predicting context. Why do words that appear in similar contexts end up close together?
- The same search works for users and items in a recommender. What are the "words" and the "context" there?
