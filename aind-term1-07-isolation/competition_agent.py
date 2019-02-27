"""Implement your own custom search agent using any combination of techniques
you choose.  This agent will compete against other students (and past
champions) in a tournament.

         COMPLETING AND SUBMITTING A COMPETITION AGENT IS OPTIONAL
"""
import random
import math


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    raise NotImplementedError


class CustomPlayer:
    """Game-playing agent to use in the optional player vs player Isolation
    competition.

    You must at least implement the get_move() method and a search function
    to complete this class, but you may use any of the techniques discussed
    in lecture or elsewhere on the web -- opening books, MCTS, etc.

    **************************************************************************
          THIS CLASS IS OPTIONAL -- IT IS ONLY USED IN THE ISOLATION PvP
        COMPETITION.  IT IS NOT REQUIRED FOR THE ISOLATION PROJECT REVIEW.
    **************************************************************************

    Parameters
    ----------
    data : string
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted.  Note that
        the PvP competition uses more accurate timers that are not cross-
        platform compatible, so a limit of 1ms (vs 10ms for the other classes)
        is generally sufficient.
    """

    def __init__(self, data=None, timeout=1.):
        self.score = custom_score
        self.time_left = None
        self.TIMER_THRESHOLD = timeout
        self.plays = {}
        self.wins = {}

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        # OPTIONAL: Finish this function!

        self.time_left = time_left

        moves = game.get_legal_moves() 

        if len(moves) < 2:
            if not len(moves): 
                return (-1,-1)
            elif (moves) == 1: 
                return moves[0]

        best_move = (-1,-1)

        try:
            games = 0
            while(True):
                self.mcts(game)
                games += 1
        except SearchTimeout:            
            player = game.active_player
            value_best = (float("-inf"),(-1,-1))
            
            for move in game.get_legal_moves():
                m,s = (move, str(game.forecast_move(move)._board_state))
                ps = (player,s)
                w = float(self.wins.get(ps,0))
                p = float(self.plays.get(ps,1))
                r = w/p
                value_best = max(value_best, (r, move))
            
            best_move = value_best[1]

        return best_move


    def mcts(self, game, depth=100):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
 
        state = game
        visited = set()
        winner = None
        current_depth = 0
        moves = []

        for _ in range(depth):
            player = state.active_player
            current_depth += 1
            
            moves_states = [(move, state.forecast_move(move)) for move in state.get_legal_moves()]

            move, state = self.ucb1(state)

            moves.append([move[0], move[1]])
            player_state = (player, str(state._board_state))

            if player_state not in self.plays:
                self.plays[player_state] = 0
                self.wins[player_state] = 0

            visited.add(player_state)

            if state.is_winner(player):
                winner = player
                break

        for player_state in visited:
            self.plays[player_state] += 1
            if player_state[0] == winner:
                self.wins[player_state] += 1

    def ucb1(self, game_state):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        player = game_state.active_player
        moves_states = [(move, game_state.forecast_move(move)) for move in game_state.get_legal_moves()]
        player_states = [self.plays.get((player, str(state._board_state))) for move,state in moves_states]
        constant = 1.4

        if all(player_states):
            values = [self.plays[(player, str(state._board_state))] for move, state in moves_states]
            log_value = math.log(sum(values))
            value, move, state = max((
                self.wins[(player, str(state._board_state))] / self.plays[(player, str(state._board_state))]
                + constant * math.sqrt(
                    log_value / self.plays[(player, str(state._board_state))]
                ), 
                move, state) for move,state in moves_states)
            return (move, state)
        else:
            move, state = random.choice(moves_states)
            return (move, state)