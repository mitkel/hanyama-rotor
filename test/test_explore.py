from returns.maybe import Nothing, Some

from rotor.explore import find_shortest_path
from rotor.puzzle import Puzzle


class TestExplore:
    initial_state = Puzzle.initial_state()
    goal_state = Puzzle.goal_state()
    invalid_goal_state = Puzzle.from_str("+00-00").unwrap()

    def test_find_shortest_path_success(self) -> None:
        path_len = find_shortest_path(self.initial_state, self.goal_state).map(len)
        assert path_len == Some(12)

    def test_find_shortest_path_failure(self) -> None:
        path = find_shortest_path(self.initial_state, self.invalid_goal_state)
        assert path == Nothing
