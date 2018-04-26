import copy
from enum import Enum

class MoveType(Enum):
    # enum to represent different type of moves
    INVALID = 0
    NORMAL = 1
    JUMP = 2

class CellsArray:
    '''
    a 2d array representing all the cells
    '''
    def __init__(self, size):
        '''
        initialise a 2d array
        '''
        self.size = size
        self.cells = [
            [0 for x in range(0, size)] \
            for y in range(0, size)
        ]

    def get(self, x, y):
        '''
        get piece type
        '''
        return self.cells[x][y]
    
    def set(self, x, y, value):
        '''
        change cell type 
        '''
        self.cells[x][y] = value

    def getInverted(self):
        '''
        utility function to invert the cells array 
        '''
        newCellsArray = copy.deepcopy(self)
        for x in range(0, self.size):
            for y in range(0, self.size):
                newCellsArray.set(x, y, self.get(y, x))
        return newCellsArray

class Board:
    '''
    represents the board
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
                self.set(x,y,Board.PIECE_EMPTY)

        self.set(0, 0, Board.PIECE_CORNER)
        self.set(0, self.boardSize-1, Board.PIECE_CORNER)
        self.set(self.boardSize-1, 0, Board.PIECE_CORNER)
        self.set(self.boardSize-1, self.boardSize-1, Board.PIECE_CORNER)

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
        print(" ", end = "")
        for i in range(self.MAX_BOARD_SIZE):
            print(i, end = " ")
        print()

        j = 0
        for line in board.cells:
            print(j, end = "")
            j = j + 1
            for piece in line:
                print(piece, end = " ")
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
        return (x in range(0, self.boardSize)) and \
        (y in range(0, self.boardSize))

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
        change coordinate (x, y)
        '''
        if (self.isWithinBoard(x, y)):
            self.board.set(x, y, value)

    def getMoveType(self, x, y, direction):
        '''
        check what type of move it is
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

        # not a valid move, so cant move
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

                possibleMoves.append(((x, y),(newX, newY)))

        return possibleMoves

    def getHashValue(self):
        '''
        reasoning for method:
        use hash value to compare board states instead of 
        iterating through each cell to check board states that have been seen

        compute hash value for entire board
        this is done by treating pieces as integers from 0 through 3
        using base 4 digit system (quaternary numeral system)
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
                else:
                    currentDigit = 3
                total = total + currentDigit * (4 ** order)
                order = order + 1
        return total

    def isWon(self, ourPiece):
        '''
        check if all opponent pieces are eliminated
        '''
        opponentPiece = self.__getOpponentColour(ourPiece)
        
        for x in range(0, self.boardSize):
            for y in range(0, self.boardSize):
                if self.get(x, y) == opponentPiece:
                    return False
        return True

    def __getOpponentColour(self, ourColour):
        '''
        return the opponent piece type/colour
        '''
        if (ourColour == self.PIECE_WHITE):
            return self.PIECE_BLACK
        else:
            return self.PIECE_WHITE

    def checkSquareFormation(self, ourPiece):
        # return True if square formation exist
        opponentPiece = self.__getOpponentColour(ourPiece)
        opponentPieces = self.getAllPieces(opponentPiece)
        for p in opponentPieces:
            (x, y) = p
            # square in the top left corner [N, NW, W]
            # N  self.ANTICLOCKWISE[7]
            # NW self.ANTICLOCKWISE[0]
            # W  self.ANTICLOCKWISE[1]
            if (self.ANTICLOCKWISE[7] in opponentPieces and \
            self.ANTICLOCKWISE[0] in opponentPieces and \
            self.ANTICLOCKWISE[1] in opponentPieces):
                return True

            # square in the bottom left corner [W, SW, S]
            # W  self.ANTICLOCKWISE[1]
            # SW self.ANTICLOCKWISE[2]
            # S  self.ANTICLOCKWISE[3]
            if (self.ANTICLOCKWISE[1] in opponentPieces and \
            self.ANTICLOCKWISE[2] in opponentPieces and \
            self.ANTICLOCKWISE[3] in opponentPieces):
                return True
            
            # square in the top right corner [N, NE, E]
            # N  self.ANTICLOCKWISE[7]
            # NE self.ANTICLOCKWISE[6]
            # E  self.ANTICLOCKWISE[5]
            if (self.ANTICLOCKWISE[7] in opponentPieces and \
            self.ANTICLOCKWISE[6] in opponentPieces and \
            self.ANTICLOCKWISE[5] in opponentPieces):
                return True
            
            # square in the bottom right corner [E, SE, S]
            # E  self.ANTICLOCKWISE[5]
            # SE self.ANTICLOCKWISE[4]
            # S  self.ANTICLOCKWISE[3]
            if (self.ANTICLOCKWISE[5] in opponentPieces and \
            self.ANTICLOCKWISE[4] in opponentPieces and \
            self.ANTICLOCKWISE[3] in opponentPieces):
                return True
                
        return False


    def checkCantWin(self, ourPiece):
        # check if only 1 white piece and black pieces beside a corner piece
        # return True if cannot win
        ourPieces = self.getAllPieces(ourPiece) 
        if len(ourPieces) < 2:
            opponentPiece = self.__getOpponentColour(ourPiece)
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

        opponentPiece = self.__getOpponentColour(ourPiece)
        allPieces = self.getAllPieces(ourPiece) + self.getAllPieces(opponentPiece)
        
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

        opponentPiece = self.__getOpponentColour(ourPiece)
        opponentPieces = self.getAllPieces(opponentPiece)
        
        for p in opponentPieces:
            (x, y) = p
            # add coordinate of opponent
            if self.isWithinBoard(x, y) and ((x, y) not in searchSpace):
                searchSpace.append((x,y))

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

    def checkElimination(self, x, y, ourPiece, board):
        '''
        check for elimination
        '''
        opponentPiece = self.__getOpponentColour(ourPiece)

        # step 1: check if we eliminated any opponent pieces
        for direction in range(0, 4):
            adjPieceX = x + self.DIRECTION[direction][0]
            adjPieceY = y + self.DIRECTION[direction][1]
            adjPieceX2 = adjPieceX + self.DIRECTION[direction][0]
            adjPieceY2 = adjPieceY + self.DIRECTION[direction][1]

            # if adjacent piece is within the board and is the opponent and
            # the piece across is within board and is an ally or a corner
            # then we remove the eliminated piece
            if board.isWithinBoard(adjPieceX, adjPieceY) and \
            board.get(adjPieceX, adjPieceY) == opponentPiece and \
            board.isWithinBoard(adjPieceX2, adjPieceY2) and \
            board.get(adjPieceX2, adjPieceY2) in \
            [ourPiece, self.PIECE_CORNER]:
                board.set(adjPieceX, adjPieceY, self.PIECE_EMPTY)

        # step 2: check if any opponent pieces eliminated us

        # case 1: left and right surround us
        if (board.isWithinBoard(x - 1, y) and \
        board.get(x - 1, y) in [opponentPiece, self.PIECE_CORNER]) and \
        (board.isWithinBoard(x + 1, y) and \
        board.get(x + 1, y) in [opponentPiece, self.PIECE_CORNER]):
            board.set(x, y, self.PIECE_EMPTY)

        # case 2: above and below surround us
        if (board.isWithinBoard(x, y - 1) and \
        board.get(x, y - 1) in [opponentPiece, self.PIECE_CORNER]) and \
        (board.isWithinBoard(x, y + 1) and \
        board.get(x, y + 1) in [opponentPiece, self.PIECE_CORNER]):
            board.set(x, y, self.PIECE_EMPTY)
            
        return board

    def makeMove(self, x, y, newX, newY, ourPiece):
        '''
        make the piece move (valid move) to new location
        and check for elimination
        '''
        board = copy.deepcopy(self)

        # make the move
        board.set(newX, newY, ourPiece)
        board.set(x, y, self.PIECE_EMPTY)

        board = self.checkElimination(newX, newY, ourPiece, board)
        
        return board

    def getAllPieces(self, ourPiece):
        '''
        get all the location of pieces of a specific colour
        '''
        result = []
        for x in range(0, self.boardSize):
            for y in range(0, self.boardSize):
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
                result = result + self.get(x,y)
            if (y!=Board.MAX_BOARD_SIZE-1):
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
                board.set(x,y, rows[y][x])

        # determine board size
        if (board.get(0,0) == cls.PIECE_INVALID):
            board.boardSize -= 1
            if (board.get(1,1) == cls.PIECE_INVALID):
                board.boardSize -= 1
        
        return board
