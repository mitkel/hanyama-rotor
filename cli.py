import argparse
from pathlib import Path

from returns.maybe import Some

from rotor.explore import find_shortest_path
from rotor.puzzle import Puzzle
from rotor.visualize import visualize_available_states


def main(initial_state_str: str, final_state_str: str, visualize: bool, save_path: Path) -> None:
    initial_state = Puzzle.from_str(initial_state_str).unwrap()
    final_state = Puzzle.from_str(final_state_str).unwrap()

    if visualize:
        visualize_available_states(initial_state, Some(save_path))

    path = find_shortest_path(initial_state=initial_state, final_state=final_state)
    for v in path:
        print(v)


if __name__ == "__main__":
    initial_state_str = Puzzle.initial_state().__str__()
    final_state_str = Puzzle.goal_state().__str__()
    parser = argparse.ArgumentParser(description="Puzzle Solver and Visualizer")
    parser.add_argument("--initial-state", type=str, default=initial_state_str, help="Initial state of the puzzle")
    parser.add_argument("--final-state", type=str, default=final_state_str, help="Final state of the puzzle")
    parser.add_argument("--visualize", action="store_true", help="Visualize the available state space")
    parser.add_argument("--save-path", type=Path, default=Path(""), help="Path to save the output")
    args = parser.parse_args()

    main(args.initial_state, args.final_state, args.visualize, args.save_path)
