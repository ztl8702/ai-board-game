import glob
import os

def runBFS(inputFile):
    if os.name == 'nt':
        cmd = "powershell -c \"Get-Content %s | python %s >%s\"" % (inputFile, "parta.py", "output.txt")
    else:
        cmd = "python %s <%s >%s" % ("parta.py", inputFile, "output.txt")
    print(cmd)
    os.system(cmd)

testcases = glob.glob('./testcases/*.in')

for i, testcase in enumerate(testcases):
    print("="*10)
    case_name = os.path.splitext(os.path.basename(testcase))[0]
    print("Testcase #%d: %s" % (i+1, case_name))
    runBFS(testcase)