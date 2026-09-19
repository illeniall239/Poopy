# Train an MLP on your own engine

Topic: 4. A scalar autograd engine (micrograd)
Difficulty: 3 of 3

## Problem

Build a tiny neural-network library on top of your `Value` class and train it. Everything goes in this one file, in plain Python (`math` and `random` are fine; no numpy, no torch). You may start by copying your `Value` from the previous exercise.

**`Value`**, as before: `Value(data, _children=(), _op="")` with `.data` and `.grad` (starting at `0.0`); `+`, `*`, `** k` (plain number `k`), `.tanh()`, unary `-`, `-`, and the reflected `2 + v`, `2 * v`, `2 - v`; `backward()` sets the output's grad to `1.0` and runs every backward step in reverse topological order, each one adding (`+=`) into its children's grads.

**`Neuron(nin, rng)`**: `nin` weights then one bias, each a `Value` initialised with `rng.uniform(-1, 1)` in that order (all weights first, then the bias). `rng` is a `random.Random`. Calling `neuron(x)` on a list of `nin` numbers or `Value`s returns `tanh(w·x + b)` as a `Value`. `neuron.parameters()` returns the weights followed by the bias.

**`Layer(nin, nout, rng)`**: `nout` neurons created in order from the same `rng`. `layer(x)` returns the list of the `nout` neuron outputs. `layer.parameters()` concatenates its neurons' parameters in order.

**`MLP(nin, nouts, seed=0)`**: creates one `random.Random(seed)` and uses it for every layer, in order: layer sizes are `[nin] + nouts`, so `MLP(3, [4, 4, 1])` has layers 3→4, 4→4, 4→1. Every layer, including the last, uses tanh. `mlp(x)` feeds `x` through the layers and returns a single `Value` when the last layer has one unit, otherwise the list of output `Value`s. `mlp.parameters()` concatenates the layers' parameters in order. `mlp.zero_grad()` sets every parameter's `grad` to `0.0`.

**`train(model, xs, ys, steps, lr)`**: plain gradient descent for `steps` steps. Each step:
1. forward every input in `xs` through `model`;
2. loss = the **sum** over examples of `(prediction − target) ** 2`, as a `Value`;
3. `model.zero_grad()`, then `loss.backward()`;
4. for every parameter `p`: `p.data -= lr * p.grad`.

Zero the gradients before `backward()` every step, so that whatever is in `.grad` beforehand never leaks into the update. Return the list of the `steps` loss values as floats, each recorded **before** that step's update.

On the four points below, `train(MLP(3, [4, 4, 1], seed=0), xs, ys, 100, 0.05)` must drive the last recorded loss below `0.02`.

## Examples

```
xs = [[2.0, 3.0, -1.0], [3.0, -1.0, 0.5], [0.5, 1.0, 1.0], [1.0, 1.0, -1.0]]
ys = [1.0, -1.0, -1.0, 1.0]

len(MLP(3, [4, 4, 1]).parameters())        → 41          (3*4+4) + (4*4+4) + (4*1+1)
MLP(3, [4, 4, 1])([2.0, 3.0, -1.0])        → a Value in (-1, 1)
MLP(2, [3, 2])([1.0, -1.0])                → a list of 2 Values
MLP(3, [4, 4, 1], seed=0).parameters()[0].data == random.Random(0).uniform(-1, 1)   → True

losses = train(MLP(3, [4, 4, 1], seed=0), xs, ys, 100, 0.05)
len(losses)                                 → 100
losses[0]                                   → about 7.73
losses[-1] < 0.02                           → True
```

## Constraints

- At most a few hundred parameters and a few hundred steps; the test file runs in a couple of seconds.
- `lr` is a positive float; `steps ≥ 1`.

## Hints

1. A neuron is `tanh(w·x + b)`. Which `Value` operations does that use, and does `sum(...)` over `Value`s need a start value or a reflected operation to work?
2. How does `MLP.parameters()` collect every `Value` a gradient step must update, and why does the order of creation matter for reproducing a run from its seed?
3. After `loss.backward()`, what is in each parameter's `.grad`? What would the next step's `.grad` contain if you never reset it?
4. Why does the update subtract `lr * p.grad` rather than add it? What would the loss curve look like if you flipped the sign or made `lr` far too large?

## Explain-back

- Why must `zero_grad()` run every step? What does training compute if you forget it, and why can the loss still sometimes go down?
- The loss is a sum over the four examples. If you switched to the mean, how would you have to change `lr` to take the same steps?
- Every hidden unit's output feeds every unit in the next layer. Which line of your `Value` makes those contributions combine correctly, and what happens with `grad =` there?
- This net has 41 parameters and takes a noticeable moment per step. Is Python the bottleneck, or is it doing one scalar operation per `Value`? What does PyTorch change?
