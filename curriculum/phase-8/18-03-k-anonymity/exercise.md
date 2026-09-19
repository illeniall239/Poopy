# k-anonymity

Topic: 18. Responsible AI: fairness, bias and privacy
Difficulty: 3 of 3

## Problem

Removing names does not make a dataset anonymous: age plus zip code is often unique, and a join with a public list re-identifies the person. A table is k-anonymous when every combination of quasi-identifier values is shared by at least `k` rows. Write two pure-Python functions over records stored as a list of dicts:

- `k_anonymity(records: list[dict], quasi_ids: list[str]) -> int` groups the records by the tuple of their `quasi_ids` values (an equivalence class) and returns the size of the smallest class. With no quasi-identifiers every record is in one class. Raise `ValueError` if `records` is empty.
- `generalize(records: list[dict], quasi_ids: list[str], rules: dict, k: int) -> list[dict]` coarsens the quasi-identifiers until the table is `k`-anonymous:
  - `rules[col]` is a list of functions for column `col`, ordered from mildest to strongest (for example "age to decade", then "age to 20-year band"). A column may be missing from `rules`, which means it has no functions.
  - Each column has a level. Level 0 is the original value; level `j` (1 to `len(rules[col])`) is `rules[col][j - 1]` applied to the **original** value; the last level, `len(rules[col]) + 1`, replaces the value with the string `"*"` (masked).
  - Start with every column at level 0. Repeat: if the table is `k`-anonymous, stop. Otherwise raise by one the level of the quasi-identifier that has the lowest level among those not yet masked, taking the one earliest in `quasi_ids` on ties.
  - Return new dicts with the generalized values. Columns that are not quasi-identifiers (such as the sensitive attribute) are copied unchanged. The input records are not modified.

  Raise `ValueError` if `records` is empty, `k < 1`, or the table is still not `k`-anonymous with every quasi-identifier masked (fewer than `k` records).

## Examples

```
records = [{"age": 34, "zip": "13053", "disease": "flu"},
           {"age": 36, "zip": "13068", "disease": "cold"},
           {"age": 38, "zip": "13053", "disease": "flu"},
           {"age": 52, "zip": "14850", "disease": "asthma"},
           {"age": 57, "zip": "14853", "disease": "flu"},
           {"age": 55, "zip": "14850", "disease": "cold"}]
rules = {"age": [lambda a: f"{a // 10 * 10}-{a // 10 * 10 + 9}"], "zip": [lambda z: z[:3] + "**"]}
k_anonymity(records, ["age", "zip"])            → 1     every row is unique
generalize(records, ["age", "zip"], rules, 3)   → age to decade, then zip to 3 digits:
    [{"age": "30-39", "zip": "130**", "disease": "flu"}, ..., {"age": "50-59", "zip": "148**", "disease": "cold"}]
generalize(records, ["age", "zip"], rules, 4)   → both columns end up "*"
generalize(records, ["age", "zip"], rules, 7)   → ValueError   only 6 records
```

## Constraints

- Pure Python (`collections` is allowed).
- Up to 100 000 records, up to 5 quasi-identifiers with up to 5 rules each.

## Hints

1. What single hashable value identifies the equivalence class of a record, and which standard container counts them for you?
2. Why must each level be computed from the original value rather than from the previous level's output?
3. How do you know which column to coarsen next, and what state do you need to keep between steps to know it?
4. When can the loop never succeed, and how can you detect that without looping forever?

## Explain-back

- The dataset had its names removed. Why was it still not anonymous, and what kind of join would re-identify someone?
- Every class in your 3-anonymous table might have the same disease. What does an attacker learn then, and what stronger property addresses it?
- Generalizing trades privacy for usefulness. Which analyses does the zip-to-3-digits step break?
- Why is a privacy check part of the design before a dataset is shared, rather than a clean-up step afterwards?
