## RULES
#  "O" is white
# "@" is black
# "X" is corner
# "-" is empty
import copy
from common import Board

hashedBoardStates = {}


# search for winning solution
# return True if found
def DFS(currentBoard, depth):
        
    def printMoves():
        '''
        '''
        for move in moves:
            print(move[0], '->', move[1])

    if depth == 0:
        return False
    if currentBoard.isWon(Board.PIECE_WHITE):
        printMoves()
        return True

    whitePieces = currentBoard.getAllPieces(Board.PIECE_WHITE)

    for p in whitePieces:
        (i, j) = p
        availableMoves = currentBoard.getAvailableMoves(i,j)
        for move in availableMoves:
            (newI, newJ) = move[1]
            newBoardState = currentBoard.makeMove(i,j, newI, newJ, Board.PIECE_WHITE)
            newBoardHash = newBoardState.getHashValue()

            # @TODO Explain the second condition (in case we reset previous states to False)
            # check if the current state is in previous states
            if (newBoardHash not in hashedBoardStates) or (hashedBoardStates[newBoardHash] < depth):
                # also consider fewer steps to reach the same state
                hashedBoardStates[newBoardHash] = depth
                moves.append(move)

                isFound = DFS(newBoardState, depth-1)

                # backtrack
                moves.pop()
                if (isFound):
                    return True
    return False


moves = []
oboard = Board()

oboard.readInput()
command = input().strip()

if command == "Moves":
    print(oboard.countMoves(Board.PIECE_WHITE))
    print(oboard.countMoves(Board.PIECE_BLACK))
else:
    for i in range(1, 1000):
        print("Trying depth ", i)
        hashedBoardStates = {}
        if (DFS(oboard,i)):
            break


