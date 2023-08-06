from __future__ import annotations

from lirpy.point import Point


class Rect:
    def __init__(
        self, xmin: int = 0, ymin: int = 0, xmax: int = 0, ymax: int = 0
    ) -> None:
        self.min: Point = Point(xmin, ymin)
        self.max: Point = Point(xmax, ymax)

    @property
    def width(self) -> int:
        return self.max.x - self.min.x

    @property
    def height(self) -> int:
        return self.max.y - self.min.y

    def normalize(self) -> Rect:
        return Rect(
            xmin=min(self.min.x, self.max.x),
            xmax=max(self.min.x, self.max.x),
            ymin=min(self.min.y, self.max.y),
            ymax=max(self.min.y, self.max.y),
        )
