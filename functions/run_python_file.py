import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    try:
        #Get working and target paths
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))

        #Check path validity
        if not os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if target_dir[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'
        
        #Building command to run
        command = ["python", target_dir]
        if args != None:
            command.extend(args)

        #Running subprocess
        completed_process = subprocess.run(command, cwd = working_dir_abs, capture_output=True, text=True, timeout=30, )
        
        #Build complete string
        complete_string = ""
        if completed_process.returncode != 0:
            complete_string += f"Process exited with code {completed_process.returncode}\n"

        if completed_process.stdout == "" and completed_process.stderr == "":
            complete_string += "No output produced"
        else:
            if completed_process.stdout:
                complete_string += f"STDOUT: {completed_process.stdout}"
            if completed_process.stderr:
                complete_string += f"\nSTDERR: {completed_process.stderr}"

        return complete_string
    except Exception as e:
        return f"Error: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute Python files with optional arguments",
    parameters=types.Schema(
        required=["file_path"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional arguments to pass to the Python file",
                items=types.Schema(
                    type=types.Type.STRING
                )
            )
        },
    ),
)