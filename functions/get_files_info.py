import os
import functions.validation as validate


def get_files_info(working_directory, directory="."):
    path_validity = validate.workdir_path(working_directory, directory)
    absolute_path = ""
    match path_validity[0]:
        case 0:
            absolute_path = path_validity[1]
        case 1:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        case _:
            return path_validity[1]

    if not os.path.isdir(absolute_path):
        return f'Error: "{directory}" is not a directory'

    def build_str(item_name):
        full_path = os.path.join(absolute_path, item_name)
        return f"- {item_name}: file_size={os.path.getsize(full_path)} bytes, is_dir={os.path.isdir(full_path)}"

    return "\n".join(list(map(build_str, os.listdir(absolute_path))))



    


