import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

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
            contents=messages
    )
    print(res.text)

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
