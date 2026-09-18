# Bayes' rule

Topic: 8. Probability for ML
Difficulty: 1 of 3

## Problem

Write two functions in pure Python (no NumPy):

- `bayes(prior: float, likelihood: float, evidence: float) -> float` — `P(H | E) = P(E | H) · P(H) / P(E)`. Raise `ValueError` if any input is outside `[0, 1]` or `evidence == 0`, or if the result would exceed 1 (that means the inputs are inconsistent).
- `posterior_positive_test(prevalence: float, sensitivity: float, specificity: float) -> float` — the probability that a person actually has a condition given a positive test, where `prevalence = P(sick)`, `sensitivity = P(positive | sick)` and `specificity = P(negative | healthy)`. Compute `P(positive)` from the two ways a test can come back positive, then apply `bayes`. Raise `ValueError` for inputs outside `[0, 1]`.

## Examples

```
bayes(0.5, 0.8, 0.4)                          → 1.0
bayes(0.01, 0.9, 0.1)                         → 0.09
posterior_positive_test(0.01, 0.99, 0.99)     → 0.5          1% prevalence: a 99% accurate test is a coin flip
posterior_positive_test(0.5, 0.99, 0.99)      → 0.99
posterior_positive_test(0.0, 0.99, 0.99)      → 0.0
bayes(0.5, 0.9, 0.0)                          → ValueError
bayes(0.9, 0.9, 0.1)                          → ValueError   posterior would be 8.1
```

## Constraints

- Answers within `1e-9`.
- `posterior_positive_test` with `prevalence = 1` returns `1.0` (no healthy people to false-positive).

## Hints

1. Write Bayes' rule with the words "prior", "likelihood", "evidence" and "posterior" next to each term. Which is the denominator?
2. A positive result comes from a sick person (with probability `sensitivity`) or from a healthy person. What is `P(positive | healthy)` in terms of `specificity`?
3. Combine the two routes to a positive test into `P(positive)` with the law of total probability. What weights each route?
4. With 1% prevalence, imagine 10 000 people. How many true positives and how many false positives does a 99%/99% test produce? Does the ratio match the example?

## Explain-back

- `P(positive | sick) = 0.99` and `P(sick | positive) = 0.5`. Explain in one sentence why they differ so much, and which one a patient actually cares about.
- What is the base-rate fallacy, and which input to `posterior_positive_test` does it ignore?
- If the same person tests positive a second time (independent test), what becomes the prior for the second application of Bayes' rule?
- A spam filter outputs `P(spam | words) = 0.8`. Which term is the prior here, and what happens to the filter if the prior is estimated on a training set with 50% spam but deployed where 5% is spam?
