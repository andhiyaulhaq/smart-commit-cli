#!/usr/bin/env python
import subprocess
import os
import sys
import time  # <--- Added for sleep functionality
from google import genai

# Configuration
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("Error: GEMINI_API_KEY environment variable not set.")
    sys.exit(1)

# Initialize the new Client
client = genai.Client(api_key=API_KEY)

def get_staged_diff():
    """Runs git diff --cached to get staged changes."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        print("Error: Not a git repository or git command failed.")
        sys.exit(1)

def generate_commit_message(diff):
    """Sends the diff to Gemini and asks for a commit message with retry logic."""
    prompt = f"""
    You are an expert developer. precise and concise.
    Analyze the following 'git diff' output and generate a commit message.

    Rules:
    1. Use the Conventional Commits format (e.g., 'feat:', 'fix:', 'chore:', 'refactor:').
    2. The first line should be under 50 characters.
    3. If necessary, add a bulleted body description.
    4. Output ONLY the commit message. Do not output markdown code blocks.

    Git Diff:
    {diff}
    """

    # Retry Configuration
    max_retries = 3
    base_delay = 2  # Start waiting 2 seconds

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-3-flash-preview',
                contents=prompt
            )
            return response.text.strip()

        except Exception as e:
            error_str = str(e)
            # Check for Overloaded (503) or Rate Limit (429) errors
            if "503" in error_str or "429" in error_str:
                if attempt < max_retries - 1:
                    sleep_time = base_delay * (2 ** attempt) # 2s, 4s, 8s...
                    print(f"⚠️  Model overloaded. Retrying in {sleep_time}s... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(sleep_time)
                    continue

            # If it's not a retriable error, or we ran out of retries, return the error
            return f"Error communicating with Gemini: {e}"

def main():
    diff = get_staged_diff()

    if not diff:
        print("No staged changes found. Did you run 'git add'?")
        sys.exit(0)

    if len(diff) > 30000:
        print("Warning: Diff is very large, truncating sent data...")
        diff = diff[:30000]

    print("Analyzing staged changes...")
    message = generate_commit_message(diff)

    print("\n" + "="*30)
    print("SUGGESTED COMMIT MESSAGE")
    print("="*30 + "\n")
    print(message)
    print("\n" + "="*30)

    # Added check: Don't ask to commit if there was an API error
    if message.startswith("Error communicating"):
        print("❌ Could not generate message due to API error.")
        sys.exit(1)

    choice = input("Do you want to commit with this message? (y/n): ")
    if choice.lower() == 'y':
        subprocess.run(["git", "commit", "-m", message])
        print("✅ Committed successfully!")
    else:
        print("❌ Commit aborted.")

if __name__ == "__main__":
    main()
