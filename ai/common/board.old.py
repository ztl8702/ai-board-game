from .cells_array import CellsArray
from .move_type import MoveType
from .board_status import BoardStatus
from .i_board import IBoard
from .config import MAX_BOARD_SIZE
import copy


class Board(IBoard):
    '''
    Representation of the board
    '''

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

    # performance optimization
    set_mapping = {
        PIECE_WHITE: 0,
        PIECE_BLACK: 1,
        PIECE_EMPTY: 2,
        PIECE_CORNER: 3,
        PIECE_INVALID: 4
    }

    get_mapping = {
        0: PIECE_WHITE,
        1: PIECE_BLACK,
        2: PIECE_EMPTY,
        3: PIECE_CORNER,
        4: PIECE_INVALID
    }

    def __init__(self):
        '''
        initially the board size is set to the maximum
        '''
        self.boardSize = MAX_BOARD_SIZE
        self._update_borders()
        self.board = CellsArray(self.boardSize)
        for x in range(MAX_BOARD_SIZE):
            for y in range(MAX_BOARD_SIZE):
                self.set_p(x, y, Board.PIECE_EMPTY)
        self._update_corners()

    def _update_borders(self):
        self._min_xy = (MAX_BOARD_SIZE - self.boardSize) // 2
        self._max_xy = self._min_xy + self.boardSize - 1

    def _corner_cells(self):
        return [
            (self._min_xy, self._min_xy),
            (self._min_xy, self._max_xy),
            (self._max_xy, self._min_xy),
            (self._max_xy, self._max_xy)
        ]

    def _update_corners(self):
        """Updates the corner cells. 

        Called after a shrink and during the initialisation.
        """
        for (x, y) in self._corner_cells():
            self.set_p(x, y, Board.PIECE_CORNER)

    def printBoard(self):
        ''' 
        Debugging utlity function to print board
        '''
        board = self.board.get_inverted()
        print(" ", end="")
        for i in range(MAX_BOARD_SIZE):
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
        return self.get(x, y) == self.PIECE_EMPTY

    def isWithinBoard(self, x, y):
        '''
        returns true if coordinate (x, y) is within the board
        '''
        return ((self._min_xy <= x <= self._max_xy) and (self._min_xy <= y <= self._max_xy))

    def get(self, x, y):
        '''
          Gets the piece at coordinate (x, y)
        '''
        # if (self.isWithinBoard(x, y)):
        return self.get_mapping[self.board.get(x, y)]
        # else:
        #   return self.PIECE_INVALID

    def set_p(self, x, y, value):
        '''
        Change the piece at coordinate (x, y)

        Avoid name conflict with set (built-in type)
        '''
        # if self.isWithinBoard(x, y):
        self.board.set_p(x, y, self.set_mapping[value])

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
        for x in range(self._min_xy, self._max_xy+1):
            for y in range(self._min_xy, self._max_xy+1):
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

    def isWon(self, ourPiece, is_placing=False):
        '''
        Check if all opponent pieces are eliminated,
        and we still have pieces left
        '''
        opponentPiece = self._get_opponent_colour(ourPiece)
        hasOurPiece = False
        for x in range(self._min_xy, self._max_xy+1):
            for y in range(self._min_xy, self._max_xy+1):
                if self.get(x, y) == opponentPiece:
                    return False
                if self.get(x, y) == ourPiece:
                    hasOurPiece = True
        return hasOurPiece

    def get_status(self, is_placing=False):
        # placing phase: it is okay to have no piece, game is not ended yet because we can place more.
        if (is_placing):
            return BoardStatus.ON_GOING
        if (self.isWon(Board.PIECE_BLACK)):
            return BoardStatus.BLACK_WON
        elif (self.isWon(Board.PIECE_WHITE)):
            return BoardStatus.WHITE_WON
        else:
            for x in range(self._min_xy, self._max_xy+1):
                for y in range(self._min_xy, self._max_xy+1):
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

    def _check_elimination(self, x, y, ourPiece):
        '''
        Check and perform elimination, typically called after a player action.
        '''
        opponentPiece = self._get_opponent_colour(ourPiece)

        DIRECTION = self.DIRECTION

        # step 1: check if we eliminated any opponent pieces
        for direction in range(0, 4):
            adjPieceX = x + DIRECTION[direction][0]
            adjPieceY = y + DIRECTION[direction][1]
            adjPieceX2 = adjPieceX + DIRECTION[direction][0]
            adjPieceY2 = adjPieceY + DIRECTION[direction][1]

            # if adjacent piece is within the board and is the opponent and
            # the piece across is within board and is an ally or a corner
            # then we remove the eliminated piece
            if self.isWithinBoard(adjPieceX, adjPieceY) and \
                    self.get(adjPieceX, adjPieceY) == opponentPiece and \
                    self.isWithinBoard(adjPieceX2, adjPieceY2) and \
                    self.get(adjPieceX2, adjPieceY2) in \
                    set([ourPiece, self.PIECE_CORNER]):
                self.set_p(adjPieceX, adjPieceY, self.PIECE_EMPTY)

        # step 2: check if any opponent pieces eliminated us

        opponentPieceOrCorner = set([opponentPiece, self.PIECE_CORNER])
        # case 1: left and right surround us
        if (self.isWithinBoard(x - 1, y) and
            self.get(x - 1, y) in opponentPieceOrCorner) and \
            (self.isWithinBoard(x + 1, y) and
             self.get(x + 1, y) in opponentPieceOrCorner):
            self.set_p(x, y, self.PIECE_EMPTY)

        # case 2: above and below surround us
        if (self.isWithinBoard(x, y - 1) and
            self.get(x, y - 1) in opponentPieceOrCorner) and \
            (self.isWithinBoard(x, y + 1) and
             self.get(x, y + 1) in opponentPieceOrCorner):
            self.set_p(x, y, self.PIECE_EMPTY)

    def makeMove(self, x, y, newX, newY, ourPiece):
        '''
        Make the piece move (valid move) to new location
        and check for elimination.

        Returns a new instance of `Board`.
        '''
        board = copy.deepcopy(self)

        # make the move
        board.set_p(newX, newY, ourPiece)
        board.set_p(x, y, self.PIECE_EMPTY)

        board._check_elimination(newX, newY, ourPiece)

        return board

    def placePiece(self, newX, newY, ourPiece):
        """
        Places a new piece. And check for elimination.

        Returns a new instance of `Board`.
        """

        board = copy.deepcopy(self)

        board.set_p(newX, newY, ourPiece)
        board._check_elimination(newX, newY, ourPiece)

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

        for x in range(board._min_xy, board._max_xy+1):
            board.set_p(x, board._min_xy, Board.PIECE_INVALID)
            board.set_p(x, board._max_xy, Board.PIECE_INVALID)

        for y in range(board._min_xy + 1, board._max_xy):
            board.set_p(board._min_xy, y, Board.PIECE_INVALID)
            board.set_p(board._max_xy, y, Board.PIECE_INVALID)

        board.boardSize -= 2
        board._update_borders()
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
                        board.set_p(adjX, adjY, Board.PIECE_EMPTY)

        return board

    def get_all_pieces(self, ourPiece):
        '''
        get all the location of pieces of a specific colour
        '''
        result = []
        for x in range(self._min_xy, self._max_xy+1):
            for y in range(self._min_xy, self._max_xy+1):
                if self.get(x, y) == ourPiece:
                    result.append((x, y))
        return result

    def count_moves(self, ourPiece):
        result = 0
        pieces = self.get_all_pieces(ourPiece)
        for p in pieces:
            (x, y) = p
            availableMoves = self.getAvailableMoves(x, y)
            result = result + len(availableMoves)
        return result

    def to_token_string(self):
        """
        Converts the board layout to one line string.
        Mainly used for unit tests.
        """
        result = ""
        for y in range(MAX_BOARD_SIZE):
            for x in range(MAX_BOARD_SIZE):
                result = result + self.get(x, y)
            if y != MAX_BOARD_SIZE-1:
                result = result + "\\\\"
        return result

    @classmethod
    def from_token_string(cls, ts):
        """
        Creates a new `Board` instance from a tokenString.
        """
        rows = ts.strip().split("\\\\")
        assert len(rows) == MAX_BOARD_SIZE
        board = cls()
        for y in range(MAX_BOARD_SIZE):
            for x in range(MAX_BOARD_SIZE):
                board.set_p(x, y, rows[y][x])

        # determine board size
        if board.get(0, 0) == cls.PIECE_INVALID:
            board.boardSize -= 2
            if board.get(1, 1) == cls.PIECE_INVALID:
                board.boardSize -= 2

        return board
