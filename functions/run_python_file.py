import os
import subprocess
import sys
import functions.validation as validate

def run_python_file(working_directory, file_path, args=[]):
    path_validation = validate.workdir_path(working_directory, file_path)
    match path_validation[0]:
        case 0:
            pass
        case 1:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        case _:
            return path_validation[1]

    absolute_path = path_validation[1]

    if not absolute_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    if not os.path.isfile(absolute_path):
        return f'Error: File "{file_path}" not found.'

    try:
        result = subprocess.run(
            ["python3", absolute_path, *args],
            timeout=30,
            capture_output=True,
            text=True,
            cwd=working_directory
        )
        msg = ""

        if result.returncode != 0:
            msg = f"Process exited with code {result.returncode}. "
        

        if result.stdout or result.stderr:
            msg += f"STDOUT: {result.stdout} STDERR: {result.stderr}"
        else:
            msg += f"No output produced"
        
        return msg
    except Exception as e:
        return f"Error: executing Python file: {e}"


