"""
Performance tests

Utility for code performance tests
We use it to find out the bottlenecks in our code
"""

from datetime import datetime, timedelta
from ai.common import Board
from ai.algos.mc import solver
from ai.algos.minimax import MiniMaxSolver
from ai.common.helpers import p
from ai.common.game_state_helpers import get_opponent_colour


def perf_test_board_io():
    start = datetime.now()
    board = Board()
    for i in range(10000):
        for x in range(8):
            for y in range(8):
                board.set_p(x, y, '@')
    for i in range(10000):
        for x in range(8):
            for y in range(8):
                board.set_p(x, y, 'O')
    elapsed = datetime.now() - start

    print("Write time:", elapsed.total_seconds(), 'seconds')
    start = datetime.now()
    board = Board()
    for i in range(10000):
        for x in range(8):
            for y in range(8):
                w = board.get(x, y)
    for i in range(10000):
        for x in range(8):
            for y in range(8):
                w = board.get(x, y)
    elapsed = datetime.now() - start

    print("Read time:", elapsed.total_seconds(), 'seconds')

def perf_test_mc_solver():
    layout = p(
        "X------X",
        "--------",
        "--------",
        "--------",
        "--------",
        "--------",
        "--------",
        "X------X",
    )
    board = Board.from_token_string(layout)

    solver.find_next_move(board, 1, '@')

def perf_test_minimax_solver_placing():
    solver = MiniMaxSolver('O')
    solver.MAX_DEPTH = 4
    layout = p(
        "X------X",
        "--------",
        "--------",
        "--------",
        "--------",
        "--------",
        "--------",
        "X------X",
    )
    board = Board.from_token_string(layout)

    solver.minimax(board, 1)

def perf_test_minimax_solver_moving():
    solver = MiniMaxSolver('O')
    solver.MAX_DEPTH = 4

    layout = p(
        "X--O---X",
        "--O--O--",
        "OOO@@-OO",
        "OO---O-O",
        "--@---@-",
        "-@--@---",
        "---@--@-",
        "X@-@---X",
    )
    board = Board.from_token_string(layout)

    solver.minimax(board, 26)

def perf_test_get_opponent_colour():
    for i in range(1000000):
        get_opponent_colour('O')
        get_opponent_colour('@')
        

#perf_test_board_io()
import cProfile

cProfile.run('perf_test_mc_solver()')
#cProfile.run('perf_test_minimax_solver_placing()')
#cProfile.run('perf_test_minimax_solver_moving()')

#cProfile.run('perf_test_get_opponent_colour()')