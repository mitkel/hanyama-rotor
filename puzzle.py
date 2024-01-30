from collections import defaultdict
from dataclasses import dataclass
from typing import Iterator, Optional, Sequence

import numpy as np

from element import Element


@dataclass(frozen=True)
class Puzzle:
    golden: Element = Element()
    silver: Element = Element()

    def next_states(self) -> Iterator[tuple["Puzzle", str]]:
        yield Puzzle(self.golden.move_inner(), self.silver.move_outer()), "Silver-outer"
        yield Puzzle(self.golden.move_outer(), self.silver.move_inner()), "Golden-outer"
        if self.silver.outer == 2:
            yield Puzzle(self.golden.change_or(), self.silver.move_inner()), "G-change-or; Silver-loop-hole"
        if self.golden.outer == 2:
            yield Puzzle(self.golden.move_inner(), self.silver.change_or()), "Golden-loop-hole; S-change-or"
        if self.silver.outer == 1 and self.golden.outer == 1:
            yield Puzzle(self.golden.change_or(), self.silver.move_inner()), "G-change-or; Silver-loop-thin"
            yield Puzzle(self.golden.move_inner(), self.silver.change_or()), "Golden-loop-thin; S-change-or"


    def random_move(self):
        return np.random.choice([s for s, _ in self.next_states()])

    def explore_states(self):
        default_distances = defaultdict(lambda: float("inf"))
        default_distances[self] = 0
        return self._explore_states(
            visited=[],
            unvisited=[s for s, _ in self.next_states()],
            distances=default_distances,
            prev=defaultdict(lambda: None),
            prev_move=defaultdict(lambda: ""),
        )

    def _explore_states(
        self,
        visited: list["Puzzle"],
        unvisited: list["Puzzle"],
        distances: dict["Puzzle", int],
        prev: dict["Puzzle", Optional["Puzzle"]],
        prev_move: dict["Puzzle", str],
    ) -> tuple[list["Puzzle"], dict["Puzzle", int], dict["Puzzle", Optional["Puzzle"]]]:
        if len(unvisited) == 0:
            return visited, distances, prev, prev_move

        min_dist = min([distances[s] for s in unvisited])
        active_state = [s for s in unvisited if distances[s] == min_dist][0]
        unvisited.remove(active_state)
        visited.append(active_state)

        for next_state_candidate, move in active_state.next_states():
            if next_state_candidate in visited:
                continue

            # next_state_candidate not visited
            unvisited.append(next_state_candidate)
            dist = min_dist + 1
            if dist < distances[next_state_candidate]:
                distances.update({next_state_candidate: dist})
                prev.update({next_state_candidate: active_state})
                prev_move.update({next_state_candidate: move})

        return active_state._explore_states(visited, unvisited, distances, prev, prev_move)

    def get_shortest_path(self, final_state: "Puzzle") -> Sequence[tuple["Puzzle", str]]:
        visited, _, prev, prev_move = self.explore_states()
        if final_state not in visited:
            print("Final state is unattainable")
            return []

        state = final_state
        move = ""
        path = []
        while state != self:
            path = [(state, move)] + path
            move = prev_move[state]
            state = prev[state]

        return [(state, move)] + path
