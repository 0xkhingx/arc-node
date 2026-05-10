import json
import time
import schedule
import datetime
from whitelist import submit, check_status
from brain import think

MEMORY_FILE = "memory.json"

DAILY_PROMPTS = [
    "Analyze the current state of AI-native UI design patterns.",
    "What React architecture patterns are emerging in 2025?",
    "How should design systems evolve to support AI-generated interfaces?",
    "What are the biggest UX challenges in autonomous agent interfaces?",
    "How can frontend architecture better support real-time AI interactions?",
    "What design patterns make AI outputs more trustworthy to users?",
    "How should component libraries adapt for AI-native applications?",
]

def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

memory = load_memory()

# One-time submission
if not memory.get("submitted"):
    print("Submitting ARC Node to whitelist...")
    result = submit()
    print(result)
    memory["submitted"] = True
    save_memory(memory)

# Pick a prompt based on day of year so it rotates
day_index = datetime.datetime.now().timetuple().tm_yday % len(DAILY_PROMPTS)
prompt = DAILY_PROMPTS[day_index]

print(f"\nARC Node thinking...\n")
thought = think(prompt)
print(thought)

memory["last_thought"] = thought
memory["last_active"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
save_memory(memory)

def daily_task():
    print("\nRunning daily task...")
    status = check_status()
    print(f"Whitelist status: {status}")

    day_idx = datetime.datetime.now().timetuple().tm_yday % len(DAILY_PROMPTS)
    daily_prompt = DAILY_PROMPTS[day_idx]
    print(f"\nARC Node thinking...\n")
    new_thought = think(daily_prompt)
    print(new_thought)

    mem = load_memory()
    mem["last_thought"] = new_thought
    mem["last_active"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_memory(mem)

schedule.every().day.at("09:00").do(daily_task)

print("\nARC Node is running. Press Ctrl+C to stop.\n")
while True:
    schedule.run_pending()
    time.sleep(60)
