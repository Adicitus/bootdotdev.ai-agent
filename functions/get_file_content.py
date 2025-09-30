
import os
import traceback
import functions.validation as validate

def get_file_content(working_directory, file_path):
    path_validity = validate.workdir_path(working_directory, file_path)

    absolute_path = ""

    match path_validity[0]:
        case 0:
            absolute_path = path_validity[1]
        case 1:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        case _:
            return path_validity[1]
    print(absolute_path)
    if not os.path.isfile(absolute_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(absolute_path, 'r') as f:
            content = f.read(10000)
            if len(content) >= 10000:
                content += f"[...File \"{file_path}\" truncated at 10000 characters]"
            return content
    except Exception as e:
        traceback.print_stack(e)
        return f"Error: failed to read {file_path}: {e}"