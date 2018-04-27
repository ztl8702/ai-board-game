from common import Board


class MiniMaxSolver:

    MAX_DEPTH = 3  # Maximum search depth
    TURNS_BEFORE_SHRINK = [128 + 24, 192 + 24]
    infinity = float('inf')

    def __init__(self, colour):
        self.colour = colour
        return

    def h(self, board):
        """Utility function

        h(state) = ourPieces - opponentsPiece
        """
        ourPieces = board.getAllPieces(self.colour)
        oppoPieces = board.getAllPieces(
            board._get_opponent_colour(self.colour))
        return len(ourPieces) - len(oppoPieces)

    def minimax(self, board, currentTurn):
        # first, find the max value
        # should be root node of tree
        self.visited = {}
        (best_move, best_val) = self.max_value(board, currentTurn, 1)
        return best_move

    def max_value(self, board, currentTurn, depth):
        """Max represents our turn
        """
        if ((currentTurn, board.getHashValue()) in self.visited):
            return self.visited[(currentTurn, board.getHashValue())]
        if self.isTerminal(board, depth, currentTurn):
            return (None, self.h(board))

        max_value = -self.infinity
        max_move = None

        successors_states = self.getSuccessors(board, currentTurn, self.colour)
        print("max", "successor_states", len(successors_states))
        for (move, state) in successors_states:
            tmp = self.min_value(state, currentTurn+1, depth+1)[1]
            if (tmp > max_value):
                max_move = move
                max_value = tmp
        self.visited[(currentTurn, board.getHashValue())
                     ] = (max_move, max_value)
        return (max_move, max_value)

    def min_value(self, board, currentTurn, depth):
        """Min represents opponent's turn
        """
        if ((currentTurn, board.getHashValue()) in self.visited):
            return self.visited[(currentTurn, board.getHashValue())]
        if self.isTerminal(board, depth, currentTurn):
            return (None, self.h(board))

        min_value = self.infinity
        min_move = None

        successors_states = self.getSuccessors(
            board, currentTurn, board._get_opponent_colour(self.colour))
        for (move, state) in successors_states:
            tmp = self.max_value(state, currentTurn+1, depth+1)[1]
            if (tmp < min_value):
                min_move = move
                min_value = tmp
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
            #print(side, moves)

            newStates = [((x, y), board.placePiece(x, y, side))
                         for (x, y) in moves]
        else:
            # Moving phase
            ourPieces = board.getAllPieces(side)
            moves = []
            for (x, y) in ourPieces:
                moves += board.getAvailableMoves(x, y)

            if currentTurn in self.TURNS_BEFORE_SHRINK:
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
