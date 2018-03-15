## RULES
#  "O" is white
# "@" is black
# "X" is corner
# "-" is empty
import copy

hashedBoardStates = {}
def invertBoard(board):
    newBoard = [[0 for x in range(0, 8)] for y in range(0, 8)]
    for i in range(0, len(board)):
        for j in range(0, len(board)):
            newBoard[i][j] = board[j][i]
    return newBoard


# print out
# for i in range(0,8):
#     print(board[i])


DIRECTION = [
    [-1, 0],  # left
    [+1, 0],  # right
    [0, -1],  # up
    [0, +1]   # down
]


def isEmpty(board,x , y):
    if board[x][y] == '-':
        return True
    return False


def isWithinBoard(x, y):
    if (x in range(0, 8)) and (y in range(0, 8)):
        return True
    return False


def isValidMove(board, x, y, direction):
    newX = x + DIRECTION[direction][0]
    newY = y + DIRECTION[direction][1]
    # if empty
    if isWithinBoard(newX, newY) and isEmpty(board, newX, newY):
        return 1

    # if can jump
    newX2 = newX + DIRECTION[direction][0]
    newY2 = newY + DIRECTION[direction][1]
    if isWithinBoard(newX2, newY2) and isEmpty(board, newX2, newY2) and board[newX][newY] in ['@', 'O']:
        return 2
    return 0


def countMoves(board, colour):
    possibleMoves = 0
    for i in range(0, len(board)):
        for j in range(0, len(board)):
            if board[i][j] == colour:
                for direction in range(0, 4):
                    if isValidMove(board, i, j, direction) != 0:
                        possibleMoves = possibleMoves + 1
    return possibleMoves



#######################################################

# computing hash value for entire board
# by treating pieces as integers from 0 through 3
# and base 4 digit system (quaternary numeral system)
# @TODO: EXPLAIN WITH AN EXAMPLE using first line
def hashBoard(board):
    order = 1
    total = 0
    for i in range(0, len(board)):
        for j in range(0, len(board)):
            if (board[i][j] == '-'):
                currentDigit = 0
            elif (board[i][j] == 'X'):
                currentDigit = 1
            elif (board[i][j] == 'O'):
                currentDigit = 2
            else:
                currentDigit = 3
            total = total + currentDigit * (4 ** order)
            order = order + 1
    return total





def makeMove(x, y, newX, newY, currentBoard):
    board = copy.deepcopy(currentBoard)
    board[newX][newY] = board[x][y]
    board[x][y] = "-"

    # step 1: white eliminating black
    for direction in range(0, 4):
        adjPieceX = newX + DIRECTION[direction][0]
        adjPieceY = newY + DIRECTION[direction][1]
        adjPieceX2 = adjPieceX + DIRECTION[direction][0]
        adjPieceY2 = adjPieceY + DIRECTION[direction][1]
        # if adjacent piece is within the board and is black
        # and jumping adjacent piece is within board and is white or a corner
        # then we remove the eliminated piece (ie. black piece)
        if isWithinBoard(adjPieceX, adjPieceY) and board[adjPieceX][adjPieceY] == '@' and isWithinBoard(adjPieceX2, adjPieceY2) and board[adjPieceX2][adjPieceY2] in ['O', 'X']:
            board[adjPieceX][adjPieceY] = '-'


    # step 2: black eliminating white
    # (is left withinBorder and have black or corner) and (right withinBoarder and have black or corner)
    if (isWithinBoard(newX - 1, newY) and board[newX - 1][newY] in ['@', 'X']) and (
            isWithinBoard(newX + 1, newY) and board[newX + 1][newY] in ['@', 'X']):
        board[newX][newY] = '-'

    # (is up withinBorder and have black or corner) and (down withinBoarder and have black or corner)
    if (isWithinBoard(newX, newY - 1) and board[newX][newY - 1] in ['@', 'X']) and (
            isWithinBoard(newX, newY + 1) and board[newX][newY + 1] in ['@', 'X']):
        board[newX, newY] = '-'

    return board


# check if all pieces needed to be killed is eliminated
def won(board, killedPiece):
    for i in range(0, len(board)):
        for j in range(0, len(board)):
            if board[i][j] == killedPiece:
                return False
    return True


# print all moves made
def printMoves():
    for move in moves:
        print(move[0],'->',move[1])


def printBoard(board):
    board = invertBoard(board)
    for line in board:
        for piece in line:
            print(piece, end=' ')
        print('')
    print('')


# search for winning solution
# return True if found
def DFS(currentBoard):

    #DEBUG
    #printBoard(currentBoard)
    #print(hashBoard(currentBoard))

    if won(currentBoard, '@'):
        printMoves()
        return True

    for i in range(0, len(currentBoard)):
        for j in range(0, len(currentBoard)):
            if currentBoard[i][j] == "O":
                for direction in range(0, 4):
                    # not zero, meaning we can move
                    if isValidMove(currentBoard, i, j, direction) != 0:
                        # check if move is valid then make normal move
                        if isValidMove(currentBoard, i, j, direction) == 1:
                            iDirection = i + DIRECTION[direction][0]
                            jDirection = j + DIRECTION[direction][1]

                        # check if move is valid then make jump move
                        elif isValidMove(currentBoard, i, j, direction) == 2:
                            iDirection = i + DIRECTION[direction][0] * 2
                            jDirection = j + DIRECTION[direction][1] * 2

                        newBoardState = makeMove(i, j, iDirection, jDirection, currentBoard)
                        newBoardHash = hashBoard(newBoardState)

                        # @TODO Explain the second condition (in case we reset previous states to False)
                        # check if the current state is in previous states
                        if (newBoardHash not in hashedBoardStates) or (hashedBoardStates[newBoardHash] == False):
                            hashedBoardStates[newBoardHash] = True
                            moves.append(((i, j), (iDirection, jDirection)))

                            #DEBUG
                            #print(((i, j), (iDirection, jDirection)))

                            isFound = DFS(newBoardState)
                            moves.pop()
                            if (isFound):
                                return True
    return False





# init & input
oboard = [[0 for x in range(0, 8)] for y in range(0, 8)]
invBoard = [[0 for x in range(0, 8)] for y in range(0, 8)]

moves = []

for i in range(0, len(oboard)):
    invBoard[i] = input().strip().split(" ")
command = input().strip()
oboard = invertBoard(invBoard)

if command == "Moves":
    print(countMoves(oboard, 'O'))
    print(countMoves(oboard, '@'))
else:
    DFS(oboard)
# print(won(board, '@'))


#print("stupid DFS")



