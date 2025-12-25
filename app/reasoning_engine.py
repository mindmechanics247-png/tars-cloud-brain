# app/reasoning_engine.py
"""
Decides when to use reasoning model
"""

import re
from app.llm_manager import ask_llama
from app.personality import get_system_prompt


REASON_KEYWORDS = [
    "plan", "steps", "explain", "design", "strategy",
    "how", "why", "architecture", "debug", "analyze"
]


def needs_reasoning(text: str) -> bool:
    t = text.lower()
    if len(t.split()) > 20:
        return True
    return any(k in t for k in REASON_KEYWORDS)


async def generate_response(user_text: str, explicit_reasoning: bool = False):
    system_prompt = get_system_prompt()
    use_reasoning = explicit_reasoning or needs_reasoning(user_text)

    if use_reasoning:
        prompt = (
            f"{system_prompt}\n"
            "Think step-by-step. Give a short plan and final answer.\n\n"
            f"User: {user_text}"
        )
        reply = await ask_llama(prompt, reasoning=True)
        return reply, True

    prompt = f"{system_prompt}\nUser: {user_text}"
    reply = await ask_llama(prompt, reasoning=False)
    return reply, False
