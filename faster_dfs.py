import copy

moves = []
# DFS called multiple times, so need to keep track globally
hashedBoardStates = {}

# search for winning solution
# return True if found
def faster_DFS(board, ourPiece, layers, depth):
        
    def printMoves():
        # print all the moves made
        for move in moves:
            print(move[0], '->', move[1])

    if depth == 0:
        return False
    if board.isWon(ourPiece):
        printMoves()
        return True

    #  get limited/interesting search space
    searchSpace = board.getSmallerSearchSpace(ourPiece, layers)

    ourPieces = board.getAllPieces(ourPiece)

    for p in ourPieces:
        (x, y) = p
        availableMoves = board.getAvailableMoves(x, y)

        for move in availableMoves:

            # only search moves that are in search space
            if (move[1] in searchSpace):

                (newX, newY) = move[1]
                newBoardState = board.makeMove(x, y, newX, newY, ourPiece)
                newBoardHash = newBoardState.getHashValue()
                
                # check if the current state is in previous states
                if (newBoardHash not in hashedBoardStates) or \
                (hashedBoardStates[newBoardHash] < depth):
                    # also consider fewer steps to reach the same state
                    hashedBoardStates[newBoardHash] = depth
                    moves.append(move)

                    isFound = faster_DFS(newBoardState, ourPiece, layers, depth - 1)

                    # backtrack
                    moves.pop()
                    if (isFound):
                        return True
    return False