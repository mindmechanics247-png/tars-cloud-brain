# agent/memory_manager.py
"""
memory_manager.py
Simple file-backed memory manager for the agent.
- add(role, text)
- recall_recent(n)
- search_memory(keyword)
"""

import json
import os
from datetime import datetime
from typing import List, Dict

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
MEMORY_FILE = os.path.join(DATA_DIR, "agent_memory.json")
MAX_DEFAULT = int(os.getenv("MAX_MEMORY_ITEMS", "500"))

def _ensure():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump({"memory": []}, f, indent=2)

class MemoryManager:
    def __init__(self, max_items: int = MAX_DEFAULT):
        _ensure()
        self.max = max_items

    def _load(self) -> Dict:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self, data: Dict):
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def add(self, role: str, text: str, meta: Dict = None) -> bool:
        """
        Add a memory item, avoid exact duplicate consecutive entries.
        Returns True if added, False if skipped.
        """
        meta = meta or {}
        data = self._load()
        mem = data.get("memory", [])
        item = {"role": role, "text": text, "meta": meta, "ts": datetime.utcnow().isoformat()}
        # avoid immediate dup
        if len(mem) and mem[-1].get("text") == text and mem[-1].get("role") == role:
            return False
        mem.append(item)
        # trim
        if len(mem) > self.max:
            mem = mem[-self.max:]
        data["memory"] = mem
        self._save(data)
        return True

    def recall_recent(self, n: int = 10) -> List[Dict]:
        data = self._load()
        mem = data.get("memory", [])
        return mem[-n:]

    def search(self, keyword: str, limit: int = 10) -> List[Dict]:
        data = self._load()
        mem = data.get("memory", [])
        res = [m for m in mem if keyword.lower() in m.get("text","").lower()]
        return res[-limit:]
