from . import Board
from typing import Type
from .config import TURNS_BEFORE_SHRINK

def get_successor_board_states(board, turn_to_play, side='@')-> Type[Board]:
        if (turn_to_play <= 24):
            # placing phase
            if side == Board.PIECE_BLACK:
                valid_zone = range(2, 8)
            else:
                valid_zone = range(0, 6)
            moves = [(x, y)
                     for (x, y) in board.get_empty_cells() if y in valid_zone]

            new_states = [((x, y), board.place_piece(x, y, side))
                         for (x, y) in moves]
        else:
            # Moving phase
            our_pieces = board.get_all_pieces(side)
            #print(our_pieces)
            #if (len(our_pieces)==0):
            #    print("no pieces")
            #    board.print_board()
            #    print(board.all_pieces)
            #    print(board.all_pieces['O'])
            #    print(board.all_pieces['@'])
            #    print(board.all_pieces[side],'side',side, side=='O', side=='@')
            #    print(list(board.all_pieces[side]))
            moves = []
            for (x, y) in our_pieces:
                moves += board.get_available_moves(x, y)

            if turn_to_play in TURNS_BEFORE_SHRINK:
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


def get_opponent_colour(our_colour):
    '''
    Returns the opponent piece type/colour
    '''
    if (our_colour == Board.PIECE_WHITE):
        return Board.PIECE_BLACK
    else:
        return Board.PIECE_WHITE