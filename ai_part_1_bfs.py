import copy
from common import Board

hashedBoardStates = {}

def BFS(board):

    # store all nodes to visit in a queue
    queue = [board]

    # store all visited nodes
    explored = []

    while queue:
        node = queue.pop(0)
        if node not in explored:
            explored.append(node)

            # iterate through all pieces on board 
            # and store board states at the back of queue

            for i in range(0, len(node)):
                for j in range(0, len(node)):
                    if node[i][j] == PIECE_WHITE:
                        # check for all directions
                        for direction in range(0, 4):
                            # if not zero = we can move
                            if isValidMove(node, i, j, direction) != 0:
                                # if one = normal move
                                if isValidMove(node, i, j, direction) == 1:
                                    iDirection = i + DIRECTION[direction][0]
                                    jDirection = j + DIRECTION[direction][1]

                                # if two = jump move
                                elif isValidMove(node, i, j, direction) == 2:
                                    iDirection = i + DIRECTION[direction][0] * 2
                                    jDirection = j + DIRECTION[direction][1] * 2

                                neighbour = makeMove(i, j, iDirection, jDirection, board)
                                newBoardHash = hashBoard(neighbour)

                                # check if the current board state was seen before
                                if (newBoardHash not in hashedBoardStates) or (hashedBoardStates[newBoardHash] == False):
                                    hashedBoardStates[newBoardHash] = True
                                    moves.append(((i, j), (iDirection, jDirection)))

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