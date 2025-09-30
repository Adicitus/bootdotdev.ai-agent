import os

def workdir_path(working_directory, child_path):
    absolute_working_directory = os.path.abspath(working_directory)
    naive_path = os.path.join(working_directory, child_path) # Naievely join paths together
    absolute_path = os.path.abspath(naive_path) # Evaluate the path for relative path shenanigans

    try:
        in_working_directory = os.path.commonpath([absolute_path, absolute_working_directory]) == absolute_working_directory
        if in_working_directory:
            # The resulting path is outside the working directory!
            return 0, absolute_path
        else:
            return 1, None
    except Exception as e:
        return -1, f"Error: System error while trying to determine if {child_path} is within the allowed working directory: {e}"