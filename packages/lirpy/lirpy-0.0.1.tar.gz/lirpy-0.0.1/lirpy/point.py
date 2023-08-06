from math import sqrt
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


def dist_points(a: Point, b: Point) -> float:
    return sqrt(((float(b.x) - float(a.x)) ** 2) + ((float(b.y) - float(a.y)) ** 2))
