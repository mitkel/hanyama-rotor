from collections import defaultdict
from dataclasses import dataclass
from typing import Iterator, Optional, Sequence

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from networkx.drawing.nx_agraph import graphviz_layout

from element import Element
from move import Move


@dataclass(frozen=True)
class Puzzle:
    golden: Element = Element()
    silver: Element = Element()

    def __str__(self):
        return f"{self.golden}-{self.silver}"

    @classmethod
    def initial_state(cls) -> "Puzzle":
        return Puzzle(Element(2, 0, 1), Element(2, 0, 1))

    @classmethod
    def goal_state(cls) -> "Puzzle":
        return Puzzle(Element(0, 0, 1), Element(0, 0, 1))

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

    def explore_states(self) -> tuple[list["Puzzle"], dict["Puzzle", int], dict["Puzzle", Optional["Puzzle"]]]:
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
        unvisited = [s for s in unvisited if s != active_state]
        visited.append(active_state)

        for next_state_candidate, move in active_state.next_states():
            if next_state_candidate in visited:
                continue

            # next_state_candidate not visited
            if next_state_candidate not in unvisited:
                unvisited.append(next_state_candidate)
            dist = min_dist + 1
            if dist < distances[next_state_candidate]:
                distances.update({next_state_candidate: dist})
                prev.update({next_state_candidate: active_state})
                prev_move.update({next_state_candidate: move.value})

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

    def visualize_states(self) -> None:
        def get_node_color(node: str) -> str:
            if node == str(Puzzle.initial_state()):
                return "y"
            elif node == str(Puzzle.goal_state()):
                return "tomato"
            else:
                return "lightblue"

        def get_edge_color(move: Move) -> str:
            if not move.changes_or():
                return "blue"
            elif not move.tricky_move():
                return "green"
            else:
                return "red"

        def get_length(move: Move) -> int:
            if move.changes_or():
                return 100
            else:
                return 35

        graph = nx.Graph()
        node_colors = []
        available_states, _, _, _ = self.explore_states()
        for state in available_states:
            for neighbour, move in state.next_states():
                edge = (str(state), str(neighbour))
                if graph.has_edge(*edge):
                    continue
                for state in edge:
                    if not graph.has_node(state):
                        node_colors.append(get_node_color(state))
                graph.add_edge(*edge, len=get_length(move), color=get_edge_color(move))

        pos = graphviz_layout(graph)
        edge_colors = [graph[u][v]["color"] for u, v in graph.edges]
        nx.draw(
            graph, pos, node_size=100, font_size=5, edge_color=edge_colors, node_color=node_colors, with_labels=True
        )
        plt.savefig("graph.png")
        plt.savefig("graph.pdf")
