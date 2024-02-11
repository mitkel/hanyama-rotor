from dataclasses import dataclass
from typing import Iterator

from returns.result import Result

from rotor.element import Element
from rotor.move import Move


@dataclass(frozen=True, slots=True)
class Puzzle:
    golden: Element
    silver: Element

    def __repr__(self) -> str:
        return f"{self.golden}{self.silver}"

    @classmethod
    def from_str(cls, s: str) -> Result["Puzzle", Exception]:
        golden, silver = Element.from_str(s[:3]), Element.from_str(s[3:])
        return Result.do(Puzzle(g, s) for g in golden for s in silver)

    @classmethod
    def initial_state(cls) -> "Puzzle":
        return cls(Element(2, 0, 1), Element(2, 0, 1))

    @classmethod
    def goal_state(cls) -> "Puzzle":
        return cls(Element(0, 0, 1), Element(0, 0, 1))

    def next_states(self) -> Iterator[tuple["Puzzle", Move]]:
        yield Puzzle(self.golden.move_inner(), self.silver.move_outer()), Move.SO
        yield Puzzle(self.golden.move_outer(), self.silver.move_inner()), Move.GO
        if self.silver.outer == 2:
            yield Puzzle(self.golden.change_or(), self.silver.move_inner()), Move.GCO_SLH
        if self.golden.outer == 2:
            yield Puzzle(self.golden.move_inner(), self.silver.change_or()), Move.GLH_SCO
        if self.silver.outer == 1 and self.golden.outer == 1:
            yield Puzzle(self.golden.change_or(), self.silver.move_inner()), Move.GCO_SLT
            yield Puzzle(self.golden.move_inner(), self.silver.change_or()), Move.GLT_SCO
