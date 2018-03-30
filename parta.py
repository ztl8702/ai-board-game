import copy

# used to only keep track of valid moves
previousMoves = []      # keep track of previous moves
currentMoves = []       # keep track of current moves

# avoid wasting resources looking into suboptimal search space
hashedBoardStates = {}  # keep track of states seen before

def BFS(board, ourPiece):
    '''
    breadth first search
    '''
    def printMoves(moves):
        # print all the moves made
        for move in moves:
            print(move[0], '->', move[1])

    # store all nodes to visit in a queue
    # start with board in queue
    queue = [(board, [])]

    # add starting board into board states seen
    hashedBoardStates[board.getHashValue()] = True

    while queue:
        (node, previousMoves) = queue.pop(0)

        # iterate through all pieces on board 
        # and store board states at the back of queue
        ourPieces = node.getAllPieces(ourPiece)

        for p in ourPieces:
            (x, y) = p
            availableMoves = node.getAvailableMoves(x, y)
        
            for move in availableMoves:
                (newX, newY) = move[1]
                neighbour = node.makeMove(x, y, newX, newY, ourPiece)

                newBoardHash = neighbour.getHashValue()

                # check if the current board state was seen before
                if (newBoardHash not in hashedBoardStates) or \
                (hashedBoardStates[newBoardHash] == False):

                    # if it was not seen before, toggle it to seen
                    hashedBoardStates[newBoardHash] = True

                    currentMoves = copy.deepcopy(previousMoves)
                    currentMoves.append(move)

                    queue.append((neighbour, currentMoves))
                    
                    # found best sequence of moves
                    # print moves and exit search
                    if (neighbour.isWon(ourPiece)):
                        printMoves(currentMoves)
                        return True

    # no solution is found, exit
    return False