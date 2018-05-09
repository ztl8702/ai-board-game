import copy

# used to only keep track of valid moves
previousMoves = []      # keep track of previous moves
currentMoves = []       # keep track of current moves

# avoid wasting resources looking into suboptimal search space
BFShashedBoardStates = {}  # keep track of states seen before

def faster_BFS(board, ourPiece, layers):
    '''
    breadth first search
    '''
    def printMoves(moves):
        # print all the moves made
        for move in moves:
            print(move[0], '->', move[1])

    def makeAllMoves(moves):
        # Debugging utility function to print all the moves
        # visually with board movements
        oboard = copy.deepcopy(board)
        oboard.printBoard()

        for move in moves:
            ((x,y), (newX, newY)) = move
            oboard = oboard.makeMove(x, y, newX, newY, ourPiece)
            oboard.printBoard()

    # store all nodes to visit in a queue
    # start with board in queue
    queue = [(board, [])]

    # add starting board into board states seen
    BFShashedBoardStates[board.getHashValue()] = True

    while queue:
        (node, previousMoves) = queue.pop(0)

        #  get smaller search space
        searchSpace = node.getSmallerSearchSpace(ourPiece, layers)
        # print(searchSpace)

        # iterate through all pieces on board 
        # and store board states at the back of queue
        ourPieces = node.getAllPieces(ourPiece)

        for p in ourPieces:
            (x, y) = p
            availableMoves = node.getAvailableMoves(x, y)
        
            for move in availableMoves:
                
                # only search moves that are in search space
                if (move[1] in searchSpace):

                    (newX, newY) = move[1]
                    neighbour = node.makeMove(x, y, newX, newY, ourPiece)

                    # neighbour.printBoard() #DEBUG

                    newBoardHash = neighbour.getHashValue()

                    # check if the current board state was seen before
                    if (newBoardHash not in BFShashedBoardStates) or \
                    (BFShashedBoardStates[newBoardHash] == False):

                        # if it was not seen before, toggle it to seen
                        BFShashedBoardStates[newBoardHash] = True

                        currentMoves = copy.deepcopy(previousMoves)
                        currentMoves.append(move)

                        queue.append((neighbour, currentMoves))
                        
                        # found best sequence of moves
                        # print moves and exit search
                        if (neighbour.isWon(ourPiece)):
                            # makeAllMoves(currentMoves) # DEBUG
                            printMoves(currentMoves)
                            return True

    # no solution is found, exit
    return False

moves = []
# DFS called multiple times, so need to keep track globally
DFShashedBoardStates = {}

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
                if (newBoardHash not in DFShashedBoardStates) or \
                (DFShashedBoardStates[newBoardHash] < depth):
                    # also consider fewer steps to reach the same state
                    DFShashedBoardStates[newBoardHash] = depth
                    moves.append(move)

                    isFound = faster_DFS(newBoardState, ourPiece, layers, depth - 1)

                    # backtrack
                    moves.pop()
                    if (isFound):
                        return True
    return False
