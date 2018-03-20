import copy
from common import Board

hashedBoardStates = {}

def BFS(board):

    # store all nodes to visit in a queue
    queue = [board]
    hashedBoardStates[board.getHashValue()] = True

    while queue:
        node = queue.pop(0)
        # iterate through all pieces on board 
        # and store board states at the back of queue
        whitePieces = currentBoard.getAllPieces(Board.PIECE_WHITE)

        for p in whitePieces:
            (i, j) = p
        availableMoves = currentBoard.getAvailableMoves(i,j)
        for move in availableMoves:
            (newI, newJ) = move[1]
            neighbour = currentBoard.makeMove(i,j, newI, newJ)
            newBoardHash = hashBoard(neighbour)

            # check if the current board state was seen before
            if (newBoardHash not in hashedBoardStates) or (hashedBoardStates[newBoardHash] == False):
                hashedBoardStates[newBoardHash] = True
                moves.append(move)
                queue.append(neighbour)

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