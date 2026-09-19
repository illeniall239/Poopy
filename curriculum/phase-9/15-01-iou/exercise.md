# Intersection over union

Topic: 15. Vision tasks beyond classification: detection and segmentation
Difficulty: 1 of 3

## Problem

A detector's box is judged by how well it overlaps the true box: **IoU** is the area of their intersection divided by the area of their union. Write `iou(box_a, box_b)` in plain Python.

- A box is `[x1, y1, x2, y2]`: the top-left corner `(x1, y1)` and bottom-right corner `(x2, y2)`, with `x1 < x2` and `y1 < y2`. Coordinates are continuous (ints or floats), so a box's area is `(x2 − x1) · (y2 − y1)`, with no `+1`.
- The union is `area_a + area_b − intersection`: the overlap must not be counted twice.
- Boxes that do not overlap, or only touch along an edge or at a corner, have IoU `0.0`.
- Return a float in `[0, 1]`. The result is symmetric: `iou(a, b) == iou(b, a)`.

Raise `ValueError` if a box does not have exactly 4 numbers or has `x2 <= x1` or `y2 <= y1`.

## Examples

```
iou([0, 0, 2, 2], [0, 0, 2, 2])  → 1.0
iou([0, 0, 2, 2], [1, 1, 3, 3])  → 0.142857...   1 / (4 + 4 − 1)
iou([0, 0, 4, 4], [1, 1, 3, 3])  → 0.25          small box inside a big one: 4 / 16
iou([0, 0, 1, 1], [2, 2, 3, 3])  → 0.0           disjoint
iou([0, 0, 1, 1], [1, 0, 2, 1])  → 0.0           touching edges
iou([0, 0, 1, 1], [1, 1, 0, 2])  → ValueError
```

## Constraints

- Coordinates are finite, with absolute value at most `1e6`.
- Plain Python only; float results are checked to `1e-9`.

## Hints

1. The intersection of two boxes is itself a box, when it exists. Which of the two `x1` values is its left edge, and which `x2` is its right edge?
2. What is that intersection's width when the boxes do not overlap horizontally, and how can one `max` stop it going negative?
3. If you add the two areas, which region have you counted twice?
4. What must you check before dividing, and why can that never be zero once both boxes are valid?

## Explain-back

- A detector is evaluated on images with several objects each. Why is plain accuracy the wrong score, and what does mAP measure instead?
- A predicted box counts as correct when its IoU with a true box is at least 0.5. How is that threshold different from the detector's confidence threshold?
- Why does a tiny box sitting inside a big true box get a low IoU even though it is "on" the object?
- What does IoU of 0.5 look like for two equal squares shifted sideways? Is it a generous or a strict threshold?
