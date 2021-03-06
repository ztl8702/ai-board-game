from .playerbase import PlayerBase
from ..algos.minimax import MiniMaxSolver


class MinimaxPlayer(PlayerBase):
    """Our minimax agent with alpha-beta pruning
    """

    def __init__(self, colour):
        super().__init__(colour)
        self.solver = MiniMaxSolver(self.colour)

    def on_opponent_action(self, action):
        # For this agent
        # We aren't going to do anything about opponent's action
        print("Player "+ self.colour, ": Oh opponent did", action, ", good to know.") #DEBUG


    def on_request_action(self, is_moving, turn, board):
        # board.print_board() #DEBUG
        if (is_moving):
            bestMove = self.solver.minimax(board, turn + 24)
        else:
            bestMove = self.solver.minimax(board, turn)
        return bestMove