# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import math


def days_to_escape(depth: int, climb: int, slide: int) -> int:
    if climb >= depth:
        return 1
    if climb <= slide:
        return -1
    # Before the last day the snail must reach depth - climb; each full day gains climb - slide.
    return math.ceil((depth - climb) / (climb - slide)) + 1
