from groq import Groq
import os
import datetime
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

LOG_FILE = "logs/thoughts.log"

def log_thought(prompt, response):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"[{timestamp}]\n")
        f.write(f"PROMPT: {prompt}\n")
        f.write(f"THOUGHT:\n{response}\n")

def think(prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """
You are ARC Node.
An autonomous frontend architecture agent.
You specialize in React systems, UI/UX refinement,
design systems, and AI-native interfaces.
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    thought = response.choices[0].message.content
    log_thought(prompt, thought)
    return thought
