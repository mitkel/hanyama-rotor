from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True, slots=True)
class Element:
    inner: int
    outer: int
    orientation: Literal[-1, 1]

    def __post_init__(self) -> None: ...

    def __str__(self) -> str:
        orientation_sign = "+" if self.orientation == 1 else "-"
        return f"{orientation_sign}{self.inner}{self.outer}"

    @property
    def rel_orientation(self) -> int:
        diff = (self.outer - self.inner) % 3
        if diff == 0:
            return 1
        elif diff == 1:
            return -1
        raise ValueError(f"Impossible position {self}")

    def move_inner(self) -> "Element":
        new_inner = (self.inner - self.rel_orientation) % 3
        return Element(inner=new_inner, outer=self.outer, orientation=self.orientation)

    def move_outer(self) -> "Element":
        new_outer = (self.outer + self.rel_orientation) % 3
        return Element(inner=self.inner, outer=new_outer, orientation=self.orientation)

    def change_or(self) -> "Element":
        return Element(inner=self.inner, outer=self.outer, orientation=-self.orientation)
