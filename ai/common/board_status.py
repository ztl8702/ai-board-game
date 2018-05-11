from enum import Enum

class BoardStatus(Enum):
    def __str__(self):
        return str(self.value)
    BLACK_WON = '@'
    WHITE_WON = 'O'
    TIE = 3
    ON_GOING = 4