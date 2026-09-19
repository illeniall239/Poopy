# Embedding lookup equals one-hot matmul

Topic: 17. Embeddings
Difficulty: 1 of 3

## Problem

An embedding layer is a table of shape `(vocab_size, dim)`: row `i` is the vector for token `i`. Looking a token up is the same as multiplying its one-hot vector by the table, just without building the one-hot. Write it in PyTorch.

`embed(indices, table)` takes an integer tensor `indices` of any shape (`torch.long`) and a float tensor `table` of shape `(V, D)`, and returns a tensor of shape `indices.shape + (D,)` whose entry at position `p` is `table[indices[p]]`.

- Every index must satisfy `0 <= index < V`; raise `ValueError` otherwise. (Plain tensor indexing would silently accept `-1` and hand back the last row.)
- The result must stay connected to `table` in the autograd graph, so that `loss.backward()` fills `table.grad`.
- Do not use `torch.nn.Embedding`, `torch.nn.functional.embedding` or `torch.nn.functional.one_hot`: the point is to see that a lookup is just indexing. Tensor indexing (`table[...]`) and `torch.index_select` are allowed.

## Examples

```
table = torch.tensor([[1., 2.], [3., 4.], [5., 6.]])
embed(torch.tensor([2, 0]), table)            → tensor([[5., 6.], [1., 2.]])
embed(torch.tensor([[1, 1], [0, 2]]), table)  → shape (2, 2, 2)
embed(torch.tensor([], dtype=torch.long), table) → shape (0, 2)
embed(torch.tensor([3]), table)               → ValueError
embed(torch.tensor([-1]), table)              → ValueError

The test also checks: embed(idx, table) == F.one_hot(idx, V).float() @ table
```

## Constraints

- `V` and `D` are at most 1000; `indices` has at most 10 000 entries.
- PyTorch on CPU.

## Hints

1. Write the one-hot vector for token 1 in a vocabulary of 3. Multiply it by a 3 × 2 table by hand: which row comes out?
2. What does indexing a 2-D tensor with a tensor of row numbers return, and what shape does it have when the index tensor is itself 2-D?
3. How do you check the smallest and largest index in one go before you look anything up? What about an empty `indices`?
4. Does indexing a tensor that has `requires_grad=True` keep the result in the graph, or do you need to do something extra?

## Explain-back

- Nobody wrote the numbers in an embedding table by hand. Where do they come from, and why is the lookup-equals-matmul view the reason ordinary backprop can train them?
- Why is the lookup preferred over the one-hot matmul in practice, even though they give the same result?
- Someone finds that dimension 7 of a trained embedding is large for animal words. Should they call it "the animal dimension"? What would happen to that reading if you rotated the whole table?
- If the same token appears three times in a batch, how many rows of `table.grad` receive a gradient from it, and what happens to the three contributions?
