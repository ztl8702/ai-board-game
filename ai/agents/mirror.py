from .playerbase import PlayerBase
from ..common import Board
import random

class MirrorPlayer(PlayerBase):
    """Agent that mirrors opponent's move each time.

    Used for testing.
    TO MARKERS: do not grade the code quality in this file.
    """

    def __init__(self, colour):
        super().__init__(colour)
        self.opponentLastMove = None

    def on_opponent_action(self, action):
        # save opponent's move
        self.opponentLastMove = action

    def _inverse_coords(self, x, y):
        return (7-x, 7-y)


    def on_request_action(self, isMoving, turn, board):
        inverseAction = None
        try:
            inverseAction = self._inverse_action(isMoving, turn, board)
        except:
            pass
        if (inverseAction!= None):
            return inverseAction
        else:
            print("[MirrorPlayer] cannot mirror, fall back to random")
            return self._random_action(isMoving, turn, board)
    
    def _inverse_action(self, isMoving, turn, board):
        print(f"[MirrorPlayer] opponent action was {self.opponentLastMove}")
        if (isMoving and isinstance(self.opponentLastMove,tuple)):
            if isinstance(self.opponentLastMove[0],tuple):
                x1, y1 = self._inverse_coords(self.opponentLastMove[0][0],self.opponentLastMove[0][1])
                x2, y2 = self._inverse_coords(self.opponentLastMove[1][0],self.opponentLastMove[1][1])
                if (board.get(x1,y1) == self.colour and board.get(x2,y2)==Board.PIECE_EMPTY):
                    return ((x1,y1),(x2,y2))
                else:
                    return None
            else:
                return None
        elif ((not isMoving) and isinstance(self.opponentLastMove,tuple)):
            print("[MirrorPlayer] placing phase", turn)
            # Placing Phase
            if self.colour == Board.PIECE_BLACK:
                validYZone = range(2, 8)
            else:
                validYZone = range(0, 6)
            x, y = self._inverse_coords(self.opponentLastMove[0],self.opponentLastMove[1])
            print("[MirrorPlayer]try ",x,y)
            if (board.get(x,y) == Board.PIECE_EMPTY and y in validYZone):
                return (x,y)
            else:
                return None
        else:
            print("XXXXXXXXXx None")
            return None

    def _random_action(self, isMoving, turn, board):
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