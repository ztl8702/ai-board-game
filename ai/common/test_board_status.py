from .helpers import p
from .board import Board
from .board_status import BoardStatus

def test_board_state_black_won():
    layout1 = p("X------X",
                "--------",
                "--------",
                "----@---",
                "--------",
                "------@-",
                "-------@",
                "X------X")
    board1 = Board.from_token_string(layout1)
    assert(board1.get_status() == BoardStatus.BLACK_WON)


def test_board_state_white_won():
    layout1 = p("X------X",
                "--------",
                "--------",
                "----O---",
                "--------",
                "--------",
                "--------",
                "X------X")
    board1 = Board.from_token_string(layout1)
    assert(board1.get_status() == BoardStatus.WHITE_WON)
    assert(board1.get_status(is_placing=True) == BoardStatus.ON_GOING)

def test_board_state_on_going():
    layout1 = p("X------X",
                "--------",
                "--------",
                "----O---",
                "----@---",
                "--------",
                "--------",
                "X------X")
    board1 = Board.from_token_string(layout1)
    assert(board1.get_status() == BoardStatus.ON_GOING)



def test_board_state_tie():
    layout1 = p("X------X",
                "--------",
                "--------",
                "--------",
                "--------",
                "--------",
                "--------",
                "X------X")
    board1 = Board.from_token_string(layout1)
    assert(board1.get_status() == BoardStatus.TIE)
    assert(board1.get_status(is_placing=True) == BoardStatus.ON_GOING)
