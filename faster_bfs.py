import copy

# used to only keep track of valid moves
previousMoves = []      # keep track of previous moves
currentMoves = []       # keep track of current moves

# avoid wasting resources looking into suboptimal search space
hashedBoardStates = {}  # keep track of states seen before

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

    ############################################################
    # check for square boxes
    if board.checkSquareFormation(ourPiece):
        return False

    # check for only 1 white piece and black pieces not beside a corner piece
    if board.checkCantWin(ourPiece):
        return False
    ############################################################

    # store all nodes to visit in a queue
    # start with board in queue
    queue = [(board, [])]

    # add starting board into board states seen
    hashedBoardStates[board.getHashValue()] = True

    while queue:
        (node, previousMoves) = queue.pop(0)

        #  get smaller search space
        searchSpace = node.getSmallerSearchSpace(ourPiece, layers)
        # print(searchSpace)

        # iterate through all pieces on board 
        # and store board states at the back of queue
        ourPieces = node.getAllPieces(ourPiece)

        ############################################################
        # check if we dont have enough pieces in the search space 
        # to eliminate opponent
        countOurs = 0
        for s in searchSpace:
            if (s in ourPieces):
                countOurs = countOurs + 1    
        if countOurs < 2:
            searchSpace = node.getMinMaxSearchSpace(ourPiece)
        ############################################################

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
                            # makeAllMoves(currentMoves) # DEBUG
                            printMoves(currentMoves)
                            return True

    # no solution is found, exit
    return False