"""
A utility program for comparing performance of different agents.
"""

import subprocess
import re
import sys
import os
from datetime import datetime
PYTHON = "python"

def get_winner(outputStr):
    matches = re.findall(r'winner: ([A-Za-z]+)!',outputStr)
    try:
        return matches[0]
    except:
        return None

def get_last_turn(outputStr):
    matches = re.findall(r'([0-9]+) turns into the',outputStr)
    try:
        return int(matches[-1])
    except:
        return 0

def play_once(whitePlayerModule="minimax_player", blackPlayerModule = "minimax_player"):
    result = subprocess.run([PYTHON,'referee.py',whitePlayerModule, blackPlayerModule], stdout=subprocess.PIPE)
    stdout = result.stdout.decode('utf-8')
    return stdout
    #print("\n\n\n\n STDOUT\n", stdout)

def play(outputDir, whitePlayerModule, blackPlayerModule, rounds = 10):
    whiteFolder = os.path.join(outputDir, "W_"+whitePlayerModule)
    blackFolder = os.path.join(outputDir, "B_"+blackPlayerModule)
    drawFolder = os.path.join(outputDir, "draw")
    unknownFolder = os.path.join(outputDir, "unknown") 

    for d in [whiteFolder, blackFolder, drawFolder, unknownFolder]:
        if not os.path.exists(d):
            os.makedirs(d)
    print("="*40)
    print(f"\t{whitePlayerModule}(W)\tvs.\t{blackPlayerModule}(B)")
    print("="*40)
    print()
    
    for i in range(rounds):
        print(f"Round {i+1}: ",end="",flush=True)
        output = play_once(whitePlayerModule, blackPlayerModule)
        winner = get_winner(output)
        finalTurn = get_last_turn(output)
        fileName = f"round_{i+1}_turn_{finalTurn}_timestamp_{int(datetime.now().timestamp())}.txt"
        if winner == "W":
            outputFolder = whiteFolder
        elif winner == "B":
            outputFolder = blackFolder
        elif winner == "draw":
            outputFolder = drawFolder
        else:
            outputFolder = unknownFolder
        
        outputFilePath = os.path.join(outputFolder, fileName)
        with open(outputFilePath, "wb") as f:
            f.write(output.encode('utf-8'))

        print(f"Winner = {winner} at {finalTurn} turns") 


if __name__ == "__main__":
    #print(sys.argv)
    if (len(sys.argv)!=5):
        print(f"Usage: {sys.argv} output_dir white_module black_module rounds")
        exit(-1)
    selfName, outputDir, whiteModule, blackModule, rounds = sys.argv
    play(outputDir, whiteModule, blackModule, int(rounds) )