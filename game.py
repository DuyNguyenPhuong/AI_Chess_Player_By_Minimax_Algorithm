"""
Main code that plays the game and manages all options.

You should not modify any code in this file.

@author Dave Musicant
"""


import random
import argparse
from typing import Optional, Dict
from game_board import GameBoard, Location
from player import Player
from human_player import HumanPlayer
from minimax_player import MinimaxPlayer, heuristic
from mcts_player import MctsPlayer
from common_values import (
    PLAYER_1, PLAYER_2, COLOR_NAMES, MARKERS)


def parse_args() -> argparse.Namespace:
    """ Parse command line arguments.
    """
    p = argparse.ArgumentParser()

    p.add_argument("player1type", choices=['human', 'minimax', 'mcts'])
    p.add_argument("player2type", choices=['human', 'minimax', 'mcts'])

    p.add_argument("--plies1", type=int, default=1, help=(
        "Only relevant if player1type is minimax; number of plies ahead that"
        " it should look. Default=1."))

    p.add_argument("--plies2", type=int, default=1, help=(
        "Only relevant if player2type is minimax; number of plies ahead that"
        " it should look. Default=1"))

    p.add_argument("--playouts1", type=int, default=0, help=(
        "Only relevant if player1type is mcts; number of playouts it should"
        " run. Default=0."))

    p.add_argument("--playouts2", type=int, default=0, help=(
        "Only relevant if player2type is mcts; number of playouts it should"
        " run. Default=0."))

    p.add_argument("--ucb1", type=float, default=.5, help=(
        "Only relevant if player1type is mcts; value for its UCB exploration"
        " constant. Default=.5"))

    p.add_argument("--ucb2", type=float, default=.5, help=(
        "Only relevant if player2type is mcts; value for its UCB exploration"
        " constant. Default=.5"))

    p.add_argument("--num_games", type=int, default=1,
                   help=("Number of games to play). Default=1"))

    p.add_argument("--silent", action="store_true", default=False, help=(
        "Hide all output for each game. This option usually makes sense when"
        "running many simulations."))

    p.add_argument("--board_size", type=int, default=7, help=(
        "Size of the game board. 7 by default."))

    p.add_argument("--seed", type=int, default=None, help=(
        "Seed for random number generator. Defaults to no seed, i.e., using"
        "Python default randomness source."))

    args = p.parse_args()
    return args


def playGame(players, board_size, silent) -> int:
    '''Manages playing an actual game.'''

    done = False
    currentBoard: GameBoard = GameBoard(board_size)
    currentPlayer = PLAYER_1

    while not done:

        # Display board and statistics
        if not silent:
            currentBoard.display()

        # Obtain move that player makes. If move is illegal, keep
        # prompting for alternative move.
        firstTime = True

        move: Optional[Location] = None
        board_copy = None

        # Loop forever until a reasonable turn is taken
        while True:
            if not firstTime:
                print("Move is illegal. Try again.", move)

            firstTime = False

            move = players[currentPlayer].choose_move(currentBoard)
            if not silent:
                if move is not None:
                    print("Move chosen = ", move.row, ",", move.column)
                else:
                    print("Move chosen = player concedes")

            if move is None:
                # Player concedes
                break

            board_copy = currentBoard.make_move(move)

            if board_copy is not None:
                # Legal move made
                currentBoard = board_copy
                break

        # Flip to other player
        currentPlayer *= -1

        # End game if player passed
        if move is None:
            done = True

    if not silent:
        # Display final outcome
        print('\n-----\n')
        print(COLOR_NAMES[currentPlayer], "wins!")
    return currentPlayer


def main() -> None:
    args = parse_args()

    players: Dict[int, Player] = {}

    if args.seed is not None:
        random.seed(args.seed)

    if args.player1type == 'human':
        players[PLAYER_1] = HumanPlayer()
    elif args.player1type == 'minimax':
        players[PLAYER_1] = MinimaxPlayer(heuristic, args.plies1)
    elif args.player1type == 'mcts':
        players[PLAYER_1] = MctsPlayer(args.playouts1, args.ucb1)
    else:
        raise Exception('Player 1 type invalid.')

    if args.player2type == 'human':
        players[PLAYER_2] = HumanPlayer()
    elif args.player2type == 'minimax':
        players[PLAYER_2] = MinimaxPlayer(heuristic, args.plies2)
    elif args.player2type == 'mcts':
        players[PLAYER_2] = MctsPlayer(args.playouts2, args.ucb2)
    else:
        raise Exception('Player 2 type invalid.')

    first_player_games_won = 0
    for _ in range(args.num_games):
        winner = playGame(players, args.board_size, args.silent)
        if winner == PLAYER_1:
            first_player_games_won += 1
        if args.silent:
            print(MARKERS[winner], end="", flush=True)

    print()
    print(f"Player 1 games won: {first_player_games_won}/{args.num_games}")
    print("Average number of boards made per game:",
          GameBoard.get_num_boards_made() / args.num_games)


if __name__ == '__main__':
    main()
