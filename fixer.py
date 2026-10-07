import re
import sys
import shutil
import ollama
from debugger import run_code

MODEL = "qwen2.5-coder:3b"
MAX_TRIES = 3

def get_fixed_code(code, error):
    prompt = f"""Fix this Python code. Reply with ONLY the full fixed code inside one ```python block. No explanation.

Code:
{code}

Error:
{error}"""
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    text = response["message"]["content"]
    match = re.search(r"```(?:python)?\n(.*?)```", text, re.DOTALL)
    return match.group(1) if match else text

if __name__ == "__main__":
    path = sys.argv[1]
    shutil.copy(path, path + ".bak")  # backup of your original file

    with open(path) as f:
        code = f.read()

    for attempt in range(MAX_TRIES + 1):
        error = run_code(path)
        if not error:
            print("Code runs with no errors!")
            break
        if attempt == MAX_TRIES:
            print("Could not fix it after", MAX_TRIES, "tries.")
            break
        print(f"Attempt {attempt + 1}: error found, asking AI to fix...")
        code = get_fixed_code(code, error)
        with open(path, "w") as f:
            f.write(code)