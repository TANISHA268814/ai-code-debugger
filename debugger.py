import subprocess
import sys
import ollama

MODEL = "qwen2.5-coder:3b"

def run_code(path):
    result = subprocess.run(
        [sys.executable, path],
        capture_output=True, text=True, timeout=30
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
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]

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
        