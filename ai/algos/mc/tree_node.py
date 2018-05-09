from typing import Type
from ...common import Board
from ...common.game_state_helpers import get_opponent_colour, get_successor_board_states
import random
import math


INFINITY = float('inf')

class TreeNode(object):
    def __init__(self, board: Board, currentTurn:int, side="@", parent: 'TreeNode'=None):
        # States
        self.board = board
        self.currentTurn = currentTurn # the turn is finished
        self.side = side
        # Monte Carlo counters
        self.visited = 0
        self.winning = 0
        # Tree stuff
        self.parent = parent
        self.children = []
        self.last_action = None

    def add_child(self, node: 'TreeNode'):
        if (node not in self.children):
            self.children.append(node)
            assert node.parent == self

    def has_children(self):
        return (len(self.children) > 0)

    def toggle_player(self):
        self.side = get_opponent_colour(self.side)

    def random_play(self):
        self.toggle_player()
        self.currentTurn+=1
        sucessors = get_successor_board_states(self.board, self.currentTurn, self.side)
        #print(f"random_play selected from {len(sucessors)} substates")
        if (len(sucessors)==0):
            print(f"no successor, side={self.side} turn={self.currentTurn}")
            self.board.printBoard()
        self.board = random.choice(sucessors)[1]
        
    def get_random_child(self):
        return random.choice(self.children)

    def get_child_with_max_score(self)->'TreeNode':
        # why choose max visited count rather than ucb?
        maxValue = -INFINITY
        maxNode = None
        for node in self.children:
            if (node.score() > maxValue):
                maxValue = node.score()
                maxNode = node
        return maxNode

    def ucb_upperbound(self, totalVisits):
        if (self.visited == 0):
            return INFINITY
        return (self.winning / self.visited) + 1.41 * math.sqrt(math.log(totalVisits) / self.visited)

    def score(self):
        if (self.visited == 0):
            return -INFINITY
        return (self.winning / self.visited)
