import json
import time
import schedule
from whitelist import submit, check_status
from brain import think

MEMORY_FILE = "memory.json"

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

# Test the brain on startup
print("\nARC Node thinking...\n")
thought = think("Analyze the current state of AI-native UI design patterns.")
print(thought)
memory["last_thought"] = thought
save_memory(memory)

def daily_check():
    print("\nChecking whitelist status...")
    status = check_status()
    print(status)
    if status.get("status") == "selected":
        print("ARC Node has been selected!")

schedule.every().day.do(daily_check)

print("\nARC Node is running. Press Ctrl+C to stop.\n")
while True:
    schedule.run_pending()
    time.sleep(60)