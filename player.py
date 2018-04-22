import copy
from common import Board
from parta import BFS
from parta_dfs import DFS
from faster_bfs import faster_BFS
from faster_dfs import faster_DFS

# test

PLACING_PHASE
MOVING_PHASE
SHRINK_ONE
SHRINK_TWO
SHRINK_THREE

class Player:
	def __init__(self, colour):
		board = Board()
		myColour = colour
		turn = 0


	def action(self, turns):
		search.bestMove() == 

		if ():
			# place a piece
			return (x, y)
		elif():
			# moving a piece
			return ((a, b), (c, d))
		else:
			# forfeit a turn
			return None


	def update(self, action):
		board.makeMove()
		def makeMove(self, x, y, newX, newY, ourPiece)



def parseAction(action):
	if action is None:
		# forfeit turn
		return None
	else:
		(x, y) = action
		if (isinstance(x, tuple) and isinstance(y, tuple)):
			(a, b) = x
			(c, d) = y

			# move piece
			return ((a, b), (c, d))
		else:
			# place piece
			return (x, y)
		




