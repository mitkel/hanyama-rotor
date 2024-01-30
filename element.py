from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class Element:
    inner: Literal[0, 1, 2] = 0
    outer: Literal[0, 1, 2] = 0
    orientation: Literal[-1, 1] = 1

    @property
    def rel_orientation(self) -> int:
        diff = (self.outer - self.inner) % 3
        if diff == 0:
            return 1
        elif diff == 1:
            return -1
        raise ValueError(f"Impossible position {self}")

    def move_inner(self):
        new_inner = (self.inner - self.rel_orientation) % 3
        return Element(inner=new_inner, outer=self.outer, orientation=self.orientation)

    def move_outer(self):
        new_outer = (self.outer + self.rel_orientation) % 3
        return Element(inner=self.inner, outer=new_outer, orientation=self.orientation)

    def change_or(self):
        return Element(inner=self.inner, outer=self.outer, orientation=-self.orientation)
