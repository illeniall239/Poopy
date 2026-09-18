def bayes(prior: float, likelihood: float, evidence: float) -> float:
    """P(H|E) = likelihood * prior / evidence; ValueError on invalid probabilities or an impossible result."""
    raise NotImplementedError


def posterior_positive_test(prevalence: float, sensitivity: float, specificity: float) -> float:
    """P(sick | positive test) from prevalence, P(pos|sick) and P(neg|healthy)."""
    raise NotImplementedError
