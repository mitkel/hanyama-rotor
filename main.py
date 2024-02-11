from rotor.explore import find_shortest_path
from rotor.puzzle import Puzzle
from rotor.visualize import visualize_available_states


def main(initial_state: Puzzle, final_state: Puzzle) -> None:
    path = find_shortest_path(initial_state=initial_state, final_state=final_state)
    for v in path:
        print(v)


if __name__ == "__main__":
    visualize_available_states(Puzzle.initial_state())
    main(Puzzle.initial_state(), Puzzle.goal_state())
