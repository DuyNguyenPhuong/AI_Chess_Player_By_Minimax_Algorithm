from __future__ import annotations
from common_values import (
    EMPTY, MAX_PLAYER, MIN_PLAYER, RED, RED_MARKER, YELLOW, YELLOW_MARKER,
    COLOR_NAMES)
from typing import Optional, List
import numpy as np
import random
from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class Location:
    row: int
    column: int


class GameBoard:
    """A game board, with a variety of methods for managing a game. We'll
    sometimes also refer to the board as a _state_. Note that this is different
    from a _move_, which is the location to which you would place the next
    piece. A move, when made, transitions you to a different board/state.
    """

    # Number of boards made (incremented in __init__). Can serve as an
    # approximate proxy for measuring how many states are measured.
    _num_boards_made = 0

    def __init__(self, size, array: Optional[np.ndarray] = None,
                 pieces_placed=None) -> None:
        '''If the parameter 'board' is left out, then the game board is
        initialized to its typical starting postion. Alternatively, a
        two-dimensional list with a pre-existing starting position can be
        supplied as well. Note that the size of the board is
        (self.size+2)x(self.size+2), instead of self.sizexself.size; this is
        because leaving a ring around the edge of the board makes the rest of
        the code much simpler. '''

        GameBoard._num_boards_made += 1

        self.size = size

        if array is not None:
            self.grid: np.ndarray = array.copy()
        else:
            self.grid = np.ones((self.size+2, self.size+2)) * EMPTY

        # Tracks number of pieces placed by each player, so as to determine
        # whether in first stage of the same or second. Can also be used to
        # determine whose turn it is.
        if pieces_placed:
            # self.pieces_placed = copy.deepcopy(pieces_placed)
            self.pieces_placed = {}
            self.pieces_placed[MAX_PLAYER] = pieces_placed[MAX_PLAYER]
            self.pieces_placed[MIN_PLAYER] = pieces_placed[MIN_PLAYER]
        else:
            self.pieces_placed = {MAX_PLAYER: 0, MIN_PLAYER: 0}

    @classmethod
    def get_num_boards_made(cls) -> int:
        return GameBoard._num_boards_made

    def get_active_player(self) -> int:
        """Return MAX_PLAYER or MIN_PLAYER, depending on whose turn it is.
        Assumes MAX_PLAYER goes first."""

        if (self.pieces_placed[MAX_PLAYER]
                == self.pieces_placed[MIN_PLAYER]):
            return MAX_PLAYER
        elif (self.pieces_placed[MAX_PLAYER]
                == self.pieces_placed[MIN_PLAYER]+1):
            return MIN_PLAYER
        else:
            raise Exception("Pieces placed is inconsistent.")

    def copy(self) -> GameBoard:
        boardCopy = GameBoard(self.size, self.grid, self.pieces_placed)
        return boardCopy

    def display(self) -> None:
        '''Displays the current board to the terminal window, with
        headers across the left and top. While some might accuse this
        text output as being "old school," having a scrollable game
        history actually makes debugging much easier.'''
        print('\n\n')
        print(' ', end=' ')
        for i in range(1, self.size+1):
            print(i, end=' ')
        print()
        for i in range(1, self.size+1):
            print(i, end=' ')
            for j in range(1, self.size+1):
                if self.grid[i][j] == RED:
                    print(RED_MARKER, end=' ')
                elif self.grid[i][j] == YELLOW:
                    print(YELLOW_MARKER, end=' ')
                else:
                    print('-', end=' ')
            print()
        print('Player to make move: ' + COLOR_NAMES[self.get_active_player()])
        if (self.in_second_stage()):
            print("In second stage")
        else:
            print("In first stage")

    def num_adjacent_friendlies(self, location, piece) -> int:
        '''Counts the number of friendly pieces that are orthogonal or diagonal
        to the provided location.'''
        row = location.row
        col = location.column
        numAdjacentFriendlies = 0
        for rowIncrement in [-1, 0, 1]:
            for colIncrement in [-1, 0, 1]:
                if rowIncrement == 0 and colIncrement == 0:
                    continue
                if self.grid[row + rowIncrement][col + colIncrement] == piece:
                    numAdjacentFriendlies += 1
        return numAdjacentFriendlies

    def in_second_stage(self) -> bool:
        return (self.pieces_placed[MAX_PLAYER] >= self.size-1 and
                self.pieces_placed[MIN_PLAYER] >= self.size-1)

    def is_legal_move(self, location) -> bool:
        ''' Returns whether or not move is legal.'''
        row = location.row
        col = location.column
        piece = self.get_active_player()

        # A move cannot be made if a piece is already there.
        if self.grid[row][col] != EMPTY:
            return False

        # A move cannot be made if the piece "value" is not red or yellow.
        if piece != YELLOW and piece != RED:
            return False

        # Extra restrictions once initial stage is over
        if (self.in_second_stage() and
                self.num_adjacent_friendlies(location, piece) < 2):
            return False

        return True

    def make_move(self, location) -> Optional[GameBoard]:
        ''' Returns None if move is not legal. Otherwise returns an
        updated board, which is a copy of the original.'''

        piece = self.get_active_player()
        if not self.is_legal_move(location):
            return None

        # Make a copy of the board (not just the pointer!) and record move
        boardCopy = self.copy()
        row = location.row
        col = location.column
        boardCopy.grid[row][col] = piece
        boardCopy.pieces_placed[piece] += 1

        return boardCopy

    def get_randomized_moves(self) -> List[Location]:
        """Returns a randomly ordered list of all Locations on this board.
        Note that these are not necessarily legal moves.
        """

        moves = []
        for row in range(1, self.size+1):
            for column in range(1, self.size+1):
                location = Location(row, column)
                moves.append(location)
        random.shuffle(moves)
        return moves

    def get_random_legal_move(self) -> Optional[Location]:
        """Returns a randomly chosen legal move. Returns None if none are
        possible.
        """

        moves = self.get_randomized_moves()
        for move in moves:
            if self.is_legal_move(move):
                return move
        return None

    def get_legal_moves(self) -> List[Location]:
        """Returns a list of Locations that represent legal moves that can be
        made.
        """

        legal_moves = []
        for row in range(1, self.size+1):
            for column in range(1, self.size+1):
                location = Location(row, column)
                if self.is_legal_move(location):
                    legal_moves.append(location)
        return legal_moves

    def is_terminal(self):
        """Returns True if this is a terminal state, i.e. the current player
        cannot move. Otherwise, returns False. Make sure to notice that this
        function calls get_legal_moves, so it is slow to call both
        this function and get_legal_moves if you need to do both.
        """

        return len(self.get_legal_moves()) == 0

    def value(self) -> int:
        """Returns 0 if the state hasn't been won by anyone, returns 1 if it's
        a win for the first player (i.e., the first player just made a move
        that resulted in this state, which is a win for the first player), and
        returns -1 if it's a win for the second player.
        """
        if len(self.get_legal_moves()) > 0:
            return 0

        if self.get_active_player() == MIN_PLAYER:
            return 1

        return -1
