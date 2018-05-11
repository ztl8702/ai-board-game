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
    assert board2.board_size == 4


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
    assert board3.board_size == 4


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

    assert(board2.board_size == 6)
    assert(board2.is_within_board(0, 0) == False)

    assert (p("########",
              "#X-@--X#",
              "#------#",
              "#-O----#",
              "#----@O#",
              "#------#",
              "#X----X#",
              "########") == board2.to_token_string())

    board3 = board2.shrink()
    assert(board3.board_size == 4)
    assert(board3.is_within_board(1, 1) == False)
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


def test_get_available_moves():
    pass


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
    assert board.is_won(Board.PIECE_BLACK) == True
    assert board.is_won(Board.PIECE_WHITE) == False

    layout = p("X------X",
               "--------",
               "--------",
               "--------",
               "--------",
               "--------",
               "--------",
               "X------X")
    board = Board.from_token_string(layout)
    assert board.is_won(Board.PIECE_BLACK) == False
    assert board.is_won(Board.PIECE_WHITE) == False


def test_elimination_edge_cases():
    layout = p("X------X",
               "--------",
               "---@----",
               "--O-@O--",
               "---@----",
               "--------",
               "--------",
               "X------X")
    board = Board.from_token_string(layout)
    board = board.make_move(2, 3, 3, 3, 'O')

    assert p("X------X",
             "--------",
             "---@----",
             "-----O--",
             "---@----",
             "--------",
             "--------",
             "X------X") == board.to_token_string()


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
    assert(board.is_won(Board.PIECE_BLACK) == False)
    assert(board.is_won(Board.PIECE_WHITE) == False)


def test_get_all_pieces():
    layout1 = p("########",
                "#XO---X#",
                "#---O--#",
                "#O----@#",
                "#-----O#",
                "#------#",
                "#X----X#",
                "########")
    board1 = Board.from_token_string(layout1)
    allWhitePieces = board1.get_all_pieces('O')
    assert((2, 1) in allWhitePieces)
    assert((4, 2) in allWhitePieces)
    assert((1, 3) in allWhitePieces)
    assert((6, 4) in allWhitePieces)
    assert(len(allWhitePieces) == 4)

    board1.set_p(4, 5, 'O')
    allWhitePieces = board1.get_all_pieces('O')
    assert(len(allWhitePieces) == 5)
    assert((4, 5) in allWhitePieces)

    layout2 = p("X-----OX",
                "--------",
                "--@---@-",
                "O-@OO--O",
                "-@@---OO",
                "-O-OO--O",
                "@--@-@@-",
                "X------X"
                )
    board2 = Board.from_token_string(layout2)
    allWhitePieces = board2.get_all_pieces('O')
    allBlackPieces = board2.get_all_pieces('@')
    assert(len(allWhitePieces) == 11)
    assert(len(allBlackPieces) == 9)


def test_get_all_pieces_should_find_pieces_after_shrink():
    # This was a bug
    # This testcase is for preventing regression

    layout1 = p("X------X",
                "--O-----",
                "----O---",
                "-O----@-",
                "@-----O-",
                "--------",
                "-@----@-",
                "X------X")
    board1 = Board.from_token_string(layout1)
    allBlackPieces = board1.shrink().get_all_pieces('@')

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
    boardAfter = board1.place_piece(5, 2, 'O')
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
    boardAfter = board1.place_piece(5, 0, '@')
    layout2 = p("X----@-X",
                "--------",
                "--------",
                "--------",
                "--------",
                "--------",
                "--------",
                "X------X")
    assert(boardAfter.to_token_string() == layout2)


def test_hash_value():
    layout1 = p("X-----OX",
                "--------",
                "--------",
                "--------",
                "--------",
                "--------",
                "--------",
                "X------X")
    board1 = Board.from_token_string(layout1)
    hash1 = board1.get_hash_value()
    hash2 = board1.make_move(6, 0, 5, 0, 'O').get_hash_value()
    hash3 = board1.make_move(6, 0, 5, 0, 'O').make_move(
        5, 0, 6, 0, 'O').get_hash_value()
    assert(hash1 == hash3)
    assert(hash2 != hash3)

    board1.set_p(1, 1, '@')
    hash4 = board1.get_hash_value()
    assert(hash4 != hash3)


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
    boardAfter = board1.make_move(3, 4, 4, 4, '@')
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
    boardAfter = board1.make_move(5, 2, 6, 2, 'O')
    layout2 = p("########",
                "#XO---X#",
                "#-----O#",
                "#O-----#",
                "#-----O#",
                "#------#",
                "#X----X#",
                "########")
    assert(boardAfter.to_token_string() == layout2)


def test_multiple_moves():
    layout1 = p("########",
                "#XO---X#",
                "#----O-#",
                "#O----@#",
                "#-----O#",
                "#------#",
                "#X----X#",
                "########")
    board1 = Board.from_token_string(layout1)
    boardAfter = board1.make_move(5, 2, 6, 2, 'O') \
        .place_piece(4, 5, '@') \
        .place_piece(3, 5, 'O') \
        .place_piece(5, 5, 'O')
    layout2 = p("########",
                "#XO---X#",
                "#-----O#",
                "#O-----#",
                "#-----O#",
                "#--O-O-#",
                "#X----X#",
                "########")
    assert(boardAfter.to_token_string() == layout2)
    pass


def test_lazy_board():
    """
    Some edge classes for LazyBoard implementation
    """

    # regression
    layout = p("X------X",
               "--------",
               "--@O----",
               "--@--O--",
               "--@O-@--",
               "--OO@@--",
               "--------",
               "X------X")

    board = Board.from_token_string(layout)
    board.unapplied_actions.append(('place_piece', (4, 3, '@')))
    board.unapplied_actions.append(('place_piece', (3, 3, 'O')))
    board.has_unapplied_actions = True
    assert p("X------X",
             "--------",
             "--@O----",
             "--@O-O--",
             "--@O-@--",
             "--OO@@--",
             "--------",
             "X------X") == board.to_token_string()


def test_lazy_board_should_shrink_properly():
    layout1 = p("X------X",
                "--------",
                "--@-@---",
                "O-O-----",
                "--OO----",
                "--O--@--",
                "---O----",
                "X------X")
    board1 = Board.from_token_string(layout1)
    board1.unapplied_actions.append(('make_move', (0, 3, 1, 3, 'O')))
    board1.has_unapplied_actions = True

    board2 = board1.shrink()
    assert p("########",
             "#X----X#",
             "#-@-@--#",
             "#OO----#",
             "#-OO---#",
             "#-O--@-#",
             "#X-O--X#",
             "########") == board2.to_token_string()


def test_board_shrink_should_eliminate_in_anti_clockwise():
    """
    Order matters.
    """
    layout1 = p("########",
                "#X----X#",
                "#--O@--#",
                "#-OO@@-#",
                "#-OO@@-#",
                "#--O@--#",
                "#X----X#",
                "########")
    board1 = Board.from_token_string(layout1)

    board2 = board1.shrink()

    assert p("########",
             "########",
             "##X-@X##",
             "##OO@@##",
             "##OO@@##",
             "##X-@X##",
             "########",
             "########") == board2.to_token_string()

    layout2 = p("########",
                "#X----X#",
                "#-OOOO-#",
                "#-OOOO-#",
                "#-@@@@-#",
                "#-@@@@-#",
                "#X----X#",
                "########")
    board3 = Board.from_token_string(layout2)
    board4 = board3.shrink()
    assert p("########",
             "########",
             "##XOOX##",
             "##-OOO##",
             "##@@@-##",
             "##X@@X##",
             "########",
             "########") == board4.to_token_string()
