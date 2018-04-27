from playerbase import PlayerBase
from minimax import MiniMaxSolver


class Player(PlayerBase):
    """Our naive minimax agent with alpha-beta pruning
    """

    def __init__(self, colour):
        super().__init__(colour)
        self.solver = MiniMaxSolver(self.colour)

    def on_opponent_action(self, action):
        # For this agent
        # We aren't going to do anything about opponent's action
        print("Player "+ self.colour, ": Oh opponent did", action, ", good to know.")

    def on_request_action(self, isMoving, turn, board):
        if (isMoving):
            bestMove = self.solver.minimax(board, turn + 24)
        else:
            bestMove = self.solver.minimax(board, turn)
        return bestMove