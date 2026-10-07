import os
import tempfile
import streamlit as st
import subprocess
from fixer import get_fixed_code
from debugger import run_code, ask_ai

st.set_page_config(page_title="AI Code Debugger", page_icon="🐞", layout="wide")

# ---------- Custom styling ----------
st.markdown("""
<style>
.hero {
    padding: 2rem;
    border-radius: 16px;
    background: linear-gradient(135deg, #6366f1, #8b5cf6, #ec4899);
    color: white;
    text-align: center;
    margin-bottom: 1.5rem;
}
.hero h1 { margin: 0; font-size: 2.4rem; }
.hero p { margin: 0.5rem 0 0; opacity: 0.9; }
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.6rem 1.5rem;
    font-weight: 600;
}
.stButton > button:hover { transform: scale(1.03); color: white; }
</style>
""", unsafe_allow_html=True)

# ---------- Example bugs ----------
EXAMPLES = {
    "Division by zero": "print(1/0)",
    "Undefined variable": "print(name)",
    "Wrong index": "numbers = [1, 2, 3]\nprint(numbers[5])",
    "Missing bracket": "print('hello'",
}

# ---------- Sidebar ----------
with st.sidebar:
    st.header("⚙️ About")
    st.write("This tool runs an AI model on your own laptop using Ollama. Your code never leaves your computer.")
    st.divider()
    st.subheader("Try an example")
    example = st.selectbox("Pick one", list(EXAMPLES.keys()))

# ---------- Header ----------
st.markdown("""
<div class="hero">
    <h1>🐞 AI Code Debugger</h1>
    <p>Paste your Python code. Get the error explained and fixed.</p>
</div>
""", unsafe_allow_html=True)

# ---------- Helper functions ----------
def safe_run(code):
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(code)
        path = f.name
    try:
        return run_code(path)
    except subprocess.TimeoutExpired:
        return "Error: code took too long to run (maybe an infinite loop)."
    finally:
        os.remove(path)

def auto_fix(code, max_tries=3):
    log = []
    for attempt in range(max_tries + 1):
        error = safe_run(code)
        if not error:
            return code, True, log
        if attempt == max_tries:
            break
        log.append(f"Attempt {attempt + 1}: {error.strip().splitlines()[-1]}")
        code = get_fixed_code(code, error)
    return code, False, log

# ---------- Two columns ----------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Your code")
    code = st.text_area("code", value=EXAMPLES[example], height=300, label_visibility="collapsed")
    b1, b2 = st.columns(2)
    explain = b1.button("🚀 Explain error")
    fix = b2.button("🪄 Auto-fix")

with col2:
    st.subheader("🤖 Result")
    if explain:
        if not code.strip():
            st.warning("Please paste some code first.")
        else:
            error = safe_run(code)
            if not error:
                st.success("✅ No errors found!")
            else:
                tab1, tab2 = st.tabs(["❌ Error", "💡 AI Explanation"])
                with tab1:
                    st.code(error, language="bash")
                with tab2:
                    with st.spinner("AI is thinking..."):
                        st.markdown(ask_ai(code, error))
    elif fix:
        if not code.strip():
            st.warning("Please paste some code first.")
        else:
            with st.spinner("AI is fixing your code..."):
                fixed, ok, log = auto_fix(code)
            for line in log:
                st.write("🔁", line)
            if ok:
                st.success("✅ Fixed! The code now runs with no errors.")
                st.balloons()
            else:
                st.error("Could not fully fix it. Here is the best attempt:")
            st.code(fixed, language="python")
    else:
        st.info("Your result will appear here.")