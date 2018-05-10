import random

from ..common import Board
from ..common import config

from .parta import faster_DFS


INFINITY = float('inf')

# Ver. 1
A = +99
B = +70
C = +60
D = +10
E = 0
F = -10
G = -10
N = 0

PLACEMENT_VALUE = [
    [ N, G, F, F, F, F, G, N],
    [ G, E, D, D, D, D, E, G],
    [ F, D, C, B, B, C, D, F],
    [ F, D, B, A, A, B, D, F],
    [ F, D, B, A, A, B, D, F],
    [ F, D, C, B, B, C, D, F],
    [ G, E, D, D, D, D, E, G],
    [ N, G, F, F, F, F, G, N]
]

# MOVEMENT_VALUE = [
#     [ N, G, F, F, F, F, G, N],
#     [ G, E, D, D, D, D, E, G],
#     [ F, D, A, A, A, A, D, F],
#     [ F, D, A, A, A, A, D, F],
#     [ F, D, A, A, A, A, D, F],
#     [ F, D, A, A, A, A, D, F],
#     [ G, E, D, D, D, D, E, G],
#     [ N, G, F, F, F, F, G, N]
# ]


class MiniMaxSolver:

    MAKE_RANDOM = True # choose random max_values when there are multiple

    def get_max_depth(self, currentTurn):

        # # in Placing Phase
        # if (currentTurn <= config.PLACING_PHASE):
        #     return 4
        
        # # in Moving Phase
        # elif (currentTurn <= config.TURNS_BEFORE_SHRINK[0]): # before first shrink
        #     return 2
        # elif (currentTurn <= config.TURNS_BEFORE_SHRINK[1]): # before second shrink
        #     return 4
        # elif (currentTurn > config.TURNS_BEFORE_SHRINK[1]): # after second shrink
        #     return 6

        # @TODO: need to check if default of depth 4 will be under time constraint
        if (currentTurn > config.TURNS_BEFORE_SHRINK[1]): # after second shrink
            return 6

        # max depth of 4 by default
        return 4
    

    def __init__(self, colour):
        self.colour = colour
        return

    def get_squares(self, board):
        """
        return array of coordinates containing squares
        """
        squares = []

        for i in range(2, 5): # y value
            for j in range(2, 5): # x value
                if (board.get(j, i) == self.colour and \
                    board.get(j+1, i) == self.colour and \
                        board.get(j+1, i+1) == self.colour and \
                            board.get(j, i+1) == self.colour):
                    
                    squares.append(tuple((j, i)))
                    squares.append(tuple((j+1, i)))
                    squares.append(tuple((j+1, i+1)))
                    squares.append(tuple((j, i+1)))

        return squares

    def get_square_quantity(self, board):
        """
        heuristic to find square formation
        """

        '''
        1. based on square in origin or 1 layer out
            -> inner square = range(3, 5)
            -> one layer out = range(2, 6)
        2. find square formation
        '''
        # look in the inner square and
            # check if it is out piece
                # then look for surrounding pieces
        
        square_quantity = 0
        for i in range(2, 5): # y value
            for j in range(2, 5): # x value
                if (board.get(j, i) == self.colour and \
                    board.get(j+1, i) == self.colour and \
                        board.get(j+1, i+1) == self.colour and \
                            board.get(j, i+1) == self.colour):
                    square_quantity += 1


        return square_quantity

    def h(self, board, currentTurn):
        """Utility function
        """

        # h1, based on location of pieces on the board
        # 1. from my extensive experimentation,
        # seems that if we consider opponent pieces, we will make worst moves
        # 2. from my extensive experimentation, 
        # the coefficient on the board should remain the same through out the phases, 
        # changing the coefficients depending on the phase doesn't seem to yield better results
        
        ourPieces = board.get_all_pieces(self.colour)
        ourTotal = 0
        
        for our in ourPieces:
            (x, y) = our
            ourTotal += PLACEMENT_VALUE[x][y]

        h1 = ourTotal
        
        # @TODO: figure out a way to use this heuristic, currently make worst moves
        # h2, give higher weightage to square formation in the inner part of board
        # h2 = self.get_square_quantity(board) * 10

        # @TODO: currently too slow to use
        # h3, find number of moves needed to kill all enemy if enemy is static
        # h3 = 1
        # layers = 2
        # for i in range(1, 1000):
        #     (found, totalMoves) = faster_DFS(board, self.colour, layers, i)
        #     if (found):
        #         h3 = totalMoves
        #         break
                
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
            return (None, self.h(board, currentTurn))

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
            elif (tmp == max_value and random.randrange(0,2) == 1 and self.MAKE_RANDOM): # occasionally uses another max_value
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
            return (None, self.h(board, currentTurn))

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
            elif (tmp == min_value and random.randrange(0,2) == 1 and self.MAKE_RANDOM): # occasionally uses another min_value
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
        if (currentTurn <= config.PLACING_PHASE):
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
            # IMPORTANT NOTE: i decided to limit the movement of pieces 
            # that form squares, as it is more advantagous to hold a square formation
            
            # Moving phase
            ourPieces = board.get_all_pieces(side)
            
            squares = self.get_squares(board)
            moves = []
            for (x, y) in ourPieces:
                if ((x, y) not in squares):
                    moves += board.getAvailableMoves(x, y)

            # @TODO: get my furthest piece away from opponent
            # prevent forfeiting when still have moves but all form squares
            if (not moves and ourPieces):
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
        return ((depth >= self.get_max_depth(currentTurn)) or
                (currentTurn > config.PLACING_PHASE and
                 (board.isWon(Board.PIECE_BLACK) or board.isWon(Board.PIECE_WHITE))
                 ))
