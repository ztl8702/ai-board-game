import glob
import os
import subprocess 

def runBFS(inputFile, outputFile = "output_bfs.txt" ):
    if os.name == 'nt': # Windows
        cmd = "powershell -c \"Get-Content %s | python %s >%s\"" % (inputFile, "parta.py", outputFile)
    else:
        cmd = "python %s <%s >%s" % ("parta.py", inputFile, outputFile)
   # print(cmd)
    os.system(cmd)

def runDFS(inputFile, outputFile = "output_dfs.txt"):
    if os.name == 'nt':
        cmd = "powershell -c \"Get-Content %s | python %s >%s\"" % (inputFile, "ai_part_1_dfs.py", outputFile)
    else:
        cmd = "python %s <%s >%s" % ("parta.py", inputFile, outputFile)
   # print(cmd)
    os.system(cmd)



def compareResults(file1="", file2=""):
    if os.name == 'nt':
        cmd = "powershell -c \"Compare-Object -ReferenceObject (Get-Content %s) -DifferenceObject (Get-Content %s)\"" % (file1, file2)
    else:
        raise NotImplementedError()

    cmp_result = subprocess.check_output(cmd)
    return (len(cmp_result) == 0) # true if the files are the same

testcases = glob.glob('./testcases/test_*.in')

for i, testcase in enumerate(testcases):
    print("="*10)
    case_name = os.path.splitext(os.path.basename(testcase))[0]
    print("Testcase #%d: %s" % (i+1, case_name))
    os.system("rm -f output_bfs.txt")
    os.system("rm -f output_dfs.txt")

    runBFS(testcase)
    print(" BFS√ ", end="", flush = True)
    runDFS(testcase)
    print(" DFS√ ", end="", flush = True)
    result = compareResults("output_bfs.txt", "output_dfs.txt")

    print("Results are " + ("the same" if result else "NOT THE SAME"))
    if (not result):
        exit(-1)
    print("="*10)
    print()