import copy
from common import Board

# search for winning solution
# return True if found
def DFS(board, ourPiece, depth):
        
    def printMoves():
        # print all the moves made
        for move in moves:
            print(move[0], '->', move[1])

    if depth == 0:
        return False
    if board.isWon(ourPiece):
        printMoves()
        return True

    ourPieces = board.getAllPieces(ourPiece)

    for p in ourPieces:
        (x, y) = p
        availableMoves = board.getAvailableMoves(x, y)

        for move in availableMoves:
            (newX, newY) = move[1]
            newBoardState = board.makeMove(x, y, newX, newY, ourPiece)
            newBoardHash = newBoardState.getHashValue()
            
            # check if the current state is in previous states
            if (newBoardHash not in hashedBoardStates) or \
            (hashedBoardStates[newBoardHash] < depth):
                # also consider fewer steps to reach the same state
                hashedBoardStates[newBoardHash] = depth
                moves.append(move)

                isFound = DFS(newBoardState, ourPiece, depth - 1)

                # backtrack
                moves.pop()
                if (isFound):
                    return True
    return False


oboard = Board()

oboard.readInput()
command = input().strip()

if command == "Moves":
    print(oboard.countMoves(Board.PIECE_WHITE))
    print(oboard.countMoves(Board.PIECE_BLACK))
else:
    for i in range(1, 1000):
        # print("Trying depth ", i) # DEBUG
        moves = []        
        hashedBoardStates = {}
        if (DFS(oboard, Board.PIECE_WHITE, i)):
            break


