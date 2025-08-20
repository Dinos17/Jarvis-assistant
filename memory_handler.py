import os
import json

MEMORY_FILE = "memory.json"

def load_memory():
    """Load memory from file or initialize."""
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                data = json.load(f)
                if "chat_history" not in data:
                    data["chat_history"] = []
                return data
        except:
            pass
    return {"chat_history": []}

def save_memory(memory):
    """Persist memory to JSON file."""
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)
