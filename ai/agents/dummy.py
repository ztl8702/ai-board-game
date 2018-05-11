from .playerbase import PlayerBase
from ..common import Board
import random

class DummyPlayer(PlayerBase):
    """Dummy agent picks a random move each time.
    Used as the baseline and for testing.
    TO MARKERS: do not grade the code quality in this file.
    """

    def __init__(self, colour):
        super().__init__(colour)

    def on_opponent_action(self, action):
        pass
    
    def on_request_action(self, is_moving, turn, board):
        if (not is_moving):
            if self.colour == Board.PIECE_BLACK:
                valid_zone = range(2, 8)
            else:
                valid_zone = range(0, 6)
            moves = [(x, y)
                     for (x, y) in board.get_empty_cells() if y in valid_zone]

            if (not moves):
                return None
            
            return random.choice(moves)
        else:
            our_pieces = board.get_all_pieces(self.colour)
            moves = []
            for (x, y) in our_pieces:
                moves += board.get_available_moves(x, y)

            if (not moves):
                return None
            return random.choice(moves)