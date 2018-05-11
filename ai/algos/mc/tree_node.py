from typing import Type
from ...common import Board
from ...common.game_state_helpers import get_opponent_colour, get_successor_board_states
import random
import math


INFINITY = float('inf')

class TreeNode(object):
    """
    Representation of a node in the game tree.

    Contains Monte Carlo stats
    """

    def __init__(self, board: Board, current_turn:int, side="@"):
        # State
        self.board = board
        self.current_turn = current_turn 
        self.side = side
        # Monte Carlo counters
        self.visited = 0
        self.winning = 0

    def toggle_player(self):
        self.side = get_opponent_colour(self.side)

    def random_play(self):
        self.toggle_player()
        self.current_turn+=1
        sucessors = get_successor_board_states(self.board, self.current_turn, self.side)
        #print(f"random_play selected from {len(sucessors)} substates")
        if (len(sucessors)==0):
            print(f"no successor, side={self.side} turn={self.current_turn}")
            self.board.print_board()
        if (len(sucessors)>0):
            self.board = random.choice(sucessors)[1]

    def ucb_upperbound(self, totalVisits):
        """
        Upper Confidence Bound.

        Used during exploration.
        """
        if (self.visited == 0):
            return INFINITY
        return (self.winning / self.visited) + 1.41 * math.sqrt(math.log(totalVisits) / self.visited)

    def score(self):
        """
        The score of this node.

        Used when choosing the final move.
        """
        if (self.visited == 0):
            return -INFINITY
        return (self.winning / self.visited)
