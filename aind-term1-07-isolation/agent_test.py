"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent as agent
import competition_agent as competition
import sample_players as sample

from game_agent import (MinimaxPlayer, AlphaBetaPlayer, custom_score,
                        custom_score_2, custom_score_3)

from sample_players import (RandomPlayer, open_move_score,
                            improved_score, center_score)

from importlib import reload

def score(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return float(len(game.get_legal_moves(player)))

class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(agent)

    def xtest_minimax(self):
        player1 = agent.MinimaxPlayer(score_fn=score)
        player2 = sample.RandomPlayer()
        game = isolation.Board(player1, player2)

        game.apply_move((2, 3))
        game.apply_move((0, 5))

        # print(game.to_string())

        assert(player1 == game.active_player)
        # print("player = %s, moves = %s" % (game.active_player, game.get_legal_moves()))

        winner, history, outcome = game.play()
        print("\nWinner: {}\nOutcome: {}".format(winner, outcome))
        print(game.to_string())
        print("Move history:\n{!s}".format(history))

    def xtest_alphabeta(self):
        player1 = agent.AlphaBetaPlayer(1, score_fn=score)
        player2 = sample.RandomPlayer()
        game = isolation.Board(player1, player2, 9 ,9)

        game._board_state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,\
        0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1,\
        1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0,\
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 39, 38]

        # in this game state, the player 1 next move should be > (6.0, (3, 6))
        # add a print to in the alphabeta to print the result

        print(game.to_string())

        assert(player1 == game.active_player)
        # print("player = %s, moves = %s" % (game.active_player, game.get_legal_moves()))

        winner, history, outcome = game.play()
        print("\nWinner: {}\nOutcome: {}".format(winner, outcome))
        print(game.to_string())
        print("Move history:\n{!s}".format(history))

    def xtest_alphabeta_id(self):
        player1 = agent.MinimaxPlayer(score_fn=score)
        player2 = sample.RandomPlayer()
        game = isolation.Board(player1, player2)

        game.apply_move((2, 3))
        game.apply_move((0, 5))

        # print(game.to_string())

        assert(player1 == game.active_player)
        # print("player = %s, moves = %s" % (game.active_player, game.get_legal_moves()))

        winner, history, outcome = game.play()
        print("\nWinner: {}\nOutcome: {}".format(winner, outcome))
        print(game.to_string())
        print("Move history:\n{!s}".format(history))

    def test_montecarlo(self):
        player1 = competition.CustomPlayer()
        player2 = AlphaBetaPlayer(score_fn=improved_score)

        game = isolation.Board(player1, player2)

        game.apply_move((2, 3))
        game.apply_move((0, 5))

        print(game.to_string())

        winner, history, outcome = game.play()
        print("\nWinner: {}\nOutcome: {}".format(winner, outcome))
        print(game.to_string())
        print("Move history:\n{!s}".format(history))

if __name__ == '__main__':
    unittest.main()
