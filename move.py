from enum import Enum


class Move(str, Enum):
    SO = "Silver-outer"
    GO = "Golden-outer"
    GCO_SLH = "G-change-or; Silver-loop-hole"
    GLH_SCO = "Golden-loop-hole; S-change-or"
    GCO_SLT = "G-change-or; Silver-loop-thin"
    GLT_SCO = "Golden-loop-thin; S-change-or"

    def changes_or(self) -> bool:
        return self != Move.SO and self != Move.GO

    def tricky_move(self) -> bool:
        return self == Move.GCO_SLT or self == Move.GLT_SCO
