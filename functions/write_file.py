import os
import functions.validation as validate

def write_file(working_directory, file_path, content):
    path_validation = validate.workdir_path(working_directory, file_path)

    match path_validation[0]:
        case 0:
            pass
        case 1:
            return f"Error: Cannot write to \"{file_path}\" as it is outside the permitted working directory"
        case _:
            return path_validation[1]

    absolute_path = path_validation[1]

    try:
        parent_dir = os.path.dirname(absolute_path)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
    except:
        return f"Error: Failed to create the parent directory for {file_path}: {e}"

    try:
        with open(absolute_path, 'w') as f:
            n = f.write(content)
            print(f"Successfully wrote to \"{file_path}\" ({n} characters written)")

    except Exception as e:
        return f"Error: failed to write to \"{file_path}\": {e}"