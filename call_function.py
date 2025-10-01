from google.genai import types
import functions


# Handles FunctionCall requests from the LLM
def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_args = function_call_part.args

    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")


    try:
        func = getattr(functions, function_name)
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    try:
        result = func("./calculator", **function_args)
        return types.Content(
            role="tool",
            parts = [
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": result}
                )
            ]
        )
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": e}
                )
            ]
        )
    