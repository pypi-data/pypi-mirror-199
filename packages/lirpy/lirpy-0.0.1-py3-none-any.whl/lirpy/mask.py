from typing import Callable, List, Tuple
from lirpy.rect import Rect


class Mask:
    def __init__(self, height: int, width: int) -> None:
        self.width: int = width
        self.height: int = height
        self.data: List[bool] = [False] * (self.height * self.width)

    def xy2idx(self, x: int, y: int) -> int:
        return x + (y * self.height)

    def idx2xy(self, i: int) -> Tuple[int, int]:
        y, x = divmod(i, self.height)
        return x, y

    def has_true_areas_left(self) -> bool:
        return any(self.data)

    def set(self, x: int, y: int, value: bool) -> None:
        self.data[self.xy2idx(x, y)] = value

    def get(self, x: int, y: int) -> bool:
        return self.data[self.xy2idx(x, y)]

    def setif(self, c: Callable[[int, int, bool], bool]) -> None:
        for i in range(len(self.data)):
            x, y = self.idx2xy(i)
            self.data[i] = c(x, y, self.data[i])

    def dump(self) -> None:
        # from rich import console
        for y in range(self.height):
            row: List[bool] = []
            for x in range(self.width):
                row.append(self.get(x, y))
            print("".join(["█" if v else " " for v in row]))

    def maskOffFromRect(self, rect: Rect) -> None:
        for y in range(self.height):
            for x in range(self.width):
                if rect.min.x <= x <= rect.max.x and rect.min.y <= y <= rect.max.y:
                    self.data[self.xy2idx(x, y)] = False
