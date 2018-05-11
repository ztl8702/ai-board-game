from .game_state_helpers import get_opponent_colour
from . import Board

def test_opponent_colour():
    assert(get_opponent_colour(Board.PIECE_BLACK) == Board.PIECE_WHITE)
    assert(get_opponent_colour(Board.PIECE_WHITE) == Board.PIECE_BLACK)