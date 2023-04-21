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
        self.ucb_const = ucb_const

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
        return 1 - self.wins_for_this_player/self.total_games_for_this_player

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

        return self.get_UCB_weight_from_parent_perspective() * self.ucb_const * \
            math.sqrt(math.log(parent.total_games_for_this_player) /
                      self.total_games_for_this_player)

        # raise NotImplementedError("You must implement this method")

    def update_play_counts(self, outcome: int) -> None:
        """Updates the total games played from this node, as well as the number
        of wins from this node for the current player.

        You will need this for backpropagating wins/losses back up the tree.

        outcome: +1 for 1st player win, -1 for 2nd player win.
        """

        """
        Question: How can we know the terminal node is player 1 or 0
        """
        state = self.state
        lastPlayer = state.get_active_player()

        if lastPlayer == 1:
            while (self.parent != None):
                self.total_games_for_this_player += 1
                self.wins_for_this_player += outcome
                self = self.parent
                if (outcome == 1):
                    outcome = 0
                else:
                    outcome = 1
        else:
            addition_number_of_win_for_player_1 = 0
            while (self.parent != None):
                self.total_games_for_this_player += 1
                self.wins_for_this_player += addition_number_of_win_for_player_1
                self = self.parent
                if addition_number_of_win_for_player_1 == 0:
                    addition_number_of_win_for_player_1 = 1
                else:
                    addition_number_of_win_for_player_1 = 0

        # raise NotImplementedError("You must implement this method")

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
        My Implementation: I finish the select and expand method. I will look on how to 
        merge that together
        """
        while (playouts > 0):
            node, unvisitedChildren = self.select()
            state = node.state
            if state.is_terminal() == False:
                outcome = self.random_play(unvisitedChildren)
            else:
                outcome = node.state.value()
            self.update_play_count(outcome)
            playouts -= 1

    def select(self):
        node = self
        highest_UCB_value = float("-inf")
        highest_UCB_node = None
        unvisitedChidlren = None

        while (unvisitedChidlren == None and (not node.state.is_terminal())):
            for move in node.legal_moves:
                if move in node.children:
                    if highest_UCB_value < node.children[move][1]:
                        highest_UCB_value = node.children[move][1]
                        highest_UCB_node = node.children[move][0]

                if move not in node.children:
                    newState = node.state.make_move(move)
                    unvisitedChidlren = MctsNode(
                        newState, node, self.ucb_const)
                    UCB_value = unvisitedChidlren.get_UCB_weight_from_parent_perspective()
                    node.children[move] = (unvisitedChidlren, UCB_value)
                    return (None, unvisitedChidlren)
            node = highest_UCB_node
        return (node, unvisitedChidlren)

    def random_play(self, root: MctsNode):
        temp_state = root.state
        while (temp_state.value != 0):
            random_move = temp_state.get_randomized_moves()
            temp_state = temp_state.make_move(random_move)
        return temp_state.value
