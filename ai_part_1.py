
## RULES
#  "O" is white
# "@" is black
# "X" is corner 
# "-" is empty
    
board = [[0 for x in range(0,8)] for y in range(0,8)]

for i in range(0, len(board)):
    board[i] = input().strip().split(" ")
        
# print out
for i in range(0,8):
    print(board[i])
    
    
DIRECTION = [
    [0, -1], #left
    [0, +1], #right
    [-1, 0], #up
    [+1, 0]  #down
]

def isEmpty(x,y):
    if board[x][y] == '-':
        return True
    return False

def isWithinBoard(x,y):
    if x in range(0, 8) and y in range(0,8):
        return True
    return False

def isValidMove(x,y, direction):
    newX = x + DIRECTION[direction][0]
    newY = y + DIRECTION[direction][1]
    # if empty
    if isWithinBoard(newX,newY) and isEmpty(newX, newY):
        return True

    # if can jump
    newX2 = newX + DIRECTION[direction][0]
    newY2 = newY + DIRECTION[direction][1]
    if isWithinBoard(newX2,newY2) and isEmpty(newX2,newY2) and board[newX][newY] in ['@', 'O']:
        return True
    return False
    
    

def countMoves(colour):
    possibleMoves = 0
    for i in range(0, len(board)):
        for j in range(0, len(board)): 
            if board[i][j] == colour:
                for direction in range(0,4):
                    if isValidMove(i,j,direction):
                        possibleMoves = possibleMoves + 1
    return possibleMoves

print(countMoves('O'))
print(countMoves('@'))