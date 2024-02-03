from puzzle import Puzzle


def main(initial_state: Puzzle, final_state: Puzzle):
    path = initial_state.get_shortest_path(final_state=final_state)
    for v in path:
        print(v)


if __name__ == "__main__":
    Puzzle.goal_state().visualize_states()
    main(Puzzle.initial_state(), Puzzle.goal_state())