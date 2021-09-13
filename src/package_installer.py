import subprocess
requirments = [
    "PyQt5",
    "openpyxl",
    "matplotlib"]

for req in requirments:
    subprocess.call(['pip', 'install', req])



