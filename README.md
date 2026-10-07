# 🐞 AI Code Debugger

An AI-powered tool that finds errors in your Python code, explains them in simple words, and can fix them automatically. It runs on your own laptop using Ollama, so your code never leaves your computer.

## ✨ Features

- Explains errors in beginner-friendly language
- 🪄 Auto-fix: the AI fixes the code and re-runs it until the error is gone
- Simple web interface built with Streamlit
- Example bugs to try in one click
- 100% local and free


## 🛠️ Tech Stack

Python, Streamlit, Ollama (qwen2.5-coder)

## 🚀 How to Run

1. Install Ollama from https://ollama.com/download
2. Download the model:
```
   ollama pull qwen2.5-coder:3b
```
3. Clone this repo:
```
   git clone https://github.com/TANISHA268814/ai-code-debugger.git
   cd ai-code-debugger
```
4. Create a virtual environment and install requirements:
```
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
```
5. Start the app:
```
   streamlit run app.py
```

## 🤝 Contributing

Contributions are welcome, especially during Hacktoberfest! Look for issues labeled `good first issue`.

1. Fork this repo
2. Create a branch: `git checkout -b my-feature`
3. Make your changes and commit
4. Open a Pull Request

## 📄 License

MIT