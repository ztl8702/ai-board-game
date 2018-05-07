from enum import Enum

class BoardStatus(Enum):
    BLACK_WON = '@'
    WHITE_WON = 'O'
    TIE = 3
    ON_GOING = 4