# Non-maximum suppression

Topic: 15. Vision tasks beyond classification: detection and segmentation
Difficulty: 2 of 3

## Problem

A detector fires many overlapping boxes around the same object. **Non-maximum suppression** keeps the most confident box and removes the others that overlap it too much. Write `nms(boxes, scores, iou_threshold, labels=None)` in plain Python. This file must contain its own IoU helper:

- Boxes are `[x1, y1, x2, y2]` with `x1 < x2`, `y1 < y2`, continuous coordinates, area `(x2 − x1)(y2 − y1)`. `IoU = intersection / (area_a + area_b − intersection)`, and `0.0` for boxes that do not overlap or only touch.

NMS:

1. Order the box indices by score, highest first. Equal scores keep the lower index first.
2. Walk that order. A box is **kept** unless its IoU with some already-kept box is **strictly greater** than `iou_threshold`, in which case it is suppressed.
3. Return the kept indices (into the original `boxes` list) in the order they were kept, i.e. descending score.

`labels`, if given, is a list of class ids, one per box. Then a box can only be suppressed by a kept box **of the same class**: a person and a bicycle may overlap heavily and both survive. With `labels=None` all boxes are treated as one class.

Raise `ValueError` if `boxes`, `scores` (and `labels` when given) have different lengths, or `iou_threshold` is outside `[0, 1]`. Empty input returns `[]`.

## Examples

```
boxes  = [[0, 0, 10, 10], [1, 1, 11, 11], [20, 20, 30, 30], [0, 0, 9, 10]]
scores = [0.9, 0.8, 0.7, 0.95]
nms(boxes, scores, 0.5)                 → [3, 2]       3 suppresses 0 (IoU 0.9) and 1 (IoU 0.60...)
nms(boxes, scores, 0.95)                → [3, 0, 1, 2]
nms(boxes, scores, 0.5, labels=[0, 1, 0, 0])  → [3, 1, 2]    box 1 is another class
nms([], [], 0.5)                        → []
nms([[0, 0, 1, 1]], [0.5, 0.4], 0.5)    → ValueError
```

## Constraints

- At most 2000 boxes; an `O(n²)` loop is fine.
- Plain Python only.

## Hints

1. Why must the boxes be visited from the highest score down? What goes wrong if you visit them in list order?
2. Which built-in sorts the indices by score descending while keeping ties in index order?
3. When you look at a candidate box, which boxes do you compare it with: all boxes, the remaining ones, or only the kept ones?
4. With `labels`, what one extra condition decides whether a kept box is allowed to suppress the candidate?

## Explain-back

- Why is class-agnostic NMS wrong for a scene where a rider sits on a bicycle? What does per-class NMS do differently?
- Raising `iou_threshold` from 0.5 to 0.9: do you keep more boxes or fewer? What failure do you risk at each extreme?
- What is the difference between the NMS IoU threshold, the confidence threshold that drops low-score boxes, and the IoU threshold used to decide a detection is correct?
- Anchor-free detectors still usually run NMS. What problem does it solve that the network does not?
