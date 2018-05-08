from . import Board
from .helpers import p

"""
Unit tests for common.py
"""

def test_board_parsing():
    """Ensures `to_token_string` and `from_token_string` works properly. Basis for other unit tests.
    """
    board = Board()

    board.set_p(5, 4, Board.PIECE_BLACK)

    assert(p("X------X",
             "--------",
             "--------",
             "--------",
             "-----@--",
             "--------",
             "--------",
             "X------X") == board.to_token_string())

    layout1 = p("X------X",
                "--------",
                "-----O--",
                "----@O--",
                "------O-",
                "-----O@-",
                "-------@",
                "X------X")
    board1 = Board.from_token_string(layout1)
    assert(board1.to_token_string() == layout1)

    layout2 = p("########",
                "########",
                "##X-OX##",
                "##-O@-##",
                "##@O--##",
                "##XO-X##",
                "########",
                "########")
    board2 = Board.from_token_string(layout2)
    assert board2.boardSize == 4


def test_min_max():
    """
    """

    board = Board()

    assert board._min_xy == 0
    assert board._max_xy == 7

    board2 = board.shrink()

    # old one should not have changed
    assert board._min_xy == 0
    assert board._max_xy == 7
    # new one should change
    assert board2._min_xy == 1
    assert board2._max_xy == 6

    board3 = board2.shrink()

    # old one should not have changed
    assert board2._min_xy == 1
    assert board2._max_xy == 6
    # new one should change
    assert board3._min_xy == 2
    assert board3._max_xy == 5
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

    board1 = Board.from_token_string(layout1)
    board2 = board1.shrink()

    assert(board2.boardSize == 6)
    assert(board2.isWithinBoard(0, 0) == False)

    assert (p("########",
              "#X-@--X#",
              "#------#",
              "#-O----#",
              "#----@O#",
              "#------#",
              "#X----X#",
              "########") == board2.to_token_string())

    board3 = board2.shrink()
    assert(board3.boardSize == 4)
    assert(board3.isWithinBoard(1, 1) == False)
    assert(board3.get(1, 1) == Board.PIECE_INVALID)

    assert (p("########",
              "########",
              "##X--X##",
              "##O---##",
              "##---@##",
              "##X--X##",
              "########",
              "########") == board3.to_token_string())


def test_get_empty_cells():
    layout = p("X------X",
               "--------",
               "--------",
               "--------",
               "--------",
               "--------",
               "--------",
               "X------X")
    assert len(Board.from_token_string(layout).get_empty_cells()) == 60


def test_is_won():
    layout = p("X------X",
               "--------",
               "--------",
               "--------",
               "---@----",
               "--------",
               "--------",
               "X------X")
    board = Board.from_token_string(layout)
    assert board.isWon(Board.PIECE_BLACK) == True
    assert board.isWon(Board.PIECE_WHITE) == False

    layout = p("X------X",
               "--------",
               "--------",
               "--------",
               "--------",
               "--------",
               "--------",
               "X------X")
    board = Board.from_token_string(layout)
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
    board = Board.from_token_string(layout)
    assert(board.isWon(Board.PIECE_BLACK) == False)
    assert(board.isWon(Board.PIECE_WHITE) == False)


def test_get_all_pieces_should_find_pieces_after_shrink():
    # This was a bug
    # This testcase is for preventing regression

    layout1 = p("########",
                "#XO---X#",
                "#---O--#",
                "#O----@#",
                "#-----O#",
                "#------#",
                "#X----X#",
                "########")
    board1 = Board.from_token_string(layout1)
    allBlackPieces = board1.get_all_pieces('@')

    assert(len(allBlackPieces) == 1)
    assert((6, 3) in allBlackPieces)


def test_place_piece():
    layout1 = p("X------X",
                "--------",
                "--------",
                "--------",
                "--------",
                "--------",
                "--------",
                "X------X")
    board1 = Board.from_token_string(layout1)
    boardAfter = board1.placePiece(5, 2, 'O')
    layout2 = p("X------X",
                "--------",
                "-----O--",
                "--------",
                "--------",
                "--------",
                "--------",
                "X------X")
    assert(boardAfter.to_token_string() == layout2)


def test_place_piece_and_eliminate():
    layout1 = p("X-----OX",
                "--------",
                "--------",
                "--------",
                "--------",
                "--------",
                "--------",
                "X------X")
    board1 = Board.from_token_string(layout1)
    boardAfter = board1.placePiece(5, 0, '@')
    layout2 = p("X----@-X",
                "--------",
                "--------",
                "--------",
                "--------",
                "--------",
                "--------",
                "X------X")
    assert(boardAfter.to_token_string() == layout2)


def test_move_piece():
    layout1 = p("X------X",
                "--------",
                "--------",
                "--------",
                "---@----",
                "--------",
                "--------",
                "X------X")
    board1 = Board.from_token_string(layout1)
    boardAfter = board1.makeMove(3, 4, 4, 4, '@')
    layout2 = p("X------X",
                "--------",
                "--------",
                "--------",
                "----@---",
                "--------",
                "--------",
                "X------X")
    assert(boardAfter.to_token_string() == layout2)


def test_move_piece_and_eliminate():
    layout1 = p("########",
                "#XO---X#",
                "#----O-#",
                "#O----@#",
                "#-----O#",
                "#------#",
                "#X----X#",
                "########")
    board1 = Board.from_token_string(layout1)
    boardAfter = board1.makeMove(5, 2, 6, 2, 'O')
    layout2 = p("########",
                "#XO---X#",
                "#-----O#",
                "#O-----#",
                "#-----O#",
                "#------#",
                "#X----X#",
                "########")
    assert(boardAfter.to_token_string() == layout2)
