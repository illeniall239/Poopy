# Embedding gradient

Topic: 17. Embeddings
Difficulty: 2 of 3

## Problem

In the forward pass an embedding layer copies rows out of its table: `out[p] = table[indices[p]]`. In the backward pass each upstream gradient `dout[p]` flows back to the row it came from. When a token appears more than once, its row was used more than once, so its gradient is the **sum** of all those contributions. Write that backward pass with NumPy.

`embedding_grad(indices, dout, vocab_size, dim)` takes:

- `indices`: an integer array of any shape (for example `(batch, block)`),
- `dout`: a float array of shape `indices.shape + (dim,)`, the gradient of the loss with respect to the embedding output,
- `vocab_size` and `dim`: the table's shape.

It returns a float array of shape `(vocab_size, dim)`: the gradient of the loss with respect to the table. Rows of tokens that never appear are zero.

Raise `ValueError` if `dout.shape != indices.shape + (dim,)` or if any index is outside `0 … vocab_size − 1`.

## Examples

```
embedding_grad(np.array([0, 2]), np.array([[1., 1.], [2., 3.]]), 3, 2)
    → [[1., 1.], [0., 0.], [2., 3.]]

embedding_grad(np.array([1, 1, 1]), np.array([[1., 0.], [2., 0.], [3., 5.]]), 2, 2)
    → [[0., 0.], [6., 5.]]          token 1 used three times: the three rows add up

embedding_grad(np.array([[0, 1], [1, 0]]), np.ones((2, 2, 4)), 2, 4)
    → [[2., 2., 2., 2.], [2., 2., 2., 2.]]
```

## Constraints

- Up to 100 000 indices, `vocab_size` up to 10 000, `dim` up to 512.
- NumPy allowed; no torch. Avoid a Python loop over the indices.

## Hints

1. For a single index `i`, which row of the table did `out[p]` depend on, and with what derivative?
2. Reshape the problem: can you flatten `indices` to 1-D and `dout` to `(N, dim)` without losing the pairing between them?
3. Try `grad[idx] += dout` on an `idx` with a repeated entry. What does NumPy actually do with the repeated row?
4. Which NumPy function performs an *unbuffered* in-place add, so that every repeated index is applied?

## Explain-back

- Why must a repeated index sum its gradients rather than keep the last one? Tie your answer to the one-hot matmul view of the lookup.
- How does the gradient of a whole `(V, D)` table look when a batch only touches 5 of the 10 000 tokens? What does that suggest about optimizers for large embedding tables?
- A rare token appears once every thousand batches. What does that mean for how well its row is learned?
- Is the embedding table updated by some special rule, or by the same gradient descent as every other weight?
