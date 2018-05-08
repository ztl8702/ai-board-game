from .Board import Board
from .helpers import p
"""
Unit tests for common.py
"""




def test_board_parsing():
    """Ensures `toTokenString` and `fromTokenString` works properly. Basis for other unit tests.
    """
    board = Board()

    board.set(5,4, Board.PIECE_BLACK)

    assert(p("X------X",
             "--------",
             "--------",
             "--------",
             "-----@--",
             "--------",
             "--------",
             "X------X") == board.toTokenString())

    layout1 = p("X------X",
                "--------",
                "-----O--",
                "----@O--",
                "------O-",
                "-----O@-",
                "-------@",
                "X------X")
    board1 = Board.fromTokenString(layout1)
    assert(board1.toTokenString() == layout1)

    layout2 = p("########",
               "########",
               "##X-OX##",
               "##-O@-##",
               "##@O--##",
               "##XO-X##",
               "########",
               "########")
    board2 = Board.fromTokenString(layout2)
    assert board2.boardSize == 4

def test_min_max():
    """
    """

    board = Board()

    assert board._min_xy() == 0
    assert board._max_xy() == 7

    board2 = board.shrink()

    # old one should not have changed
    assert board._min_xy() == 0
    assert board._max_xy() == 7
    # new one should change
    assert board2._min_xy() == 1
    assert board2._max_xy() == 6

    board3 = board2.shrink()

    # old one should not have changed
    assert board2._min_xy() == 1
    assert board2._max_xy() == 6
    # new one should change
    assert board3._min_xy() == 2
    assert board3._max_xy() == 5
    assert board3.boardSize == 4

def test_shrink_board():
    layout1 = p("X------X",
                "--O@----",
                "--------",
                "--O-----",
                "-----@O-",
                "@-----@-",
                "--------",
                "X------X") 

    board1 = Board.fromTokenString(layout1)
    board2 = board1.shrink()

    assert(board2.boardSize == 6)
    assert(board2.isWithinBoard(0,0) == False)

    assert (p("########",
              "#X-@--X#",
              "#------#",
              "#-O----#",
              "#----@O#",
              "#------#",
              "#X----X#",
              "########") == board2.toTokenString())
    
def test_get_empty_cells():
    layout =p("X------X",
             "--------",
             "--------",
             "--------",
             "--------",
             "--------",
             "--------",
             "X------X")
    assert len(Board.fromTokenString(layout).get_empty_cells()) == 60


def test_is_won():
    layout=p("X------X",
             "--------",
             "--------",
             "--------",
             "---@----",
             "--------",
             "--------",
             "X------X")
    board = Board.fromTokenString(layout)
    assert board.isWon(Board.PIECE_BLACK) == True
    assert board.isWon(Board.PIECE_WHITE) == False

    layout=p("X------X",
             "--------",
             "--------",
             "--------",
             "--------",
             "--------",
             "--------",
             "X------X")
    board = Board.fromTokenString(layout)
    assert board.isWon(Board.PIECE_BLACK) == False
    assert board.isWon(Board.PIECE_WHITE) == False


def test_is_won_on_shrinked_board():

    # This was a layout that caused a bug. 
    # This testcase is for preventing regression. 
    layout = p("########",
               "########",
               "##X-OX##",
               "##-O@-##",
               "##@O--##",
               "##XO-X##",
               "########",
               "########")
    board = Board.fromTokenString(layout)
    assert(board.isWon(Board.PIECE_BLACK) == False)
    assert(board.isWon(Board.PIECE_WHITE) == False)


def test_place_piece():
    pass

def test_move_piece():
    pass
