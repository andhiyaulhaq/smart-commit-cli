from google import genai
import os

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
print("Checking available models...")
for m in client.models.list():
    if "flash" in m.name:
        print(f"Found: {m.name}")
