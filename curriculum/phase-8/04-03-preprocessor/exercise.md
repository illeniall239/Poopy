# Preprocessor

Topic: 4. Features: scaling, encoding and feature engineering
Difficulty: 3 of 3

## Problem

Build one object that turns raw table rows into a numeric feature matrix, learning every statistic from the training rows and never again. Write a `Preprocessor` class (NumPy allowed). Rows are dicts from column name to raw value.

`Preprocessor(spec: dict[str, dict])` — `spec` maps each input column to how it is encoded, by `"kind"`:

| kind | fit learns (from training rows only) | transform outputs |
|---|---|---|
| `"numeric"` | mean and population std of the values | 1 column: `(x − mean) / std` |
| `"log"` | mean and population std of `log1p(x)` | 1 column: `(log1p(x) − mean) / std` |
| `"bucket"` (needs `"boundaries"`) | nothing | `len(boundaries) + 1` one-hot columns for the bucket index: `i` = number of boundaries `≤ x` |
| `"category"` | vocabulary: the distinct training values, **sorted** | `len(vocabulary) + 1` one-hot columns, the last one the unknown bucket |

A std of `0` is replaced by `1.0`, as in a standard scaler. The constructor raises `ValueError` for an empty spec, an unknown kind, or a `"bucket"` column whose `"boundaries"` is missing, empty or not strictly increasing.

- `fit(self, rows: list[dict]) -> "Preprocessor"` — learn the statistics and vocabularies above, and return `self`. Raise `ValueError` if `rows` is empty, if a row lacks a column named in the spec, or if a `"log"` value is negative.
- `transform(self, rows: list[dict]) -> np.ndarray` — a float array of shape `(len(rows), n_features)`. Output columns follow the spec's key order, each column's block laid out as in the table. Only the stored statistics are used, so transforming one row alone gives exactly that row's line of a batch transform, and unseen categories go to the unknown bucket instead of crashing. Raise `RuntimeError` before `fit`, and `ValueError` for a missing column or a negative `"log"` value. An empty `rows` list returns shape `(0, n_features)`. Extra keys in a row are ignored.

## Examples

```
spec = {"age": {"kind": "numeric"}, "income": {"kind": "log"},
        "hour": {"kind": "bucket", "boundaries": [6, 12, 18]}, "city": {"kind": "category"}}
train = [{"age": 20, "income": 0,  "hour": 5,  "city": "Paris"},
         {"age": 30, "income": 9,  "hour": 12, "city": "Lahore"},
         {"age": 40, "income": 99, "hour": 23, "city": "Paris"}]
p = Preprocessor(spec).fit(train)          vocabulary for city: ["Lahore", "Paris"]
p.transform(train[:1])
  → [[-1.2247, -1.2247, 1, 0, 0, 0, 0, 1, 0]]      age | income | hour ×4 | city ×3
p.transform([{"age": 30, "income": 9, "hour": 18, "city": "Oslo"}])
  → [[0.0, 0.0, 0, 0, 0, 1, 0, 0, 1]]               Oslo → unknown bucket
Preprocessor({"x": {"kind": "ordinal"}})  → ValueError
```

## Constraints

- NumPy and `math` allowed; scikit-learn is not.
- Up to 50 000 rows and 50 spec columns; `fit` and `transform` are each one pass over the rows per column.
- Values compared within `1e-9`.

## Hints

1. Which attributes must exist after `fit` for `transform` to work with no access to the training rows at all?
2. If `transform` computed a mean from the rows it was given, what would it return for a single row, and how would a test catch it?
3. Why sort the vocabulary instead of keeping first-seen order? What changes if you fit twice on the same rows in a different order?
4. How many output columns does each kind contribute, and can you compute the total width right after `fit`, before seeing any rows to transform?

## Explain-back

- Walk through what leaks if `fit` is called on train and test rows together, for each of the four kinds. Which kinds are safe anyway, and why?
- Why does income get `log1p` before scaling, and what would a plain z-score do with a few billionaires in the data?
- A decision tree will consume these features. Which of these steps could you drop for a tree, and which would you keep?
- Features chosen by correlation with the target, computed on the full dataset: why is that the same mistake as fitting the scaler on everything?
