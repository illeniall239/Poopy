# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import math
from dataclasses import dataclass
from typing import Union


@dataclass
class Circle:
    radius: float


@dataclass
class Rectangle:
    width: float
    height: float


@dataclass
class Triangle:
    base: float
    height: float


Shape = Union[Circle, Rectangle, Triangle]


def area(shape: Shape) -> float:
    if isinstance(shape, Circle):
        return math.pi * shape.radius * shape.radius
    if isinstance(shape, Rectangle):
        return shape.width * shape.height
    return shape.base * shape.height / 2
