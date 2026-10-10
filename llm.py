import os

def chat(prompt):
    token = os.environ.get("HF_TOKEN")
    if token:
        from huggingface_hub import InferenceClient
        client = InferenceClient(api_key=token)
        r = client.chat_completion(
            model="Qwen/Qwen2.5-Coder-32B-Instruct",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
        )
        return r.choices[0].message.content
    import ollama
    r = ollama.chat(
        model="qwen2.5-coder:3b",
        messages=[{"role": "user", "content": prompt}],
    )
    return r["message"]["content"]