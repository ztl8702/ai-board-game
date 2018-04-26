import copy
from common import Board
from minimax import MiniMaxSolver

class Player:
	def __init__(self, colour):
		self.board = Board()
		self.colour = Board.PIECE_BLACK if colour=='black' else Board.PIECE_WHITE
		self.lastTurn = 0
		self.moving = False
		self.solver = MiniMaxSolver(self.colour)


	def action(self, turns):
		if (turns < self.lastTurn and not self.moving):
			self.moving = True
			self.solver.MAX_DEPTH += 2
		
		if (self.moving):
			bestMove = self.solver.minimax(self.board, turns+1+24)
		else:
			bestMove = self.solver.minimax(self.board, turns+1)
			self.lastTurn = turns
		self.board = self.board.apply_action(bestMove, self.colour)
		print('bestmove', bestMove)
		return bestMove
		"""
		if ():
			# place a piece
			return (x, y)
		elif():
			# moving a piece
			return ((a, b), (c, d))
		else:
			# forfeit a turn
			return None
"""

	def update(self, action):
		"""Opponent made a move
		"""
		self.board = self.board.apply_action(action, self.board._get_opponent_colour(self.colour))






