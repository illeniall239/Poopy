# Segmentation IoU

Topic: 15. Vision tasks beyond classification: detection and segmentation
Difficulty: 2 of 3

## Problem

A semantic segmenter outputs one class id per pixel. It is scored per class: for class `c`, treat "pixel is `c`" as a region in the prediction and in the ground truth, and compute their IoU. Write `mean_iou(pred_mask, true_mask, n_classes)` in plain Python.

- `pred_mask` and `true_mask` are lists of rows of ints, the same shape, every value in `range(n_classes)`.
- For each class `c` in `0 … n_classes − 1`:
  - `intersection` = number of pixels where both masks are `c`;
  - `union` = number of pixels where either mask is `c`;
  - its IoU is `intersection / union`. If `union` is `0`, the class appears in neither mask and its IoU is `None`: it is ignored, not counted as `0` or `1`.
- `mean` is the average of the per-class IoUs that are not `None`.

Return the tuple `(per_class, mean)`: a list of length `n_classes` of floats or `None`, and a float. A class present in the ground truth but never predicted scores `0.0` and **does** count in the mean.

Raise `ValueError` if the masks are empty or differ in shape, if `n_classes < 1`, or if any value is outside `range(n_classes)`.

## Examples

```
pred = [[0, 0, 1],
        [0, 1, 1]]
true = [[0, 0, 0],
        [0, 1, 1]]
mean_iou(pred, true, 2)  → ([0.75, 0.666...], 0.708...)    class 0: 3/4, class 1: 2/3
mean_iou(pred, true, 3)  → ([0.75, 0.666..., None], 0.708...)  class 2 absent everywhere: ignored

A 10×10 image that is all background (0) except a 2×2 object (1), and a model that predicts all 0:
pixel accuracy 0.96, per-class IoU [0.96, 0.0], mean IoU 0.48

mean_iou([[0, 1]], [[0]], 2)  → ValueError   shapes differ
mean_iou([[0, 3]], [[0, 1]], 2)  → ValueError   3 is not a class
```

## Constraints

- Masks are at most 256 × 256.
- Plain Python only; float results are checked to `1e-9`.

## Hints

1. For a single class `c`, how do you turn each mask into a yes/no region, and what are intersection and union of two such regions?
2. Can you count all classes' intersections and unions in a single pass over the pixel pairs?
3. What is the right IoU for a class that appears in neither mask, and why would `0` or `1` both distort the mean?
4. What goes into the mean for a class the model never predicted but the ground truth contains?

## Explain-back

- In the all-background example, why does pixel accuracy look excellent while mean IoU exposes the failure?
- Segmentation labels every pixel of a class with one id. Do you need one model per object to segment three cars? What is the difference between semantic and instance segmentation?
- Why are classes absent from both masks left out of the mean instead of scoring a perfect 1?
- A U-Net outputs a tensor of shape `(n_classes, H, W)`. How do you get from that to the `pred_mask` this function takes?
