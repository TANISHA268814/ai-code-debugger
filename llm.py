import os

MODELS = [
    "Qwen/Qwen2.5-Coder-32B-Instruct",
    "meta-llama/Llama-3.1-8B-Instruct",
    "Qwen/Qwen2.5-72B-Instruct",
]

def chat(prompt):
    token = os.environ.get("HF_TOKEN")
    if token:
        from huggingface_hub import InferenceClient
        client = InferenceClient(api_key=token)
        last_error = ""
        for model in MODELS:
            try:
                r = client.chat_completion(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1000,
                )
                return r.choices[0].message.content
            except Exception as e:
                last_error = f"{model}: {e}"
        return f"AI error, all models failed. Last error: {last_error}"
    import ollama
    r = ollama.chat(
        model="qwen2.5-coder:3b",
        messages=[{"role": "user", "content": prompt}],
    )
    return r["message"]["content"]