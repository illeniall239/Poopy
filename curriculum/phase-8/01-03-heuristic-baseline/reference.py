# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import re


def keyword_classify(text: str, keywords: dict[str, list[str]], default: str) -> str:
    words = re.findall(r"[a-z0-9]+", text.lower())
    best_label, best_hits = default, 0
    for label, label_keywords in keywords.items():
        wanted = set(label_keywords)
        hits = sum(word in wanted for word in words)
        if hits > best_hits:  # strictly greater, so the earlier label wins a tie
            best_label, best_hits = label, hits
    return best_label


def rule_accuracy(texts: list[str], labels: list[str], keywords: dict[str, list[str]], default: str) -> float:
    if not texts or len(texts) != len(labels):
        raise ValueError("texts and labels must be non-empty and the same length")
    correct = sum(keyword_classify(t, keywords, default) == y for t, y in zip(texts, labels))
    return correct / len(texts)


def improvement_over_baseline(model_score: float, baseline_score: float) -> float:
    if not (0.0 <= model_score <= 1.0 and 0.0 <= baseline_score <= 1.0):
        raise ValueError("scores must be accuracies in [0, 1]")
    baseline_error = 1.0 - baseline_score
    if baseline_error == 0.0:
        raise ValueError("the baseline is perfect; there is no error to reduce")
    model_error = 1.0 - model_score
    return (baseline_error - model_error) / baseline_error
