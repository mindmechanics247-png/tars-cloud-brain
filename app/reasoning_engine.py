"""
reasoning_engine.py
Decides when to use reasoning model and prepares prompts.
"""

import re
from typing import Tuple
from app.llm_manager import ask_gemini
from app.personality import get_system_prompt

# ----------------------------
# Reasoning indicators
# ----------------------------
REASON_KEYWORDS = [
    "plan", "steps", "step-by-step", "strategy", "design", "implement",
    "explain", "why", "reason", "solve", "debug", "optimize",
    "proposal", "roadmap", "architecture", "multi-step",
    "timeline", "algorithm", "pseudocode", "write code"
]

TRIGGER_PHRASES = [
    "enable reasoning",
    "reasoning mode",
    "think step-by-step",
    "use reasoning",
    "activate brain",
    "brain mode"
]

# ----------------------------
# Heuristic decision
# ----------------------------
def needs_reasoning_auto(text: str) -> bool:
    """
    Decide automatically whether reasoning is required.
    """
    t = text.lower()

    # Explicit triggers
    if any(p in t for p in TRIGGER_PHRASES):
        return True

    # Strong reasoning keywords
    if any(k in t for k in REASON_KEYWORDS):
        return True

    # Long / complex input
    if len(t.split()) > 20 or len(t) > 120:
        return True

    return False


# ----------------------------
# Main response generator
# ----------------------------
async def generate_response(
    user_text: str,
    explicit_reasoning: bool = False
) -> Tuple[str, bool]:
    """
    Returns:
        (reply_text, used_reasoning)
    """

    system_prompt = get_system_prompt()

    use_reasoning = explicit_reasoning or needs_reasoning_auto(user_text)

    if use_reasoning:
        prompt = f"""
{system_prompt}

You are TARS's reasoning brain.
Think step-by-step internally.
If tools are useful, mention which tool you'd use (do NOT hallucinate results).
Then provide the final clear answer.

User request:
{user_text}
"""
        reply = await ask_gemini(prompt, reasoning=True)
        return reply, True

    # Fast / standard response
    prompt = f"""
{system_prompt}

User:
{user_text}

Respond clearly, confidently, and concisely.
"""
    reply = await ask_gemini(prompt, reasoning=False)
    return reply, False
