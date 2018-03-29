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
                newCellsArray.set(x, y, self.get(j,i))
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

        for line in board.cells:
            for piece in line:
                print(piece, end=' ')
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
                    xNew = x + self.DIRECTION[direction][0]
                    yNew = y + self.DIRECTION[direction][1]

                # make jump move
                elif result == MoveType.JUMP:
                    xNew = x + self.DIRECTION[direction][0] * 2
                    yNew = y + self.DIRECTION[direction][1] * 2
                possibleMoves.append(((x, y),(xNew, yNew)))

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
        for i in range(0, self.boardSize):
            for j in range(0, self.boardSize):
                if (self.get(i,j) == self.PIECE_EMPTY):
                    currentDigit = 0
                elif (self.get(i,j) == self.PIECE_CORNER):
                    currentDigit = 1
                elif (self.get(i,j) == self.PIECE_WHITE):
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
        
        for i in range(0, self.boardSize):
            for j in range(0, self.boardSize):
                if self.get(i,j) == opponentPiece:
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

    # def checkSurrounded(self, board, ourPiece, pieces):
    #     '''
    #     check if ourPiece is surrounded by opponent pieces
    #     '''
        
    #     for p in pieces:
    #         (x, y) = p  # current piece coordinate
    #         opponentPiece = self.__getOpponentColour(ourPiece)

    #         # # alternative2: step 1
    #         # for direction in range(0, 4):
    #         #     adjPieceX = x + self.DIRECTION[direction][0]
    #         #     adjPieceY = y + self.DIRECTION[direction][1]
    #         #     adjPieceX2 = adjPieceX + self.DIRECTION[direction][0]
    #         #     adjPieceY2 = adjPieceY + self.DIRECTION[direction][1]
    #         #     # if adjacent piece is within the board and is the opponent and
    #         #     # piece across adjacent is within board and is ours or a corner
    #         #     # then we remove the eliminated adjacent piece
    #         #     if board.isWithinBoard(adjPieceX, adjPieceY) and \
    #         #     board.get(adjPieceX, adjPieceY) == opponentPiece and \
    #         #     board.isWithinBoard(adjPieceX2, adjPieceY2) and \
    #         #     board.get(adjPieceX2, adjPieceY2) in \
    #         #     [ourPiece, self.PIECE_CORNER]:
    #         #         board.set(adjPieceX, adjPieceY, self.PIECE_EMPTY)

    #         #  alternative 2: step 2
    #         (left, right, up, down) = self.DIRECTION

    #         leftPieceX = x + left[0]
    #         leftPieceY = y + left[1]
    #         rightPieceX = x + right[0]
    #         rightPieceY = y + right[1]

    #         # if pieces on the left and on the right are opponent pieces
    #         # eliminate ourself
    #         if board.isWithinBoard(leftPieceX,leftPieceY) and \
    #         board.get(leftPieceX,leftPieceY) in \
    #         [opponentPiece,self.PIECE_CORNER] and \
    #         board.isWithinBoard(rightPieceX,rightPieceY) and \
    #         board.get(rightPieceX,rightPieceY) in \
    #         [opponentPiece,self.PIECE_CORNER]:
    #             board.set(x, y,self.PIECE_EMPTY)

    #         upPieceX = x + up[0]
    #         upPieceY = y + up[1]
    #         downPieceX = x + down[0]
    #         downPieceY = y + down[1]
    #         # if pieces above and below are opponent pieces
    #         # eliminate ourself
    #         if board.isWithinBoard(upPieceX,upPieceY) and \
    #         board.get(upPieceX,upPieceY) in \
    #         [opponentPiece,self.PIECE_CORNER] and \
    #         board.isWithinBoard(downPieceX,downPieceY) and \
    #         board.get(downPieceX,downPieceY) in \
    #         [opponentPiece,self.PIECE_CORNER]:
    #             board.set(x, y,self.PIECE_EMPTY)

    #     return board

    # def checkElimination(self, board, ourPiece):
    #     '''
    #     eliminate pieces based on rules
    #     and return the board
    #     '''        
        
    #     # alternative 1: step 1
    #     # check if we eliminated opponent pieces first
    #     opponentPiece = self.__getOpponentColour(ourPiece)
    #     opponentPieces = self.getAllPieces(opponentPiece)
    #     board = self.checkSurrounded(board, opponentPiece, opponentPieces)

    #     # alternative 1: step 2
    #     # then check if opponents eliminated us
    #     ourPieces = self.getAllPieces(ourPiece)
    #     board = self.checkSurrounded(board, ourPiece, ourPieces)

    #     return board

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
        board.get(x, y -1 ) in [opponentPiece, self.PIECE_CORNER]) and \
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
        for i in range(0, self.boardSize):
            for j in range(0, self.boardSize):
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