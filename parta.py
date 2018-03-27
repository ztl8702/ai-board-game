import copy
from common import Board

hashedBoardStates = {}

def BFS(board):

    def printMoves(moves):
        '''
        '''
        for move in moves:
            print(move[0], '->', move[1])

    # store all nodes to visit in a queue
    queue = [(board, [])]
    hashedBoardStates[board.getHashValue()] = True

    while queue:
        (node, previousMoves) = queue.pop(0)
        # iterate through all pieces on board 
        # and store board states at the back of queue
        whitePieces = node.getAllPieces(Board.PIECE_WHITE)

        for p in whitePieces:
            (i, j) = p
            availableMoves = node.getAvailableMoves(i,j)
        
            for move in availableMoves:
                (newI, newJ) = move[1]
                neighbour = node.makeMove(i,j, newI, newJ)
                newBoardHash = neighbour.getHashValue()

                # check if the current board state was seen before
                if (newBoardHash not in hashedBoardStates) or (hashedBoardStates[newBoardHash] == False):
                    hashedBoardStates[newBoardHash] = True

                    currentMoves = copy.deepcopy(previousMoves)
                    currentMoves.append(move)

                    queue.append((neighbour, currentMoves))

                    if (neighbour.isWon(Board.PIECE_WHITE)):
                        printMoves(currentMoves)
                        return True

    return False


previousMoves = []
currentMoves = []


oboard = Board()

oboard.readInput()
command = input().strip()

if command == "Moves":
    print(oboard.countMoves(Board.PIECE_WHITE))
    print(oboard.countMoves(Board.PIECE_BLACK))
else:
    hashedBoardStates = {}
    BFS(oboard)
