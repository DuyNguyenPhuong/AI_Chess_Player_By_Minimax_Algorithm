"""Human player. When prompted to choose a move, it communicates with the user
via the terminal to oobtain a proper move.

You should not modify any of this code.
"""


from game_board import Location
from typing import Optional
from player import Player


class HumanPlayer(Player):
    """Interactive player: prompts the user to make a move."""

    def choose_move(self, board) -> Optional[Location]:
        while True:
            try:
                move = eval('(' + input(
                 'enter row, column (or type "0,0" to pass): ')
                 + ')')

                if (len(move) == 2
                    and type(move[0]) == int and type(move[1]) == int
                    and (move[0] in range(1, board.size+1) and
                         move[1] in range(1, board.size+1)
                         or move == (0, 0))):
                    break

                print('Illegal entry, try again.')
            except Exception:
                print('Illegal entry, try again.')

        if move == (0, 0):
            return None
        else:
            return Location(move[0], move[1])
