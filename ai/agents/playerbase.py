from ..common import Board


TURNS_BEFORE_SHRINK = [128, 192]

class PlayerBase(object):
    """Base class for `Player`. Implements commmon functionalities like 
    keeping track of the board state for the different AI agents."""


    def __init__(self, colour):
        self.colour = Board.PIECE_BLACK if colour == 'black' else Board.PIECE_WHITE
        self.board = Board()
        self.current_turn = 0
        self.moving_phase = False
        pass
    
    def _increment_turns(self):
        self.current_turn += 1
        if (self.moving_phase == False and self.current_turn > 24):
            self.current_turn = 1
            self.moving_phase = True 

    def action(self, turns):
        """Called by `referee`
        """
        self._increment_turns()
        assert turns + 1 == self.current_turn
        print("[PlayerBase]", "Requesting action for", self.colour, "player on turn", self.current_turn)
        player_action = self.on_request_action(self.moving_phase, self.current_turn, self.board)
        print("[PlayerBase] decision is:", player_action)

        # now apply the action
        self.board = self.board.apply_action(player_action, self.colour)
        if (self.current_turn in TURNS_BEFORE_SHRINK):
            self.board = self.board.shrink()
        
        return player_action

    def update(self, action):
        """Called by `referee` when the opponent made a move
        """
        self._increment_turns()
        self.board = self.board.apply_action(action, 
            self.board._get_opponent_colour(self.colour))
        if (self.current_turn in TURNS_BEFORE_SHRINK):
            self.board = self.board.shrink()

        # notify the subclass
        self.on_opponent_action(action)


    def on_opponent_action(self, action):
        pass

    def on_request_action(self, moving_phase, turn, board):
        raise NotImplementedError("on_request_action is not implemented")
