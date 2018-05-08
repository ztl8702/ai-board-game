"""
Performance tests
"""

from datetime import datetime, timedelta
from ai.common import Board
from ai.algos.mc import solver
from ai.common.helpers import p


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

    print("I/O time:", elapsed.total_seconds(), 'seconds')


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

perf_test_board_io()
import cProfile

#cProfile.run('perf_test_mc_solver()')