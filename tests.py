import sys
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

def test_get_files_info(working_dir, path):
    if path == ".":
        print("Result for working directory root:")
    else:
        print(f"Result for working direcotry \"{path}\" sub-path:")
    print(get_files_info(working_dir, path))

def test_get_file_content(working_dir, path):
    print(f"Result for file \"{path}\":")
    print(get_file_content(working_dir, path))

def main(working_dir, path):
    if workdir == None:
        test_get_files_info("calculator", ".")
        test_get_files_info("calculator", "pkg")
        test_get_files_info("calculator", "/bin")
        test_get_files_info("calculator", "../")
        test_get_file_content("calculator", "main.py")
        test_get_file_content("calculator", "pkg/calculator.py")
        test_get_file_content("calculator", "/bin/cat")
        test_get_file_content("calculator", "pkg/does_not_exist.py")
        exit(0)
    test_get_files_info(working_dir, path)

    

if __name__ == "__main__":
    workdir = sys.argv[1] if len(sys.argv) > 1 else None
    directory = sys.argv[2] if len(sys.argv) > 2 else None
    main(workdir, directory)