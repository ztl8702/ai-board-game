# -*- coding: utf-8 -*-
import glob
import os
import subprocess 

def runBFS(inputFile, outputFile = "output_bfs.txt" ):
    if os.name == 'nt': # Windows
        cmd = "powershell -c \"Get-Content %s | python %s >%s\"" % (inputFile, "parta.py", outputFile)
    else:
        cmd = "python3 %s <%s >%s" % ("parta.py", inputFile, outputFile)
    #print(cmd)
    os.system(cmd)

def runDFS(inputFile, outputFile = "output_dfs.txt"):
    if os.name == 'nt':
        cmd = "powershell -c \"Get-Content %s | python %s >%s\"" % (inputFile, "ai_part_1_dfs.py", outputFile)
    else:
        cmd = "python3 %s <%s >%s" % ("parta.py", inputFile, outputFile)
    #print(cmd)
    os.system(cmd)



def compareResults(file1="", file2=""):
    if os.name == 'nt':
        cmd = "powershell -c \"Compare-Object -ReferenceObject (Get-Content %s) -DifferenceObject (Get-Content %s)\"" % (file1, file2)
    else:
        cmd = ["diff",file1, file2]

    try:
        cmp_result = subprocess.check_output(cmd)
        return (len(cmp_result) == 0) # true if the files are the same
    except:
        return False

testcases = glob.glob('./testcases/*.in')
OUTPUT_BFS = "output_bfs.txt"
OUTPUT_DFS = "output_dfs.txt"

for i, testcase in enumerate(testcases):
    print("="*30)
    case_name = os.path.splitext(os.path.basename(testcase))[0]
    
    ans_file = os.path.splitext(testcase)[0] + '.out'
    ans_exists = os.path.exists(ans_file)

    print("Testcase #%d: %s" % (i+1, case_name))
    os.system("rm -f "+OUTPUT_BFS)
    os.system("rm -f "+OUTPUT_DFS)

    runBFS(testcase)
    print(" BFS✔ ", end="", flush = True)
    runDFS(testcase)
    print(" DFS✔ ", end="", flush = True)
    result = compareResults(OUTPUT_BFS, OUTPUT_DFS)

    print("Results are " + ("the same" if result else "NOT THE SAME"), end=" ", flush=True)
    if (not result):
        exit(-1)

    if ans_exists:
        print("|" + ("Same" if compareResults(OUTPUT_BFS, ans_file) else "NOT SAME") + " with answer")

    print()
    print("="*30)
    print()