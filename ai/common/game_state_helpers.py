from . import Board, BoardStatus
from typing import Type
from .config import TURNS_BEFORE_SHRINK


def get_successor_board_states(board, turnToPlay, side='@')-> Type[Board]:
    if (turnToPlay <= 24):
        # placing phase
        if side == Board.PIECE_BLACK:
            validYZone = range(2, 8)
        else:
            validYZone = range(0, 6)
        moves = [(x, y)
                 for (x, y) in board.get_empty_cells() if y in validYZone]

        newStates = [((x, y), board.place_piece(x, y, side))
                     for (x, y) in moves]
    else:
        # Moving phase
        ourPieces = board.get_all_pieces(side)
        moves = []
        for (x, y) in ourPieces:
            moves += board.get_available_moves(x, y)

        if turnToPlay in TURNS_BEFORE_SHRINK:
            newStates = [
                (((fromX, fromY), (toX, toY)),
                 board.make_move(fromX, fromY, toX, toY, side).shrink()
                 )
                for ((fromX, fromY), (toX, toY)) in moves
            ]
        else:
            newStates = [
                (((fromX, fromY), (toX, toY)),
                 board.make_move(fromX, fromY, toX, toY, side)
                 )
                for ((fromX, fromY), (toX, toY)) in moves
            ]

    return newStates


opponents_mapping = {'@': 'O', 'O': '@'}


def get_opponent_colour(our_colour):
    '''
    Returns the opponent piece type/colour
    '''
    # using dict is about 10% faster than if-else statement
    return opponents_mapping[our_colour]


def fake_status(board):
    """
    Returns a fake "Game Status" (i.e. who won? is it a tie?)
    based on the number of pieces left.
    """
    whitePieces = board.get_all_pieces(Board.PIECE_WHITE)
    blackPieces = board.get_all_pieces(Board.PIECE_BLACK)
    if (len(whitePieces) > len(blackPieces)):
        return BoardStatus.WHITE_WON
    elif (len(blackPieces) > len(whitePieces)):
        return BoardStatus.BLACK_WON
    else:
        return BoardStatus.TIE
