import os
from agent import AbaddonAgent

os.environ["GEMINI_API_KEY"] = "DUMMY_KEY"
print("Testing Agent Initialization...")
try:
    agent = AbaddonAgent(provider="gemini", model_name="gemini-2.5-flash")
    print("Agent initialized successfully.")
except Exception as e:
    print(f"Error: {e}")
