"""Abstract class representing a game player. This is overridden by the various
different players in the assignment.

You should not modify any of this code.
"""

from abc import abstractmethod
from typing import Optional
from game_board import Location


class Player:

    @abstractmethod
    def choose_move(self, board) -> Optional[Location]:
        assert True, "choose_move base method should never be called."
        return None
