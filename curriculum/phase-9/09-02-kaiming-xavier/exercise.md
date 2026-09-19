# Kaiming and Xavier

Topic: 9. Initialization and activation/gradient statistics
Difficulty: 1 of 3

## Problem

Write the two standard initialization scales, in plain Python (the `math` module is enough).

- `kaiming_std(fan_in, gain)` returns the standard deviation of Kaiming/He **normal** initialization: `gain / √fan_in`. `gain` depends on the activation that follows the layer: `√2` for ReLU, `5/3` for tanh, `1` for no activation. It matches `torch.nn.init.kaiming_normal_(w, mode="fan_in")` and the gains from `torch.nn.init.calculate_gain`.
- `xavier_bound(fan_in, fan_out)` returns the bound `a` of Xavier/Glorot **uniform** initialization (gain 1), where weights are drawn from `U(−a, a)`: `a = √(6 / (fan_in + fan_out))`. It matches `torch.nn.init.xavier_uniform_`.

`fan_in` is the number of inputs each output unit sums over; `fan_out` is the number of outputs. For `nn.Linear(in_features, out_features)` the weight has shape `(out_features, in_features)`, so `fan_in = in_features` (the **second** dimension).

Both return a Python `float`. Raise `ValueError` if a fan is less than 1 or `gain <= 0`.

## Examples

```
kaiming_std(512, math.sqrt(2))   → 0.0625
kaiming_std(100, 1.0)            → 0.1
kaiming_std(0, 1.0)              → ValueError
xavier_bound(100, 200)           → 0.1414213562373095     √(6 / 300)
xavier_bound(3, 3)               → 1.0
```

## Constraints

- Fans up to 10 000 000.
- Values match the formulas within `1e-12`.

## Hints

1. If the inputs have variance 1 and the weights have variance `σ²`, what is the variance of a sum of `fan_in` products of independent inputs and weights?
2. What `σ` keeps that variance at 1? How does ReLU, which zeroes half of its inputs, change the answer, and where does `√2` come from?
3. Xavier tries to keep the variance steady in both the forward and the backward pass. Why does that bring `fan_out` in, and how does it average the two?
4. A uniform distribution on `[−a, a]` has variance `a² / 3`. How do you turn a target variance into a bound `a`?

## Explain-back

- Why does initializing every weight to zero fail, even though each layer's output is perfectly "stable"?
- Why is "small random numbers, like 0.01" not enough for a deep net? What happens to the activations 20 layers in?
- For `nn.Linear(784, 256)`, what are `fan_in` and `fan_out`, and which dimension of `weight.shape` is which? What goes wrong if you swap them in Kaiming init?
- Why is Kaiming the default for ReLU networks and Xavier for tanh? What does the gain correct for?
