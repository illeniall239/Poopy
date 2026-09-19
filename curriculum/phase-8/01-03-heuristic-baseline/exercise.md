# Heuristic baseline

Topic: 1. Framing a problem, baselines, and when not to use ML
Difficulty: 2 of 3

## Problem

Before training a text classifier, write the hand-made rule it has to beat, and a function that says honestly how much better a model is. Pure Python (no numpy).

- `keyword_classify(text: str, keywords: dict[str, list[str]], default: str) -> str` labels one text. Lowercase it and split it into words with `re.findall(r"[a-z0-9]+", text.lower())`. For every label in `keywords`, count how many of the text's words are in that label's keyword list (each occurrence counts; keywords are given in lowercase and match whole words only, so `"free"` does not match `"freedom"`). Return the label with the highest count. On a tie, return the tied label that comes first in `keywords`' order. If no label has a single hit, return `default`.
- `rule_accuracy(texts: list[str], labels: list[str], keywords: dict[str, list[str]], default: str) -> float` returns the accuracy of `keyword_classify` over the texts. Raise `ValueError` if the lists are empty or their lengths differ.
- `improvement_over_baseline(model_score: float, baseline_score: float) -> float` returns the relative error reduction of a model over a baseline, where both scores are accuracies in `[0, 1]` and error is `1 - accuracy`: `(baseline_error - model_error) / baseline_error`. It is negative when the model is worse than the baseline. Raise `ValueError` if either score is outside `[0, 1]`, or if the baseline is already perfect (`baseline_score == 1`), since there is no error left to reduce.

## Examples

```
kw = {"spam": ["free", "winner", "prize"], "ham": ["meeting", "lunch"]}
keyword_classify("FREE prize inside", kw, "ham")          → "spam"     2 hits vs 0
keyword_classify("Lunch meeting, free pizza", kw, "ham")  → "ham"      2 hits vs 1
keyword_classify("free lunch", kw, "other")               → "spam"     1 vs 1, "spam" comes first
keyword_classify("Freedom!", kw, "other")                 → "other"    no whole-word hit
improvement_over_baseline(0.95, 0.90)                     → 0.5        errors 0.10 → 0.05
improvement_over_baseline(0.92, 0.90)                     → 0.2
improvement_over_baseline(0.85, 0.90)                     → -0.5       worse than the baseline
```

## Constraints

- Pure Python: `re`, `collections` and `math` are allowed.
- At most 10 000 texts of at most 1 000 characters each; keep keyword lookups O(1) per word.
- Scores are compared within `1e-9`.

## Hints

1. How do you turn "does this word appear in this list" into a constant-time check, and when should you build that structure?
2. Why does splitting the text into words before matching avoid the `"freedom"` problem that a substring check (`"free" in text`) has?
3. Going from 90% to 92% accuracy sounds like 2 points. How much of the remaining error did the model actually remove?
4. What does the formula give when the baseline makes no errors at all, and what should the function do instead of dividing?

## Explain-back

- A trained model scores 0.91 and your keyword rule scores 0.90. What would make you ship the rule instead of the model?
- Why is relative error reduction a more honest summary than the difference in accuracy, especially near 100%?
- Name a product problem where a hand-written threshold or keyword rule is already enough and ML is not worth building.
- Your spam labels come from users clicking "report". In what way is that a proxy for the real goal, and how could a model that fits it perfectly still fail?
