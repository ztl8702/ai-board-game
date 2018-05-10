from .MoveType import MoveType
from .board_status import BoardStatus
from .i_board import IBoard
from .config import MAX_BOARD_SIZE
import copy
import array


class LazyBoard(IBoard):
    '''
    Representation of the board

    With "lazy actions" to improve performance
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

    PLAYER_PIECES = set([PIECE_BLACK, PIECE_WHITE])

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

    def __init__(self, cloneFrom=None):
        '''
        initially the board size is set to the maximum
        '''
        if (cloneFrom != None):
            self.boardSize = cloneFrom.boardSize
            self._update_borders()
            self.masterCopy = False
            self.unapplied_actions = list(cloneFrom.unapplied_actions)
            self.all_pieces = cloneFrom.all_pieces
            self.has_unapplied_actions = True
            self.board = cloneFrom.board
            self.hash_value_cache = None
        else:
            self.boardSize = MAX_BOARD_SIZE
            self._update_borders()
            self.masterCopy = True
            self.has_unapplied_actions = False
            self.unapplied_actions = []
            self.board = [array.array('B', [2]*MAX_BOARD_SIZE)
                          for x in range(MAX_BOARD_SIZE)]
            # optimization for get_all_pieces
            self.all_pieces = {
                self.PIECE_WHITE: set(),
                self.PIECE_BLACK: set(),
                self.PIECE_EMPTY: set([(x, y) for x in range(MAX_BOARD_SIZE) for y in range(MAX_BOARD_SIZE)]),
                self.PIECE_CORNER: set(),
                self.PIECE_INVALID: set()
            }
            self._update_corners()
            self.hash_value_cache = None

        self._reentrant_counter_do_place_piece = 0
        self._reentrant_counter_do_make_move = 0

    def _update_borders(self):
        self._min_xy = (MAX_BOARD_SIZE - self.boardSize) // 2
        self._max_xy = self._min_xy + self.boardSize - 1

    def _corner_cells(self):
        return [
            (self._min_xy, self._min_xy),
            (self._max_xy, self._min_xy),
            (self._max_xy, self._max_xy),
            (self._min_xy, self._max_xy)
        ]

    def _update_corners(self):
        """Updates the corner cells. 

        Called after a shrink and during the initialisation.
        """
        for (x, y) in self._corner_cells():
            self.set_p(x, y, self.PIECE_CORNER)

    def printBoard(self):
        ''' 
        Debugging utlity function to print board
        '''
        print(" ", end="")
        for i in range(MAX_BOARD_SIZE):
            print(i, end=" ")
        print()

        for y in range(MAX_BOARD_SIZE):
            print(y, end="")
            for x in range(MAX_BOARD_SIZE):
                print(self.get(x, y), end=" ")
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
          return the piece type
        '''
        if self.has_unapplied_actions:
            self.has_unapplied_actions = False
            self._apply_unapplied_actions()
        # if (self.isWithinBoard(x, y)):
        return self.get_mapping[self.board[x][y]]
        # else:
        #   return self.PIECE_INVALID
    
    def raw_get(self, x, y):
        """
        get() without the laziness checking.

        This is for preventing reentrant into _apply_unapplied_actions
        """
        return self.get_mapping[self.board[x][y]]

    def set_p(self, x, y, value):
        '''
        Change the piece at coordinate (x, y)

        Avoid name conflict with set (built-in type)
        '''
        if not self.masterCopy:
            self.board = copy.deepcopy(self.board)
            old_all_pieces = self.all_pieces
            # manual "deepcopy" seems faster
            # using string literals for performance
            self.all_pieces = {
                "O": set(old_all_pieces['O']),
                "@": set(old_all_pieces['@']),
                "-": set(old_all_pieces['-']),
                "X": set(old_all_pieces['X']),
                "#": set(old_all_pieces['#'])
            }
            # copy.deepcopy(self.all_pieces)
            self.masterCopy = True
        self.hash_value_cache = None
        oldValue = self.get_mapping[self.board[x][y]]
        self.board[x][y] = self.set_mapping[value]
        self.all_pieces[oldValue].remove((x, y))
        self.all_pieces[value].add((x, y))

    def _apply_unapplied_actions(self):
        for action in self.unapplied_actions:
            actionType, args = action
            if actionType == 'makeMove':
                x, y, newX, newY, ourPiece = args
                self._do_make_move(x, y, newX, newY, ourPiece)
            elif actionType == 'placePiece':
                newX, newY, ourPiece = args
                self._do_place_piece(newX, newY, ourPiece)
        self.unapplied_actions.clear()

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
                self.get(newX, newY) in self.PLAYER_PIECES:
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
        if not (self.get(x, y) in self.PLAYER_PIECES):
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
        #result = []
        # for x in range(self._min_xy, self._max_xy+1):
        #    for y in range(self._min_xy, self._max_xy+1):
        #        if (self.isEmpty(x, y)):
        #            result.append((x, y))
        self._apply_unapplied_actions()
        return list(self.all_pieces[self.PIECE_EMPTY])

    def getHashValue(self):
        '''
        Computes a hash value for entire board.
        '''
        if self.hash_value_cache != None:
            return self.hash_value_cache
        self._apply_unapplied_actions()
        joined = b''
        for arr in self.board:
            joined = joined+arr.tobytes()
        self.hash_value_cache = hash(joined)
        return hash(joined)

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
        if (self.isWon(self.PIECE_BLACK)):
            return BoardStatus.BLACK_WON
        elif (self.isWon(self.PIECE_WHITE)):
            return BoardStatus.WHITE_WON
        else:
            for x in range(self._min_xy, self._max_xy+1):
                for y in range(self._min_xy, self._max_xy+1):
                    if self.get(x, y) in [self.PIECE_BLACK, self.PIECE_WHITE]:
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

    def getSmallerSearchSpace(self, ourPiece, layers):
        '''
        mark cells around opponent pieces 
        and return the smaller search space
        '''
        searchSpace = []

        opponentPieces = self.get_all_pieces( \
            self._get_opponent_colour(ourPiece))
        
        for p in opponentPieces:
            (x, y) = p
            # add coordinate of opponent
            searchSpace.append((x,y))

            for direction in range(0, 4):

                # add coordinate of cells around opponent
                for i in range(1, layers + 1):
                    newX = x + self.DIRECTION[direction][0] * i
                    newY = y + self.DIRECTION[direction][1] * i
                    
                    if (self.isWithinBoard(newX, newY)):
                        searchSpace.append((newX, newY))

        return searchSpace

    def _check_elimination(self, x, y, ourPiece):
        '''
        Check and perform elimination, typically called after a player action.

        WARNING: to prevent reentrant, _check_elimination should only be called
        in _do_make_move and _do_place_piece
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
                    self.raw_get(adjPieceX, adjPieceY) == opponentPiece and \
                    self.isWithinBoard(adjPieceX2, adjPieceY2) and \
                    self.raw_get(adjPieceX2, adjPieceY2) in \
                    set([ourPiece, self.PIECE_CORNER]):
                self.set_p(adjPieceX, adjPieceY, self.PIECE_EMPTY)

        # step 2: check if any opponent pieces eliminated us

        opponentPieceOrCorner = set([opponentPiece, self.PIECE_CORNER])
        # case 1: left and right surround us
        if (self.isWithinBoard(x - 1, y) and
            self.raw_get(x - 1, y) in opponentPieceOrCorner) and \
            (self.isWithinBoard(x + 1, y) and
             self.raw_get(x + 1, y) in opponentPieceOrCorner):
            self.set_p(x, y, self.PIECE_EMPTY)

        # case 2: above and below surround us
        if (self.isWithinBoard(x, y - 1) and
            self.raw_get(x, y - 1) in opponentPieceOrCorner) and \
            (self.isWithinBoard(x, y + 1) and
             self.raw_get(x, y + 1) in opponentPieceOrCorner):
            self.set_p(x, y, self.PIECE_EMPTY)

    def makeMove(self, x, y, newX, newY, ourPiece):
        '''
        Make the piece move (valid move) to new location
        and check for elimination.

        Returns a new instance of `Board`.
        '''
        board = LazyBoard(self)
        board.unapplied_actions.append(
            ('makeMove', (x, y, newX, newY, ourPiece))
        )
        return board

    def _do_make_move(self, x, y, newX, newY, ourPiece):
        if (self._reentrant_counter_do_make_move > 0):
            raise Exception("Reentrant: _do_make_move")
        self._reentrant_counter_do_make_move+=1
        self.set_p(newX, newY, ourPiece)
        self.set_p(x, y, self.PIECE_EMPTY)

        self._check_elimination(newX, newY, ourPiece)
        self._reentrant_counter_do_make_move-=1
        

    def placePiece(self, newX, newY, ourPiece):
        """
        Places a new piece. And check for elimination.

        Returns a new instance of `Board`.

        Lazy action: we don't actually modify the board.
        """

        board = LazyBoard(self)
        board.unapplied_actions.append(
            ('placePiece', (newX, newY, ourPiece))
        )

        return board

    def _do_place_piece(self, newX, newY, colour):
        """
        Realisation of lazy action.
        """
        if (self._reentrant_counter_do_place_piece > 0):
            raise Exception("Reentrant: _do_place_piece")
        self._reentrant_counter_do_place_piece+=1
        self.set_p(newX, newY, colour)
        self._check_elimination(newX, newY, colour)
        self._reentrant_counter_do_place_piece -= 1

    def apply_action(self, action, colour):
        """
        Apply oppponent's actions given by the referee.

        Used for keeping the states up to date.
        """
        if action is None:
            # forfeit turn
            return LazyBoard(self)
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

        board = LazyBoard(self)
        board._apply_unapplied_actions()
        # clean the surrounding circle

        for x in range(board._min_xy, board._max_xy+1):
            board.set_p(x, board._min_xy, self.PIECE_INVALID)
            board.set_p(x, board._max_xy, self.PIECE_INVALID)

        for y in range(board._min_xy + 1, board._max_xy):
            board.set_p(board._min_xy, y, self.PIECE_INVALID)
            board.set_p(board._max_xy, y, self.PIECE_INVALID)

        board.boardSize -= 2
        board._update_borders()
        board._update_corners()

        # do the elimination caused by new corners

        for (x, y) in board._corner_cells():
            for direction in self.DIRECTION:
                adjX = x + direction[0]
                adjY = y + direction[1]
                adj2X = adjX + direction[0]
                adj2Y = adjY + direction[1]

                if (board.isWithinBoard(adjX, adjY) and
                    board.get(adjX, adjY) in [self.PIECE_BLACK, self.PIECE_WHITE] and
                    board.isWithinBoard(adj2X, adj2Y) and
                        board.get(adj2X, adj2Y) in [self.PIECE_BLACK, self.PIECE_WHITE]):
                    if (board.get(adjX, adjY) != board.get(adj2X, adj2Y)):
                        board.set_p(adjX, adjY, self.PIECE_EMPTY)

        return board

    def get_all_pieces(self, ourPiece):
        '''
        get all the location of pieces of a specific colour
        '''
        #result = []
        # for x in range(self._min_xy, self._max_xy+1):
        #    for y in range(self._min_xy, self._max_xy+1):
        #        if self.get(x, y) == ourPiece:
        #            result.append((x, y))
        self._apply_unapplied_actions()
        #print("get_all_pieces called", ourPiece, self.all_pieces[ourPiece])
        return list(self.all_pieces[ourPiece])

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
