import random
from ..common import Board
from ..common import config


INFINITY = float('inf')

# Values representing different weightage
# based on location of board
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



class MiniMaxSolver:
    """
    Uses minimax algorithm to find best move with the help of heuristics
    """

    # choose random max_values for minimax when there are multiple
    MAKE_RANDOM = True


    def __init__(self, colour):
        self.colour = colour
        return

    def h(self, board, current_turn):
        """
        Utility function
        where all the heuristics are located
        """

        # heuristic 1
        # add up the values of each of our pieces based on its location on the board
        # based on our testing:
        # - only considering our pieces is optimal
        # - keeping the same PLACEMENT_VALUE throughout the game is optimal

        our_pieces = board.get_all_pieces(self.colour)
        ourTotal = 0
        
        for our in our_pieces:
            (x, y) = our
            ourTotal += PLACEMENT_VALUE[x][y]

        h1 = ourTotal

        return h1
    
    def get_max_depth(self, current_turn):
        # after first shrink, before second second shrink
        if (current_turn > config.TURNS_BEFORE_SHRINK[0] and 
            current_turn <= config.TURNS_BEFORE_SHRINK[1]):
            return 6
        # after second shrink
        elif (current_turn > config.TURNS_BEFORE_SHRINK[1]):
            return 8

        # max depth of 4 by default
        return 4

    def get_squares(self, board):
        """
        return array of coordinates containing squares
        squares are square formation in inner parts of the board
        """
        squares = []

        for i in range(2, 5): # y value
            for j in range(2, 5): # x value

                # only if square is formed
                if (board.get(j, i) == self.colour and \
                    board.get(j+1, i) == self.colour and \
                        board.get(j+1, i+1) == self.colour and \
                            board.get(j, i+1) == self.colour):
                    
                    squares.append(tuple((j, i)))
                    squares.append(tuple((j+1, i)))
                    squares.append(tuple((j+1, i+1)))
                    squares.append(tuple((j, i+1)))

        return squares

    def minimax(self, board, current_turn):
        # first, find the max value
        # should be root node of tree
        self.visited = {}
        (best_move, best_val) = self.max_value(board, current_turn, 1)
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

    def max_value(self, board, current_turn, depth, valid_range=(-INFINITY, INFINITY)):
        """Max represents our turn

        valid_range is used for alpha-beta pruning
        The boundaries are inclusive.
        """
        if ((current_turn, board.get_hash_value()) in self.visited):
            return self.visited[(current_turn, board.get_hash_value())]
        if self.is_terminal(board, depth, current_turn):
            return (None, self.h(board, current_turn))

        max_value = -INFINITY
        max_move = None

        successors_states = self.get_successors(board, current_turn, self.colour)
       # print(" "*(depth-1)+"max", "successor_states", len(successors_states))
        for (move, state) in successors_states:
            tmp = self.min_value(state, current_turn+1, depth+1,
                                 self._range_intersect((max_value, INFINITY), valid_range))[1]
            if (tmp > max_value):
                max_move = move
                max_value = tmp
                if (self._is_empty_set(self._range_intersect(valid_range, (max_value, INFINITY)))):
                    break
            elif (tmp == max_value and random.randrange(0,2) == 1 and self.MAKE_RANDOM): # occasionally uses another max_value
                max_move = move
                max_value = tmp
                if (self._is_empty_set(self._range_intersect(valid_range, (max_value, INFINITY)))):
                    break
        self.visited[(current_turn, board.get_hash_value())
                     ] = (max_move, max_value)
        return (max_move, max_value)

    def min_value(self, board, current_turn, depth, valid_range=(-INFINITY, INFINITY)):
        """Min represents opponent's turn
        """
        if ((current_turn, board.get_hash_value()) in self.visited):
            return self.visited[(current_turn, board.get_hash_value())]
        if self.is_terminal(board, depth, current_turn):
            return (None, self.h(board, current_turn))

        min_value = INFINITY
        min_move = None

        successors_states = self.get_successors(
            board, current_turn, board._get_opponent_colour(self.colour))
        #print(" "*(depth-1)+"min", "successor_states", len(successors_states))
        for (move, state) in successors_states:
            tmp = self.max_value(state, current_turn+1, depth+1,
                                 self._range_intersect((-INFINITY, min_value), valid_range))[1]
            if (tmp < min_value):
                min_move = move
                min_value = tmp
                if (self._is_empty_set(self._range_intersect(valid_range, (-INFINITY, min_value)))):
                    break
            elif (tmp == min_value and random.randrange(0,2) == 1 and self.MAKE_RANDOM): # occasionally uses another min_value
                min_move = move
                min_value = tmp
                if (self._is_empty_set(self._range_intersect(valid_range, (-INFINITY, min_value)))):
                    break
        self.visited[(current_turn, board.get_hash_value())
                     ] = (min_move, min_value)
        return (min_move, min_value)

    # successor states in a game tree are the child nodes...
    def get_successors(self, board, current_turn, side='@'):
        if (current_turn <= config.PLACING_PHASE): # Placing phase
            
            if side == Board.PIECE_BLACK:
                valid_range = range(2, 8)
            else:
                valid_range = range(0, 6)
            moves = [(x, y)
                     for (x, y) in board.get_empty_cells() if y in valid_range]

            new_states = [((x, y), board.place_piece(x, y, side))
                         for (x, y) in moves]
        
        else: # Moving phase

            # reduce the movement of pieces that form squares
            # as it is more advantagous to hold a square formation    
            our_pieces = board.get_all_pieces(side)
            
            squares = self.get_squares(board)
            moves = []
            for (x, y) in our_pieces:
                if ((x, y) not in squares):
                    moves += board.get_available_moves(x, y)

            # prevent forfeiting when still have moves but all form squares
            if (not moves and our_pieces):
                for (x, y) in our_pieces:
                    moves += board.get_available_moves(x, y)

            # finalise the new_states to run minimax on
            if current_turn in config.TURNS_BEFORE_SHRINK:
                new_states = [
                    (((from_x, from_y), (to_x, to_y)),
                     board.make_move(from_x, from_y, to_x, to_y, side).shrink()
                     )
                    for ((from_x, from_y), (to_x, to_y)) in moves
                ]
            else:
                new_states = [
                    (((from_x, from_y), (to_x, to_y)),
                     board.make_move(from_x, from_y, to_x, to_y, side)
                     )
                    for ((from_x, from_y), (to_x, to_y)) in moves
                ]

        return new_states

    def is_terminal(self, board, depth, current_turn):
        """Terminate if either side wins;
        or if we reached maximum search depth.
        """
        return ((depth >= self.get_max_depth(current_turn)) or
                (current_turn > config.PLACING_PHASE and
                 (board.is_won(Board.PIECE_BLACK) or board.is_won(Board.PIECE_WHITE))
                 ))
