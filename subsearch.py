import copy

from common import Board


moves = []
# DFS called multiple times, so need to keep track globally
hashedBoardStates = {}

# search for winning solution
# return True if found
def DFS(board, ourPiece, layers, depth):
        
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
    searchSpace = board.getInterestingSpots(ourPiece, layers)

    ourPieces = board.getAllPieces(ourPiece)

    for p in ourPieces:
        (x, y) = p
        

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


#previous paths
ppath = {}
plen = {}
def findpath(subboard, fromX, fromY, toX, toY, steps):
    
    def seen():
        h = subboard.getHashValue()
        if (h not in ppath):
            return False
        if ((fromX, fromY, toX, toY) not in ppath[h]):
            return False

    if (fromX == toX and fromY == toY):
        return []

    if seen():
        if ppath[subboard][(fromX, fromY, toX, toY)] == -1:
            return -1
        elif len(ppath[subboard][(fromX, fromY, toX, toY)]) <= steps:
            return copy.deepcopy(ppath[subboard][(fromX, fromY, toX, toY)])
    else:
        ppath[subboard] = {}
        ppath[subboard][(fromX, fromY, toX, toY)] = -1

    for i in range(4):
        newX = Board.DIRECTION[i][0] + fromX
        newY = Board.DIRECTION[i][1] + fromY
        newSB = subboard.getSubBoard(newX, newY, toX, toY).extend()
        deltaX = newSB.xOffset - subboard.xOffset
        deltaY = newSB.yOffset - subboard.yOffset
        path = findpath(newSB, newX-deltaX, newY-deltaY, toX-deltaX, toY-deltaY, steps+1)
        if (path != -1) and ((ppath[subboard][(fromX, fromY, toX, toY)]==-1) or len(path)+1 < len(ppath[subboard][(fromX, fromY, toX, toY)])):
            newPath = []
            newPath.append(((fromX, fromY),(newX, newY)))
            for move in path:
                if (not (subboard.isWithinSubBoard(move[0]) and subboard.isWithinSubBoard(move[1]))):
                    raise Exception("Something wrong")
                ((a,b),(c,d)) = move
                newPath.append(((a+deltaX),(b+deltaY), (c+deltaX,d+deltaY)))
            ppath[subboard][(fromX, fromY, toX, toY)] = newPath

    return ppath[subboard][(fromX, fromY, toX, toY)]


b = Board()

b.readInput()

b.printBoard()

c = b.getSubBoard(2,2,5,3)

print(findpath(c, 0,0,2,2,0))