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
    """Return the area of a Circle, Rectangle or Triangle without rounding."""
    raise NotImplementedError
