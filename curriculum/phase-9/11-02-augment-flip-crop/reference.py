# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import random


def augment_flip_crop(img: list[list[float]], rng: random.Random, crop: int) -> list[list[float]]:
    h, w = len(img), len(img[0])
    if crop < 1 or crop > h or crop > w:
        raise ValueError("crop must be between 1 and the image size")
    rows = [row[::-1] for row in img] if rng.random() < 0.5 else [list(row) for row in img]
    top = rng.randint(0, h - crop)
    left = rng.randint(0, w - crop)
    return [row[left:left + crop] for row in rows[top:top + crop]]
