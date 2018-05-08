"""
Performance tests
"""

from datetime import datetime, timedelta
from ai.common.board import Board


def perf_test_board_io():
    start = datetime.now()
    board = Board()
    for i in range(10000):
        for x in range(8):
            for y in range(8):
                board.set(x, y, '@')
    for i in range(10000):
        for x in range(8):
            for y in range(8):
                board.set(x, y, 'O')
    elapsed = datetime.now() - start

    print("I/O time:", elapsed.total_seconds(), 'seconds')


perf_test_board_io()
import cProfile

#cProfile.run('perf_test_board_io()')