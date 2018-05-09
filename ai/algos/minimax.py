import random

from ..common import Board
from ..common import config


INFINITY = float('inf')

PLACEMENT_VALUE = [
    [  0,-10,-10,-10,-10,-10,-10,  0],
    [-10,  0, 10, 10, 10, 10,  0,-10],
    [-10, 10, 20, 30, 30, 20, 10,-10],
    [-10, 10, 30, 99, 99, 30, 10,-10],
    [-10, 10, 30, 99, 99, 30, 10,-10],
    [-10, 10, 20, 30, 30, 20, 10,-10],
    [-10,  0, 10, 10, 10, 10,  0,-10],
    [  0,-10,-10,-10,-10,-10,-10,  0]
]

class MiniMaxSolver:

    MAX_DEPTH = 3  # Maximum search depth
    

    def __init__(self, colour):
        self.colour = colour
        return

    def h(self, board):
        """Utility function

        h(state) = ourPieces - opponentsPiece
        """
        ourPieces = board.get_all_pieces(self.colour)
        oppoPieces = board.get_all_pieces(
            board._get_opponent_colour(self.colour))

        # h1 = len(ourPieces) - 2*len(oppoPieces)

        ourTotal = 0
        oppTotal = 0
        for our in ourPieces:
            (x, y) = our
            ourTotal += PLACEMENT_VALUE[x][y]
        for opp in ourPieces:
            (x, y) = opp
            oppTotal += PLACEMENT_VALUE[x][y]
        h1 = ourTotal

        return h1

    def minimax(self, board, currentTurn):
        # first, find the max value
        # should be root node of tree
        self.visited = {}
        (best_move, best_val) = self.max_value(board, currentTurn, 1)
        return best_move

    def _range_intersect(self, a, b):
        a_lower, a_upper = a
        b_lower, b_upper = b
        if (a_upper < b_lower or b_upper < a_lower):
            return (INFINITY, -INFINITY)  # No intersection
        return (max(a_lower, b_lower), min(a_upper, b_upper))

    def _is_empty_set(self, a):
        a_lower, a_upper = a
        return a_lower > a_upper

    def max_value(self, board, currentTurn, depth, validRange=(-INFINITY, INFINITY)):
        """Max represents our turn

        validRange is used for alpha-beta pruning
        The boundaries are inclusive.
        """
        if ((currentTurn, board.getHashValue()) in self.visited):
            return self.visited[(currentTurn, board.getHashValue())]
        if self.isTerminal(board, depth, currentTurn):
            return (None, self.h(board))

        max_value = -INFINITY
        max_move = None

        successors_states = self.getSuccessors(board, currentTurn, self.colour)
       # print(" "*(depth-1)+"max", "successor_states", len(successors_states))
        for (move, state) in successors_states:
            tmp = self.min_value(state, currentTurn+1, depth+1,
                                 self._range_intersect((max_value, INFINITY), validRange))[1]
            if (tmp > max_value):
                max_move = move
                max_value = tmp
                if (self._is_empty_set(self._range_intersect(validRange, (max_value, INFINITY)))):
                    break
            elif (tmp == max_value and random.randrange(0,2) == 1): # occasionally uses another max_value
                max_move = move
                max_value = tmp
                if (self._is_empty_set(self._range_intersect(validRange, (max_value, INFINITY)))):
                    break
        self.visited[(currentTurn, board.getHashValue())
                     ] = (max_move, max_value)
        return (max_move, max_value)

    def min_value(self, board, currentTurn, depth, validRange=(-INFINITY, INFINITY)):
        """Min represents opponent's turn
        """
        if ((currentTurn, board.getHashValue()) in self.visited):
            return self.visited[(currentTurn, board.getHashValue())]
        if self.isTerminal(board, depth, currentTurn):
            return (None, self.h(board))

        min_value = INFINITY
        min_move = None

        successors_states = self.getSuccessors(
            board, currentTurn, board._get_opponent_colour(self.colour))
        #print(" "*(depth-1)+"min", "successor_states", len(successors_states))
        for (move, state) in successors_states:
            tmp = self.max_value(state, currentTurn+1, depth+1,
                                 self._range_intersect((-INFINITY, min_value), validRange))[1]
            if (tmp < min_value):
                min_move = move
                min_value = tmp
                if (self._is_empty_set(self._range_intersect(validRange, (-INFINITY, min_value)))):
                    break
            elif (tmp == min_value and random.randrange(0,2) == 1): # occasionally uses another min_value
                min_move = move
                min_value = tmp
                if (self._is_empty_set(self._range_intersect(validRange, (-INFINITY, min_value)))):
                    break
        self.visited[(currentTurn, board.getHashValue())
                     ] = (min_move, min_value)
        return (min_move, min_value)

    #                     #
    #   UTILITY METHODS   #
    #                     #

    # successor states in a game tree are the child nodes...
    def getSuccessors(self, board, currentTurn, side='@'):
        if (currentTurn <= 24):
            # placing phase
            if side == Board.PIECE_BLACK:
                validYZone = range(2, 8)
            else:
                validYZone = range(0, 6)
            moves = [(x, y)
                     for (x, y) in board.get_empty_cells() if y in validYZone]

            newStates = [((x, y), board.placePiece(x, y, side))
                         for (x, y) in moves]
        else:
            # Moving phase
            ourPieces = board.get_all_pieces(side)
            moves = []
            for (x, y) in ourPieces:
                moves += board.getAvailableMoves(x, y)

            if currentTurn in config.TURNS_BEFORE_SHRINK:
                newStates = [
                    (((fromX, fromY), (toX, toY)),
                     board.makeMove(fromX, fromY, toX, toY, side).shrink()
                     )
                    for ((fromX, fromY), (toX, toY)) in moves
                ]
            else:
                newStates = [
                    (((fromX, fromY), (toX, toY)),
                     board.makeMove(fromX, fromY, toX, toY, side)
                     )
                    for ((fromX, fromY), (toX, toY)) in moves
                ]

        return newStates

    def isTerminal(self, board, depth, currentTurn):
        """Terminate if either side wins;
        or if we reached maximum search depth.
        """
        return ((depth >= self.MAX_DEPTH) or
                (currentTurn > 24 and
                 (board.isWon(Board.PIECE_BLACK) or board.isWon(Board.PIECE_WHITE))
                 ))
