from common import Board


def p(*args):
    """Test Helper function"""
    assert len(args) == 8
    return "\\\\".join(args)


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

def test_min_max():
    """
    """

    board = Board()

    assert board._min_xy() == 0

    assert board._max_xy() == 7

    # todo: after shrink


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
    

def test_place_piece():
    pass

def test_move_piece():
    pass
