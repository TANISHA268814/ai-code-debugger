import os

def chat(prompt):
    key = os.environ.get("GROQ_API_KEY")
    if key:
        try:
            from groq import Groq
            client = Groq(api_key=key)
            r = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
            )
            return r.choices[0].message.content
        except Exception as e:
            return f"AI error: {e}"
    import ollama
    r = ollama.chat(
        model="qwen2.5-coder:3b",
        messages=[{"role": "user", "content": prompt}],
    )
    return r["message"]["content"]