# Train and evaluate loop

Topic: 19. Capstone: a tiny CNN and a character-level LM from scratch
Difficulty: 2 of 3

## Problem

Write the loop every capstone run goes through: train for an epoch, then measure the validation loss honestly, and keep the history so you can draw both curves. Use PyTorch.

`train_and_eval(model, train, val, epochs, make_optimizer)` takes

- `model`: any `nn.Module` classifier that maps a batch `X` to logits,
- `train` and `val`: lists of `(X, y)` batches, where `y` is a `torch.long` tensor of class indices (batches may have different sizes),
- `epochs`: how many passes over `train`,
- `make_optimizer`: a function that takes the model's parameters and returns an optimizer, for example `lambda p: torch.optim.Adam(p, lr=0.01)`. Call it **exactly once**, with `model.parameters()`, before the first epoch.

For every epoch:

1. Put the model in training mode. For each train batch, in order: compute `F.cross_entropy(model(X), y)`, zero the gradients, backpropagate, take an optimizer step.
2. The epoch's **train loss** is the mean of those batch losses weighted by batch size (each example counts once), i.e. `Σ loss_b · n_b / Σ n_b`, using the loss values computed during training.
3. Put the model in evaluation mode and, under `torch.no_grad()`, compute the **val loss**: the mean cross-entropy over all validation examples (again each example counts once, whatever the batch sizes).

Return `{"train": [...], "val": [...]}`: two lists of `epochs` Python floats. Raise `ValueError` if `epochs < 1` or either batch list is empty.

The test model is a tiny CNN with BatchNorm and Dropout trained on seeded synthetic 8 × 8 images (bright top half vs bright bottom half). It records, at every forward pass, whether gradients were enabled and whether the model was in training mode.

## Examples

```
hist = train_and_eval(tiny_cnn, train_batches, val_batches, 8, lambda p: torch.optim.Adam(p, lr=0.01))
hist["train"]  → 8 floats, falling
hist["val"]    → 8 floats, the last one below 0.4

val batches of 20 and 12 examples with mean losses 0.5 and 0.1:
  val loss = (0.5 · 20 + 0.1 · 12) / 32 = 0.35     not (0.5 + 0.1) / 2 = 0.30
```

## Constraints

- Batches have at most 64 examples; the tests run a few epochs on under 100 images.
- PyTorch on CPU. `F.cross_entropy` and the optimizer returned by `make_optimizer` are all you need.

## Hints

1. What do `model.train()` and `model.eval()` change inside Dropout and BatchNorm, and at which two points of every epoch must you switch?
2. Why is it wrong to create the optimizer inside the epoch loop? What state would Adam lose?
3. If `F.cross_entropy` returns the mean over its batch, what must you multiply by before adding up the batches? Is there a `reduction` argument that helps?
4. What does `torch.no_grad()` save during validation, and how do you turn a one-element loss tensor into a Python float without keeping the graph alive?

## Explain-back

- Forget `model.eval()` for validation and your val loss becomes noisy and the BatchNorm statistics drift. Explain both effects.
- Why report the val loss rather than the train loss as "the result"? And when you finally report the test loss, why only once, at the very end?
- Your training loss is recorded *during* the epoch while the weights keep changing, the val loss *after* it. How does that make early train and val curves hard to compare directly?
- In an ablation you swap Adam for SGD through `make_optimizer`. What else must stay fixed (think seeds, data order) for the comparison to mean anything?
