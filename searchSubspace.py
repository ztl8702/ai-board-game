
def getInterestingCells(self, ourPiece):
	'''
	look at opponent pieces and mark cells around them as interesting 
	and return the smaller search space
	'''
	interestingCells = []
	opponentPiece = self.__getOpponentColour(ourPiece)
	opponentPieces = self.getAllPieces(opponentPiece)
	
	for p in opponentPieces:
		(x, y) = p
		# add coordinate of opponent @TOGGLE
		interestingCells.append((x,y))

		for direction in range(0, 4):
			newX = x + self.DIRECTION[direction][0]
            newY = y + self.DIRECTION[direction][1]
			
			# add cells around itself (layer 1)
			interestingCells.append(newX, newY)

			newX2 = newX + self.DIRECTION[direction][0]
            newY2 = newY + self.DIRECTION[direction][1]

            # add cells around itself (layer 2)
			interestingCells.append(newX2, newY2)

	return interestingCells


def searchInterestingSpace(self, ourPiece)
	board = copy.deepcopy(self)

	searchSpace = self.getInterestingCells(ourPiece)

	ourPieces = self.getAllPieces(ourPiece)

	for p in ourPieces:
		(x, y) = p
		for s in searchSpace:
			moves = self.getAvailableMoves(x, y)
			for m in moves:
				(newX, newY) = m[1]
				if m[1] in searchSpace:
					# perform sub search
					board = self.makeMove(x, y, newX, newY, ourPiece)


			



























