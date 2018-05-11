from .move_type import MoveType
from .board_status import BoardStatus
from .i_board import IBoard
from .config import MAX_BOARD_SIZE
import copy
import array


class LazyBoard(IBoard):
    """
    Representation of the board

    With "lazy actions" to improve performance
    """

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

    def __init__(self, clone_from=None):
        """
        initially the board size is set to the maximum
        """
        if (clone_from != None):
            self.board_size = clone_from.board_size
            self._update_borders()
            self.master_copy = False
            self.unapplied_actions = list(clone_from.unapplied_actions)
            self.all_pieces = clone_from.all_pieces
            self.has_unapplied_actions = True
            self.board = clone_from.board
            self.hash_value_cache = None
        else:
            self.board_size = MAX_BOARD_SIZE
            self._update_borders()
            self.master_copy = True
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
        self._min_xy = (MAX_BOARD_SIZE - self.board_size) // 2
        self._max_xy = self._min_xy + self.board_size - 1

    def _corner_cells(self):
        return [
            (self._min_xy, self._min_xy),
            (self._min_xy, self._max_xy),
            (self._max_xy, self._max_xy),
            (self._max_xy, self._min_xy)
        ]

    def _update_corners(self):
        """Updates the corner cells. 

        Called after a shrink and during the initialisation.
        """
        for (x, y) in self._corner_cells():
            self.set_p(x, y, self.PIECE_CORNER)

    def print_board(self):
        """ 
        Debugging utlity function to print board
        """
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

    def is_empty(self, x, y):
        """
        check if coordinate (x, y) is empty
        """
        return self.get(x, y) == self.PIECE_EMPTY

    def is_within_board(self, x, y):
        """
        returns true if coordinate (x, y) is within the board
        """
        return ((self._min_xy <= x <= self._max_xy) and (self._min_xy <= y <= self._max_xy))

    def get(self, x, y):
        """
          Gets the piece at coordinate (x, y)
          return the piece type
        """
        if self.has_unapplied_actions:
            self.has_unapplied_actions = False
            self._apply_unapplied_actions()
        # if (self.is_within_board(x, y)):
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
        """
        Change the piece at coordinate (x, y)

        Avoid name conflict with set (built-in type)
        """
        if not self.master_copy:
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
            self.master_copy = True
        self.hash_value_cache = None
        old_value = self.get_mapping[self.board[x][y]]
        self.board[x][y] = self.set_mapping[value]
        self.all_pieces[old_value].remove((x, y))
        self.all_pieces[value].add((x, y))

    def _apply_unapplied_actions(self):
        for action in self.unapplied_actions:
            action_type, args = action
            if action_type == 'make_move':
                x, y, new_x, new_y, our_piece = args
                self._do_make_move(x, y, new_x, new_y, our_piece)
            elif action_type == 'place_piece':
                new_x, new_y, our_piece = args
                self._do_place_piece(new_x, new_y, our_piece)
        self.unapplied_actions.clear()

    def _get_move_type(self, x, y, direction):
        """
        Check what type of move it is
        and return its type
        """
        new_x = x + self.DIRECTION[direction][0]
        new_y = y + self.DIRECTION[direction][1]
        # if the cell is not occupied, its a normal move
        if self.is_within_board(new_x, new_y) and self.is_empty(new_x, new_y):
            return MoveType.NORMAL

        # its a jump move
        new_x_2 = new_x + self.DIRECTION[direction][0]
        new_y_2 = new_y + self.DIRECTION[direction][1]
        if self.is_within_board(new_x_2, new_y_2) and \
                self.is_empty(new_x_2, new_y_2) and \
                self.get(new_x, new_y) in self.PLAYER_PIECES:
            return MoveType.JUMP

        # not a valid move, so can't move
        return MoveType.INVALID

    def get_available_moves(self, x, y):
        """
        Returns a list of available moves that are valid 
        for the piece at (x, y) as a nested tuple in the form
        ((from), (to)) because we need to print moves from and to 
        """

        # return no moves available if piece is not playable
        if not (self.get(x, y) in self.PLAYER_PIECES):
            return []

        possible_moves = []
        for direction in range(0, 4):
            result = self._get_move_type(x, y, direction)

            # check if move is valid
            if result != MoveType.INVALID:
                # make normal move
                if result == MoveType.NORMAL:
                    new_x = x + self.DIRECTION[direction][0]
                    new_y = y + self.DIRECTION[direction][1]

                # make jump move
                elif result == MoveType.JUMP:
                    new_x = x + self.DIRECTION[direction][0] * 2
                    new_y = y + self.DIRECTION[direction][1] * 2

                possible_moves.append(((x, y), (new_x, new_y)))

        return possible_moves

    def get_empty_cells(self):
        """
        """
        self._apply_unapplied_actions()
        return list(self.all_pieces[self.PIECE_EMPTY])

    def get_hash_value(self):
        """
        Computes a hash value for entire board.
        """
        if self.hash_value_cache != None:
            return self.hash_value_cache
        self._apply_unapplied_actions()
        joined = b''
        for arr in self.board:
            joined = joined+arr.tobytes()
        self.hash_value_cache = hash(joined)
        return hash(joined)

    def is_won(self, our_piece, is_placing=False):
        """
        Check if all opponent pieces are eliminated,
        and we still have pieces left
        """
        opponent_piece = self._get_opponent_colour(our_piece)
        has_our_piece = False
        for x in range(self._min_xy, self._max_xy+1):
            for y in range(self._min_xy, self._max_xy+1):
                if self.get(x, y) == opponent_piece:
                    return False

                if self.get(x, y) == our_piece:
                    has_our_piece = True
        return has_our_piece

    def get_status(self, is_placing=False):
        # placing phase: it is okay to have no piece, game is not ended yet because we can place more.
        if (is_placing):
            return BoardStatus.ON_GOING
        if (self.is_won(self.PIECE_BLACK)):
            return BoardStatus.BLACK_WON
        elif (self.is_won(self.PIECE_WHITE)):
            return BoardStatus.WHITE_WON
        else:
            for x in range(self._min_xy, self._max_xy+1):
                for y in range(self._min_xy, self._max_xy+1):
                    if self.get(x, y) in [self.PIECE_BLACK, self.PIECE_WHITE]:
                        return BoardStatus.ON_GOING
            return BoardStatus.TIE
            # TODO: LOW-PERF

    def _get_opponent_colour(self, our_colour):
        """
        Returns the opponent piece type/colour
        """
        if (our_colour == self.PIECE_WHITE):
            return self.PIECE_BLACK
        else:
            return self.PIECE_WHITE

    def _check_elimination(self, x, y, our_piece):
        """
        Check and perform elimination, typically called after a player action.

        WARNING: to prevent reentrant, _check_elimination should only be called
        in _do_make_move and _do_place_piece
        """

        opponent_piece = self._get_opponent_colour(our_piece)
        DIRECTION = self.DIRECTION

        # step 1: check if we eliminated any opponent pieces
        for direction in range(0, 4):
            adj_piece_x = x + DIRECTION[direction][0]
            adj_piece_y = y + DIRECTION[direction][1]
            adj_piece_x_2 = adj_piece_x + DIRECTION[direction][0]
            adj_piece_y_2 = adj_piece_y + DIRECTION[direction][1]

            # if adjacent piece is within the board and is the opponent and
            # the piece across is within board and is an ally or a corner
            # then we remove the eliminated piece
            if self.is_within_board(adj_piece_x, adj_piece_y) and \
                    self.raw_get(adj_piece_x, adj_piece_y) == opponent_piece and \
                    self.is_within_board(adj_piece_x_2, adj_piece_y_2) and \
                    self.raw_get(adj_piece_x_2, adj_piece_y_2) in \
                    set([our_piece, self.PIECE_CORNER]):

                self.set_p(adj_piece_x, adj_piece_y, self.PIECE_EMPTY)

        # step 2: check if any opponent pieces eliminated us

        opponent_piece_or_corner = set([opponent_piece, self.PIECE_CORNER])
        # case 1: left and right surround us
        if (self.is_within_board(x - 1, y) and
            self.raw_get(x - 1, y) in opponent_piece_or_corner) and \
            (self.is_within_board(x + 1, y) and
             self.raw_get(x + 1, y) in opponent_piece_or_corner):
            self.set_p(x, y, self.PIECE_EMPTY)

        # case 2: above and below surround us
        if (self.is_within_board(x, y - 1) and
            self.raw_get(x, y - 1) in opponent_piece_or_corner) and \
            (self.is_within_board(x, y + 1) and
             self.raw_get(x, y + 1) in opponent_piece_or_corner):
            self.set_p(x, y, self.PIECE_EMPTY)

    def make_move(self, x, y, new_x, new_y, our_piece):
        """
        Make the piece move (valid move) to new location
        and check for elimination.

        Returns a new instance of `Board`.
        """
        board = LazyBoard(self)
        board.unapplied_actions.append(
            ('make_move', (x, y, new_x, new_y, our_piece))
        )
        return board

    def _do_make_move(self, x, y, new_x, new_y, our_piece):
        if (self._reentrant_counter_do_make_move > 0):
            raise Exception("Reentrant: _do_make_move")
        self._reentrant_counter_do_make_move+=1
        self.set_p(new_x, new_y, our_piece)
        self.set_p(x, y, self.PIECE_EMPTY)

        self._check_elimination(new_x, new_y, our_piece)
        self._reentrant_counter_do_make_move-=1
        

    def place_piece(self, new_x, new_y, our_piece):
        """
        Places a new piece. And check for elimination.

        Returns a new instance of `Board`.

        Lazy action: we don't actually modify the board.
        """

        board = LazyBoard(self)
        board.unapplied_actions.append(
            ('place_piece', (new_x, new_y, our_piece))
        )

        return board

    def _do_place_piece(self, new_x, new_y, colour):
        """
        Realisation of lazy action.
        """
        if (self._reentrant_counter_do_place_piece > 0):
            raise Exception("Reentrant: _do_place_piece")
        self._reentrant_counter_do_place_piece+=1
        self.set_p(new_x, new_y, colour)
        self._check_elimination(new_x, new_y, colour)
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
                return self.make_move(a, b, c, d, colour)
            else:
                # place piece
                return self.place_piece(x, y, colour)

    def shrink(self):
        """
        Shrinks the board. (`board_size -= 2`)

        Returns a new `Board` instance.
        """
        if (self.board_size <= 4):
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

        board.board_size -= 2
        board._update_borders()
        board._update_corners()

        # do the elimination caused by new corners

        for (x, y) in board._corner_cells():
            for direction in self.DIRECTION:
                adj_x = x + direction[0]
                adj_y = y + direction[1]
                adj_x_2 = adj_x + direction[0]
                adj_y_2 = adj_y + direction[1]

                if (board.is_within_board(adj_x, adj_y) and
                    board.get(adj_x, adj_y) in [self.PIECE_BLACK, self.PIECE_WHITE] and
                    board.is_within_board(adj_x_2, adj_y_2) and
                        board.get(adj_x_2, adj_y_2) in [self.PIECE_BLACK, self.PIECE_WHITE]):
                    if (board.get(adj_x, adj_y) != board.get(adj_x_2, adj_y_2)):
                        board.set_p(adj_x, adj_y, self.PIECE_EMPTY)

        return board

    def get_all_pieces(self, our_piece):
        """
        get all the location of pieces of a specific colour
        """
        self._apply_unapplied_actions()
        #print("get_all_pieces called", our_piece, self.all_pieces[our_piece])
        return list(self.all_pieces[our_piece])

    def count_moves(self, our_piece):
        result = 0
        pieces = self.get_all_pieces(our_piece)
        for p in pieces:
            (x, y) = p
            available_moves = self.get_available_moves(x, y)
            result = result + len(available_moves)
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
            board.board_size -= 2
            if board.get(1, 1) == cls.PIECE_INVALID:
                board.board_size -= 2

        return board
