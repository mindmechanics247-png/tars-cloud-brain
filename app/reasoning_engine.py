"""
reasoning_engine.py
Decides when to use reasoning model and prepares prompts.
Heuristics:
 - explicit trigger phrases (e.g. "enable reasoning", "think step-by-step", "plan", "reason")
 - question complexity (length, presence of keywords)
 - user flag use_reasoning in API
"""

import re
from typing import Tuple
from app.llm_manager import ask_gemini
from app.personality import get_system_prompt

# Keywords strongly indicating a reasoning call
REASON_KEYWORDS = [
    "plan", "steps", "step-by-step", "strategy", "design", "implement", "how to",
    "explain", "why", "reason", "solve", "debug", "optimize", "proposal", "roadmap",
    "detailed", "architect", "architecture", "multi-step", "task list"
]

TRIGGER_PHRASES = [
    "enable reasoning", "reasoning mode", "think step-by-step", "use reasoning",
    "activate brain", "brain mode"
]

def needs_reasoning_auto(text: str) -> bool:
    """Heuristic: return True if text likely needs reasoning."""
    t = text.lower()
    # explicit trigger phrase
    for p in TRIGGER_PHRASES:
        if p in t:
            return True
    # presence of strong keywords
    for k in REASON_KEYWORDS:
        if k in t:
            return True
    # long queries ( > 80 chars ) often need reasoning
    if len(t) > 120 or len(t.split()) > 20:
        return True
    # numeric/complex tasks: planning, timelines, coding
    if re.search(r"\b(schedule|timeline|milestone|refactor|algorithm|pseudocode|write code|generate code)\b", t):
        return True
    return False

async def generate_response(user_text: str, explicit_reasoning: bool=False) -> Tuple[str, bool]:
    """
    Returns (reply_text, used_reasoning_bool).
    If explicit_reasoning True, force reasoning model.
    """
    system_prompt = get_system_prompt()
    use_reasoning = explicit_reasoning or needs_reasoning_auto(user_text)

    # Build prompt with system + user + tool hints
    if use_reasoning:
        prompt = (
            f"{system_prompt}\nYou are the reasoning brain of TARS. "
            "Break down the user's request into clear steps, choose which tools to call (if needed), and provide a plan + final answer.\n\n"
            f"User: {user_text}\n\nProvide step-by-step plan and final result. Be explicit about which tools you'd call."
        )
        reply = await ask_gemini(prompt, reasoning=True)
        return reply, True

    # standard quick reply
    prompt = f"{system_prompt}\nUser: {user_text}\nAnswer concisely and clearly."
    reply = await ask_gemini(prompt, reasoning=False)
    return reply, False
