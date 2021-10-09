import subprocess
requirments = [
    "PyQt5",
    "openpyxl",
    "matplotlib",
    "scipy"]

for req in requirments:
    subprocess.call(['pip', 'install', req])