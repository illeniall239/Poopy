# Character-level MLP language model

Topic: 19. Capstone: a tiny CNN and a character-level LM from scratch
Difficulty: 3 of 3

## Problem

Build the Bengio-style language model from makemore: look up an embedding for each of the last `block` characters, concatenate them, pass them through one `tanh` hidden layer, and predict the next character. Use PyTorch, and write the training loop yourself.

The vocabulary is the same 27 tokens as the bigram model: index 0 is `"."` (start and end of a word), indices 1 to 26 are `"a"` to `"z"`.

- `make_dataset(words, block)` returns `(X, Y)`: for every word, start with a context of `block` zeros; for each character of the word followed by the end marker `"."`, append the current context to `X` and that character's index to `Y`, then slide the context left by one and put the character at its end. `X` is a `torch.long` tensor of shape `(N, block)` and `Y` a `torch.long` tensor of shape `(N,)`, where `N` is the total number of characters plus one per word. Raise `ValueError` if a word contains anything other than `a`–`z`.
- `CharMLP(vocab, block, dim, hidden)` is an `nn.Module` with exactly these learnable parts:
  - one `nn.Embedding(vocab, dim)` table, shared by all `block` positions,
  - a `nn.Linear(block * dim, hidden)` followed by `tanh`, where the input row is the `block` embeddings concatenated in context order (oldest character first),
  - a `nn.Linear(hidden, vocab)` producing the logits.

  `forward(x)` takes a `(B, block)` long tensor and returns `(B, vocab)` logits (no softmax).
- `train_lm(model, X, Y, steps, lr)` trains `model` in place with `torch.optim.Adam(model.parameters(), lr=lr)` for `steps` full-batch steps (every step uses all of `X`) on `F.cross_entropy(model(X), Y)`, and returns the list of the `steps` loss values as Python floats, each recorded at its step *before* the update. It must not reseed or create any randomness itself: the caller controls the seed.

The test seeds with `torch.manual_seed`, builds `CharMLP(27, 3, 8, 64)` on 8 short names, and requires the first loss to be near `ln 27 ≈ 3.30` and the loss after 200 steps at `lr = 0.01` to fall below 0.6.

## Examples

```
make_dataset(["ab"], 2)
  → X = [[0, 0], [0, 1], [1, 2]]      contexts "..", ".a", "ab"
    Y = [1, 2, 0]                      next chars  a,   b,   .

model = CharMLP(27, 3, 8, 64)
model(torch.zeros(5, 3, dtype=torch.long)).shape      → (5, 27)
sum(p.numel() for p in model.parameters())            → 3571   27·8 + (24·64 + 64) + (64·27 + 27)

torch.manual_seed(0); losses = train_lm(model, X, Y, 200, 0.01)
losses[0] ≈ 3.3,  losses[-1] < 0.6
```

## Constraints

- Words are at most 12 characters; the test data has under 100 examples, so full-batch training is fast.
- PyTorch on CPU. `nn.Embedding`, `nn.Linear`, `F.cross_entropy` and `torch.optim.Adam` are allowed.

## Hints

1. For the word `"ab"` with `block = 2`, write every (context, next character) pair by hand. How many are there, and why does the last target have to be `"."`?
2. The embedding lookup turns a `(B, block)` tensor into `(B, block, dim)`. What shape does the first `Linear` expect, and which tensor method gets you there?
3. Your first loss is about 3.3. Why is `ln 27` the loss you should expect before training, and what would a first loss of 20 tell you about the init?
4. In your loop, in which order do you compute the loss, zero the gradients, call `backward()` and `step()`, and at which point do you record the loss?

## Explain-back

- The same embedding table serves all three context positions. What would change (parameters, generalization) if each position had its own table?
- Your final training loss is about 0.35. Is that the number to report as how good the model is? What would you measure instead?
- Why can this model never do better than 0.35 on this data, however long you train? (Look at the contexts that start a word.)
- The samples from a trained model start to look like names. Does the model "understand" names? What is the most it can know about a character more than `block` positions back?
