from .playerbase import PlayerBase
from ..common import Board

import random
from typing import Type, Union, Tuple
import math

from ..algos.mc import solver


class MCPlayer(PlayerBase):
    """Monto Carlo Player

    """

    def __init__(self, colour):
        super().__init__(colour)

    def on_opponent_action(self, action):
        pass

    def on_request_action(self, isMoving, turn, board):
        if (isMoving):
            return solver.find_next_move(board, turn+24, self.colour)
        else:
            return solver.find_next_move(board, turn, self.colour)
