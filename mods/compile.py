from os import makedirs

thunk = """1>2# : ^
'''
@echo off
python "%~f0"
exit /b
'''
"""

py_program = "sync.py"

def read_file(path: str):
    with open(path, "r") as file:
        return file.readlines()

makedirs("out", exist_ok=True)
with open("out/sync.bat", "w") as file:
    file.writelines(thunk)
    file.write('\n')
    file.writelines(read_file(py_program))
