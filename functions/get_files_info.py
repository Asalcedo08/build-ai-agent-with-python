import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    try:
        #Get the working and target dirs
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        #Checks if target directory is within scope of the working directory
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        #Checking directory validity
        if not valid_target_dir:
            return f'Error: cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        contents = ""
        for file in os.listdir(target_dir):
            path_to_file = os.path.join(target_dir, file)
            contents += f"\n- {file}: file_size={os.path.getsize(path_to_file)} bytes, is_dir={os.path.isdir(path_to_file)}"
        return contents
    except Exception as e:
        return f"Error: {e}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)