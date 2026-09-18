# Maximum likelihood and negative log-likelihood

Topic: 13. Likelihood, entropy and cross-entropy
Difficulty: 2 of 3

## Problem

Write three functions in pure Python (no NumPy; `math` allowed):

- `mle_bernoulli(ys: list[int]) -> float` — the maximum-likelihood estimate of `p` for 0/1 outcomes: the fraction of ones. Raise `ValueError` on an empty list or a value other than 0 or 1.
- `mle_gaussian(xs: list[float]) -> tuple[float, float]` — the MLE `(mean, variance)` for a Gaussian: the sample mean and the variance with `ddof=0` (divide by `n`, not `n - 1`). Raise `ValueError` on an empty list.
- `nll_bernoulli(ys: list[int], ps: list[float]) -> float` — the mean negative log-likelihood `-(1/n) Σ [yᵢ log pᵢ + (1 - yᵢ) log(1 - pᵢ)]`, which is binary cross-entropy. Clip each `pᵢ` into `[1e-12, 1 - 1e-12]` before taking logs so that a confident wrong prediction gives a large finite loss rather than `inf`. Raise `ValueError` on a length mismatch, an empty list, or a `pᵢ` outside `[0, 1]`.

## Examples

```
mle_bernoulli([1, 0, 1, 1])              → 0.75
mle_bernoulli([0, 0, 0])                 → 0.0
mle_gaussian([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0])   → (5.0, 4.0)     ddof=0
nll_bernoulli([1, 0], [0.9, 0.1])        → 0.1053...      -log 0.9
nll_bernoulli([1, 0], [0.5, 0.5])        → 0.6931...      log 2, a coin flip
nll_bernoulli([1], [0.0])                → 27.63...       -log(1e-12), large but finite
nll_bernoulli([1, 0, 1, 1], [0.75] * 4)  → the minimum over any constant p (the MLE)
```

## Constraints

- Up to 100 000 samples.
- Must match NumPy (`np.mean`, `np.var`) within `1e-12`.
- The test checks that `nll_bernoulli(ys, [p] * n)` is minimized at `p = mle_bernoulli(ys)` by comparing against nearby `p` values.

## Hints

1. The likelihood of i.i.d. Bernoulli data is `p^k (1-p)^(n-k)`. Take the log, differentiate with respect to `p`, set to zero. What is `p`?
2. For the Gaussian, maximizing the log-likelihood in `μ` gives the mean; in `σ²` it gives which normalizer, `n` or `n - 1`? Why is the MLE biased?
3. `log(0)` raises. Which predictions make `nll_bernoulli` explode, and where does the clip go so both `log pᵢ` and `log(1 - pᵢ)` are safe?
4. For a constant prediction `p` on data with `k` ones out of `n`, write the NLL as a function of `p`. Where is its minimum?

## Explain-back

- Explain in one sentence why "minimize cross-entropy" and "maximize likelihood" are the same thing for a Bernoulli model.
- Why take logs? Give one numerical reason (what does a product of 10 000 probabilities look like in float64?) and one mathematical convenience.
- MSE is the negative log-likelihood of which noise model? What assumption about the errors does that build in?
- Accuracy on `[1, 0]` with predictions `[0.51, 0.49]` is 100% and with `[0.99, 0.01]` also 100%. What does `nll_bernoulli` say about the two, and why is that the better training signal?
