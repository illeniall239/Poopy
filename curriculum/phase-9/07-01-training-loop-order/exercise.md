# Training loop order

Topic: 7. PyTorch fundamentals: tensors, autograd, nn.Module, the training loop
Difficulty: 1 of 3

## Problem

Every PyTorch training loop makes the same five calls per batch, in the same order. Write that loop against a fake model so the tests can check the order itself. You do not need torch.

`training_loop(step_fns, batches, epochs)`:

- `step_fns` is a dict of five callables:
  - `"zero_grad"()` clears old gradients (like `optimizer.zero_grad()`);
  - `"forward"(x)` returns the model output for input `x` (like `model(x)`);
  - `"loss"(out, y)` returns the loss for that output and target (like `loss_fn(out, y)`), as a number;
  - `"backward"(loss)` fills the gradients (like `loss.backward()`). Pass it the exact object that `"loss"` returned;
  - `"step"()` updates the parameters (like `optimizer.step()`).
- `batches` is a list of `(x, y)` pairs. Each epoch goes through the whole list once, in order.
- `epochs` is how many times to go through it.

For **every** batch, call exactly `zero_grad()`, `forward(x)`, `loss(out, y)`, `backward(loss)`, `step()`, in that order, once each.

Return a list with one entry per epoch: the mean of that epoch's loss values, as a Python `float`. `epochs == 0` makes no calls and returns `[]`.

Raise `ValueError`, before calling anything, if `epochs` is negative, if `batches` is empty, or if any of the five keys is missing from `step_fns`.

## Examples

```
log = []
fns = {
    "zero_grad": lambda: log.append("zero_grad"),
    "forward":   lambda x: (log.append("forward"), x * 2)[1],
    "loss":      lambda out, y: (log.append("loss"), out - y)[1],
    "backward":  lambda loss: log.append("backward"),
    "step":      lambda: log.append("step"),
}
training_loop(fns, [(1, 0), (3, 1)], 1)   → [3.5]        losses 2 and 5
log → ["zero_grad", "forward", "loss", "backward", "step",
       "zero_grad", "forward", "loss", "backward", "step"]

training_loop(fns, [(1, 0)], 0)           → []           no calls
training_loop(fns, [], 3)                 → ValueError
```

## Constraints

- `batches` has at most 10 000 pairs; `epochs` is at most 1000.
- Do not look inside `x`, `y` or the outputs: pass them along untouched.

## Hints

1. In a real PyTorch loop, what happens to `.grad` if you call `backward()` twice without clearing it in between?
2. Which of the five calls produces the value the next call needs? Write the chain of values from `x` to the parameter update.
3. Why must `zero_grad` run for every batch rather than once per epoch?
4. Where in the loop do you collect each loss so you can average it per epoch, without changing what goes into `backward`?

## Explain-back

- What goes wrong in a real model if `optimizer.zero_grad()` is forgotten? Would the loss curve look obviously broken, or only slightly off?
- Could `zero_grad` go anywhere else in the cycle and still be correct? What is the one constraint on where it goes?
- Why is calling `.item()` on the loss inside the hot loop slow on a GPU, and when is it acceptable?
- What two things does a real evaluation pass add around the forward call (`model.eval()` and `torch.no_grad()`), and what does each one prevent?
