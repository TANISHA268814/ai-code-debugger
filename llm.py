import os

MODELS = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]

def get_key():
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        try:
            import streamlit as st
            key = st.secrets.get("GROQ_API_KEY")
        except Exception:
            key = None
    return key.strip() if key else None

def chat(prompt):
    key = get_key()
    if key:
        from groq import Groq
        client = Groq(api_key=key)
        last = ""
        for model in MODELS:
            try:
                r = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1000,
                )
                return r.choices[0].message.content
            except Exception as e:
                last = f"{model}: {e}"
        return f"AI error: {last}"
    try:
        import ollama
        r = ollama.chat(
            model="qwen2.5-coder:3b",
            messages=[{"role": "user", "content": prompt}],
        )
        return r["message"]["content"]
    except Exception:
        return "AI error: GROQ_API_KEY secret not found, and Ollama is not available here."