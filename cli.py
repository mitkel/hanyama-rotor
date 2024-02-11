import argparse
from pathlib import Path

from returns.maybe import Some

from rotor.explore import find_shortest_path
from rotor.puzzle import Puzzle
from rotor.visualize import visualize_available_states


def main(initial_state: Puzzle, final_state: Puzzle, visualize: bool, save_path: Path) -> None:
    if visualize:
        visualize_available_states(initial_state, Some(save_path))

    path = find_shortest_path(initial_state=initial_state, final_state=final_state)
    for v in path:
        print(v)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Puzzle Solver and Visualizer")
    parser.add_argument("--visualize", action="store_true", help="Visualize the available state space")
    parser.add_argument("--save-path", type=Path, default=Path(""), help="Path to save the output")
    args = parser.parse_args()

    initial_state = Puzzle.initial_state()
    final_state = Puzzle.goal_state()

    main(initial_state, final_state, args.visualize, args.save_path)
