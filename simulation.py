import copy
from common import Board
from parta import BFS
from parta_dfs import DFS
from faster_bfs import faster_BFS
from faster_dfs import faster_DFS

MAX_LAYERS = 2 # number of cells to mark into smaller search space
MAX_DEPTH = 1000

oboard = Board() # original board
oboard.readInput()
command = input().strip()

if command == "Moves":
    print(oboard.countMoves(Board.PIECE_WHITE))
    print(oboard.countMoves(Board.PIECE_BLACK))
else:
    # SEARCH 1: BFS with smaller search space
    # if (not faster_BFS(oboard, Board.PIECE_WHITE, MAX_LAYERS)):
    # 	print("solution not found")
    
    # SEARCH 2: depth limited DFS with smaller search space
    for i in range(1, MAX_DEPTH):
        # print("Trying depth ", i) # DEBUG 
        if (faster_DFS(oboard, Board.PIECE_WHITE, MAX_LAYERS, i)):
            break

    # SEARCH 3: normal BFS
    # if (not BFS(oboard, Board.PIECE_WHITE)):
    # 	print("solution not found")

    # SEARCH 4: depth limited DFS
    # for i in range(1, MAX_DEPTH):
    #     # print("Trying depth ", i) # DEBUG
    #     if (DFS(oboard, Board.PIECE_WHITE, i)):
    #         break

    
