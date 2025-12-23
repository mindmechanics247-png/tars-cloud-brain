# agent/memory/mem0_manager.py

import os
from mem0 import MemoryClient

class Mem0Manager:
    """
    Persistent long-term memory manager using Mem0.
    Stores and retrieves important user/assistant memories.
    """

    def __init__(self):
        api_key = os.getenv("MEM0_API_KEY")
        if not api_key:
            raise ValueError("MEM0_API_KEY not found in environment")

        self.client = MemoryClient(api_key=api_key)

    async def fetch_user_memory(self, user_id: str) -> str:
        """
        Fetch all stored memories for a user and format them
        for LLM prompt injection.
        """
        try:
            memories = await self.client.get_all(user_id=user_id)

            if not memories:
                return "No previous user history."

            memory_text = "\n".join(
                m.get("memory", "") or m.get("text", "")
                for m in memories
            )

            return f"KNOWN USER HISTORY:\n{memory_text}"

        except Exception as e:
            return f"(Memory system unavailable: {e})"

    async def save_memory(self, user_id: str, role: str, content: str):
        """
        Save a new memory intelligently.
        Mem0 automatically avoids duplicates.
        """
        try:
            await self.client.add(
                user_id=user_id,
                memory=f"{role}: {content}"
            )
        except Exception as e:
            print("Mem0 save error:", e)
