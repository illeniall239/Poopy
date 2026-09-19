# Flip and crop augmentation

Topic: 11. Regularization in deep nets
Difficulty: 2 of 3

## Problem

Data augmentation makes new training examples for free by transforming the ones you have in ways that do not change the label. Write `augment_flip_crop(img, rng, crop)` in plain Python (no numpy, no torch).

- `img` is a grayscale image as a list of `H` rows, each a list of `W` numbers (all rows the same length, `H, W >= 1`).
- `rng` is a `random.Random`. Use it in exactly this order:
  1. Call `rng.random()` once. If it is `< 0.5`, flip the image **horizontally** (reverse every row, left becomes right).
  2. `top = rng.randint(0, H - crop)`, then `left = rng.randint(0, W - crop)`.
- Return the `crop × crop` window whose top-left corner is at row `top`, column `left` of the (possibly flipped) image, as a new list of lists.

Raise `ValueError` if `crop < 1` or `crop` is larger than `H` or `W`. Never modify `img`. Every output pixel comes from the input, so the output's pixels are a sub-multiset of the input's. When `crop` equals both `H` and `W` the output is the whole image, flipped or not.

## Examples

```
img = [[1, 2, 3],
       [4, 5, 6],
       [7, 8, 9]]
augment_flip_crop(img, rng, 3)  → img or [[3, 2, 1], [6, 5, 4], [9, 8, 7]]
augment_flip_crop(img, rng, 2)  → a 2×2 window, e.g. [[5, 6], [8, 9]] or, after a flip, [[2, 1], [5, 4]]
augment_flip_crop(img, rng, 4)  → ValueError
```

## Constraints

- Images are at most 64 × 64.
- Use only the `rng` you are given, in the order above, so results are reproducible from a seed.

## Hints

1. Which label-preserving change is a horizontal flip for a photo of a cat? For which kinds of image would it change the label?
2. How do you reverse one row in Python without modifying the original list?
3. For an image `H` rows tall, what are the smallest and largest valid values of `top` so the window stays inside the image?
4. Once you have `top` and `left`, how do slices of the rows give you the window in one expression?

## Explain-back

- Should you augment the validation set? What would that do to the number you use to pick a model?
- Why is augmentation described as "free data", and what is its cost?
- Name an image task where a horizontal flip would change the correct label.
- A model that underfits the training set: would more augmentation help or hurt? Why?
