# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def _check(*ps: float) -> None:
    if any(not 0.0 <= p <= 1.0 for p in ps):
        raise ValueError("probabilities must lie in [0, 1]")


def bayes(prior: float, likelihood: float, evidence: float) -> float:
    _check(prior, likelihood, evidence)
    if evidence == 0:
        raise ValueError("evidence probability must be positive")
    posterior = likelihood * prior / evidence
    if posterior > 1 + 1e-12:
        raise ValueError("inconsistent inputs: posterior exceeds 1")
    return min(posterior, 1.0)


def posterior_positive_test(prevalence: float, sensitivity: float, specificity: float) -> float:
    _check(prevalence, sensitivity, specificity)
    p_positive = sensitivity * prevalence + (1 - specificity) * (1 - prevalence)
    if p_positive == 0:
        return 0.0
    return bayes(prevalence, sensitivity, p_positive)
