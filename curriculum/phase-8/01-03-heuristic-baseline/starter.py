import re


def keyword_classify(text: str, keywords: dict[str, list[str]], default: str) -> str:
    """Label with the most whole-word keyword hits, ties to the first label, default when no hits."""
    raise NotImplementedError


def rule_accuracy(texts: list[str], labels: list[str], keywords: dict[str, list[str]], default: str) -> float:
    """Accuracy of keyword_classify over the texts; ValueError on empty or mismatched lists."""
    raise NotImplementedError


def improvement_over_baseline(model_score: float, baseline_score: float) -> float:
    """Relative error reduction (baseline_err - model_err) / baseline_err for accuracies in [0, 1]."""
    raise NotImplementedError
