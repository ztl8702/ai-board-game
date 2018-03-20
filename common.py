import copy
from enum import Enum

class MoveType(Enum):
    INVALID = 0
    SIMPLEMOVE = 1
    JUMP = 2

class CellsArray:
    '''
    '''
    def __init__(self, size):
        self.size = size
        self.cells = [
            [0 for x in range(0, size)] \
            for y in range(0, size)
        ]

    def get(self,x,y):
        return self.cells[x][y]
    
    def set(self,x,y,value):
        self.cells[x][y] = value

    def getInverted(self):
        newCA = copy.deepcopy(self)
        for i in range(0, self.size):
            for j in range(0, self.size):
                newCA.set(i,j, self.get(j,i))
        return newCA

class Board:
    MAX_BOARD_SIZE = 8

    DIRECTION = [
        [-1, 0],  # left
        [+1, 0],  # right
        [0, -1],  # up
        [0, +1]   # down
    ]

    PIECE_WHITE = 'O'
    PIECE_BLACK = '@'
    PIECE_EMPTY = '-'
    PIECE_CORNER = 'X'
   
    def __init__(self):
        # initially the board size is set to the maximum
        self.boardSize = self.MAX_BOARD_SIZE

    def readInput(self):
        '''
          Read and parse the board layout from stdin
        '''
        tmpBoard = CellsArray(self.MAX_BOARD_SIZE)

        for i in range(0, self.MAX_BOARD_SIZE):
            row = input().strip().split(" ")
            for j in range(0, self.MAX_BOARD_SIZE):
                tmpBoard.set(i,j,row[j])
                
        self.cells = tmpBoard.getInverted()
    
    def printBoard(self):
        board = self.cells.getInverted()

        for line in board.cells:
            for piece in line:
                print(piece, end=' ')
            print('')
        print('')

    def isEmpty(self, x, y):
        return self.cells.get(x, y) == self.PIECE_EMPTY
    
    def isWithinBoard(self, x, y):
        return (x in range(0, self.boardSize)) and (y in range(0, self.boardSize))

    def get(self, x, y):
        '''
          Gets the piece at (x, y)
          Returns 'X' if (x, y) is outside the board
        '''
        if (self.isWithinBoard(x,y)):
            return self.cells.get(x,y)
        else:
            return self.PIECE_CORNER

    def set(self, x, y, value):
        if (self.isWithinBoard(x,y)):
            self.cells.set(x,y, value)

    def getMoveType(self, x, y, direction):
        '''
        '''
        newX = x + self.DIRECTION[direction][0]
        newY = y + self.DIRECTION[direction][1]
        # if empty
        if self.isWithinBoard(newX, newY) and self.isEmpty(newX, newY):
            return MoveType.SIMPLEMOVE

        # if can jump
        newX2 = newX + self.DIRECTION[direction][0]
        newY2 = newY + self.DIRECTION[direction][1]
        if self.isWithinBoard(newX2, newY2) and \
        self.isEmpty(newX2, newY2) and \
        self.get(newX, newY) in [self.PIECE_WHITE, self.PIECE_BLACK]:
            return MoveType.JUMP

        return MoveType.INVALID

    def getAvailableMoves(self, x, y):
        '''
            Returns a list of available move for the piece at (x,y)

        '''
        if not (self.get(x,y) in [self.PIECE_WHITE, self.PIECE_BLACK]):
            return []
        
        possibleMoves = []
        for direction in range(0, 4):
            result = self.getMoveType(x, y, direction)
            if result != MoveType.INVALID:
                # check if move is valid then make normal move
                if result == MoveType.SIMPLEMOVE:
                    xNew = x + self.DIRECTION[direction][0]
                    yNew = y + self.DIRECTION[direction][1]
                # check if move is valid then make jump move
                elif result == MoveType.JUMP:
                    xNew = x + self.DIRECTION[direction][0] * 2
                    yNew = y + self.DIRECTION[direction][1] * 2
                possibleMoves.append(((x, y),(xNew, yNew)))
        return possibleMoves

    def getHashValue(self):
        '''
            computing hash value for entire board
            by treating pieces as integers from 0 through 3
            and base 4 digit system (quaternary numeral system)
            @TODO: EXPLAIN WITH AN EXAMPLE using first line
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

    # check if all pieces needed to be killed is eliminated
    def isWon(self, ourPieceColour = PIECE_WHITE):
        pieceToKill = self.__getOpponentColour(ourPieceColour)
        
        for i in range(0, self.boardSize):
            for j in range(0, self.boardSize):
                if self.get(i,j) == pieceToKill:
                    return False
        return True

    def __getOpponentColour(self, ourColour):
        if (ourColour == self.PIECE_WHITE):
            return self.PIECE_BLACK
        else:
            return self.PIECE_WHITE

    def makeMove(self, x, y, newX, newY, pieceColour = PIECE_WHITE):
        opponentColour = self.__getOpponentColour(pieceColour)
        board = copy.deepcopy(self)
        board.set(newX, newY, board.get(x,y))
        board.set(x, y, self.PIECE_EMPTY)

        # step 1: white eliminating black
        for direction in range(0, 4):
            adjPieceX = newX + self.DIRECTION[direction][0]
            adjPieceY = newY + self.DIRECTION[direction][1]
            adjPieceX2 = adjPieceX + self.DIRECTION[direction][0]
            adjPieceY2 = adjPieceY + self.DIRECTION[direction][1]
            # if adjacent piece is within the board and is the opponent
            # and jumping adjacent piece is within board and is ours or a corner
            # then we remove the eliminated piece (ie. black piece)
            if board.isWithinBoard(adjPieceX, adjPieceY) and \
            board.get(adjPieceX, adjPieceY) == opponentColour and \
            board.isWithinBoard(adjPieceX2, adjPieceY2) and \
            board.get(adjPieceX2, adjPieceY2) in [pieceColour, self.PIECE_CORNER]:
                board.set(adjPieceX, adjPieceY, self.PIECE_EMPTY)


        # step 2: black eliminating white
        # (is left within Border and have opponent or corner) and (right withinBoarder and have opponent or corner)
        if (board.isWithinBoard(newX - 1, newY) and \
        board.get(newX - 1, newY) in [opponentColour, self.PIECE_CORNER]) and \
        (board.isWithinBoard(newX + 1, newY) and \
        board.get(newX + 1, newY) in [opponentColour, self.PIECE_CORNER]):
            board.set(newX, newY, self.PIECE_EMPTY)

        # (is up within Border and have opponent or corner) and (down withinBoarder and have opponent or corner)
        if (board.isWithinBoard(newX, newY - 1) and \
        board.get(newX, newY -1 ) in [opponentColour, self.PIECE_CORNER]) and \
        (board.isWithinBoard(newX, newY+1) and \
        board.get(newX, newY+1) in [opponentColour, self.PIECE_CORNER]):
            board.set(newX, newY, self.PIECE_EMPTY)

        return board

    def getAllPieces(self, pieceColour = PIECE_WHITE):
        '''
        '''
        result = []
        for i in range(0, self.boardSize):
            for j in range(0, self.boardSize):
                if self.get(i, j) == pieceColour:
                    result.append((i,j))
        return result

    def countMoves(self, pieceColour =PIECE_WHITE):
        result = 0
        pieces = self.getAllPieces(pieceColour)
        for p in pieces:
            (i, j) = p
            availableMoves = self.getAvailableMoves(i,j)
            result = result + len(availableMoves)
        return result
