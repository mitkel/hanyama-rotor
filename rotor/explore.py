from typing import NamedTuple, Sequence, TypeAlias

from returns.maybe import Maybe, Nothing, Some

from rotor.puzzle import Puzzle

P: TypeAlias = Puzzle


class DijkstraStep(NamedTuple):
    visited: list[P]
    unvisited: list[P]
    distances: dict[P, float]
    prev: dict[P, P]
    prev_move: dict[P, str]

    def get_distance_to(self, state: P) -> float:
        return self.distances.get(state, float("inf"))


def explore_puzzle(step: DijkstraStep) -> DijkstraStep:
    """Applies Dijkstra's algorithm to find distances to all unvisited states."""
    if len(step.unvisited) == 0:
        return step

    min_dist = min([step.get_distance_to(s) for s in step.unvisited])
    active_state = [s for s in step.unvisited if step.get_distance_to(s) == min_dist][0]
    step.unvisited.remove(active_state)
    step.visited.append(active_state)

    for next_state_candidate, move in active_state.next_states():
        if next_state_candidate in step.visited:
            continue
        # next_state_candidate not visited
        if next_state_candidate not in step.unvisited:
            step.unvisited.append(next_state_candidate)
        dist = min_dist + 1.0
        if dist < step.get_distance_to(next_state_candidate):
            step.distances.update({next_state_candidate: dist})
            step.prev.update({next_state_candidate: active_state})
            step.prev_move.update({next_state_candidate: move.value})

    return explore_puzzle(step)


def explore_puzzle_from(initial_state: P) -> DijkstraStep:
    """Runs Dijkstra's algorithm to find distances to all states reachable from the initial state."""
    return explore_puzzle(
        DijkstraStep(
            visited=[],
            unvisited=[initial_state],
            distances={initial_state: 0.0},
            prev={initial_state: initial_state},
            prev_move={initial_state: ""},
        )
    )


def find_shortest_path(initial_state: P, final_state: P) -> Maybe[Sequence[tuple[P, str]]]:
    """Returns a list of (state, move) pairs that form the shortest path from the initial state to the final state."""
    final_dijkstra_step = explore_puzzle_from(initial_state)
    if final_state not in final_dijkstra_step.visited:
        return Nothing

    state, move = final_state, ""
    path: list[tuple["Puzzle", str]] = []
    while state != initial_state:
        path = [(state, move)] + path
        move = final_dijkstra_step.prev_move[state]
        state = final_dijkstra_step.prev[state]

    return Some([(state, move)] + path)
