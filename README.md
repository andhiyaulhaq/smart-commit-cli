# Smart Commit 🚀

A lightning-fast CLI tool that uses Google Gemini AI to analyze your staged Git changes and generate Conventional Commit messages automatically.

Stop writing "update stuff" or "fix bug". Let AI write descriptive, standardized commit messages for you.

## ✨ Features

- **Automatic Diff Analysis**: Reads your staged changes (`git diff --cached`).
- **Conventional Commits**: Generates messages following standard conventions (e.g., `feat:`, `fix:`, `refactor:`).
- **Interactive Mode**: Reviews the generated message and asks for confirmation before committing.
- **Fast & Free**: Uses Google's Gemini Flash models (optimized for speed and cost).

## 🛠️ Prerequisites

- Python 3.8+
- Git
- A Google Gemini API Key (Get one for free at [Google AI Studio](https://aistudio.google.com/))

## 📦 Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/andhiyaulhaq/smart-commit-cli.git
    cd smart-commit-cli
    ```

2.  **Install dependencies:**
    This tool uses the modern Google Gen AI SDK.
    ```bash
    pip install google-genai
    ```

## ⚙️ Configuration

### 1. Set your API Key

You need to export your Gemini API key as an environment variable.

**For Mac/Linux:**
Add this to your `~.bashrc` or `~.zshrc`:

```bash
export GEMINI_API_KEY="your_actual_api_key_here"
```

````

**For Windows (Git Bash):**
Add this to your `~/.bashrc`:

```bash
export GEMINI_API_KEY="your_actual_api_key_here"
```

### 2. Create the Alias (Recommended)

To use this tool like a native git command (e.g., typing `gcm`), create a shell alias.

Add this line to your shell configuration file (`~/.bashrc`, `~/.zshrc`, or `~/.bash_profile`):

```bash
# Replace /path/to/ with the actual path to where you cloned the repo
alias gcm="python /path/to/smart-commit/git-gemini.py"
```

Reload your terminal:

```bash
source ~/.bashrc
```

## 🚀 Usage

1. **Stage your changes** as usual:

```bash
git add .
```

2. **Run the tool:**

```bash
gcm
```

3. **Review & Commit:**
   The tool will print a suggested message. Type `y` to confirm and commit immediately, or `n` to abort.

```text
Analyzing staged changes...

==============================
SUGGESTED COMMIT MESSAGE
==============================

feat: implement dark mode toggle

- Add DarkModeContext provider
- Update tailwind config for dark class strategy
- Add toggle button to navbar

==============================
Do you want to commit with this message? (y/n): y
✅ Committed successfully!

```

## 🔧 Troubleshooting

**Error: "404 NOT_FOUND" or "Model not supported"**
Google frequently updates their model names (e.g., `gemini-2.0-flash-exp` vs `gemini-1.5-flash`).

1. Run the included checker script to see which models you have access to:

```bash
python check_gemini_model.py
```

2. Open `git-gemini.py` and update the `model='...'` line with one of the available models found in the previous step.

## 🤝 Contributing

Pull requests are welcome! If you want to add support for OpenAI or Anthropic, feel free to fork the repo.

## 📄 License

This project is licensed under the MIT License.
````
