import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import call_function

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            )
        }
    )
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the contents of the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to get contents from, relative to the working directory."
            )
        },
        required=["file_path"]
    )
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the specified content to the specified file path, constrained by the directory. The current content of the file will be overwritten.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file that the content should be written to."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that should be written to the file."
            )
        },
        required=["file_path", "content"]
    )
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the python script file at the provied file_path using the provided arguments (args). Constrained by the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the script file that should be run."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Positional arguments that should be passed to the script.",
                items=types.Schema(
                    description="Argument that should be passed to the script."
                )
            )
        },
        required=["file_path"]
    )
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]
)

config=types.GenerateContentConfig(
    tools=[available_functions],
    system_instruction=system_prompt
)

def main(prompt, debug=False, verbose=False):
    load_dotenv()

    messages = [
        types.Content(
            role="user",
            parts=[
                types.Part(text=prompt)
            ]
        )
    ]

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    if verbose: print(f"User prompt: {prompt}")
    if debug:
        print("skipping call because of debug flag")
        return
    res = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=config
    )
    if res.text:
        print(res.text)
    if res.function_calls:
        for call in res.function_calls:
            # print(f"Calling function: {call.name}({call.args})")
            function_call_result = call_function(call, verbose)
            if not function_call_result.parts[0].function_response.response:
                raise Exception("Internal system error: call_function returned type.Content without a response.")

            print(f"-> {function_call_result.parts[0].function_response.response}")

    if verbose: print(f"Prompt tokens: {res.usage_metadata.prompt_token_count}")
    if verbose: print(f"Response tokens: {res.usage_metadata.candidates_token_count}")



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No prompt provided.")
        exit(1)
    prompt = sys.argv[1]
    if prompt.startswith("-"):
        print("The prompt must be the first argument provided.")
        exit(1)
    debug = "--debug" in sys.argv or "-D" in sys.argv
    verbose = "--verbose" in sys.argv or "-V" in sys.argv

    main(prompt, debug=debug, verbose=verbose)
