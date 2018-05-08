from ..common import Board


TURNS_BEFORE_SHRINK = [128, 192]

class PlayerBase(object):
    """Base class for `Player`. Implements commmon functionalities like 
    keeping track of the board state for the different AI agents."""


    def __init__(self, colour):
        self.colour = Board.PIECE_BLACK if colour == 'black' else Board.PIECE_WHITE
        self.board = Board()
        self.currentTurn = 0
        self.movingPhase = False
        pass
    
    def _increment_turns(self):
        self.currentTurn += 1
        if (self.movingPhase == False and self.currentTurn > 24):
            self.currentTurn = 1
            self.movingPhase = True 

    def action(self, turns):
        """Called by `referee`
        """
        self._increment_turns()
        assert turns + 1 == self.currentTurn
        print("[PlayerBase]", "Requesting action for", self.colour, "player on turn", self.currentTurn)
        playerAction = self.on_request_action(self.movingPhase, self.currentTurn, self.board)
        print("[PlayerBase] decision is:", playerAction)

        # now apply the action
        self.board = self.board.apply_action(playerAction, self.colour)
        if (self.currentTurn in TURNS_BEFORE_SHRINK):
            self.board = self.board.shrink()
        
        return playerAction

    def update(self, action):
        """Called by `referee` when the opponent made a move
        """
        self._increment_turns()
        self.board = self.board.apply_action(action, 
            self.board._get_opponent_colour(self.colour))
        if (self.currentTurn in TURNS_BEFORE_SHRINK):
            self.board = self.board.shrink()

        # notify the subclass
        self.on_opponent_action(action)


    def on_opponent_action(self, action):
        pass

    def on_request_action(self, movingPhase, turn, board):
        raise NotImplementedError("on_request_action is not implemented")
