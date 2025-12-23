import json
import os
from datetime import datetime
from app.config import MAX_MEMORY

MEMORY_FILE = "data/conversation_memory.json"

def _ensure_file():
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump({"memory": [], "conversations": []}, f, indent=2)

def load_memory():
    _ensure_file()
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memory_item(item: dict):
    """Saves a unique memory item; avoids duplicates by string match."""
    _ensure_file()
    data = load_memory()
    mem = data.get("memory", [])
    # simple dedupe: check if item text already present
    txt = item.get("text", "")
    if any(txt == m.get("text", "") for m in mem):
        return False
    mem.append({"text": txt, "meta": item.get("meta", {}), "ts": datetime.utcnow().isoformat()})
    # trim
    if len(mem) > MAX_MEMORY:
        mem = mem[-MAX_MEMORY:]
    data["memory"] = mem
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return True

def append_conversation(turn: dict):
    """Adds a chat turn to conversation list (stores sequence), avoids repeated identical duplicates"""
    _ensure_file()
    data = load_memory()
    conv = data.get("conversations", [])
    # avoid exact duplicate last
    if len(conv) and conv[-1].get("text") == turn.get("text"):
        return False
    conv.append({"role": turn.get("role"), "text": turn.get("text"), "ts": datetime.utcnow().isoformat()})
    if len(conv) > MAX_MEMORY * 2:
        conv = conv[-(MAX_MEMORY*2):]
    data["conversations"] = conv
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return True
