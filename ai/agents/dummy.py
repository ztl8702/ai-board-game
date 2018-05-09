from .playerbase import PlayerBase
from ..common import Board
import random

class DummyPlayer(PlayerBase):
    """Dummy agent picks a random move each time.

    Used as the baseline.
    """

    def __init__(self, colour):
        super().__init__(colour)

    def on_opponent_action(self, action):
        pass
    
    def on_request_action(self, isMoving, turn, board):
        if (not isMoving):
            if self.colour == Board.PIECE_BLACK:
                validYZone = range(2, 8)
            else:
                validYZone = range(0, 6)
            moves = [(x, y)
                     for (x, y) in board.get_empty_cells() if y in validYZone]

            if (not moves):
                return None
            
            return random.choice(moves)
        else:
            ourPieces = board.get_all_pieces(self.colour)
            moves = []
            for (x, y) in ourPieces:
                moves += board.getAvailableMoves(x, y)

            if (not moves):
                return None
            return random.choice(moves)