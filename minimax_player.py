"""Minimax game player. You should modify the choose_move code for the
MinimaxPlayer class. You should also modify the heuristic function, which
should return a number indicating the value of that board position.

Feel free to add additional helper methods or functions.
"""

from __future__ import annotations
from game_board import GameBoard, Location
from typing import Optional, Callable
from player import Player
from common_values import (
    EMPTY, MAX_PLAYER, MIN_PLAYER, RED, RED_MARKER, YELLOW, YELLOW_MARKER,
    COLOR_NAMES)
from typing import Optional, List


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

    '''
    My idea is calculate number of possible moves of each players. Then who has more 
    possible moves  will be more likely to win
    '''
    # Get active player
    active_player = board.get_active_player()

    # If max_player plays:
    if (active_player == 1):
        num_legal_moves_for_max_player = len(board.get_legal_moves())
        num_legal_moves_for_min_player = len(
            get_legal_moves_for_other_player(board))

    else:
        num_legal_moves_for_max_player = len(
            get_legal_moves_for_other_player(board))
        num_legal_moves_for_min_player = len(board.get_legal_moves())

    if num_legal_moves_for_max_player + num_legal_moves_for_min_player <= 0:
        return 0
    # Our formula (difference between move)/(total of moves)
    return (num_legal_moves_for_max_player-num_legal_moves_for_min_player)/(num_legal_moves_for_max_player+num_legal_moves_for_min_player)


class MinimaxPlayer(Player):
    """Minimax player: uses minimax to find the best move."""

    def __init__(self,
                 heuristic: Callable[[GameBoard], float],
                 plies: int) -> None:
        self.heuristic = heuristic
        self.plies = plies

    def choose_move(self, board: GameBoard) -> Optional[Location]:
        # Get player
        player = board.get_active_player()
        # If player 1, plays max_value
        if player == 1:
            value, move = self.max_value(self.plies, board)
        else:
            value, move = self.min_value(self.plies, board)
        return move

    def max_value(self, depth, board):
        # Value of the Node
        value = heuristic(board)

        list_moves = board.get_legal_moves()
        v, new_move = float("-inf"), None
        v2 = float("-inf")

        for move in list_moves:
            temp_board = board.copy()
            new_board = temp_board.make_move(move)
            # If there is more plies
            if depth > 0:
                v2, a2 = self.min_value(depth-1, new_board)
            # If there is no plies
            else:
                v2 = value
            if v2 > v:
                v, new_move = v2, move
        return v, new_move

    def min_value(self, depth, board):
        # Value of the Node
        value = heuristic(board)

        list_moves = board.get_legal_moves()
        v, new_move = float("inf"), None
        v2 = float("inf")

        for move in list_moves:
            temp_board = board.copy()
            new_board = temp_board.make_move(move)
            # If there is more plies
            if depth > 0:
                v2, a2 = self.max_value(depth-1, new_board)
            # If there is no plies
            else:
                v2 = value
            if v2 < v:
                v, new_move = v2, move
        return v, new_move


def is_legal_move_for_other_player(board, location) -> bool:
    ''' Returns whether or not move is legal.'''
    row = location.row
    col = location.column
    piece = -board.get_active_player()

    # A move cannot be made if a piece is already there.
    if board.grid[row][col] != EMPTY:
        return False

    # A move cannot be made if the piece "value" is not red or yellow.
    if piece != YELLOW and piece != RED:
        return False

    # Extra restrictions once initial stage is over
    if (board.in_second_stage() and
            board.num_adjacent_friendlies(location, piece) < 2):
        return False

    return True


def get_legal_moves_for_other_player(board) -> List[Location]:
    """Returns a list of Locations that represent legal moves that can be
    made.
    """

    legal_moves = []
    for row in range(1, board.size+1):
        for column in range(1, board.size+1):
            location = Location(row, column)
            if is_legal_move_for_other_player(board, location):
                legal_moves.append(location)
    return legal_moves
