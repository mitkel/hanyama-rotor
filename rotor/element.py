from dataclasses import dataclass

from returns.result import Failure, Result, Success


@dataclass(frozen=True, slots=True)
class Element:
    inner: int
    outer: int
    is_positive_oriented: bool

    def __post_init__(self) -> None:
        diff = (self.outer - self.inner) % 3
        if diff == 2:
            raise ValueError(f"Impossible element position {self}")

    def __str__(self) -> str:
        orientation_sign = "+" if self.is_positive_oriented else "-"
        return f"{orientation_sign}{self.inner % 3}{self.outer % 3}"

    @classmethod
    def from_str(cls, s: str) -> Result["Element", ValueError]:
        if len(s) != 3 or s[1] not in "012" or s[2] not in "012" or s[0] not in "+-":
            return Failure(ValueError(f"Invalid element description {s}"))
        inner = int(s[1])
        outer = int(s[2])
        return Success(Element(inner, outer, s[0] == "+"))

    @property
    def rel_orientation(self) -> int:
        diff = (self.outer - self.inner) % 3
        if diff == 0:
            return 1
        else:  # diff = 1 (2 is impossible due to __post_init__ validation)
            return -1

    def move_inner(self) -> "Element":
        new_inner = (self.inner - self.rel_orientation) % 3
        return Element(inner=new_inner, outer=self.outer, is_positive_oriented=self.is_positive_oriented)

    def move_outer(self) -> "Element":
        new_outer = (self.outer + self.rel_orientation) % 3
        return Element(inner=self.inner, outer=new_outer, is_positive_oriented=self.is_positive_oriented)

    def change_or(self) -> "Element":
        return Element(inner=self.inner, outer=self.outer, is_positive_oriented=not self.is_positive_oriented)
