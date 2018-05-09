from ..common import Board
from ..common import config

# for heuristics
from .parta import faster_BFS
from .parta import faster_DFS # make faster 

INFINITY = float('inf')

PLACEMENT_VALUE = [
    [0,  0,  0,  0,  0,  0,  0,  0],
    [0,  0, 10, 10, 10, 10,  0,  0],
    [0, 10, 20, 30, 30, 20, 10,  0],
    [0, 10, 30, 50, 50, 30, 10,  0],
    [0, 10, 30, 50, 50, 30, 10,  0],
    [0, 10, 20, 30, 30, 20, 10,  0],
    [0,  0, 10, 10, 10, 10,  0,  0],
    [0,  0,  0,  0,  0,  0,  0,  0]
]

class MiniMaxSolver:

    MAX_DEPTH = 3  # Maximum search depth
    
    MAX_LAYERS = 1 # For utility h3    

    def __init__(self, colour):
        self.colour = colour
        return

    def h(self, board):
        """Utility function
        """

        # h1 number of our pieces - opponent pieces
        ourPieces = board.get_all_pieces(self.colour)
        oppPieces = board.get_all_pieces(
            board._get_opponent_colour(self.colour))
        
        h1 = len(ourPieces) - len(oppPieces) # * 2

        # h1 modified to take into account placement value
        # loop through all the pieces and multiply with coefficient
        # ourTotal = 0
        # oppTotal = 0
        # for our in ourPieces:
        #     (x, y) = our
        #     ourTotal += PLACEMENT_VALUE[x][y]
        # for opp in ourPieces:
        #     (x, y) = opp
        #     oppTotal += PLACEMENT_VALUE[x][y]

        # h1 = ourTotal - oppTotal # *2

        # h2, number of moves we can make - number of moves the opponent can make
        # ourPiecesMoves = board.count_moves(self.colour)
        # oppPiecesMoves = board.count_moves(
        #     board._get_opponent_colour(self.colour))
        # h2 = ourPiecesMoves - oppPiecesMoves

        # @TODO, takes too long to compute
        # h3, number of moves we need to win - number of moves our opponent need to win
        # ourMinMoves = faster_BFS(board, self.colour, MAX_LAYERS)
        # oppMinMoves = faster_BFS(board, 
        #     board._get_opponent_colour(self.colour), MAX_LAYERS)
        # h3 = ourMinMoves - oppMinMoves

        '''
        for i in range(1, MAX_DEPTH):
        # print("Trying depth ", i) # DEBUG 
        if (faster_DFS(oboard, Board.PIECE_WHITE, MAX_LAYERS, i)):
            break
        '''

        return h1 #* h2 # * h3

    def minimax(self, board, currentTurn):
        # first, find the max value
        # should be root node of tree
        self.visited = {}
        (best_move, best_val) = self.get_max_value(board, currentTurn, 1)
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

    def get_max_value(self, board, currentTurn, depth, validRange=(-INFINITY, INFINITY)):
        """Max represents our turn

        validRange is used for alpha-beta pruning
        The boundaries are inclusive.
        """

        # check if current board state is seen before
        if ((currentTurn, board.getHashValue()) in self.visited):
            return self.visited[(currentTurn, board.getHashValue())]
        
        # check if we are at a leaf node or max depth has been reached
        if self.isTerminal(board, depth, currentTurn):
            return (None, self.h(board))

        max_value = -INFINITY
        max_move = None

        successors_states = self.getSuccessors(board, currentTurn, self.colour)
       # print(" "*(depth-1)+"max", "successor_states", len(successors_states))
        for (move, state) in successors_states:
            tmp = self.get_min_value(state, currentTurn+1, depth+1,
                                 self._range_intersect((max_value, INFINITY), validRange))[1]
            if (tmp > max_value):
                max_move = move
                max_value = tmp
                if (self._is_empty_set(self._range_intersect(validRange, (max_value, INFINITY)))):
                    break
        self.visited[(currentTurn, board.getHashValue())
                     ] = (max_move, max_value)
        return (max_move, max_value)

    def get_min_value(self, board, currentTurn, depth, validRange=(-INFINITY, INFINITY)):
        """Min represents opponent's turn
        """

        # check if current board state is seen before
        if ((currentTurn, board.getHashValue()) in self.visited):
            return self.visited[(currentTurn, board.getHashValue())]
        
        # check if we are at a leaf node or max depth has been reached
        if self.isTerminal(board, depth, currentTurn):
            return (None, self.h(board))

        min_value = INFINITY
        min_move = None

        successors_states = self.getSuccessors(
            board, currentTurn, board._get_opponent_colour(self.colour))
        #print(" "*(depth-1)+"min", "successor_states", len(successors_states))
        for (move, state) in successors_states:
            tmp = self.get_max_value(state, currentTurn+1, depth+1,
                                 self._range_intersect((-INFINITY, min_value), validRange))[1]
            if (tmp < min_value):
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

    # limit the zones of play for placing phase
    def getPlacingZone(self, board, currentTurn, side):
        '''
        turn 0, no pieces are placed
        4
        4+12 = 16
        16+12 = 28
        '''
        
        # zone limited to inner square (1 cell thick)
        placingZone = range(3, 5)

        if (currentTurn < 5):
            pass
            
        elif (currentTurn < 17): 
            moves = [(x, y) for (x, y) in board.get_empty_cells() 
                if y in placingZone and x in placingZone]
            
            # check if the inner square is completely filled
            if (moves):
                placingZone = range(3, 5)
            else: # valid zone increases by a buffer of 1 cell thickness
                placingZone = range(2, 6)

        else:
            # valid zone increases by a buffer of 1 cell thickness
            placingZone = range(2, 6)

            if (side == Board.PIECE_BLACK):    
                moves = [(x, y) for (x, y) in board.get_empty_cells() 
                    if y in placingZone and x in placingZone]
                if (moves):
                    pass
                else: # increase cell thickness by 1 again, limit to black area
                    placingZone = range(2, 8)

            else:
                moves = [(x, y) for (x, y) in board.get_empty_cells()
                    if y in placingZone and x in placingZone]
                if (moves):
                    pass
                else: # increase cell thickness by 1 again, limit to white area
                    placingZone = range(0, 6)

        return placingZone

    # successor states in a game tree are the child nodes...
    def getSuccessors(self, board, currentTurn, side='@'):
        
        if (currentTurn <= 24): # Placing phase
            if side == Board.PIECE_BLACK:
                placingZone = self.getPlacingZone(board, currentTurn, side)
            else:
                placingZone = self.getPlacingZone(board, currentTurn, side)
                
            moves = [(x, y) for (x, y) in board.get_empty_cells()
                if (x in placingZone and y in placingZone)]

            newStates = [((x, y), board.placePiece(x, y, side))
                         for (x, y) in moves]
        
        else: # Moving phase
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
