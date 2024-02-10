from dataclasses import dataclass
from typing import Literal, Self


@dataclass(frozen=True)
class Element:
    inner: int = 0
    outer: int = 0
    orientation: Literal[-1, 1] = 1

    def __post_init__(self) -> None: ...

    def __str__(self) -> str:
        return f"{self.inner}{self.outer}{self.orientation}"

    @property
    def rel_orientation(self) -> int:
        diff = (self.outer - self.inner) % 3
        if diff == 0:
            return 1
        elif diff == 1:
            return -1
        raise ValueError(f"Impossible position {self}")

    def move_inner(self) -> Self:
        new_inner = (self.inner - self.rel_orientation) % 3
        return self.__class__(inner=new_inner, outer=self.outer, orientation=self.orientation)

    def move_outer(self) -> Self:
        new_outer = (self.outer + self.rel_orientation) % 3
        return self.__class__(inner=self.inner, outer=new_outer, orientation=self.orientation)

    def change_or(self) -> Self:
        return self.__class__(inner=self.inner, outer=self.outer, orientation=-self.orientation)
