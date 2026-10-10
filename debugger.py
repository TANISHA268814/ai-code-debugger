import os
import subprocess
import sys
from llm import chat

def run_code(path):
    env = {k: v for k, v in os.environ.items() if k not in ("HF_TOKEN", "GROQ_API_KEY")}
    result = subprocess.run(
        [sys.executable, path],
        capture_output=True, text=True, timeout=30, env=env
    )
    return result.stderr

def ask_ai(code, error):
    prompt = f"""You are a helpful code debugger for beginners.

Code:
{code}

Error:
{error}

1. Explain the error in simple words.
2. Show the fixed code."""
    return chat(prompt)

if __name__ == "__main__":
    path = sys.argv[1]
    with open(path) as f:
        code = f.read()

    error = run_code(path)
    if not error:
        print("No errors found!")
    else:
        print("Error found, asking AI...\n")
        print(ask_ai(code, error))