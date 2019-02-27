#!/usr/bin/env python

# run the test in a multriprocessing fashion

import sys
import os
import logging
import random
import itertools
import warnings
import multiprocessing
from multiprocessing import Pool

from importlib import reload

from isolation import Board
from sample_players import (RandomPlayer, open_move_score, improved_score, center_score)
from game_agent import (MinimaxPlayer, AlphaBetaPlayer, custom_score, custom_score_2, custom_score_3)

import pickle

results = []

def func(id):
    player1 = AlphaBetaPlayer(score_fn=custom_score_2)
    player2 = AlphaBetaPlayer(score_fn=improved_score)

    games = [(True, Board(player1, player2)), (False, Board(player2, player1))]
    
    # randon move and response
    for _ in range(2):
        move = random.choice(games[0][1].get_legal_moves())
        for game in games:
            game[1].apply_move(move)

    results = []
    for game in games:
        isplayer1 = game[0]
        winner, history, outcome = game[1].play(time_limit=150)
        winner = 'player1' if winner == player1 else 'player2'
        results.append((id, isplayer1, winner, history, outcome))
    return results

def callback(arg0):
    global results
    for result in arg0:
        results.append(result)

def error_callback(arg0):
    print("err:", arg0)

if __name__ == "__main__":
    # multiprocessing
    with Pool() as pool:
        for id in range(5):
            pool.apply_async(func=func,callback=callback, error_callback=error_callback, args=(id,))
        pool.close()
        pool.join()

    p1win = 0
    p2win = 0
    games = float(len(results))

    for result in results:
        if result[2] == 'player1':
            p1win += 1
            print(result)
        else:
            p2win += 1

    print('player1', p1win, (p1win/games)*100.0)
    print('player2', p2win, (p2win/games)*100.0)

    # pickle.dump(results, open('results.p', 'wb'))

