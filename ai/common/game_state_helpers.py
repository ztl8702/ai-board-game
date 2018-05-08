from . import Board
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

            newStates = [((x, y), board.placePiece(x, y, side))
                         for (x, y) in moves]
        else:
            # Moving phase
            ourPieces = board.get_all_pieces(side)
            moves = []
            for (x, y) in ourPieces:
                moves += board.getAvailableMoves(x, y)

            if turnToPlay in TURNS_BEFORE_SHRINK:
                newStates = [
                    (((fromX, fromY), (toX, toY)),
                     board.makeMove(fromX, fromY, toX, toY, side).shrink()
                     )
                    for ((fromX, fromY), (toX, toY)) in moves
                ]
            else:
                newStates = [
                    (((fromX, fromY), (toX, toY)),
                     board.makeMove(fromX, fromY, toX, toY, side)
                     )
                    for ((fromX, fromY), (toX, toY)) in moves
                ]

        return newStates


def get_opponent_colour(ourColour):
    '''
    Returns the opponent piece type/colour
    '''
    if (ourColour == Board.PIECE_WHITE):
        return Board.PIECE_BLACK
    else:
        return Board.PIECE_WHITE