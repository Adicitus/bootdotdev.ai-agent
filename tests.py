import sys
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file

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
        tests = [
            {
                "function": test_get_files_info,
                "cases": [
                    ("calculator", "."),
                    ("calculator", "pkg"),
                    ("calculator", "/bin"),
                    ("calculator", "../")
                ]
            },
            {
                "function": test_get_file_content,
                "cases": [
                    ("calculator", "main.py"),
                    ("calculator", "pkg/calculator.py"),
                    ("calculator", "/bin/cat"),
                    ("calculator", "pkg/does_not_exist.py"),
                ]
            },
            {
                "function": lambda wd, p, c: print(write_file(wd, p, c)),
                "cases": [
                    ("calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
                    ("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
                    ("calculator", "/tmp/temp.txt", "this should not be allowed")
                ]
            }
        ]

        for test in tests:
            f = test["function"]
            for case in test["cases"]:
                print("[START: test case] " + "-" * 60)
                print(f"Testing {f} with the following arguments: {case}")
                f(*case)
                print("[END:   test case] " + "-" * 60)

        exit(0)
    test_get_files_info(working_dir, path)

    

if __name__ == "__main__":
    workdir = sys.argv[1] if len(sys.argv) > 1 else None
    directory = sys.argv[2] if len(sys.argv) > 2 else None
    main(workdir, directory)