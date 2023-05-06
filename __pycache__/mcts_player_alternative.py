"""MCTS game player starter code. Fill in the methods as indicated below.

Feel free to add additional helper methods or functions.

Originally based on work by:
@author Bryce Wiedenbeck
@author Anna Rafferty
@author Dave Musicant
"""

from __future__ import annotations
import random
from game_board import GameBoard, Location
from typing import Optional
from player import Player
import math
import numpy


class MctsPlayer(Player):
    """Uses MCTS to find the best move.

    Plays random games from the root node to a terminal state. In each playout,
    play proceeds according to UCB while all children have been expanded. The
    first node with unexpanded children has a random child expanded. After
    expansion, play proceeds by selecting uniform random moves. Upon reaching a
    terminal state, values are propagated back along the expanded portion of
    the path. After all playouts are completed, the move generating the highest
    value child of root is returned.
    """

    def __init__(self, playouts, ucb_const):
        self.playouts = playouts
        self.ucb_const = math.sqrt(2)

    def choose_move(self, board) -> Optional[Location]:
        root = MctsNode(board, None, self.ucb_const)
        return root.choose_move_via_mcts(self.playouts)


class MctsNode:
    """Node used in MCTS. It is a wrapper to contain a board/state as a node
    within a tree."""

    def __init__(self, state: GameBoard, parent: Optional[MctsNode],
                 ucb_const: float) -> None:
        """Constructor for a new node representing game state
        state. parent_node is the Node that is the parent of this
        one in the MCTS tree.
        """

        self.state = state
        self.parent = parent
        self.ucb_const = ucb_const

        # All of the known children for this node. To get to each child, a move
        # (specificed by a Location) is used.
        self.children: dict[Location, MctsNode] = {}

        # Stats of games played out from this node, from the perspective of the
        # player at this node.
        self.wins_for_this_player = 0
        self.total_games_for_this_player = 0

        # All legal moves that can me made from this node; useful to have once
        # to avoid recalculating later. Your code will be faster if you use
        # this value rather than calculating it when you need it.
        self.legal_moves = self.state.get_legal_moves()

        # You may add additional fields if needed below.
        self.is_expanded = False

    def get_win_percentage_if_chosen_by_parent(self) -> float:
        """Gets the win percentage for the current node, from the perspective
        of the parent node that is trying to decide whether or not to select
        this node.

        You will need this for computing the UCB weight when doing playouts,
        and also for making the final choice on which move to make.
        """

        """
        My Implementation: I have finsihed this function
        """
        if self.total_games_for_this_player == 0:
            return 0

        return 1 - (self.wins_for_this_player/self.total_games_for_this_player)

    def get_UCB_weight_from_parent_perspective(self) -> float:
        """Weight from the UCB formula for this node, when used by its parent
        to select a node proportionally to its weight. The win percentage
        aspect of this formula must be from the parent's perspective, since
        that is the node making the decision.

        You will need to use this as part of the selection phase when doing
        playouts.
        """

        """
        My Implementation: I finsished this function
        """
        parent = self.parent

        if (parent.total_games_for_this_player == 0 or self.total_games_for_this_player == 0):
            return 0

        return self.get_win_percentage_if_chosen_by_parent() + self.ucb_const * \
            math.sqrt(numpy.log(parent.total_games_for_this_player) /
                      self.total_games_for_this_player)

    def update_play_counts(self, outcome: int) -> None:
        """Updates the total games played from this node, as well as the number
        of wins from this node for the current player.

        You will need this for backpropagating wins/losses back up the tree.

        outcome: +1 for 1st player win, -1 for 2nd player win.
        """
        temp_node = self
        # Update from final node to the root
        while (temp_node != None):
            temp_node.total_games_for_this_player += 1
            if (temp_node.state.get_active_player() == outcome):
                temp_node.wins_for_this_player += 1
            temp_node = temp_node.parent

    def choose_move_via_mcts(self, playouts: int) -> Optional[Location]:
        """Select a move by Monte Carlo tree search. Plays playouts random
        games from the root node to a terminal state. In each playout, play
        proceeds according to UCB while all children have been expanded. The
        first node with unexpanded children has a random child expanded. After
        expansion, play proceeds by selecting uniform random moves. Upon
        reaching a terminal state, values are propagated back along the
        expanded portion of the path. After all playouts are completed, the
        move generating the highest value child of root is returned.

        Returns None if no legal moves are available. If playouts is 0, returns
        a random choice from the legal moves.

        You will undoubtedly want to use helper functions when writing this,
        both some that I've provided, as well as helper functions of your own.
        """
        """
        My Implementation: I finsihed. If you increase the difference of playouts --> More clear result
        """

        temp_node = self
        # Expand Root Node
        temp_node.expand()

        while (playouts > 0):
            # Select
            final_node, message = self.select()

            # Stimulation
            if (message == "Terminal"):
                outcome = final_node.state.value()
            elif (message == "Unexpanded"):
                final_node.expand()
                outcome = final_node.random_play()

            # Update Play count
            final_node.update_play_counts(outcome)

            playouts -= 1

        # Choose move with highest win percentage

        chosen_Move = None
        max_win_percentage = float("-inf")

        for move, child in self.children.items():
            temp_win_percent = child.get_win_percentage_if_chosen_by_parent()
            if (temp_win_percent > max_win_percentage):
                max_win_percentage = temp_win_percent
                chosen_Move = move
        return chosen_Move

    def expand(self):
        for move in self.legal_moves:
            newState = self.state.make_move(move)
            self.children[move] = MctsNode(newState, self, self.ucb_const)
        self.is_expanded = True

    def select(self):
        final_node = None
        temp_node = self
        while (final_node == None):
            max_UCB_node = None
            max_UCB_value = float("-inf")
            # If the Current Node is Terminal
            if temp_node.state.is_terminal():
                final_node = temp_node
                return (final_node, "Terminal")

            for _, child in temp_node.children.items():
                # If the children is terminal, return children
                if (child.is_expanded == False):
                    final_node = child
                    return (final_node, "Unexpanded")
                elif child.is_expanded == True:
                    # Pick children with highest UCB weight
                    child_UCB_value = child.get_UCB_weight_from_parent_perspective()
                    if child_UCB_value >= max_UCB_value:
                        max_UCB_node = child
                        max_UCB_value = child_UCB_value
            # Move to node with highest UCB weight
            temp_node = max_UCB_node

    def random_play(self):
        temp_state = self.state
        while (temp_state.value() == 0):
            randomMove = temp_state.get_random_legal_move()
            temp_state = temp_state.make_move(randomMove)

        return temp_state.value()
