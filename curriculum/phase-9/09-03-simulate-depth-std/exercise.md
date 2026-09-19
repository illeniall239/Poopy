# Simulate activation std through depth

Topic: 9. Initialization and activation/gradient statistics
Difficulty: 2 of 3

## Problem

See for yourself what initialization does to a deep network, before any training. Write `simulate_depth_std(depth, width, init_std, act, seed)` in NumPy:

1. `rng = np.random.default_rng(seed)`.
2. Draw a batch of inputs `x = rng.standard_normal((1000, width))`: 1000 examples with unit variance.
3. For each of the `depth` layers, in order: draw a fresh weight matrix `W = rng.standard_normal((width, width)) * init_std`, then set `x = act(x @ W)`. There are no biases.
4. After each layer, record the standard deviation of all the entries of `x` (after the activation), as a Python `float`.

Return the list of `depth` recorded values, first layer first.

`act` is one of the strings `"linear"` (identity), `"relu"` (`max(0, z)`) or `"tanh"`. Raise `ValueError` for any other value, if `depth < 1` or `width < 1`, or if `init_std <= 0`.

Very large values are allowed: with a bad init the activations may explode, and that is part of what you are meant to see. Tests use at most 20 layers, where float64 does not overflow.

## Examples

```
simulate_depth_std(20, 100, 0.1, "linear", 0)       → 20 values all near 1.0     1/√100 keeps the scale
simulate_depth_std(10, 100, 1.0, "linear", 0)       → grows about 10× per layer, near 1e10 at the end
simulate_depth_std(20, 100, 0.01, "tanh", 0)        → shrinks about 10× per layer, near 1e-20 at the end
simulate_depth_std(20, 100, 1.0, "tanh", 0)         → values near 0.9–1.0: saturated at ±1
simulate_depth_std(1, 100, 0.1, "relu", 0)          → [about 0.58]               std of ReLU of a unit normal
simulate_depth_std(3, 100, 0.1, "sigmoid", 0)       → ValueError
```

## Constraints

- NumPy only; `depth` at most 50, `width` at most 512.
- Same arguments always give the same list.

## Hints

1. If `x` has unit-variance entries and `W` has entries with standard deviation `σ`, what is the variance of one entry of `x @ W`? What does it depend on besides `σ`?
2. So what factor does each linear layer multiply the std by, and what happens after 20 layers when that factor is 10, or 0.1?
3. What does tanh do to large inputs, and to tiny ones? Which of the two cases is the dead end, and which one saturates?
4. ReLU zeroes about half its inputs. With `init_std = 1/√width`, why does the std still shrink a little each layer, and which gain would fix it?

## Explain-back

- In the linear case, which `init_std` keeps the std constant through depth, and why does it depend on the width?
- What does a saturated tanh layer (std near 1, values stuck at ±1) do to the gradients flowing back through it?
- A net initialized with "small random" weights of 0.01 trains at 3 layers but not at 30. Explain using your results.
- What is the update-to-data ratio, and why is a value near `1e-3` a useful sign that the init and the learning rate are about right?
