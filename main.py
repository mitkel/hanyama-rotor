from element import Element
from puzzle import Puzzle

# TODO: port to python 3.11
# TODO: add readme and publish repo

INITIAL_STATE = Puzzle(Element(2, 0, 1), Element(2, 0, 1))
GAOL_STATE = Puzzle(Element(0, 0, 1), Element(0, 0, 1))


def get_random_final():
    puzzle = Puzzle(golden=Element(1, 1), silver=Element(1, 2))
    final_state = puzzle
    for _ in range(10):
        final_state = final_state.random_move()
    
    return puzzle, final_state


def main(initial_state, final_state):
    path = initial_state.get_shortest_path(final_state=final_state)
    for v in path:
        print(v)


if __name__ == "__main__":
    main(INITIAL_STATE, GAOL_STATE)

