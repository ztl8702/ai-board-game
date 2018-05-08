from .cells_array import CellsArray
from .MoveType import MoveType
from .board_status import BoardStatus
import copy



class Board:
    '''
    Representation of the board
    '''
    MAX_BOARD_SIZE = 8  # maximum board size

    DIRECTION = [
        [-1, 0],  # left
        [+1, 0],  # right
        [0, -1],  # up
        [0, +1]   # down
    ]

    ANTICLOCKWISE = [
        (-1, -1),   # NW
        (-1, 0),    # W
        (-1, +1),   # SW
        (0, +1),    # S
        (+1, +1),   # SE
        (+1, 0),    # E
        (+1, -1),   # NE
        (0, -1)     # N
    ]

    PIECE_WHITE = 'O'   # while piece
    PIECE_BLACK = '@'   # black piece
    PIECE_EMPTY = '-'   # empty piece
    PIECE_CORNER = 'X'  # corner piece
    PIECE_INVALID = '#'    # not a valid piece

    def __init__(self):
        '''
        initially the board size is set to the maximum
        '''
        self.boardSize = self.MAX_BOARD_SIZE
        self.board = CellsArray(self.boardSize)
        for x in range(Board.MAX_BOARD_SIZE):
            for y in range(Board.MAX_BOARD_SIZE):
                self.set(x, y, Board.PIECE_EMPTY)
        self._update_corners()

    def _max_xy(self):
        """Max value of X or Y
        """
        return self._min_xy() + self.boardSize - 1

    def _min_xy(self):
        """Min value of X or Y
        """
        return (Board.MAX_BOARD_SIZE - self.boardSize) // 2

    def _corner_cells(self):
        return [
            (self._min_xy(), self._min_xy()),
            (self._min_xy(), self._max_xy()),
            (self._max_xy(), self._min_xy()),
            (self._max_xy(), self._max_xy())
        ]

    def _update_corners(self):
        """Updates the corner cells. 

        Called after a shrink and during the initialisation.
        """
        for (x, y) in self._corner_cells():
            self.set(x, y, Board.PIECE_CORNER)

    def readInput(self):
        ''' 
        Read and parse the board layout from stdin
        leaving aside last command line
        '''
        tmpBoard = CellsArray(self.MAX_BOARD_SIZE)

        for x in range(0, self.MAX_BOARD_SIZE):
            row = input().strip().split(" ")
            for y in range(0, self.MAX_BOARD_SIZE):
                tmpBoard.set(x, y, row[y])

        self.board = tmpBoard.getInverted()

    def printBoard(self):
        ''' 
        Debugging utlity function to print board
        '''
        board = self.board.getInverted()
        print(" ", end="")
        for i in range(self.MAX_BOARD_SIZE):
            print(i, end=" ")
        print()

        j = 0
        for line in board.cells:
            print(j, end="")
            j = j + 1
            for piece in line:
                print(piece, end=" ")
            print()
        print()

    def isEmpty(self, x, y):
        '''
        check if coordinate (x, y) is empty
        '''
        return self.board.get(x, y) == self.PIECE_EMPTY

    def isWithinBoard(self, x, y):
        '''
        returns true if coordinate (x, y) is within the board
        '''
        return (x in range(self._min_xy(), self._max_xy()+1)) and \
            (y in range(self._min_xy(), self._max_xy()+1))

    def get(self, x, y):
        '''
          Gets the piece at coordinate (x, y)
        '''
        if (self.isWithinBoard(x, y)):
            return self.board.get(x, y)
        else:
            return self.PIECE_INVALID

    def set(self, x, y, value):
        '''
        Change the piece at coordinate (x, y)
        '''
        if (self.isWithinBoard(x, y)):
            self.board.set(x, y, value)

    def getMoveType(self, x, y, direction):
        '''
        Check what type of move it is
        and return its type
        '''
        newX = x + self.DIRECTION[direction][0]
        newY = y + self.DIRECTION[direction][1]
        # if the cell is not occupied, its a normal move
        if self.isWithinBoard(newX, newY) and self.isEmpty(newX, newY):
            return MoveType.NORMAL

        # its a jump move
        newX2 = newX + self.DIRECTION[direction][0]
        newY2 = newY + self.DIRECTION[direction][1]
        if self.isWithinBoard(newX2, newY2) and \
                self.isEmpty(newX2, newY2) and \
                self.get(newX, newY) in [self.PIECE_WHITE, self.PIECE_BLACK]:
            return MoveType.JUMP

        # not a valid move, so can't move
        return MoveType.INVALID

    def getAvailableMoves(self, x, y):
        '''
        Returns a list of available moves that are valid 
        for the piece at (x, y) as a nested tuple in the form
        ((from), (to)) because we need to print moves from and to 
        '''

        # return no moves available if piece is not playable
        if not (self.get(x, y) in [self.PIECE_WHITE, self.PIECE_BLACK]):
            return []

        possibleMoves = []
        for direction in range(0, 4):
            result = self.getMoveType(x, y, direction)

            # check if move is valid
            if result != MoveType.INVALID:
                # make normal move
                if result == MoveType.NORMAL:
                    newX = x + self.DIRECTION[direction][0]
                    newY = y + self.DIRECTION[direction][1]

                # make jump move
                elif result == MoveType.JUMP:
                    newX = x + self.DIRECTION[direction][0] * 2
                    newY = y + self.DIRECTION[direction][1] * 2

                possibleMoves.append(((x, y), (newX, newY)))

        return possibleMoves

    def get_empty_cells(self):
        """
        """
        result = []
        for x in range(self._min_xy(), self._max_xy()+1):
            for y in range(self._min_xy(), self._max_xy()+1):
                if (self.isEmpty(x, y)):
                    result.append((x, y))
        return result

    def getHashValue(self):
        '''
        Computes a hash value for entire board.

        reasoning for method:
        use hash value to compare board states instead of 
        iterating through each cell to check board states that have been seen

        this is done by treating pieces as integers from 0 through 3
        using a base-4 digit system (quaternary numeral system)
        higher order represent higher significance of the bit
        order is in the range of (1, 64) for 8x8 board
        '''
        order = 1
        total = 0
        for x in range(0, self.boardSize):
            for y in range(0, self.boardSize):
                if (self.get(x, y) == self.PIECE_EMPTY):
                    currentDigit = 0
                elif (self.get(x, y) == self.PIECE_CORNER):
                    currentDigit = 1
                elif (self.get(x, y) == self.PIECE_WHITE):
                    currentDigit = 2
                elif (self.get(x, y) == self.PIECE_BLACK):
                    currentDigit = 3
                else:
                    currentDigit = 4
                total = total + currentDigit * (5 ** order)
                order = order + 1
        return total

    def isWon(self, ourPiece, is_placing = False):
        '''
        Check if all opponent pieces are eliminated,
        and we still have pieces left
        '''
        opponentPiece = self._get_opponent_colour(ourPiece)
        hasOurPiece = False
        for x in range(self._min_xy(), self._max_xy()+1):
            for y in range(self._min_xy(), self._max_xy()+1):
                if self.get(x, y) == opponentPiece:
                    return False
                if self.get(x, y) == ourPiece:
                    hasOurPiece = True
        return hasOurPiece

    def get_status(self, is_placing = False):
        if (is_placing): # placing phase: it is okay to have no piece, game is not ended yet because we can place more.
                return BoardStatus.ON_GOING
        if (self.isWon(Board.PIECE_BLACK)):
            return BoardStatus.BLACK_WON
        elif (self.isWon(Board.PIECE_WHITE)):
            return BoardStatus.WHITE_WON
        else:
            for x in range(self._min_xy(), self._max_xy()+1):
                for y in range(self._min_xy(), self._max_xy()+1):
                    if self.get(x, y) in [Board.PIECE_BLACK, Board.PIECE_WHITE]:
                        return BoardStatus.ON_GOING
            return BoardStatus.TIE
            # TODO: LOW-PERF


    def _get_opponent_colour(self, ourColour):
        '''
        Returns the opponent piece type/colour
        '''
        if (ourColour == self.PIECE_WHITE):
            return self.PIECE_BLACK
        else:
            return self.PIECE_WHITE

    def checkSquareFormation(self, ourPiece):
        # return True if square formation exist
        opponentPiece = self._get_opponent_colour(ourPiece)
        opponentPieces = self.getAllPieces(opponentPiece)
        for p in opponentPieces:
            (x, y) = p
            # square in the top left corner [N, NW, W]
            # N  self.ANTICLOCKWISE[7]
            # NW self.ANTICLOCKWISE[0]
            # W  self.ANTICLOCKWISE[1]
            if (self.ANTICLOCKWISE[7] in opponentPieces and
                self.ANTICLOCKWISE[0] in opponentPieces and
                    self.ANTICLOCKWISE[1] in opponentPieces):
                return True

            # square in the bottom left corner [W, SW, S]
            # W  self.ANTICLOCKWISE[1]
            # SW self.ANTICLOCKWISE[2]
            # S  self.ANTICLOCKWISE[3]
            if (self.ANTICLOCKWISE[1] in opponentPieces and
                self.ANTICLOCKWISE[2] in opponentPieces and
                    self.ANTICLOCKWISE[3] in opponentPieces):
                return True

            # square in the top right corner [N, NE, E]
            # N  self.ANTICLOCKWISE[7]
            # NE self.ANTICLOCKWISE[6]
            # E  self.ANTICLOCKWISE[5]
            if (self.ANTICLOCKWISE[7] in opponentPieces and
                self.ANTICLOCKWISE[6] in opponentPieces and
                    self.ANTICLOCKWISE[5] in opponentPieces):
                return True

            # square in the bottom right corner [E, SE, S]
            # E  self.ANTICLOCKWISE[5]
            # SE self.ANTICLOCKWISE[4]
            # S  self.ANTICLOCKWISE[3]
            if (self.ANTICLOCKWISE[5] in opponentPieces and
                self.ANTICLOCKWISE[4] in opponentPieces and
                    self.ANTICLOCKWISE[3] in opponentPieces):
                return True

        return False

    def checkCantWin(self, ourPiece):
        # check if only 1 white piece and black pieces beside a corner piece
        # return True if cannot win
        ourPieces = self.getAllPieces(ourPiece)
        if len(ourPieces) < 2:
            opponentPiece = self._get_opponent_colour(ourPiece)
            opponentPieces = self.getAllPieces(opponentPiece)
            for p in opponentPieces:
                cornerExist = False
                (x, y) = p
                for direction in range(0, 4):
                    newX = x + self.DIRECTION[direction][0]
                    newY = y + self.DIRECTION[direction][1]
                    if (self.get(newX, newY) == self.PIECE_CORNER):
                        cornerExist = True
                if (cornerExist == False):
                    return True
        return False

    def getMinMaxSearchSpace(self, ourPiece):

        opponentPiece = self._get_opponent_colour(ourPiece)
        allPieces = self.getAllPieces(
            ourPiece) + self.getAllPieces(opponentPiece)

        allX = []
        allY = []

        for p in allPieces:
            (x, y) = p
            allX.append(x)
            allY.append(y)

        minX = min(allX)
        maxX = max(allX)
        minY = min(allY)
        maxY = max(allY)

        searchSpace = []
        # include square space with a buffer
        for x in range(minX - 1, maxX + 2):
            for y in range(minY - 1, maxY + 2):
                if (self.isWithinBoard(x, y)):
                    searchSpace.append((x, y))

        return searchSpace

    def getSmallerSearchSpace(self, ourPiece, layers):
        '''
        mark cells around opponent pieces 
        and return the smaller search space
        '''
        searchSpace = []

        opponentPiece = self._get_opponent_colour(ourPiece)
        opponentPieces = self.getAllPieces(opponentPiece)

        for p in opponentPieces:
            (x, y) = p
            # add coordinate of opponent
            if self.isWithinBoard(x, y) and ((x, y) not in searchSpace):
                searchSpace.append((x, y))

            # for direction in range(0, 4):
            for direction in range(0, 8):

                # add coordinate of cells around opponent
                for i in range(1, layers + 1):
                    # newX = x + self.DIRECTION[direction][0] * i
                    # newY = y + self.DIRECTION[direction][1] * i
                    newX = x + self.ANTICLOCKWISE[direction][0] * i
                    newY = y + self.ANTICLOCKWISE[direction][1] * i

                    if self.isWithinBoard(newX, newY) and \
                        ((newX, newY) not in searchSpace) and \
                            self.get(newX, newY) != self.PIECE_CORNER:
                        searchSpace.append((newX, newY))

        return searchSpace

    def checkElimination(self, x, y, ourPiece):
        '''
        Check and perform elimination, typically called after a player action.
        '''
        opponentPiece = self._get_opponent_colour(ourPiece)

        # step 1: check if we eliminated any opponent pieces
        for direction in range(0, 4):
            adjPieceX = x + self.DIRECTION[direction][0]
            adjPieceY = y + self.DIRECTION[direction][1]
            adjPieceX2 = adjPieceX + self.DIRECTION[direction][0]
            adjPieceY2 = adjPieceY + self.DIRECTION[direction][1]

            # if adjacent piece is within the board and is the opponent and
            # the piece across is within board and is an ally or a corner
            # then we remove the eliminated piece
            if self.isWithinBoard(adjPieceX, adjPieceY) and \
                    self.get(adjPieceX, adjPieceY) == opponentPiece and \
                    self.isWithinBoard(adjPieceX2, adjPieceY2) and \
                    self.get(adjPieceX2, adjPieceY2) in \
                    [ourPiece, self.PIECE_CORNER]:
                self.set(adjPieceX, adjPieceY, self.PIECE_EMPTY)

        # step 2: check if any opponent pieces eliminated us

        # case 1: left and right surround us
        if (self.isWithinBoard(x - 1, y) and
            self.get(x - 1, y) in [opponentPiece, self.PIECE_CORNER]) and \
            (self.isWithinBoard(x + 1, y) and
             self.get(x + 1, y) in [opponentPiece, self.PIECE_CORNER]):
            self.set(x, y, self.PIECE_EMPTY)

        # case 2: above and below surround us
        if (self.isWithinBoard(x, y - 1) and
            self.get(x, y - 1) in [opponentPiece, self.PIECE_CORNER]) and \
            (self.isWithinBoard(x, y + 1) and
             self.get(x, y + 1) in [opponentPiece, self.PIECE_CORNER]):
            self.set(x, y, self.PIECE_EMPTY)

    def makeMove(self, x, y, newX, newY, ourPiece):
        '''
        Make the piece move (valid move) to new location
        and check for elimination.

        Returns a new instance of `Board`.
        '''
        board = copy.deepcopy(self)

        # make the move
        board.set(newX, newY, ourPiece)
        board.set(x, y, self.PIECE_EMPTY)

        board.checkElimination(newX, newY, ourPiece)

        return board

    def placePiece(self, newX, newY, ourPiece):
        """
        Places a new piece. And check for elimination.

        Returns a new instance of `Board`.
        """

        board = copy.deepcopy(self)

        board.set(newX, newY, ourPiece)
        board.checkElimination(newX, newY, ourPiece)

        return board

    def apply_action(self, action, colour):
        if action is None:
            # forfeit turn
            return copy.deepcopy(self)
        else:
            (x, y) = action
            if (isinstance(x, tuple) and isinstance(y, tuple)):
                (a, b) = x
                (c, d) = y
                return self.makeMove(a, b, c, d, colour)
            else:
                # place piece
                return self.placePiece(x, y, colour)

    def shrink(self):
        """
        Shrinks the board. (`boardSize -= 2`)

        Returns a new `Board` instance.
        """
        if (self.boardSize <= 4):
            return self

        board = copy.deepcopy(self)
        # clean the surrounding circle

        for x in range(board._min_xy(), board._max_xy()+1):
            board.set(x, board._min_xy(), Board.PIECE_INVALID)
            board.set(x, board._max_xy(), Board.PIECE_INVALID)

        for y in range(board._min_xy() + 1, board._max_xy()):
            board.set(board._min_xy(), y, Board.PIECE_INVALID)
            board.set(board._max_xy(), y, Board.PIECE_INVALID)

        board.boardSize -= 2
        board._update_corners()

        # do the elimination caused by new corners

        for (x, y) in board._corner_cells():
            for direction in Board.DIRECTION:
                adjX = x + direction[0]
                adjY = y + direction[1]
                adj2X = adjX + direction[0]
                adj2Y = adjY + direction[1]

                if (board.isWithinBoard(adjX, adjY) and
                    board.get(adjX, adjY) in [Board.PIECE_BLACK, Board.PIECE_WHITE] and
                    board.isWithinBoard(adj2X, adj2Y) and
                        board.get(adj2X, adj2Y) in [Board.PIECE_BLACK, Board.PIECE_WHITE]):
                    if (board.get(adjX, adjY) != board.get(adj2X, adj2Y)):
                        board.set(adjX, adjY, Board.PIECE_EMPTY)

        return board

    def getAllPieces(self, ourPiece):
        '''
        get all the location of pieces of a specific colour
        '''
        result = []
        for x in range(self._min_xy(), self._max_xy()+1):
            for y in range(self._min_xy(), self._max_xy()+1):
                if self.get(x, y) == ourPiece:
                    result.append((x, y))
        return result

    def countMoves(self, ourPiece):
        result = 0
        pieces = self.getAllPieces(ourPiece)
        for p in pieces:
            (x, y) = p
            availableMoves = self.getAvailableMoves(x, y)
            result = result + len(availableMoves)
        return result

    def toTokenString(self):
        """
        Converts the board layout to one line string.
        Mainly used for unit tests.
        """
        result = ""
        for y in range(Board.MAX_BOARD_SIZE):
            for x in range(Board.MAX_BOARD_SIZE):
                result = result + self.get(x, y)
            if (y != Board.MAX_BOARD_SIZE-1):
                result = result + "\\\\"
        return result

    @classmethod
    def fromTokenString(cls, ts):
        """
        Creates a new `Board` instance from a tokenString.
        """
        rows = ts.strip().split("\\\\")
        assert len(rows) == cls.MAX_BOARD_SIZE
        board = cls()
        for y in range(Board.MAX_BOARD_SIZE):
            for x in range(Board.MAX_BOARD_SIZE):
                board.set(x, y, rows[y][x])

        # determine board size
        if (board.get(0, 0) == cls.PIECE_INVALID):
            board.boardSize -= 2
            if (board.get(1, 1) == cls.PIECE_INVALID):
                board.boardSize -= 2

        return board
