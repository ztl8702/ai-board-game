from common import Board


def p(*args):
    """Test Helper function"""
    assert len(args) == 8
    return "\\\\".join(args)


def test_board_parsing():
    board = Board()

    board.set(5,4, Board.PIECE_BLACK)

    print(p("X------X",
      "--------",
      "--------",
      "--------",
      "-----@--",
      "--------",
      "--------",
      "X------X"))

    assert(p("X------X",
             "--------",
             "--------",
             "--------",
             "-----@--",
             "--------",
             "--------",
             "X------X") == board.toTokenString())

