from pathlib import Path
from typing import TypeAlias

import networkx as nx
from matplotlib import pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout
from pyvis.network import Network
from returns.maybe import Maybe, Nothing

from rotor.explore import explore_puzzle_from
from rotor.move import Move
from rotor.puzzle import Puzzle

P: TypeAlias = Puzzle
default_save_path = Path(__file__).parent.parent / "res"


def visualize_available_states(initial_state: P, save_path: Maybe[Path] = Nothing) -> None:
    graph = nx.Graph()
    available_states = explore_puzzle_from(initial_state).visited
    for state in available_states:
        for neighbour, move in state.next_states():
            edge = (str(state), str(neighbour))
            if graph.has_edge(*edge):
                continue
            graph.add_edge(
                *edge, len=_get_edge_length(move), color=_get_edge_color(move), weight=_get_edge_weight(move)
            )

    pos = graphviz_layout(graph)
    edge_colors = [graph[u][v]["color"] for u, v in graph.edges]
    node_colors = [_get_node_color(u) for u in graph.nodes]
    nx.draw(graph, pos, node_size=100, font_size=5, edge_color=edge_colors, node_color=node_colors, with_labels=True)
    nt = Network("800px", width="100%", filter_menu=True, layout=False)
    nt.show_buttons(filter_=["nodes"])
    nt.from_nx(graph, default_node_size=20)

    final_save_path = save_path.value_or(default_save_path)
    final_save_path.mkdir(parents=True, exist_ok=True)
    plt.savefig(final_save_path / "graph.pdf")
    # TODO: for some reasone writing to the final_save_path is not working
    nt.write_html("graph.html")


def _get_node_color(node: str) -> str:
    if node == str(Puzzle.initial_state()):
        return "y"
    elif node == str(Puzzle.goal_state()):
        return "tomato"
    else:
        return "lightblue"


def _get_edge_color(move: Move) -> str:
    if not move.changes_or():
        return "blue"
    elif not move.tricky_move():
        return "green"
    else:
        return "red"


def _get_edge_length(move: Move) -> int:
    if move.changes_or():
        return 100
    else:
        return 25


def _get_edge_weight(move: Move) -> int:
    if move.changes_or():
        return 3
    else:
        return 6
