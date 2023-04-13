"""Minimax game player. You should modify the choose_move code for the
MinimaxPlayer class. You should also modify the heuristic function, which
should return a number indicating the value of that board position.

Feel free to add additional helper methods or functions.
"""

from __future__ import annotations
from game_board import GameBoard, Location
from typing import Optional, Callable
from player import Player


def heuristic(board: GameBoard) -> float:
    """Measure the value of the game board, where a high number means that is
    good for the max player, and a low number means that it is good for the min
    player. The maximum possible value should be 1, which is the value that
    should be returned if the board supplied is a guaranteed win for the max
    player. Likewise, the minimum possible value should be a -1, which is a
    guaranteed win for the min player.

    (The textbook indicates at some point in passing that this heuristic should
    range from 0 to 1, but there's no theoretical reason for 0 as opposed to -1
    for the bottom end, and the asymmetry just makes everything more
    complicated. What does matter is that the heuristic value for a
    non-terminal state should never be bigger in magnitude than that for an
    terminal state, because that would suggest that it the non-terminal state
    is more conclusive than a terminal state (which it can't be).
    """

    # This very silly heuristic just adds up all the 1s, -1s, and 0s
    # stored internally on the board, and then normalizes the result.
    sum = 0
    for row in range(1, board.size+1):
        for column in range(1, board.size+1):
            # The grid is stored as a numpy array for speed, so access
            # individual items (if you need to) via a comma as below
            sum += board.grid[row, column]

    maximum_magnitude = board.size**2
    return sum / maximum_magnitude


class MinimaxPlayer(Player):
    """Minimax player: uses minimax to find the best move."""

    def __init__(self,
                 heuristic: Callable[[GameBoard], float],
                 plies: int) -> None:
        self.heuristic = heuristic
        self.plies = plies

    def choose_move(self, board: GameBoard) -> Optional[Location]:
        raise NotImplementedError("You must implement this method")
